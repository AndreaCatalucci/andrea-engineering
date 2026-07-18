---
name: ce-compound-refresh
description: "Refresh docs/solutions learnings against the current codebase. Use when auditing stale, overlapping, superseded, or drifted learnings; avoid general refactor, debugging, or code review unless docs/solutions is explicit."
---

# Compound Refresh

Immediately before writing user-facing text, read and follow
[`references/plain-language.md`](references/plain-language.md).

Keep `docs/solutions/` accurate, searchable, and non-redundant as the codebase changes. Review individual learnings before any pattern documents derived from them.

Before asking the user for input, read [`references/codex-interaction.md`](references/codex-interaction.md).

## Modes

Default to interactive mode. When the input contains `mode:headless`, remove that token and treat the remainder as the scope hint.

- **Interactive:** ask only for genuinely ambiguous maintenance decisions.
- **Headless:** never ask questions. Apply clear actions, mark ambiguous documents stale, and return a self-contained report. Do not commit, push, or open a PR unless the invoking workflow explicitly authorized shipping.

If the request is specifically to bootstrap `CONCEPTS.md`, ask whether the user wants a standalone repo-wide concept map or a normal refresh that updates vocabulary only for the refreshed scope. In headless mode, choose the normal refresh.

## Core rules

1. Match documentation to verified current behavior; do not turn documentation drift into a code-review project.
2. Prefer a no-write Keep over cosmetic churn.
3. Use Update only when the recommended solution remains correct.
4. Use Replace only when current evidence supports a trustworthy successor.
5. Check inbound links before Delete.
6. Delete obsolete documents; do not create or extend an archive directory. Git history is the archive.
7. Evaluate the document set as a whole. Contradictory or redundant guidance is more dangerous than an old but still-correct document.
8. Preserve unrelated user changes and stage only files owned by this run if later asked to commit.

## Phase 0: Resolve scope

Discover Markdown files under `docs/solutions/` with `rg --files`. Exclude `README.md` and legacy `_archived/` contents. Report `_archived/` as cleanup debt rather than treating it as active knowledge.

When a scope hint exists, resolve it in this order and stop at the first useful match:

1. directory name;
2. frontmatter `module`, `component`, or `tags`;
3. filename;
4. content match.

If a headless scope hint matches nothing, report the miss and stop; never widen silently. Without a hint, interactive mode may offer a focused area when the corpus is broad, while headless mode processes all candidates in bounded batches.

If no candidates exist, report that `ce-compound` can create the first learning after a verified problem is solved.

## Phase 1: Investigate

For every candidate, compare its claims with the current codebase and related documentation. Record:

- referenced paths, types, functions, and links that moved or disappeared;
- whether the recommended solution still matches current behavior;
- code examples or metadata that drifted;
- newer learnings, pattern documents, PRs, or issues that supersede it;
- inbound links and whether each citation is decorative or substantive;
- overlapping documents and their unique content;
- contradictions between documents;
- project-specific vocabulary surfaced by the learning.

Age alone is not evidence of staleness. Match investigation depth to claim specificity: exact code claims need defining source lines; general principles need enough evidence to prove they still apply.

For broad scopes, use `spawn_agent` with Codex's inherited model to investigate independent groups in parallel. Pass each agent explicit file ownership and require a read-only result containing path, evidence, recommended action, confidence, and open questions. Investigate overlapping documents together. Run replacement writers one at a time.

After individual learnings, inspect relevant `docs/solutions/patterns/` documents against their supporting learning set. A generalized rule without current support is a strong stale signal.

## Phase 2: Classify

Read [`references/action-classification.md`](references/action-classification.md) and assign exactly one action to every candidate:

- **Keep** — accurate and independently useful;
- **Update** — local drift, same core recommendation;
- **Consolidate** — compatible overlap with one clear canonical document;
- **Replace** — materially misleading guidance with sufficient successor evidence;
- **Delete** — implementation/problem is gone or guidance is wholly redundant, with no substantive inbound contract.

