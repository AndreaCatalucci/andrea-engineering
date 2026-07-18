---
name: ce-brainstorm
description: 'Turn a vague or ambitious idea into confirmed requirements. Use while deciding what to build, before implementation planning; not for execution, debugging, code review, or choosing a project technology.'
---

# Brainstorm a Feature or Improvement

Immediately before writing user-facing text, read and follow
[`references/plain-language.md`](references/plain-language.md).

Resolve the decisions that define **what** to build. `ce-plan` later decides **how** to build it.

Research the facts, identify the questions that matter, and help the user answer
one question at a time. Propose useful options, challenge assumptions, and
point out concrete consequences the user may not have noticed.

Do not implement code. Do not write a plan, invoke a handoff, or take downstream action until the user explicitly confirms the final shared understanding.

## Conversation Rules

1. **One question per turn.** Ask it, wait, and use the answer before asking another. Never bundle related questions.
2. **Facts are researched.** If a fact can be established from the filesystem, repo, tools, or supplied material, look it up instead of asking the user. Verify before claiming, especially absence claims.
3. **Consequential decisions belong to the user.** Put choices to them when preference defines the product or a wrong answer materially changes value, risk, or rework. Use visible defaults for lower-cost choices.
4. **Recommend an answer.** Every decision question includes one clear recommendation and a short reason. Add up to two genuinely distinct alternatives only when they improve the choice.
5. **User-held facts stay open.** Goals, preferences, observed behavior, and lived experience may require a specific open-ended question. Do not recommend or fabricate these answers.
6. **Be proactive, not sprawling.** Point out overlooked constraints,
   opportunities, risks, edge cases, and later effects. Ask about one only when
   it changes scope, behavior, architecture, or acceptance.
7. **Default with judgment.** When one option is strongly supported and cheap to reverse, adopt it as a visible default even if it affects behavior. Expose defaults in the final synthesis so they can be corrected.
8. **Confirm the whole.** Individual answers are parts of the same proposal.
   End with a short summary and wait for explicit confirmation before writing
   a document or handing work to another skill.
9. **Define scope before dialogue.** Do not begin the decision interview until research supports a manageable proposed scope. Push back on work too broad for one coherent brainstorm.

Before the first decision question, read and follow [`references/codex-interaction.md`](references/codex-interaction.md). A useful decision turn normally has this shape:

```text
<brief context or consequence>

Recommendation: <answer> — <why it best fits the known goal and constraints>.

<optional: up to two alternatives with their material trade-off>

<one decision question>
```

## Intake and Routing

The feature description is the invoking prompt or current conversation. If none exists, ask: “What would you like to explore?” and wait.

Before interviewing:

- If requirements are already complete, research enough to verify them, present the shared-understanding synthesis, and wait for confirmation. Do not manufacture questions.
- If the request is a quick factual or single-step task, answer directly and stop this workflow.
- If it asks whether to adopt, switch to, or replace a named external technology, library, pattern, platform, or architecture for this project, read `references/verdict-routing.md` and offer `ce-pov`.
- For non-software decisions, use the same interview loop. Read
  `references/universal-brainstorming.md` only for its domain-specific guidance;
  do not use the software-plan format.
- If resuming a matching requirements-only plan, ask one decision: resume it or start fresh. Preserve its format unless the user requests a different one.

Classify the work silently as **Lightweight**, **Standard**, or **Deep**. Depth controls research and completeness, never the one-question interaction rule.

For Deep work, distinguish an extension of an established product from work that must establish the actor, core outcome, positioning, or primary flows. The latter requires product-level decisions.

## Assess Scope Before Questions

Use the prompt, available context, and an initial environment scan to assess **problem breadth before asking substantive questions**. Judge conceptual coherence, not implementation effort.

Consider:

- how many distinct actors and outcomes are involved;
- whether the request spans independent parts of the product or separate problems;
- whether one product thesis and boundary can organize the work;
- how many high-impact unknowns depend on unrelated decisions;
- whether one requirements document could stay clear and actionable.

A technically large feature may still be manageable when it serves one actor, outcome, and product shape. A request combining several independent outcomes or product theses is not manageable merely because they share a codebase.

