---
name: ae-work
description: Implement a concrete request or plan. Use for building or changing code; use ae-debug when the main problem is discovering why something fails.
---

# Work

Implement the requested outcome with the least process that keeps the change sound.

1. Read the request or plan and inspect the affected code. Reuse relevant project lessons and current evidence. Preserve unrelated user changes.
2. If a missing product decision would materially change the result, ask. Otherwise make the smallest reasonable assumption and state it briefly.
3. Implement the complete requested behavior using existing patterns. Remove complexity when that is simpler than extending it.
4. When architecture changes, update or create every affected current-state C4 artifact under `docs/architecture/`. Each view is one Markdown file with its scope, verification basis at a named implementation revision, and one Mermaid block. The basis names inspected code, configuration, or checks.
5. Verify the changed acceptance behavior. Reuse existing coverage; where it is missing, add the smallest meaningful test or direct check that would detect an incorrect result. Run required repository checks and check affected architecture artifacts. Repeat only after relevant changes or conflicting evidence.
6. If an Implementation Plan guided this work, mark only criteria supported by that evidence complete and record the architecture result. Leave unverified criteria open with the missing check named.
7. Report what changed, what was checked, which architecture artifacts changed, and any real limitation.
8. Follow the request's review disposition. If it has none, run `ae-review` only when a named material risk remains after the direct checks: a trust or security boundary, irreversible data change, concurrency, a public compatibility contract, a broad cross-module refactor, or conflicting evidence. Skip review for low-risk, well-covered changes.

The user's request defines which adjacent actions—planning, review, browser work, and Git operations—join implementation. A trajectory change is a lesson.

Load at most one matching file from `recipes/` before acting:

- [`autonomous.md`](recipes/autonomous.md) for explicitly hands-off delivery;
- [`optimize.md`](recipes/optimize.md) for measurable improvement;
- [`simplify.md`](recipes/simplify.md) for behavior-preserving cleanup;
- [`polish.md`](recipes/polish.md) for interactive UI refinement;
- [`dogfood.md`](recipes/dogfood.md) for real-flow product use;
- [`worktree.md`](recipes/worktree.md) for isolation.

Load another recipe only when the request actually crosses that boundary.
