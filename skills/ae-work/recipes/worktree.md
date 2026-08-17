# Worktree

Use when the user asks for an isolated checkout.

First detect whether the current checkout is already a worktree. Continue there when isolated; otherwise preserve the current working tree and choose the requested ref or repository default branch.

Create a meaningful `agent/` branch and sibling worktree with plain Git. Attach an existing PR or branch ref directly.

Protect dirty files by leaving them in place. Permission and checkout conflicts end with a clear report of the blocked ref.
