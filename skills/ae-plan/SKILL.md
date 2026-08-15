---
name: ae-plan
description: Produce the shortest implementation plan that settles consequential choices. Use for multi-step work or to turn confirmed requirements into executable steps.
---

# Plan

Plan enough for implementation to begin without reopening an important decision.

1. Read the request or requirements and inspect the smallest relevant part of the repository.
2. Identify choices whose wrong answer would cause meaningful rework. Resolve them from evidence or ask one focused question when the user must decide.
3. Prefer existing seams and delete unnecessary abstraction from the proposed approach.
4. Write 2-4 outcome-sized work steps. Name affected areas only when they help the implementer start.

Keep the plan under 700 words unless the user explicitly asks for depth. Include:

- goal;
- confirmed requirements;
- consequential technical decisions;
- work steps;
- a short completion condition.

Omit review workflows, validation frameworks, test matrices, diagrams, appendices, source bureaucracy, and exhaustive file lists unless one is essential to the requested change.

For atomic work, answer inline instead of creating a document. Otherwise write or update one canonical file under `docs/plans/`. Do not implement the plan or invoke another skill automatically.
