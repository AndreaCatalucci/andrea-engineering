---
name: ae-coordinate
description: Coordinate delivery with execution prompts, settings previews, and user-approved chat creation.
disable-model-invocation: true
---

# Coordinate

Advance delivery through a state machine. Delegate execution through complete, copyable prompts; reconcile the returned evidence before advancing dependent work.

The coordinator owns the Delivery Map, evidence reconciliation, plan status, and evidence-backed architecture corrections. Executors own implementation, debugging, experiments, and requested Git actions. Deployment belongs to the user; track it as an external dependency only when it is in scope. A discovered defect becomes an execution packet, even when its fix looks small.

Use the fewest chats that preserve clear ownership and independent write scopes. After each ready prompt, preview its launch settings and proactively ask whether to create that chat programmatically. Every creation requires an explicit answer approving the displayed prompt and settings. General requests to coordinate or run autonomously are not approval for future chats. Keep the copyable prompt available for manual launch; never substitute a subagent to bypass the creation decision.

## Advance state

On every turn, load the active map and reconcile new input. Derive the state from current evidence and outstanding packets; a saved status alone is not proof. Apply the first matching row after reconciliation:

| State | Condition | Required action and exit |
|---|---|---|
| `reconcile` | New scope, report, decision, failure, or invalidated evidence needs inspection | Inspect the relevant primary evidence, update the map, and select the next state in this turn. |
| `complete` | Every scoped completion criterion below is verified | Archive the map and return final evidence references. |
| `ready` | Useful work has satisfied prerequisites and compatible write scope, with no existing proposal or handoff | Load [dispatch.md](recipes/dispatch.md). Output the complete prompt, preview settings, and ask to create the chat. Record it as `proposed`, then enter `approval`. A description of the next step does not complete this transition. |
| `approval` | A displayed proposal awaits a decision or its approved launch | Wait for explicit input before creation. Approval of the exact preview permits creation through the host's tool; record the returned reference and enter `waiting`. Changed settings or prompt require a new preview and decision. |
| `waiting` | Issued work can still advance delivery, with no additional independent work worth starting | Identify outstanding packet IDs and required reports. Collect results from created chats through the host's supported waiting mechanism or accept user-returned reports. A new report returns to `reconcile`. |
| `blocked` | No useful work can proceed without a decision, access, or external change | Name the exact blocker and the input that releases it. Route actionable investigation or planning through `ready`; resume reconciliation when the input arrives. |

Planning and exploration are executable frontier work: unresolved implementation detail produces an `ae-plan` packet; a consequential choice produces an `ae-explore` packet. Uncertain failure causes produce `ae-debug`; known repairs produce `ae-work`. Block only dependent work. Reconciliation that verifies one packet and unlocks another must issue the next prompt in the same response.

A displayed prompt is `proposed`; successful chat creation or the user's choice to launch it manually makes it `issued`, not completed. Reuse its ID while its scope is unchanged. On a repeated status request, identify the pending decision or outstanding work instead of duplicating it. Reproduce the full prompt when requested. A failure or changed scope returns to reconciliation; retire any superseded packet before replacing it, and confirm its executor has stopped before reusing its write scope. Never infer approval or completion from silence.

Match each returned report to its packet ID, issued scope, and implementation basis. A late report for superseded work remains historical evidence; inspect any resulting writes for conflicts, but never revive that packet or accept its old completion claim for the replacement. Independently verify any evidence reused for current scope.

## Map delivery

Maintain one Delivery Map at `docs/delivery-maps/<date>-<slug>.md`. Accept any combination of end-to-end flows, invariants, requirements, and Implementation Plans.

Keep this operational index:

- delivery outcome and Implementation Plan paths, statuses, and in-scope slices or gaps;
- end-to-end behaviors and invariants with verified, reported, stale, or blocked evidence;
- current architecture references and intended architecture deltas with plan coverage;
- current state, frontier, and decisions;
- a packet ledger with packet ID, covered slices or gap, status, previewed launch settings, user decision, and evidence or chat references.

