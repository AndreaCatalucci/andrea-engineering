---
title: Radical Eight-Skill Catalog - Plan
date: 2026-08-15
type: refactor
plan_format: andrea-plan/v1
plan_readiness: implementation-ready
requirements_source: ae-plan-bootstrap
execution: code
---

# Radical Eight-Skill Catalog - Plan

## Goal

Replace the 30-skill catalog with eight small, human-readable skills: `ae-ideate`, `ae-brainstorm`, `ae-plan`, `ae-work`, `ae-debug`, `ae-review`, `ae-ship`, and `ae-learn`.

**Source:** Confirmed catalog and simplification decisions.
**Input:** Current skills, packaging, and README.
**Operation:** Rewrite the eight skills around their essential loops; delete everything else.
**Outcome:** The whole catalog can be understood and changed without navigating a framework, and ordinary skill use loads far less text.

## What We're Building

### Requirements

- R1. Expose exactly the eight named skills with no aliases or compatibility layer.
- R2. Rewrite each `SKILL.md` to at most 400 words and keep all eight entry files within 2,800 words total.
- R3. A normal invocation loads only its entry file. A selected recipe may add one file of at most 300 words; load another only when the task actually crosses that boundary.
- R4. Prefer the user's natural language over selector grammars, modes, schemas, receipts, state machines, scoring systems, and generated reports.
- R5. Do not automatically invoke review, learning, planning, browser work, or shipping. The only compound path is explicitly requested autonomous work, which uses only the stages needed by that request.
- R6. Delete instructions, references, scripts, tests, and assets that exist mainly to validate the workflow rather than perform its essential job. Do not replace them with new infrastructure.
- R7. Keep commentary under 60 words per update and default final handoffs under 150 words. Read the smallest relevant file range and do not repeat context in multiple artifacts.

### Essential Skill Loops

| Skill | Keep only | Default output budget |
|---|---|---:|
| `ae-ideate` | Inspect context, generate distinct options, compare, recommend. No questions. | 700 words |
| `ae-brainstorm` | Ask one useful question at a time, resolve decisions, summarize confirmed requirements. | 100 words per turn; 500 final |
| `ae-plan` | Inspect the relevant code, settle consequential choices, write 2-4 outcome steps. | 700 words |
| `ae-work` | Read the request or plan, implement it, run only directly relevant existing checks, report. Autonomous work may include plan and ship when requested. | 60-word updates; 150 final |
| `ae-debug` | Reproduce, isolate the cause, fix when authorized, run the narrow regression check, report cause and result. | 200 words |
| `ae-review` | Inspect the requested target and return only material findings with locations; say so plainly when none exist. It is an explicit tool, not a mandatory gate. | 500 words |
| `ae-ship` | Perform only the requested commit, push, PR, feedback, or watch action and return its state or URL. | 120 words |
| `ae-learn` | Capture one reusable lesson. Run `garden [scope]` only when explicitly requested to merge, prune, or refresh existing lessons. | 600-word lesson; 300-word garden report |

Project-fit exploration belongs to `ae-ideate`. Product-direction questions belong to `ae-brainstorm`. `ae-brainstorm` writes `STRATEGY.md` only when asked.

Absorb `lfg`, optimize, simplify, polish, dogfood, and worktree into `ae-work`; document, browser, and Xcode review into `ae-review`; commit, PR feedback, and PR watching into `ae-ship`; and compound refresh into `ae-learn garden`. Delete explain, POV, product pulse, promote, Proof, Riffrec analysis, setup, strategy, and sweep.

## How We'll Build It

- D1. Rewrite from a blank page instead of merging old prose. Copy an old instruction only when removing it would prevent the essential loop above.
- D2. Keep recipes beside their owner with obvious names. Retain a script only when it performs essential, error-prone work more clearly than short instructions.
- D3. Remove `lfg`; autonomous delivery becomes a small `ae-work` recipe. Rename `ae-code-review` to `ae-review`, `ae-commit-push-pr` to `ae-ship`, and `ae-compound` to `ae-learn`.
- D4. Move useful behavior from work, review, ship, and learn specialists into lazy recipes, then delete all retired directories. Delete peripheral skills rather than finding them new homes.
- D5. Update all host metadata and README examples directly to the eight names and bump `3.19.0-fork.2` to `3.19.0-fork.3`.

## Work Steps

### W1. Rewrite the eight entry files

Write each essential loop in plain language within its budget. Remove routing tables, exhaustive edge cases, duplicated safety prose, phase ceremony, mandatory review tails, and internal reporting protocols.

### W2. Keep only tiny lazy recipes

For absorbed behavior, write the smallest recipe that makes the action usable. Delete unused references, validators, report renderers, schemas, orchestration state, and tests tied to removed machinery. Rewrite cross-skill references to the eight names.

### W3. Collapse the distributed catalog

Delete the 22 retired public directories, obsolete shared-asset mirrors, and stale documentation. Make Codex, Claude Code, and Grok Build expose the same eight entrypoints.

## How We'll Check It

No new review, evaluation, validation framework, or test suite. The implementer reads all eight entry files once, confirms the word budgets and eight-name catalog, and runs only existing checks directly affected by retained runtime scripts or packaging edits.

## Done When

There are eight obvious skills; a human can read their complete entry surface in one sitting; normal use loads one short file; optional behavior stays lazy; nothing automatically expands into review or ceremony; and no deleted workflow survives as hidden compatibility machinery.
