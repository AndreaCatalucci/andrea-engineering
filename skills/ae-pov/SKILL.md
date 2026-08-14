---
name: ae-pov
description: "Verdict on whether an external technology, pattern, platform, architecture, or ecosystem change fits this project. Use for project-grounded adoption decisions or second opinions; not neutral explanation or ideation."
---

# Form a Point of View

When writing text the user will read, reuse their words and the repository's
existing names. Keep workflow labels, routing terms, and prompt terminology
out of the result. Leave metadata keys, stable IDs, code, commands, and
existing project terms unchanged.

Return a clear recommendation about an external technology, pattern, or
platform based on how well it fits this project.

The subject of this point of view — the thing to judge — is the input this skill was invoked with, present in the current prompt or conversation (whether the user asked directly or a calling skill passed it).

## Base the Answer on Evidence

Do not recommend something until two kinds of evidence exist (see
`references/method.md`):

- **Project evidence:** at least one verified fact showing what the project uses
  now, where the proposed change would apply, or what the team decided before.
- **External evidence:** at least one verified primary or authoritative source.

Both are required. A strong article cannot replace reading the project, and a
project detail cannot establish what an external technology actually does.

## Interaction Method

Before asking the user for input, read and follow [`references/codex-interaction.md`](references/codex-interaction.md).

## Codex Agents

Dispatch scouts with `spawn_agent` and let them inherit the parent Codex model. Keep verdict reasoning—the two-floor gate, skeptic synthesis, and verdict contract—in the main conversation. Bound cost with the existing read budgets and scout count.

## Execution Flow

### Phase 0: Decide the Question and Risk

**Output mode:** by default `ae-pov` writes no document — the verdict is a compact chat block. An optional full write-up and a durable `ae-compound` capture are available on request at Phase 4. Do not resolve an `OUTPUT_FORMAT` or load a rendering reference up front.

1. **Detect the invocation context — cold or warm.** Warm means `ae-pov` was
   invoked mid-session for a second opinion, with the question in the surrounding
   conversation or absent. For the warm-invocation rules—use only the question
   and claims to verify, return control afterward, and keep evidence groups
   separate—read `references/invocation.md`.

2. **Confirm the question before researching it.** A link to a new sign-in
   method might mean “adopt it,” “migrate to it,” “compare it with what we use,”
   or simply “explain it.” Read just enough to identify the subject, then settle
   the exact question. If the intent is unclear, read `references/intake.md`,
   propose the 2-3 likely questions, and ask the user to choose. Do not research
   several guessed questions in parallel.

3. **Apply the selection escape hatch.** If the input is a *selection* over a field ("what should we use for auth?"), it belongs here only when the realistic field is bounded (roughly five or fewer real candidates) and the criteria are knowable. If the field can't be bounded without inventing options, or the criteria are unclear, **stop**: return a Hold and route to `ae-ideate` (to enumerate) or `ae-brainstorm` (to surface criteria), then offer to re-run. Read `references/boundaries.md` only when the input's fit for `ae-pov` is genuinely in doubt or the field can't be bounded; skip it for a clearly in-scope verdict.

4. **Classify how hard the choice is to undo.** Infer it from the project:
   - **Tier 1 — easy to undo:** a dependency, lint rule, or configuration change.
   - **Tier 2 — costly but contained:** a data store, internal API, or migration
     whose effects stay inside this codebase.
   - **Tier 3 — hard to undo or high risk:** security, legal, privacy, a public
     API, or an irreversible data migration.

   State the tier in the verdict and let the user override. The tier sizes the rest of the run (Phase 1 scout count, Phase 2 depth, Phase 3 reversal trigger): Tier 1 stays a one-screen verdict off a single combined evidence pass; Tier 2 adds the full scout fleet and an alternatives pass; Tier 3 adds deep external research, a precedent search, and a durable-record offer. Do not run a Tier-3 workup on a trivially reversible `npm i`, or treat a security decision as a moderate Tier-2 choice.

### Phase 1: Gather Evidence

Search code, git history, issues, pull requests, project documents, and external
sources. Let scout agents do the noisy searching and return a short research
note plus its path. Read a note only when needed; do not paste raw search output
into the main conversation.

**Resolve the project profile from the shared cache first.** The question-agnostic profile (stack, dependency surface + licenses, conventions, structure) is identical for every run at this commit, so reuse it instead of re-deriving. Set `SKILL_DIR` to this skill's directory and run the helper (full protocol in `references/repo-profile-cache.md`):

```bash
SKILL_DIR="<absolute path of the directory containing the SKILL.md you just read>";
python3 "$SKILL_DIR/scripts/repo-profile-cache.py" get
```

On `HIT`, load the profile JSON — that is your agnostic project orientation; do not re-derive it. On `MISS`, dispatch a generic subagent with `references/agents/repo-profiler.md` to derive the profile, write its JSON to a file, then persist with `python3 "$SKILL_DIR/scripts/repo-profile-cache.py" put <file>` (re-set `SKILL_DIR` in that call because Codex shell calls do not share shell variables). On `NO-CACHE` — or if the call errors or returns nothing — derive it inline via that persona and skip the `put`; never block on the cache. The profile supplies the agnostic facts; the scouts below only run the **candidate-specific** slice on top of it.

Create the scratch dir once, and reuse the echoed path for every scout this run:

```bash
SCRATCH_DIR="/tmp/andrea-engineering/ae-pov/$(openssl rand -hex 4)"
mkdir -p "$SCRATCH_DIR"
echo "$SCRATCH_DIR"
```

