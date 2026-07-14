# Decision-Discovery Rubric

Use this internally after grounding. It finds missing decisions and creative opportunities; it is not a visible phase or a script of questions.

For every candidate gap:

1. Research it if it is discoverable.
2. Ignore it if it cannot materially change scope, behavior, architecture, or acceptance.
3. Record a minor default when the choice is low-impact.
4. Otherwise place the decision in the dependency map and ask it at the right time, with a recommendation.

## Lightweight

- Does this solve the actual problem?
- Does existing behavior already cover it?
- Is there a simpler framing with equal value?

## Standard

Include Lightweight, then check:

- **Evidence:** What observable behavior, workaround, cost, or user-held evidence supports the need? Ask only when the evidence belongs to the user and cannot be researched.
- **Actor and outcome:** Is the beneficiary specific enough, and is the change for them clear?
- **Current alternative:** What happens today, and what happens if nothing ships?
- **Product shape:** Which user-visible behavior or mechanism delivers the outcome?
- **Smallest valuable form:** What can be removed without losing the real value?
- **Boundaries:** What adjacent work is deliberately excluded or deferred?
- **Failure and edge cases:** Which failures materially alter expected behavior?
- **Success:** What observable signals establish that the work is acceptable or valuable?
- **Dependencies:** Which choices unlock or constrain later choices?
- **Combined consequences:** Do accepted decisions interact in a way the user has not approved?

## Deep

Include Standard, then check:

- Does the direction improve the broader system rather than create a local patch?
- Which decisions are costly to reverse?
- Which assumptions could invalidate the direction?
- What adjacent or inverted framing offers substantially more value without disproportionate carrying cost?

## Deep Product

Include Deep, then check:

- Who is the primary actor, and what core outcome defines the product?
- What is inside versus outside the product's identity?
- How is it positioned against current alternatives?
- Does the value proposition survive plausible near-term shifts?
- What adjacent product might accidentally be built instead?
- What must be true in the world for this direction to succeed or fail?

## Creativity Pass

For Standard and Deep work, deliberately test at least one lens before convergence:

- **Inversion:** would the opposite framing reveal a better shape?
- **Constraint removal:** is an assumed limitation hiding the best option?
- **Analogy:** does another domain solve the underlying problem more cleanly?
- **Adjacent value:** is there a low-carrying-cost addition with disproportionate upside?

Promote the result into the decision map only if it is credible and materially distinct. Creativity should improve the choice, not increase the option count.
