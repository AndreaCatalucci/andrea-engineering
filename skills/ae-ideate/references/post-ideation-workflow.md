# Post-Ideation Workflow

Read this after `consolidated-candidates.json` has been sealed. Critique starts
here, never during generation.

## Phase 3: Verify and select

### Independent verification

Spawn one verifier with no inherited turns. Supply only:

- the compact grounding summary and evidence-dossier paths;
- the absolute consolidated candidate path and checked digest;
- `verifier_role: basis-integrity`;
- absolute `skill_dir`, `helper_path`, `verifier_protocol_path`, draft path, and
  authoritative verdict path;
- the fixed protocol loaded from `verifier_protocol_path`.

The verifier reads candidates by path, writes one verdict per `candidate_id`,
seals the file with the packet's absolute `helper_path`, and returns a receipt.
The parent reruns `receipt-verdicts` through the same helper against the
allocated result path and requires an exact match. Under
`go deep` or non-software Full, dispatch one additional verifier with
`verifier_role: novelty-feasibility`. Give it distinct draft and authoritative
result paths; the two verifiers share only read inputs and schema. Dispatch
both together when capacity permits.

Allow one repair. An inline fallback is acceptable only as one complete verdict
document that the parent persists and seals through the same helper. If a
verifier remains unavailable, record the degradation and continue with root
critique; never imply independent verification ran.

### Root arbitration

Load the consolidated candidates and accepted verdict files once. Treat
verdicts as strong evidence, not authority. Overrule one only when the
grounding supports the decision and record why.

Reject candidates that are vague, duplicative, unsupported, contradicted,
outside scope, below the ambition floor, too costly for their value, or better
handled as an unresolved brainstorm. Do not generate replacements during this
cut. Record every disposition by `candidate_id`, with one rejection reason or a
survivor marker. Persist the complete list as `dispositions.json` in the run
directory before developing survivors. Keep any unrecovered area as its own
rejection row.

Rank survivors using groundedness, basis strength, expected value, novelty,
pragmatism, leverage, burden, overlap, and topic-area spread. Keep 5-7 by
default; honor an explicit volume override. Tighten the bar when too many pass
and report fewer honestly rather than lowering it.

### Develop survivors

Only after the cut, expand survivors with a concrete description, rationale,
downsides, confidence, and complexity. Preserve candidate ID, verified basis,
and area. If expansion exposes a weak premise, return the candidate to
arbitration instead of polishing through it.

Before delivery, confirm that every raw candidate has one disposition and every
survivor has complete fields, a supporting basis, and a scope and area check.

## Phase 4: Write and deliver

Resolve the destination:

- repository mode: create or use `docs/ideation/`;
- elsewhere mode with an existing `docs/ideation/`: use it;
- otherwise use the run scratch directory and identify it as temporary.

Write `YYYY-MM-DD-<topic>-ideation.<ext>`, or `open-ideation` without a fixed
topic. On explicit resume, preserve useful content and rejection history.

Read `ideation-sections.md` and exactly one renderer: `markdown-rendering.md` or
`html-rendering.md`. Write the relevant context, topic areas or skip reason,
ranked ideas, and complete rejection summary. Rendering changes presentation,
not content.

Return only:

- raw, rejected, and surviving counts plus the absolute document path;
- one line per survivor with rank, title, area, confidence, and complexity;
- the top pick;
- any area with zero survivors;
- any missing generation assignment or verification degradation.

Do not reproduce the document, open applications, publish, commit, delete
files, or present an action menu.

## Later selected-idea handoff

Only after the user chooses an idea, build a compact capsule containing its
title, move, constraints, desired outcomes, evidence, downsides, and source
document. Send clear software directions to `ae-plan`; send unresolved product
meaning, non-software directions, or scope questions to `ae-brainstorm`. Never
route directly to implementation.
