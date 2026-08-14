# Optimization Spec Authoring

Read this reference only when the optimization input is a prose goal rather than an existing YAML spec.

## 1. Choose the metric type

Analyze the project to identify what can be measured.

- Use `type: hard` when the target is an objective scalar with a clear better direction, such as build time, latency, coverage, memory, or pass rate.
- Use `type: judge` when quality requires semantic judgment, proxy metrics can mislead, or a degenerate result could score well numerically, such as search relevance, clustering, summarization, readability, recommendations, or UX copy.

For qualitative targets, recommend `judge` and explain its three layers:

1. cheap degenerate gates reject obviously broken output;
2. the judge rubric scores the actual quality target;
3. diagnostics explain score movement without becoming targets.

If the user chooses a hard proxy for a qualitative target, record the risk and continue.

## 2. Design judge sampling

Define what one evaluated item is, the natural quality or size strata, likely failure regions, and a sample size that balances signal with cost. Stratify by domain-relevant boundaries—for example top/middle/tail search results, short/long/multi-topic documents, or large/mid/small clusters. When coverage matters, sample omitted or singleton items to detect false negatives.

Use a small first-run sample (`sample_size: 10`, `batch_size: 5`) until the harness and rubric are trusted. Expand only when the first measurements show stable signal.

## 3. Write the rubric

A judge rubric must:

- use a bounded scale with concrete descriptions for every level;
- name observable quality, not proxy size or volume;
- be specific enough that independent judges should converge;
- request only diagnostic fields that help explain failures.

Example shape:

```yaml
rubric: |
  Rate this result from 1-5.
  5: Fully satisfies the named quality contract with no material defect.
  4: Strong result with a minor defect.
  3: Mixed result with a material but bounded defect.
  2: Weak result that satisfies only part of the contract.
  1: Broken, irrelevant, or degenerate result.
  Also report the specific defect and any diagnostic counts required by the domain.
```

## 4. Complete and approve the spec

Resolve:

- degenerate rejection gates;
- the measurement command and working directory;
- mutable and immutable paths;
- constraints, dependencies, and exclusive resources;
- stopping limits and cost budget.

For the first run, recommend serial execution, `max_concurrent: 1`, `max_iterations: 4`, and `max_hours: 1`. For judge mode, recommend `max_total_cost_usd: 5` until measurement is trusted.

Write the result to `.context/andrea-engineering/ae-optimize/<spec-name>/spec.yaml`, validate every rule in `optimize-spec-schema.yaml`, present it for approval, and stop at the approval gate. This branch is complete only when the saved spec validates and the user has approved it.
