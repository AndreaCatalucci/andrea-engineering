#!/usr/bin/env python3
"""Validate and seal compact ce-ideate candidate and verdict files."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DISPATCH_CONTRACT = ROOT / "references" / "dispatch-contract.json"
BASIS_PREFIXES = ("direct:", "external:", "reasoned:")
ASSIGNMENT_KINDS = {"frame", "theme", "recovery", "universal"}
ORIGINS = {"original", "recovery", "deduped", "synthesis"}
VERDICTS = {"sound", "weak", "refuted"}
SOURCE_KEY = re.compile(r"^(frame|theme|recovery|universal):([^:]+):([0-9a-f]{64}):(\d+)$")


class ArtifactError(ValueError):
    """A result file failed structural or integrity validation."""


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
    return _load_json_with_digest(path)[0]


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
        raise ArtifactError(f"authoritative artifact write failed: {error}") from error
    return hashlib.sha256(data).hexdigest()


def _validate_text_list(value: Any, name: str) -> list[str]:
    items = _list(value, name)
    for index, item in enumerate(items):
        _text(item, f"{name}[{index}]")
    _require(len(items) == len(set(items)), f"{name} must be unique")
    return items


def _validate_assignment(value: Any, name: str = "assignment") -> tuple[dict[str, Any], list[str], dict[str, tuple[int, int]]]:
    assignment = _object(value, name)
    _keys(assignment, {"kind", "assignment_id", "areas", "buckets"}, set(), name)
    kind = _text(assignment["kind"], f"{name}.kind")
    _require(kind in ASSIGNMENT_KINDS, f"unsupported assignment kind: {kind}")
    assignment_id = _text(assignment["assignment_id"], f"{name}.assignment_id")
    _require(":" not in assignment_id, "assignment_id must not contain ':'")

    areas = _validate_text_list(assignment["areas"], f"{name}.areas")
    buckets = _list(assignment["buckets"], f"{name}.buckets")
    _require(bool(buckets), f"{name} requires at least one bucket")
    bucket_ids: list[str] = []
    quotas: dict[str, tuple[int, int]] = {}
    for index, raw_bucket in enumerate(buckets):
        bucket_name = f"{name}.buckets[{index}]"
        bucket = _object(raw_bucket, bucket_name)
        _keys(bucket, {"id", "minimum", "maximum"}, set(), bucket_name)
        bucket_id = _text(bucket["id"], f"{bucket_name}.id")
        minimum, maximum = bucket["minimum"], bucket["maximum"]
        _require(
            isinstance(minimum, int) and not isinstance(minimum, bool) and minimum >= 1,
            f"{bucket_id} minimum must be >= 1",
        )
        _require(
            isinstance(maximum, int) and not isinstance(maximum, bool) and maximum >= minimum,
            f"{bucket_id} maximum must be >= minimum",
        )
        bucket_ids.append(bucket_id)
        quotas[bucket_id] = (minimum, maximum)
    _require(len(bucket_ids) == len(set(bucket_ids)), "bucket ids must be unique")
    return assignment, areas, quotas


def _load_expected_assignment(path: str | Path) -> tuple[dict[str, Any], Path]:
    document = _load_json(path)
    _keys(document, {"schema_version", "assignment", "result_path"}, set(), "expected assignment")
    _require(document["schema_version"] == 1, "unsupported expected assignment schema_version")
    assignment, _, _ = _validate_assignment(document["assignment"], "expected assignment.assignment")
    result_path = Path(_text(document["result_path"], "expected assignment.result_path"))
    _require(result_path.is_absolute(), "expected assignment.result_path must be absolute")
    return assignment, result_path.resolve()


def _require_expected_assignment(
    document: dict[str, Any],
    result_path: str | Path,
    expected_path: str | Path,
) -> None:
    expected_assignment, expected_result_path = _load_expected_assignment(expected_path)
    _require(document["assignment"] == expected_assignment, "candidate assignment does not match expected assignment")
    _require(
        Path(result_path).resolve() == expected_result_path,
        "candidate result path does not match expected assignment",
    )


def validate_candidate_document(document: dict[str, Any]) -> None:
    _keys(document, {"schema_version", "assignment", "candidates"}, set(), "candidate document")
    _require(document["schema_version"] == 1, "unsupported candidate schema_version")
    _, areas, quotas = _validate_assignment(document["assignment"])

    candidates = _list(document["candidates"], "candidates")
    counts = {bucket_id: 0 for bucket_id in quotas}
    for index, raw_candidate in enumerate(candidates):
        candidate = _object(raw_candidate, f"candidates[{index}]")
        _keys(candidate, {"assignment", "title", "move", "basis", "significance"}, {"area"}, f"candidates[{index}]")
        bucket_id = _text(candidate["assignment"], f"candidates[{index}].assignment")
        _require(bucket_id in counts, f"candidates[{index}] references unknown assignment {bucket_id}")
        counts[bucket_id] += 1
        for field in ("title", "move", "basis", "significance"):
            _text(candidate[field], f"candidates[{index}].{field}")
        _require(candidate["basis"].startswith(BASIS_PREFIXES), f"candidates[{index}].basis requires direct:, external:, or reasoned:")
        if areas:
            area = _text(candidate.get("area"), f"candidates[{index}].area")
            _require(area in areas, f"candidates[{index}].area is not declared")
        else:
            _require("area" not in candidate, f"candidates[{index}] must omit area for an atomic subject")

    for bucket_id, count in counts.items():
        minimum, maximum = quotas[bucket_id]
        _require(count >= minimum, f"assignment {bucket_id} has {count} candidates; minimum is {minimum}")
        _require(count <= maximum, f"assignment {bucket_id} has {count} candidates; maximum is {maximum}")


def _candidate_receipt(document: dict[str, Any], digest: str, path: str | Path) -> dict[str, Any]:
    counts = Counter(candidate["assignment"] for candidate in document["candidates"])
    return {
        "kind": "ideation-candidates",
        "path": str(Path(path).resolve()),
        "sha256": digest,
        "assignment_id": document["assignment"]["assignment_id"],
        "candidate_count": len(document["candidates"]),
        "counts": dict(sorted(counts.items())),
    }


def candidate_receipt(path: str | Path) -> dict[str, Any]:
    document, digest = _load_json_with_digest(path)
    validate_candidate_document(document)
    return _candidate_receipt(document, digest, path)


def seal_candidate_file(
    draft_path: str | Path,
    output_path: str | Path,
    expected_path: str | Path,
) -> dict[str, Any]:
    document = _load_json(draft_path)
    validate_candidate_document(document)
    _require_expected_assignment(document, output_path, expected_path)
    digest = _seal(document, output_path)
    return _candidate_receipt(document, digest, output_path)


def make_candidate_id(parents: list[str], title: str, move: str) -> str:
    material = json.dumps([sorted(parents), title.strip(), move.strip()], ensure_ascii=False, separators=(",", ":"))
    return "cand-" + hashlib.sha256(material.encode()).hexdigest()[:20]


def _project_candidates(document: dict[str, Any], digest: str) -> list[dict[str, Any]]:
    assignment = document["assignment"]
    projected = []
    for index, candidate in enumerate(document["candidates"]):
        source_key = f"{assignment['kind']}:{assignment['assignment_id']}:{digest}:{index}"
        item = dict(candidate)
        item.update(
            {
                "candidate_id": make_candidate_id([source_key], candidate["title"], candidate["move"]),
                "origin": "recovery" if assignment["kind"] == "recovery" else "original",
                "parents": [source_key],
            }
        )
        projected.append(item)
    return projected


def project_candidates(path: str | Path) -> list[dict[str, Any]]:
    document, digest = _load_json_with_digest(path)
    validate_candidate_document(document)
    return _project_candidates(document, digest)


def accept_candidate_receipt(receipt: dict[str, Any], expected_path: str | Path) -> dict[str, Any]:
    _keys(
        receipt,
        {"kind", "path", "sha256", "assignment_id", "candidate_count", "counts"},
        set(),
        "candidate receipt",
    )
    _require(receipt["kind"] == "ideation-candidates", "candidate receipt kind mismatch")
    path = _text(receipt["path"], "candidate receipt.path")
    expected_assignment, expected_result_path = _load_expected_assignment(expected_path)
    _require(
        Path(path).resolve() == expected_result_path,
        "candidate result path does not match expected assignment",
    )
    document, digest = _load_json_with_digest(path)
    validate_candidate_document(document)
    _require(document["assignment"] == expected_assignment, "candidate assignment does not match expected assignment")
    actual = _candidate_receipt(document, digest, path)
    _require(receipt == actual, "candidate receipt does not match the authoritative file")
    return {"receipt": actual, "schema_version": 1, "candidates": _project_candidates(document, digest)}


def validate_consolidated_document(
    document: dict[str, Any],
    source_keys: set[str] | None = None,
) -> None:
    _keys(document, {"schema_version", "areas", "candidates"}, set(), "consolidated document")
    _require(document["schema_version"] == 1, "unsupported consolidated schema_version")
    areas = _validate_text_list(document["areas"], "consolidated areas")
    candidates = _list(document["candidates"], "candidates")
    _require(bool(candidates), "consolidated candidates must not be empty")
    ids: list[str] = []
    for index, raw_candidate in enumerate(candidates):
        candidate = _object(raw_candidate, f"candidates[{index}]")
        required = {"candidate_id", "origin", "parents", "assignment", "title", "move", "basis", "significance"}
        optional = set()
        if areas:
            required.add("area")
        _keys(candidate, required, optional, f"candidates[{index}]")
        for field in ("candidate_id", "origin", "assignment", "title", "move", "basis", "significance"):
            _text(candidate[field], f"candidates[{index}].{field}")
        _require(candidate["origin"] in ORIGINS, f"candidates[{index}] has unsupported origin")
        _require(candidate["basis"].startswith(BASIS_PREFIXES), f"candidates[{index}].basis is invalid")
        if areas:
            area = _text(candidate["area"], f"candidates[{index}].area")
            _require(area in areas, f"candidates[{index}].area is not declared")
        parents = _list(candidate["parents"], f"candidates[{index}].parents")
        _require(bool(parents), f"candidates[{index}].parents must not be empty")
        for parent in parents:
            _text(parent, f"candidates[{index}].parents entry")
            _require(bool(SOURCE_KEY.fullmatch(parent)), f"candidates[{index}] has invalid parent source key")
            if source_keys is not None:
                _require(parent in source_keys, f"candidates[{index}] parent is not in the source registry")
        _require(len(parents) == len(set(parents)), f"candidates[{index}].parents must be unique")
        if candidate["origin"] in {"deduped", "synthesis"}:
            _require(len(parents) >= 2, f"{candidate['origin']} candidate requires at least two parents")
        else:
            _require(len(parents) == 1, f"{candidate['origin']} candidate requires exactly one parent")
        expected = make_candidate_id(parents, candidate["title"], candidate["move"])
        _require(candidate["candidate_id"] == expected, f"candidates[{index}].candidate_id does not match lineage")
        ids.append(candidate["candidate_id"])
    _require(len(ids) == len(set(ids)), "candidate_id values must be unique")


def assign_missing_candidate_ids(document: dict[str, Any]) -> None:
    _keys(document, {"schema_version", "areas", "candidates"}, set(), "consolidated draft")
    for index, raw_candidate in enumerate(_list(document["candidates"], "candidates")):
        candidate = _object(raw_candidate, f"candidates[{index}]")
        if "candidate_id" not in candidate:
            parents = _list(candidate.get("parents"), f"candidates[{index}].parents")
            title = _text(candidate.get("title"), f"candidates[{index}].title")
            move = _text(candidate.get("move"), f"candidates[{index}].move")
            candidate["candidate_id"] = make_candidate_id(parents, title, move)


def _consolidated_receipt(document: dict[str, Any], digest: str, path: str | Path) -> dict[str, Any]:
    return {
        "kind": "ideation-consolidated",
        "path": str(Path(path).resolve()),
        "sha256": digest,
        "candidate_count": len(document["candidates"]),
    }


def consolidated_receipt(path: str | Path) -> dict[str, Any]:
    document, digest = _load_json_with_digest(path)
    validate_consolidated_document(document)
    return _consolidated_receipt(document, digest, path)


def _load_source_registry(path: str | Path) -> tuple[list[str], set[str]]:
    document = _load_json(path)
    _keys(document, {"schema_version", "areas", "source_keys"}, set(), "source registry")
    _require(document["schema_version"] == 1, "unsupported source registry schema_version")
    areas = _validate_text_list(document["areas"], "source registry.areas")
    source_keys = _validate_text_list(document["source_keys"], "source registry.source_keys")
    _require(bool(source_keys), "source registry.source_keys must not be empty")
    for source_key in source_keys:
        _require(bool(SOURCE_KEY.fullmatch(source_key)), "source registry contains an invalid source key")
    return areas, set(source_keys)


def seal_consolidated_file(
    draft_path: str | Path,
    output_path: str | Path,
    source_registry_path: str | Path,
) -> dict[str, Any]:
    document = _load_json(draft_path)
    areas, source_keys = _load_source_registry(source_registry_path)
    assign_missing_candidate_ids(document)
    validate_consolidated_document(document, source_keys)
    _require(document["areas"] == areas, "consolidated areas do not match the source registry")
    digest = _seal(document, output_path)
    return _consolidated_receipt(document, digest, output_path)


def _validate_verdict_document(
    document: dict[str, Any],
    candidates: dict[str, Any],
    candidate_digest: str,
) -> None:
    _keys(document, {"schema_version", "candidate_file_sha256", "verdicts"}, set(), "verdict document")
    _require(document["schema_version"] == 1, "unsupported verdict schema_version")
    validate_consolidated_document(candidates)
    _require(document["candidate_file_sha256"] == candidate_digest, "verdict candidate digest mismatch")
    expected_ids = {candidate["candidate_id"] for candidate in candidates["candidates"]}
    seen: set[str] = set()
    for index, raw_verdict in enumerate(_list(document["verdicts"], "verdicts")):
        verdict = _object(raw_verdict, f"verdicts[{index}]")
        _keys(verdict, {"candidate_id", "verdict", "reason"}, set(), f"verdicts[{index}]")
        candidate_id = _text(verdict["candidate_id"], f"verdicts[{index}].candidate_id")
        _require(candidate_id in expected_ids, f"verdicts[{index}] references unknown candidate_id")
        _require(candidate_id not in seen, f"duplicate verdict for {candidate_id}")
        seen.add(candidate_id)
        _require(verdict["verdict"] in VERDICTS, f"verdicts[{index}] has unsupported verdict")
        _text(verdict["reason"], f"verdicts[{index}].reason")
    missing = expected_ids - seen
    _require(not missing, f"verdict coverage is incomplete: {len(missing)} candidates missing")


def validate_verdict_document(document: dict[str, Any], candidate_path: str | Path) -> None:
    candidates, candidate_digest = _load_json_with_digest(candidate_path)
    _validate_verdict_document(document, candidates, candidate_digest)


def _verdict_receipt(
    document: dict[str, Any],
    digest: str,
    path: str | Path,
    candidate_path: str | Path,
) -> dict[str, Any]:
    return {
        "kind": "ideation-verdicts",
        "path": str(Path(path).resolve()),
        "sha256": digest,
        "candidate_path": str(Path(candidate_path).resolve()),
        "candidate_file_sha256": document["candidate_file_sha256"],
        "verdict_count": len(document["verdicts"]),
    }


def verdict_receipt(path: str | Path, candidate_path: str | Path) -> dict[str, Any]:
    document, digest = _load_json_with_digest(path)
    candidates, candidate_digest = _load_json_with_digest(candidate_path)
    _validate_verdict_document(document, candidates, candidate_digest)
    return _verdict_receipt(document, digest, path, candidate_path)


def seal_verdict_file(draft_path: str | Path, output_path: str | Path, candidate_path: str | Path) -> dict[str, Any]:
    document = _load_json(draft_path)
    candidates, candidate_digest = _load_json_with_digest(candidate_path)
    _validate_verdict_document(document, candidates, candidate_digest)
    digest = _seal(document, output_path)
    return _verdict_receipt(document, digest, output_path, candidate_path)


def load_dispatch_contract() -> dict[str, Any]:
    document = _load_json(DISPATCH_CONTRACT)
    _keys(document, {"schema_version", "modes"}, set(), "dispatch contract")
    _require(document["schema_version"] == 1, "unsupported dispatch schema_version")
    modes = _object(document["modes"], "dispatch modes")
    required = {"default-software", "issue-tracker", "surprise-me", "go-deep", "non-software-quick", "non-software-standard", "non-software-full", "recovery"}
    _require(required == set(modes), "dispatch modes are incomplete or unsupported")
    for mode_name, raw_mode in modes.items():
        mode = _object(raw_mode, f"dispatch mode {mode_name}")
        if "agents" in mode:
            agents = _list(mode["agents"], f"dispatch mode {mode_name}.agents")
            assignments: list[str] = []
            for index, raw_agent in enumerate(agents):
                agent = _list(raw_agent, f"dispatch mode {mode_name}.agents[{index}]")
                _require(bool(agent), f"dispatch mode {mode_name} contains an empty agent assignment")
                for assignment in agent:
                    assignments.append(_text(assignment, f"dispatch mode {mode_name} assignment"))
            _require(len(assignments) == len(set(assignments)), f"dispatch mode {mode_name} repeats an assignment")
        for quota_name in ("candidate_quota", "survivor_quota", "dynamic_assignments"):
            if quota_name in mode:
                quota = _list(mode[quota_name], f"dispatch mode {mode_name}.{quota_name}")
                _require(len(quota) == 2, f"dispatch mode {mode_name}.{quota_name} requires two bounds")
                lower, upper = quota
                _require(
                    isinstance(lower, int) and not isinstance(lower, bool) and lower >= 0,
                    f"dispatch mode {mode_name}.{quota_name} lower bound is invalid",
                )
                _require(
                    isinstance(upper, int) and not isinstance(upper, bool) and upper >= lower,
                    f"dispatch mode {mode_name}.{quota_name} upper bound is invalid",
                )
    return document


def _print(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    seal_candidates = subparsers.add_parser("seal-candidates")
    seal_candidates.add_argument("draft")
    seal_candidates.add_argument("output")
    seal_candidates.add_argument("--expected", required=True)
    seal_consolidated = subparsers.add_parser("seal-consolidated")
    seal_consolidated.add_argument("draft")
    seal_consolidated.add_argument("output")
    seal_consolidated.add_argument("--sources", required=True)
    receipt_candidates = subparsers.add_parser("receipt-candidates")
    receipt_candidates.add_argument("path")
    accept_candidates = subparsers.add_parser("accept-candidates")
    accept_candidates.add_argument("receipt")
    accept_candidates.add_argument("--expected", required=True)
    receipt_consolidated = subparsers.add_parser("receipt-consolidated")
    receipt_consolidated.add_argument("path")
    project = subparsers.add_parser("project-candidates")
    project.add_argument("path")
    seal_verdicts = subparsers.add_parser("seal-verdicts")
    seal_verdicts.add_argument("draft")
    seal_verdicts.add_argument("output")
    seal_verdicts.add_argument("--candidates", required=True)
    receipt_verdicts = subparsers.add_parser("receipt-verdicts")
    receipt_verdicts.add_argument("path")
    receipt_verdicts.add_argument("--candidates", required=True)
    subparsers.add_parser("dispatch-contract")
    args = parser.parse_args(argv)
    try:
        if args.command == "seal-candidates":
            result = seal_candidate_file(args.draft, args.output, args.expected)
        elif args.command == "receipt-candidates":
            result = candidate_receipt(args.path)
        elif args.command == "accept-candidates":
            result = accept_candidate_receipt(_load_json(args.receipt), args.expected)
        elif args.command == "receipt-consolidated":
            result = consolidated_receipt(args.path)
        elif args.command == "project-candidates":
            result = {"schema_version": 1, "candidates": project_candidates(args.path)}
        elif args.command == "seal-consolidated":
            result = seal_consolidated_file(args.draft, args.output, args.sources)
        elif args.command == "seal-verdicts":
            result = seal_verdict_file(args.draft, args.output, args.candidates)
        elif args.command == "receipt-verdicts":
            result = verdict_receipt(args.path, args.candidates)
        else:
            result = load_dispatch_contract()
        _print(result)
        return 0
    except ArtifactError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
