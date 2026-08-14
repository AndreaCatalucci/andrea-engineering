# Reviewer Rules

Return only this JSON shape:

```json
{
  "reviewer": "challenge|feasibility|security|design",
  "findings": [
    {
      "title": "Short problem statement",
      "severity": "P0|P1|P2",
      "section": "Document section or identifier",
      "evidence": ["Direct quote from the document"],
      "consequence": "Observable reader, implementation, product, or security outcome",
      "disposition": "mechanical|decision|fyi",
      "recommendation": "One committed action"
    }
  ],
  "residual_risks": []
}
```

## Finding bar

- Quote the document directly. Search the whole document before claiming an omission.
- State what breaks, gets misread, blocks progress, or causes rework.
- Use P0 for a blocking or unsafe plan, P1 for a material correctness or direction problem, and P2 for a worthwhile non-blocking improvement.
- Use `mechanical` only when the document proves one exact local edit. Use `decision` when author intent or tradeoffs matter. Use `fyi` when nothing breaks but the observation is useful.
- Give one recommendation, not a menu. For `fyi`, the recommendation may be an empty string.
- Suppress style preferences, speculative future concerns, theoretical scale or performance concerns without a stated target, pre-existing problems unrelated to the document, and content explicitly deferred.
- Ignore `## Deferred / Open Questions`; it is prior review output.
- Do not edit files or invoke other skills. Return an empty `findings` array when no issue clears the bar.