**Give every scout the same facts.** A fresh agent does not inherit this
conversation. Pass the exact question, the current tool or approach, the tier,
the resolved `<scratch-dir>`, and any user-supplied links. A generic prompt will
produce unfocused research.

**Tier-sensitive dispatch.** For **Tier 1** (reversible), run a single combined evidence pass: seed one subagent with `references/agents/project-grounding-scout.md` covering the candidate-specific project facts (incumbent, call-sites) on top of the cached profile at a tight read budget, and one with `references/agents/external-evidence-researcher.md`; skip the standalone precedent scout — on this tier the project-grounding scout's **prior-decision scan** (`docs/solutions/`, ADRs, design docs) is the precedent check, so it must run. For **Tier 2/3**, dispatch the full fleet in parallel:

- **project-grounding scout** — read `references/agents/project-grounding-scout.md` and seed a generic subagent with it. With the agnostic profile already loaded from the cache, this scout runs only the **candidate-specific** slice: the named incumbent for *this* candidate, its call-sites/footprint, incumbent-pain, and the license/compat check against the profile's dependency-license set. Do not re-derive stack, conventions, or structure — those are in the profile. But note the profile may *name* an incumbent dependency, and a named dep is only a **lead** — it does not satisfy the project floor (see `references/method.md`), which still requires a freshly verified call-site the cache never holds. Do not let a cache-named incumbent short-circuit the fresh touchpoint check.
- **precedent-&-activity scout** — read `references/agents/precedent-activity-scout.md` and seed a generic subagent with it. Always run its **local-doc precedent pass** (`docs/solutions/`, ADRs, design docs — file reads, no tools needed); only its tracker/PR portion is capability-gated and degrades gracefully when those interfaces aren't reachable. Do **not** skip the whole scout for missing tracker access — that would drop the only path that surfaces a prior local adopt/reject decision.
- **external-evidence researcher** — read `references/agents/external-evidence-researcher.md` and seed a generic subagent with it. **Scale the remit to the reversibility tier so Tier 3's deeper-workup promise is real, not nominal:** at **Tier 3**, seed it with a deeper brief — a wider source net, a larger read budget, and *mandatory* two-source corroboration on every important claim (at Tier 3 a single-source claim cannot anchor the verdict); **Tier 2** uses the persona's standard budget and its prefer-two-sources default.

Skip only the part of a scout's work whose source cannot be reached. Local file
reads always run; issue, PR, and external research depend on available tools.
Record missing sources and lower confidence. If no external evidence is
available, Phase 2 must return Hold instead of guessing.

**Keep evidence groups separate.** Returned project facts and verified external
facts count as evidence. Conversation claims and unconfirmed assumptions do not
count until a scout verifies them. Read research notes from their paths only as
needed; do not load all of them into the main context.

### Phase 2: Check the Evidence

Read `references/method.md` now. Check the project evidence and external
evidence separately. If either is missing, do not return Adopt or Reject;
return the matching Hold result. Read research notes only as needed.

### Phase 3: Verdict

Use the verdict format in `references/method.md`. Lead with the recommendation,
keep each field short, cite the evidence, and do not reproduce research notes
or raw search output. Tier 1 should fit on one screen; Tier 2 and 3 can be
longer, but the recommendation still comes first.

### Phase 4: Follow-up

The chat verdict (the TL;DR) is the deliverable. What you offer next is **reasoned from the verdict and sized to the tier — never a fixed menu, and never an assumption that everything routes to a plan.**

**Compute the next step.** From the grade and the verdict's Handoff field, reason about the single best next move and a one-clause why — it is not always obvious between plan and brainstorm, so decide in context:

- **Adopt**, scope clear → take it into `ae-plan`.
- **Adopt**, scope still fuzzy → `ae-brainstorm` to pin down what "adopt" means before planning.
- **Trial** → scope a timeboxed spike (`ae-work`).
- **Hold / Reject / Not-our-problem** → no handoff; there is nothing to take forward.

**Tier-gate the offer (anti-ritual):**

- **Tier 1, or a Reject / Not-our-problem grade** → end with a single prose line — e.g. "Want the full write-up, or `<computed next step>`? Otherwise we're done." No blocking menu; silence means done.
- **Tier 2/3 with an actionable grade** → ask through the shared codex-interaction contract, with the *computed* next step as the first, dynamically-labeled option:
  1. **`<computed next step>`** (e.g. "Plan the adoption with `ae-plan`") — seeded with the verdict substance, not a file pointer.
  2. **Full write-up** — the expanded, shareable report.
  3. **Done.**
  Add `ae-compound` as a one-line prose nudge under the menu, **not** a slot: "Want it in our decision history? say 'compound it.'" It is the least-frequent path and is never the first thing offered.

**On each selection:**

- **Computed next step** → load and follow that Codex skill, seeding it with the verdict substance (the decision, conditions, and verified facts).
- **Full write-up** → read `references/report.md` and follow it (HTML by default; opened locally or published via Proof / an available HTML tool). Opt-in; the default stays chat-only.
- **"compound it"** → invoke `ae-compound` with `mode:headless`, seeding it with the structured verdict for `tooling_decision` / `architecture_pattern` storage (no schema change; headless avoids its interactive prompts). Never mandatory.

**Warm invocations stay a guest:** output the verdict block, hand control back, and offer none of the above unless the user asks — a mid-session interjection does not push a next-step or capture decision.
