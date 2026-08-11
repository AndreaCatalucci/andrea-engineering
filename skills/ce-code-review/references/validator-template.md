# Batched Validator Protocol

The parent writes `/tmp/andrea-engineering/ce-code-review/<run-id>/validator-packet.json`
and dispatches one independent validator with `fork_turns="none"`. The launch
prompt supplies only this protocol's absolute path and the packet path.

The packet contains the run ID, hydrated full findings path, staged diff and
file-list paths, scope mode and fetched refs, intent, requirements, PR context,
project orientation, applicable governing instructions, and up to three Known
Pattern notes. It is complete; do not use inherited conversation history.

For every supplied finding independently decide:

1. Is the issue real in the code as written?
2. Was it introduced or newly exposed by this diff?
3. Is it already prevented by callers, guards, middleware, framework behavior,
   types, tests, or parallel handling?

Read the cited code and relevant surrounding paths yourself. Findings are
candidates, not evidence of one another. In remote scope, inspect the supplied
remote head with `git show` or the staged hunks; never inspect a stale workspace
copy. Do not invent findings or edit files.

Return only:

```json
{
  "verdicts": [
    {
      "finding_number": 1,
      "validated": true,
      "reason": "One sentence grounded in independently inspected evidence."
    }
  ]
}
```

Return exactly one verdict for every finding number. Reject when evidence is
insufficient or a cited file cannot be inspected. Each input finding includes
its stable number, title, severity, file, line, confidence, source reviewers,
full `why_it_matters`, evidence, and suggested fix when present.
