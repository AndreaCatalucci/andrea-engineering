#!/usr/bin/env python3
"""Report deterministic word and implementation-unit counts for a plan."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
MARKDOWN_UNIT_RE = re.compile(r"^###\s+U(\d+)\.", re.MULTILINE)
HTML_UNIT_RE = re.compile(r"\bid=[\"']u(\d+)[\"']", re.IGNORECASE)


def visible_text(path: Path, source: str) -> str:
    if path.suffix.lower() != ".html":
        return source
    without_scripts = re.sub(
        r"<(script|style)\b[^>]*>.*?</\1>", " ", source, flags=re.IGNORECASE | re.DOTALL
    )
    return html.unescape(re.sub(r"<[^>]+>", " ", without_scripts))


def unit_ids(path: Path, source: str) -> set[str]:
    pattern = HTML_UNIT_RE if path.suffix.lower() == ".html" else MARKDOWN_UNIT_RE
    return set(pattern.findall(source))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()

    source = args.plan.read_text(encoding="utf-8")
    payload = {
        "path": str(args.plan),
        "word_count": len(WORD_RE.findall(visible_text(args.plan, source))),
        "implementation_unit_count": len(unit_ids(args.plan, source)),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
