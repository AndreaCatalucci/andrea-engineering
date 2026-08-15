---
name: ae-debug
description: Find the cause of a bug or failing behavior and fix it when requested. Use for errors, regressions, failing tests, and stuck investigations.
---

# Debug

Find the smallest explanation that accounts for the failure.

1. Read the exact symptom, error, or failing check. Reproduce it when practical.
2. Trace the real execution path and compare failing behavior with expected behavior.
3. Form one concrete hypothesis and test the cheapest discriminating observation. Revise it when evidence disagrees.
4. State the root cause, not merely the line that surfaced it.
5. If the user asked for a fix, make the smallest causal change and run the narrow regression check. If they asked only for diagnosis, do not edit.

Inspect persisted state before logs when the product stores workflow state. Keep secrets and unrelated production data out of output.

Do not expand into general cleanup, review, shipping, or learning capture. Avoid long investigation diaries; report the cause, evidence, fix if any, and remaining uncertainty in at most 200 words by default.
