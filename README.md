# Andrea Engineering

Nine engineering skills for Codex, Claude Code, and Grok Build.

| Skill | Purpose |
|---|---|
| `ae-ideate` | Understand demand and alternatives; recommend which product idea to pursue or test. |
| `ae-explore` | A solution direction. Explore how it could work. |
| `ae-plan` | Problem and solution are settled enough. See how it lands in this codebase. |
| `ae-coordinate` | Track delivery state and delegate work with prompts and model recommendations. |
| `ae-work` | Implement a request or plan. |
| `ae-debug` | Find and fix the cause of failing behavior. |
| `ae-review` | Report material problems; use independent perspectives when requested or useful. |
| `ae-ship` | Commit, push, open or update PRs, and monitor them. |
| `ae-learn` | Capture a lesson when the trajectory changes, or garden existing ones. |

Reach for the skill that matches the current question. A problem with no solution starts at `ae-ideate`. A solution direction to open up starts at `ae-explore`. A settled solution starts at `ae-plan`, which writes an Implementation Plan under `docs/plans/`. A trivial change can start at `ae-work`.

Use only stages that advance the current decision. `ae-explore` includes bounded runnable experiments for prototypes; the catalog has no dependency on an external prototype skill. `ae-work` verifies changed acceptance behavior with existing coverage or the smallest meaningful additional check. `ae-ship` handles Git and PR work; deployment belongs to the user.

`ae-ideate` starts with the user's problem and current alternatives, including competitors and manual work. Impact Mapping connects the desired outcome to behavior changes and ideas. Wardley Mapping helps decide what deserves custom work and what to reuse or buy. The result is a recommendation, a first useful scope, and a next action with a decision criterion.

Invoke `ae-coordinate` explicitly for a large delivery. It turns user-defined scope and available Implementation Plans into a Delivery Map under `docs/delivery-maps/`. The coordinator advances through reconcile, ready, approval, waiting, blocked, and complete states. Ready work receives a complete copyable execution prompt, followed by a preview of the project, local checkout or worktree, starting code, model, and reasoning effort. It proactively asks to create that chat programmatically and waits for explicit approval of the preview. Returned reports are verified before dependent work advances.

Each chat needs its own approved preview; general autonomy does not authorize future chat creation. The user can also launch manually or defer. One chat may cover part of one plan or cohesive slices from several plans. The coordinator preserves packet IDs and presents newly unlocked prompts in the same response that reconciles their prerequisites.

Model recommendations favor the least expensive option likely to meet the acceptance criteria, accounting for retries and rework. A premium model needs a task-specific reason. Model and reasoning effort are chosen separately from the host's available settings.

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
