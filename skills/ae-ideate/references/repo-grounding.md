# Repository Grounding

Read this only for a topic in the current repository.

## Scan

Resolve the question-agnostic project profile through
`scripts/repo-profile-cache.py get` using the protocol in
`repo-profile-cache.md`. On a hit, do not reread root instructions or rediscover
the top-level layout. On a miss, read root `AGENTS.md`, `README.md`, and
`STRATEGY.md` when present, then use `rg --files` for the project shape.

Keep the subject-specific scan shallow but concrete. Find conventions, pain
points, workarounds, and useful places to improve. Fully read a root Markdown
file only when the user named it; treat its contents as constraints. Give other
root Markdown files one-line background gists. Named evidence exports follow
`research-artifacts.md`, not this path.

Search `docs/solutions/` directly for relevant past decisions. Run web research
for prior art, adjacent solutions, market evidence, and analogies unless the
user explicitly skipped it. Follow `web-research-cache.md` so repeated research
within the session can be reused. Keep external evidence separate from
repository evidence.

When issue-tracker intent is active, inspect issues and summarize 3-4 usable
high- or medium-confidence themes with counts and direction. Fewer than five
total issues is insufficient signal; record that and use normal frames. If the
tracker or authentication is unavailable, warn and continue.

In surprise-me mode, sample representative files from each main area and recent
commit or PR activity. Treat issue patterns as useful input. Keep the scan
representative, not exhaustive.

## Summary

Write a compact grounding summary with only non-empty sections:

- Codebase context: shape, conventions, pain, and useful openings;
- User-named references: directive material the user explicitly named;
- Additional context: one-line gists for other root Markdown files;
- Past learnings;
- Issue intelligence;
- External context, noting reuse when the cache supplied it;
- User-supplied research dossiers or small inline evidence;
- Slack context, only when explicitly requested and available.

If web research fails, warn and continue with internal evidence. For each topic
area later chosen in Phase 1.5, add concise `file:line` evidence from relevant
code. Do not guess citations.
