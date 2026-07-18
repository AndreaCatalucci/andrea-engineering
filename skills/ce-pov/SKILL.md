---
name: ce-pov
description: "Verdict on whether an external technology, pattern, platform, architecture, or ecosystem change fits this project. Use for project-grounded adoption decisions or second opinions; not neutral explanation or ideation."
---

# Form a Point of View

Return a decisive, **graded verdict** on something from the outside world — judged against *this project*, not in the abstract.

The subject of this point of view — the thing to judge — is the input this skill was invoked with, present in the current prompt or conversation (whether the user asked directly or a calling skill passed it).

## The one rule that is the whole moat

**Do not issue a verdict you did not earn against the project's own context.** Generic web research already covers "tell me about X"; the differentiator is never "research the web" — it is the refusal to answer in the abstract. The verdict must clear **two absolute floors** (see `references/method.md`): a **project floor** (a concrete verified project fact — a named incumbent + a touchpoint, or for a net-new adoption the verified absence of one plus where it would fit, or a prior decision) and an **external floor** (at least one verified external source). The floors are absolute and independent — strong external evidence never compensates for a thin project leg, and vice versa. Neither the conversation nor the user's own assertions substitute for grounding.

## Interaction Method

Before asking the user for input, read and follow [`references/codex-interaction.md`](references/codex-interaction.md).

## Codex Agents

Dispatch scouts with `spawn_agent` and let them inherit the parent Codex model. Keep verdict reasoning—the two-floor gate, skeptic synthesis, and verdict contract—in the main conversation. Bound cost with the existing read budgets and scout count.

## Execution Flow

### Phase 0: Frame and Classify

**Output mode:** by default `ce-pov` writes no document — the verdict is a compact chat block. An optional full write-up and a durable `ce-compound` capture are available on request at Phase 4. Do not resolve an `OUTPUT_FORMAT` or load a rendering reference up front.

1. **Detect the invocation context — cold or warm.** Warm means `ce-pov` was invoked mid-session for a second opinion, with the question sitting in the surrounding conversation or absent. For the warm contract beyond the frame — taking only the *question and claims-to-verify* (never grounding), the guest output, the provenance buckets — read `references/invocation.md`.

2. **Establish the frame before grounding — orient, then infer or propose; never guess.** The same input supports very different verdicts: a bare link to a new sign-in method could mean adopt it, migrate to it, compare it to what we have, or just answer a question about it. Guessing sends the scouts after the wrong question. So orient cheaply on what was provided — fetch a bare link lightly to learn what it is, recognize a bare topic, read a paste (orientation, not grounding) — then settle the **subject and the POV intent** (adopt / migrate / compare / is-this-our-problem / explainer):
   - Both clear → state the frame in one line and proceed.
   - Intent ambiguous (a bare link or topic with no stated intent, or a warm invocation with no clear question) → **read `references/intake.md`** and follow it: propose the concrete candidate framings this input suggests and confirm before grounding. Do not guess and fan out.

3. **Apply the selection escape hatch.** If the input is a *selection* over a field ("what should we use for auth?"), it belongs here only when the realistic field is bounded (roughly five or fewer real candidates) and the criteria are knowable. If the field can't be bounded without inventing options, or the criteria are unclear, **stop**: return a Hold and route to `ce-ideate` (to enumerate) or `ce-brainstorm` (to surface criteria), then offer to re-run. Read `references/boundaries.md` only when the input's fit for `ce-pov` is genuinely in doubt or the field can't be bounded; skip it for a clearly in-scope verdict.

4. **Classify the reversibility tier — three levels.** Infer it from project signals:
   - **Tier 1 — two-way door:** a dependency, lint rule, or config; trivially reversible.
   - **Tier 2 — one-way but bounded:** a data store, an internal API/contract, or a migration whose blast radius stays inside this codebase.
   - **Tier 3 — one-way and high-stakes:** a security, legal, or privacy surface; a public API/contract; or an irreversible data migration.

   State the tier in the verdict and let the user override. The tier sizes the rest of the run (Phase 1 scout count, Phase 2 depth, Phase 3 reversal trigger): Tier 1 stays a one-screen verdict off a single combined grounding pass; Tier 2 adds the full scout fleet and an alternatives pass; Tier 3 adds deep external research, a precedent search, and a durable-record offer. Do not run a Tier-3 workup on a trivially reversible `npm i`, or hand a security-surface decision the moderate Tier-2 treatment.

