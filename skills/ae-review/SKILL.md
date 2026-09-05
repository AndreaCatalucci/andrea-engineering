---
name: ae-review
description: Review code or another requested artifact for material problems. Use for code review, document review, browser QA, and Xcode verification; apply fixes when requested.
---

# Review

Dispatch independent perspectives. They start with no inherited conversation, so they are not anchored on the author's rationale.

1. Resolve the target, intended change, and concrete review question. Reuse current review evidence for unchanged scope; review changes and unresolved risks. For a diff-only request with an empty diff, report no changes and stop; that does not establish product correctness.
2. Load at most one matching recipe:

- [`document.md`](recipes/document.md) for an Opportunity Brief, Concept Notebook, Implementation Plan, Delivery Map, or other specification;
- [`browser.md`](recipes/browser.md) for a real web flow;
- [`xcode.md`](recipes/xcode.md) for an Apple project;
- [`perspectives.md`](recipes/perspectives.md) for code, including the current diff.

The loaded recipe is the charge. `perspectives.md` may name several; every other recipe names one.

3. Select the smallest set of perspectives that answers the review question. On `perspectives.md`, use one perspective when it covers the question; add another only for a separate material risk. For an open-ended code review, use correctness plus any materially distinct perspective triggered by the target. A request for a thorough review takes every materially matching row. Name the trigger for each selection. On any other recipe, take its charge as the one perspective.
4. Spawn each selected perspective as a subagent. Dispatch them together. Each packet contains the intended change, the target paths, that perspective's charge, and the finding format below. Dispatch is done when every selected perspective has been spawned with those four fields. Inspecting the target in this conversation is the fallback only when the host cannot spawn a subagent.
5. Wait until every perspective has returned a finding list or a clean pass. A failed spawn or missing return is a failed perspective. Confirm each kept finding at the cited location. Keep findings that name a consequence and a correction. Collapse duplicates. Style survives only when it hides a defect.
6. Report findings ordered by severity, which perspectives ran, and any that failed. A clean review states that plainly. Apply fixes when the user requests them. Wording fixes run the `unslop` skill.

Each finding contains:

- severity;
- precise location (file and line, passage, or page) when applicable;
- the concrete consequence;
- the smallest useful correction.

Each perspective reports findings and leaves the tree unchanged.
