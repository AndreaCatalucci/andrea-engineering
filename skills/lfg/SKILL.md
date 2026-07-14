---
name: lfg
description: "Ship software autonomously from request to open PR: plan, implement, simplify, independently review and fix, test, commit, push, open a PR, and drive CI to a decided state. Use only when the user explicitly invokes lfg or asks for hands-off delivery through an open PR. Not for interactive work or shipping an already-finished diff."
---

# LFG

Run the complete software delivery pipeline without check-ins:

`ce-plan → ce-work → ce-simplify-code → ce-code-review → review closure → ce-test-browser → ce-commit-push-pr → ce-babysit-pr`

Planning, simplification, independent review, applied fixes, relevant testing, and shipping are quality stages—not optional ceremony. Keep the orchestrator thin: each child skill owns its own workflow and validation. LFG checks transition state; it does not restate or second-guess child contracts.

Resolve every child skill against the host's available-skills list and invoke the exact listed name, including a plugin namespace when present.

## Autonomy Contract

- Do not ask the user questions. Pipeline-capable child skills resolve safe defaults or return blocked.
- Run stages in order. Never implement before an implementation-ready plan exists.
- If a required child returns `blocked`, `failed`, or an invalid transition result, stop and report the blocker. Do not invent a recovery loop.
- Do not weaken tests, requirements, security, or review findings to make the pipeline pass.
- Keep the same plan path through planning, work, and review.

Before planning, run `git remote`. If no remote exists, stop immediately: LFG cannot deliver its promised open PR. Recommend repository setup or `ce-work` for local-only implementation.

## Pipeline

### 1. Plan

If LFG's input references a readable plan, inspect it first. Reuse it without invoking `ce-plan` only when it is under `docs/plans/` and has:

- `artifact_contract: ce-unified-plan/v1`
- `artifact_readiness: implementation-ready`
- `execution: code`

Otherwise invoke `ce-plan` in pipeline mode with LFG's original request and require it to produce a plan with those fields.

Record the valid plan path. If the task is non-software, requirements-only, or no valid plan is produced, stop. Do not retry planning from the orchestrator.

### 2. Implement

Invoke `ce-work mode:return-to-caller <plan-path>`.

Proceed only when it returns `status: complete` for the same plan and reports changed work plus verification. Trust `ce-work` to own implementation completeness, test strategy, evidence, and its internal recovery. If it returns blocked or incomplete, stop with its reason.

### 3. Simplify

Invoke `ce-simplify-code` on the branch diff unless the change is docs-only or trivial (roughly fewer than 10 changed lines). It preserves behavior and verifies its edits. Do not commit yet.

### 4. Independently review

Invoke `ce-code-review mode:agent plan:<plan-path>`. Require a successful review result and its Actionable Findings summary or artifact.

Close the review in the working tree:

- Apply a finding only when it has a concrete fix, confidence 100 (or 75 with cross-reviewer agreement), current evidence still matches, and the change is mechanical—not a product, API, auth, permission, or security decision.
- Apply eligible fixes in severity order and run their requested targeted verification.
- Stop before shipping if any P0/P1 remains unresolved.
- Write unresolved P2/P3 findings to `docs/residual-review-findings/<branch-or-head-sha>.md` with run identity, severity, title, `file:line`, evidence, and suggested fix.

Do not commit, push, file tickets, or duplicate residuals in the PR body here. The shipping stage commits all intentional pipeline changes.

### 5. Browser-test relevant behavior

Invoke `ce-test-browser mode:pipeline` only when the plan or branch diff changes browser-visible behavior or a browser-backed user flow. Run it when relevance is ambiguous for a web-facing change. Skip it for backend-only, CLI, infrastructure, docs, and other non-browser work; `ce-work` verification and independent review still apply.

A failed required browser test blocks shipping. Record an intentional skip in the completion summary.

### 6. Ship

Invoke `ce-commit-push-pr mode:pipeline`. Require an open PR URL or a clear blocked result.

Do not duplicate commit grouping, branch selection, pushing, or PR composition in LFG.

### 7. Drive CI

When shipping produced an open PR, invoke `ce-babysit-pr mode:pipeline <pr-url>`. It owns CI watching, convergent repairs, and PR-feedback resolution. Accept its terminal result: green/decided, or surfaced residuals. Do not recreate its loop.

Skip this stage only when shipping failed to produce an open PR, in which case LFG reports blocked rather than complete.

## Completion

After planning, review closure, and shipping all succeed, report one compact result with the plan path, PR URL, verification and review outcome, CI state, and any surfaced residuals. Preserve concept guidance returned by shipping.

Pipeline babysitting stops at its bounded terminal state rather than waiting indefinitely for merge. When further watch-through-merge is useful, point to `ce-babysit-pr <pr-url>`.
