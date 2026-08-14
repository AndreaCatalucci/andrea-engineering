---
name: ae-ideate
description: "Generate and evaluate grounded ideas. Use when the user asks for ideas, improvements, surprising options, or AI-generated directions before choosing one to develop; use ae-brainstorm to refine the user's own idea."
---

# Generate Improvement Ideas

`ae-ideate` answers: “What are the strongest ideas worth exploring?” It writes
a ranked ideation document. It does not write requirements, plans, or code.
Use `ae-brainstorm` when the product meaning or scope is unclear and `ae-plan`
after the user selects a sufficiently clear software direction.

Immediately before user-facing text, read `references/plain-language.md`.
Before asking a question, read `references/codex-interaction.md`.

## Non-negotiable rules

1. Gather evidence before generation.
2. Generate the complete raw set before critiquing any candidate.
3. Record a concrete basis for every candidate and a reason for every rejection.
4. Preserve requested scope, topic-area coverage, candidate quotas, independent
   verification, and final-document fields before pursuing token savings.
5. Use the active Codex model. Do not select models or capability tiers.
6. Spawn generation and verification agents with no inherited conversation
   history. Their supplied packets must be complete.
7. Keep full candidate and verdict prose in checked files. Normal agent returns
   are compact receipts.

The optional focus hint may name a concept, path, constraint, research file, or
volume request. An empty hint means open-ended ideation.

## Phase 0: Resolve the run

Read `references/intake-and-routing.md`. Resolve:

- output format and any explicitly resumed document;
- an identifiable subject or surprise-me mode;
- repository, outside-software, or non-software handling;
- enough source material for work outside the repository;
- focus, volume, tactical scope, and explicit `go deep` depth.

Do not ask solution-shaping questions. State the chosen source of substance in
the user's language. Before Phase 2, state the actual generation-agent count,
one verifier, and the possible single recovery agent.

## Phase 1: Gather relevant context

Create one eight-hex-character run ID and a scratch directory at
`/tmp/andrea-engineering/ae-ideate/<run-id>`. Reuse it for caches, candidate
files, verdicts, and temporary delivery. Do not delete it on completion.

Load exactly one grounding branch:

- current repository: `references/repo-grounding.md`;
- outside software or non-software: `references/elsewhere-grounding.md`.

If the user supplied gathered evidence, also read
`references/research-artifacts.md`. Do not load that branch otherwise. Follow
the named cache references only when their feature runs.

Produce one compact grounding summary. Separate user directives from
background evidence mechanically: constraints can exclude an idea; background
can support one but must not redirect a named focus.

## Phase 1.5: Cover the topic

From the existing grounding, choose 3-5 distinct topic areas at the same level
and in the topic's own language. Do not dispatch another agent or ask another
question. In repository mode, add concise `file:line` evidence for each area.

Skip decomposition when the topic is atomic or in surprise-me mode. Record
`Decomposition skipped — atomic subject` or
`Decomposition skipped — surprise-me mode` in the grounding summary.

## Phase 2: Generate candidates

Read `references/divergent-ideation.md` immediately before dispatch. It owns
the structured dispatch table, frame definitions, fresh-context packet,
candidate schema, receipt handling, merge, lineage, synthesis, recovery, and
raw checkpoint.

Use the selected entry in `references/dispatch-contract.json` as the only source
for fleet assignments, quotas, and evidence-read budgets. Do not restate those
values in a dispatch prompt; copy the selected values into its structured
assignment packet.

After candidate files are accepted, merged, deduplicated, combined, and checked
for area coverage, continue to Phase 3. Do not critique before then.

## Phases 3 and 4: Verify, select, and deliver

Read `references/post-ideation-workflow.md` only after Phase 2 completes. It
owns independent verification, root arbitration, survivor development,
rendering, delivery, and later selected-idea handoff.

At save time, read `references/ideation-sections.md` and exactly one renderer:
`references/markdown-rendering.md` or `references/html-rendering.md`.

Write to `docs/ideation/` when it exists or can be created in repository mode.
Otherwise use the run scratch directory and state that the path is temporary.
Return a compact orientation summary; do not reproduce the full document,
open an application, publish, commit, delete files, or present an action menu.

## Failure behavior

- If external research fails, warn and continue with available evidence.
- If a result file fails validation, allow one focused repair. A second failure
  marks that assignment missing; do not quietly invent its quota in the root.
- If an agent cannot write its authoritative file, accept one complete inline
  JSON fallback only after the parent persists and validates it with the same
  helper.
- If verification cannot run or any assignment remains missing, continue only
  with explicit degraded-coverage reporting in the rejection record and final
  summary.
- If final delivery fails, preserve the checked run files and ask for a writable
  destination.
