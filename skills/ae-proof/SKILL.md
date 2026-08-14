---
name: ae-proof
description: Publish, read, comment on, or edit markdown in Proof. Use for Proof links, sharing specs/plans/drafts, or publish handoffs from planning workflows; avoid proofread, math, evidence, or proof-of-concept meanings.
---

# Proof - Collaborative Markdown Editor

Proof is a collaborative document editor for humans and agents. It supports two modes:

1. **Web API** - Create and edit shared documents via HTTP (no install needed)
2. **Local Bridge** - Drive the macOS Proof app via localhost:9847

## Identity and Attribution

Every write to a Proof doc must be attributed. Two fields carry the agent's identity:

- **Machine ID (`by` on every op, `X-Agent-Id` header):** `ai:andrea-engineering` — stable, lowercase-hyphenated, machine-parseable. Appears in marks, events, and the API response.
- **Display name (`name` on `POST /presence`):** `Andrea Engineering` — human-readable, shown in Proof's presence chips and comment-author badges.

Set the display name once per doc session by posting to presence with the `X-Agent-Id` header; Proof binds the name to that agent ID for the session. These values are the defaults for any caller of this skill; a caller may pass a different `identity` pair if a distinct subagent should own the doc. Do not use `ai:compound` or other ad-hoc variants — identity stays uniform unless a caller explicitly overrides it.

## Publish Mode

The primary use is one-way publishing: take an existing local markdown file (a brainstorm, a plan, a learning, a draft), read its full contents and post them as the new doc's body (see "Workflow: Create and Share a New Document" for the source-file recipe — never publish placeholder content), and hand the user a shareable URL. The local file stays canonical — publishing does not sync anything back to disk. The user can open the link to read, comment, and share with others; the agent can also participate via the edit APIs below when given the URL. Two entry points, identical mechanics (see "Workflow: Create and Share a New Document"):

- **Direct user request** — a bare user phrase naming a local markdown file and asking to share it via Proof: "share this to proof", "publish this to proof", "open this in proof editor so I can review", "get me a proof link for this doc". The file is whichever markdown the user just created, edited, or referenced; if ambiguous, ask which file. This is a first-class entry point — do not require an upstream caller.
- **Upstream skill handoff** — `ae-brainstorm`, `ae-ideate`, or `ae-plan` finishes a draft and hands it off to publish for human review, passing the file path and title explicitly.

Only publish markdown. If the source is an HTML plan, do not upload it
to Proof; return the local browser/open path instead. When publishing a unified
plan, label the title by readiness when available, e.g. `Plan: <title>
(requirements-only)` or `Plan: <title> (implementation-ready)`.

## Transport References

Choose one transport before making a request:

- **Shared Proof URL or web API** — read `references/web-api.md` before the first request. It owns authentication, mutation tokens, retry discipline, edit primitives, and endpoint shapes.
- **Running macOS Proof app** — read `references/local-bridge.md` before the first localhost request.

Do not load both unless the task explicitly crosses transports. The workflows below define the user-facing jobs; the selected transport reference defines the wire contract.

## Workflow: Review a Shared Document

When given a Proof URL like `https://www.proofeditor.ai/d/abc123?token=xxx`:

1. Extract the slug (`abc123`) and token from the URL
2. Read the document via content negotiation on the shared URL or via `/api/agent/{slug}/state` when you need marks/mutation metadata
3. For content edits, prefer `/edit/v2` `find_replace_in_doc` or block operations; use `/ops` for comments, suggestions, and comment replies/resolution
4. The author sees changes in real-time

