import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install-claude-plugin"


class InstallClaudePluginTest(unittest.TestCase):
    def make_fake_claude(self, directory):
        executable_directory = Path(directory) / "fake cli"
        executable_directory.mkdir()
        path = executable_directory / "claude"
        path.write_text(
            textwrap.dedent(
                """\
                #!/usr/bin/env bash
                set -euo pipefail

                printf '%s\\n' "$*" >> "$FAKE_CLAUDE_LOG"

                case "$*" in
                  "plugin list --json")
                    if [[ -f "$FAKE_PLUGIN_STATE" || "${FAKE_PLUGIN_PRESENT:-0}" == "1" ]]; then
                      printf '[{"id":"andrea-engineering@andrea-engineering","enabled":%s}]\\n' "${FAKE_PLUGIN_ENABLED:-true}"
                    else
                      printf '[]\\n'
                    fi
                    ;;
                  "plugin marketplace list --json")
                    if [[ "${FAKE_MARKETPLACE_PRESENT:-0}" == "1" ]]; then
                      printf '[{"name":"andrea-engineering","source":"directory","path":"%s"}]\\n' "$FAKE_MARKETPLACE_ROOT"
                    else
                      printf '[]\\n'
                    fi
                    ;;
                  "plugin marketplace add "*)
                    [[ "${FAKE_FAIL_MUTATIONS:-0}" != "1" ]]
                    printf '{"name":"andrea-engineering"}\\n'
                    ;;
                  "plugin install andrea-engineering@andrea-engineering --scope user")
                    [[ "${FAKE_FAIL_MUTATIONS:-0}" != "1" ]]
                    printf 'installed' > "$FAKE_PLUGIN_STATE"
                    printf '{"id":"andrea-engineering@andrea-engineering"}\\n'
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
        fake_claude,
        *arguments,
        plugin_present=False,
        plugin_enabled=True,
        marketplace_root=None,
    ):
        log_path = fake_claude.parent / "commands.log"
        state_path = fake_claude.parent / "plugin-installed"
        environment = os.environ.copy()
        environment.update(
            {
                "CLAUDE_PLUGIN_CLI": str(fake_claude),
                "FAKE_CLAUDE_LOG": str(log_path),
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

    def test_dry_run_does_not_launch_claude(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_claude = self.make_fake_claude(directory)
            result, commands = self.run_installer(
                fake_claude, "--dry-run", plugin_present=True
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(commands, [])
        self.assertIn("plugin marketplace add", result.stdout)
        self.assertIn(
            "plugin install andrea-engineering@andrea-engineering --scope user",
            result.stdout,
        )
        self.assertIn("Claude Code was not launched or changed", result.stdout)

    def test_registers_checkout_when_no_marketplace_matches(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_claude = self.make_fake_claude(directory)
            result, commands = self.run_installer(fake_claude)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            any(command.startswith("plugin marketplace add ") for command in commands)
        )
        self.assertIn(
            "plugin install andrea-engineering@andrea-engineering --scope user",
            commands,
        )

    def test_reuses_marketplace_pointing_at_this_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_claude = self.make_fake_claude(directory)
            result, commands = self.run_installer(
                fake_claude,
                marketplace_root=ROOT,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(
            any(command.startswith("plugin marketplace add ") for command in commands)
        )
        self.assertIn(
            "plugin install andrea-engineering@andrea-engineering --scope user",
            commands,
        )

    def test_refuses_to_replace_a_same_name_marketplace(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_claude = self.make_fake_claude(directory)
            result, commands = self.run_installer(
                fake_claude,
                marketplace_root=Path(directory) / "different checkout",
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Refusing to replace it", result.stderr)
        self.assertFalse(any(command.startswith("plugin install ") for command in commands))

    def test_refresh_verifies_the_plugin_is_enabled(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_claude = self.make_fake_claude(directory)
            result, _ = self.run_installer(fake_claude, plugin_present=True)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Installed and enabled", result.stdout)

    def test_refresh_fails_when_plugin_remains_disabled(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_claude = self.make_fake_claude(directory)
            result, _ = self.run_installer(
                fake_claude,
                plugin_present=True,
                plugin_enabled=False,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("installed and enabled", result.stderr)


if __name__ == "__main__":
    unittest.main()
