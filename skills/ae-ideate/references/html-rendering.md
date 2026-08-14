# Ideation HTML Rendering

Load this reference only when `OUTPUT_FORMAT=html`. Use `ideation-sections.md` as the content contract; this file defines presentation.

## Output contract

Produce one self-contained HTML5 file:

- Put CSS in one `<style>` block.
- Use no external stylesheets, scripts, frameworks, or companion assets.
- Put diagrams inline as SVG.
- Keep all semantic content in HTML text; CSS and SVG never carry unique meaning.
- Render metadata once as visible text. Do not mirror it in JSON, `data-*`, or metadata tags.
- End with a visible footer containing the composition timestamp and source (`ae-ideate` plus an explicit upstream document when one exists).

Use UTF-8, a descriptive `<title>`, viewport metadata, and semantic HTML.

## Page design

Create a polished reading document, not an application UI.

- Center the page in a responsive container around `900px`; keep prose near `70ch`.
- Use a system font stack, comfortable line height, and a clear type scale.
- Establish a restrained palette through CSS custom properties for page, surface, text, muted text, border, accent, and soft accent.
- Meet readable contrast on every local background. Do not reuse page-muted text inside tinted cards when it becomes faint.
- Leave body `<strong>` text in the normal text color.
- Use consistent rounded shapes for chips and cards. Differentiate by full tint and label color, never a stripe on one edge.
- Use whitespace and typography for hierarchy; avoid decorative gradients, hero art, animation, glass effects, and dashboard chrome.
- Honor an explicit style request from the current conversation. Otherwise use the restrained default above; do not inspect separate design systems.

Include responsive rules for narrow screens:

- Reduce outer padding.
- Stack multi-column layouts.
- Allow tables to scroll horizontally.
- Keep tap targets and anchor offsets usable.

Add a minimal print stylesheet that removes decorative shadows and preserves readable contrast.

## Semantic structure

Use this document shape:

```html
<header>
  <p class="eyebrow">Ideation</p>
  <h1>Ideation: Topic</h1>
  <dl class="metadata">...</dl>
</header>
<main>
  <section id="grounding-context">...</section>
  <section id="topic-areas">...</section>
  <section id="ranked-ideas">...</section>
  <section id="rejection-summary">...</section>
</main>
<footer class="composition-signal">...</footer>
```

- Match section headings to `ideation-sections.md`: Relevant Context, Topic Areas, Ranked Ideas, Rejection Summary.
- Omit Topic Areas only when the content contract says it is inapplicable.
- Use `<article id="idea-1">` for each surviving idea and show its rank visibly in the card heading.
- Use `<dl>` with visible `<dt>` labels for Area, Basis, Rationale, Downsides, Confidence, and Complexity.
- Keep idea cards fully expanded. Do not hide their substance in `<details>`.
- Use a real `<table>` for the rejection summary with visible column headings.
- Keep labels, ranks, and field values in text rather than attributes or generated CSS content.

The HTML source must remain understandable to a text-reading agent. Prefer `<header>`, `<main>`, `<section>`, `<article>`, `<nav>`, `<dl>`, and `<table>` over generic `<div>` nesting.

## Navigation

Add a compact top navigation linking to the major sections. At the start of Ranked Ideas, add a numbered jump list linking to every idea card. Use stable lowercase ASCII IDs.

Do not add JavaScript for navigation. Native anchors are sufficient.

## Idea cards

Make the candidate set easy to compare without flattening its reasoning:

- Show rank and title first.
- Put area, confidence, and complexity in one compact metadata row.
- Give Description and Basis the strongest body emphasis.
- Keep Rationale and Downsides clearly labeled and fully visible.
- Use confidence and complexity colors only as secondary signals; always include their text values.
- Keep all cards structurally consistent even when one field is longer.
- Let the top-ranked idea receive a subtle full-card tint or “Top pick” badge, not a radically different layout.

Do not reduce the cards to dashboard metrics. The prose and basis are the document's value.

## Illustrative visuals

Add a visual only when an idea hinges on a shape that a picture communicates faster: a flow, relationship, before/after, analogy mapping, structural arrangement, or quantitative comparison. Do not add a quota or decorate single-point ideas.

Render visuals as responsive inline SVG inside their idea card:

- Include `viewBox`, `role="img"`, and a concise accessible label.
- Keep the idea's full meaning in prose; the SVG only accelerates understanding.
- Stay conceptual. Do not turn an ideation direction into an architecture specification or wireframe.
- Keep labels legible at rendered size.
- Route arrows and shape edges around text. If necessary, use a restrained background-colored text halo.
- Keep arrow labels near the relevant line and avoid long paths crossing unrelated elements.
- Use geometry and labels before relying on color.
- Ensure the visual remains understandable in grayscale and on narrow screens.

Skip a visual when its only content would restate the title.

## Grounding and rejection sections

Render Relevant Context as readable prose with small grouped lists or callouts only when the content has a natural grouping. Do not turn evidence into a wall of chips.

Render Topic Areas as a compact numbered list or uniform cards. Preserve the topic's own vocabulary.

Render Rejection Summary as a concise table. Include every considered-and-cut idea and its one-line reason, plus any unrecovered area gap. Keep this section visually quieter than Ranked Ideas but fully readable.

## Links and code

- Render URLs as clickable links.
- Render paths, identifiers, and code terms with `<code>`.
- Do not invent repository or tracker URLs.
- Use descriptive link text and visible focus styles.

## Final audit

Before saving, inspect the source and rendered structure:

- Exactly one self-contained HTML file; no external runtime or companion asset.
- All required sections and metadata from `ideation-sections.md` are present.
- Every idea has a stable anchor, visible rank, and all required labeled fields.
- The ranked jump list targets valid anchors.
- Every rejected idea has a table row and reason.
- Metadata has one visible representation and the composition footer exists.
- Heading levels are ordered and visually distinct.
- Text contrast, line length, card spacing, tables, and mobile layout are readable.
- Strong text is not globally accent-colored; chips and callouts use no one-edge stripe.
- SVG labels do not collide with arrows or shapes, and diagrams add no unique claims.
- No placeholders, process notes, action menus, or downstream-skill instructions leaked into the document.
