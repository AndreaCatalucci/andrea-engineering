---
name: ae-coordinate
description: Coordinate a large delivery across focused agent chats.
disable-model-invocation: true
---

# Coordinate

Return copyable prompts; the user starts chats and returns their reports.

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
3. Recompute the frontier. Bundle by bounded user behavior, satisfied dependencies, expected write scope, and useful shared context. A packet may cover part of one plan or cohesive slices from several plans.
4. Emit every independent ready packet together. Name its expected write scope and compatible packets. Cited plan files belong to the write scope; packets sharing one are incompatible and run serially.

Unplanned work stays visible and gets an `ae-plan` prompt. The coordinator applies evidence-backed architecture corrections; a consequential product or architecture choice with plausible alternatives gets an `ae-explore` prompt. Pause only the affected frontier.

## Work packets

Each `ae-work` prompt contains a stable ID, plan paths and slices, bounded behavior, expected write scope, compatible packets, and authorization boundaries. Before dispatch, ensure each cited plan's Architecture section names the starting artifacts or `None`, intended delta, invariants, and artifacts to update or create. Point to that section instead of copying its architecture context or target diagrams, and keep the Delivery Map out of executor prompts. The expected write scope still names every affected architecture file so parallel-safety is inspectable. A missing planned view is a gap that blocks closure. Permit adjacent changes required for the behavior and require plan updates for discovered gaps.

The packet completes when every cited slice has current completion evidence, or the executor returns a concrete blocker. Require a copyable report containing:

- outcome and user-visible behavior;
- changed files or commits;
- checks with exact commands and summarized results;
- architecture artifacts and their verification result;
- plan sections updated;
- scope expansion, deviations, gaps, and blockers.

References replace copied content and passing logs. Include a failure excerpt when it makes a blocker actionable.

## Response and completion

Return only state changes, ready prompts, blocked-frontier decisions, and newly stale evidence. The map carries full status.

Delivery completes when every in-scope plan slice is complete; every in-scope behavior and invariant has current verified evidence; and every affected current-state C4 artifact matches the verified implementation. Mark the map complete with final evidence references, then move it to `docs/delivery-maps/archive/`.

Before finishing, run the `unslop` skill.
