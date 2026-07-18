# Andrea Engineering

Andrea Engineering is a personal, Codex-native fork of the Compound Engineering skill suite. It packages 30 workflows for strategy, ideation, planning, implementation, debugging, review, shipping, browser testing, and durable project learnings.

## Codex only

This plugin targets Codex directly. Its skills assume Codex conventions and capabilities, including:

- `$skill-name` invocation;
- `AGENTS.md` for repository instructions;
- Codex subagents through `spawn_agent`;
- persistent commands through `exec_command` and `write_stdin`;
- the Codex in-app browser for browser workflows; and
- Codex interaction, approval, sandbox, and automation behavior.

There are deliberately no compatibility adapters for Claude Code, Cursor, Gemini, or other coding-agent harnesses. Portability should be implemented as a separate fork rather than by adding conditional branches back into these skills.

## Install from Git

Prerequisites: Git and a current Codex CLI installation.

1. Add this repository as a Codex plugin marketplace:

   ```bash
   codex plugin marketplace add AndreaCatalucci/andrea-engineering --ref main
   ```

2. Install the plugin from that marketplace:

   ```bash
   codex plugin add andrea-engineering@andrea-engineering
   ```

3. Verify that Codex reports the plugin as installed and enabled:

   ```bash
   codex plugin list
   ```

4. Restart the Codex desktop app, or start a new Codex CLI session, so the installed skills are loaded.

The marketplace follows `main`. To refresh an existing installation after new changes land:

```bash
codex plugin marketplace upgrade andrea-engineering
codex plugin add andrea-engineering@andrea-engineering
```

Restart the Codex desktop app, or start a new CLI session, after upgrading.

To remove the plugin:

```bash
codex plugin remove andrea-engineering@andrea-engineering
```

## Use

Invoke a workflow by name in a Codex prompt, for example:

```text
$ce-brainstorm shape this feature idea
$ce-plan create an implementation plan
$ce-work execute the plan
$ce-code-review review the current changes
$lfg ship this request end to end
```

Each skill's `SKILL.md` defines its trigger and workflow. The plugin manifest is at [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json).

## Development

Shared skill assets have one canonical source and generated mirrors. This
includes the Codex interaction rules and the plain-language rules used by
document-producing skills. After changing a shared asset, regenerate the
mirrors:

```bash
scripts/sync-shared-skill-assets
```

Verify that committed mirrors are current with:

```bash
scripts/sync-shared-skill-assets --check
```

## License

MIT. See [LICENSE](LICENSE).