### Phase 1: Ground (dispatch scouts, never inline)

Grounding searches code, git, the issue tracker, PRs, and docs — noisy work that would flood this context and crowd out the verdict reasoning. Dispatch it to scout subagents that search in their own context and return only a dossier path plus a short gist; read a dossier on demand, never inline the raw search.

**Resolve the project profile from the shared cache first.** The question-agnostic profile (stack, dependency surface + licenses, conventions, structure) is identical for every run at this commit, so reuse it instead of re-deriving. Set `SKILL_DIR` to this skill's directory and run the helper (full protocol in `references/repo-profile-cache.md`):

```bash
SKILL_DIR="<absolute path of the directory containing the SKILL.md you just read>";
python3 "$SKILL_DIR/scripts/repo-profile-cache.py" get
```

On `HIT`, load the profile JSON — that is your agnostic project orientation; do not re-derive it. On `MISS`, dispatch a generic subagent with `references/agents/repo-profiler.md` to derive the profile, write its JSON to a file, then persist with `python3 "$SKILL_DIR/scripts/repo-profile-cache.py" put <file>` (re-set `SKILL_DIR` in that call because Codex shell calls do not share shell variables). On `NO-CACHE` — or if the call errors or returns nothing — derive it inline via that persona and skip the `put`; never block on the cache. The profile supplies the agnostic facts; the scouts below only run the **candidate-specific** slice on top of it.

Create the scratch dir once, and reuse the echoed path for every scout this run:

```bash
SCRATCH_DIR="/tmp/andrea-engineering/ce-pov/$(openssl rand -hex 4)"
mkdir -p "$SCRATCH_DIR"
echo "$SCRATCH_DIR"
```

**Every scout payload carries the same context.** A fresh subagent does not inherit this conversation, so fill the persona files' `{subject}` / `{scratch-dir}` placeholders at dispatch: pass each scout the framed question (subject + intent), the named incumbent and the reversibility tier, and the resolved `<scratch-dir>` path — plus any user-supplied links for the external researcher. A scout seeded with only its generic persona grounds "some external thing" and can produce an empty or unfocused dossier.

**Tier-sensitive dispatch.** For **Tier 1** (reversible), run a single combined grounding pass: seed one subagent with `references/agents/project-grounding-scout.md` covering the candidate-specific project facts (incumbent, call-sites) on top of the cached profile at a tight read budget, and one with `references/agents/external-evidence-researcher.md`; skip the standalone precedent scout — on this tier the project-grounding scout's **prior-decision scan** (`docs/solutions/`, ADRs, design docs) is the precedent check, so it must run. For **Tier 2/3**, dispatch the full fleet in parallel:

- **project-grounding scout** — read `references/agents/project-grounding-scout.md` and seed a generic subagent with it. With the agnostic profile already loaded from the cache, this scout runs only the **candidate-specific** slice: the named incumbent for *this* candidate, its call-sites/footprint, incumbent-pain, and the license/compat check against the profile's dependency-license set. Do not re-derive stack, conventions, or structure — those are in the profile. But note the profile may *name* an incumbent dependency, and a named dep is only a **lead** — it does not satisfy the project floor (see `references/method.md`), which still requires a freshly verified call-site the cache never holds. Do not let a cache-named incumbent short-circuit the fresh touchpoint check.
- **precedent-&-activity scout** — read `references/agents/precedent-activity-scout.md` and seed a generic subagent with it. Always run its **local-doc precedent pass** (`docs/solutions/`, ADRs, design docs — file reads, no tools needed); only its tracker/PR portion is capability-gated and degrades gracefully when those interfaces aren't reachable. Do **not** skip the whole scout for missing tracker access — that would drop the only path that surfaces a prior local adopt/reject decision.
- **external-evidence researcher** — read `references/agents/external-evidence-researcher.md` and seed a generic subagent with it. **Scale the remit to the reversibility tier so Tier 3's deeper-workup promise is real, not nominal:** at **Tier 3**, seed it with a deeper brief — a wider source net, a larger read budget, and *mandatory* two-source corroboration on every load-bearing claim (at Tier 3 a single-source claim cannot anchor the verdict); **Tier 2** uses the persona's standard budget and its prefer-two-sources default.

