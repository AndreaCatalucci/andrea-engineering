# Plan Handoff

Load this reference after the plan is written and its confidence check is complete.

## 5.3.8 Document Review

Run this phase only for Markdown plans. `ae-doc-review` currently applies Markdown-specific mutations, so HTML plans skip it and report that limitation.

For Markdown, run `ae-doc-review` with `mode:headless <plan-path>`. This review
is mandatory even when the confidence check passed. Review important decisions,
boundaries, risks, and proof; do not treat missing local coding tactics as a
feasibility gap.

Capture:

- fixes applied;
- remaining proposed fixes, decisions, and FYI observations;
- any P0/P1 findings.

Give the reviewer the pre-review `scripts/plan-metrics.py` word and
step counts and the selected depth budget. Review fixes should replace,
clarify, consolidate, or delete. New sections, technical decisions, diagrams,
abstractions, steps, or implementation details require evidence that a P0/P1
issue would otherwise leave the plan unsafe or force the implementer to reopen
an important decision.

Address P0/P1 findings before returning from a pipeline run. Otherwise preserve remaining findings in the final summary so the user can request an interactive review later.

## 5.3.9 Final Checks and Cleanup

Verify:

- the plan is stronger, not merely longer;
- post-review word growth is at most 10%, unless the summary records the P0/P1
  correctness reason for exceeding it;
- step count did not grow without that same justification;
- the planning boundary remains intact;
- origin decisions were preserved;
- the artifact exists at one canonical path.

Clean temporary scratch data after the artifact is safely written. If cleanup is impractical, report its location.

For HTML, follow `references/html-rendering.md`; for Markdown, follow `references/markdown-rendering.md`.

## 5.4 Optional Next Steps

Return the absolute plan path and one concise document-review summary. Mention appropriate optional next steps—implementation, interactive review, issue creation, or publishing/opening—without presenting a blocking menu.

Do not invoke another skill, create a goal or issue, publish, open an application, or wait for a selection unless the user explicitly asks in a later message. The plan is complete once the artifact exists, confidence checking and required document review have finished, and final checks pass.