Packet statuses are `proposed`, `issued`, `reported`, `verified`, `blocked`, or `superseded`. Retain the preview's message reference with the decision so approval stays bound to its prompt and settings. Only reconciliation marks a reported result verified. A blocked return preserves its evidence and reason; it does not complete the covered slices. Keep partial slice completion in the referenced plan.

Implementation Plans own slice detail. Plan criteria describe intended behavior, not evidence: `reported` is an executor claim; `verified` names the coordinator-inspected check or primary artifact, revision, and result; missing proof is `blocked`. Reference repository facts; keep full prompts, reports, and logs out of the map.

Architecture truth lives under `docs/architecture/`. Each maintained C4 view is one Markdown file with its scope, verification basis at a named implementation revision, and one Mermaid block. The basis names inspected code, configuration, or checks. Maintain the smallest useful set, normally Context and Container; add Component, Dynamic, or Deployment views when delivery depends on them. Architecture is verified only after comparing the diagram's elements and relationships with that implementation; syntax or document inspection alone is insufficient.

## Reconcile

1. Inspect the plans, repository, architecture artifacts, and existing map until every scoped behavior, invariant, requirement, and intended architecture delta maps to an Implementation Plan slice or explicit gap.
2. Check returned reports against repository facts and architecture. Update affected plans and artifacts, then classify each evidence claim. Before coordinator edits, check outstanding executor write scopes too: defer conflicting edits in the map until the owner returns or is confirmed stopped. Evidence becomes stale when later work or an observed state or revision change invalidates its basis; record why.
3. Recompute the frontier. Bundle by bounded user behavior, satisfied dependencies, expected write scope, and useful shared context. Prefer one cohesive packet. Split only when ownership or write scopes are genuinely independent and running them separately materially helps delivery. A packet may cover part of one plan or cohesive slices from several plans.
4. Select the independent ready packets worth starting now, excluding work already proposed or issued. Name each packet's expected write scope and compatible packets. Cited plan files belong to the write scope; packets sharing one are incompatible and run serially. Include outstanding executors when checking compatibility. Reconcile proposed scope expansions before permitting concurrent executors to edit the additional paths; serialize or reassign conflicting work. Do not expose all possible parallel work merely because it is ready.

Unplanned work stays visible and gets an `ae-plan` prompt. The coordinator applies evidence-backed architecture corrections; a consequential product or architecture choice with plausible alternatives gets an `ae-explore` prompt. Pause only the affected frontier.

## Work packets

Each `ae-work` prompt contains a stable ID, plan paths and slices, bounded behavior, expected write scope, compatible packets, authorization boundaries, and an explicit review disposition: `none` or one or more concrete questions with their selected perspectives. Before dispatch, ensure each cited plan's Architecture section names the starting artifacts or `None`, intended delta, invariants, and artifacts to update or create. Point to that section instead of copying its architecture context or target diagrams, and keep the Delivery Map out of executor prompts. The expected write scope still names every affected architecture file so parallel-safety is inspectable. A missing planned view is a gap that blocks closure. Permit adjacent changes required for the behavior and require plan updates for discovered gaps.

The executor returns when every cited slice has current completion evidence or a concrete blocker prevents further progress. Require a copyable report containing:

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

Lead with the current state and what changed. For each selected ready packet, output the complete fenced prompt, then the settings preview and creation question defined in [dispatch.md](recipes/dispatch.md). After approved creation, return its chat reference and expected report. The map carries full status.

Before ending the turn, check that every selected ready packet has a complete prompt, settings preview, and pending creation question; every waiting packet has an ID and expected report; and every blocker names its release condition. If a ready packet has only a next-step summary, finish its prompt and preview now.

Delivery completes when every in-scope plan slice is complete; every in-scope behavior and invariant has current verified evidence; every affected current-state C4 artifact matches the verified implementation; and every issued packet is reconciled or explicitly retired with its executor confirmed stopped. Retire unused proposals and withdraw unlaunched manual handoffs before closure. Mark the map complete with final evidence references, then move it to `docs/delivery-maps/archive/`.

Before finishing, run the `unslop` skill.
