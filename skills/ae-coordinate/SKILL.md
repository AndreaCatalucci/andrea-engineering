---
name: ae-coordinate
description: Coordinate a large delivery across focused agent chats.
disable-model-invocation: true
---

# Coordinate

Return copyable prompts; the user starts chats and returns their reports.

Use the fewest chats that preserve clear ownership and independent write scopes. Do not spawn subagents unless the user explicitly asks the coordinator to run them. Do not create a separate chat merely to add another opinion, review an existing report, or parallelize work that one focused chat can finish.

## Map delivery

Maintain one Delivery Map at `docs/delivery-maps/<date>-<slug>.md`. Accept any combination of end-to-end flows, invariants, requirements, and Implementation Plans.

Keep this operational index:

- delivery outcome and Implementation Plan paths, statuses, and in-scope slices or gaps;
- end-to-end behaviors and invariants with verified, reported, stale, or blocked evidence;
- current architecture references and intended architecture deltas with plan coverage;
- current frontier and decisions;
- a packet ledger with only packet ID, covered slices, status, and evidence references.

Implementation Plans own slice detail. Plan criteria describe intended behavior, not evidence: `reported` is an executor claim; `verified` names the coordinator-inspected check or primary artifact, revision, and result; missing proof is `blocked`. Reference repository facts; keep full prompts, reports, and logs out of the map.

Architecture truth lives under `docs/architecture/`. Each maintained C4 view is one Markdown file with its scope, verification basis at a named implementation revision, and one Mermaid block. The basis names inspected code, configuration, or checks. Maintain the smallest useful set, normally Context and Container; add Component, Dynamic, or Deployment views when delivery depends on them. Architecture is verified only after comparing the diagram's elements and relationships with that implementation; syntax or document inspection alone is insufficient.

## Reconcile

1. Inspect the plans, repository, architecture artifacts, and existing map until every scoped behavior, invariant, requirement, and intended architecture delta maps to an Implementation Plan slice or explicit gap.
2. Check returned reports against repository facts and architecture. Update affected plans and artifacts, then classify each evidence claim. Evidence becomes stale when later work or an observed state or revision change invalidates its basis; record why.
3. Recompute the frontier. Bundle by bounded user behavior, satisfied dependencies, expected write scope, and useful shared context. Prefer one cohesive packet. Split only when ownership or write scopes are genuinely independent and running them separately materially helps delivery. A packet may cover part of one plan or cohesive slices from several plans.
4. Emit the independent ready packets worth starting now. Name each packet's expected write scope and compatible packets. Cited plan files belong to the write scope; packets sharing one are incompatible and run serially. Do not expose all possible parallel work merely because it is ready.

Unplanned work stays visible and gets an `ae-plan` prompt. The coordinator applies evidence-backed architecture corrections; a consequential product or architecture choice with plausible alternatives gets an `ae-explore` prompt. Pause only the affected frontier.

## Work packets

Each `ae-work` prompt contains a stable ID, plan paths and slices, bounded behavior, expected write scope, compatible packets, authorization boundaries, and an explicit review disposition: `none` or one or more concrete questions with their selected perspectives. Before dispatch, ensure each cited plan's Architecture section names the starting artifacts or `None`, intended delta, invariants, and artifacts to update or create. Point to that section instead of copying its architecture context or target diagrams, and keep the Delivery Map out of executor prompts. The expected write scope still names every affected architecture file so parallel-safety is inspectable. A missing planned view is a gap that blocks closure. Permit adjacent changes required for the behavior and require plan updates for discovered gaps.

The packet completes when every cited slice has current completion evidence, or the executor returns a concrete blocker. Require a copyable report containing:

- outcome and user-visible behavior;
- changed files or commits;
- checks with exact commands and summarized results;
- architecture artifacts and their verification result;
- plan sections updated;
- scope expansion, deviations, gaps, and blockers.

References replace copied content and passing logs. Include a failure excerpt when it makes a blocker actionable.

## Select reviews and perspectives

Ordinary implementation checks and coordinator verification stay in the owning chat. Do not add a review packet, reviewer subagent, or extra perspective by default.

Request a review only when the user asks for one or when a named unresolved risk could materially change acceptance and cannot be settled by inspecting the implementation and its checks. Examples include security boundaries, irreversible data changes, concurrency, compatibility contracts, and conflicting evidence. Reuse current review evidence instead of repeating it.

For each review, state the concrete question it must answer and choose the single perspective best suited to that question. Add another perspective only for a separate material risk that the first perspective cannot assess. Do not request generic correctness, simplicity, security, testing, or architecture perspectives as a standard set. Do not review a review unless its evidence conflicts with repository facts.

Keep review proportional to the change. Documentation, plan receipts, narrow refactors, and well-covered local changes normally need coordinator inspection only. Put review in the same work packet when the author can act on its findings without compromising the required independence; create a separate packet only when independence or write-scope isolation matters.

## Response and completion

Return only state changes, ready prompts, blocked-frontier decisions, and newly stale evidence. The map carries full status.

Delivery completes when every in-scope plan slice is complete; every in-scope behavior and invariant has current verified evidence; and every affected current-state C4 artifact matches the verified implementation. Mark the map complete with final evidence references, then move it to `docs/delivery-maps/archive/`.

Before finishing, run the `unslop` skill.
