# Review Scope, Intent, and Plan

Resolve scope without mutating the checkout. Return the diff, files, scope mode, refs, intent, plan data, PR context, and untracked exclusions.

## Explicit base

With `base:<ref>`, reject any additional PR/branch target. Resolve the merge base against the current `HEAD`; diff that base against the working tree so committed, staged, and unstaged tracked changes are included. Record untracked files as excluded.

## PR number or URL

Never checkout the PR.

1. Read PR state, title, body, and files. Skip closed/merged PRs. A clearly automated lockfile/release/version-only PR may be skipped; when uncertain, review it.
2. Read base/head refs, head SHA, fork status, URL, files, reviews, and comments.
3. Use `local-aligned` only when the current branch name matches the PR head, the PR is not cross-repository, and the PR head SHA is an ancestor of local `HEAD`.
4. For `local-aligned`, fetch/resolve the base if needed and diff the merge base against the working tree. This includes unpushed local fixes and is canonical; do not mix in `gh pr diff` hunks.
5. Otherwise use `pr-remote`: files come from PR metadata and diff from `gh pr diff`. Stop if the diff cannot be read.
6. Best-effort fetch the remote head and base without checkout into review refs. Reviewers use those refs with `git show`; if fetch fails, they use diff hunks only.

Never read changed workspace files in remote scope. Record prior-comments availability for the conditional reviewer.

## Branch target

Never checkout the branch.

- If the target equals the current branch, use current-branch scope.
- Otherwise resolve local or remote branch ref, resolve its default-base merge base, and diff the two refs.
- Mark remote-branch scope and require reviewers to use `git show <branch-ref>:<path>` or hunks, never workspace files.

## Current branch / no target

Resolve the default base in this order: current PR base when available, `origin/HEAD`, remote default branch, then `main`. Resolve a merge base and diff it against the working tree. Include tracked committed/staged/unstaged changes and list untracked exclusions.

Do not review an empty diff. Do not hide command failures behind a zero-sized result.

## Intent

Build a 2–3 line best-effort intent summary from, in order:

- explicit plan or conversation context;
- PR title/body/linked issues;
- branch name and commits;
- changed behavior in the diff.

Never block on ambiguity. Record intent confidence as explicit, inferred, or uncertain.

## Plan discovery

Choose at most one plan:

1. explicit `plan:` path;
2. one unambiguous existing `docs/plans/*.{md,html}` path in the PR body;
3. one unambiguous filename match from specific branch keywords.

Wrong-plan matching is worse than no plan. Verify existence. Tag explicit paths/PR links as `explicit`; keyword discovery as `inferred`.

For plans, read metadata first:

- `requirements-only`: product intent only; do not create work-step completeness findings;
- `implementation-ready` + `execution: code`: extract Requirements and Work Steps;
- invalid progress-like readiness values are contract errors.

Extract requirements from `### Requirements` under What We're Building and
W-IDs from `## Work Steps`. HTML uses the same visible headings and IDs.

Completeness routing happens during merge:

- explicit plan omissions are actionable P1 findings;
- inferred plan omissions are advisory P3 findings;
- no plan means no completeness section.

## Remote inspection invariant

Pass scope mode and fetched head/base refs to every reviewer and validator. In remote scope they may inspect only fetched refs or supplied hunks. In local-aligned/current scope they may use normal read/search/git inspection.