```bash
SHARE_URL="https://www.proofeditor.ai/d/abc123?token=xxx"
curl -s -H "Accept: application/json" "$SHARE_URL"
curl -s -H "Accept: text/markdown" "$SHARE_URL"

# Read once for content + the initial baseToken.
# After each successful mutation, update BASE from the response's mutationBase.token.
STATE=$(curl -s "https://www.proofeditor.ai/api/agent/abc123/state" \
  -H "x-share-token: xxx")
BASE=$(printf '%s' "$STATE" | jq -r '.mutationBase.token')
# Inspect doc fields as needed: printf '%s' "$STATE" | jq '.markdown, .revision'

# Comment
OP_RESP=$(curl -s -X POST "https://www.proofeditor.ai/api/agent/abc123/ops" \
  -H "Content-Type: application/json" \
  -H "x-share-token: xxx" \
  -H "X-Agent-Id: ai:andrea-engineering" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d "$(jq -n --arg base "$BASE" '{type:"comment.add",quote:"text",by:"ai:andrea-engineering",text:"comment",baseToken:$base}')")
NEXT_BASE=$(printf '%s' "$OP_RESP" | jq -r '.mutationBase.token // empty')
[ -n "$NEXT_BASE" ] && BASE="$NEXT_BASE"

# Suggest edit (tracked, pending)
OP_RESP=$(curl -s -X POST "https://www.proofeditor.ai/api/agent/abc123/ops" \
  -H "Content-Type: application/json" \
  -H "x-share-token: xxx" \
  -H "X-Agent-Id: ai:andrea-engineering" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d "$(jq -n --arg base "$BASE" '{type:"suggestion.add",kind:"replace",quote:"old",by:"ai:andrea-engineering",content:"new",baseToken:$base}')")
NEXT_BASE=$(printf '%s' "$OP_RESP" | jq -r '.mutationBase.token // empty')
[ -n "$NEXT_BASE" ] && BASE="$NEXT_BASE"

# Suggest and immediately apply (tracked, committed)
OP_RESP=$(curl -s -X POST "https://www.proofeditor.ai/api/agent/abc123/ops" \
  -H "Content-Type: application/json" \
  -H "x-share-token: xxx" \
  -H "X-Agent-Id: ai:andrea-engineering" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d "$(jq -n --arg base "$BASE" '{type:"suggestion.add",kind:"replace",quote:"old",by:"ai:andrea-engineering",content:"new",status:"accepted",baseToken:$base}')")
NEXT_BASE=$(printf '%s' "$OP_RESP" | jq -r '.mutationBase.token // empty')
[ -n "$NEXT_BASE" ] && BASE="$NEXT_BASE"

# Direct content edit (preferred when visible suggestion marks are not needed)
SNAPSHOT=$(curl -s "https://www.proofeditor.ai/api/agent/abc123/snapshot" \
  -H "x-share-token: xxx")
EDIT_BASE=$(printf '%s' "$SNAPSHOT" | jq -r '.mutationBase.token')
curl -X POST "https://www.proofeditor.ai/api/agent/abc123/edit/v2?return=minimal" \
  -H "Content-Type: application/json" \
  -H "x-share-token: xxx" \
  -H "X-Agent-Id: ai:andrea-engineering" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d "$(jq -n --arg base "$EDIT_BASE" '{by:"ai:andrea-engineering",baseToken:$base,operations:[{op:"find_replace_in_doc",find:"old",replace:"new",occurrence:"all"}]}')"
```

## Workflow: Create and Share a New Document

**Publishing a local file (the primary case):** read the file and JSON-encode its full contents into the `markdown` field with `jq --rawfile` so newlines, quotes, and backticks are escaped correctly. Never hand-write the body or leave the inline placeholder — that publishes a placeholder doc instead of the source artifact (the plan, requirements, or ideation file the caller passed).

