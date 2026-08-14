---
name: ae-plan
description: "Plan multi-step work with implementation guardrails. Use when asked to plan software or non-software work, break down implementation, plan from requirements, or revise an existing plan; prefer ae-brainstorm when the user is still deciding what to build."
---

# Create Technical Plan

When writing text the user will read, reuse their words and the repository's
existing names. Keep workflow labels, routing terms, and prompt terminology
out of the result. Leave metadata keys, stable IDs, code, commands, and
existing project terms unchanged.

Turn requirements, a feature request, a bug report, or a rough description into
the shortest plan that lets implementation begin without reopening important
decisions.

A plan is a set of guardrails, not an execution script. Settle choices whose
wrong answer would cause material risk or rework. Leave local coding choices to
the implementer unless the plan has evidence that one choice matters.

`ae-brainstorm` defines what to build. `ae-plan` explains how to build it.
`ae-work` carries out the finished plan. A brainstorm can help, but is not
required.

## Completion Requirements

A software planning run completes only when:

- one canonical plan exists in `docs/plans/`;
- external sources that shape implementation are established or recorded as blockers;
- each implementation-ready step passes the guardrail rules in
  `references/plan-sections.md`;
- confidence checking and required document review completed or took a documented format/interactive skip;
- the final compactness and concreteness audits pass;
- the absolute plan path and review state are returned.

Do not implement code, run downstream workflows, or require a separate handoff choice.

## Primary Rule

Write the shortest plan from which a competent implementer can begin without
making an important product or architecture decision that the plan should have
settled.

Depth follows unresolved decisions and implementation ambiguity. Risk strengthens validation, failure handling, rollout, and tests; it does not by itself justify more sections, abstractions, diagrams, or prose.

Soft budgets:

| Depth | Words | Work steps |
|---|---:|---:|
| Lightweight | 300-700 | 1-3 |
| Standard | 700-1,200 | 2-5 |
| Deep | Over 1,200 only when additional decisions cannot be expressed more compactly | Usually 4-7 |

An explicit request for a short, concrete, simple, or practical plan selects the compact end of the applicable range. Exceeding a budget is allowed only for material decisions, not ceremony.

A focused feature with no more than four outcome steps targets at most 1,000
words, even when it handles external data or other high-risk behavior. Exceeding
that cap requires a documented P0/P1 correctness reason naming the decision
that could not be expressed compactly.

## Interaction and Safety

- When a blocking decision is genuinely necessary, read and follow [`references/codex-interaction.md`](references/codex-interaction.md).
- In pipeline or headless contexts, do not block. Make reversible choices, expose assumptions, and force Markdown output.
- Use repo-relative paths inside plans. Absolute paths are permitted only in the chat handoff so the document is clickable.
- Honor user-named files, URLs, CLIs, tools, and prior documents. Discover them before substituting.
- A direct invocation always stays in a planning workflow. If the prompt lacks a feature description, ask what to plan.

## Route the Request

Apply these routes in order:

1. **Output format.** Resolve `md` or `html` from explicit request or `output:` token, then known user preference, active `plan_output` in `.andrea-engineering/config.local.yaml`, otherwise Markdown. Pipeline mode forces Markdown. Read `references/plan-sections.md` and exactly one of `references/markdown-rendering.md` or `references/html-rendering.md` before composition.
2. **Existing document.** A referenced implementation-ready plan is an edit/resume target. A requirements-only plan is enrichment input, not a resume prompt. Preserve its format unless explicitly converting it or pipeline mode forces Markdown.
3. **Deepen intent.** For an explicit whole-plan deepening request, skip to Confidence and Review in interactive mode. Read `references/deepening-workflow.md` and `references/plan-handoff.md`. Section-specific edits use the normal resume path.
4. **Plan the method first.** When the user explicitly asks how to approach the
   planning work, read `references/approach-altitude.md`. Suggest this route
   only when the method is genuinely unclear and choosing badly would be costly.
5. **Task domain.** Software modification continues below. Non-software planning and answer-seeking work reads `references/universal-planning.md` and stops after that workflow. Classify by requested action, not by whether the topic mentions code or data.

Recognized control tokens are consumed, not treated as feature text. `confirm:auto` skips only the scoping-confirmation gate; `confirm:ask` forces it. Pipeline mode also skips that gate. Unknown `output:` values are ignored with a final note; unrelated colon-prefixed text remains part of the request.

