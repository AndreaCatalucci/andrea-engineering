#!/usr/bin/env python3
"""Validate, seal, accept, and hydrate ce-code-review result files."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "references" / "findings-schema.json"
SOURCE_KEY = re.compile(r"^([a-z0-9][a-z0-9_-]*):([0-9a-f]{64}):(\d+)$")
SCHEMA_KEYWORDS = {
    "$schema",
    "_meta",
    "additionalProperties",
    "description",
    "enum",
    "items",
    "maxLength",
    "minItems",
    "minLength",
    "minimum",
    "properties",
    "required",
    "title",
    "type",
}
SCHEMA_TYPES = {"array", "boolean", "integer", "null", "object", "string"}
COMPACT_REQUIRED_FIELDS = (
    "title",
    "severity",
    "file",
    "line",
    "confidence",
    "autofix_class",
    "owner",
    "requires_verification",
    "pre_existing",
)
COMPACT_OPTIONAL_FIELDS = {"suggested_fix", "first_evidence"}


class ArtifactError(ValueError):
    """A review result or its schema failed validation."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ArtifactError(message)


def _object(value: Any, name: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{name} must be an object")
    return value


def _list(value: Any, name: str) -> list[Any]:
    _require(isinstance(value, list), f"{name} must be an array")
    return value


def _text(value: Any, name: str) -> str:
    _require(isinstance(value, str) and bool(value.strip()), f"{name} must be non-empty text")
    return value


def _keys(value: dict[str, Any], required: set[str], optional: set[str], name: str) -> None:
    missing = required - value.keys()
    extra = value.keys() - required - optional
    _require(not missing, f"{name} missing fields: {', '.join(sorted(missing))}")
    _require(not extra, f"{name} has unsupported fields: {', '.join(sorted(extra))}")


def _load_json_with_digest(path: str | Path) -> tuple[dict[str, Any], str]:
    try:
        data = Path(path).read_bytes()
        value = json.loads(data)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ArtifactError(f"cannot read JSON from {path}: {error}") from error
    return _object(value, "document"), hashlib.sha256(data).hexdigest()


def _load_json(path: str | Path) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ArtifactError(f"cannot read JSON from {path}: {error}") from error
    return _object(value, "document")


def _load_schema(path: str | Path) -> tuple[dict[str, Any], str]:
    schema, digest = _load_json_with_digest(path)
    validate_schema_support(schema)
    return schema, digest


def _canonical_bytes(document: dict[str, Any]) -> bytes:
    return (json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _seal(document: dict[str, Any], output_path: str | Path) -> str:
    output = Path(output_path)
    data = _canonical_bytes(document)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{output.name}.", dir=output.parent)
        try:
            with os.fdopen(descriptor, "wb") as temporary:
                temporary.write(data)
                temporary.flush()
                os.fsync(temporary.fileno())
            os.replace(temporary_name, output)
        except Exception:
            try:
                os.unlink(temporary_name)
            except OSError:
                pass
            raise
    except OSError as error:
        raise ArtifactError(f"authoritative review result write failed: {error}") from error
    return hashlib.sha256(data).hexdigest()


def validate_schema_support(schema: dict[str, Any], location: str = "$") -> None:
    schema = _object(schema, f"schema {location}")
    for keyword in schema:
        _require(keyword in SCHEMA_KEYWORDS, f"unsupported schema keyword at {location}: {keyword}")

    raw_types = schema.get("type")
    if raw_types is not None:
        types = [raw_types] if isinstance(raw_types, str) else _list(raw_types, f"schema {location}.type")
        _require(bool(types), f"schema {location}.type must not be empty")
        for value in types:
            _require(value in SCHEMA_TYPES, f"unsupported schema type at {location}: {value}")

    if "required" in schema:
        required = _list(schema["required"], f"schema {location}.required")
        _require(all(isinstance(item, str) for item in required), f"schema {location}.required must contain strings")
    if "properties" in schema:
        properties = _object(schema["properties"], f"schema {location}.properties")
        for name, subschema in properties.items():
            validate_schema_support(subschema, f"{location}.{name}")
    if "items" in schema:
        validate_schema_support(schema["items"], f"{location}[]")
    if "additionalProperties" in schema:
        _require(isinstance(schema["additionalProperties"], bool), f"schema {location}.additionalProperties must be boolean")
    for keyword in ("minItems", "maxLength", "minLength", "minimum"):
        if keyword in schema:
            value = schema[keyword]
            _require(isinstance(value, int) and not isinstance(value, bool), f"schema {location}.{keyword} must be an integer")
    if "enum" in schema:
        _require(bool(_list(schema["enum"], f"schema {location}.enum")), f"schema {location}.enum must not be empty")


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "array":
        return isinstance(value, list)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    if expected == "object":
        return isinstance(value, dict)
    return isinstance(value, str)


def validate_instance(value: Any, schema: dict[str, Any], location: str = "document") -> None:
    raw_types = schema.get("type")
    if raw_types is not None:
        types = [raw_types] if isinstance(raw_types, str) else raw_types
        _require(any(_matches_type(value, expected) for expected in types), f"{location} has invalid type")
    if "enum" in schema:
        _require(value in schema["enum"], f"{location} has unsupported value: {value}")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        required = set(schema.get("required", []))
        missing = required - value.keys()
        _require(not missing, f"{location} missing fields: {', '.join(sorted(missing))}")
        if schema.get("additionalProperties") is False:
            extra = value.keys() - properties.keys()
            _require(not extra, f"{location} has unsupported field: {', '.join(sorted(extra))}")
        for name, item in value.items():
            if name in properties:
                validate_instance(item, properties[name], f"{location}.{name}")
    elif isinstance(value, list):
        if "minItems" in schema:
            _require(len(value) >= schema["minItems"], f"{location} has too few items")
        if "items" in schema:
            for index, item in enumerate(value):
                validate_instance(item, schema["items"], f"{location}[{index}]")
    elif isinstance(value, str):
        if "minLength" in schema:
            _require(len(value) >= schema["minLength"], f"{location} is too short")
        if "maxLength" in schema:
            _require(len(value) <= schema["maxLength"], f"{location} is too long")
    elif isinstance(value, int) and not isinstance(value, bool) and "minimum" in schema:
        _require(value >= schema["minimum"], f"{location} is below its minimum")


def _validate_reviewer(reviewer: Any, name: str = "reviewer") -> str:
    reviewer = _text(reviewer, name)
    _require(bool(re.fullmatch(r"[a-z0-9][a-z0-9_-]*", reviewer)), f"{name} has invalid characters")
    return reviewer


def _require_schema_version(value: Any, name: str) -> None:
    _require(
        isinstance(value, int) and not isinstance(value, bool) and value == 1,
        f"unsupported {name} schema_version",
    )


def _require_first_evidence(finding: dict[str, Any], evidence: Any, name: str) -> None:
    evidence = _text(evidence, f"{name}.first_evidence")
    locator = f"{finding['file']}:{finding['line']}"
    _require(
        evidence.startswith(locator)
        and (len(evidence) == len(locator) or evidence[len(locator)].isspace()),
        f"{name}.first_evidence must quote {locator}",
    )


def validate_review_document(document: dict[str, Any], schema: dict[str, Any], expected_reviewer: str) -> None:
    validate_instance(document, schema)
    expected_reviewer = _validate_reviewer(expected_reviewer, "expected reviewer")
    _require(document["reviewer"] == expected_reviewer, "review result reviewer does not match expected reviewer")
    for index, finding in enumerate(document["findings"]):
        evidence = finding["evidence"]
        if finding["confidence"] in {75, 100}:
            _require_first_evidence(finding, evidence[0], f"findings[{index}]")


def _receipt(
    document: dict[str, Any],
    digest: str,
    schema_digest: str,
    path: str | Path,
) -> dict[str, Any]:
    return {
        "kind": "code-review-result",
        "path": str(Path(path).resolve()),
        "sha256": digest,
        "schema_sha256": schema_digest,
        "reviewer": document["reviewer"],
        "finding_count": len(document["findings"]),
        "residual_risk_count": len(document["residual_risks"]),
        "testing_gap_count": len(document["testing_gaps"]),
    }


def seal_review_file(
    draft_path: str | Path,
    output_path: str | Path,
    reviewer: str,
    schema_path: str | Path = DEFAULT_SCHEMA,
) -> dict[str, Any]:
    schema, schema_digest = _load_schema(schema_path)
    document = _load_json(draft_path)
    validate_review_document(document, schema, reviewer)
    digest = _seal(document, output_path)
    return _receipt(document, digest, schema_digest, output_path)


def _source_key(reviewer: str, digest: str, index: int) -> str:
    return f"{reviewer}:{digest}:{index}"


def _compact_finding(finding: dict[str, Any], source_key: str, reviewer: str) -> dict[str, Any]:
    compact = {field: finding[field] for field in COMPACT_REQUIRED_FIELDS}
    if finding.get("suggested_fix") is not None:
        compact["suggested_fix"] = finding["suggested_fix"]
    if finding["confidence"] in {75, 100}:
        compact["first_evidence"] = finding["evidence"][0]
    compact["reviewers"] = [reviewer]
    compact["source_keys"] = [source_key]
    _validate_compact_finding(compact, "projected finding", include_lineage=True)
    return compact


def _validate_compact_finding(
    finding: dict[str, Any],
    name: str,
    *,
    include_lineage: bool = False,
) -> None:
    optional = set(COMPACT_OPTIONAL_FIELDS)
    if include_lineage:
        optional.update({"reviewers", "source_keys"})
    _keys(finding, set(COMPACT_REQUIRED_FIELDS), optional, name)
    _text(finding["title"], f"{name}.title")
    _require(len(finding["title"]) <= 100, f"{name}.title is too long")
    _text(finding["file"], f"{name}.file")
    _require(finding["severity"] in {"P0", "P1", "P2", "P3"}, f"{name}.severity is invalid")
    _require(
        isinstance(finding["line"], int)
        and not isinstance(finding["line"], bool)
        and finding["line"] >= 1,
        f"{name}.line is invalid",
    )
    _require(finding["confidence"] in {0, 25, 50, 75, 100}, f"{name}.confidence is invalid")
    _require(finding["autofix_class"] in {"gated_auto", "manual", "advisory"}, f"{name}.autofix_class is invalid")
    _require(finding["owner"] in {"downstream-resolver", "human", "release"}, f"{name}.owner is invalid")
    for field in ("requires_verification", "pre_existing"):
        _require(isinstance(finding[field], bool), f"{name}.{field} must be boolean")
    if finding.get("suggested_fix") is not None:
        _text(finding["suggested_fix"], f"{name}.suggested_fix")
    if "first_evidence" in finding:
        _text(finding["first_evidence"], f"{name}.first_evidence")
    if finding["confidence"] in {75, 100}:
        _require_first_evidence(finding, finding.get("first_evidence"), name)


def accept_review_receipt(
    receipt: dict[str, Any],
    expected_path: str | Path,
    reviewer: str,
    schema_path: str | Path = DEFAULT_SCHEMA,
) -> dict[str, Any]:
    _keys(
        receipt,
        {
            "kind",
            "path",
            "sha256",
            "schema_sha256",
            "reviewer",
            "finding_count",
            "residual_risk_count",
            "testing_gap_count",
        },
        set(),
        "review receipt",
    )
    reviewer = _validate_reviewer(reviewer, "expected reviewer")
    _require(receipt["kind"] == "code-review-result", "review receipt kind mismatch")
    _require(receipt["reviewer"] == reviewer, "review receipt reviewer mismatch")
    expected = Path(expected_path).resolve()
    _require(Path(_text(receipt["path"], "review receipt.path")).resolve() == expected, "review receipt path mismatch")

    schema, schema_digest = _load_schema(schema_path)
    document, digest = _load_json_with_digest(expected)
    validate_review_document(document, schema, reviewer)
    actual = _receipt(document, digest, schema_digest, expected)
    _require(receipt == actual, "review receipt does not match the authoritative result")

    findings = []
    sources = {}
    for index, finding in enumerate(document["findings"]):
        source_key = _source_key(reviewer, digest, index)
        findings.append(_compact_finding(finding, source_key, reviewer))
        sources[source_key] = {
            "reviewer": reviewer,
            "path": str(expected),
            "sha256": digest,
            "index": index,
        }
    return {
        "schema_version": 1,
        "receipt": actual,
        "findings": findings,
        "residual_risks": document["residual_risks"],
        "testing_gaps": document["testing_gaps"],
        "sources": sources,
    }


def accept_inline_fallback(payload: dict[str, Any], reviewer: str) -> dict[str, Any]:
    _keys(
        payload,
        {"reviewer", "findings", "residual_risks", "testing_gaps", "handoff_error"},
        set(),
        "inline fallback",
    )
    reviewer = _validate_reviewer(reviewer, "expected reviewer")
    _require(payload["reviewer"] == reviewer, "inline fallback reviewer mismatch")
    _text(payload["handoff_error"], "inline fallback.handoff_error")
    for name in ("residual_risks", "testing_gaps"):
        for index, item in enumerate(_list(payload[name], f"inline fallback.{name}")):
            _text(item, f"inline fallback.{name}[{index}]")

    findings = []
    for index, raw_finding in enumerate(_list(payload["findings"], "inline fallback.findings")):
        name = f"inline fallback.findings[{index}]"
        finding = _object(raw_finding, name)
        _validate_compact_finding(finding, name)
        item = dict(finding)
        item["reviewers"] = [reviewer]
        item["source_keys"] = []
        findings.append(item)
    return {
        "schema_version": 1,
        "reviewer": reviewer,
        "findings": findings,
        "residual_risks": payload["residual_risks"],
        "testing_gaps": payload["testing_gaps"],
        "handoff_error": payload["handoff_error"],
        "sources": {},
    }


def hydrate_findings(
    request: dict[str, Any],
    registry: dict[str, Any],
    schema_path: str | Path = DEFAULT_SCHEMA,
) -> dict[str, Any]:
    _keys(request, {"schema_version", "findings"}, set(), "hydration request")
    _require_schema_version(request["schema_version"], "hydration request")
    _keys(registry, {"schema_version", "sources"}, set(), "source registry")
    _require_schema_version(registry["schema_version"], "source registry")
    sources = _object(registry["sources"], "source registry.sources")
    schema, _ = _load_schema(schema_path)
    cache: dict[str, tuple[dict[str, Any], str]] = {}
    output = []

    for item_index, raw_item in enumerate(_list(request["findings"], "hydration request.findings")):
        item = _object(raw_item, f"hydration request.findings[{item_index}]")
        source_keys = _list(item.get("source_keys"), f"hydration request.findings[{item_index}].source_keys")
        _require(bool(source_keys), f"hydration request.findings[{item_index}].source_keys must not be empty")
        _require(len(source_keys) == len(set(source_keys)), f"hydration request.findings[{item_index}].source_keys must be unique")
        records = []
        for source_key in source_keys:
            source_key = _text(source_key, "source key")
            match = SOURCE_KEY.fullmatch(source_key)
            _require(bool(match), f"invalid source key: {source_key}")
            _require(source_key in sources, f"source key is not in the source registry: {source_key}")
            source = _object(sources[source_key], f"source registry.sources.{source_key}")
            _keys(source, {"reviewer", "path", "sha256", "index"}, set(), f"source {source_key}")
            reviewer, digest, index_text = match.groups()
            index = int(index_text)
            source_reviewer = _validate_reviewer(source["reviewer"], f"source {source_key}.reviewer")
            _require(source_reviewer == reviewer, f"source reviewer does not match key: {source_key}")
            _require(_text(source["sha256"], f"source {source_key}.sha256") == digest, f"source digest does not match key: {source_key}")
            _require(
                isinstance(source["index"], int)
                and not isinstance(source["index"], bool)
                and source["index"] == index,
                f"source index does not match key: {source_key}",
            )
            path = _text(source["path"], f"source {source_key}.path")
            if path not in cache:
                document, actual_digest = _load_json_with_digest(path)
                validate_review_document(document, schema, reviewer)
                cache[path] = document, actual_digest
            document, actual_digest = cache[path]
            _require(document["reviewer"] == reviewer, f"source reviewer does not match file: {source_key}")
            _require(actual_digest == digest, f"source digest mismatch: {source_key}")
            _require(index < len(document["findings"]), f"source index is out of range: {source_key}")
            records.append({"source_key": source_key, "reviewer": reviewer, "finding": document["findings"][index]})
        output.append({"source_keys": source_keys, "records": records})
    return {"schema_version": 1, "findings": output}


def _print(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    seal = subparsers.add_parser("seal-review")
    seal.add_argument("draft")
    seal.add_argument("output")
    seal.add_argument("--reviewer", required=True)
    seal.add_argument("--schema", default=str(DEFAULT_SCHEMA))

    accept = subparsers.add_parser("accept-review")
    accept.add_argument("receipt")
    accept.add_argument("--expected", required=True)
    accept.add_argument("--reviewer", required=True)
    accept.add_argument("--schema", default=str(DEFAULT_SCHEMA))

    inline = subparsers.add_parser("accept-inline")
    inline.add_argument("payload")
    inline.add_argument("--reviewer", required=True)

    hydrate = subparsers.add_parser("hydrate-findings")
    hydrate.add_argument("request")
    hydrate.add_argument("--sources", required=True)
    hydrate.add_argument("--schema", default=str(DEFAULT_SCHEMA))

    args = parser.parse_args(argv)
    try:
        if args.command == "seal-review":
            result = seal_review_file(args.draft, args.output, args.reviewer, args.schema)
        elif args.command == "accept-review":
            receipt = _load_json(args.receipt)
            result = accept_review_receipt(receipt, args.expected, args.reviewer, args.schema)
        elif args.command == "accept-inline":
            payload = _load_json(args.payload)
            result = accept_inline_fallback(payload, args.reviewer)
        else:
            request = _load_json(args.request)
            registry = _load_json(args.sources)
            result = hydrate_findings(request, registry, args.schema)
        _print(result)
        return 0
    except ArtifactError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
