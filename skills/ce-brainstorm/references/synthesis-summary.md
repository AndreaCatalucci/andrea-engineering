# Shared-Understanding Synthesis

Read this only after the decision interview has no material unresolved decision.

The synthesis is the final alignment gate. It proves that individually resolved decisions form a coherent whole. It is not a preview of the full Product Contract and contains no implementation design.

## Compose

Draft from the decision ledger and verified evidence. Use these sections, omitting empty conditional sections:

1. **What we're building** — 1–3 sentences naming the actor, outcome, and product shape.
2. **Key decisions** — only material choices, each with its short rationale.
3. **Scope boundaries** — meaningful exclusions or deferrals a reasonable reader might otherwise expect.
4. **Success** — observable acceptance or outcome signals.
5. **Defaults and assumptions** — minor defaults, user-supplied facts, or unverifiable premises that affect the direction.
6. **Open non-blockers** — uncertainties that can safely remain for planning or later work.

Do not include an unresolved choice that affects scope, behavior, architecture, or acceptance. Return to the one-question decision loop instead.

## Keep It Compact

Keep only decision-relevant content:

- Lightweight: usually 3–6 bullets total.
- Standard: usually 5–10 bullets total.
- Deep: usually 8–15 bullets total.

Combine related sub-decisions under the higher-level choice. Use one sentence per bullet. Exclude transcript history, implementation details, file inventories, and ideas that were considered and rejected unless the exclusion itself matters.

Before presenting, test the whole for:

- contradictions between decisions;
- combined consequences not yet accepted;
- hidden assumptions framed as facts;
- scope that exceeds the stated outcome;
- missing acceptance signals.

If a material issue appears, return to the interview and ask one recommended decision question. Do not bury it in the synthesis.

## Present and Wait

Use this shape:

```text
Shared understanding

What we're building
<1–3 sentences>

Key decisions
- <decision — reason>

Scope boundaries
- <meaningful exclusion or deferral>

Success
- <observable signal>

Defaults and assumptions
- <visible default or premise>

Open non-blockers
- <safe uncertainty>

Recommendation: adopt this as the requirements direction.

Does this match our shared understanding?
```

Omit empty conditional sections rather than writing “none.” Always ask for explicit confirmation and wait. There is no auto-write path.

On revision:

1. Update the ledger.
2. If the revision opens a material dependency, resolve it through the one-question loop.
3. Present the complete revised synthesis.
4. Wait for explicit confirmation again.

“Proceed,” “approved,” “yes,” or an equivalent unambiguous response confirms. Questions, additions, and revisions do not.

## Route After Confirmation

Only after confirmation may the workflow write or hand off. Route synthesis content into the Product Contract rather than adding a `Synthesis` section:

| Synthesis content | Product Contract destination |
|---|---|
| What we're building | Summary and Problem Frame |
| Key decisions | Key Decisions and Requirements |
| Scope boundaries | Scope Boundaries |
| Success | Acceptance Criteria / Success Criteria |
| Defaults and assumptions | Dependencies / Assumptions |
| Open non-blockers | Deferred to Planning or Outstanding Questions |

If the user redirects to another workflow before confirming, stop the brainstorm and offer the fitting skill. Do not write a partial plan automatically.