Every classification needs current evidence, confidence, and inbound-link evidence whenever Delete is possible. When replacement evidence is insufficient, mark the document stale instead of inventing a successor.

## Phase 3: Resolve ambiguity

In interactive mode, apply obvious Updates and clear Consolidations without ceremony. Ask one question only when:

- two actions remain genuinely plausible;
- a Delete is not unambiguous;
- the canonical document is unclear;
- a Replace will create a successor whose scope needs confirmation.

Lead with the recommendation, cite the decisive evidence, and show only plausible alternatives.

In headless mode, skip questions. Execute high-confidence actions and add or update `status: stale`, `stale_reason`, and `stale_date` for ambiguous cases. If a write fails, record the intended action under Recommended and continue.

## Phase 4: Execute

Read [`references/per-action-flows.md`](references/per-action-flows.md) and follow only the section matching each classification.

Key invariants:

- Keep performs no edit.
- Update changes only evidence-backed drift.
- Consolidate merges unique content into the canonical document, updates citations, then deletes subsumed documents.
- Replace uses one writer subagent, validates the successor, then deletes the old document.
- Delete repeats the inbound-link check immediately before removal and reclassifies if a substantive citation appears.

After any new or materially changed learning, run both bundled validators:

```bash
SKILL_DIR="<absolute path to this skill>";
python3 "$SKILL_DIR/scripts/validate-frontmatter.py" <learning-path>
```

```bash
SKILL_DIR="<absolute path to this skill>";
python3 "$SKILL_DIR/scripts/validate-doc-claims.py" <learning-path>
```

Treat claim-validator findings as adjudication input: fix bad citations and scaffolding, annotate intentional historical references, and never silently ignore flags.

## Phase 5: Reconcile vocabulary

Read [`references/concepts-vocabulary.md`](references/concepts-vocabulary.md). Apply its qualification rules to terms surfaced during investigation.

- If `CONCEPTS.md` exists, add missing in-scope core terms, refine inaccurate entries, merge duplicates, and remove implementation details or drift-prone values.
- If it does not exist and qualifying terms were found, seed the scoped domain's core vocabulary rather than creating a one-entry file.
- Do not expand beyond the refreshed domain and do not inject retrospective pointers into every learning.
- If nothing qualifies, record that explicit result in the report.

For a standalone repo-wide bootstrap, seed from the declared domain model, core types/models, and top-level domain docs, then continue to discoverability below without running learning classifications.

## Phase 6: Check discoverability

If root `AGENTS.md` exists, verify that it makes these artifacts discoverable:

- `docs/solutions/` as searchable past learnings, including enough structure/frontmatter detail to search it;
- `CONCEPTS.md`, when present, as shared domain vocabulary.

If awareness is missing, draft the smallest natural addition. In interactive mode, show the proposed `AGENTS.md` edit and get consent before applying it. In headless mode, report a discoverability recommendation and do not edit project instructions.

## Report

Return a full Markdown report with:

```text
Compound Refresh Summary
Scanned: N
Kept: N
Updated: N
Consolidated: N
Replaced: N
Deleted: N
Marked stale: N
CONCEPTS.md: <outcome>
```

Then list every processed file with its classification, evidence, action taken, and any remaining uncertainty. For consolidation, name the canonical and deleted documents plus the unique content merged. Keep no-edit results visible.

In headless mode, split writes into:

- **Applied** — changes successfully written;
- **Recommended** — changes that could not be written, with enough evidence for a human to apply them;
- **Legacy cleanup** — `_archived/` findings, when any.

Finish with modified paths and validation results. Leave changes uncommitted unless shipping was explicitly authorized; when authorized, follow the repository's normal commit/PR skill instead of duplicating git workflow here.

`ce-compound` captures a newly solved problem. `ce-compound-refresh` maintains the accuracy and shape of the existing knowledge set.
