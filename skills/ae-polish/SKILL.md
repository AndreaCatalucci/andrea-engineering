---
name: ae-polish
description: "Start the dev server, inspect a feature in the browser, and iterate on polish. Use when the user wants interactive visual or UX refinement of a working feature."
---

# Polish

Start the dev server, open the feature in a browser, and iterate. You use the feature, say what feels off, and fixes happen.

## Phase 0: Confirm the workspace

1. If a PR number or branch name was provided, check it out (probe for existing worktrees first).
2. If blank, use the current branch.
3. Report the active branch and preserve any unrelated local changes.

## Phase 1: Start the dev server

The scripts below ship in this skill's `scripts/` directory. Codex shell calls run from the user's project, so invoke each script through the absolute path to this skill. Shell state does not persist across calls; set `SKILL_DIR` in every command.

### 1.1 Detect the project

Identify the framework:

```bash
SKILL_DIR="<absolute path of the directory containing this SKILL.md>";
bash "$SKILL_DIR/scripts/detect-project-type.sh"
```

Route by type to the matching recipe reference for start command and port defaults:

| Type | Recipe |
| --- | --- |
| `rails` | `references/dev-server-rails.md` |
| `next` | `references/dev-server-next.md` |
| `vite` | `references/dev-server-vite.md` |
| `nuxt` | `references/dev-server-nuxt.md` |
| `astro` | `references/dev-server-astro.md` |
| `remix` | `references/dev-server-remix.md` |
| `sveltekit` | `references/dev-server-sveltekit.md` |
| `procfile` | `references/dev-server-procfile.md` |
| `unknown` | Ask the user how to start the project |

For framework types that need a package manager, run the resolver and substitute the result into the start command:

```bash
SKILL_DIR="<absolute path of the directory containing this SKILL.md>";
bash "$SKILL_DIR/scripts/resolve-package-manager.sh"
```

Resolve the port:

```bash
SKILL_DIR="<absolute path of the directory containing this SKILL.md>";
bash "$SKILL_DIR/scripts/resolve-port.sh" --type <type>
```

Before choosing the detected default, honor any explicit start command, working directory, URL, or port already supplied by the user or active project instructions. For an unknown project, ask the user for the start command instead of inventing one.

### 1.2 Start the server

Start the dev server in a persistent Codex terminal session so it remains available while browser inspection and edits continue. Keep the session ID, and poll it for startup failures. Probe `http://localhost:<port>` for up to 30 seconds. If it does not come up, show the relevant recent log output and ask the user how the project should be started.

### 1.3 Inspect in the Codex browser

Load Codex's `browser:control-in-app-browser` skill and open `http://localhost:<port>` in the in-app browser. Navigate to the requested feature, inspect visible and interactive states, and capture screenshots when visual comparison helps. Use `chrome:control-chrome` only when the task specifically depends on the user's existing Chrome session.

Send a commentary update:
```
Dev server running on http://localhost:<port>
Inspecting the requested feature now; you can also browse it at that URL.
```

## Phase 2: Iterate

This is the core loop. The user browses the feature and tells you what to improve. You fix it. Repeat until they're happy.

- When the user describes something to fix → make the change, the dev server hot-reloads
- When the user asks to check something → use the Codex in-app browser to inspect the page and capture evidence
- When the user says they're done → stop the dev server if it is no longer needed, summarize the changes and verification, and leave committing to an explicit request

No checklist. No envelope. Just conversation.

## References

Reference files (loaded on demand):
- `references/dev-server-detection.md` — port resolution documentation
- `references/dev-server-rails.md` — Rails dev-server defaults
- `references/dev-server-next.md` — Next.js dev-server defaults
- `references/dev-server-vite.md` — Vite dev-server defaults
- `references/dev-server-nuxt.md` — Nuxt dev-server defaults
- `references/dev-server-astro.md` — Astro dev-server defaults
- `references/dev-server-remix.md` — Remix dev-server defaults
- `references/dev-server-sveltekit.md` — SvelteKit dev-server defaults
- `references/dev-server-procfile.md` — Procfile-based dev-server defaults

Scripts (invoked via `bash "$SKILL_DIR/scripts/<name>"` — see Phase 1 for `SKILL_DIR`):
- `scripts/detect-project-type.sh` — project-type classifier
- `scripts/resolve-package-manager.sh` — lockfile-based package-manager resolver
- `scripts/resolve-port.sh` — port resolution cascade
