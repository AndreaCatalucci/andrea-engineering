---
name: ae-work
description: Implement a concrete request or plan end to end. Use for building or changing code; use ae-debug when the main problem is discovering why something fails.
---

# Work

Implement the requested outcome with the least process that keeps the change sound.

1. Read the request or plan and inspect the affected code. Preserve unrelated user changes.
2. If a missing product decision would materially change the result, ask. Otherwise make the smallest reasonable assumption and state it briefly.
3. Implement the complete requested behavior using existing patterns. Remove complexity when that is simpler than extending it.
4. Run existing checks directly relevant to the changed behavior.
5. Report what changed, what was checked, and any real limitation.

The user's request defines which adjacent actions—planning, review, browser work, learning, and Git operations—join implementation.

Load at most one matching file from `recipes/` before acting:

- [`autonomous.md`](recipes/autonomous.md) for explicitly hands-off delivery;
- [`optimize.md`](recipes/optimize.md) for measurable improvement;
- [`simplify.md`](recipes/simplify.md) for behavior-preserving cleanup;
- [`polish.md`](recipes/polish.md) for interactive UI refinement;
- [`dogfood.md`](recipes/dogfood.md) for real-flow product use;
- [`worktree.md`](recipes/worktree.md) for isolation.

Add another recipe when the request genuinely crosses that boundary. Recipes refine this loop within the user's granted authority.
