---
name: ce-simplify-code
description: "Simplify recently changed code for clarity, reuse, quality, and efficiency while preserving behavior. Use for tidy/refactor passes; use ce-debug for bugs."
---

Simplify recently changed code for clarity, reuse, quality, and efficiency while preserving exact behavior. Prioritize readable, explicit code over compact code — fewer lines is not the goal.

## Step 1: Identify scope

Resolve the simplification scope in this order:

1. **If the user explicitly named a scope** (a file, a directory, "the function I just wrote", "the changes from this morning"), use that scope. Treat user-named scope as authoritative — do not widen it.
2. **Otherwise, in a git repository**, default to the diff between the current branch and its base branch (e.g., `git diff origin/main...` or against the configured upstream). This covers the common case of "simplify everything I've added on this feature branch before opening a PR." If the branch has no upstream or base ref, fall back to staged + unstaged changes (`git diff HEAD`).
3. **Outside a git repository or when no diff is available**, review the most recently modified files mentioned by the user or edited earlier in this conversation.

If none of the above produces a non-empty scope, ask the user what to simplify and stop rather than guessing.

**Preflight — skip a no-yield scope before spending reviewers.** The three reviewers hunt for reuse, quality, and efficiency issues in *code*. If the resolved scope contains no substantive human-authored code — it is documentation- or Markdown-only, or only generated, vendored, dependency/lockfile, or purely mechanical (formatting, lint autofix, mass rename) churn — stop here with a one-line note that there is nothing to simplify, and do **not** dispatch the reviewers. On a mixed diff that includes both real code and these no-yield changes, narrow the scope to the code files and continue. This preflight gates on the *kind* of change only, never on size or count: an explicit user-named scope is authoritative and still runs even when small. (Callers that already gate on size — `ce-work`, `$lfg` — and any standing "run this automatically" instruction own the size/cost policy; this preflight is only the no-code safety net.)

## Step 2: Launch 3 review agents in parallel

Dispatch three generic Codex subagents—code-reuse, code-quality, and efficiency reviewers—with `spawn_agent`, queuing if all active-agent slots are occupied. For each reviewer, pass its **full prompt asset** plus scope identifiers such as the base ref, diff range, and file paths. Do not embed a copy of the diff; each reviewer inspects the current diff and surrounding code independently.

- `references/personas/code-reuse-reviewer.md` — existing utilities, duplicated functionality, reimplemented stdlib/runtime primitives.
- `references/personas/code-quality-reviewer.md` — redundant state, parameter sprawl, copy-paste, leaky abstractions, stringly-typed code, dead code, over-nesting, and the over-simplification balance guard.
- `references/personas/efficiency-reviewer.md` — unnecessary work, missed concurrency, hot-path bloat, no-op updates, memory leaks.

Do not paraphrase these rubrics from memory — read each file and pass it verbatim, or the reviewer loses the gating rules that keep the pass behavior-preserving.

**Bounded dispatch.** Queue the three reviewers and launch only as many as Codex accepts at once; treat the concurrency limit as backpressure and start queued reviewers when a slot frees.

## Step 3: Fix issues

Wait for all three agents to complete. Aggregate their findings and fix each issue directly. If a finding is a false positive or not worth addressing, note it and move on. Do not argue with the finding or raise questions to the user, just skip it.

Before applying each fix, confirm it preserves behavior: same output for every input, same error behavior, and same side effects and ordering. If a fix can't clear that test, skip it — automated checks in Step 4 don't cover every behavior.

**Never simplify away a safety check.** Input validation at trust boundaries, error handling that prevents data loss, security checks (authorization, escaping, sanitization), and accessibility affordances are not removable boilerplate — preserve them even when a finding frames them as redundant or inline-able. Code that drops one of these is not simpler, it is unfinished. If a proposed simplification would thin or remove one, skip it.

## Step 4: Verify behavior is preserved

The premise of this skill is that simplification preserves exact functionality. After applying fixes:

**Run typecheck and lint over the full project.** They are usually fast and catch the most common simplification regressions — broken imports, unused exports, dropped type narrowings, dead code other modules still reference.

**Run tests:**
- Run tests scoped to the changed paths. CI runs the full suite on PR — this local check is a fast signal, not the final guarantee. Match scope to blast radius; a 3-line simplification doesn't warrant a 20-minute test run.
- Broaden scope when the change has obvious wide reach — e.g., a heavily-imported utility was rewritten, or the code-quality reviewer's consolidation/dedup fixes modified shared code. This is a judgment call about ripple risk, not a mechanical rule.
- If the test runner has no scoping mechanism, run the full suite.

Surface any failure clearly with the failing check name and the relevant output. Do not relax assertions, weaken type signatures, or skip tests to make checks pass — that defeats the "preserves functionality" guarantee. Either fix the underlying break introduced by simplification, or revert the specific change that caused the regression.

If no test suite, lint, or typecheck is configured, state that explicitly in the summary; do not silently skip verification.

## Step 5: Summarize

Briefly summarize what was good vs improved and fixed, including which checks were run and their results. If there were no findings to act on, confirm the code didn't require any changes.

**Quantify the impact by dimension.** Report what was actually applied, not a line count: fixes applied per reviewer dimension (reuse, quality, efficiency), how many findings were skipped as false-positive or not worth addressing, and the behavior-preservation result (checks run and outcome). For example: "Applied 6 — reuse 2, quality 3, efficiency 1; skipped 2 false positives; typecheck + lint clean, 11 scoped tests pass." Do not headline a net-lines-removed figure or frame fewer lines as the win — many clarity, safety, and efficiency fixes preserve or add lines. The measure is what improved and that behavior held, not how much code shrank.
