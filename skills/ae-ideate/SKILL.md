---
name: ae-ideate
description: Decide which product idea is worth pursuing. Use for an unsolved user problem, product opportunities, competing directions, or Impact and Wardley mapping.
---

# Ideate

Act as a product leader responsible for choosing useful work. Understand the problem, consider what people already use, and recommend where to spend effort. Explain the customer behavior and tradeoff behind each claim in ordinary language.

## Understand the opportunity

1. Read the request and relevant project evidence: product decisions, user feedback, support issues, usage, and known constraints. Name who struggles, in what situation, how they cope today, and what it costs them. Separate a requested feature from the underlying need. For commercial products, distinguish the user from whoever buys or approves it.
2. State the outcome that would make this worth doing and why now. Use observed frequency, time, cost, or failures where available; label proposed targets and unknowns. Ask only for missing information that could change the recommendation and cannot be discovered. Otherwise state the assumption and proceed.
3. Inspect the closest alternatives, including competitors, existing product features, manual work, and doing nothing. For market-facing ideas, check current product pages, pricing, documentation, and relevant customer evidence. Compare the actual task, audience, price or effort, and limitations that matter here. Start with the closest substitute and expand only if another could change the choice. Separate supplier claims and stated interest from observed use or willingness to pay. Missing evidence remains unknown.

## Develop and choose ideas

4. Use Impact Mapping to connect **outcome → people → behavior change → possible solutions**. Include people who can enable or block adoption when relevant. Generate alternatives at the behavior-change step, so the ideas solve the problem in different ways. For example: fewer missed appointments → patients → remember, reschedule early, or attend remotely → reminders, easier rescheduling, or remote appointments. These links are hypotheses to check.
5. Compare a few credible options, including a simpler process or buying an existing solution when plausible. Explain who benefits, why they would change their current behavior, and why this team or product can serve them well. Weigh expected benefit against building, operating, supporting, and adopting it. For a new product, explain how the first users could be reached and why they would switch. Prefer reasoned tradeoffs to invented scores or market-size estimates.

Load [wardley.md](recipes/wardley.md) when deciding what to build or buy, where competitors already provide enough, how supplier or market changes affect the idea, or when a Wardley map is requested. Use its conclusions to revise the options.

6. Recommend **pursue, test first, defer, or drop**. Name the strongest reason against your recommendation and the observation that would change it. Choose the cheapest next action that resolves the most consequential uncertainty: specify what to examine or try, with whom or what data, and what result would support continuing or stopping. Perform useful read-only checks now; propose customer contact or runnable experiments without initiating them unless requested.

## Return the decision

Lead the Opportunity Brief with the recommendation and its reason. Include only what the decision needs:

- who has the problem and what improves for them;
- evidence and relevant alternatives, with source links and material unknowns;
- options considered and why the recommendation wins;
- the first useful scope and what to leave out;
- the next action, its decision criterion, and what could overturn the recommendation.

Maps are working material; show them when requested or when they clarify the decision. Answer bounded questions inline; save multi-round work or requested artifacts under `docs/ideation/`. Stop when the evidence supports a choice or a specific next test. Use `ae-explore` when the chosen direction needs design or experimentation, and `ae-plan` when it is ready to land in the codebase.

Optional background: [Impact Mapping](https://www.impactmapping.org/).

Before finishing, run the `unslop` skill.
