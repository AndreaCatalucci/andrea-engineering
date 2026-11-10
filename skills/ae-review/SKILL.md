---
name: ae-review
description: Review code or another requested artifact for material problems. Use for code review, document review, browser QA, and Xcode verification; apply fixes when requested.
---

# Review

1. Resolve the target, its baseline or revision, the intended behavior, the review question, and any constraints such as read-only or no test runs. Reuse current evidence for unchanged scope. For a diff-only request with an empty diff, report no changes and stop; that does not establish product correctness.
2. Load the one recipe that matches the primary target:

- [`perspectives.md`](recipes/perspectives.md) for code, including the current diff;
- [`document.md`](recipes/document.md) for an Opportunity Brief, Concept Notebook, Implementation Plan, Delivery Map, skill, or other prose;
- [`browser.md`](recipes/browser.md) for a real web flow;
- [`xcode.md`](recipes/xcode.md) for an Apple build, launch, or test.

Load another recipe only when the request actually crosses that boundary.

3. For code, select the smallest set of perspectives that answers the review question, using the rules in `perspectives.md`, and name the trigger for each. Other recipes are one perspective each.
4. Inspect directly unless independent review is requested or a separate reviewer would materially improve confidence. A delegated packet contains the target and baseline, intended behavior, question, perspective, constraints, evidence already gathered, and the report format below, with no inherited conversation. When a delegate fails or does not return, inspect that perspective directly and report that its independence was lost.
5. Admit a finding only after tracing it from a triggering condition to a concrete consequence and checking callers, contracts, and existing coverage for counterevidence. For a diff, show that the change introduces or worsens the problem. Unverified concerns go under open questions. Merge findings that share a root cause. Style survives only when it hides a defect.
6. Report in the format below. Review leaves the tree unchanged. When fixes are requested, apply them after the report through `ae-work`, then re-review the affected behavior. Posting to a PR and handling PR feedback belong to `ae-ship`. Wording fixes run the `unslop` skill.

## Report

Use the requested format; otherwise GitHub Markdown, findings first, ordered by severity. Each finding has:

- a heading `[P0–P3] <actionable title>`;
- the location: `path:line`, quoted passage, or page;
- the triggering condition, expected and actual behavior, and the evidence;
- the smallest useful correction; for a coverage gap, the faulty implementation existing tests would accept and the smallest test that would reject it.

Severity follows the demonstrated consequence, not the perspective: P0 blocks release now, P1 is a high-impact failure to fix promptly, P2 is another material defect or regression gap, P3 is a low-impact actionable defect.

End with a verdict: **Changes needed** when material findings remain; otherwise **Incomplete** when required scope went unreviewed; otherwise **No material findings**, which does not claim overall correctness. Then a short coverage note: perspectives covered, direct or independent, what was inspected versus executed, and what was not verified.
