---
title: Lightweight code review protocol and handoff
date: 2026-08-11
type: refactor
plan_format: andrea-plan/v1
plan_readiness: implementation-ready
requirements_source: ae-plan-bootstrap
execution: code
source_ideation: docs/ideation/2026-08-11-lightweight-code-review-ideation.html
---

# Lightweight code review protocol and handoff

## Goal

Reduce the fixed and duplicated tokens used by `ae-code-review` without changing which reviewers run, what they inspect, the evidence bar, or independent validation.

**Source:** Internal `ae-code-review` instructions and the selected directions in the linked ideation document.
**Input:** A resolved review scope, intent, plan requirements, PR context, project profile, diff paths, reviewer persona, and run ID.
**Operation:** Dispatch each reviewer with a lean self-contained packet, validate its full JSON file deterministically, and return a small receipt plus merge view.
**Outcome:** The smallest core review carries no more than 1,500 words of shared non-persona instructions before run-specific context, while valid findings, fallback behavior, and final review output remain equivalent.

Authority order: this plan, existing `ae-code-review` scope and merge rules, then local implementation choices. Stop rather than weakening evidence, confidence, remote-scope safety, or validation to meet the target.

## What We're Building

### Summary

The review keeps one core reviewer and the same risk-selected specialists. Each reviewer starts with fresh context, writes one full result file, and normally returns only a receipt. A small standard-library helper validates the file and derives the compact fields used during merge.

### Requirements

- R1. Reviewer selection, specialist triggers, scope rules, evidence thresholds, false-positive suppression, confidence anchors, and independent validation remain behaviorally unchanged.
- R2. The initial reviewer packet contains at most 1,500 words of shared non-persona instructions, measured without the persona, plan, PR data, file list, or diff.
- R3. Every reviewer and validator is spawned with no inherited conversation history and receives a complete packet containing authoritative intent, scope, requirements, applicable project instructions, and selected Known Pattern notes.
- R4. A reviewer writes the full JSON once, runs the helper, and returns its receipt when valid. The parent reruns the helper before accepting it.
- R5. The standard-library helper fails closed on malformed or unsupported data, verifies SHA-256, and emits compact fields with a stable source key of reviewer, file digest, and finding index.
- R6. A write or reviewer-side validation failure returns the existing compact inline result. A parent-side failure gets one repair request, then marks that reviewer failed; every degraded path appears in Coverage.
- R7. Final `mode:agent` JSON and default markdown retain the full explanation, evidence, residual risks, testing gaps, and actionable findings required by current callers.

### Scope

This change does not combine reviewers, alter risk classification, introduce a fast path, remove fresh validation, or defer writing `why_it_matters`. Prompt caching may benefit from a stable prefix but is not an acceptance criterion because it does not reduce nominal tokens.

## How We'll Build It

### Technical Decisions

- D1. Keep persona files separate. The concise protocol retains the complete artifact field list and all semantic rules for impact, evidence, suppression, confidence, and fixes. Only machine-checkable schema syntax, enums, and bounds move to the helper.
- D2. Add one deep helper under `skills/ae-code-review/scripts/` rather than spreading validation and projection rules through the skill. It supports exactly the JSON Schema features used by `findings-schema.json` and rejects schema features it cannot enforce.
- D3. Use explicit fresh-context subagent dispatch. The packet, not prior conversation, is the complete source for intent, requirements, scope, repository orientation, and output rules.
- D4. Treat the full JSON as authoritative. Synthesis preserves each compact finding's source key and reloads full records before validation and final output. Inline findings exist only as the documented fallback.

## Work Steps

### W1. Add deterministic result validation and projection

**Goal:** Provide the checked handoff required by R4-R6 before changing reviewer output.

**Affected area:** `skills/ae-code-review/scripts/`, `skills/ae-code-review/references/findings-schema.json`.

**Constraints:** No package installation. Validate required fields, types, enums, bounds, evidence, digest, source keys, and compact projection. Unsupported schema keywords fail clearly.

**Verification:** Standard-library unit tests cover a valid empty review, a valid finding, missing fields, invalid enums and confidence, missing evidence, digest mismatch, unsupported schema features, and stable compact output.

### W2. Slim and isolate reviewer dispatch

**Goal:** Meet R1-R4 by replacing repeated prose and duplicate model output while keeping the same review decisions.

**Affected area:** `skills/ae-code-review/SKILL.md`, `skills/ae-code-review/references/subagent-template.md`.

**Approach:** Assemble a fresh-context packet from resolved inputs, including governing instruction text and up to three selected Known Pattern notes. The reviewer writes one full file, runs the helper, and returns its receipt or documented inline fallback. The parent validates receipts independently and allows one repair attempt.

**Verification:** A dispatch fixture proves the packet includes intent, requirements, PR context, scope refs, orientation, governing instructions, Known Patterns, diff paths, persona, run ID, semantic rules, and output path. The shared packet remains at most 1,500 words.

### W3. Preserve merge, validation, and caller behavior

**Goal:** Prove R1, R6, and R7 across the rest of the review pipeline.

**Affected area:** `skills/ae-code-review/references/merge-apply-contract.md`, `skills/ae-code-review/references/validator-template.md`.

**Constraints:** Preserve source keys through filtering, corroboration, and deduplication, then load full records before validation and output. Do not change confidence, severity, routing, numbering, validation selection, or protected-artifact behavior. Validators use fresh context and inspect independently.

**Verification:** Fixtures cover no findings, duplicates with source lineage, confidence-75 evidence, write failure, reviewer-side validation failure, parent-side repair exhaustion, P0/P1 validation, soft buckets, and final `mode:agent` JSON.

## How We'll Check It

- `python3 -m unittest discover -s tests -p 'test_review_artifact.py'`
- Run the new helper against valid and invalid reviewer fixtures and confirm stable JSON plus non-zero fail-closed errors.
- Measure the assembled shared reviewer packet with `wc -w`; it must be at most 1,500 words.
- Confirm every selected reviewer and validator dispatch explicitly uses fresh context and receives the required packet fields.
- `scripts/sync-shared-skill-assets --check`
- `git diff --check`

## Done When

The review produces the same reviewer coverage, findings, validation decisions, and caller-facing reports from a materially smaller self-contained packet; normal reviewer handoff contains only a checked receipt; fallback paths are visible and tested; and no runtime dependency has been added.
