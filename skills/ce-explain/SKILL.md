---
name: ce-explain
description: "Turn a concept, a diff, an idea, or a window of your own recent work into a dense, visual explainer written for you personally — with an optional check-in (predict-then-reveal for diffs, corrected exercises) that makes the material stick. For learning, not repo docs or verdicts."
---

# Explain It To Me

Teach the user one thing well: a concept, a change, an idea, or a window of their own recent work. Agent-driven development removed the learning that writing code by hand used to provide; this skill is the replacement — the human keeps learning while agents do the writing.

What to explain is the input this skill was invoked with, present in the current prompt or conversation (whether the user asked directly or a calling skill passed it).

## Who the explainer is for

The user personally — dense, technical, one voice, no audience adaptation. Meeting prep preps the user; it never produces the deck. The artifact is display-only: no embedded quizzes, forms, or widgets — the doing happens in the session, where answers can be checked.

## Interaction Method

Before asking the user for input, read and follow [`references/codex-interaction.md`](references/codex-interaction.md).

## Codex Agents

Dispatch extraction scouts with `spawn_agent` and let them inherit the parent Codex model. Keep explainer composition, check-in reasoning, and corrections in the main conversation. If no agent slot is available, run the scout work inline with the same read budgets.

## Execution Flow

### Phase 1: Classify the input

Read `references/intake.md` now and classify the request into one of the four input shapes — concept, diff, idea, or work-recap window. It owns the token table (`diff:`, `since:`, `output:`), the explicit-token-beats-inference rule, the concept-vs-diff tiebreak, and conflict handling. Do not improvise classification.

**Bare invocation** (no input at all): ask one blocking question — "What should I explain?" — offering a shortcut option for a recap of recent work in this repo alongside free-text. Do not produce a default artifact unprompted.

### Phase 2: Ground

Match grounding to the input shape. Create the run directory first — every run gets one, before any artifact exists:

```bash
RUN_DIR="/tmp/andrea-engineering/ce-explain/$(date +%Y%m%d)-$(openssl rand -hex 3)"
mkdir -p "$RUN_DIR"
echo "$RUN_DIR"
```

**Repo-touching inputs** (a concept with footprint in this repo, a diff, a recap): resolve the question-agnostic project profile from the shared cache instead of re-deriving it. Set `SKILL_DIR` to this skill's directory and run the helper (full protocol in `references/repo-profile-cache.md`):

```bash
SKILL_DIR="<absolute path of the directory containing the SKILL.md you just read>";
python3 "$SKILL_DIR/scripts/repo-profile-cache.py" get
```

On `HIT`, load the profile JSON — stack, conventions, vocabulary — and take orientation from it. On `MISS`, dispatch a generic subagent with `references/agents/repo-profiler.md` to derive the profile, write its JSON to a file, then persist with `python3 "$SKILL_DIR/scripts/repo-profile-cache.py" put <file>` (re-set `SKILL_DIR` in that call because Codex shell calls do not share shell variables). On `NO-CACHE` — or if the call errors — derive orientation inline and skip the `put`. The cache is an optimization, never a correctness dependency. The topic-specific evidence (the diff, the concept's call-sites, the window's commits) is always gathered fresh.

