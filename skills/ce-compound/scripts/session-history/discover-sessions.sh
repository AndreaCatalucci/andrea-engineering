#!/usr/bin/env bash
# Discover recent Codex session files.
#
# Usage: discover-sessions.sh <repo-name> <days> [--cwd /abs/repo/root]
#
# Outputs one ~/.codex/sessions JSONL path per line. Repository filtering is
# handled by extract-metadata.py, because Codex stores every repository under
# the same date-based session tree.

set -euo pipefail

REPO_NAME="${1:?Usage: discover-sessions.sh <repo-name> <days> [--cwd /abs/repo/root]}"
DAYS="${2:?Usage: discover-sessions.sh <repo-name> <days> [--cwd /abs/repo/root]}"

# Retain the caller-facing repository arguments for compatibility. Discovery
# cannot use them until it reads JSONL metadata, which extract-metadata.py does.
: "$REPO_NAME"
shift 2
while [ $# -gt 0 ]; do
    case "$1" in
        --cwd)
            [ $# -ge 2 ] || { echo "--cwd requires a value" >&2; exit 2; }
            shift 2
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 2
            ;;
    esac
done

BASE="$HOME/.codex/sessions"
[ -d "$BASE" ] || exit 0

# mtime includes long-running sessions that began before the scan window but
# received new messages within it.
find "$BASE" -type f -name "*.jsonl" -mtime "-${DAYS}" 2>/dev/null
