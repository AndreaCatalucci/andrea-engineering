import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install-grok-plugin"


class InstallGrokPluginTest(unittest.TestCase):
    def make_fake_grok(self, directory):
        executable_directory = Path(directory) / "fake cli"
        executable_directory.mkdir()
        path = executable_directory / "grok"
        path.write_text(
            textwrap.dedent(
                """\
                #!/usr/bin/env bash
                set -euo pipefail

                printf '%s\\n' "$*" >> "$FAKE_GROK_LOG"

                case "$*" in
                  "plugin list --json")
                    if [[ -f "$FAKE_PLUGIN_STATE" || "${FAKE_PLUGIN_PRESENT:-0}" == "1" ]]; then
                      printf '[{"name":"andrea-engineering","enabled":%s}]\\n' "${FAKE_PLUGIN_ENABLED:-true}"
                    else
                      printf '[]\\n'
                    fi
                    ;;
                  "plugin marketplace list --json")
                    if [[ "${FAKE_MARKETPLACE_PRESENT:-0}" == "1" ]]; then
                      printf '[{"name":"andrea-engineering","kind":"local","source":{"path":"%s"}}]\\n' "$FAKE_MARKETPLACE_ROOT"
                    else
                      printf '[]\\n'
                    fi
                    ;;
                  "plugin marketplace add "*)
                    [[ "${FAKE_FAIL_MUTATIONS:-0}" != "1" ]]
                    printf '{"name":"andrea-engineering"}\\n'
                    ;;
                  "plugin install "*" --trust")
                    [[ "${FAKE_FAIL_MUTATIONS:-0}" != "1" ]]
                    printf 'installed' > "$FAKE_PLUGIN_STATE"
                    printf '{"name":"andrea-engineering"}\\n'
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
        fake_grok,
        *arguments,
        plugin_present=False,
        plugin_enabled=True,
        marketplace_root=None,
    ):
        log_path = fake_grok.parent / "commands.log"
        state_path = fake_grok.parent / "plugin-installed"
        environment = os.environ.copy()
        environment.update(
            {
                "GROK_PLUGIN_CLI": str(fake_grok),
                "FAKE_GROK_LOG": str(log_path),
                "FAKE_PLUGIN_STATE": str(state_path),
                "FAKE_PLUGIN_PRESENT": "1" if plugin_present else "0",
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

    def test_dry_run_does_not_launch_grok(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_grok = self.make_fake_grok(directory)
            result, commands = self.run_installer(
                fake_grok, "--dry-run", plugin_present=True
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(commands, [])
        self.assertIn("plugin marketplace add", result.stdout)
        self.assertIn("plugin install", result.stdout)
        self.assertIn("--trust", result.stdout)
        self.assertIn("Grok Build was not launched or changed", result.stdout)

    def test_registers_checkout_when_no_marketplace_matches(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_grok = self.make_fake_grok(directory)
            result, commands = self.run_installer(fake_grok)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            any(command.startswith("plugin marketplace add ") for command in commands)
        )
        self.assertTrue(
            any(command.startswith("plugin install ") and command.endswith(" --trust") for command in commands)
        )

    def test_reuses_marketplace_pointing_at_this_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_grok = self.make_fake_grok(directory)
            result, commands = self.run_installer(
                fake_grok,
                marketplace_root=ROOT,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(
            any(command.startswith("plugin marketplace add ") for command in commands)
        )
        self.assertTrue(
            any(command.startswith("plugin install ") and command.endswith(" --trust") for command in commands)
        )

    def test_refuses_to_replace_a_same_name_marketplace(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_grok = self.make_fake_grok(directory)
            result, commands = self.run_installer(
                fake_grok,
                marketplace_root=Path(directory) / "different checkout",
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Refusing to replace it", result.stderr)
        self.assertFalse(any(command.startswith("plugin install ") for command in commands))

    def test_refresh_verifies_the_plugin_is_enabled(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_grok = self.make_fake_grok(directory)
            result, _ = self.run_installer(fake_grok, plugin_present=True)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Installed and enabled", result.stdout)

    def test_refresh_fails_when_plugin_remains_disabled(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_grok = self.make_fake_grok(directory)
            result, _ = self.run_installer(
                fake_grok,
                plugin_present=True,
                plugin_enabled=False,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("installed and enabled", result.stderr)


if __name__ == "__main__":
    unittest.main()
