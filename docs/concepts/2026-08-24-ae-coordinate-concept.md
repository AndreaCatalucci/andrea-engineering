---
title: ae-coordinate Concept Notebook
date: 2026-08-24
status: implemented
---

# ae-coordinate

## Problem

Large milestones span several executor chats. Each chat benefits from a narrow context, while the milestone needs one place to preserve cross-slice invariants, end-to-end user behavior, dependencies, implementation gaps, and current evidence. Coordination sometimes stops at a description of the next step, leaving the user to reconstruct the execution prompt and choose its model settings.

## Desired outcome

`ae-coordinate` turns user-defined delivery scope and available Implementation Plans into the next useful prompts. It maintains a Delivery Map, reconciles returned reports against the delivery outcome, and prepares the next prompts until the milestone is complete or needs a user decision.

The skill delegates through complete prompts the user can inspect and copy. After each ready prompt it previews the project, checkout or worktree, starting code, model, and reasoning effort, then asks to create the chat programmatically. Every creation requires explicit approval of that preview; manual launch and deferral remain available. The coordinator owns tracking and verification; executors own implementation, diagnosis, experiments, and requested Git actions. Deployment belongs to the user.

The authoritative transition rules live in [the skill](../../skills/ae-coordinate/SKILL.md); [the dispatch recipe](../../skills/ae-coordinate/recipes/dispatch.md) owns settings selection, the prompt contract, and approved creation. The state machine distinguishes reconciliation, ready work, pending approval, outstanding handoffs, blockers, and verified completion. Ready work requires a full prompt, launch preview, and creation question before the coordinator can finish its turn.

## Concepts

- **Implementation Plan:** An input produced by `ae-plan`; it owns implementation slices and done criteria.
- **Delivery Map:** A compact cross-plan view of the delivery outcome, user behavior, invariants, dependencies, gaps, evidence freshness, and current frontier.
- **Work packet:** One complete prompt for a bounded executor, with a model and reasoning-effort recommendation. Implementation packets may cover part of one plan or cohesive slices from several plans; planning, exploration, and diagnosis packets name their question and expected artifact or evidence.
- **Work report:** The implementer's copyable return containing outcome, evidence, plan changes, and remaining gaps.
- **Frontier:** Work whose prerequisites are satisfied and whose result can change milestone evidence.

## Prototypes

### A. Prompt compiler

Read the plans and emit all work packets once. Keep no coordination state beyond the plans.

Hypothesis: lowest overhead, but weak when discoveries change later work or several plans share invariants.

### B. Delivery coordinator

Maintain a Delivery Map, issue only frontier work packets, reconcile each returned report, and update the next frontier.

Hypothesis: best balance of focused executor context, human control, and end-to-end accountability.

### C. Execution controller

Maintain a task graph, fixed report schema, gates, and detailed execution ledger.

Hypothesis: more complete automation, but recreates project-management machinery and spends context on process instead of delivery.

## Architecture prototypes

### A. Diagrams inside each Delivery Map

Embed the delivery's C4 diagrams beside its frontier and evidence.

Hypothesis: the target change stays visible, but every milestone can copy and diverge from the repository architecture.

### B. Repository architecture with delivery deltas

Maintain repository-level C4 artifacts under `docs/architecture/`. The Delivery Map names the intended architecture delta, plan coverage, and verification state; the coordinator reconciles the shared diagrams after implementation.

Hypothesis: one architecture source of truth supports several milestones while the Delivery Map keeps each change accountable.

### C. Architecture decisions only

Keep decision records and infer diagrams from code when coordinating.

Hypothesis: fewer maintained diagrams, but every coordinator chat spends context reconstructing system boundaries and drift becomes harder to inspect.

## Emerging principles

- Plans describe intended work; evidence establishes current truth.
- Each work packet should point to its Implementation Plan slices instead of repeating Delivery Map context.
- The coordinator owns cross-slice coherence, while the implementer owns code-level decisions inside its packet.
- Repository C4 artifacts describe architecture; Implementation Plans describe intended changes to it.
- `ae-work` updates affected architecture artifacts with the implementation, and the coordinator reconciles code, plans, evidence, and diagrams against the intended end state.
- Returned reports are claims to reconcile, not automatic proof of completion.
- The user approves the exact prompt and settings before each programmatic creation. A changed preview requires a new decision; an unchanged approved launch needs no repeated confirmation.

