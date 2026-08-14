# Andrea Engineering

Andrea Engineering is a personal fork of the Compound Engineering skill suite. It packages 30 `ae-*` workflows for strategy, ideation, planning, implementation, debugging, review, shipping, browser testing, and durable project learnings.

The same skill tree is packaged for **Codex**, **Claude Code**, and **Grok Build**. Each host discovers the plugin through its own marketplace and plugin manifest.

## Install this checkout

One command installs or refreshes the plugin for every supported CLI on your `PATH`:

```bash
scripts/install
```

Limit the install, or preview it without changing anything:

```bash
scripts/install --codex --claude --grok
scripts/install --dry-run
```

Each host also has a dedicated installer. Restart that agent, or start a new session, after installation. Existing sessions keep the skills they loaded when they started.

### Codex

```bash
scripts/install-codex-plugin
scripts/install-codex-plugin --dry-run
```

From Git:

```bash
codex plugin marketplace add AndreaCatalucci/andrea-engineering --ref main
codex plugin add andrea-engineering@andrea-engineering
codex plugin list
```

Refresh:

```bash
codex plugin marketplace upgrade andrea-engineering
codex plugin add andrea-engineering@andrea-engineering
```

Remove:

```bash
codex plugin remove andrea-engineering@andrea-engineering
```

Codex Desktop and Codex CLI share one user plugin install. The IDE extension does not currently support plugins.

### Claude Code

```bash
scripts/install-claude-plugin
scripts/install-claude-plugin --dry-run
```

From Git:

```bash
claude plugin marketplace add AndreaCatalucci/andrea-engineering
claude plugin install andrea-engineering@andrea-engineering
claude plugin list
```

Refresh:

```bash
claude plugin marketplace update andrea-engineering
claude plugin update andrea-engineering@andrea-engineering
```

Remove:

```bash
claude plugin uninstall andrea-engineering@andrea-engineering
```

If the install summary asks you to reload, run `/reload-plugins`.

### Grok Build

```bash
scripts/install-grok-plugin
scripts/install-grok-plugin --dry-run
```

From Git:

```bash
grok plugin marketplace add AndreaCatalucci/andrea-engineering
grok plugin install andrea-engineering --trust
grok plugin list
```

Refresh:

```bash
grok plugin marketplace update andrea-engineering
grok plugin update andrea-engineering
```

Remove:

```bash
grok plugin uninstall andrea-engineering --confirm
```

Reload plugins with `r` in the Plugins tab, or start a new session.

## Use

Invoke a workflow by name. Codex uses `$skill-name`. Claude Code and Grok Build use `/skill-name`, or `/andrea-engineering:skill-name` when the plugin namespace is required.

```text
$ae-brainstorm shape this feature idea
$ae-plan create an implementation plan
$ae-work execute the plan
$ae-code-review review the current changes
$lfg ship this request end to end
```

```text
/ae-brainstorm shape this feature idea
/ae-plan create an implementation plan
/ae-work execute the plan
/ae-code-review review the current changes
/lfg ship this request end to end
```

Each skill's `SKILL.md` defines its trigger and workflow. Skill directories are named `ae-*` (plus `lfg`). Manifests live at:

- [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json)
- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) and [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
- [`.grok-plugin/plugin.json`](.grok-plugin/plugin.json) and [`.grok-plugin/marketplace.json`](.grok-plugin/marketplace.json)

## Development

Shared skill assets have one canonical source and generated mirrors. This
includes the Codex interaction rules used by document-producing skills.
After changing a shared asset, regenerate the mirrors:

```bash
scripts/sync-shared-skill-assets
```

Verify that committed mirrors are current with:

```bash
scripts/sync-shared-skill-assets --check
```

Validate host packages with:

```bash
claude plugin validate .
grok plugin validate .
```

## License

MIT. See [LICENSE](LICENSE).
