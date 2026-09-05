---
name: ae-plan
description: See how a settled solution lands in this codebase. Use for multi-step work or slicing delivery.
---

# Plan

Problem and solution are settled enough. See how the solution lands in this codebase.

1. Read the request, relevant project lessons, and affected code until the current seams are visible.
2. Name the desired outcome and the gap between that codebase and it.
3. Identify choices whose wrong answer would cause meaningful rework. Resolve them from evidence, or ask one focused question when the user must decide. Leave the rest deferred.
4. Use the fewest vertical slices that deliver observable behavior on existing seams. Start with a walking skeleton when no end-to-end path exists. Give each slice acceptance criteria and the cheapest meaningful verification. Name a spike only when its result could change the implementation.
5. Write an Implementation Plan covering:

- desired outcome;
- relevant current codebase;
- gap;
- walking skeleton;
- vertical delivery slices;
- technical bets or spikes;
- deferred decisions;
- done criteria.

Every plan includes an Architecture section with current `docs/architecture/` references or `None`, intended boundary or relationship changes, affected invariants, and artifacts `ae-work` must update or create. State `No architecture change` when applicable. A material change may include a target Mermaid C4 diagram; repository architecture artifacts continue to describe verified current state.

Answer atomic work inline. Write multi-step work to one canonical file under `docs/plans/`. Point to code and earlier artifacts rather than restating them.

The Implementation Plan is the deliverable.

Before finishing, run the `unslop` skill.
