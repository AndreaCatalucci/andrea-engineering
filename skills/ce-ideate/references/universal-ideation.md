# Universal Ideation Facilitator

This file is loaded when ce-ideate detects an elsewhere-mode topic with no software surface at all — naming (independent of product), narrative writing, personal decisions, non-digital business strategy, physical-product design. Topics that concern a software artifact (page, app, feature, flow, product) are routed to elsewhere-software and do not load this file, even when the ideas are about copy, UX, or visual design for that artifact.

Phase 1 elsewhere-mode grounding runs before this reference takes over — user-context synthesis and web-research feed the facilitation below. Learnings-researcher is skipped by default for elsewhere-non-software since the CWD's `docs/solutions/` almost always contains engineering patterns that do not transfer to non-digital topics. What this file replaces is Phase 2's software-flavored frame dispatch and the post-ideation wrap-up; the repo-specific codebase scan never runs in elsewhere mode. Absorb these principles and facilitate ideation in the topic's native domain, using the Phase 1 grounding summary as input.

The mechanism that makes ideation good — generate many, critique adversarially, present survivors with reasons — is preserved. Only the framing of the work changes.

---

## Your role

Be a divergent thinking partner, not a delivery service. The user came here for a stronger candidate set than they could generate alone, not a single recommendation. Resist the urge to converge early. A premature favorite anchors the conversation and crowds out better candidates that have not surfaced yet.

Match the tone to the stakes. For business or product decisions (pricing, positioning, roadmap), lead with constraints and tradeoffs. For creative work (naming, narrative, visual concepts), lead with energy and range. For personal decisions, lead with values before mechanics.

## How to start

Match depth to scope:

- **Quick** — the user wants a starter set right now. Generate one round, critique briefly, present 3-5 survivors, done.
- **Standard** — light intake (one or two questions), one round of generation, adversarial critique, present 5-7 survivors.
- **Full** — rich intake, multiple frames in parallel, deep critique, present 5-7 survivors with strong rationale.

Apply the discrimination test before asking anything. Would swapping one piece of the user's stated context for a contrasting alternative materially change which ideas survive? If yes, the context is important — proceed. If no, ask 1-3 narrowly chosen questions. Follow the questioning principles from SKILL.md Phase 0.2: ask only about the **subject** (what to ideate on) or **substance** (what Phase 1 agents need to say something specific) — never about solution direction, constraints, audience, tone, or success criteria. Those belong to `ce-brainstorm`. Build on what the user already provided rather than starting from a template. After each answer, re-apply the test before asking another. Stop on dismissive responses ("idk just go") and treat genuine "no constraint" answers as real answers.

**Grounding freshness.** Phase 1 elsewhere-mode grounding (user-context synthesis + web-research by default; learnings skipped for non-software, see SKILL.md Phase 1) has already run before this reference takes over, and its outputs feed the generation below. If intake answers here materially refine the topic or constraints — new scope, different audience, a domain shift that the original grounding did not cover — re-dispatch the affected Phase 1 agents on the refined topic before generating ideas. The guardrail mirrors SKILL.md Phase 0.4's rule that mode and grounding re-evaluate when intake changes the scope to be acted on; ranking against stale grounding risks surfacing ideas fit to the wrong topic.

When the user provides rich context up front (a paste, a brief, an existing draft), confirm understanding in one line and skip intake.

## How to decompose

Before generating, split the topic into 3-5 distinct **areas**. Areas identify
the parts that need ideas; the generation approaches determine how to think
about each part. Without this list, several approaches can still cluster around
the same obvious part of the topic.

This step is the facilitator's own analysis — no subagent, no additional research. The Phase 1 grounding supplies the substance.

Areas should be:

- **3-5 in number.** Fewer means atomic — skip decomposition. More fragments coverage.
- **Orthogonal.** A single idea should fall on one area, not span multiple.
- **Derived from grounding**, not from a generic template.
- **At the same level** of granularity.
- **Named in the topic's language**, not meta-language about ideation.

**Worked examples (illustrative, not a template):**

- "Name my new coffee shop" → atomic; skip decomposition (the candidate *is* a name)
- "Plot ideas for a short story" → atomic; skip decomposition (the candidate *is* a plot)
- "Brand strategy for a launch" → areas might be: positioning; visual identity; voice; launch channels; pricing/packaging
- "Career options for the next 5 years" → areas might be: domain (industry/role); structure (employee/founder/freelance); geography; growth ambition; financial floor

**Skip condition.** Many elsewhere-non-software topics are atomic by nature — a single name, tagline, or one-shot creative output. When 3+ non-overlapping areas do not emerge, skip decomposition and note `Decomposition skipped — atomic subject` in the grounding summary.

**Surprise-me skip.** No settled subject in surprise-me mode; skip decomposition and note `Decomposition skipped — surprise-me mode`.

Record the areas (or skip-reason) at the head of generation. Generation will distribute ideas across areas; convergence will weight area spread alongside other rubric criteria.

## How to generate

Generate the full candidate list before critiquing any idea. Use the same six frames as software ideation, described in domain-agnostic language. Each frame is a **starting bias, not a constraint** — follow promising threads across frames. At Full depth, dispatch the six frames in parallel using the inherited Codex model.

