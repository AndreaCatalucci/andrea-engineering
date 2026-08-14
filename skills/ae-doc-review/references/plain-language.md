# Plain-Language Writing

Read this reference immediately before writing text that the user will read,
including plans, reports, reviews, explanations, PR descriptions, and chat
summaries. It does not apply to metadata keys, stable IDs, code, commands, or
terms that already belong to the project.

Write for the person solving the problem, not for the workflow producing the
document.

1. Reuse the user's words and the repository's existing names.
2. Name the actual person, behavior, file, component, event, or decision.
3. Prefer common words and short sentences. Explain one idea at a time.
4. Keep internal skill vocabulary internal. Do not copy workflow labels,
   routing terms, review machinery, or prompt terminology into the result.
5. Replace an abstract claim with the concrete fact it stands for. Use an
   example when behavior could otherwise be misunderstood.
6. Define an unavoidable specialist term the first time it appears.
7. Delete background that does not change the decision or the work.
8. Do not make routine work sound strategic, architectural, or academic.
9. Describe observable changes with active verbs. Say “the task file changes,”
   not “effects occur” or “the write skip becomes visible.”

Prefer these forms in user-facing prose:

| Avoid | Prefer |
| --- | --- |
| load-bearing decision | important decision, followed by the decision itself |
| decision surface | questions we need to answer |
| grounding | repository evidence, research, or known facts |
| leverage point | useful place to improve, followed by the place |
| signal | measure, event, evidence, or warning, whichever is meant |
| lens | check, concern, or point of view |
| framing | description, interpretation, or scope |
| trajectory | direction or expected change |
| surface | page, API, component, workflow, or affected area |
| artifact | document, file, report, plan, or result |
| contract | requirements or rules, unless it is a stable schema name |
| implementation discovery | a detail to verify while coding, followed by the detail |
| effects occur | say exactly what changes |

Before saving, check:

- Could someone unfamiliar with this skill understand every sentence?
- Does each paragraph refer to this specific problem?
- Could a sentence be pasted unchanged into an unrelated document? If so,
  rewrite it with concrete details or delete it.
- Did any internal term leak into a heading or explanation? Replace it with
  words the user already knows.