## Workflow

### 1. Confirm What We Are Building

Resolve planning input in this order:

1. an explicit `andrea-plan/v1` plan path;
2. a recent topic-matching requirements-only plan under `docs/plans/`;
3. the user's request, producing a `ae-plan-bootstrap` What We're Building.

When enriching `plan_format: andrea-plan/v1` with
`plan_readiness: requirements-only`, update it in place and preserve the
text under What We're Building and the stable R/A/F/AE IDs. Record whether the
requirements changed. Confirm before making a substantive product-scope change.

Without existing requirements, clarify enough product behavior to plan
responsibly. Recommend `ae-brainstorm` when the user has not yet decided what
to build, but allow them to continue here.

Classify remaining questions:

- **Planning blocker:** an important product, source, architecture, security, or
  data decision; resolve it now or mark the plan as not ready to implement.
- **Planning assumption:** a reversible choice that can proceed when stated explicitly.
- **Detail to verify while coding:** a bounded detail the implementer can resolve without changing product or architecture; defer to its step.

### 2. Establish External Sources Before Architecture

This is a hard gate whenever work depends on external data, an API, portal, standard, provider, or imported files.

Before designing importers, abstractions, schemas, or orchestration, establish:

- authoritative owner;
- exact official URL or documented endpoint;
- acquisition method;
- required filters, parameters, or selection criteria;
- expected files, exports, response fields, or schemas;
- provenance captured during import;
- the boundary between immutable raw source data and project-derived data.

Use user-named sources first, then official primary documentation. Research
unknown facts instead of asking the user. Reject vague source descriptions such
as “use CEREP data,” “consume provider statistics,” or “import the official
files.”

If a source detail materially affects implementation and cannot be established after reasonable research:

- do not design a generic importer around the unknown;
- record the missing authority and how to get the source as a blocking open question;
- leave `plan_readiness` as `requirements-only` or otherwise explicitly non-implementation-ready;
- stop before work steps that would pretend the source is known.

Write a compact requirements-only blocker document containing the goal, known
source facts and research attempts, the exact missing source details, and the
blocking open question. Omit architecture, technical decisions, work steps, and
deepening, then run only the applicable final document checks and handoff.

The gate completes only when the exact source details are cited or the document clearly names the blocker and is not implementation-ready.

### 3. Check the plan against the repository

Inspect the repository before structuring the plan:

- governing instructions and existing plan conventions;
- entry points, domain models, data flow, tests, and operator surfaces;
- at least two analogous local patterns when available;
- relevant `docs/solutions/`, `CONCEPTS.md`, and git history when they affect the decision;
- repo-specific verification commands.

Use the repo-profile cache when available; it is orientation, not evidence. Prefer existing deep modules and established seams over new frameworks. External best practices supplement thin local evidence; they do not override project conventions without a stated reason.

Keep only research that changes the plan: exact source details, patterns to
follow, constraints, rejected alternatives, and unanswered blockers.

### 4. Select Depth and Resolve Decisions

Choose depth from unresolved decisions and ambiguity:

- **Lightweight:** the implementation path is established and only a few bounded decisions remain, even if several files change.
- **Standard:** multiple components or meaningful choices require coordination.
- **Deep:** genuinely cross-cutting or novel work has several irreducible decisions that cannot be summarized compactly.

File count and risk are not depth proxies. A broad mechanical change may remain Lightweight; a small authorization change may require stronger verification without becoming a long plan.

Resolve planning blockers one at a time. Prefer a recommendation with rationale. Do not ask for discoverable facts.

For brainstorm-sourced Standard or Deep work, or Lightweight work with meaningful call-outs, read `references/synthesis-summary.md`, present the compact scoping synthesis, and wait unless pipeline/`confirm:auto` applies. Lightweight work with no surviving call-outs auto-proceeds.

### 5. Structure Source to Outcome

Within the first 25 lines of the plan, make the execution path explainable:

- **Source:** authoritative origin of the input, or “internal” when no external source exists.
- **Input:** exact document, request, record set, or trigger required.
- **Operation:** operator-facing job, command surface, or workflow that processes it.
- **Outcome:** observable condition proving success.

