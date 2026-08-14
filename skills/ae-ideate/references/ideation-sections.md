# Ideation Artifact Contract

Load this content contract at save time with exactly one renderer: `references/html-rendering.md` or the canonical `references/markdown-rendering.md`.

The artifact is a ranked, critiqued candidate set plus the evidence and rejection record needed to judge it. It is not a requirements document, implementation plan, or status tracker.

## Section order

Render these sections in order:

1. Visible title and metadata
2. Relevant Context
3. Topic Areas, when applicable
4. Ranked Ideas
5. Rejection Summary

Do not add next steps, workflow state, skill instructions, or work steps.

## Metadata

Include:

- `date` — `YYYY-MM-DD`
- `topic` — kebab-case slug
- `focus` — optional focus hint; omit when open-ended
- `mode` — `repo-grounded`, `elsewhere-software`, or `elsewhere-non-software`

Markdown uses YAML frontmatter. HTML renders the values once as visible header text. Do not add document or per-idea status fields.

## Relevant Context

Include the consolidated Phase 1 grounding that qualified the ideas. Label the content “Codebase Context” in repo mode and “Topic Context” elsewhere. Preserve concrete evidence, constraints, pain points, and opportunity signals; omit orchestration details.

## Topic Areas

When Phase 1.5 produced areas, list all 3–5 in the topic's own language. When decomposition was attempted but skipped, record one line:

- `Decomposition skipped — atomic subject`, or
- `Decomposition skipped — surprise-me mode`

Omit the section when areas are not applicable.

## Ranked Ideas

Rank every survivor. Each idea must include:

- **Title**
- **Description** — concrete explanation
- **Area** — omit only when decomposition was skipped
- **Basis** — `direct:`, `external:`, or `reasoned:` evidence that supports the move
- **Rationale** — why that basis makes the move significant
- **Downsides** — real tradeoffs and costs
- **Confidence** — `0–100%`
- **Complexity** — `Low`, `Medium`, or `High`

Keep all fields visible. HTML uses expanded idea cards and a ranked jump list; Markdown uses headings and labeled fields.

### Visual decision

Add an illustrative visual only when an idea hinges on a structure a picture communicates faster: a relationship, flow, before/after, analogy map, arrangement, or quantitative comparison. Skip visuals for single propositions and anything that merely restates the title.

Keep visuals conceptual, not specifications or wireframes. Show the basis or why-it-matters at the idea's altitude. Prose must remain complete without the visual. Follow the selected renderer for mechanics: responsive inline SVG in HTML or Mermaid in Markdown when suitable.

Decide per idea; there is no quota or cap.

## Rejection Summary

Record every considered-and-cut idea in a table with a one-line rejection reason. Add any area with zero survivors as its own row, including whether recovery failed or hit the cap.

## Completion check

Before saving, verify:

- Every survivor has every required field and a basis that supports its move.
- Every rejection has a reason.
- Grounding and areas match the run that generated the candidates.
- The ranked order matches the final arbitration.
- No placeholder, process note, lifecycle state, or downstream instruction remains.
- The renderer contains the full content; format changes presentation only.
