---
name: ce-code-review
description: "Structured code review for bugs, regressions, tests, and standards. Use before PRs or when asked for review; interactive mode can fix locally, while mode:agent reports only for pipeline callers."
---

# Code Review

Review a branch, PR, or working-tree diff with one core reviewer and only the specialists justified by criticality and blast radius. Merge, independently validate, and present a single evidence-backed result.

## Modes and Arguments

Recognize and strip these tokens before interpreting the remaining target:

| Token | Effect |
|---|---|
| `mode:agent` | Report-only JSON; never mutate the tree |
| `mode:headless` | Deprecated alias for `mode:agent` |
| `mode:report-only` | Deprecated; ignore |
| `base:<ref>` | Review the current checkout against an explicit base |
| `plan:<path>` | Use this plan for requirements completeness |
| `grouping:auto` | Group findings when distinct concerns exist; default |
| `grouping:off` | Disable triage groups |
| `grouping:always` | Always form useful groups |

Ignore deprecated `mode:autofix`; default mode already owns safe local application. Reject incompatible scope selectors, conflicting modes, or conflicting grouping tokens. In `mode:agent`, failures are `{"status":"failed","reason":"..."}`.

## Invariants

- Never ask blocking questions. Infer intent and record uncertainty.
- Never checkout or switch branches. A target selects review scope, not mutation authority.
- Never push, open PRs, or file tickets.
- Default mode may apply verified fixes locally; `mode:agent` is strictly report-only.
- Review tracked changes only. List excluded untracked paths in Coverage.
- Never recommend deleting or ignoring `docs/brainstorms/*`, `docs/plans/*`, or `docs/solutions/*`.
- Report review outcomes, not dispatch mechanics.

## Fast Review

When the user explicitly asks for a quick/light/fast review and `mode:agent` is absent, announce the quick path and run only the inline fast pass plus `core-reviewer`. `mode:agent` always uses the full structured workflow.

## Severity and Routing

| Level | Meaning |
|---|---|
| P0 | Critical breakage, exploit, data loss, or corruption |
| P1 | High-impact normal-path defect or broken contract |
| P2 | Moderate issue with meaningful downside |
| P3 | Narrow, low-impact improvement |

Severity is urgency, not mutation permission. `autofix_class` is `gated_auto`, `manual`, or `advisory`; owner is `downstream-resolver`, `human`, or `release`. Read `references/action-class-rubric.md` only when routing is ambiguous. Synthesis may make routing more conservative, never less, without stronger evidence.

## Workflow

### 1. Resolve scope, intent, and plan

Read `references/review-scope.md` and follow it. It owns:

- `base:`, current-branch, remote-branch, and PR scope;
- local-aligned versus remote inspection safety;
- skip rules and no-checkout behavior;
- intent inference;
- explicit/conservative plan discovery and requirements extraction.

Stop on an invalid or inaccessible scope. Preserve the resolved diff, files, mode, refs, intent, plan data, PR context, and untracked exclusions for later stages.

### 2. Resolve shared project orientation

For local-aligned/current-checkout scope, set `SKILL_DIR` to this skill's directory and query `python3 "$SKILL_DIR/scripts/repo-profile-cache.py" get`. On a miss, use `references/agents/repo-profiler.md` to derive and persist the compact profile; on failure or `NO-CACHE`, continue without it. Never use the local cache for remote scope because it describes the wrong tree.

The profile is orientation, not evidence. Applicable project instructions and current code remain authoritative.

### 3. Assess criticality and select reviewers

Read the diff once and assess:

- trust/permission boundaries;
- money, durable data, and irreversible mutation;
- shared/public contracts and downstream consumers;
- cross-component state, ordering, and failure propagation;
- external/operational dependencies;
- silent-pass verification or deployment mechanisms;
- reversibility and containment.

Do not use changed-line count as a risk proxy.

Read `references/persona-catalog.md`. Always select `core-reviewer`, which covers correctness, testing, and maintainability. Add specialists only when the diff presents their runtime concern. Select `agent-native-reviewer` only for a changed capability that should be agent-operable. Select deployment verification only for risky migration operations.

Read the project instructions governing changed files. An inline standards finding requires both a direct rule quote and a violating line; otherwise suppress it. If `docs/solutions/` exists, search by changed modules/concepts and carry at most three strong Known Pattern notes. Historical guidance is context, not a defect.

