---
title: Lightweight Ideation Workflow - Plan
date: 2026-08-11
type: refactor
plan_format: andrea-plan/v1
plan_readiness: implementation-ready
requirements_source: ce-plan-bootstrap
execution: code
related_plan: docs/plans/2026-08-11-001-refactor-lightweight-code-review-plan.md
---

# Lightweight Ideation Workflow - Plan

## Goal

Reduce `ce-ideate` token use without reducing grounding, frame diversity, candidate volume, area coverage, independent basis verification, or final-document quality.

**Source:** Internal `ce-ideate` instructions and the receipt pattern selected in the related code-review plan.
**Input:** A resolved subject, mode, focus, grounding summary, constraints, topic areas, assignments, and run directory.
**Operation:** Load instructions only for the active phase, use a small fresh-context fleet, and exchange validated files through receipts.
**Outcome:** `SKILL.md` is at most 2,000 words, fixed agent protocols are at most 700 words, and the default fleet falls from five generation agents to three while retaining six frames and 36-48 raw candidates.

Coverage and verification rules outrank token targets. Stop rather than silently shrinking them.

## What We're Building

### Summary

The root becomes a short orchestration spine with optional branches in phase-specific references. Agents receive no inherited conversation history, write schema-valid results once, and return checked receipts. The root and verifier read authoritative files rather than repeated candidate prose.

### Requirements

- R1. Default to three generation agents, each handling two dissimilar frames with separate quotas. Preserve six frames, 6-8 candidates per frame, generation-before-critique, survivor count, and output fields.
- R2. Reduce `skills/ce-ideate/SKILL.md` to at most 2,000 words by moving optional intake, mode, research-artifact, and delivery details behind phase-specific references.
- R3. Keep generation, recovery, verifier, critic, and distillation fixed protocols at or below 700 words, excluding run-specific grounding and assignments.
- R4. Give every agent a complete fresh-context packet preserving constraints, evidence provenance, scope, areas, assignment quotas, and evidence-read budget.
- R5. Agents write candidate JSON once and normally return a receipt. The parent revalidates every file and digest before use.
- R6. A standard-library helper validates candidate and verdict files, projects merge fields, and follows the related review plan's write-failure, one-repair, and degraded-coverage behavior.
- R7. Persist consolidated candidates, verifier verdicts, raw checkpoints, rejection accounting, and final output in the run directory.
- R8. Add no runtime dependency or prompt-caching assumption.

### Dispatch Contract

| Mode | Generation fleet and assignments | Candidate quota | Evidence-read budget |
|---|---|---|---|
| Default software | 3 agents: pain + constraint; inversion + analogy; leverage + assumption | 6-8 per frame | Up to 4 per frame, 24 total |
| Issue tracker | At most 2 agents; distribute 3-4 dynamic themes round-robin | 6-8 per theme | Up to 5 per theme, 20 total |
| Surprise me | 4 agents: pain; analogy; inversion + constraint; leverage + assumption | 6-8 per frame | Up to 5 per frame, 30 total |
| Go deep | 6 agents, one per frame | 6-8 per frame | Up to 10 per frame, 60 total |
| Non-software Quick | Root-only compact round | Existing 3-5 survivors | Existing root research budget |
| Non-software Standard | Same 3 paired agents as default | 5-8 per frame | Up to 4 per frame |
| Non-software Full | 6 agents, one per frame | 5-8 per frame | Up to 10 per frame |
| Recovery | 1 agent covering at most 2 missing areas | 3-5 per area | Up to 3 per area |

## How We'll Build It

### Technical Decisions

- D1. Keep `SKILL.md` as the phase map and invariant list. Load elsewhere-only, large-research, or delivery branches only when selected.
- D2. Add an ideation-specific schema and helper under `skills/ce-ideate/`. Reuse receipt vocabulary and failure behavior, not a generic review/ideation framework.
- D3. Keep ambition, scope, basis types, area spread, quotas, and direct-evidence rules in the agent protocol. Code handles structure, digesting, and projection only.
- D4. Give each original a stable source key: kind, assignment ID, checked-file digest, and index. Every consolidated candidate gets a `candidate_id` and parent source keys. Deduplication retains all parents; combinations and root synthesis list their inputs; recovery candidates identify their recovery assignment. The verifier reports by `candidate_id`.
- D5. Inline fallback is not trusted prose: the parent persists it as candidate JSON, runs the same validation, and only then consolidates it.

## Work Steps

### W1. Make the root workflow progressively loaded

**Affected area:** `skills/ce-ideate/SKILL.md`, `skills/ce-ideate/references/`.

Move branch detail behind phase routes while preserving phase order. Verify word budgets and map every existing rule to the spine or one reachable reference. Cover repo, elsewhere-software, non-software depths, issue, surprise, resume, research-document, and output-format branches.

### W2. Add fresh-context candidate files and receipts

**Affected area:** `skills/ce-ideate/references/divergent-ideation.md`, `skills/ce-ideate/references/universal-ideation.md`, `skills/ce-ideate/scripts/`.

Implement standard-library validation for required fields, basis tags, area rules, quotas, digests, source keys, candidate lineage, and deterministic projections. Test every dispatch-table row, single and paired assignments, inline fallback, write failure, one repair, recovery, and degraded coverage.

### W3. Keep verification and delivery complete

**Affected area:** `skills/ce-ideate/references/post-ideation-workflow.md`, `skills/ce-ideate/references/ideation-sections.md`.

Make the verifier consume consolidated candidates by path and emit one verdict file by `candidate_id`. Sealed grounding fixtures compare old and new protocols for raw count, frame/theme and area coverage, valid bases, disposition coverage, rejection accounting, survivor fields, and degraded-path reporting. Run one representative end-to-end ideation and render audit.

## How We'll Check It

- `python3 -m unittest discover -s tests -p 'test_ideation_artifact.py'`
- Word-budget and routing fixtures for the root and assembled agent protocols.
- Sealed-context comparisons across every dispatch mode.
- `scripts/sync-shared-skill-assets --check`
- `git diff --check`

## Done When

The workflow produces the same required coverage, provenance, verification, rejection record, and final document with a three-agent default; normal returns are checked receipts; deeper fleets require an explicit mode; and every fallback is visible and tested.
