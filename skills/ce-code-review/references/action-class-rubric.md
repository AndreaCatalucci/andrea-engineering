# `autofix_class` rubric (personas)

`autofix_class` describes the **intrinsic shape** of follow-up work — it is signal, **not an apply gate or permission**. In `mode:agent` the caller owns apply; in default mode the review applies safe fixes by judgment (SKILL.md “Apply fixes”). The class informs priority and handoff shape; it does not mechanically decide mutation.

| `autofix_class` | Meaning |
|-----------------|---------|
| `gated_auto` | A concrete change is proposed in `suggested_fix`. Callers may apply after their own judgment. |
| `manual` | Actionable work that needs design input or a decision before code changes. Include `suggested_fix` when you can propose a defensible default. |
| `advisory` | Report-only — learnings, residual risk, rollout notes. |

## Persona guidance

- Prefer `gated_auto` when you can write a defensible `suggested_fix` for a localized change.
- Use `manual` when the right fix depends on product intent, architecture, or cross-cutting refactors.
- Use `advisory` when nothing breaks if left unfixed but the observation has value.
- Do **not** emit `safe_auto` — callers decide what to apply; reviewers classify and propose.

## Owner field

| `owner` | Meaning |
|---------|---------|
| `downstream-resolver` | Caller or human should act after review. |
| `human` | Judgment required before implementation. |
| `release` | Operational / rollout follow-up. |

Do not use `review-fixer`.
