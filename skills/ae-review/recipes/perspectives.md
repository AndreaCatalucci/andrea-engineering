# Code perspectives

A request for a thorough review matches every row whose trigger is present in the target or requested change.

| Perspective | Trigger |
|---|---|
| correctness | behavior-changing code, a bug fix, or an open-ended code review |
| simplicity | a refactor, new abstraction, duplicated mechanism, or architecture change |
| security | auth, secrets, untrusted input, permissions, cryptography, or a moved trust boundary |
| tests | test files in the target |
| concurrency | shared mutable state, locks, async races, or cancellation |

## correctness

Read the diff and enough surrounding code to understand its effects. Report bugs, regressions, unsafe assumptions, missing failure handling, broken contracts, and changed behavior whose verification cannot detect a named failure.

## simplicity

Read the diff, its immediate callers, and existing code that already does this job. Report dead code, duplication, needless indirection, premature abstraction, special cases that will cost later edits, and a new pattern that an existing one already covers. Cite that existing pattern. When two versions are equally clear, that is not a finding.

## security

Trace untrusted input, privilege, and secret handling across the changed paths and their callees. Report issues that bypass a trust boundary or leak a secret.

## tests

Read each changed test with the behavior it claims to cover. Report tests that pass for the wrong reason, miss the failure they name, or leave a named contract unpinned.

## concurrency

Trace shared state, ordering, and cancellation through the changed paths. Report races, lost wakeups, double-closes, and work on the wrong thread.