- **Pain and friction** — what is consistently annoying, slow, or broken in the current state of the topic? Generate ideas that remove or reduce that friction.
- **Inversion, removal, automation** — what would happen if a step were inverted, removed entirely, or automated away? The result is often a candidate even if the inversion itself is unrealistic.
- **Assumption-breaking and reframing** — what is being treated as fixed that is actually a choice? Reframe the problem one level up or sideways.
- **Leverage and compounding** — what choices, once made, make many future moves cheaper or stronger? Look for second-order effects.
- **Cross-domain analogy** — how do completely different fields solve a structurally similar problem? The grounding domain is the user's topic; the analogy domain is anywhere else (other industries, biology, games, infrastructure, history). Push past the obvious analogy to non-obvious ones.
- **Constraint-flipping** — invert the obvious constraint to its opposite or extreme. What if the budget were 10x or 0? What if there were one constraint instead of ten, or ten instead of one? Use the resulting design as a candidate even if the flip itself is not realistic.

Aim for 5-8 ideas per frame. **When areas are present, distribute ideas across areas** — each frame's point of view applies to every area, but ideas should not all cluster on one. Tag each idea with the area it targets. After generating, merge and dedupe; scan for cross-cutting combinations (3-5 additions at most; more in surprise-me mode, where different frames often discover different subjects and combinations are the magic layer).

**Area-coverage check (when areas are present).** After merging, count ideas per area. If any area has zero ideas, generate one additional small batch (3-5 ideas) targeting the empty area with the frame whose point of view best fits — Pain & friction for usability gaps, Cross-domain analogy for distribution or compounding gaps, etc. Cap recovery at 2 areas; beyond that, accept thin coverage rather than fan out. Note any area that was not recovered in the rejection summary so the gap is visible.

**Compact candidate contract (mirrors `references/divergent-ideation.md`):** return title, a one-sentence concrete move, **area** when decomposition produced one, a required tagged **basis** (`direct:`, `external:`, or `reasoned:`), and one line of significance. Do not pre-write final-artifact prose for raw candidates. The root agent develops only survivors after verification.

**Generation rules:**

- Every idea carries an articulated basis. The failure mode to prevent is plausible-sounding speculation that lacks any basis the user can verify.
- Aim past the obvious. The first few ideas per frame are warm-up — keep only those that earn their place once the non-obvious ideas exist. If an idea would appear in a generic listicle about this topic, sharpen it with grounding or drop it.
- Bias toward the basis type your frame naturally produces — pain/inversion/leverage tend toward `direct:`; analogy and constraint-flipping tend toward `reasoned:` — but don't exclude other types. When a frame produces a reasoned basis, write the argument out, don't gesture at it.
- Apply the meeting-test internally as a default floor, but do not emit a self-attestation field; the independent verifier judges it. The floor is relaxed only when Phase 0.5 detected tactical focus signals.
- Stay within the subject's identity. Expansions, new surfaces, new directions, retirements are fair game when the basis supports them. Subject-replacement moves (abandoning the subject, pivoting to an unrelated domain) are out regardless of basis.

**Surprise-me mode in this reference.** When Phase 0.2 routed to surprise-me, there is no user-specified subject. Through each frame's point of view, explore the Phase 1 grounding (user-context synthesis + web research) and identify the subject(s) you find most interesting for that point of view. Different frames finding different subjects is the feature. The basis may include identification of the subject itself — why this subject is worth ideating on through this point of view, citing what in the Phase 1 material signals it.

## How to converge

Before the final cut, dispatch one fresh-context basis verifier using the inherited Codex model. Its payload is only the grounding summary and candidate list, and it attempts to refute bases that do not support the claimed move, prior art that is not real or relevantly analogous, and reasoned arguments that do not hold. In this mode verification runs against the user-supplied context and web research — no repo reads. Weigh its verdicts in the cut, overruling with stated reasons; if dispatch is unavailable, fall back to facilitator-only critique and note the degradation.

Apply adversarial critique. For each candidate, write a one-line reason if rejected. **Basis-integrity check:** reject any idea lacking an articulated basis, any idea whose stated basis does not actually support the claimed move (speculation dressed as ambition), and any idea that replaces the subject rather than operating on it. Score survivors using a consistent rubric weighing: groundedness in stated context, **basis strength** (`direct:` > `external:` > `reasoned:`; none excluded, but direct-evidence ideas score higher all else equal), expected value, novelty, pragmatism, leverage, implementation burden, overlap with stronger candidates, and **area spread** (when areas were defined) — survivor sets that cover the topic's surface outscore sets that cluster on one area, all else equal. Area spread is a list-level concern, not a per-idea reject reason; apply it after per-idea filtering when choosing among comparable candidates.

Target 5-7 survivors by default. If too many survive, run a second stricter pass. If fewer than five survive, report that honestly rather than lowering the bar.

After the cut, expand only the survivors into the final artifact fields: concrete description, rationale, downsides, confidence, and complexity. Preserve their verified basis and area; do not invent support while polishing.

## When to wrap up

Load `references/post-ideation-workflow.md` and follow Phase 4 to write and deliver the artifact. End after the compact summary; do not open, publish, commit, delete, or present an action menu. If the user later selects an idea, use that reference's compact handoff and route it to `ce-brainstorm` for further development.
