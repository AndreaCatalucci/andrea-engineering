# Lean Reviewer Protocol

This is the fixed protocol for every reviewer. The parent writes one complete
JSON packet per reviewer and dispatches with `fork_turns="none"`. The launch
prompt contains only the absolute `protocol_path` and packet path and asks the
reviewer to follow them and return one receipt or documented inline fallback.

## Packet

The packet contains:

```json
{
  "schema_version": 1,
  "protocol_path": "/absolute/.../subagent-template.md",
  "persona_path": "/absolute/.../personas/core-reviewer.md",
  "scope_rules_path": "/absolute/.../diff-scope.md",
  "schema_path": "/absolute/.../findings-schema.json",
  "helper_path": "/absolute/.../review-result.py",
  "run_id": "...",
  "reviewer": "core",
  "intent": "...",
  "requirements": [],
  "pr_context": {},
  "project_orientation": {},
  "governing_instructions": [],
  "known_patterns": [],
  "scope": {},
  "files_path": "/absolute/.../files.txt",
  "diff_path": "/absolute/.../diff.patch",
  "draft_path": "/absolute/.../core-draft.json",
  "result_path": "/absolute/.../core.json"
}
```

Every path is parent-allocated and absolute. `known_patterns` contains at most
three selected notes. `governing_instructions` contains the applicable project
rules themselves, not only their filenames. The packet is authoritative; do
not reconstruct paths or seek missing conversation history.

## Review

Read the packet, then its persona, scope rules, changed-file list, and diff.
Inspect surrounding code, callers, guards, middleware, types, tests, and
parallel handlers as needed. In remote scope, inspect only the supplied fetched
refs or hunks. The project profile and Known Patterns orient the search but are
not evidence.

Compare the change with `intent`, `requirements`, and `pr_context`. Report an
intent mismatch when the code adds undescribed behavior or omits promised
behavior. Apply the persona's concerns without lowering this protocol's
evidence bar. Persona output examples are illustrative; this protocol's JSON
file and receipt handoff always win when a persona describes another format.

Emit a finding only after you can name a concrete failure or useful advisory:

- `why_it_matters` leads with observable user, caller, operator, security, or
  runtime behavior in 2-4 sentences and explains why the proposed fix works;
- `evidence` has at least one code-grounded string;
- confidence 75 or 100 requires the first evidence item to quote the motivating
  line with exact `file:line`; inspect both sides when the claim involves two
  paths;
- `suggested_fix` gives the smallest defensible code change and names any
  assumption; omit it only when no code-level action exists;
- `requires_verification` is true when the fix needs a targeted test, focused
  re-review, or operational check.

Use the schema's exact fields and enums. Confidence means:

- 0/25: unverified or false positive; do not emit;
- 50: verified but narrow, minor, or advisory;
- 75: double-checked normal-path consequence;
- 100: mechanically proven by code or a directly quoted project rule.

Severity is independent: P0 critical loss/exploit/breakage, P1 high-impact
normal-path defect, P2 meaningful moderate issue, P3 narrow low-impact issue.
Use `gated_auto` for a bounded proposed fix, `manual` for a real design or
cross-cutting decision, and `advisory` when nothing breaks. Default actionable
ownership to `downstream-resolver`; use `human` or `release` only when that
ownership is real.

Suppress:

- formatter/linter output and uncodified style preferences;
- intentional code, explicit lint suppressions, or behavior already protected
  by callers, guards, middleware, types, framework defaults, or parallel paths;
- restatements of existing behavior and generic "consider adding" advice;
- speculative future concerns without a reachable current failure;
- unchanged unrelated issues from the primary verdict. Mark `pre_existing`
  true only when retaining one for the separate pre-existing section.

The false-positive rules take precedence over advisory routing. A leaf reviewer
does not invoke other skills or agents and does not edit the checkout.

## Result handoff

Write one draft JSON object with exactly `reviewer`, `findings`,
`residual_risks`, and `testing_gaps`. Each finding contains `title`, `severity`,
`file`, `line`, `why_it_matters`, `autofix_class`, `owner`,
`requires_verification`, `confidence`, `evidence`, `pre_existing`, and optional
`suggested_fix`. Empty findings are valid.

Copy the packet's exact lowercase path values, then seal the authoritative file:

```bash
python3 "$helper_path" seal-review "$draft_path" "$result_path" --reviewer "$reviewer" --schema "$schema_path"
```

Return only the receipt JSON printed by the helper. Do not repeat findings in
chat. The parent independently accepts that receipt and derives compact merge
fields from the checked file.

If the write or reviewer-side validation fails, repair once. If it still fails,
return the prior compact inline shape with top-level `reviewer`, `findings`,
`residual_risks`, `testing_gaps`, and `handoff_error`. Each compact finding has
`title`, `severity`, `file`, `line`, `confidence`, `autofix_class`, `owner`,
`requires_verification`, `pre_existing`, optional `suggested_fix`, and
`first_evidence` for confidence 75/100. This is a degraded fallback, not a
second normal output.
