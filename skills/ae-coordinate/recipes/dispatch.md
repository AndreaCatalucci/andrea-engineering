# Dispatch

Use in `ready` state. A packet is complete only when another agent can execute it without the coordinator's conversation history.

## Recommend settings

For each packet, recommend one model and one supported reasoning-effort setting, with a sentence tying the choice to the work. Respect user-selected settings. Resolve exact names and supported combinations from the execution host's current model catalog or tool metadata; use current official provider documentation only for capability guidance the host does not expose. Public API availability does not establish availability in the user's coding agent. Reuse a verified catalog within the session until the host or availability changes.

Optimize for expected cost to a correct result, including likely retries and rework. Start with the least expensive available model likely to meet the packet's acceptance criteria:

| Work | Starting recommendation |
|---|---|
| Mechanical, bounded edits with decisive checks | Fast coding model; low effort |
| Feature work on known seams with several interacting requirements | Economical general coding model; medium effort |
| Ambiguous diagnosis, cross-module design, concurrency, security, or difficult evidence reconciliation | Start with a capable general coding model at medium effort; increase effort or model capability for a specific unresolved difficulty |

These are heuristics, not measured guarantees. A premium model needs a concrete reason a cheaper option is unlikely to suffice; keywords such as security or architecture alone do not establish that. Adjust model and effort separately. Fix missing context or access before escalation, and use cheaper settings again for routine follow-up work. Reuse local performance evidence when available; do not launch comparative model trials just to choose a packet's settings.

If the catalog is unavailable, name the known current model where possible; otherwise recommend `host default`, with effort `host default` when support is unknown. State the availability limitation and continue preparing the packet. Do not invent a model identifier, effort value, price, or benchmark.

Recommendations become launch settings only when the user approves the exact preview. They do not change an already-running executor.

## Write the prompt

Output one complete fenced text block per packet, followed by its launch preview. Fill every field below with concrete values; use `None` where appropriate. Use the host's skill invocation syntax. Keep launch settings outside the prompt so executors do not mistake them for runtime controls.

```text
$<execution-skill> <bounded outcome>

Packet: <stable ID>
Repository: <source project path; work in the checkout assigned to the new chat>
Read: <repository-relative plan paths and exact slices/sections, or scope and evidence for an unplanned gap; resolve paths in the assigned checkout>
Deliver: <observable behavior or decision artifact; acceptance criteria or exact reference>
Write scope: <expected code, plan, and architecture paths>
Dependencies and compatibility: <satisfied prerequisites; compatible or conflicting packet IDs>
Authorization and finish line: <inherited permissions; requested local or Git stopping point; deployment handoff to the user if needed>
Review: <none, or concrete questions with selected perspectives>

Inspect the cited context and affected code. Complete this bounded outcome,
including adjacent changes necessary for it. Record discovered gaps in the
cited plan. While other packets are outstanding, return any proposed expansion
beyond the declared write scope before making those edits; the coordinator
must reconcile ownership first. Continue independent work within your scope.
Stop at the stated finish line or return a concrete blocker.

Return packet ID, outcome, changed files or commits, exact checks and results,
architecture verification where applicable, updated plan sections or produced
decision artifacts, and deviations, gaps, or blockers. Provide evidence
references the coordinator can inspect; distinguish observations from claims.
```

For `ae-plan` and `ae-explore`, name the question, required artifact path, and decision or planning boundary instead of inventing implementation slices. For `ae-debug`, state whether the executor should diagnose only or also fix. Preserve the work-packet Architecture requirements for `ae-work`.

## Preview and ask

Resolve the host's available project and chat-creation settings before asking. This preparation is read-only; create neither a checkout nor a chat yet. Preview:

- packet ID and proposed chat title;
- host, saved project, and actual local checkout path;
- environment: use that local checkout directly or create an isolated worktree, with the reason;
- starting code: default branch, an exact existing ref, or a copy of the current local working tree including uncommitted changes; identify the inspected revision and relevant local changes;
- model and supported reasoning effort, with the value-based rationale above;
- the exact prompt just displayed, identified by packet ID.

Prefer a worktree for Git implementation work unless the user wants the local checkout directly; use local for a non-Git project. Verify which checkout the host would copy. If the packet needs uncommitted plans or code, propose including that local working tree explicitly. Ensure all referenced inputs exist in the proposed starting state. Do not silently substitute a different checkout, drop local changes, invent a branch, or promise an unsupported copy mode.

After the prompt and preview, proactively ask one direct question: “Create a new chat for packet <ID> with these settings and this prompt?” Use the host's permitted user-input mechanism and wait for an explicit answer. Explain that creation waits because this skill requires approval of each preview. A suggested or preselected answer, silence, timeout, and prior general autonomy are not approval. The user may approve, request changes, launch manually, or defer. Record deferral without repeatedly asking until new input reopens that proposal. Batch creation requires explicit approval of the listed packet IDs and their individual previews.

## Create after approval

Recheck availability, source state, and write-scope compatibility. If the approved setup or prompt must change, show the revised preview and ask again. Otherwise call the chat-creation tool once with exactly the approved values; an unchanged approved launch needs no second confirmation. Approval of a preview naming a specific model or local-copy source is the explicit request for that setting.

For Codex, discover `list_projects` and `create_thread`. Use the returned project ID and `isGitRepository` to choose the preview. Map direct checkout to `environment.type=local`; map isolation to `worktree`. Omit `startingState` for the default branch, use `working-tree` for the approved local copy, or `branch` for an approved exact ref. Omit unknown default model/effort fields. These options follow the current tool schema; verify it before calling.

Record a successful creation reference as `issued` and follow setup or completion through supported host tools. A queued client ID is not a ready thread ID. Return the host's created-chat link or directive and collect the executor report before verification. A failure or uncertain response is not proof of no creation: inspect host state before retrying to avoid duplicates. If creation tools or the proposed settings are unavailable, keep the full prompt available and explain the manual option; never claim a chat was created.
