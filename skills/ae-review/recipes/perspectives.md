# Code perspectives

A request for a thorough review matches every row whose trigger is present in the target or requested change.

| Perspective | Trigger |
|---|---|
| correctness | behavior-changing code, a bug fix, or an open-ended code review |
| simplicity | a refactor, new abstraction, duplicated mechanism, or architecture change |
| security | auth, secrets, untrusted input, permissions or consent, sensitive data, cryptography, or a moved trust boundary |
| tests | changed test files, or a changed contract whose coverage is in question |
| concurrency | shared mutable state, locks, async races, or cancellation |

## correctness

Read the diff and enough surrounding code to understand its effects. Report bugs, regressions, unsafe assumptions, missing failure handling, broken contracts, and regression gaps tied to a named faulty implementation.

## simplicity

Read the diff, its immediate callers, and existing code that already does this job. Report dead code, duplication, needless indirection, premature abstraction, special cases that will cost later edits, and a new pattern that an existing one already covers. Cite that existing pattern. When two versions are equally clear, that is not a finding.

## security

Trace untrusted input, privilege, and sensitive data across the changed paths and their callees, through processing, storage, sync, and deletion. Report trust-boundary bypasses, leaked secrets, and processing or retention without the required permission or consent. Name the violated contract and the conditions that reach it.

## tests

Read the coverage for each changed contract, including unchanged tests. Name a plausible faulty implementation and check whether the tests would reject it. Report tests that pass for the wrong reason, miss the failure they name, or accept that faulty implementation, with the smallest test that would reject it.

## concurrency

Trace shared state, ordering, and cancellation through the changed paths. Report races, lost wakeups, double-closes, and work on the wrong thread.
