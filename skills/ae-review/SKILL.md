---
name: ae-review
description: Review code or another requested artifact for material problems. Use for code review, document review, browser QA, and Xcode verification; apply fixes when requested.
---

# Review

Inspect the requested target and return material findings affecting correctness, security, behavior, maintainability, or the user's decision.

For code, read the diff and enough surrounding code to understand its effects. Check for bugs, regressions, unsafe assumptions, missing failure handling, and tests that claim more than they prove. Treat style as material when it hides a defect.

Each finding contains:

- severity;
- precise file and line when applicable;
- the concrete consequence;
- the smallest useful correction.

Order findings by severity. A clean review states that plainly.

Apply fixes when the user requests them.

Load at most one matching recipe:

- [`document.md`](recipes/document.md) for requirements, plans, or specifications;
- [`browser.md`](recipes/browser.md) for a real web flow;
- [`xcode.md`](recipes/xcode.md) for an Apple project.