```bash
SRC="docs/plans/2026-05-04-001-feat-foo-plan.md"   # source file from the caller
TITLE="Plan: Foo"                                   # caller-provided title

# 1. Create — from a local source file:
RESPONSE=$(jq -n --arg title "$TITLE" --rawfile md "$SRC" '{title:$title, markdown:$md}' \
  | curl -s -X POST https://www.proofeditor.ai/share/markdown \
    -H "Content-Type: application/json" -d @-)
# (Ad-hoc inline content instead of a file:
#  -d '{"title":"My Doc","markdown":"# Title\n\nContent here."}')

# 2. Extract URL and token
URL=$(echo "$RESPONSE" | jq -r '.tokenUrl')
SLUG=$(echo "$RESPONSE" | jq -r '.slug')
TOKEN=$(echo "$RESPONSE" | jq -r '.accessToken')

# 3. Bind display name via presence
curl -s -X POST "https://www.proofeditor.ai/api/agent/$SLUG/presence" \
  -H "Content-Type: application/json" \
  -H "x-share-token: $TOKEN" \
  -H "X-Agent-Id: ai:andrea-engineering" \
  -d '{"name":"Andrea Engineering","status":"reading","summary":"Uploaded doc"}'

# 4. Share the URL
echo "$URL"

# 5. Make comment/suggestion edits using the ops endpoint (baseToken required)
BASE=$(curl -s "https://www.proofeditor.ai/api/agent/$SLUG/state" \
  -H "x-share-token: $TOKEN" | jq -r '.mutationBase.token')
OP_RESP=$(curl -s -X POST "https://www.proofeditor.ai/api/agent/$SLUG/ops" \
  -H "Content-Type: application/json" \
  -H "x-share-token: $TOKEN" \
  -H "X-Agent-Id: ai:andrea-engineering" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d "$(jq -n --arg base "$BASE" '{type:"comment.add",quote:"Content here",by:"ai:andrea-engineering",text:"Added a note",baseToken:$base}')")
NEXT_BASE=$(printf '%s' "$OP_RESP" | jq -r '.mutationBase.token // empty')
[ -n "$NEXT_BASE" ] && BASE="$NEXT_BASE"

# For content edits, prefer /edit/v2 over rewrite.apply.
SNAPSHOT=$(curl -s "https://www.proofeditor.ai/api/agent/$SLUG/snapshot" \
  -H "x-share-token: $TOKEN")
EDIT_BASE=$(printf '%s' "$SNAPSHOT" | jq -r '.mutationBase.token')
curl -X POST "https://www.proofeditor.ai/api/agent/$SLUG/edit/v2?return=minimal" \
  -H "Content-Type: application/json" \
  -H "x-share-token: $TOKEN" \
  -H "X-Agent-Id: ai:andrea-engineering" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d "$(jq -n --arg base "$EDIT_BASE" '{by:"ai:andrea-engineering",baseToken:$base,operations:[{op:"find_replace_in_doc",find:"Content",replace:"Updated content",occurrence:"all"}]}')"
```

## Workflow: Pull a Proof Doc to Local

Sync the current Proof doc state to a local markdown file. Used for:

- Ad-hoc snapshots of a Proof doc to disk (before closing the tab, archiving, handing off)
- Pulling a shared Proof doc that the user (or others) edited back down to a local working copy
- Refreshing a local working copy against the live Proof version

```bash
SLUG=<slug>
TOKEN=<accessToken>
LOCAL=<absolute-path>

# One read to a temp file — avoids passing markdown through $(...), which would strip trailing newlines.
STATE_TMP=$(mktemp)
curl -s "https://www.proofeditor.ai/api/agent/$SLUG/state" \
  -H "x-share-token: $TOKEN" > "$STATE_TMP"
REVISION=$(jq -r '.revision' "$STATE_TMP")

# Atomic write: stream .markdown bytes directly to a temp sibling, then rename.
TMP="${LOCAL}.proof-sync.$$"
jq -jr '.markdown' "$STATE_TMP" > "$TMP" && mv "$TMP" "$LOCAL"
rm "$STATE_TMP"
```

`jq -jr` (`-j` no trailing newline, `-r` raw string) streams the markdown bytes straight to the temp file without going through a shell variable, so trailing newlines survive intact. `mv` within the same filesystem is atomic — a crashed write leaves the original untouched rather than a half-written file.

**Confirm before writing when the pull isn't directly asked for.** If a workflow ends up pulling as a side-effect of a different action, surface the impending write with a short confirm like "Sync Proof doc to `<localPath>`?" A silent overwrite is surprising — the user may have forgotten the local file exists in that session, or expected Proof to stay canonical until they explicitly asked to pull.

## Safety

- Use `/state` content as source of truth before editing
- During active collab use `edit/v2` (direct block changes) or `suggestion.add` (tracked changes); reserve `rewrite.apply` for no-client scenarios since it's blocked by `LIVE_CLIENTS_PRESENT` when anyone is connected
- Prefer `find_replace_in_doc` and block-level `/edit/v2` edits before considering `rewrite.apply`
- Don't span table cells in a single replace
- Always include `by: "ai:andrea-engineering"` on every op and `X-Agent-Id: ai:andrea-engineering` in headers for consistent attribution
- Reuse `baseToken` from your most recent `/state` or `/snapshot` read; on `STALE_BASE`, re-read and retry once
