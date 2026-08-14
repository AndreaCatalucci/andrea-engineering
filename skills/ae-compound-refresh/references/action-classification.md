# Maintenance Action Classification

Read this reference after investigation and before asking for decisions. Assign exactly one action to every candidate and attach the evidence that satisfies its criterion.

## Keep

The guidance remains accurate, useful, and supported by current code. Do not edit merely to record that it was reviewed; report the unchanged result.

## Update

The core solution remains correct, but paths, names, links, snippets, examples, or metadata drifted. The correction is local and does not change the recommended approach.

Do not use Update for style-only cleanup or when the old fix has become misleading; those are no-op churn or Replace.

## Consolidate

Two or more materially correct documents solve the same searchable problem with compatible guidance, and one canonical document can absorb the others' unique content without becoming unwieldy.

Keep documents separate when they cover independently searchable sub-problems. If a subsumed document has no unique content, Delete is sufficient; otherwise merge before deleting.

## Replace

The problem domain still exists, but the old document's root cause, architecture, troubleshooting path, or recommended solution is materially misleading.

- With sufficient evidence of both the old and current approaches, write a successor through the Replace flow.
- Without sufficient evidence, mark the document stale in place and state what is missing. Do not fabricate a successor.

## Delete

Delete only when all three conditions hold:

1. the implementation is gone, clearly superseded, or the document is wholly redundant;
2. the underlying problem domain is gone or already fully represented elsewhere;
3. inbound links are absent or unambiguously decorative.

If the problem persists under a new implementation, choose Replace. If a substantive citation depends on the document, choose Replace or Keep with narrower scope. In headless mode, ambiguity becomes stale-marking rather than deletion.

## Inbound-link test

Before Delete, search repository Markdown for the filename slug and read the citing context.

- **Decorative:** the principle is stated inline and the citation is optional; cleanup is mechanical.
- **Substantive:** the citing document delegates missing content to this document; preserve that contract through Replace or narrowed Keep.
- **Mixed or unclear:** stale-mark and surface the uncertainty.

## Pattern documents

Apply the same actions to pattern documents, but judge their generalized rule against the current supporting learning set:

- Keep when the rule and examples remain representative.
- Update when the rule holds but examples, links, or scope drifted.
- Consolidate when multiple patterns generalize the same concern.
- Replace when the supporting learnings now imply a different rule.
- Delete when the rule is no longer valid, recurring, or independently useful.

Classification is complete only when every candidate has one action, current evidence, inbound-link evidence when deletion is possible, and an explicit confidence or open question.
