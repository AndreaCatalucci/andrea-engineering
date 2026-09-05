---
name: ae-explore
description: Explore a solution direction. Use when a solution exists and how it should work is still open.
---

# Explore

The user has a solution direction. Explore how it could work.

Read the request and relevant project context. Bring discoverable facts into the conversation.

Compare different approaches where the choice matters. Treat each as a hypothesis.

When inspection cannot settle a consequential hypothesis, build the smallest runnable experiment that can. Name the question, decisive observation, and stopping condition first. Use the project's tools, representative data, and isolated or stubbed writes. Add only the interface and checks needed to answer the question. Record the result and decision. Keep requested runnable experiments with a run command; remove disposable scratch work outside that deliverable. Production implementation uses `ae-work` and its verification criteria.

Finding facts is your job. When a hypothesis is cheap to check, check it: curl a public API to see its real response shape, auth, and rate limits; fetch a site's terms or pricing page to check licensing; read the relevant docs; run a quick snippet to confirm a claim. Look up what the code, docs, and environment already answer, and check claims against the code. Put only decisions to the user.

Ask only decisions that materially affect the next experiment or implementation and require the user's judgment. Batch independent questions sparingly, give recommended answers with concrete alternatives, and wait for required decisions. Resolve routine reversible choices from the available evidence.

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

Keep one bounded decision inline. For multi-round exploration or a requested artifact, maintain a Concept Notebook under `docs/concepts/` covering the relevant tracks. Point to evidence rather than restating it.

The deliverable is the decision and its evidence, plus any requested runnable experiment. Unobserved results remain open.

Before finishing, run the `unslop` skill.
