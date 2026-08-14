#!/usr/bin/env python3
"""Extract failed tool calls from a current Codex session JSONL stream."""

import argparse
import io
import json
import os
import sys


parser = argparse.ArgumentParser()
parser.add_argument(
    "--output",
    metavar="PATH",
    help="Write extracted errors to PATH and emit only status on stdout.",
)
args = parser.parse_args()

original_stdout = sys.stdout
if args.output:
    sys.stdout = io.StringIO()

stats = {"lines": 0, "parse_errors": 0, "errors_found": 0}
calls = {}


def output_text(output):
    if isinstance(output, str):
        return output
    if not isinstance(output, list):
        return ""
    return "\n".join(
        block.get("text", "")
        for block in output
        if isinstance(block, dict) and isinstance(block.get("text"), str)
    )


def failure(payload):
    text = output_text(payload.get("output", ""))
    if payload.get("is_error") is True:
        return text
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines and lines[0] in ("Script failed", "Script error:"):
        return text
    marker = "Process exited with code "
    status_text = "\n".join(lines[:8])
    if marker in status_text:
        try:
            if int(status_text.split(marker, 1)[1].split("\n", 1)[0]) != 0:
                return text
        except (IndexError, ValueError):
            return text
    return ""


def summarize(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        if line not in ("Script failed", "Script error:", "Output:") and not line.startswith("Wall time"):
            return line[:240]
    return lines[0][:240] if lines else "tool call failed"


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    stats["lines"] += 1
    try:
        obj = json.loads(line)
        if obj.get("type") != "response_item":
            continue
        payload = obj.get("payload", {})
        item_type = payload.get("type")
        if item_type in ("function_call", "custom_tool_call"):
            call_id = payload.get("call_id")
            if call_id:
                calls[call_id] = {
                    "ts": obj.get("timestamp", "")[:19],
                    "name": payload.get("name", "tool"),
                }
            continue
        if item_type not in ("function_call_output", "custom_tool_call_output"):
            continue
        error = failure(payload)
        if not error:
            continue
        entry = calls.get(
            payload.get("call_id"),
            {"ts": obj.get("timestamp", "")[:19], "name": "tool"},
        )
        print(f"[{entry['ts']}] [error] {entry['name']}: {summarize(error)}")
        print("---")
        stats["errors_found"] += 1
    except (json.JSONDecodeError, ValueError, KeyError, TypeError):
        stats["parse_errors"] += 1

print(json.dumps({"_meta": True, **stats}))

if args.output:
    body = sys.stdout.getvalue()
    sys.stdout = original_stdout
    with open(args.output, "w") as output_file:
        output_file.write(body)
    print(
        json.dumps(
            {
                "_meta": True,
                "wrote": args.output,
                "bytes": os.path.getsize(args.output),
                **stats,
            }
        )
    )
