# Persona Catalog

Run one core reviewer on every review. Add specialists only when the diff presents their runtime concern.

## Always-on

| Persona | Prompt asset | Focus |
|---|---|---|
| `core` | `core-reviewer` | Correctness/regressions, test adequacy/assertion quality, and maintainability/simplification |

The core rubric always covers all three lenses. Do not split them into separate subagents.

## Conditional specialists

| Persona | Select when the diff materially touches... |
|---|---|
| `security` | Auth, public input, permissions, secrets, or trust boundaries |
| `performance` | Queries, heavy transforms, caching, or concurrency with performance risk |
| `api` | Routes, serializers, events, exported types, or versioned interfaces |
| `data-migration` | Migration/schema artifacts or explicit backfills/data transforms |
| `reliability` | Retries, timeouts, background jobs, error recovery, or health behavior |
| `adversarial` | High-criticality or wide-blast-radius behavior: auth, payments, durable data mutation, external integrations, cross-component failure propagation, or a guard that could silently pass while production fails |
| `previous-comments` | A PR with actual existing review comments or review submissions |
| `julik-frontend-races` | Stimulus/Turbo, DOM events, timers, async UI, animation, or frontend state races |
| `swift-ios` | Meaningful Swift/iOS lifecycle, entitlements, persistence, target, or signing behavior |

Selection is judgment-based, not keyword-based. A path signal prompts inspection; it never forces a reviewer.

For `data-migration`, require a migration/schema/backfill artifact in the diff. Model-only and query-only changes do not qualify. Add `deployment-verification-agent` only for risky migration operations such as destructive DDL, backfills, column drops/renames, or `NOT NULL` without a safe rollout.

Select `agent-native-reviewer` only when the diff adds or materially changes a user-facing capability, command, API, or workflow that should also be operable by an agent. Do not run it for internal refactors, tests, docs-only edits, or implementation details with no capability surface.

The orchestrator handles applicable project-instruction compliance and relevant `docs/solutions/` research inline; never spawn separate standards or learnings agents.
