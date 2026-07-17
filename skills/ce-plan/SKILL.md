---
name: ce-plan
description: "Create structured plans for multi-step work, including software and non-software tasks. Use when asked to plan, break down implementation, plan from requirements, or deepen an existing plan; prefer ce-brainstorm for exploratory framing."
---

# Create Technical Plan

Turn a product contract, feature request, bug report, or rough description into the shortest implementation-ready plan that preserves every load-bearing decision.

`ce-brainstorm` defines what to build. `ce-plan` adds how to build it. `ce-work` executes the implementation-ready artifact. A brainstorm is useful, never required.

## Completion Contract

A software planning run completes only when:

- one canonical plan exists in `docs/plans/`;
- external sources that shape implementation are established or recorded as blockers;
- each implementation-ready unit names real repo-relative implementation and test paths;
- confidence checking and required document review completed or took a documented format/interactive skip;
- the final compactness and concreteness audits pass;
- the absolute plan path and review state are returned.

Do not implement code, run downstream workflows, or require a separate handoff choice.

## Primary Rule

Write the shortest plan from which a competent implementer can begin without making a load-bearing product or architecture decision.

Depth follows unresolved decisions and implementation ambiguity. Risk strengthens validation, failure handling, rollout, and tests; it does not by itself justify more sections, abstractions, diagrams, or prose.

Soft budgets:

| Depth | Words | Implementation units |
|---|---:|---:|
| Lightweight | 500-1,000 | 2-4 |
| Standard | 1,000-2,000 | 3-5 |
| Deep | Over 2,000 only when additional decisions cannot be expressed more compactly | Usually 4-8 |

An explicit request for a short, concrete, simple, or practical plan selects the compact end of the applicable range. Exceeding a budget is allowed only for material decisions, not ceremony.

A focused feature with no more than four outcome units targets at most 1,500
words, even when it handles external data or other high-risk behavior. Exceeding
that cap requires a documented P0/P1 correctness reason naming the decision
that could not be expressed compactly.

## Interaction and Safety

- When a blocking decision is genuinely necessary, ask one question at a time with `request_user_input` when available; otherwise ask in chat and wait.
- In pipeline or `disable-model-invocation` contexts, do not block. Make reversible choices, expose assumptions, and force Markdown output.
- Use repo-relative paths inside plans. Absolute paths are permitted only in the chat handoff so the artifact is clickable.
- Honor user-named files, URLs, CLIs, tools, and prior artifacts. Discover them before substituting.
- A direct invocation always stays in a planning workflow. If the prompt lacks a feature description, ask what to plan.

## Route the Request

Apply these routes in order:

1. **Output format.** Resolve `md` or `html` from explicit request or `output:` token, then known user preference, active `plan_output` in `.andrea-engineering/config.local.yaml`, otherwise Markdown. Pipeline mode forces Markdown. Read `references/plan-sections.md` and exactly one of `references/markdown-rendering.md` or `references/html-rendering.md` before composition.
2. **Existing artifact.** A referenced implementation-ready plan is an edit/resume target. A requirements-only unified plan is enrichment input, not a resume prompt. Preserve its format unless explicitly converting it or pipeline mode forces Markdown.
3. **Deepen intent.** For an explicit whole-plan deepening request, skip to Confidence and Review in interactive mode. Read `references/deepening-workflow.md` and `references/plan-handoff.md`. Section-specific edits use the normal resume path.
4. **Approach altitude.** When the user explicitly asks for a plan of approach rather than the deliverable, read `references/approach-altitude.md`. Offer this route proactively only when both method uncertainty and cost of being wrong are clearly high.
5. **Task domain.** Software modification continues below. Non-software planning and answer-seeking work reads `references/universal-planning.md` and stops after that workflow. Classify by requested action, not by whether the topic mentions code or data.

Recognized control tokens are consumed, not treated as feature text. `confirm:auto` skips only the scoping-confirmation gate; `confirm:ask` forces it. Pipeline mode also skips that gate. Unknown `output:` values are ignored with a final note; unrelated colon-prefixed text remains part of the request.

## Workflow

### 1. Establish the Product Contract

Resolve planning input in this order:

1. explicit unified plan or legacy requirements path;
2. a recent topic-matching requirements-only unified plan under `docs/plans/`;
3. a matching legacy `docs/brainstorms/*-requirements.{md,html}` artifact;
4. the user's request, producing a `ce-plan-bootstrap` Product Contract.

When enriching `artifact_contract: ce-unified-plan/v1` with `artifact_readiness: requirements-only`, update it in place and preserve Product Contract text and stable R/A/F/AE IDs. Record whether the Product Contract changed. Confirm before making a substantive product-scope change.

When using a legacy artifact, preserve its intent, scope boundaries, requirements, decisions, dependencies, questions, and relevant IDs. Carry its path in `origin:` and write a new unified plan.

Without an upstream contract, establish enough product clarity to plan responsibly. Recommend `ce-brainstorm` when product framing is the unresolved problem, but allow the user to continue here.

Classify remaining questions:

- **Planning blocker:** a load-bearing product, source, architecture, security, or data decision; resolve now or keep the artifact non-implementation-ready.
- **Planning assumption:** a reversible choice that can proceed when stated explicitly.
- **Implementation discovery:** a bounded detail the implementer can resolve without changing product or architecture; defer to its unit.

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

Use user-named sources first, then official primary documentation. Research unknown facts instead of asking the user. Reject vague contracts such as “use CEREP data,” “consume provider statistics,” or “import the official files.”

If a source detail materially affects implementation and cannot be established after reasonable research:

- do not design a generic importer around the unknown;
- record the missing authority/acquisition contract as a blocking open question;
- leave `artifact_readiness` as `requirements-only` or otherwise explicitly non-implementation-ready;
- stop before implementation units that would pretend the source is known.