For external-data plans, prefer one compact path:

`Source -> Import -> Transform -> Apply -> Publish -> Verify`

Do not lead with generic architecture, governance, lifecycle, or abstraction sections.

Apply “one fact, one home”:

- Requirements define behavior.
- technical decisions explain only important technical choices.
- Work steps say where and how work lands.
- Verification proves requirements.
- Done When summarizes completion without restating the plan.

For focused work, use 4-8 requirements and 2-5 technical decisions unless the final audit names
the independent behavior or decision that requires each additional item.
Stable IDs remain required, but item count is not a quality target. Keep only
acceptance examples that disambiguate conditional or failure behavior; do not
mirror every requirement with an example.

Build work steps around independently understandable outcomes, not
architectural layers. Keep supporting work with the outcome it serves unless
it is useful on its own. A step sets the boundary and proof; it does not narrate
the coding. Exact files, patterns, sequencing, and test cases belong only when
they preserve an important decision or control a material risk. Defer other
details to implementation.

Before composing, read `references/plan-sections.md`. It is the single source
of truth for the plan sections and work-step fields. Do not invent abstractions
for hypothetical reuse.

### 6. Choose the Smallest Useful Representation

Use prose or a short numbered flow by default. Add a diagram only when it communicates a non-obvious relationship, state transition, branch, or multi-party sequence more clearly than text.

Three components or stages alone do not require a diagram. A compact plan uses
at most one small flow unless another diagram clears up a different important
ambiguity. Never add diagrams merely because a category suggests one.

Load the format-specific rendering reference selected in Route the Request. Its presentation rules do not expand the content rules.

### 7. Write the Plan

Write software plans to:

`docs/plans/YYYY-MM-DD-NNN-<type>-<descriptive-name>-plan.<md|html>`

For implementation-ready software plans set:

- `plan_format: andrea-plan/v1`
- `plan_readiness: implementation-ready`
- `execution: code`

Requirements-only blockers must not be mislabeled implementation-ready. Universal, answer-seeking, and approach-plan outputs do not use the Andrea plan format unless they contain every required section.

Update a requirements-only plan in place unless format conversion requires a sibling. Preserve What We're Building IDs and content; add How We'll Build It, Work Steps, How We'll Check It, and Done When. Never renumber surviving W-IDs after reordering, splitting, or deletion.

Do not include implementation code, detailed git steps, exact method
signatures, or an execution prompt. Use brief pseudocode only when it makes an
important design easier to understand.

If `CONCEPTS.md` already exists, add only missing project-specific domain concepts used by the plan. Do not create the file.

### 8. Confidence and Document Review

Run `scripts/plan-metrics.py <plan-path>` and record its pre-review word and
work-step counts.

Add more detail only when the plan still has a real gap in reasoning, order of
work, source evidence, risks, or system impact. Lightweight plans normally skip
this. When needed, read `references/deepening-workflow.md` and choose only the
reviewers that address the gap.

Then read `references/plan-handoff.md`. Markdown plans run `ae-doc-review mode:headless`; HTML plans take its documented format skip.

Review changes should replace, clarify, consolidate, or delete existing text. Adding a section, D, diagram, abstraction, or work step requires evidence that the plan would otherwise be unimplementable.

After review, run the metrics script again. Growth above 10% requires a
documented P0/P1 correctness reason. Without one, compress the review changes
back into the selected budget while preserving the fix. “Stronger, not longer”
is a mechanical gate, not a preference.

### 9. Final Audits and Handoff

Before returning, verify:

- every external source has exact authority and acquisition path;
- the Source/Input/Operation/Outcome path appears within the first 25 lines;
- every step passes the guardrail test in `references/plan-sections.md`;
- the operator-facing action and observable success condition are identifiable;
- no abstraction exists only for hypothetical reuse;
- no implementation choice is prescribed without a material risk or rework
  reason;
- one fact has one home;
- removing any section would lose an actual decision; otherwise remove it;
- word and step budgets pass, including the post-review growth check;
- origin decisions and stable IDs remain intact;
- the document exists at one canonical path.

Confirm with the absolute path:

`Plan written to <absolute-path>`

Return the plan path, depth, word count, step count, source-gate state, and one concise review summary. Mention optional next steps without invoking them or presenting a blocking menu.