**Capability gating is two-level:** skip only a scout (or scout-portion) with **no reachable surface at all** — the project-grounding scout and the precedent scout's local-doc pass are file reads and always run; the tracker/PR reads and the external researcher are tool-gated and degrade. Let a scout that loses a tool mid-run self-report "unavailable." Never block on a missing surface — record it and let it lower the verdict's stated confidence, or trip the external floor (Phase 2) when the external leg is entirely absent.

**Populate the provenance buckets** from the returned dossiers, keeping them separate for Phase 2: *observed-project-facts* and *verified-external-facts* (these count as grounding) vs. *conversation-claims* and *unconfirmed-assumptions* from a warm invocation (these do not count until a scout corroborates them). Read dossiers from their paths on demand; do not pull their bulk into this context.

### Phase 2: Verify against the two floors

**Read `references/method.md` now**, before reasoning about the verdict — it defines the Verify and Verdict steps, the skeptic stance and reversibility tiering as cross-cutting properties, and the two-floor Invalid-Verdict gate. Apply that gate as a pass/fail checklist over the dossiers: a failed floor forbids Adopt/Reject and returns the matching Hold subtype. Do this reasoning on the clean context — read a dossier on demand, never pull its bulk in.

### Phase 3: Verdict

Emit the verdict contract defined in `references/method.md` — grade vocabulary, schema fields, tier sizing, and output economy are all specified there. The verdict is a **compact chat block, not a research report**: lead with the grade, keep each schema field terse, and never reprint scout dossiers or raw search output. Size it to the tier — a Tier 1 verdict fits one screen; Tier 2/3 carries the full workup but still leads with the verdict and cites evidence rather than pasting it.

### Phase 4: Follow-up

The chat verdict (the TL;DR) is the deliverable. What you offer next is **reasoned from the verdict and sized to the tier — never a fixed menu, and never an assumption that everything routes to a plan.**

**Compute the next step.** From the grade and the verdict's Handoff field, reason about the single best next move and a one-clause why — it is not always obvious between plan and brainstorm, so decide in context:

- **Adopt**, scope clear → take it into `ce-plan`.
- **Adopt**, scope still fuzzy → `ce-brainstorm` to pin down what "adopt" means before planning.
- **Trial** → scope a timeboxed spike (`ce-work`).
- **Hold / Reject / Not-our-problem** → no handoff; there is nothing to take forward.

**Tier-gate the offer (anti-ritual):**

- **Tier 1, or a Reject / Not-our-problem grade** → end with a single prose line — e.g. "Want the full write-up, or `<computed next step>`? Otherwise we're done." No blocking menu; silence means done.
- **Tier 2/3 with an actionable grade** → ask through the shared codex-interaction contract, with the *computed* next step as the first, dynamically-labeled option:
  1. **`<computed next step>`** (e.g. "Plan the adoption with `ce-plan`") — seeded with the verdict substance, not a file pointer.
  2. **Full write-up** — the expanded, shareable artifact.
  3. **Done.**
  Add `ce-compound` as a one-line prose nudge under the menu, **not** a slot: "Want it in our decision history? say 'compound it.'" It is the least-frequent path and is never the first thing offered.

**On each selection:**

- **Computed next step** → load and follow that Codex skill, seeding it with the verdict substance (the decision, conditions, and verified facts).
- **Full write-up** → read `references/report.md` and follow it (HTML by default; opened locally or published via Proof / an available HTML tool). Opt-in; the default stays chat-only.
- **"compound it"** → invoke `ce-compound` with `mode:headless`, seeding it with the structured verdict for `tooling_decision` / `architecture_pattern` storage (no schema change; headless avoids its interactive prompts). Never mandatory.

**Warm invocations stay a guest:** output the verdict block, hand control back, and offer none of the above unless the user asks — a mid-session interjection does not push a next-step or capture decision.
