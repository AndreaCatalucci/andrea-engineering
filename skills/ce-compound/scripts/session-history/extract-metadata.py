#!/usr/bin/env python3
"""Extract metadata and keyword matches from Codex JSONL sessions.

Batch mode (preferred):
  python3 extract-metadata.py session1.jsonl session2.jsonl

Single-file mode:
  head -25 session.jsonl | python3 extract-metadata.py

Outputs one JSON object per session followed by a `_meta` status object.
"""

import json
import os
import sys


MAX_LINES = 25
TAIL_BYTES = 16_384


def extract_from_lines(lines):
    """Return metadata from Codex session_meta and turn_context records."""
    metadata = {}
    for line in lines:
        try:
            obj = json.loads(line.strip())
        except (json.JSONDecodeError, ValueError):
            continue

        record_type = obj.get("type")
        payload = obj.get("payload", {})
        if record_type == "session_meta":
            metadata.update(
                platform="codex",
                cwd=payload.get("cwd", ""),
                session=payload.get("id", ""),
                ts=payload.get("timestamp", obj.get("timestamp", "")),
                source=payload.get("source", ""),
                cli_version=payload.get("cli_version", ""),
            )
        elif record_type == "turn_context":
            metadata["platform"] = "codex"
            metadata["model"] = payload.get("model", "")
            metadata["cwd"] = metadata.get("cwd") or payload.get("cwd", "")

    return metadata or None


def get_last_timestamp(filepath, size):
    """Read the file tail and return the last timestamped record."""
    try:
        with open(filepath, "rb") as session_file:
            session_file.seek(max(0, size - TAIL_BYTES))
            lines = session_file.read().decode("utf-8", errors="ignore").splitlines()
        for line in reversed(lines):
            try:
                timestamp = json.loads(line).get("timestamp")
                if timestamp:
                    return timestamp
            except (json.JSONDecodeError, ValueError):
                continue
    except OSError:
        pass
    return None


def _extract_user_assistant_text(filepath):
    """Return searchable Codex user and assistant text, excluding tool output."""
    chunks = []
    try:
        with open(filepath, "r", errors="replace") as session_file:
            for line in session_file:
                try:
                    obj = json.loads(line)
                except (json.JSONDecodeError, ValueError):
                    continue

                payload = obj.get("payload", {})
                if obj.get("type") == "event_msg" and payload.get("type") == "user_message":
                    message = payload.get("message", "")
                    if isinstance(message, str):
                        # Codex may prefix user messages with an injected system
                        # instruction block. Search only user-authored text.
                        chunks.append(message.split("</system_instruction>")[-1])
                elif obj.get("type") == "response_item":
                    if payload.get("type") != "message" or payload.get("role") != "assistant":
                        continue
                    for block in payload.get("content", []):
                        if isinstance(block, dict) and block.get("type") == "output_text":
                            chunks.append(block.get("text", ""))
    except OSError:
        pass
    return "\n".join(chunks)


def count_keyword_matches(filepath, keywords):
    text = _extract_user_assistant_text(filepath).lower()
    return {keyword: text.count(keyword.lower()) for keyword in keywords}


def process_file(filepath):
    try:
        size = os.path.getsize(filepath)
        with open(filepath, "r") as session_file:
            lines = []
            for index, line in enumerate(session_file):
                if index >= MAX_LINES:
                    break
                lines.append(line)
        result = extract_from_lines(lines)
        if not result:
            return None, filepath

        result["file"] = filepath
        result["size"] = size
        last_timestamp = get_last_timestamp(filepath, size)
        if last_timestamp:
            result["last_ts"] = last_timestamp
        return result, None
    except OSError:
        return None, filepath


def cwd_matches_filter(session_cwd, cwd_filter):
    if not session_cwd or not cwd_filter:
        return True
    if os.path.isabs(cwd_filter):
        return os.path.normpath(session_cwd) == os.path.normpath(cwd_filter)
    return cwd_filter in session_cwd


def parse_args(argv):
    files = []
    cwd_filter = None
    keywords = None
    index = 0
    while index < len(argv):
        if argv[index] == "--cwd-filter" and index + 1 < len(argv):
            cwd_filter = argv[index + 1]
            index += 2
        elif argv[index] == "--keyword" and index + 1 < len(argv):
            keywords = [word for word in argv[index + 1].split(",") if word]
            index += 2
        elif not argv[index].startswith("-"):
            files.append(argv[index])
            index += 1
        else:
            index += 1
    return files, cwd_filter, keywords


def print_batch(files, cwd_filter, keywords):
    processed = 0
    parse_errors = 0
    filtered = 0
    matched = 0

    for filepath in files:
        if not filepath.endswith(".jsonl"):
            continue
        result, error = process_file(filepath)
        processed += 1
        if error:
            parse_errors += 1
            continue

        if cwd_filter and result.get("cwd") and not cwd_matches_filter(result["cwd"], cwd_filter):
            filtered += 1
            continue
        if keywords:
            matches = count_keyword_matches(filepath, keywords)
            result["keyword_matches"] = matches
            result["match_count"] = sum(matches.values())
            if result["match_count"] == 0:
                continue
            matched += 1
        print(json.dumps(result))

    status = {"_meta": True, "files_processed": processed, "parse_errors": parse_errors}
    if filtered:
        status["filtered_by_cwd"] = filtered
    if keywords:
        status["files_matched"] = matched
    print(json.dumps(status))


def print_stdin(keywords):
    lines = [] if sys.stdin.isatty() else list(sys.stdin)
    if not lines:
        status = {"_meta": True, "files_processed": 0, "parse_errors": 0}
        if keywords:
            status["files_matched"] = 0
        print(json.dumps(status))
        return

    result = extract_from_lines(lines)
    if result:
        print(json.dumps(result))
    print(
        json.dumps(
            {"_meta": True, "files_processed": 1, "parse_errors": 0 if result else 1}
        )
    )


files, cwd_filter, keywords = parse_args(sys.argv[1:])
if files:
    print_batch(files, cwd_filter, keywords)
else:
    print_stdin(keywords)
