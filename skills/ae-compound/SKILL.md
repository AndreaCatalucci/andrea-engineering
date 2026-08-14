---
name: ae-compound
description: Document one recently solved problem or durable project learning in docs/solutions/, with optional project-vocabulary updates. Use after verified, non-trivial work is complete.
---

# $ae-compound

Immediately before writing user-facing text, read and follow
[`references/plain-language.md`](references/plain-language.md).

Capture one verified learning while its evidence is fresh. The root agent owns research, synthesis, writing, and validation so the final document preserves the full problem-solving narrative without subagent handoffs.

## Usage

```text
$ae-compound [optional context]
$ae-compound history:true [optional context]
$ae-compound deep:true [optional context]
$ae-compound mode:headless [optional flags and context]
```

- `history:true` searches prior sessions for relevant failed approaches or recurring evidence. Do not search session history otherwise.
- `deep:true` adds one independent, read-only semantic grounding review after the root agent's validation. Use only when explicitly requested.
- `mode:headless` suppresses questions and emits a structured terminal report. It does not imply `history:true` or `deep:true`.
- Strip recognized flags before treating the remaining arguments as context.

## Scope

Document exactly one learning per run. If several independent lessons emerged, process them sequentially so each is grounded against the current tree and related documentation.

The learning must be:

1. Solved, not merely diagnosed
2. Verified by tests, observed behavior, or other concrete evidence
3. Non-trivial enough to help future work

If these conditions are not met, explain why documentation was skipped. In headless mode, use the structured skipped report below.

If asked only to bootstrap `CONCEPTS.md`, redirect to `ae-compound-refresh`; this skill updates vocabulary only as a side effect of documenting a real learning.

## Durable contract

Read supporting files only when their step needs them:

- `assets/resolution-template.md` — section structure for a new solution document
- `references/schema.yaml` — canonical frontmatter fields and enums
- `references/yaml-schema.md` — category mapping and YAML-safety rules
- `references/concepts-vocabulary.md` — vocabulary inclusion and format rules
- `references/grounding-validation.md` — claim adjudication and optional reviewer prompt
- `references/agents/session-historian.md` — synthesis rules for `history:true`
- `scripts/session-history/` — discovery and extraction for `history:true`
- `scripts/validate-frontmatter.py` — parser-safety validation
- `scripts/validate-doc-claims.py` — paths, SHAs, links, and drafting-scaffold validation

Set `SKILL_DIR` to the directory containing this `SKILL.md` before invoking bundled scripts.

## Workflow

The root agent performs the workflow in order. Do not dispatch context analyzers, solution extractors, related-doc finders, repo profilers, or specialist reviewers.

### 1. Reconstruct the learning

Use the current conversation and repository evidence to identify:

- Observable symptom or motivation
- Investigation and failed approaches that teach something durable
- Root cause or governing insight
- Verified solution and why it works
- Prevention, diagnostic, or reuse guidance
- Files, tests, commits, PRs, and external references that support the claims

Inspect the current diff, relevant commits, tests, and defining source as needed. Never promote conversation memory into a code-behavior claim without checking the current source. Prefer PR references over raw commit SHAs when both identify the same change.

For a knowledge-track learning, frame the durable decision or pattern rather than inventing a bug narrative. Omit empty or inapplicable sections instead of filling them with generic prose.

### 2. Check related solutions and overlap

Enumerate `docs/solutions/` fresh and search by the problem's concrete signals: error text, module names, domain terms, root cause, and solution mechanism. Read only plausible matches.

Assess overlap across problem, root cause, and solution:

| Overlap | Action |
| --- | --- |
| High: same problem, cause, and solution | Update the existing document; preserve its path and frontmatter shape, add `last_updated`, and refresh stale evidence |
| Moderate: related area but meaningfully different cause or solution | Create a new document and record a narrow `ae-compound-refresh` recommendation |
| Low or none | Create a new document |

Do not edit other solution documents during capture. Cross-document consolidation and broad drift repair belong to `ae-compound-refresh`.

### 3. Optional historical evidence

Run only with `history:true`.

Use the bundled `scripts/session-history/` tooling to find Codex sessions for the current repository. Apply a strict relevance gate before extraction: candidates must concern the same concrete problem, component, failure mode, or solution mechanism.

If relevant candidates exist, read `references/agents/session-historian.md` and synthesize the evidence in the root agent. Do not dispatch a historian. Incorporate useful failed approaches or recurring patterns and mark historical-session material as `(session history)`. If scripts are unavailable or no relevant sessions exist, continue without history and report that outcome.

### 4. Write or update the solution

For a new document:

1. Read `assets/resolution-template.md`.
2. Read `references/yaml-schema.md` and classify the learning into the narrowest fitting category.
3. Read `references/schema.yaml` and construct valid frontmatter.
4. Preserve the template's section order unless the user requested another structure.
5. Write `docs/solutions/<category>/<descriptive-slug>.md`.

For an existing document with high overlap, integrate the fresher evidence instead of appending a second narrative. Preserve useful historical context and remove claims contradicted by the current tree.

The document should capture concrete evidence, not the conversation itself. Remove drafting labels, agent commentary, placeholder text, and incidental process details.

### 5. Capture qualifying vocabulary

Read `references/concepts-vocabulary.md`, then scan the learning and surrounding conversation for qualifying project-specific entities, named processes, and status concepts.

- If `CONCEPTS.md` exists, add missing qualifying terms or refine entries when the learning provides better evidence.
- If it does not exist and clear qualifying terms surfaced, create it and seed only the learning's immediate domain area according to the reference.
- Verify behavioral definitions against their defining source.
- Inspect only the coherence neighborhood of entries touched; defer broader auditing to `ae-compound-refresh`.
- If no terms qualify, record that the vocabulary scan found none.

Vocabulary updates are part of the capture and require no separate prompt. Do not turn `CONCEPTS.md` into an implementation index or repo-wide glossary.

### 6. Validate frontmatter

Run:

```bash
python3 "$SKILL_DIR/scripts/validate-frontmatter.py" <doc-path>
```

Fix and rerun until it exits successfully. If the script cannot be resolved, manually verify its exact safeguards:

- Opening and closing delimiters are lines containing `---`.
- Unquoted top-level scalar values contain neither ` #` nor `: `.
- Array values follow the quoting rules in `references/yaml-schema.md`.

Report a manual fallback rather than silently skipping validation.

### 7. Ground all durable claims

Read `references/grounding-validation.md`.

First run the deterministic validator:

```bash
python3 "$SKILL_DIR/scripts/validate-doc-claims.py" <doc-path>
```

Adjudicate every flag; do not auto-fix blindly. A historical path may be intentionally cited, while an unsupported current-path or SHA claim may need correction or qualification. Rerun after edits until all remaining flags are intentionally resolved. If the script is unavailable, apply the reference's manual checklist and report the fallback.

Then perform a root-agent semantic pass over the solution document and any vocabulary entries changed in this run:

- Verify behavioral claims against the defining source.
- Verify countable assertions for internal completeness.
- Verify merge-state claims with available repository or GitHub evidence; mark them degraded when offline.
- Correct contradicted claims and soften or remove claims that cannot be verified.
- Rerun deterministic validation after substantive edits.

With `deep:true`, dispatch exactly one read-only generic reviewer using the semantic validator prompt from `references/grounding-validation.md`. Give it the document path, changed vocabulary entries, and relevant repository scope; do not copy the full document or source into the prompt. Adjudicate its evidence-backed findings, then rerun affected validators. The reviewer must not edit files.

### 8. Finish without expanding scope

Recommend `ae-compound-refresh` only when the new evidence identifies a concrete stale or overlapping target. Provide the narrowest useful scope: a file, component, category, or pattern topic. Do not invoke a refresh automatically.

End after reporting the result. Do not present a follow-up menu.

## Output

Interactive output should stay compact:

```text
Documentation complete

File: docs/solutions/<category>/<filename>.md (created | updated)
Overlap: <none | low | moderate with path | high; existing document updated>
Grounding: <clean | flags adjudicated | degraded detail>
History: <not requested | no relevant sessions | evidence incorporated>
Vocabulary: <no qualifying terms | CONCEPTS.md created/updated summary>
Deep review: <not requested | findings adjudicated>
Refresh recommendation: <none | narrow scope>
```

Headless success output must end with `Documentation complete`:

```text
File: docs/solutions/<category>/<filename>.md (created | updated)
Track: <bug | knowledge>
Category: <category>
Overlap: <result>
Grounding: <result>
History: <result>
Vocabulary: <result>
Deep review: <result>
Refresh recommendation: <none | narrow scope>

Documentation complete
```

When preconditions fail in headless mode:

```text
Reason: <one-sentence explanation>

Documentation skipped
```

## Quality bar

A successful capture:

- Produces or meaningfully updates one solution document
- Explains the causal mechanism, not only the patch
- Records useful failed approaches when evidence exists
- Grounds durable claims in current source or labels historical/degraded evidence
- Avoids duplicating an existing solution
- Uses valid, searchable frontmatter
- Updates only qualifying vocabulary
- Leaves broad knowledge-store maintenance to `ae-compound-refresh`

## Auto-invoke signals

Phrases such as "that worked", "it's fixed", "working now", or "problem solved" may indicate a candidate learning. Auto-invocation still requires the solved, verified, and non-trivial preconditions; do not document every successful edit.
