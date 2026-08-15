# Andrea Engineering

Eight small engineering skills for Codex, Claude Code, and Grok Build.

| Skill | Purpose |
|---|---|
| `ae-ideate` | Explore options without asking questions. |
| `ae-brainstorm` | Turn an unclear idea into confirmed requirements. |
| `ae-plan` | Write the shortest useful implementation plan. |
| `ae-work` | Implement a request or plan. |
| `ae-debug` | Find and fix the cause of failing behavior. |
| `ae-review` | Report material problems in code or another artifact. |
| `ae-ship` | Commit, push, open or update PRs, and monitor them. |
| `ae-learn` | Capture one reusable lesson or explicitly garden existing ones. |

Each `SKILL.md` contains the complete default workflow. Optional behavior lives in a short `recipes/` file and is loaded only when requested. There are no compatibility aliases or shared workflow framework.

## Install this checkout

Install or refresh every supported CLI on your `PATH`:

```bash
scripts/install
```

Limit the hosts or preview commands:

```bash
scripts/install --codex --claude --grok
scripts/install --dry-run
```

Dedicated installers are also available:

```bash
scripts/install-codex-plugin
scripts/install-claude-plugin
scripts/install-grok-plugin
```

Restart the agent or begin a new session after refreshing. Existing sessions keep skills already loaded into their context.

## Use

Codex uses `$skill-name`; Claude Code and Grok Build use `/skill-name` or `/andrea-engineering:skill-name`.

```text
$ae-ideate ways to simplify this feature
$ae-brainstorm help me define this idea
$ae-plan plan the confirmed change
$ae-work perform the plan
$ae-debug find this regression
$ae-review review the current diff
$ae-ship open a PR
$ae-learn capture what we learned
$ae-learn garden authentication
```

Natural language controls optional behavior. For example, asking `ae-work` for autonomous delivery loads its autonomous recipe; asking `ae-review` to inspect a web flow loads its browser recipe.

## Change a skill

Edit its `skills/<name>/SKILL.md`. Keep the entrypoint short and put optional behavior in one plainly named file under `recipes/`. Avoid adding shared abstractions, schemas, validators, or generated copies.

Plugin metadata lives under `.codex-plugin/`, `.claude-plugin/`, `.grok-plugin/`, and `.agents/plugins/`.

## License

MIT. See [LICENSE](LICENSE).
