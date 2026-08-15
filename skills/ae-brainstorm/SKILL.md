---
name: ae-brainstorm
description: Turn an unclear idea into confirmed requirements through an interactive question-and-answer session. Use before planning; not for open-ended idea generation or implementation.
---

# Brainstorm

Help the user decide what to build.

First read the request and any directly relevant project context. Do not ask for facts that can be discovered cheaply.

Ask one useful question at a time. Keep each turn under 100 words and prefer concrete alternatives with a recommendation when the choice is bounded. Use free-form questions when fixed choices would hide the real decision.

Track only decisions that affect the product:

- goal and user;
- essential behavior;
- important boundaries and non-goals;
- consequential tradeoffs;
- observable success;
- unresolved blockers.

Challenge contradictions and unnecessary scope directly. Stop asking when a competent planner could proceed without inventing a product decision.

Finish with at most 500 words of confirmed requirements and clearly marked remaining blockers. Do not add architecture, implementation steps, review, or validation ceremony.

Stay in chat by default. If the user asks to preserve the result, write a short requirements document under `docs/plans/`. Write or update `STRATEGY.md` only when explicitly requested.
