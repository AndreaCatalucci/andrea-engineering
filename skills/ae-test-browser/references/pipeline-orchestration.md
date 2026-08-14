# Pipeline-Mode Server Orchestration

Read and follow this file only when invoked with `mode:pipeline` by LFG or another automated runner. It overrides manual-mode port handling and dev-server verification. Browser testing still uses `browser:control-in-app-browser`. Pipeline mode is unattended: never block on a question.

## 1. Use the Codex in-app browser without a visibility question

Keep the normal integrated browser surface visible and non-blocking. Do not repeatedly steal focus while routes change.

## 2. Claim a free port

Multiple Codex tasks may run on the same machine. Starting from the preferred port computed by the main workflow, scan upward and print the first free port:

```bash
START_PORT=3000 # replace with the preferred port from step 4
find_free_port() {
  local candidate="$1"
  while lsof -i ":${candidate}" -sTCP:LISTEN -t >/dev/null 2>&1; do
    candidate=$((candidate + 1))
  done
  printf '%s\n' "$candidate"
}
find_free_port "$START_PORT"
```

Record the literal port printed by this command. Shell variables do not persist between Codex terminal calls.

## 3. Start the server in a persistent Codex terminal session

Use Codex `exec_command` to launch the project command on the selected literal port. The long-running command should yield a session ID; retain it for polling and eventual cleanup. Prefer an explicit command from the user or active project instructions. Otherwise choose the first applicable command:

```bash
PORT=<selected-port> exec bin/dev
```

```bash
exec bin/rails server -p <selected-port>
```

```bash
PORT=<selected-port> exec npm run dev
```

Do not background the process, redirect it to a shared log file, or discard the session ID. Poll the session output with Codex `write_stdin` when startup progress or failures need inspection.

## 4. Verify readiness

From a separate Codex terminal call, probe the literal URL for up to 30 seconds. If it does not respond, poll the persistent server session, report its relevant recent output, record the pipeline failure, and stop browser testing.

Once ready, return to "Test Each Affected Page" in the main workflow. Navigate the Codex in-app browser to `http://localhost:<selected-port>` and use that literal port for every route. Stop the retained terminal session when the pipeline no longer needs the server.