- **Diff mode:** resolve the change (the `diff:` ref, or the most recent substantial change when the request points at one implicitly) and gather its evidence — the diff itself, the files it touches, any plan or solution doc that motivated it. Gather silently: nothing learned here is narrated to the user until Phase 3's ordering rule is satisfied.
- **Recap mode:** dispatch a generic subagent with `spawn_agent`, seeded with `references/agents/work-recap-scout.md` and using Codex's inherited model. Pass the resolved window, the repo root, and `$RUN_DIR`. It returns an evidence summary with commit shas and `file:line` pointers. **Empty window** (no git activity, no doc changes): say so, offer to widen the window, write no artifact, and end the run after the user responds.
- **External concepts** (no footprint in this repo): skip repo grounding entirely — do not force repo context into the output. Research with whatever web tools are reachable. When none are, you may explain from model knowledge, but the artifact must label that content **Unverified — from model knowledge, not checked against current sources** in its metadata header.
- **Idea mode:** the idea is a fixed given. Explain its implications, mechanics, and trade-offs for the user's understanding. Never scope it (`ce-brainstorm`'s job), never generate and rank alternatives (`ce-ideate`'s job).

### Phase 3: Check-in gate — before anything is revealed

Judge whether the material warrants a check-in (a routine recap does not; a gnarly diff or a hard concept does), then offer it through the Interaction Method. The user can always decline, and declining is never re-litigated. Read `references/check-in.md` for the warrant test, the prediction protocol, and exercise design.

**Diff mode with check-in accepted — hard ordering rule.** No interpretive content — explanation, annotation, diagram, or surfaced opportunity — may be shown before the user's prediction turn ends. Show only the raw change reference (the diff or its stat summary), ask for the prediction through the shared interaction contract ("What do you think this change does, and why was it made?"), and **end the turn there**. Never print the reveal in the same message as the prediction prompt. Compose the explainer only after the prediction lands; the reveal names the gaps between the prediction and what the change actually does.

### Phase 4: Compose the explainer

Read the rendering reference for the resolved format **now**, not earlier: `references/explainer-html.md` (default) or `references/explainer-markdown.md` (when intake resolved `output:md`). Compose per its contract — visible metadata header, show-n-tell form matched to the material, ~70ch measure, single self-contained file — and write the artifact to `$RUN_DIR/explainer.html` (or `$RUN_DIR/explainer.md` when intake resolved `output:md`) before anything else happens with it. Display it to the user (inline summary plus the file path; open locally per Phase 6 when chosen). The artifact exists at that stable path from this moment — a declined destination ask never loses it.

### Phase 5: Exercises (when warranted)

For concepts, ideas, and dense recaps where the check-in was accepted: pose the exercises from `references/check-in.md` in chat, one at a time, using the Interaction Method for bounded choices and free chat for narrative answers. Check each answer, correct it, and name the gap it exposed. Do not put exercises inside the artifact.

### Phase 6: Destination ask and close

Detect destinations by capability — probe the agent's own toolset and session context, never a closed list, and never treat a missing binary, env var, or unloaded MCP tool as proof a destination is unavailable when a connector could supply it. Local file and Leave it are ungated and always offered. Offer only what is detected; absence hides an option silently. Ask once through the Interaction Method; when the visible set exceeds the host's option cap, render a numbered list in chat with "Pick a number or describe what you want." and wait instead. Per-option routing:

- **Artifact surface** (offered when an artifact-publishing tool is present in the current session's tools) — publish per `references/destinations.md`: re-emit the explainer as body-only markup (no doctype/html/head/body, styles inline, no external font links); the surface wraps content in its own skeleton and blocks external hosts.
- **Local file** — copy the artifact out of `$RUN_DIR` to the path the user names, then print the absolute path.
- **Publish to Proof** (markdown output only) — publish per `references/destinations.md` and surface the returned share URL; on failure retry once, then report and move on.
- **Send to Thinkroom** (offered only when a Thinkroom skill or CLI capability is detected) — send per `references/destinations.md`.
- **Leave it** — report the `$RUN_DIR` path and state it is a temporary location that does not survive reboot; nothing else is written.

**Non-interactive degradation:** when no interaction is possible at this ask (no blocking tool and no reply), do not hang and do not discard — the artifact is already at `$RUN_DIR`; report that path and end, skipping the improvement-observation handoffs below (they are offers, and an offer cannot fire without a user).

**Improvement observations.** When composing the explainer surfaced things that could be better, route them by type after the destination ask — offer, don't auto-fire:

- **New-capability ideas** — offer first; on acceptance load and follow `ce-ideate`, passing the observations as seed context.
- **Code-clarity findings** — offer first; on acceptance load and follow `ce-simplify-code`, passing the observations and files they concern.
- **UI/UX polish opportunities** — offer first; on acceptance load and follow `ce-polish`, passing the observations and affected feature.

## Boundaries

- **Not a verdict.** "Should we adopt X?" is `ce-pov`. ce-explain teaches what X is and how it works.
- **Not repo memory.** Documenting a solved problem for future work is `ce-compound`. ce-explain teaches the human, not the repo.
- **Not ideation or scoping.** An idea input is explained as given — implications and trade-offs — never expanded into options or a requirements dialogue.
- **The check-in is never headless.** It exists to exercise the human; automating the answers deletes the product.
