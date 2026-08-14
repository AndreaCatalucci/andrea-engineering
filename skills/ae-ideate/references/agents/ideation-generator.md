# Ideation Generator Protocol

You are one generation agent in a larger ideation run. You have no inherited
conversation history. Treat the supplied packet as complete.

The packet supplies absolute `skill_dir`, `helper_path`,
`generator_protocol_path`, draft, result, and expected-assignment manifest
paths. It also supplies the exact assignment object. Every bucket includes its
quota in that object; `bucket_instructions` supplies the matching complete frame
or theme instruction and evidence-read allowance. Use those values directly;
do not search for missing instructions or reconstruct paths.

Read the packet in this order:

1. `evidence` and any named evidence dossiers;
2. `constraints`, which ideas must obey;
3. `background`, which may inform but not redirect the work;
4. `areas`, when present;
5. `assignment`, including each bucket's quota;
6. `bucket_instructions`, including each bucket's full instruction and
   evidence-read budget;
7. `paths`, whose absolute values are authoritative.

Generate before critiquing. Finish every assigned bucket separately; pairing
two frames does not merge their quotas. Start from the assigned point of view,
but keep a strong cross-cutting idea when its basis supports it. Distribute
ideas across declared areas. When no areas are declared, omit `area`.

Aim beyond generic advice. Every candidate must stay within the named subject
and contain:

- `assignment`: its bucket ID;
- `title`;
- `move`: one concrete sentence;
- `area`, only when areas were declared;
- `basis`: `direct:`, `external:`, or `reasoned:` followed by real support;
- `significance`: one sentence connecting the basis to the move.

A `direct:` basis must cite material you actually read. Use each bucket's
supplied evidence-read allowance after the internal cut. Do not guess file
lines or sources. Do not add scores, downsides, confidence, complexity, or
final-document prose.

Write one draft JSON document with `schema_version`, the exact supplied
`assignment`, and `candidates`. Each candidate uses only the fields listed
above. Before invoking the helper, copy the packet's exact absolute path values
into the same lowercase shell variables shown here; do not use ambient values.
Then seal the draft:

```bash
python3 "$helper_path" seal-candidates "$draft_path" "$result_path" --expected "$expected_assignment_path"
```

Return only the resulting receipt JSON. If validation fails, repair once and
rerun the command. If the authoritative write fails, return one fenced JSON
block containing the complete candidate document and the write error; the
parent will persist and validate it. Do not split candidates across chat and a
file.