Write a compact requirements-only blocker artifact containing the goal, known
source facts and research attempts, the exact missing contract, and the
blocking open question. Omit architecture, KTDs, implementation units, and
deepening, then run only the applicable final artifact checks and handoff.

The gate completes only when the exact source contract is cited or the artifact clearly names the blocker and is not implementation-ready.

### 3. Ground the Plan in the Repository

Inspect the repository before structuring the plan:

- governing instructions and existing plan conventions;
- entry points, domain models, data flow, tests, and operator surfaces;
- at least two analogous local patterns when available;
- relevant `docs/solutions/`, `CONCEPTS.md`, and git history when they affect the decision;
- repo-specific verification commands.

Use the repo-profile cache when available; it is orientation, not evidence. Prefer existing deep modules and established seams over new frameworks. External best practices supplement thin local evidence; they do not override project conventions without a stated reason.

Consolidate research into only what changes the plan: exact source contracts, patterns to follow, constraints, rejected alternatives, and remaining blockers.

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
- **Input:** exact artifact, request, record set, or trigger required.
- **Operation:** operator-facing job, command surface, or workflow that processes it.
- **Outcome:** observable condition proving success.

For external-data plans, prefer one compact path:

`Source -> Import -> Transform -> Apply -> Publish -> Verify`

Do not lead with generic architecture, governance, lifecycle, or abstraction sections.

Apply “one fact, one home”:

- Requirements define behavior.
- KTDs explain only load-bearing choices.
- Implementation units say where and how work lands.
- Verification proves requirements.
- Definition of Done summarizes completion without restating the plan.

For focused work, use 4-8 requirements and 2-5 KTDs unless the final audit names
the independent behavior or decision that requires each additional item.
Stable IDs remain required, but item count is not a quality target. Keep only
acceptance examples that disambiguate conditional or failure behavior; do not
mirror every requirement with an example.

Build implementation units around independently understandable outcomes, not architectural layers. Combine codecs, receipts, lifecycle handling, orchestration, readiness, rollback, and documentation into the outcome they serve unless one is independently valuable. Each feature-bearing unit names:

- one outcome-oriented goal and covered requirement IDs;
- real repo-relative implementation files;
- real repo-relative test files;
- existing patterns to follow;
- approach and dependencies;
- concrete happy-path, edge, failure, and integration scenarios when applicable;
- observable verification.

Do not invent abstractions for hypothetical reuse. Read `references/plan-sections.md` for the complete unified artifact contract and section ownership.

### 6. Choose the Smallest Useful Representation

Use prose or a short numbered flow by default. Add a diagram only when it communicates a non-obvious relationship, state transition, branch, or multi-party sequence more clearly than text.

Three components or three stages alone do not require a diagram. A compact plan uses at most one small flow unless additional diagrams each resolve a distinct, load-bearing ambiguity. Never add diagrams to satisfy trigger categories.

Load the format-specific rendering reference selected in Route the Request. Its presentation rules do not expand the content contract.

### 7. Write the Unified Artifact

Write software plans to:

`docs/plans/YYYY-MM-DD-NNN-<type>-<descriptive-name>-plan.<md|html>`

For implementation-ready software plans set:

- `artifact_contract: ce-unified-plan/v1`
- `artifact_readiness: implementation-ready`
- `execution: code`

Requirements-only blockers must not be mislabeled implementation-ready. Universal, answer-seeking, and approach-plan outputs do not receive the unified software contract unless they contain it fully.

Update a requirements-only unified artifact in place unless format conversion requires a sibling. Preserve Product Contract IDs and content; add Planning Contract, Implementation Units, Verification Contract, and Definition of Done. Preserve `ce-work`'s stable U-ID contract: never renumber surviving units after reordering, splitting, or deletion.

Do not include implementation code, git choreography, exact method signatures, or an execution prompt. Directional pseudocode is allowed only when it communicates a load-bearing design.

If `CONCEPTS.md` already exists, add only missing project-specific domain concepts used by the plan. Do not create the file.

### 8. Confidence and Document Review

Run `scripts/plan-metrics.py <plan-path>` and record its pre-review word and
implementation-unit counts.

Use confidence deepening only for material gaps in rationale, sequencing, source grounding, risks, or system impact. Lightweight plans normally skip it unless a real gap remains. When warranted, read `references/deepening-workflow.md`; select only the specialist lenses justified by the gap.

Then read `references/plan-handoff.md`. Markdown plans run `ce-doc-review mode:headless`; HTML plans take its documented format skip.

Review changes should replace, clarify, consolidate, or delete existing text. Adding a section, KTD, diagram, abstraction, or implementation unit requires evidence that the plan would otherwise be unimplementable.

After review, run the metrics script again. Growth above 10% requires a
documented P0/P1 correctness reason. Without one, compress the review changes
back into the selected budget while preserving the fix. “Stronger, not longer”
is a mechanical gate, not a preference.

### 9. Final Audits and Handoff

Before returning, verify:

- every external source has exact authority and acquisition path;
- the Source/Input/Operation/Outcome path appears within the first 25 lines;
- every unit names real implementation and test files;
- the operator-facing action and observable success condition are identifiable;
- no abstraction exists only for hypothetical reuse;
- one fact has one home;
- removing any section would lose an actual decision; otherwise remove it;
- word and unit budgets pass, including the post-review growth check;
- origin decisions and stable IDs remain intact;
- the artifact exists at one canonical path.

Confirm with the absolute path:

`Plan written to <absolute-path>`

Return the plan path, depth, word count, unit count, source-gate state, and one concise review summary. Mention optional next steps without invoking them or presenting a blocking menu.
