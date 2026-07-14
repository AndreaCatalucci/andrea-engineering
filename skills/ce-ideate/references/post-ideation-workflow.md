# Post-Ideation Workflow

Read this file after Phase 2 agents return and the root agent has merged and deduplicated their candidates.

## Phase 3: Verify and Select

### Independent verification

Dispatch one fresh-context verifier using the inherited Codex model. Give it only:

- The consolidated grounding summary and dossier paths
- The merged candidate list
- The per-idea basis contract

Ask it to attempt to refute each candidate: verify that `direct:` evidence exists, `external:` prior art is real and relevant, `reasoned:` arguments hold, and the move passes the meeting-test. Require a `sound`, `weak`, or `refuted` verdict with a one-line reason. Under `go deep`, dispatch one additional fresh-context critic focused on novelty and feasibility using the same payload.

If verification cannot run, filter in the root agent and record the degradation.

### Root arbitration

Review every candidate and make the final cut. Treat verifier verdicts as strong evidence, not authority; overrule only when the grounding supports the decision, and record why.

Reject candidates that are:

- Vague, unactionable, duplicative, or already covered
- Unsupported or contradicted by their stated basis
- Below the meeting-test, unless tactical focus explicitly waived it
- Too costly for their expected value
- Outside the requested scope or a replacement for the subject
- Better treated as an unresolved brainstorm variant

Give every rejected idea a one-line reason. Do not generate replacements during filtering.

Score survivors on groundedness, basis strength, expected value, novelty, pragmatism, leverage, implementation burden, overlap, and axis spread. Evaluate axis spread across the survivor set; note any axis left empty after recovery.

Keep 5–7 survivors by default. Tighten the cut if more survive; report fewer honestly rather than lowering the bar.

### Develop survivors

After the cut, expand only the survivors into the final artifact fields: concrete description, rationale, downsides, confidence, and complexity. Preserve the verified basis and axis. Add nuance from the grounding, not invented support. If development exposes a weak premise, return the idea to arbitration instead of polishing it through.

Completion criterion: every raw candidate has a recorded disposition; every survivor has a verified basis, complete artifact fields, and a scope/axis check.

## Phase 4: Write and Deliver

Write the ideation artifact automatically.

1. Resolve the target:
   - Repo mode: create or use `docs/ideation/`.
   - Elsewhere mode with an existing `docs/ideation/`: use it.
   - Otherwise: use `<scratch-dir>` under `/tmp/andrea-engineering/ce-ideate/<run-id>/` and state that the path is temporary.
2. Use `<dir>/YYYY-MM-DD-<topic>-ideation.<ext>`, or `open-ideation` when no topic exists. The extension follows `OUTPUT_FORMAT`.
3. Read `references/ideation-sections.md` and only the matching renderer: `markdown-rendering.md` or `html-rendering.md`.
4. Write the grounding context, topic axes when present, ranked ideas, and rejection summary according to those references.
5. On resume, update the existing artifact in its current format and preserve prior useful content.

If writing fails, report the failure and ask for a writable path. Do not lose the survivor list.

Return a compact summary:

- Raw, rejected, and surviving counts plus the absolute artifact path
- One line per survivor: rank, title, axis, confidence, and complexity
- One sentence naming the top pick
- Any axis with zero survivors
- Any verification degradation

Do not reproduce the full artifact in chat, open applications, publish, commit, delete files, or present an action menu. End after delivery.

## Later Selected-Idea Handoff

Only when the user subsequently chooses an idea, build this compact capsule from the saved artifact and current context:

> Selected direction: <title and description>. Constraints: <known constraints>. Success criteria: <known outcomes>. Evidence: <basis>. Tradeoffs: <downsides>. Provenance: <path and idea title>.

Route a software direction with clear constraints and success criteria to `ce-plan`. Route unresolved product meaning or scope to `ce-brainstorm`. Route non-software ideas to `ce-brainstorm`. Never route directly to implementation.

## Quality Gate

Before finishing, confirm:

- Ideas were generated before critique.
- Every survivor has a basis that supports its move.
- Load-bearing direct evidence was checked.
- Every rejection has a reason.
- The survivor set passes ambition, scope, subject-identity, and axis-spread checks.
- The saved artifact contains the full reasoning; chat contains only orientation.
