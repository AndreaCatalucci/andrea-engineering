# Handoff

This content is loaded when handoff begins — after the requirements-only
plan is written.

---

#### 4.1 Present Next-Step Options

The handoff menu's visible option count varies by state: no plan
artifact hides the review and Proof options, `OUTPUT_FORMAT=html` also hides
the review option (ae-doc-review is markdown-only today), unresolved `Resolve
Before Planning` hides both `Create the implementation plan` and `Ship it
autonomously with lfg`, and the lfg option is also hidden for non-software
brainstorms (`execution` other than `code`). Count the visible options for the
current state and choose the rendering mode accordingly:

- **Up to three visible options:** use the [shared codex-interaction contract](codex-interaction.md).
- **More than three options, or the tool is unavailable:** render a numbered list in chat and wait. Do not trim legitimate destinations. Include: "Pick a number or describe what you want."

Never silently skip the question.

If `Resolve Before Planning` contains any items:
- Ask the blocking questions now, one at a time, by default
- If the user explicitly wants to proceed anyway, first convert each remaining item into an explicit decision, assumption, or `Deferred to Planning` question
- If the user chooses to pause instead, present the handoff as paused or blocked rather than complete
- Do not offer the `Create the implementation plan` or `Ship it autonomously with lfg` options while `Resolve Before Planning` remains non-empty

In both preambles below, the "Pick a number or describe what you want." hint applies only in numbered-list mode. When using the blocking tool, omit that line and pass the remaining stem as the question.

**Path format:** Use absolute paths for chat-output file references — relative paths are not auto-linked as clickable in most terminals.

**Preamble when no blocking questions remain:**

```
Brainstorm complete.

Plan: <absolute path to requirements-only plan>  # omit line if no plan was created

What would you like to do next? (Pick a number or describe what you want.)
```

**Preamble when blocking questions remain and user wants to pause:**

```
Brainstorm paused. Planning is blocked until the remaining questions are resolved.

Plan: <absolute path to requirements-only plan>  # omit line if no plan was created

What would you like to do next? (Pick a number or describe what you want.)
```

Present only the options that apply. Renumber so visible options stay contiguous starting at 1.

1. **Create the implementation plan** *(recommended)* - Hand off to `ae-plan` and sharpen the requirements into a complete, testable plan. Shown only when `Resolve Before Planning` is empty.
2. **Ship it autonomously with `lfg`** - Hand the requirements to the full autonomous pipeline: `lfg` plans (`ae-plan`), implements, simplifies, runs independent code review and applies the fixes, opens a PR, and watches CI to green — hands-off, no check-ins. It plans first (unlike a raw `/goal` straight from requirements), so it's the safer autonomous path. Best when you trust the requirements and want it built and shipped without steering. **Opens a PR and pushes a branch.** Shown only for software brainstorms (`execution: code`) with `Resolve Before Planning` empty **and a plan artifact was created** — `lfg` hands `ae-plan` that artifact path in pipeline mode and cannot prompt, so with no artifact (e.g. a brief-alignment brainstorm that skipped doc creation per the "Decide whether a doc is warranted" rule) there is nothing to enrich; offer option 1 instead, which can plan interactively from the conversation. For a quicker plan-then-decide flow, or to run a `/goal` yourself, pick option 1 and choose at the `ae-plan` handoff.
3. **Pressure-test the requirements** - Run `ae-doc-review` to find contradictions, weak decisions, scope issues, and triggered design or security risks; auto-apply mechanically certain fixes and report the remaining author decisions together. Shown only when a markdown plan exists **and `OUTPUT_FORMAT=md`** because this handoff option promises in-place corrections. HTML reviews are report-only, so under HTML mode surface a one-line note above the menu: `Requirements review is report-only in output:html mode. Switch to output:md if you want the handoff to apply mechanical corrections.`
4. **Publish to Proof — shareable link** - Publish the markdown plan to Every's Proof editor and get a shareable link to read, comment on, or share with others. One-way: the local doc stays canonical. Shown only when a markdown plan exists. **Render only when `OUTPUT_FORMAT=md`** (Proof operates on markdown and cannot ingest HTML).
4. **Open in browser** — open the HTML plan locally for review and sharing. Shown only when an HTML plan exists. **Render only when `OUTPUT_FORMAT=html`.** Replaces "Publish to Proof" at the same slot under exclusive output mode — the artifact is either markdown OR HTML, never both, so exactly one of the two labels applies per run.
5. **More clarifying questions to sharpen the doc** - Keep refining scope, edge cases, constraints, and preferences through further dialogue. Always shown.

There is no "done" / "pause" option — the blocking question already waits, and the user ends by dismissing it (Esc) or saying they're finished. The plan artifact is already saved.

