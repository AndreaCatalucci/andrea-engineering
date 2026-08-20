---
name: ae-explore
description: Explore a solution direction. Use when a solution exists and how it should work is still open.
---

# Explore

The user has a solution direction. Explore how it could work.

Read the request and relevant project context. Bring discoverable facts into the conversation.

Sketch genuinely different prototypes of the solution. Treat each as a hypothesis.

Finding facts is your job. When a hypothesis is cheap to check, check it: curl a public API to see its real response shape, auth, and rate limits; fetch a site's terms or pricing page to check licensing; read the relevant docs; run a quick snippet to confirm a claim. Look up what the code, docs, and environment already answer, and check claims against the code. Put only decisions to the user.

Map the work as a design tree. The frontier is every decision whose prerequisites are already settled. Each round, ask the whole frontier, then wait. Number each question and give your recommended answer. Offer concrete alternatives when the choice is bounded; use a free-form question when fixed choices would hide the real decision. Put any looked-up fact in the question.

A question that depends on an unanswered one belongs to a later round. Sharpen fuzzy or conflicting terms into the project's own words. Stress-test a relationship with a concrete scenario when the boundary is the real issue.

Track:

- concepts and prototypes explored;
- hypotheses;
- learnings;
- emerging principles;
- decisions;
- remaining uncertainty;
- leading concept;
- next experiments.

Challenge contradictions and unnecessary scope directly. Conclude when a leading concept is named and remaining uncertainty is marked. Unasked branches become remaining uncertainty.

Keep a Concept Notebook under `docs/concepts/` covering those tracks. Update it as terms, decisions, and learnings crystallise. Point to the brief, docs, and checks rather than restating them.

The notebook is the deliverable.

Before finishing, run the `unslop` skill.
