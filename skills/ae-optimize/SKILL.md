---
name: ae-optimize
description: "Run metric-driven optimization loops. Use when improving measurable outcomes such as search relevance, clustering quality, build performance, prompt quality, or scored behavior through experiments."
---

# Iterative Optimization

Run repeatable experiments against one trusted measurement contract. Keep the best verified result, not the most persuasive hypothesis.

Before asking the user for input, read [`references/codex-interaction.md`](references/codex-interaction.md).

## Input and defaults

Accept either:

- a prose optimization goal; or
- a YAML spec path.

If neither is present, ask for one. For prose goals, read [`references/spec-authoring.md`](references/spec-authoring.md), create a spec, and validate it against [`references/optimize-spec-schema.yaml`](references/optimize-spec-schema.yaml). For a friendly overview and examples, read [`references/usage-guide.md`](references/usage-guide.md) only when the user needs orientation.

Use a hard metric when “better” is an objective scalar. Use judge mode when a scalar proxy can improve while actual quality degrades. Start conservatively:

- `execution.mode: serial`
- `execution.max_concurrent: 1`
- `stopping.max_iterations: 4`
- `stopping.max_hours: 1`
- judge sample size `10`, batch size `5`, cost cap `$5`

Do not add dependencies until the baseline and measurement contract are trustworthy.

## Durable state

Store run state under:

```text
.context/andrea-engineering/ae-optimize/<spec-name>/
```

Keep at least:

- `spec.yaml` — approved measurement and execution contract
- `experiment-log.yaml` — append-only experiment history following [`references/experiment-log-schema.yaml`](references/experiment-log-schema.yaml)
- `strategy-digest.md` — current synthesis and next hypotheses

The disk state is authoritative. After every measurement:

1. append the measured experiment to `experiment-log.yaml` with outcome `measured`;
2. read the log back and confirm the entry;
3. only then evaluate it and update the outcome.

Re-read the spec, log, and strategy digest at every phase boundary. On resume, continue from the last complete log entry. Never present a result that exists only in conversation context.

## Phase 0: Set up

1. Resolve `SKILL_DIR` to this skill's absolute directory. Codex shell calls do not share shell variables, so set it in each command that runs a bundled script.
2. Load and validate the supplied spec, or author one from prose.
3. If `docs/solutions/` exists, search it with `rg` for prior attempts, constraints, and failure modes. Read only plausible matches.
4. Inspect the current branch and working tree. Preserve unrelated user changes. If experiments would overlap dirty files, ask before proceeding.
5. Create the run directory and save the validated spec.
6. Create or reuse a dedicated optimization branch. Do not run experiments directly on the default branch.

For a newly authored spec, show the measurement target, mutable scope, immutable scope, stopping limits, and expected cost. Get approval before running the baseline.

## Phase 1: Establish the baseline

### Validate the measurement contract

The measurement command must be deterministic enough to compare variants and must not mutate the implementation under test. Confirm:

- the command and working directory exist;
- required fixtures and inputs are available;
- mutable and immutable paths do not overlap;
- degenerate gates reject broken output;
- exclusive resources are declared;
- judge mode has a bounded rubric and cost limit.

Run the measurement command once through:

```bash
SKILL_DIR="<absolute path to this skill>";
bash "$SKILL_DIR/scripts/measure.sh" \
  "<measurement.command>" \
  "<measurement.timeout_seconds>" \
  "<repo-root>/<measurement.working_directory>"
```

If the measurement fails, stop and repair the contract before generating hypotheses. Do not optimize against a broken harness.

### Measure stability

Run the baseline according to the spec's stability mode. When repeat mode is configured, use the declared repeat count and aggregate exactly the same way for every experiment. Record variance and reject a baseline whose noise is too large to distinguish meaningful improvement.

Write and verify the baseline in the log. In judge mode, inspect the first sample for rubric clarity, obvious judge inconsistency, and degenerate outputs before approving further spend.

### Probe safe parallelism

Use serial execution unless the spec explicitly allows concurrency. When it does, run:

```bash
SKILL_DIR="<absolute path to this skill>";
bash "$SKILL_DIR/scripts/parallel-probe.sh" \
  "<repo-root>" \
  "<measurement.command>" \
  "<measurement.working_directory>" \
  <shared-file>...
```

Parallelism is allowed only when the probe confirms isolated worktrees, inputs, outputs, ports, databases, and other exclusive resources. Otherwise set concurrency to `1` and continue.

## Phase 2: Build the hypothesis backlog

Inspect the current implementation, baseline diagnostics, prior learnings, and any user constraints. Generate hypotheses that name:

- the proposed change;
- why it should move the target metric;
- mutable files;
- expected risk and failure mode;
- required dependency or resource changes;
- the smallest experiment that can falsify it.

Prefer distinct mechanisms over parameter variants of the same idea. Rank by expected information gain, not confidence alone.

Before dispatch, group any new dependencies or external-cost changes and ask for one approval. Rejected dependencies remove only the affected hypotheses.

Write the ranked backlog and current reasoning to `strategy-digest.md` before starting experiments.

## Phase 3: Run experiments

Select a batch within the approved concurrency and resource budget. Give each experiment one hypothesis and an isolated worktree created with:

```bash
SKILL_DIR="<absolute path to this skill>";
bash "$SKILL_DIR/scripts/experiment-worktree.sh" \
  create <spec-name> <experiment-index> <base-ref> <shared-file>...
```

Dispatch independent implementations with `spawn_agent`, using Codex's inherited model and [`references/experiment-prompt-template.md`](references/experiment-prompt-template.md). Each worker owns only its worktree and mutable scope. It must not edit the measurement harness, evaluate itself, commit, or merge.

For each completed implementation:

1. verify its diff stays inside mutable scope;
2. run the same measurement contract used for baseline;
3. in repeat mode, use the same repeat count and aggregation;
4. in judge mode, apply degenerate gates first, then the rubric from [`references/judge-prompt-template.md`](references/judge-prompt-template.md);
5. write and verify the result immediately;
6. update the outcome using the values defined by the experiment-log schema.

Never rank an invalid or gate-failing experiment. Compare valid candidates against the current best, including variance, guardrails, judge cost, and implementation complexity.

After each batch:

- update the log's best result only when the improvement clears the spec's gates;
- rewrite `strategy-digest.md` with what worked, what failed, and which assumptions changed;
- generate the next hypotheses from disk state, not memory;
- remove completed experiment worktrees after their result and diff are safely recorded.

Continue until a configured stop is reached: iteration limit, time limit, cost cap, target achieved, no credible hypotheses, repeated inconclusive results, or user stop.

## Phase 4: Preserve the winner

Reproduce the best result once from a clean worktree. A winner that cannot be reproduced is inconclusive.

When reproducible:

1. apply only the winning change to the optimization branch;
2. run the full project checks relevant to the change;
3. run the measurement contract once more on that branch;
4. record the final verification in the log;
5. leave rejected experiment diffs out of the branch.

Report:

- baseline and final result;
- absolute and relative improvement;
- stability or judge confidence;
- winning mechanism and changed files;
- rejected hypotheses and what they taught;
- remaining risks and deferred hypotheses;
- run-state path for audit or resume.

Offer a next step only after the verified result is durable: another bounded round, handoff to `ae-work`, or shipping through the user's normal workflow. Do not commit, push, or open a PR unless the user or invoking workflow authorized it.