## Current evidence

- `ae-plan` writes Implementation Plans with slices and done criteria.
- `ae-work` already updates the guiding plan and reports changes, checks, and limitations.
- The catalog was previously simplified to avoid generated workflow infrastructure. The reported missing-prompt behavior now calls for explicit state transitions and a checkable handoff criterion within the existing Markdown skill and Delivery Map.
- Mermaid supports C4 Context, Container, Component, Dynamic, and Deployment diagrams. Its C4 diagrams use fixed styling; tags, links, sprites, and legends remain unfinished. Diagrams can carry structure, while evidence and coordination metadata remain in the Delivery Map.

## Leading concept

Prototype B: a delivery coordinator with a persistent Delivery Map. On each turn it emits the smallest useful set of independent work packets on the current frontier.

## Decisions

- Keep one compact Delivery Map for the input plans. It preserves cross-plan state without turning each Implementation Plan into a coordination ledger.
- Prefer one cohesive execution packet. Present multiple ready packets only when their ownership and write scopes are independent and separate chats materially help delivery. Include outstanding executors when checking compatibility. Approval covers only the packet IDs and individual previews the user accepts.
- Give each work packet an explicit review disposition. Ordinary checks and coordinator verification need no separate review; request the single best perspective only for a named material risk, and add perspectives only for separate risks.
- The coordinator may update plan evidence and status, split or reorder slices, and add gap slices while preserving the agreed milestone outcome. A change to product behavior or milestone scope remains a user decision.
- Reconcile each report against the repository and plans. `Reported` is an executor claim; `verified` names the coordinator-inspected check or primary artifact, revision, and result; `stale` records invalidated proof; `blocked` means proof is missing.
- Require a work report containing the outcome, changed files or commits, checks and results, plan updates, deviations, gaps, and user-visible behavior. Prefer references and exact result summaries over copied logs.
- Complete a milestone only when every in-scope plan slice is marked complete, the repository has current verified evidence for every in-scope end-to-end behavior and invariant, and all issued work is reconciled or explicitly retired with executors stopped. Withdraw unlaunched manual prompts before closure. Superseded late reports remain historical evidence; inspect their writes and verify any evidence reused for current scope.
- Evidence becomes stale when later work or an observed underlying state or revision change invalidates the behavior, seam, dependency, or assumption it covered. Record why it became stale.
- Each packet declares its expected write scope and compatible packets. Cited plan files belong to that write scope; packets sharing one are incompatible and run serially. Coordinator edits obey the same ownership limits; defer conflicting plan or architecture edits in the map until the executor returns or is confirmed stopped.
- Keep work packets plan-bound. Before dispatch, improve the cited slices so they contain the constraints needed to discover cross-slice effects. The executor reads the cited plans and affected code, and records newly discovered gaps in the plans.
- A packet owns one bounded behavior and permits adjacent changes required to complete it. While other packets are outstanding, executors return proposed edits beyond their declared write scope before making them so the coordinator can reconcile ownership. The report names any scope expansion.
- A new product or architectural decision pauses only the affected frontier. Present the gap and provide a copyable `ae-explore` prompt to inspect potential solutions and their tradeoffs; independent work may continue.
- The Delivery Map is an operational index: delivery outcome, Implementation Plan links, statuses, and in-scope slices or gaps; cross-plan behaviors and invariants with evidence; current frontier; gaps; and decisions. Implementation Plans remain the source of truth for slice detail.
- Each coordinator response names the current state and changes. Ready packets receive complete prompts, settings previews, and a creation question; approved creations receive chat references and expected reports. The Delivery Map carries complete status.
- Work reports have required information but no word limit. Write for the next agent: point to repository facts instead of copying them, name exact outcomes, and give each claimed completion checkable evidence.
- Invoke `ae-coordinate` explicitly. A displayed prompt is a proposal, not authorization. Record the user's decision against its preview; general autonomy does not authorize later chats. Deferral does not trigger repeated creation questions without new input.
- Recommend the least expensive model likely to satisfy the packet, accounting for retries and rework. Increase model capability or reasoning effort for a concrete difficulty; security or architecture labels alone do not justify a premium model. The dispatch recipe owns the selection rules.
- Treat plans as planning units and chats as execution-context units. Bundle work by bounded user behavior, satisfied dependencies, expected edit scope, and useful shared context; a plan-to-chat ratio is not a constraint.
- On completion, mark the Delivery Map complete with final evidence references, then move it to the archive.
- Store active Delivery Maps at `docs/delivery-maps/<date>-<slug>.md`. Move completed maps to `docs/delivery-maps/archive/<date>-<slug>.md` without dropping their final evidence references.
- Let the user establish scope with any useful combination of end-to-end flows, invariants, requirements, and Implementation Plans. Resolve that scope against the repository instead of requiring one input form.
- Keep a compact packet ledger in the Delivery Map: packet identifier, covered slices or gap, status, previewed settings, user decision and preview reference, and evidence or chat references. Full prompts and returned reports remain outside the map. Proposed means displayed; issued means chat creation succeeded or the user chose manual launch. Only inspected evidence establishes verified completion. Preserve blocked returns and retire superseded work before replacing it.
- When scoped work lacks an execution-ready Implementation Plan, block dependent implementation and issue a ready `ae-plan` packet. Add the verified returned Implementation Plan to the Delivery Map before dispatching implementation.
- Keep architecture truth under `docs/architecture/`.
- Maintain the smallest useful C4 baseline, normally Context and Container views. Add Component, Dynamic, or Deployment views only when a delivery changes or depends on those boundaries.
- The coordinator owns architectural coherence and artifacts. It applies evidence-backed corrections and sends consequential alternatives to `ae-explore`.
- Each Implementation Plan carries the relevant starting architecture and intended end-state delta. Each `ae-work` executor updates the affected architecture artifacts; the coordinator verifies that the resulting code and artifacts match the intended end state.
- `docs/architecture/` describes verified current state. An Implementation Plan carries the intended delta and may include a target C4 diagram. `ae-work` applies the verified result to the current-state artifacts after implementation.
- Keep each maintained C4 view in its own Markdown file. Start with `context.md` and `containers.md` when those views are useful; add one Component, Dynamic, or Deployment file per needed view without creating empty placeholders.
- Every Implementation Plan includes an Architecture section with current artifact references, intended boundary or relationship changes, affected invariants, and artifacts `ae-work` must update. State `No architecture change` when applicable.
- Each C4 view is a Markdown file containing its scope, verification basis at a named implementation revision, and one Mermaid block. The basis names inspected code, configuration, or checks.
- Architecture-changing delivery completes only after every affected current-state C4 artifact is updated and verified against the implementation.
- Architecture verification compares diagram elements and relationships with the implementation at the named revision; syntax or document inspection alone does not establish current-state truth.
- An Implementation Plan records `None` when a needed starting view is absent and names each C4 file `ae-work` must create. A missing planned view remains a delivery gap.

## Working contracts

### Work packet

Each packet follows the [dispatch recipe](../../skills/ae-coordinate/recipes/dispatch.md), including a complete prompt followed by a settings preview and creation question. It tells the selected executor to inspect context in its assigned checkout, complete the bounded outcome, record discovered gaps, and return evidence. Approving a named model or local-copy source authorizes that launch setting; prompt text itself does not change runtime settings.

The packet points to plan content instead of repeating it. The executor returns completion evidence or a concrete blocker. A blocker ends that attempt without completing its slices. The coordinator verifies the result and issues any newly unlocked packet in the same response.

### Work report

The executor returns:

- outcome and user-visible behavior;
- changed files or commits;
- checks with exact commands and summarized results;
- architecture artifacts and their verification result;
- plan sections updated;
- scope expansion, deviations, gaps, or blockers.

References replace copied file content and passing logs. Include the smallest failure excerpt that makes a blocker actionable.

## Remaining uncertainty

- How well the bundling criteria behave on a real milestone with several overlapping plans.

## Next experiment

Install the changed catalog and dogfood `ae-coordinate` on a real delivery with several overlapping Implementation Plans.
