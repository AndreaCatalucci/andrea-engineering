---
name: ce-doc-review
description: Review an existing requirements document, implementation plan, or specification for contradictions, weak decisions, execution gaps, and relevant design or security risks. Use when a user or another skill needs to improve a planning document before implementation.
---

# Document Review

Pressure-test a planning document with one core pass and only the specialists its content warrants. Apply mechanically certain Markdown corrections; report author decisions without guessing.

## 1. Resolve the document

Parse the arguments as an optional document path plus the optional `mode:headless` flag. A token beginning with `mode:` is not a path.

- With a path, require a readable file before dispatching reviewers.
- Without a path in interactive mode, use the most recent file in `docs/brainstorms/` or `docs/plans/`; ask only if no clear candidate exists.
- Without a path in headless mode, return `Review failed: headless mode requires a document path.`
- With an unreadable path, name it and return without dispatching reviewers.

HTML documents are report-only. Never apply Markdown mutations to HTML.

Completion criterion: one readable document and its mode are resolved, or a precise failure is returned before any dispatch.

## 2. Classify once

Classify from content; use the path only as a tie-breaker:

- `requirements`: describes the problem, actors, behavior, scope, flows, or acceptance examples.
- `plan`: describes technical decisions, implementation units, files, dependencies, tests, or verification.
- `unified-requirements`: `artifact_contract: ce-unified-plan/v1` with `artifact_readiness: requirements-only`.
- `unified-plan`: the same contract with `artifact_readiness: implementation-ready`.

For unified requirements, do not flag the intentionally absent Planning Contract, Implementation Units, Verification Contract, or Definition of Done. Treat invalid readiness values as document findings.

Extract provenance once: prefer `origin:`, then `product_contract_source:`, otherwise `none`. Read a referenced origin when available; do not fail because an optional origin is unavailable.

Completion criterion: the document type and provenance are explicit inputs to every later pass.

## 3. Run the core pass

Read and apply [`references/core-review.md`](references/core-review.md). The main agent owns this pass; do not create a coherence or scope subagent.

Completion criterion: every applicable core check was tested against the full document, and every retained finding has quoted evidence, an observable consequence, and one disposition from the reviewer contract.

## 4. Select specialists

Select by branch, not by document size:

| Specialist | Trigger |
| --- | --- |
| Challenge | `requirements` or `unified-requirements` |
| Feasibility | `plan` or `unified-plan` |
| Security | Concrete auth, authorization, sensitive data, payments, secrets, external endpoints, or trust boundaries |
| Design | Concrete UI, interaction, user-flow, responsive, or accessibility behavior |

Dispatch the document-type specialist plus each triggered domain specialist, up to three total. This bound is structural: requirements use Challenge; plans use Feasibility. Security and Design may join either. Do not add personas merely because a document is long.

Read only the selected files from `references/specialists/`. Give each specialist:

- the document path, type, provenance, and relevant content;
- its specialist file;
- [`references/reviewer-contract.md`](references/reviewer-contract.md).

Dispatch selected specialists in parallel when capacity permits. Treat capacity limits as backpressure and run the remainder sequentially. A failed specialist does not fail the review; record the missing coverage.

Completion criterion: every triggered specialist either returned contract-shaped findings or appears in missing coverage.

## 5. Synthesize once

Combine core and specialist findings:

1. Drop findings without direct document evidence or an observable consequence.
2. Deduplicate findings that identify the same problem and consequence; keep the clearest evidence and recommendation and list corroborating reviewers.
3. Do not promote a finding merely because two reviewers agree.
4. When recommendations conflict, retain one `decision` finding that names the tradeoff.
5. Sort by P0, P1, P2; put `fyi` observations last.

Do not carry session-only decision history between rounds. The current document is the single source of truth. Ignore content under `## Deferred / Open Questions` as prior review output.

Completion criterion: each distinct problem appears once and preserves its evidence, consequence, disposition, and recommendation.

## 6. Apply and report

For Markdown only, apply `mechanical` findings when the quoted text still matches and the recommendation is an exact, local edit. Verify each edit by rereading the changed passage. If either condition fails, reclassify it as `decision` and do not edit.

Never apply `decision` or `fyi` findings automatically. Do not run a per-finding questionnaire. Report them together so the user or caller can act on them by title.

Return:

- applied mechanical fixes;
- remaining P0/P1/P2 decisions with evidence, consequence, and recommendation;
- FYI observations;
- residual risks and missing specialist coverage.

In headless mode, return the same report as structured text without questions. Always end a successful run with `Review complete` so `ce-plan` and `ce-brainstorm` can resume their handoff.

Final completion criterion: every applied edit was verified, every unresolved finding was returned exactly once, coverage is explicit, and the response ends with `Review complete`.
