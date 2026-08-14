# Divergent Ideation

Read this only at Phase 2. Generation must finish before critique begins.

## Dispatch the smallest complete fleet

Read `dispatch-contract.json`; it is authoritative for agent assignments,
candidate quotas, and evidence-read budgets. Use these rules when applying it:

- Issue themes replace named frames and use the contract's round-robin rule. If
  issue evidence is insufficient, select the default-software entry.
- Non-software depth selects the matching entry described in
  `universal-ideation.md`.
- Recovery runs only after the area check and treats each empty area as a
  separate assignment.

Volume overrides change the explicit bucket bounds before dispatch. They do not
erase a bucket or let a paired agent combine its quotas.

Dispatch the initial fleet concurrently. If local capacity is smaller than the
selected fleet, use a bounded queue and start the next assignment as soon as a
slot opens. Recovery starts only after the whole initial fleet is accepted.

## Build a fresh-context packet

Spawn each agent with no inherited turns and supply:

1. `grounding`: the byte-identical summary and dossier paths;
2. `constraints`: the user prompt, focus, and named directive files;
3. `background`: codebase, learnings, external evidence, and research gists;
4. `areas`: the declared area list, or an empty list;
5. `assignment`: the exact candidate-file object: kind, stable assignment ID,
   declared areas, and buckets with ID, minimum, and maximum;
6. `bucket_instructions`: keyed by bucket ID, with the evidence-read allowance
   and full frame instruction; a theme also includes its complete theme summary
   and evidence, while recovery names the missing area;
7. `paths`: absolute `skill_dir`, `helper_path`, `generator_protocol_path`,
   scratch directory, draft path, authoritative result path, and expected-
   assignment manifest path;
8. the fixed protocol loaded from `generator_protocol_path`.

Before dispatch, the parent writes the expected-assignment manifest. It contains
the exact `assignment` object and its allocated `result_path`; agents must not
reconstruct either value. Copy the selected frame definitions below into the
matching `bucket_instructions` so a fresh agent never needs conversation
history or another instruction file to understand its assignment.

The fixed protocol stays unchanged across agents. Put long shared material
before assignment-specific content. Dossier gists orient the agent; the dossier
itself is evidence and must be read before citation.

## Frames

Frames are starting points, not walls:

1. **Pain and friction** — recurring user, operator, or topic pain.
2. **Inversion, removal, automation** — reverse, delete, or automate a step.
3. **Assumption-breaking** — expose a fixed-looking choice and reframe it.
4. **Leverage and compounding** — make future work cheaper or stronger.
5. **Cross-domain analogy** — transfer a structurally similar pattern from a
   non-obvious field.
6. **Constraint-flipping** — invert or exaggerate the obvious constraint and
   turn the useful result into a realistic direction.

For surprise-me, tell each agent to find the subject most interesting from its
frame. Different frames finding different subjects is intentional.

## Candidate file

Each agent writes one JSON document. The shape below is abbreviated; the real
file must include enough candidates to satisfy every declared minimum.

```json
{
  "schema_version": 1,
  "assignment": {
    "kind": "frame",
    "assignment_id": "default-01",
    "areas": ["delivery"],
    "buckets": [
      {"id": "pain-and-friction", "minimum": 6, "maximum": 8},
      {"id": "constraint-flipping", "minimum": 6, "maximum": 8}
    ]
  },
  "candidates": [
    {
      "assignment": "pain-and-friction",
      "title": "Concrete title",
      "move": "One concrete direction.",
      "area": "delivery",
      "basis": "direct: path/file.py:42 shows the repeated wait",
      "significance": "Why the evidence makes the move matter."
    }
  ]
}
```

Use assignment kind `theme` for issue themes, `recovery` for missing areas, and
`universal` for non-software frames. Omit `area` only when the assignment's
`areas` array is empty. The helper rejects unknown fields, invalid basis tags,
undeclared areas, and incomplete bucket quotas.

The agent seals the file with the packet's absolute `helper_path`, passing
`--expected` with the expected-assignment manifest, and returns only its
receipt. The parent saves that receipt as JSON and runs `accept-candidates`
with the same `--expected` manifest. The helper binds the receipt to the exact
assignment and allocated result path, then returns the only projected
candidates used by merge.

Allow one repair for an invalid file or receipt. On a write failure, the agent
may return one complete inline candidate document. The parent writes it to a
draft, seals it through the same command, and accepts it only if validation
passes. A second failure leaves the assignment missing and must be reported as
degraded coverage.

## Merge without losing provenance

Merge only the projections returned by `accept-candidates`; do not run
`project-candidates` afterward. Each projection already has its stable source
key, deterministic `candidate_id`, and `parents` list.

Merge projections, then deduplicate semantically. A retained original keeps its
single parent. A deduplicated candidate lists every merged parent and uses
origin `deduped`. A cross-cutting or root-created combination lists all input
parents and uses origin `synthesis`. Recovery projections use origin
`recovery`. For a changed or new candidate, omit `candidate_id` from the draft;
`seal-consolidated` computes all missing IDs from title, move, and parents in
one pass. A supplied but stale ID fails validation. Never discard lineage.

In specified mode, add at most 3-5 genuinely stronger combinations. In
surprise-me mode, allow 5-8 because different frames may discover complementary
subjects. Do not pad these counts.

Check declared areas after dedupe. If an area has no candidates, dispatch the
recovery entry from the contract. Give each missing area its own bucket and
apply its declared quota and evidence reads independently. Record any area
beyond the contract's recovery cap rather than spawning more agents.

Collect every accepted projection's source key into `source-registry.json` with
exactly `schema_version`, `areas`, and `source_keys`. Seal the resulting
`consolidated-candidates.json` with `seal-consolidated --sources
<source-registry>`. The helper fills missing candidate IDs and rejects supplied
stale IDs, unknown sources, undeclared areas, or incomplete lineage. Also write
a best-effort `raw-candidates.md` checkpoint grouped by candidate ID and
assignment. If that
human-readable checkpoint fails, warn and continue; the checked JSON remains
authoritative.

Pass the consolidated receipt, not repeated candidates, into Phase 3.
