import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install-codex-plugin"


class InstallCodexPluginTest(unittest.TestCase):
    def make_fake_codex(self, directory):
        executable_directory = Path(directory) / "fake cli"
        executable_directory.mkdir()
        path = executable_directory / "codex"
        path.write_text(
            textwrap.dedent(
                """\
                #!/usr/bin/env bash
                set -euo pipefail

                printf '%s\\n' "$*" >> "$FAKE_CODEX_LOG"

                case "$*" in
                  "plugin list --available --json"|"plugin list --json")
                    if [[ -f "$FAKE_PLUGIN_STATE" || "${FAKE_PLUGIN_PRESENT:-0}" == "1" ]]; then
                      plugin_id="andrea-engineering@personal"
                      if [[ -f "$FAKE_PLUGIN_STATE" ]]; then
                        plugin_id="$(<"$FAKE_PLUGIN_STATE")"
                      fi
                      printf '{"installed":[{"pluginId":"%s","name":"andrea-engineering","installed":true,"enabled":%s,"source":{"source":"local","path":"%s"}}],"available":[]}\\n' "$plugin_id" "${FAKE_PLUGIN_ENABLED:-true}" "$FAKE_PLUGIN_ROOT"
                    elif [[ "${FAKE_PLUGIN_AVAILABLE:-0}" == "1" ]]; then
                      printf '{"installed":[],"available":[{"pluginId":"andrea-engineering@personal","name":"andrea-engineering","installed":false,"enabled":false,"source":{"source":"local","path":"%s"}}]}\\n' "$FAKE_PLUGIN_ROOT"
                    else
                      printf '{"installed":[],"available":[]}\\n'
                    fi
                    ;;
                  "plugin marketplace list --json")
                    if [[ "${FAKE_MARKETPLACE_PRESENT:-0}" == "1" ]]; then
                      printf '{"marketplaces":[{"name":"andrea-engineering","root":"%s"}]}\\n' "$FAKE_MARKETPLACE_ROOT"
                    else
                      printf '{"marketplaces":[]}\\n'
                    fi
                    ;;
                  "plugin marketplace add "*" --json")
                    [[ "${FAKE_FAIL_MUTATIONS:-0}" != "1" ]]
                    printf '{"marketplaceName":"andrea-engineering"}\\n'
                    ;;
                  "plugin add "*" --json")
                    [[ "${FAKE_FAIL_MUTATIONS:-0}" != "1" ]]
                    printf '%s' "$3" > "$FAKE_PLUGIN_STATE"
                    printf '{"pluginId":"andrea-engineering@personal"}\\n'
                    ;;
                  *)
                    printf 'unexpected command: %s\\n' "$*" >&2
                    exit 1
                    ;;
                esac
                """
            ),
            encoding="utf-8",
        )
        path.chmod(0o755)
        return path

    def run_installer(
        self,
        fake_codex,
        *arguments,
        plugin_present=False,
        plugin_available=False,
        plugin_enabled=True,
        marketplace_root=None,
    ):
        log_path = fake_codex.parent / "commands.log"
        state_path = fake_codex.parent / "plugin-installed"
        environment = os.environ.copy()
        environment.update(
            {
                "CODEX_PLUGIN_CLI": str(fake_codex),
                "FAKE_CODEX_LOG": str(log_path),
                "FAKE_PLUGIN_STATE": str(state_path),
                "FAKE_PLUGIN_ROOT": str(ROOT),
                "FAKE_PLUGIN_PRESENT": "1" if plugin_present else "0",
                "FAKE_PLUGIN_AVAILABLE": "1" if plugin_available else "0",
                "FAKE_PLUGIN_ENABLED": "true" if plugin_enabled else "false",
                "FAKE_MARKETPLACE_PRESENT": "1" if marketplace_root else "0",
                "FAKE_MARKETPLACE_ROOT": str(marketplace_root or ROOT),
                "FAKE_FAIL_MUTATIONS": "1" if "--dry-run" in arguments else "0",
            }
        )
        result = subprocess.run(
            [str(INSTALLER), *arguments],
            cwd=ROOT,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        commands = (
            log_path.read_text(encoding="utf-8").splitlines()
            if log_path.exists()
            else []
        )
        return result, commands

    def test_dry_run_does_not_launch_codex(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_codex = self.make_fake_codex(directory)
            result, commands = self.run_installer(
                fake_codex, "--dry-run", plugin_present=True
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(commands, [])
        self.assertIn("plugin list --available --json", result.stdout)
        self.assertIn("andrea-engineering@\\<marketplace\\>", result.stdout)
        self.assertIn("Codex was not launched or changed", result.stdout)

    def test_registers_checkout_when_no_marketplace_matches(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_codex = self.make_fake_codex(directory)
            result, commands = self.run_installer(fake_codex)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            any(command.startswith("plugin marketplace add ") for command in commands)
        )
        self.assertIn(
            "plugin add andrea-engineering@andrea-engineering --json", commands
        )

    def test_reuses_an_uninstalled_plugin_from_this_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_codex = self.make_fake_codex(directory)
            result, commands = self.run_installer(
                fake_codex,
                plugin_available=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "plugin add andrea-engineering@personal --json", commands
        )
        self.assertFalse(any("marketplace list" in command for command in commands))

    def test_refuses_to_replace_a_same_name_marketplace(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_codex = self.make_fake_codex(directory)
            result, commands = self.run_installer(
                fake_codex,
                marketplace_root=Path(directory) / "different checkout",
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Refusing to replace it", result.stderr)
        self.assertFalse(any(command.startswith("plugin add ") for command in commands))

    def test_refresh_verifies_the_plugin_is_enabled(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_codex = self.make_fake_codex(directory)
            result, _ = self.run_installer(fake_codex, plugin_present=True)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Installed and enabled", result.stdout)

    def test_refresh_fails_when_plugin_remains_disabled(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_codex = self.make_fake_codex(directory)
            result, _ = self.run_installer(
                fake_codex,
                plugin_present=True,
                plugin_enabled=False,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("installed and enabled", result.stderr)


if __name__ == "__main__":
    unittest.main()
