# Proof Web API

Read this reference before using a shared Proof URL or any `proofeditor.ai` agent endpoint.

## Authentication and identity

Extract the document slug and `token` from the shared URL. Send the token as `x-share-token` on agent API requests. Every mutation also sends:

- `Content-Type: application/json`
- `X-Agent-Id: ai:andrea-engineering`
- `by: "ai:andrea-engineering"` in the body
- an `Idempotency-Key` when required by the contract, and preferably on every mutation

Bind the human-readable name with `/presence` before the first mutation when attribution has not yet been established.

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/agent/{slug}/state` | Markdown, marks, revision, live clients, mutation token |
| GET | `/api/agent/{slug}/snapshot` | Block refs plus mutation token for block edits |
| POST | `/api/agent/{slug}/ops` | Comments, suggestions, replies, resolution, rewrite |
| POST | `/api/agent/{slug}/edit/v2` | Direct block/range/find-replace edits |
| POST | `/api/agent/{slug}/presence` | Attribution and status |
| POST | `/api/bridge/report_bug` | Report a persistently inconsistent mutation failure |

`/ops` accepts one top-level `type` or a top-level `operations` array whose entries each contain `type`. `/edit/v2` accepts a top-level `operations` array whose entries each contain `op`. Never mix the two shapes.

The `/state` response contains a heterogeneous `marks` union: comments, suggestions, and provenance/authorship marks can all appear. Workflows that ingest review comments should request `/state?kinds=comment`; never interpret provenance or authorship marks as user feedback.

## Mutation tokens and retries

Every mutation requires `baseToken`. Reuse `mutationBase.token` from the most recent `/state`, `/snapshot`, or successful mutation response.

- `STALE_BASE`, `BASE_TOKEN_REQUIRED`, `MISSING_BASE`, `INVALID_BASE_TOKEN`: re-read state, rebuild with the new token, and retry once with a new idempotency key.
- `ANCHOR_NOT_FOUND`, `ANCHOR_AMBIGUOUS`: tighten or regenerate the anchor before retrying.
- `INVALID_OPERATIONS`, `INVALID_REQUEST`, `INVALID_REF`, `INVALID_BLOCK_MARKDOWN`, `INVALID_RANGE`, `INVALID_MARKDOWN`, or 422: fix the payload; do not retry unchanged.
- `COLLAB_SYNC_FAILED`, `REWRITE_BARRIER_FAILED`, `PROJECTION_STALE`, `INTERNAL_ERROR`, 5xx, network timeout, or a 202 with pending collaboration: the write may have landed. Re-read and verify before retrying.

Reuse an idempotency key only for the exact same serialized request body. A changed `baseToken` makes a new body and requires a new key.

## Edit selection

Use the narrowest primitive that expresses the requested change:

1. literal repeated change: `/edit/v2` `find_replace_in_doc`;
2. known block or section: fresh `/snapshot`, then `replace_block`, `insert_before`, `insert_after`, `delete_block`, `replace_range`, or `find_replace_in_block`;
3. visible track changes: `/ops` `suggestion.add`;
4. whole document: `/ops` `rewrite.apply` only when explicitly requested or genuinely unavoidable and no live clients are present.

Block refs are tied to a snapshot and base token. Re-read `/snapshot` after intervening writes. A single `/edit/v2` operations array is atomic. Validate large batches with `?dryRun=1` or `?validate=1`; use `?return=minimal` when only the next token and applied count are needed.

`rewrite.apply` is blocked while live clients are connected. Direct `/edit/v2` edits, comments, and suggestions remain available during active collaboration.

## Operation shapes

Common `/ops` types:

- `comment.add`: `quote`, `text`
- `comment.reply`: `markId`, `text`, optional `resolve`
- `comment.resolve` / `comment.unresolve`: `markId`
- `suggestion.add`: `kind` (`insert`, `delete`, `replace`), `quote`, `content`, optional `status: "accepted"`
- `suggestion.accept` / `suggestion.reject`: `markId`
- `rewrite.apply`: `content`

Common `/edit/v2` operations:

| `op` | Required fields |
|---|---|
| `replace_block` | `ref`, singular `block: {markdown}` |
| `insert_after`, `insert_before` | `ref`, plural `blocks: [{markdown}]` |
| `delete_block` | `ref` |
| `replace_range` | `fromRef`, `toRef`, `blocks: [{markdown}]` |
| `find_replace_in_block` | `ref`, `find`, `replace`, `occurrence` |
| `find_replace_in_doc` | `find`, `replace`, `occurrence`, optional range/filter |

If a mutation still fails after a fresh read and one justified retry, report the bug with the failing request ID, slug, and raw response rather than looping.
