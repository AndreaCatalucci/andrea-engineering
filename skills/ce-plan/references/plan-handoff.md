# Plan Handoff

Load this reference after the plan is written and its confidence check is complete.

## 5.3.8 Document Review

Run this phase only for Markdown plans. `ce-doc-review` currently applies Markdown-specific mutations, so HTML plans skip it and report that limitation.

For Markdown, run `ce-doc-review` with `mode:headless <plan-path>`. This review is mandatory even when the confidence check passed: confidence strengthens rationale and grounding; document review checks coherence, feasibility, scope, and role-specific concerns.

Capture:

- fixes applied;
- remaining proposed fixes, decisions, and FYI observations;
- any P0/P1 findings.

Address P0/P1 findings before returning from a pipeline run. Otherwise preserve remaining findings in the final summary so the user can request an interactive review later.

## 5.3.9 Final Checks and Cleanup

Verify:

- the plan is stronger, not merely longer;
- the planning boundary remains intact;
- origin decisions were preserved;
- the artifact exists at one canonical path.

Clean temporary scratch data after the artifact is safely written. If cleanup is impractical, report its location.

For HTML, follow `references/html-rendering.md`; for Markdown, follow `references/markdown-rendering.md`.

## 5.4 Optional Next Steps

Return the absolute plan path and one concise document-review summary. Mention appropriate optional next steps—implementation, interactive review, issue creation, or publishing/opening—without presenting a blocking menu.

Do not invoke another skill, create a goal or issue, publish, open an application, or wait for a selection unless the user explicitly asks in a later message. The plan is complete once the artifact exists, confidence checking and required document review have finished, and final checks pass.
