---
name: ce-worktree
description: Set up isolated git worktrees — create a new branch for fresh work, or attach a worktree to an existing branch/PR/commit to work on it in isolation. Use when starting isolated work or isolating an existing ref; detects existing isolation first.
---

# Worktree Isolation

Ensure the current Codex task happens in an isolated workspace without disturbing the user's main checkout. Codex may already start the task in a linked worktree, so detect that first and do not create a redundant one.

Order of operations: **detect existing Codex isolation -> otherwise use plain Git.**

**Two modes, set by the caller's need:**

- **New work (default).** No specific ref named — create a fresh branch from a base (trunk). This is what `ce-work` uses.
- **Isolate an existing ref.** The caller names a ref to work on in isolation — a PR head, an existing branch, or a commit. Attach the worktree to that ref instead of creating a new branch. One hard git rule governs this mode: **a branch can be checked out in only one worktree at a time.** If the named ref is already checked out somewhere (most commonly because it is the current branch in the primary checkout), do **not** create a second worktree for it — report that it is already checked out at `<path>` and let the caller act (work there in place; or, only if a clean separate tree is essential, create a *detached* worktree at the same commit). Never put one branch in two worktrees.

The steps below apply to both modes; the mode only changes what gets checked out and reported back to the caller.

## Step 0: Detect existing isolation

Before creating anything, check whether the current directory is already a linked worktree. Compare Git's absolute worktree-specific directory with its absolute common directory:

```bash
git rev-parse --absolute-git-dir
git rev-parse --path-format=absolute --git-common-dir
```

If the two absolute paths are **equal**, this is a normal checkout — continue to Step 1.

If they **differ**, you are in a linked worktree *or* a submodule. Distinguish them:

```bash
git rev-parse --show-superproject-working-tree
```

- **Non-empty** output -> you are in a submodule; treat it as a normal checkout and continue to Step 1.
- **Empty** output -> you are **already in an isolated Codex worktree**. Report the worktree path (`git rev-parse --show-toplevel`) and current branch. Do not create another worktree. Then **work in place**: in new-work mode, continue here; in isolate-an-existing-ref mode, check that ref out here (unless it is already the current branch) rather than nesting a worktree.

## Step 1: Create the worktree with Git

Only when Step 0 found no existing isolation.

1. **Run from the repo root.** Resolve it with `git rev-parse --show-toplevel`, then set that absolute path as `workdir` on each Codex shell call in this step. The `.worktrees/` and `.gitignore` paths below are repo-root-relative.
2. Choose a meaningful branch name from the work description (e.g. `feat/login`, `fix/email-validation`) — avoid opaque auto-generated names. Derive a filesystem-safe path slug separately (for example `feat-login`), because branch names may contain `/`. Pick a base branch (default: origin's default branch, else `main`).
3. **Ensure `.worktrees/` is gitignored before creating anything**, so worktree contents are never committed: check `git check-ignore -q .worktrees/` — **with the trailing slash**, so an existing directory-only `.worktrees/` rule is honored even before the directory exists (`git check-ignore .worktrees` without the slash would miss it and dirty a correctly-configured repo). If it is not ignored, add a `.worktrees/` line to `.gitignore`.
4. Best-effort refresh the base branch without disturbing the current checkout: `git fetch origin <from-branch>`. This is **non-fatal** — if it errors (no `origin` remote, a differently-named remote, or a local-only branch), do not abort; continue to the next step and use the local ref.
5. Create the worktree — the command depends on the mode:
   - **New work:** `git worktree add -b <branch-name> .worktrees/<slug> origin/<from-branch>` (use the local `<from-branch>` ref if `origin/<from-branch>` does not exist). This creates a new branch from the base.
   - **Isolate an existing ref:** attach to the ref instead of branching — for an existing branch or tag, `git worktree add .worktrees/<slug> <target-ref>`. For a **PR**, check it out **on a local branch** (never a detached `FETCH_HEAD` — that orphans the fix loop's commits instead of updating the PR): `git fetch origin pull/<n>/head:pr-<n>` then `git worktree add .worktrees/pr-<n> pr-<n>`. To preserve fork-safe push tracking, create the worktree detached with `git worktree add --detach .worktrees/pr-<n>`, then run `gh pr checkout <n>` in a separate Codex shell call whose `workdir` is that new worktree. If Git reports the ref is already checked out elsewhere, follow the already-checked-out rule under **Two modes** — do not force a second worktree.
6. Resolve the new worktree's absolute path and use it as the `workdir` for every subsequent Codex shell call. A `cd` in one shell call does not persist into the next.

If `git worktree add` fails with a Codex sandbox or permission error, request escalation through Codex when the command is safely within the user's requested scope. If escalation is unavailable or denied, the requested isolation could not be created. This then needs a **blocking** user decision before touching the current checkout — do not silently continue there (the user chose isolation specifically to avoid it, especially when `ce-work` / `ce-code-review` routed here for the worktree option). Read and follow [`references/codex-interaction.md`](references/codex-interaction.md), offering "work in the current checkout" versus "stop and resolve the permission issue". Only work in the current checkout on explicit confirmation, and do not retry alternative paths automatically.

## Other worktree operations

Use `git` directly — no wrapper is needed:

```bash
git worktree list                          # list worktrees
git worktree remove .worktrees/<branch>    # remove a worktree
```

To enter or leave a worktree, change the `workdir` on subsequent Codex shell calls; a standalone `cd` does not persist across calls.

## When to create a worktree

Create one (Step 1) only when you are **not** already isolated and you need a separate workspace:

- Reviewing a PR while keeping the current checkout free for other work
- Running multiple features in parallel without branch-switching overhead

Do not create a worktree for single-task work that can happen on a branch in the current checkout — and never when Step 0 shows you are already in one.

## Integration

`ce-work` and `ce-code-review` offer this skill as an option. When the user selects "worktree" in those flows, run Step 0 first: if the work is already isolated, proceed in place; otherwise create one with plain Git and a meaningful branch name derived from the work description.

## Troubleshooting

**"Worktree already exists"**: the path is in use. Set subsequent Codex shell calls to that worktree's absolute `workdir`, or remove it with `git worktree remove .worktrees/<slug>` before recreating.

**"Cannot remove worktree: it is the current worktree"**: run `git worktree remove` from a Codex shell call whose `workdir` is another checkout.