**Post-review nudge (subsequent rounds only):** If the user has already run `ae-doc-review` this session and residual P0/P1 findings remain unaddressed, add a one-line prose nudge adjacent to the menu (e.g., "Document review flagged 2 P1 findings you may want to address — pick \"Pressure-test the requirements\" to run another pass."). Reference the option by label, not number: the menu renumbers when `Resolve Before Planning` hides `Create the implementation plan` and the lfg option, so a hardcoded option number can point users at the wrong action. Do not add a separate menu option; reuse the existing `Pressure-test the requirements` option. Suppress this nudge when `OUTPUT_FORMAT=html` — that option is hidden in that mode, so the nudge would point users at a missing action.

#### 4.2 Handle the Selected Option

Selections may be the literal option label (when the user types the label or a close paraphrase) or the option number. Match numbers against the currently-rendered (post-trim) list. Free-form input that doesn't match an option or describe an alternative action should be treated as clarification — ask a follow-up rather than guessing.

**If user selects "Create the implementation plan":**

Immediately load the `ae-plan` skill in the current session. Pass the unified
plan artifact path when one exists; otherwise pass a concise summary of the
finalized brainstorm decisions. When the conditional grounding scout produced a
dossier and the file still exists, also pass its path
(`/tmp/andrea-engineering/ae-brainstorm/<run-id>/grounding.md`) — it gives
planning verified quotes with `file:line` pointers to start from instead of
re-scanning the repo. Do not print the closing summary first.

**If user selects "Pressure-test the requirements":**

Load the `ae-doc-review` skill, passing the plan path as the argument.
When ae-doc-review returns "Review complete", return to the handoff options
and re-render the menu (the requirements may have changed, so re-evaluate
`Resolve Before Planning`, the lfg software gate, and residual findings). If
residual P0/P1 findings remain unaddressed, include the post-review nudge
above the menu. Do not show the closing summary yet.

**If user selects "Ship it autonomously with `lfg`":**

Load and follow the Codex `lfg` skill immediately, passing the plan
artifact path so its `ae-plan` step enriches *this* requirements-only artifact
in place rather than bootstrapping a new plan. `lfg` then owns the full pipeline:
plan, implement (`ae-work` in `return-to-caller` mode), simplify, independently
review and apply fixes, commit, push, open the PR, and watch CI to green. Do not
load `ae-work` directly; `lfg` orchestrates it.

Do not print the closing summary first.

**If user selects "More clarifying questions to sharpen the doc":** Return to the dependency-ordered decision interview and continue one question at a time. Re-present the complete shared-understanding synthesis and get explicit confirmation before updating the artifact or returning to the handoff menu. Do not show the closing summary yet.

**If user selects "Publish to Proof — shareable link":**

Load the `ae-proof` skill to publish the markdown plan. Pass:

- **source file:** `docs/plans/YYYY-MM-DD-NNN-<type>-<topic>-plan.md`
- **doc title:** `Plan: <topic title> (requirements-only)`
- **identity:** `ai:andrea-engineering` / `Andrea Engineering`

ae-proof creates a shared Proof doc from the markdown plan file (Create and
Share workflow), binds the display name, and returns the share URL. Surface
the URL to the user — they can open it to read, comment, or share with others
— then return to the handoff options and re-render the menu. This is a one-way
publish: the local doc stays canonical and nothing syncs back, so option
eligibility is unchanged (no need to re-evaluate `Resolve Before Planning`,
the lfg software gate, or residual findings on account of Proof).

If the upload fails (network error, Proof API down), retry once after a short wait. If it still fails, tell the user the upload didn't succeed and briefly explain why, then return to the handoff options — don't leave them wondering why the option did nothing.

**If user selects "Open in browser":** Load `browser:control-in-app-browser`, display the absolute path to the `.html` plan in Codex's in-app browser, then return to the handoff options.

**If the user indicates they're finished** (says "done"/"that's all", or dismisses the menu without picking an option): display the closing summary (see 4.3) and end the turn.

#### 4.3 Closing Summary

Use the closing summary only when this run of the workflow is ending or handing off, not when returning to the handoff options.

In both templates below, substitute `<absolute path to plan>` with the
actual file path written this run — `.md` for `OUTPUT_FORMAT=md`, `.html` for
`OUTPUT_FORMAT=html`. Do not emit a hardcoded `.md` path when the artifact is
HTML, or the closing summary will point users at a file that was never written.

When complete and ready for planning, display:

```text
Brainstorm complete!

Plan: <absolute path to plan>  # omit line if no plan was created

Key decisions:
- [Decision 1]
- [Decision 2]

Recommended next step: `ae-plan <plan artifact path>`
```

If the user pauses with `Resolve Before Planning` still populated, display:

```text
Brainstorm paused.

Plan: <absolute path to plan>  # omit line if no plan was created

Planning is blocked by:
- [Blocking question 1]
- [Blocking question 2]

Resume with `ae-brainstorm` when ready to resolve these before planning.
```
