# Proof Local Bridge

Read this reference only when the user wants to operate the running macOS Proof app through `http://localhost:9847`.

Send `X-Agent-Id: ai:andrea-engineering` and `Content-Type: application/json`. When multiple documents are open, include the selected `X-Window-Id`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/windows` | List open documents |
| GET | `/state` | Read markdown, cursor, and word count |
| GET | `/marks` | List comments and suggestions |
| POST | `/marks/suggest-replace` | Suggest replacing quoted text |
| POST | `/marks/suggest-insert` | Suggest inserting after quoted text |
| POST | `/marks/suggest-delete` | Suggest deleting quoted text |
| POST | `/marks/comment` | Comment on quoted text |
| POST | `/marks/reply` | Reply to a mark |
| POST | `/marks/resolve` | Resolve a mark |
| POST | `/marks/accept` | Accept a suggestion |
| POST | `/marks/reject` | Reject a suggestion |
| POST | `/rewrite` | Last-resort whole-document replacement |
| POST | `/presence` | Set `thinking`, `reading`, `idle`, `acting`, `waiting`, or `completed` |
| GET | `/events/pending` | Poll for user actions |

Prefer marks and narrow edits to `/rewrite`. Keep the `by` identity aligned with `X-Agent-Id` on every attributed operation.
