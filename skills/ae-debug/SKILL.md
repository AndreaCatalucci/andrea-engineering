---
name: ae-debug
description: Find the cause of failing behavior and fix it when requested. Use for errors, regressions, failing tests, and stuck investigations.
---

# Debug

Find the smallest explanation that accounts for the failure.

1. Read the exact symptom, error, or failing check. Reproduce it when practical.
2. Trace the real execution path and compare failing behavior with expected behavior.
3. Form one concrete hypothesis and test the cheapest discriminating observation. Revise it when evidence disagrees. A trajectory change is a lesson.
4. State the root cause and causal chain.
5. A fix request leads to the smallest causal change and a narrow regression check. A diagnosis request ends with the findings.

Inspect stored state before logs when the product persists it. Redact secrets and unrelated production data.

Report the cause, evidence, fix if any, and remaining uncertainty.
