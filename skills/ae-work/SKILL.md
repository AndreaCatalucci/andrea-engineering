---
name: ae-work
description: Implement a concrete request or plan. Use for building or changing code; use ae-debug when the main problem is discovering why something fails.
---

# Work

Implement the requested outcome with the least process that keeps the change sound.

1. Read the request or plan and inspect the affected code. Preserve unrelated user changes.
2. If a missing product decision would materially change the result, ask. Otherwise make the smallest reasonable assumption and state it briefly.
3. Implement the complete requested behavior using existing patterns. Remove complexity when that is simpler than extending it.
4. When architecture changes, update or create every affected current-state C4 artifact under `docs/architecture/`. Each view is one Markdown file with its scope, verification basis at a named implementation revision, and one Mermaid block. The basis names inspected code, configuration, or checks.
5. Run existing checks directly relevant to the changed behavior and architecture artifacts.
6. If an Implementation Plan (from `ae-plan`, under `docs/plans/`) guided this work, mark the slices or done criteria just completed as done and record the architecture result.
7. Report what changed, what was checked, which architecture artifacts changed, and any real limitation.
8. Run ae-review on the changes. Skip only trivial changes.

The user's request defines which adjacent actions—planning, review, browser work, and Git operations—join implementation. A trajectory change is a lesson.

Load at most one matching file from `recipes/` before acting:

- [`autonomous.md`](recipes/autonomous.md) for explicitly hands-off delivery;
- [`optimize.md`](recipes/optimize.md) for measurable improvement;
- [`simplify.md`](recipes/simplify.md) for behavior-preserving cleanup;
- [`polish.md`](recipes/polish.md) for interactive UI refinement;
- [`dogfood.md`](recipes/dogfood.md) for real-flow product use;
- [`worktree.md`](recipes/worktree.md) for isolation.

Load another recipe only when the request actually crosses that boundary.
