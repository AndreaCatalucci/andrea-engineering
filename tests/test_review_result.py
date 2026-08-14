import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "ae-code-review" / "scripts" / "review-result.py"
SCHEMA = ROOT / "skills" / "ae-code-review" / "references" / "findings-schema.json"
SPEC = importlib.util.spec_from_file_location("review_result", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def finding(**overrides):
    value = {
        "title": "Rejects valid empty review",
        "severity": "P1",
        "file": "skills/ae-code-review/scripts/review-result.py",
        "line": 42,
        "why_it_matters": "A valid reviewer result is discarded, so the final report silently loses review coverage.",
        "autofix_class": "gated_auto",
        "owner": "downstream-resolver",
        "requires_verification": True,
        "suggested_fix": "Accept an empty findings array while preserving reviewer coverage.",
        "confidence": 75,
        "evidence": [
            "skills/ae-code-review/scripts/review-result.py:42 -- findings = document['findings']"
        ],
        "pre_existing": False,
    }
    value.update(overrides)
    return value


def review_document(reviewer="core", findings=None):
    return {
        "reviewer": reviewer,
        "findings": [] if findings is None else findings,
        "residual_risks": [],
        "testing_gaps": [],
    }


class ReviewArtifactTest(unittest.TestCase):
    def write_json(self, directory, name, document):
        path = Path(directory) / name
        path.write_text(json.dumps(document), encoding="utf-8")
        return path

    def seal(self, directory, document, reviewer="core", name="review"):
        draft = self.write_json(directory, f"{name}-draft.json", document)
        output = Path(directory) / f"{name}.json"
        receipt = MODULE.seal_review_file(draft, output, reviewer, SCHEMA)
        return output, receipt

    def test_valid_empty_review_seals_and_accepts(self):
        with tempfile.TemporaryDirectory() as directory:
            output, receipt = self.seal(directory, review_document())
            accepted = MODULE.accept_review_receipt(receipt, output, "core", SCHEMA)

            self.assertEqual(receipt["kind"], "code-review-result")
            self.assertEqual(receipt["finding_count"], 0)
            self.assertEqual(accepted["findings"], [])
            self.assertEqual(accepted["sources"], {})
            self.assertEqual(accepted["receipt"], receipt)

    def test_valid_finding_projects_stable_compact_source(self):
        with tempfile.TemporaryDirectory() as directory:
            output, receipt = self.seal(directory, review_document(findings=[finding()]))
            first = MODULE.accept_review_receipt(receipt, output, "core", SCHEMA)
            second = MODULE.accept_review_receipt(receipt, output, "core", SCHEMA)

            self.assertEqual(first, second)
            compact = first["findings"][0]
            self.assertNotIn("why_it_matters", compact)
            self.assertNotIn("evidence", compact)
            self.assertIn("first_evidence", compact)
            self.assertEqual(compact["reviewers"], ["core"])
            self.assertEqual(len(compact["source_keys"]), 1)
            source_key = compact["source_keys"][0]
            self.assertRegex(source_key, r"^core:[0-9a-f]{64}:0$")
            self.assertEqual(first["sources"][source_key]["path"], str(output.resolve()))

    def test_schema_and_semantic_failures_are_rejected(self):
        failures = {
            "missing": review_document(findings=[finding()]),
            "severity": review_document(findings=[finding(severity="high")]),
            "confidence": review_document(findings=[finding(confidence=80)]),
            "evidence": review_document(findings=[finding(evidence=[])]),
            "quote": review_document(findings=[finding(evidence=["some other line"])]),
        }
        del failures["missing"]["findings"][0]["why_it_matters"]

        for name, document in failures.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                draft = self.write_json(directory, "draft.json", document)
                with self.assertRaises(MODULE.ArtifactError):
                    MODULE.seal_review_file(draft, Path(directory) / "result.json", "core", SCHEMA)

        wrong_line = review_document(
            findings=[
                finding(
                    line=4,
                    evidence=[
                        "skills/ae-code-review/scripts/review-result.py:42 -- wrong line"
                    ],
                )
            ]
        )
        with tempfile.TemporaryDirectory() as directory:
            draft = self.write_json(directory, "wrong-line.json", wrong_line)
            with self.assertRaisesRegex(MODULE.ArtifactError, "must quote"):
                MODULE.seal_review_file(draft, Path(directory) / "result.json", "core", SCHEMA)

    def test_reviewer_and_extra_fields_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            wrong_reviewer = review_document(reviewer="security")
            draft = self.write_json(directory, "wrong-reviewer.json", wrong_reviewer)
            with self.assertRaisesRegex(MODULE.ArtifactError, "reviewer"):
                MODULE.seal_review_file(draft, Path(directory) / "result.json", "core", SCHEMA)

            extra = review_document()
            extra["unexpected"] = True
            draft = self.write_json(directory, "extra.json", extra)
            with self.assertRaisesRegex(MODULE.ArtifactError, "unsupported field"):
                MODULE.seal_review_file(draft, Path(directory) / "result.json", "core", SCHEMA)

    def test_parent_rejects_wrong_path_before_read_and_digest_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            output, receipt = self.seal(directory, review_document(findings=[finding()]))

            wrong_path = dict(receipt)
            wrong_path["path"] = str(Path(directory) / "missing.json")
            with self.assertRaisesRegex(MODULE.ArtifactError, "path"):
                MODULE.accept_review_receipt(wrong_path, output, "core", SCHEMA)

            output.write_text(output.read_text(encoding="utf-8") + " ", encoding="utf-8")
            with self.assertRaisesRegex(MODULE.ArtifactError, "receipt"):
                MODULE.accept_review_receipt(receipt, output, "core", SCHEMA)

    def test_unsupported_schema_features_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
            schema["properties"]["reviewer"]["oneOf"] = [{"type": "string"}]
            schema_path = self.write_json(directory, "schema.json", schema)
            draft = self.write_json(directory, "review.json", review_document())
            with self.assertRaisesRegex(MODULE.ArtifactError, "unsupported schema keyword.*oneOf"):
                MODULE.seal_review_file(draft, Path(directory) / "result.json", "core", schema_path)

    def test_inline_fallback_preserves_old_compact_shape_and_quote_gate(self):
        compact = {
            key: value
            for key, value in finding().items()
            if key not in {"why_it_matters", "evidence"}
        }
        compact["first_evidence"] = finding()["evidence"][0]
        payload = {
            "reviewer": "core",
            "findings": [compact],
            "residual_risks": [],
            "testing_gaps": [],
            "handoff_error": "authoritative write failed",
        }
        accepted = MODULE.accept_inline_fallback(payload, "core")
        self.assertEqual(accepted["findings"][0]["source_keys"], [])
        self.assertEqual(accepted["findings"][0]["reviewers"], ["core"])

        del payload["findings"][0]["first_evidence"]
        with self.assertRaisesRegex(MODULE.ArtifactError, "first_evidence"):
            MODULE.accept_inline_fallback(payload, "core")

        payload["findings"][0]["first_evidence"] = finding()["evidence"][0]
        payload["findings"][0]["line"] = 4
        with self.assertRaisesRegex(MODULE.ArtifactError, "must quote"):
            MODULE.accept_inline_fallback(payload, "core")

        payload["findings"][0]["line"] = 42
        payload["findings"][0]["title"] = "x" * 101
        with self.assertRaisesRegex(MODULE.ArtifactError, "title is too long"):
            MODULE.accept_inline_fallback(payload, "core")

        payload["findings"][0]["title"] = "Valid title"
        payload["findings"][0]["confidence"] = 50
        payload["findings"][0]["first_evidence"] = 42
        with self.assertRaisesRegex(MODULE.ArtifactError, "first_evidence"):
            MODULE.accept_inline_fallback(payload, "core")

    def test_normal_and_inline_compact_fields_stay_in_parity(self):
        with tempfile.TemporaryDirectory() as directory:
            output, receipt = self.seal(directory, review_document(findings=[finding()]))
            normal = MODULE.accept_review_receipt(receipt, output, "core", SCHEMA)["findings"][0]
            inline_finding = {
                key: value
                for key, value in normal.items()
                if key not in {"reviewers", "source_keys"}
            }
            inline = MODULE.accept_inline_fallback(
                {
                    "reviewer": "core",
                    "findings": [inline_finding],
                    "residual_risks": [],
                    "testing_gaps": [],
                    "handoff_error": "write failed",
                },
                "core",
            )["findings"][0]
            self.assertEqual(set(normal), set(inline))

    def test_atomic_write_failure_leaves_no_authoritative_result(self):
        with tempfile.TemporaryDirectory() as directory:
            draft = self.write_json(directory, "draft.json", review_document())
            output = Path(directory) / "result.json"
            with mock.patch.object(MODULE.os, "replace", side_effect=OSError("disk full")):
                with self.assertRaisesRegex(MODULE.ArtifactError, "write"):
                    MODULE.seal_review_file(draft, output, "core", SCHEMA)
            self.assertFalse(output.exists())

    def test_hydration_reloads_full_records_from_duplicate_lineage(self):
        with tempfile.TemporaryDirectory() as directory:
            core_output, core_receipt = self.seal(
                directory,
                review_document("core", [finding()]),
                "core",
                "core",
            )
            api_finding = finding(
                evidence=[
                    "skills/ae-code-review/scripts/review-result.py:42 -- findings = document['findings']",
                    "tests/test_review_result.py:1 -- regression coverage",
                ]
            )
            api_output, api_receipt = self.seal(
                directory,
                review_document("api-contract", [api_finding]),
                "api-contract",
                "api",
            )
            core = MODULE.accept_review_receipt(core_receipt, core_output, "core", SCHEMA)
            api = MODULE.accept_review_receipt(api_receipt, api_output, "api-contract", SCHEMA)
            registry = {**core["sources"], **api["sources"]}
            source_keys = core["findings"][0]["source_keys"] + api["findings"][0]["source_keys"]

            hydrated = MODULE.hydrate_findings(
                {"schema_version": 1, "findings": [{"source_keys": source_keys}]},
                {"schema_version": 1, "sources": registry},
                SCHEMA,
            )

            records = hydrated["findings"][0]["records"]
            self.assertEqual([record["reviewer"] for record in records], ["core", "api-contract"])
            self.assertIn("why_it_matters", records[0]["finding"])
            self.assertEqual(len(records[1]["finding"]["evidence"]), 2)

    def test_hydration_rejects_boolean_index_and_cached_reviewer_conflict(self):
        with tempfile.TemporaryDirectory() as directory:
            output, receipt = self.seal(directory, review_document(findings=[finding()]))
            accepted = MODULE.accept_review_receipt(receipt, output, "core", SCHEMA)
            source_key, source = next(iter(accepted["sources"].items()))
            request = {"schema_version": 1, "findings": [{"source_keys": [source_key]}]}

            boolean_source = dict(source)
            boolean_source["index"] = True
            with self.assertRaisesRegex(MODULE.ArtifactError, "source index"):
                MODULE.hydrate_findings(
                    request,
                    {"schema_version": 1, "sources": {source_key: boolean_source}},
                    SCHEMA,
                )

            with self.assertRaisesRegex(MODULE.ArtifactError, "hydration request schema_version"):
                MODULE.hydrate_findings(
                    {"schema_version": True, "findings": [{"source_keys": [source_key]}]},
                    {"schema_version": 1, "sources": {source_key: source}},
                    SCHEMA,
                )
            with self.assertRaisesRegex(MODULE.ArtifactError, "source registry schema_version"):
                MODULE.hydrate_findings(
                    request,
                    {"schema_version": True, "sources": {source_key: source}},
                    SCHEMA,
                )

            digest = receipt["sha256"]
            conflicting_key = f"api-contract:{digest}:0"
            conflicting_source = dict(source, reviewer="api-contract")
            with self.assertRaisesRegex(MODULE.ArtifactError, "reviewer"):
                MODULE.hydrate_findings(
                    {
                        "schema_version": 1,
                        "findings": [{"source_keys": [source_key, conflicting_key]}],
                    },
                    {
                        "schema_version": 1,
                        "sources": {
                            source_key: source,
                            conflicting_key: conflicting_source,
                        },
                    },
                    SCHEMA,
                )

    def test_instruction_packet_is_complete_and_within_budget(self):
        template = (
            ROOT / "skills" / "ae-code-review" / "references" / "subagent-template.md"
        ).read_text(encoding="utf-8")
        for field in (
            "protocol_path",
            "persona_path",
            "scope_rules_path",
            "schema_path",
            "helper_path",
            "run_id",
            "reviewer",
            "intent",
            "requirements",
            "pr_context",
            "project_orientation",
            "governing_instructions",
            "known_patterns",
            "files_path",
            "diff_path",
            "draft_path",
            "result_path",
        ):
            self.assertIn(field, template)
        self.assertIn('fork_turns="none"', template)
        self.assertIn("receipt handoff always win", template)
        scope_rules = (
            ROOT / "skills" / "ae-code-review" / "references" / "diff-scope.md"
        ).read_text(encoding="utf-8")
        self.assertLessEqual(len(template.split()) + len(scope_rules.split()), 1500)

    def test_merge_validator_and_agent_output_keep_existing_guards(self):
        merge = (
            ROOT / "skills" / "ae-code-review" / "references" / "merge-apply-rules.md"
        ).read_text(encoding="utf-8")
        validator = (
            ROOT / "skills" / "ae-code-review" / "references" / "validator-template.md"
        ).read_text(encoding="utf-8")
        output = (
            ROOT / "skills" / "ae-code-review" / "references" / "review-output-template.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "source_keys",
            "source-registry.json",
            "hydrate-findings",
            "one repair",
            "write failure",
            "reviewer-side validation failure",
            "P0/P1",
            "testing_gaps",
            "residual_risks",
        ):
            self.assertIn(phrase, merge)
        self.assertIn('fork_turns="none"', validator)
        self.assertIn("validator-packet.json", validator)
        for field in (
            '"status"',
            '"verdict"',
            '"scope"',
            '"intent"',
            '"reviewers"',
            '"findings"',
            '"actionable_findings"',
            '"result_path"',
            '"run_id"',
        ):
            self.assertIn(field, output)


if __name__ == "__main__":
    unittest.main()