Announce the core lenses and one short reason per specialist.

### 4. Dispatch review

Run a short inline fast pass for obvious high-signal defects. In default mode, label it preliminary; in `mode:agent`, keep it internal. Fast-pass findings enter merge at confidence 50, cannot create corroboration, and survive alone only as P0.

Create `/tmp/andrea-engineering/ce-code-review/<run-id>/`. Stage large diffs/file lists there once and pass paths instead of duplicating contents.

Before dispatch, read:

- `references/subagent-template.md`
- `references/diff-scope.md`
- `references/findings-schema.json`
- each selected `references/personas/<name>.md`

Spawn generic read-only Codex subagents with `spawn_agent`, passing the exact shared scope, intent, PR context, profile orientation, diff/files, run ID, and schema. Let every reviewer inherit the parent model. Respect Codex's active-agent limit with a bounded queue; capacity is backpressure, not reviewer failure.

Remote reviewers inspect fetched refs with `git show` or diff hunks, never stale workspace files. Subagents may write only their run artifact under `/tmp`; they never edit the project.

### 5. Merge findings

Read `references/merge-apply-contract.md` and run its merge stage. It owns schema validation, evidence gates, deduplication, confidence/corroboration, pre-existing separation, mode-aware demotion, stable numbering, triage groups, plan completeness, and protected-artifact filtering.

If every reviewer fails, return a degraded result with the reason. Otherwise continue even when some specialists fail and record them in Coverage.

### 6. Independently validate

Directly verify confidence-100 P2/P3 findings only when the cited line itself mechanically proves the issue. Runtime, cross-file, security, concurrency, performance, auth, and contract judgments never qualify.

For all P0/P1 and other surviving consequential findings, read `references/validator-template.md` and dispatch one fresh validator with the complete finding array. Cap only the P2/P3 tail at 15 total items; never exclude P0/P1. Apply each returned verdict independently. On validator infrastructure failure, keep P0/P1 marked degraded and drop unvalidated P2/P3. Prune triage groups after drops.

### 7. Apply fixes in default mode

Skip entirely in `mode:agent` or remote scope. Otherwise follow the apply stage in `references/merge-apply-contract.md`:

- apply clear, bounded, reversible improvements;
- do not apply design calls, disputed findings, or changes requiring product/security authority;
- run targeted tests/lint and revert any fix that fails verification;
- self-review only the autofix diff;
- commit one isolated `fix(review): ...` commit only when the pre-review tree was clean; leave fixes uncommitted when it was already dirty.

Never push.

### 8. Present and persist

Read `references/review-output-template.md` and the output stage of `references/merge-apply-contract.md`.

- **Default:** ASCII-safe markdown report plus a final compact Actionable Findings summary.
- **`mode:agent`:** one raw JSON object and nothing after it.

Always write run artifacts under `/tmp/andrea-engineering/ce-code-review/<run-id>/`, including synthesized findings, actionable findings, advisory outputs, per-agent JSON, metadata, and `report.md` or `review.json`.

## Final Quality Gate

Before delivery verify:

- every finding is specific and actionable or explicitly advisory;
- surrounding code was inspected and the line is accurate;
- severity and confidence are calibrated;
- pre-existing issues are separated;
- protected artifacts are respected;
- findings do not duplicate formatter/linter output;
- triage groups reference only surviving stable numbers;
- the verdict and final actionable list stand alone.

After output, stop. Do not offer push/PR actions or run post-review triage.

## References

| Reference | Load when |
|---|---|
| `references/review-scope.md` | Scope, intent, plan discovery |
| `references/repo-profile-cache.md` | Cache protocol details if needed |
| `references/persona-catalog.md` | Reviewer selection |
| `references/subagent-template.md` | Reviewer dispatch |
| `references/diff-scope.md` | Shared scope rules for reviewers |
| `references/findings-schema.json` | Reviewer JSON contract |
| `references/validator-template.md` | Single batched validation pass |
| `references/merge-apply-contract.md` | Merge, apply, JSON, artifacts |
| `references/review-output-template.md` | Markdown report skeleton |

Read only selected persona prompt files under `references/personas/`.
