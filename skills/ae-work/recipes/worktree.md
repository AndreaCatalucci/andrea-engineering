# Worktree

Identify the requested starting revision and the code, plans, and local changes this task needs. Reuse an existing worktree only when it contains those inputs. Honor the requested ref; otherwise choose a revision containing the required code, using the repository default branch when sufficient.

When a new worktree is needed, create a meaningfully named branch using the repository or host convention and a sibling worktree with plain Git. Attach an existing PR or branch ref directly.

Preserve original dirty files. Where required inputs are uncommitted, carry only those inputs into the isolated checkout using the available workflow. Verify the destination contains the intended revision and inputs before implementation. If that starting state cannot be reproduced, report the missing input or conflict instead of silently substituting another state.
