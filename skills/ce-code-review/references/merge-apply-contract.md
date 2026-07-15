# Merge, Apply, and Output Contract

## Merge

1. Validate every compact reviewer return against `findings-schema.json`. Drop malformed findings and record counts.
2. Discard findings outside the resolved diff unless the diff newly exposes a pre-existing issue. Separate genuine pre-existing findings from the verdict.
3. Discard recommendations to delete or ignore protected planning/learning artifacts.
4. Require `first_evidence` for confidence 75/100. Demote or suppress unsupported claims.
5. Deduplicate by normalized file, nearby line bucket, and normalized title/root cause. Merge evidence, reviewers, and the strongest conservative route.
6. Confidence uses anchors 0/25/50/75/100. Independent corroboration may promote one anchor; the orchestrator fast pass never promotes.
7. Route weak testing-only findings to `testing_gaps` and weak maintainability/advisory findings to `residual_risks` rather than inflating actionable findings.
8. Assign stable `#` values after filtering. Never renumber them later.
9. Build triage groups only when they represent a real shared decision, root cause, or apply order. Groups supplement findings and reference stable numbers.
10. Add plan-completeness findings from the resolved plan contract: explicit omissions P1/actionable; inferred omissions P3/advisory.
11. Preserve agent-native, deployment, Known Pattern, residual-risk, and testing-gap outputs separately.

P0/P1 at confidence 50 may survive for validation rather than being silently lost. P2/P3 require stronger evidence or soft-bucket routing.

## Apply (default local scope only)

Checkpoint whether the tree was clean before review. Apply only findings that are clear, bounded improvements:

- concrete bug fixes;
- test hardening tied to changed behavior;
- dead-code removal or simplification with preserved behavior;
- mechanical standards fixes backed by an explicit rule.

Do not apply design decisions, disputed findings, taste calls, permission/auth/security posture changes, or public contract changes needing authority.

Apply in severity/order groups when useful. Run targeted tests/lint after each coherent batch. Revert a fix that fails. Review only the autofix diff for duplication, widened contracts, missing types/docs/tests, and accidental unrelated edits; verify follow-up edits again.

If the pre-review tree was clean, commit verified fixes as one isolated repo-convention commit, normally `fix(review): <summary>`. If it was dirty, leave fixes uncommitted. Never push.

## Markdown output

Follow `review-output-template.md`. Keep ASCII-safe output, stable numbers, escaped table pipes, and no per-item separators. Include only material sections:

1. scope, intent, and selected lenses;
2. applied fixes and validation (default only);
3. triage groups;
4. findings by severity;
5. requirements completeness when a plan exists;
6. actionable findings;
7. pre-existing findings;
8. Known Patterns, agent-native gaps, deployment notes;
9. Coverage;
10. final verdict and self-contained prioritized actionable recap.

Every finding makes clear what/where, why it matters, required response, and confidence. Match detail to severity; never reprint the diff.

## JSON output (`mode:agent`)

Emit one raw JSON object with no fence or trailing prose, and write the same payload to `review.json`:

```json
{
  "status": "complete",
  "verdict": "Ready to merge | Ready with fixes | Not ready",
  "scope": {
    "base": "<base>",
    "branch": "<branch>",
    "head_sha": "<sha>",
    "pr_url": null,
    "files_changed": 0
  },
  "intent": "<summary>",
  "intent_confidence": "explicit | inferred | uncertain",
  "reviewers": ["core"],
  "findings": [],
  "actionable_findings": [],
  "triage_groups": [],
  "pre_existing_findings": [],
  "requirements_completeness": null,
  "learnings": [],
  "agent_native_gaps": [],
  "deployment_notes": [],
  "residual_risks": [],
  "testing_gaps": [],
  "coverage": {},
  "artifact_path": "/tmp/andrea-engineering/ce-code-review/<run-id>/",
  "run_id": "<run-id>"
}
```

Finding objects carry stable `#`, title, severity, file, line, confidence, routing, verification requirement, pre-existing flag, suggested fix/evidence, and reviewers. `actionable_findings` is the downstream-resolver subset. Groups may reference all findings, but callers apply only their intersection with `actionable_findings`.

Use `status:failed` with a reason for setup failure, `status:skipped` for scope skip, and `status:degraded` when all reviewers fail.

## Run artifacts

Always write under `/tmp/andrea-engineering/ce-code-review/<run-id>/`:

- per-reviewer JSON;
- synthesized and actionable findings;
- advisory outputs;
- `report.md` or `review.json`;
- `metadata.json` with run ID, branch, head SHA at dispatch, verdict, and completion timestamp.

In default mode, finish with a compact Actionable Findings summary containing stable number, severity, `file:line`, title, route, suggested-fix presence, confidence, and artifact path. State `Actionable findings: none.` explicitly when empty.
