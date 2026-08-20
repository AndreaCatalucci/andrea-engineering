---
name: ae-ship
description: Perform a requested Git or pull-request action. Use for commits, pushes, PR creation or updates, review feedback, and PR monitoring.
---

# Ship

Perform the Git or PR state change the user requested.

Before writing, inspect the branch, working tree, diff, and remote. Preserve unrelated changes and stage the intended change set. Use a concise commit message and PR description focused on value. Run the `unslop` skill before posting.

Commit requests use this core flow. Broader actions load the matching recipe:

- [`pr.md`](recipes/pr.md) to push and create or update a PR;
- [`feedback.md`](recipes/feedback.md) to address PR feedback;
- [`watch.md`](recipes/watch.md) to monitor an open PR.

The user's request grants the scope for external writes. Merges, force-pushes, shared-history rebases, branch deletion, and releases follow explicit authorization.

Return the resulting commit, PR URL, or current state plus any blocker.
