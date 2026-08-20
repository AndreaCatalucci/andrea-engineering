# Andrea Engineering

Eight engineering skills for Codex, Claude Code, and Grok Build.

| Skill | Purpose |
|---|---|
| `ae-ideate` | A problem with no solution yet. Generate ideas. |
| `ae-explore` | A solution direction. Explore how it could work. |
| `ae-plan` | Problem and solution are settled enough. See how it lands in this codebase. |
| `ae-work` | Implement a request or plan. |
| `ae-debug` | Find and fix the cause of failing behavior. |
| `ae-review` | Report material problems in code or another artifact. |
| `ae-ship` | Commit, push, open or update PRs, and monitor them. |
| `ae-learn` | Capture a lesson when the trajectory changes, or garden existing ones. |

Reach for the skill that matches the current question. A problem with no solution starts at `ae-ideate`. A solution direction to open up starts at `ae-explore`. A settled solution starts at `ae-plan`. A trivial change can start at `ae-work`. An exploration that ends in no still leaves an Opportunity Brief.

Each `SKILL.md` contains the complete default workflow. Branch-specific behavior lives in a simple `recipes/` file and loads when the request matches it.

## Install this checkout

Install via [`npx skills`](https://www.npmjs.com/package/skills):

```bash
npx skills add AndreaCatalucci/andrea-engineering
```

Restart the agent or begin a new session after refreshing. Existing sessions keep skills already loaded into their context.

## Use

Codex uses `$skill-name`; Claude Code and Grok Build use `/skill-name` or `/andrea-engineering:skill-name`.

```text
$ae-work add a timeout to the retry helper
$ae-explore this solution
$ae-ideate is this worth doing
$ae-plan slice the leading concept
$ae-debug find this regression
$ae-review review the current diff
$ae-ship open a PR
$ae-learn capture what we learned
$ae-learn garden authentication
```

Natural language controls optional behavior. For example, asking `ae-work` for autonomous delivery loads its autonomous recipe; asking `ae-review` to inspect a web flow loads its browser recipe.

## Change a skill

Edit its `skills/<name>/SKILL.md`. Keep the entrypoint focused and put branch-specific behavior in one plainly named file under `recipes/`.

Plugin metadata lives under `.codex-plugin/`, `.claude-plugin/`, `.grok-plugin/`, and `.agents/plugins/`.

## License

MIT. See [LICENSE](LICENSE).