If the scope is too broad for one conversation:

1. Explain the competing problem areas and why combining them would produce shallow or contradictory decisions.
2. Recommend the smallest useful part to work through first.
3. Offer at most two meaningfully different slices when useful.
4. Ask the user to choose one and wait. Do not begin detailed questioning until a slice is selected.

If the scope is manageable, form an internal **proposed scope** before dialogue:

- problem and desired outcome;
- primary actor;
- recommended product shape or direction;
- smallest valuable scope and major exclusions;
- highest-risk assumptions;
- why this is one coherent brainstorm.

Use best judgment to fill low-risk gaps and record them as defaults or assumptions. Ask a scope question only when no coherent thesis can be chosen without the user selecting between materially different problem boundaries.

Before the decision interview, show the user a compact working scope:

```text
Working scope: <problem, primary actor, desired outcome, and proposed boundary in 2–4 sentences>
Out of scope: <only the major exclusions needed to make the boundary legible>
```

This is a proposal, not a routine confirmation gate. When evidence strongly supports one coherent boundary, state it and continue to the highest-impact unresolved decision in the same turn. Ask the user to confirm scope only when two or more materially different boundaries remain genuinely plausible.

## Ground the Proposed Scope

Complete enough exploration to support or revise the proposed scope before asking substantive questions.

### Repo orientation

For software work, search for the topic, similar behavior, relevant plans,
conventions, vocabulary, and the affected parts of the codebase. Search first
and read only the relevant sections.

- **Lightweight:** a small inline scan.
- **Standard:** inline research, roughly 20 targeted reads at most.
- **Deep:** research inline when the affected code is cohesive. When it spans
  many areas, create a research note of at most 150 lines with `file:line`
  evidence.

The repo-profile cache may provide stable orientation. If needed, set `SKILL_DIR` to this skill's directory and run `python3 "$SKILL_DIR/scripts/repo-profile-cache.py" get`. On a miss, read `references/agents/repo-profiler.md`, derive its compact profile inline, and persist it with the same script. Never dispatch a profiler. If caching fails, continue with targeted inline research. The protocol lives in `references/repo-profile-cache.md`.

Use one extraction-only scout for deep research only when the affected code is
broad, unfamiliar, or cross-cutting enough to crowd out the conversation. Read
`references/delegation-budgets.md` before dispatching. Otherwise keep research
in the main thread.

Do not ask the user for discoverable facts such as existing routes, dependencies, schemas, config, or prior art. Tie consequential factual claims to evidence. Label anything that cannot be verified as an assumption.

Implementation details belong to `ce-plan` unless the product decision is itself architectural.

### Special exploration aids

- If the user lacks enough domain knowledge to evaluate upcoming decisions, read `references/blindspot-pass.md`. Map the territory before asking them to choose within it.
- If a material decision is inherently visual or spatial, read `references/visual-probes.md` and offer the cheapest useful visual probe. The probe supports one decision; it does not create a parallel dialogue.
- Search Slack only when the user explicitly requests it and the tools are available.

Read-only research and user-approved temporary probes are part of reaching understanding. They do not authorize writing the plan or taking downstream action.

## Build the Decision Map

Begin only after a manageable proposed scope exists. Candidate questions refine or challenge that thesis; they do not precede it.

Maintain a compact internal ledger throughout the conversation:

- **Facts:** verified, user-supplied, or explicitly uncertain.
- **Decided:** choices the user has answered.
- **Defaulted:** minor choices Codex proposes to carry into synthesis.
- **Unresolved:** material choices and their prerequisites.

Do not show the ledger mechanically. Use it to choose the next question.

Read `references/product-pressure-test.md` once after the initial research. Use
its checks internally to find missing questions and stronger options. Do not
show it as a separate phase or checklist.

Discover candidate decisions across:

- problem, evidence, actor, and desired outcome;
- product shape and user-visible behavior;
- scope boundaries, exclusions, and smallest valuable form;
- constraints, risks, failure modes, and edge cases;
- measures of success and acceptance criteria;
- dependencies, reversibility, and non-obvious combined consequences;
- adjacent or inverted ideas with meaningfully higher upside;
- for Deep-product work: positioning, durability, and product identity.

