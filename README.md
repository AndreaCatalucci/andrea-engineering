# Andrea Engineering

Nine engineering skills for Codex, Claude Code, and Grok Build.

| Skill | Purpose |
|---|---|
| `ae-ideate` | A problem with no solution yet. Generate ideas. |
| `ae-explore` | A solution direction. Explore how it could work. |
| `ae-plan` | Problem and solution are settled enough. See how it lands in this codebase. |
| `ae-coordinate` | Coordinate a large delivery across focused agent chats. |
| `ae-work` | Implement a request or plan. |
| `ae-debug` | Find and fix the cause of failing behavior. |
| `ae-review` | Report material problems in code or another artifact using independent reviewers. |
| `ae-ship` | Commit, push, open or update PRs, and monitor them. |
| `ae-learn` | Capture a lesson when the trajectory changes, or garden existing ones. |

Reach for the skill that matches the current question. A problem with no solution starts at `ae-ideate`. A solution direction to open up starts at `ae-explore`. A settled solution starts at `ae-plan`, which writes an Implementation Plan under `docs/plans/`. A trivial change can start at `ae-work`.

Invoke `ae-coordinate` explicitly for a large delivery. It turns user-defined scope and available Implementation Plans into a Delivery Map under `docs/delivery-maps/`. The coordinator keeps end-to-end behaviors, invariants, architecture, evidence, and implementation gaps current. It returns copyable `ae-plan`, `ae-explore`, and `ae-work` prompts; the user starts those chats and brings their reports back. One chat may cover part of one plan or cohesive slices from several plans.

Verified current architecture lives as Mermaid C4 views under `docs/architecture/`, one Markdown file per view. Implementation Plans reference the starting views and describe their intended architecture delta. `ae-work` updates affected views with the implementation; `ae-coordinate` closes delivery only after the diagrams, code, plans, and evidence agree.

Each `SKILL.md` contains the complete default workflow. Branch-specific behavior lives in a simple `recipes/` file and loads when the request matches it.

## Install this checkout

Install via [`npx skills`](https://www.npmjs.com/package/skills):

```bash
npx skills add AndreaCatalucci/andrea-engineering
```

Restart the agent or begin a new session after refreshing. Existing sessions keep skills already loaded into their context.

## Use

Codex uses `$skill-name`; Claude Code and Grok Build use `/skill-name`.

```text
$ae-work add a timeout to the retry helper
$ae-explore this solution
$ae-ideate is this worth doing
$ae-plan slice the leading concept
$ae-coordinate coordinate these implementation plans
$ae-debug find this regression
$ae-review review the current diff
$ae-ship open a PR
$ae-learn capture what we learned
$ae-learn garden authentication
```

Natural language controls optional behavior. For example, asking `ae-work` for autonomous delivery loads its autonomous recipe; asking `ae-review` to inspect a web flow loads its browser recipe.

## Change a skill

Edit its `skills/<name>/SKILL.md`. Keep the entrypoint focused and put branch-specific behavior in one plainly named file under `recipes/`.

## License

MIT. See [LICENSE](LICENSE).
