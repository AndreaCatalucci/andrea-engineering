# The Optional Full Write-Up

Load this only when the user asks for the full write-up. The default is the
short chat recommendation; this optional version is for reading, sharing, or
handing to the next skill.

## What it contains

The verdict, expanded — lead with the decision, then the evidence the TL;DR omitted:

- **Recommendation** — the grade and any conditions ("yes, if ..."), first.
- **Question** — what is being considered, why, what the project uses now, and
  how hard the choice would be to undo.
- **Project evidence** — cited `file:line`, issue, and PR evidence.
- **External evidence** — cited authoritative sources and dates.
- **Alternatives** — including keeping the current approach and doing nothing.
- **What would change the recommendation** — for Tier 2 and 3.
- **Uncertainty** — anything not verified.

## Format and economy

- **HTML by default** — a single self-contained file (a verdict is a thing people share). Use markdown when the user asks, or when the write-up will feed `ae-brainstorm`/`ae-plan`.
- Write to a temp path, or under `docs/` when the user wants it kept; announce the absolute path. Do **not** introduce a new mandated `docs/` location — that store is deferred.
- Lead with the recommendation and cite evidence instead of pasting research
  notes. Write a case a person can follow, not a research dump.

## Sharing

Publish via whatever the user has — best available, never required:

- `ae-proof` (Proof) — markdown-only, so if the report is HTML, render a throwaway markdown copy of it as the Proof source.
- Otherwise an available HTML publishing tool the user has connected.
- If neither is reachable, the local file is the deliverable — announce its path.