Remove questions that research can answer. Default choices when one answer is strongly supported and reversal is cheap. A question earns a turn only when user preference defines the product, plausible answers materially change scope or value, a wrong choice creates substantial rework or risk, or evidence cannot distinguish credible directions. Merely affecting behavior is not enough. Collapse coupled choices into the upstream decision when possible. Order what remains by dependency: ask the highest-upstream unresolved decision whose prerequisites are known. Prefer high-impact and hard-to-reverse decisions when several are ready.

## Run the Decision Interview

Do not enter this section until you have assessed the size of the request,
researched the relevant facts, and explained the proposed scope to the user.

For each turn:

1. Update the ledger from the user's last answer and new evidence.
2. Recompute which downstream decisions are now unlocked or made irrelevant.
3. Check for contradictions and combined consequences across earlier answers.
4. Select one material unresolved decision.
5. Give the recommendation, rationale, and at most two useful alternatives.
6. Ask only that question and wait.

Recommendations should be project-grounded and decisive. Prefer the simplest shape that delivers meaningful value, but include low-carrying-cost polish or delight when it materially improves the product. At least once in Standard or Deep work, test whether inversion, constraint removal, analogy, or an adjacent addition reveals a better option. Do not force a novelty option when it is weaker.

When a question concerns an approach, compare product behavior or mechanism rather than premature implementation details. Reuse, extension, and net-new behavior are useful distinctions. Present only options that a reasonable person might choose.

If the answer exposes uncertainty, resolve discoverable facts and then ask the resulting decision. If the user cannot decide because they lack domain knowledge, explain or map the territory before returning to the choice. Never decide for them.

Stop interviewing when no unresolved decision materially affects scope, behavior, architecture, or acceptance. Minor defaults and non-blocking uncertainties remain visible in synthesis.

## Verify Consequential Claims

Verify routine claims inline. Use one independent verifier only when a factual mistake could materially distort the direction or when a Deep claim remains unusually uncertain after targeted research. Read `references/delegation-budgets.md` before dispatching.

Give the verifier a short claim list and any research-note path. Require
`confirmed` with `file:line`, `refuted` with contradictory evidence, or
`unverifiable`. Correct refuted claims and record important unverifiable claims
as assumptions before the final summary.

No independent verifier is needed merely because the brainstorm is Standard or because a document may be written.

## Confirm Shared Understanding

Read `references/synthesis-summary.md` and produce the final synthesis. It must distinguish:

- what is being built and for whom;
- material decisions and their rationale;
- scope boundaries and meaningful exclusions;
- acceptance criteria or measures of success;
- defaults and assumptions;
- unresolved non-blockers, if any.

Ask the user to confirm or revise the complete synthesis. A revision is not confirmation: update the ledger, resolve any newly opened decisions one at a time, then present the complete synthesis again.

Do nothing downstream until the user explicitly confirms.

## After Confirmation

For software work, write or update a requirements-only plan only when the decisions are worth preserving. Resolve output format at composition time: explicit request, then known user preference, then active `brainstorm_output` in `.andrea-engineering/config.local.yaml`, otherwise markdown. Pipeline contexts force markdown. Preserve a resumed document's format unless explicitly overridden.

Read only the references needed at this point:

- `references/brainstorm-sections.md` for the requirements sections and whether
  a document is warranted.
- `references/html-rendering.md` or `references/markdown-rendering.md` for the selected format.

Write to `docs/plans/YYYY-MM-DD-NNN-<type>-<topic>-plan.<md|html>` with:

- `plan_format: andrea-plan/v1`
- `plan_readiness: requirements-only`
- `requirements_source: ce-brainstorm`

Keep the document requirements-only, concise, and standalone. Capture resolved project vocabulary in an existing root `CONCEPTS.md`; never create that file here.

For non-software work, keep the confirmed synthesis in chat unless the user chooses a durable document or a handoff to `ce-plan`.

Finally read `references/handoff.md` and offer only applicable next steps. This happens after confirmation and, when warranted, document creation—never before.
