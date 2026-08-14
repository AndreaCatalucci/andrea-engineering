---
name: lfg
description: "Ship software autonomously from request to open PR: plan, implement, simplify, independently review and fix, test, commit, push, open a PR, and drive CI to a decided state. Use only when the user explicitly invokes lfg or asks for hands-off delivery through an open PR. Not for interactive work or shipping an already-finished diff."
---

# LFG

Run the complete software delivery pipeline without check-ins:

`ae-plan → ae-work → ae-simplify-code → ae-code-review → review closure → conditional ae-test-browser → ae-commit-push-pr → ae-babysit-pr`

Planning, simplification, independent review, applied fixes, relevant testing, and shipping are quality stages—not optional ceremony. Keep the orchestrator thin: each child skill owns its own workflow and validation. LFG checks transition state; it does not restate or second-guess child contracts.

Resolve every child skill against the host's available-skills list and invoke the exact listed name, including a plugin namespace when present.

## Autonomy Contract

- Do not ask the user questions. Pipeline-capable child skills resolve safe defaults or return blocked.
- Run stages in order. Never implement before an implementation-ready plan exists.
- If a required child returns `blocked`, `failed`, or an invalid transition result, stop and report the blocker. Do not invent a recovery loop.
- Do not weaken tests, requirements, security, or review findings to make the pipeline pass.
- Keep the same plan path through planning, work, and review.

Before planning, run `git remote`. If no remote exists, stop immediately: LFG cannot deliver its promised open PR. Recommend repository setup or `ae-work` for local-only implementation.

## Pipeline

### 1. Plan

If LFG's input references a readable plan, inspect it first. Reuse it without invoking `ae-plan` only when it is under `docs/plans/` and has:

- `plan_format: andrea-plan/v1`
- `plan_readiness: implementation-ready`
- `execution: code`

Otherwise invoke `ae-plan` in pipeline mode with LFG's original request and require it to produce a plan with those fields.

Record the valid plan path. If the task is non-software, requirements-only, or no valid plan is produced, stop. Do not retry planning from the orchestrator.

### 2. Implement

Invoke `ae-work mode:return-to-caller <plan-path>`.

Proceed only when it returns `status: complete` for the same plan and reports changed work plus verification. Trust `ae-work` to own implementation completeness, test strategy, evidence, and its internal recovery. If it returns blocked or incomplete, stop with its reason.

### 3. Simplify

Invoke `ae-simplify-code` on the branch diff unless the change is docs-only or trivial (roughly fewer than 10 changed lines). It preserves behavior and verifies its edits. Do not commit yet.

### 4. Independently review

Invoke `ae-code-review mode:agent plan:<plan-path>`. Require a successful review result and its Actionable Findings summary or artifact.

Close the review in the working tree:

- Apply a finding only when it has a concrete fix, confidence 100 (or 75 with cross-reviewer agreement), current evidence still matches, and the change is mechanical—not a product, API, auth, permission, or security decision.
- Apply eligible fixes in severity order and run their requested targeted verification.
- Stop before shipping if any P0/P1 remains unresolved.
- Write unresolved P2/P3 findings to `docs/residual-review-findings/<branch-or-head-sha>.md` with run identity, severity, title, `file:line`, evidence, and suggested fix.

Do not commit, push, file tickets, or duplicate residuals in the PR body here. The shipping stage commits all intentional pipeline changes.

### 5. Browser-test interaction-only behavior

Browser testing is not a default finishing stage for UI or web-facing changes.
Prefer focused component or integration tests when they can prove the changed
behavior without a person driving the rendered interface.

Invoke `ae-test-browser mode:pipeline` only when a material claim cannot be
covered confidently by practical integration tests and the remaining risk
depends on fiddly real-user interaction or browser rendering. Typical examples
are pointer or drag behavior, focus and keyboard transitions, responsive
layout, browser-native APIs, or multi-step rendered state whose correctness is
only apparent while using it. A changed view, route, component, or browser-backed
flow is not sufficient by itself.

When relevance is ambiguous, skip browser testing and rely on the focused
automated verification; mention any meaningful interaction-only uncertainty in
the completion summary. Also skip for backend-only, CLI, infrastructure, docs,
and other non-browser work. If this narrow gate is met, a failed browser test
blocks shipping.

### 6. Ship

Invoke `ae-commit-push-pr mode:pipeline`. Require an open PR URL or a clear blocked result.

Do not duplicate commit grouping, branch selection, pushing, or PR composition in LFG.

### 7. Drive CI

When shipping produced an open PR, invoke `ae-babysit-pr mode:pipeline <pr-url>`. It owns CI watching, convergent repairs, and PR-feedback resolution. Accept its terminal result: green/decided, or surfaced residuals. Do not recreate its loop.

Skip this stage only when shipping failed to produce an open PR, in which case LFG reports blocked rather than complete.

## Completion

After planning, review closure, and shipping all succeed, report one compact result with the plan path, PR URL, verification and review outcome, CI state, and any surfaced residuals. Preserve concept guidance returned by shipping.

Pipeline babysitting stops at its bounded terminal state rather than waiting indefinitely for merge. When further watch-through-merge is useful, point to `ae-babysit-pr <pr-url>`.
