#!/usr/bin/env python3
"""Extract a compact conversation skeleton from a current Codex JSONL session.

Usage:
  python3 extract-skeleton.py < session.jsonl
  python3 extract-skeleton.py --output PATH < session.jsonl

The skeleton includes user messages, assistant output text, and collapsed tool
summaries. Reasoning and tool output are intentionally omitted.
"""

import argparse
import io
import json
import os
import sys


parser = argparse.ArgumentParser()
parser.add_argument(
    "--output",
    metavar="PATH",
    help="Write the skeleton to PATH and emit only status on stdout.",
)
args = parser.parse_args()

original_stdout = sys.stdout
if args.output:
    sys.stdout = io.StringIO()

stats = {
    "lines": 0,
    "parse_errors": 0,
    "user": 0,
    "assistant": 0,
    "tool": 0,
}
calls = {}
completed_tools = []


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


def call_target(payload):
    raw = payload.get("arguments", payload.get("input", ""))
    if not isinstance(raw, str):
        return ""
    try:
        parsed = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return raw.strip().splitlines()[0][:120] if raw.strip() else ""
    if not isinstance(parsed, dict):
        return str(parsed)[:120]
    for key in ("cmd", "path", "file_path", "query", "question", "target"):
        value = parsed.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip().splitlines()[0][:120]
    return ""


def failed_status(payload):
    text = output_text(payload.get("output", ""))
    if payload.get("is_error") is True:
        return "error"
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines and lines[0] in ("Script failed", "Script error:"):
        return "error"
    marker = "Process exited with code "
    status_text = "\n".join(lines[:8])
    if marker in status_text:
        try:
            code = int(status_text.split(marker, 1)[1].split("\n", 1)[0])
            return "ok" if code == 0 else f"error(exit {code})"
        except (IndexError, ValueError):
            return "error"
    return "ok"


def flush_tools():
    if not completed_tools:
        return
    if len(completed_tools) <= 2:
        for entry in completed_tools:
            suffix = f" {entry['target']}" if entry["target"] else ""
            print(f"[{entry['ts']}] [tool] {entry['name']}{suffix} -> {entry['status']}")
    else:
        names = [entry["name"] for entry in completed_tools]
        shown = ", ".join(names[:3])
        if len(names) > 3:
            shown += f", +{len(names) - 3} more"
        failures = sum(entry["status"] != "ok" for entry in completed_tools)
        status = "all ok" if failures == 0 else f"{failures} error"
        print(
            f"[{completed_tools[0]['ts']}] [tools] {len(completed_tools)} calls"
            f" ({shown}) -> {status}"
        )
    stats["tool"] += len(completed_tools)
    completed_tools.clear()


def handle_event_message(obj, payload):
    if payload.get("type") != "user_message":
        return
    text = payload.get("message", "")
    if not isinstance(text, str):
        return
    text = text.split("</system_instruction>")[-1].strip()
    if len(text) <= 15:
        return
    flush_tools()
    print(f"[{obj.get('timestamp', '')[:19]}] [user] {text[:800]}")
    print("---")
    stats["user"] += 1


def handle_response_item(obj, payload):
    item_type = payload.get("type")
    timestamp = obj.get("timestamp", "")[:19]

    if item_type == "message" and payload.get("role") == "assistant":
        for block in payload.get("content", []):
            if not isinstance(block, dict) or block.get("type") != "output_text":
                continue
            text = block.get("text", "")
            if not isinstance(text, str) or len(text) <= 20:
                continue
            flush_tools()
            print(f"[{timestamp}] [assistant] {text[:800]}")
            print("---")
            stats["assistant"] += 1
        return

    if item_type in ("function_call", "custom_tool_call"):
        call_id = payload.get("call_id")
        if call_id:
            calls[call_id] = {
                "ts": timestamp,
                "name": payload.get("name", "tool"),
                "target": call_target(payload),
            }
        return

    if item_type not in ("function_call_output", "custom_tool_call_output"):
        return
    call_id = payload.get("call_id")
    entry = calls.pop(call_id, {"ts": timestamp, "name": "tool", "target": ""})
    entry["status"] = failed_status(payload)
    completed_tools.append(entry)


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    stats["lines"] += 1
    try:
        obj = json.loads(line)
        payload = obj.get("payload", {})
        if obj.get("type") == "event_msg":
            handle_event_message(obj, payload)
        elif obj.get("type") == "response_item":
            handle_response_item(obj, payload)
    except (json.JSONDecodeError, ValueError, KeyError, TypeError):
        stats["parse_errors"] += 1

for entry in calls.values():
    entry["status"] = "missing output"
    completed_tools.append(entry)
flush_tools()
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
