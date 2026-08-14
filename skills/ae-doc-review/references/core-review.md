# Core Review

Apply this pass to the full document. Retain only findings that meet the reviewer contract.

## Internal coherence

- Find passages that cannot both be true.
- Resolve broken references, duplicate or missing identifiers, and header/body count mismatches.
- Flag terminology drift only when readers could implement different meanings.
- Check that summaries, diagrams, tables, and detailed sections agree.

When one passage is clearly authoritative, a local reconciliation may be `mechanical`. If authority is uncertain, use `decision`.

## Traceability

For requirements, trace goals to requirements, actors, flows, and acceptance examples. Find orphan requirements and goals with no supporting behavior.

For plans, trace requirements to work steps and each step to an affected area
and observable verification. Require exact files, dependencies, or test cases
only when they preserve an important decision or control a material risk. Do
not demand plan-level detail from requirements documents.

For unified documents, review What We're Building as the requirements. When the
plan is ready to implement, review How We'll Build It and the work steps as the
implementation plan.

## Scope and simplicity

- Identify work that serves no stated goal.
- Identify goals the proposed work cannot achieve.
- Challenge new abstractions, frameworks, configuration, or generic utilities without a current consumer.
- Check that deferred or out-of-scope work has not returned through an work step.
- Check priority dependencies: a higher-priority item must not silently depend on a deferred or lower-priority item.

Do not flag optional future improvements merely because they are possible.

## Decision readiness

- Find choices hidden behind vague language, undefined ownership, missing thresholds, or non-exhaustive behavior.
- Distinguish a deliberate deferral from a decision implementers would be forced to guess.
- For plans, require rollout, compatibility, error handling, and verification only where relevant to the proposed change.
- For requirements, require enough behavioral clarity to plan the work, not implementation mechanics.

## Mechanical corrections

Use `mechanical` only when the document itself proves one exact correction, such as:

- a wrong count;
- a stale internal reference with one valid target;
- a minority term that clearly denotes the same concept as the dominant term;
- a summary that contradicts a more specific authoritative passage;
- an exhaustive list missing a peer explicitly established elsewhere.

Typos or syntax errors caught reliably by ordinary linters are not review findings.
