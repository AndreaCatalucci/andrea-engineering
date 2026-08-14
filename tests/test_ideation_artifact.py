import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "ae-ideate" / "scripts" / "ideation-artifact.py"
SPEC = importlib.util.spec_from_file_location("ideation_artifact", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def candidate_document(*, areas=None, paired=False):
    areas = [] if areas is None else areas
    buckets = [{"id": "pain", "minimum": 1, "maximum": 2}]
    candidates = [
        {
            "assignment": "pain",
            "title": "Remove the queue",
            "move": "Process the smallest safe unit immediately.",
            "basis": "direct: workflow.py:42 serializes every request",
            "significance": "Removes the main wait state.",
        }
    ]
    if paired:
        buckets.append({"id": "constraint", "minimum": 1, "maximum": 2})
        candidates.append(
            {
                "assignment": "constraint",
                "title": "Zero-state operation",
                "move": "Make the workflow useful before setup completes.",
                "basis": "reasoned: removing setup exposes the smallest useful core",
                "significance": "Cuts time to first value.",
            }
        )
    if areas:
        for candidate in candidates:
            candidate["area"] = areas[0]
    return {
        "schema_version": 1,
        "assignment": {
            "kind": "frame",
            "assignment_id": "default-01",
            "areas": areas,
            "buckets": buckets,
        },
        "candidates": candidates,
    }


class IdeationArtifactTest(unittest.TestCase):
    def write_json(self, directory, name, document):
        path = Path(directory) / name
        path.write_text(json.dumps(document), encoding="utf-8")
        return path

    def write_expected(self, directory, name, document, result_path):
        return self.write_json(
            directory,
            name,
            {
                "schema_version": 1,
                "assignment": document["assignment"],
                "result_path": str(Path(result_path).resolve()),
            },
        )

    def write_sources(self, directory, name, areas, candidates):
        source_keys = sorted(
            {
                parent
                for candidate in candidates
                for parent in candidate["parents"]
            }
        )
        return self.write_json(
            directory,
            name,
            {"schema_version": 1, "areas": areas, "source_keys": source_keys},
        )

    def document_for_buckets(self, *, kind, assignment_id, bucket_ids, minimum, maximum):
        return {
            "schema_version": 1,
            "assignment": {
                "kind": kind,
                "assignment_id": assignment_id,
                "areas": [],
                "buckets": [
                    {"id": bucket_id, "minimum": minimum, "maximum": maximum}
                    for bucket_id in bucket_ids
                ],
            },
            "candidates": [
                {
                    "assignment": bucket_id,
                    "title": f"{bucket_id} idea {index}",
                    "move": f"Apply {bucket_id} move {index}.",
                    "basis": f"reasoned: {bucket_id} premise {index} supports this move",
                    "significance": "The move changes a material choice.",
                }
                for bucket_id in bucket_ids
                for index in range(minimum)
            ],
        }

    def test_seals_single_and_paired_candidate_files(self):
        with tempfile.TemporaryDirectory() as directory:
            for paired in (False, True):
                document = candidate_document(paired=paired)
                draft = self.write_json(directory, f"draft-{paired}.json", document)
                output = Path(directory) / f"sealed-{paired}.json"
                expected = self.write_expected(directory, f"expected-{paired}.json", document, output)
                receipt = MODULE.seal_candidate_file(draft, output, expected)
                self.assertEqual(receipt["kind"], "ideation-candidates")
                self.assertEqual(receipt["candidate_count"], 2 if paired else 1)
                self.assertEqual(receipt, MODULE.candidate_receipt(output))
                accepted = MODULE.accept_candidate_receipt(receipt, expected)
                self.assertEqual(accepted["receipt"], receipt)
                self.assertEqual(len(accepted["candidates"]), 2 if paired else 1)

    def test_expected_manifest_rejects_assignment_and_path_mismatches(self):
        with tempfile.TemporaryDirectory() as directory:
            original = self.document_for_buckets(
                kind="frame",
                assignment_id="default-01",
                bucket_ids=["pain"],
                minimum=2,
                maximum=3,
            )
            output = Path(directory) / "sealed.json"
            expected = self.write_expected(directory, "expected.json", original, output)

            mutations = {}
            lowered_quota = json.loads(json.dumps(original))
            lowered_quota["assignment"]["buckets"][0]["minimum"] = 1
            mutations["quota"] = lowered_quota
            changed_bucket = json.loads(json.dumps(original))
            changed_bucket["assignment"]["buckets"][0]["id"] = "friction"
            for candidate in changed_bucket["candidates"]:
                candidate["assignment"] = "friction"
            mutations["bucket"] = changed_bucket
            changed_assignment = json.loads(json.dumps(original))
            changed_assignment["assignment"]["assignment_id"] = "default-02"
            mutations["assignment"] = changed_assignment
            changed_kind = json.loads(json.dumps(original))
            changed_kind["assignment"]["kind"] = "universal"
            mutations["kind"] = changed_kind
            changed_areas = json.loads(json.dumps(original))
            changed_areas["assignment"]["areas"] = ["delivery"]
            for candidate in changed_areas["candidates"]:
                candidate["area"] = "delivery"
            mutations["areas"] = changed_areas

            for name, document in mutations.items():
                with self.subTest(name=name):
                    draft = self.write_json(directory, f"draft-{name}.json", document)
                    with self.assertRaisesRegex(MODULE.ArtifactError, "expected assignment"):
                        MODULE.seal_candidate_file(draft, output, expected)

            path_draft = self.write_json(directory, "draft-path.json", original)
            wrong_path_expected = self.write_expected(
                directory,
                "expected-wrong-path.json",
                original,
                Path(directory) / "other.json",
            )
            with self.assertRaisesRegex(MODULE.ArtifactError, "result path"):
                MODULE.seal_candidate_file(path_draft, output, wrong_path_expected)

            receipt = MODULE.seal_candidate_file(path_draft, output, expected)
            with self.assertRaisesRegex(MODULE.ArtifactError, "result path"):
                MODULE.accept_candidate_receipt(receipt, wrong_path_expected)
            unreadable_wrong_path_receipt = dict(receipt)
            unreadable_wrong_path_receipt["path"] = str(Path(directory) / "not-json.json")
            with self.assertRaisesRegex(MODULE.ArtifactError, "result path"):
                MODULE.accept_candidate_receipt(unreadable_wrong_path_receipt, expected)
            changed_expected_document = json.loads(expected.read_text(encoding="utf-8"))
            changed_expected_document["assignment"]["assignment_id"] = "default-02"
            changed_expected = self.write_json(
                directory, "expected-changed.json", changed_expected_document
            )
            with self.assertRaisesRegex(MODULE.ArtifactError, "expected assignment"):
                MODULE.accept_candidate_receipt(receipt, changed_expected)

    def test_rejects_quota_basis_and_area_failures(self):
        quota = candidate_document(paired=True)
        quota["candidates"] = quota["candidates"][:1]
        with self.assertRaisesRegex(MODULE.ArtifactError, "constraint.*minimum"):
            MODULE.validate_candidate_document(quota)

        basis = candidate_document()
        basis["candidates"][0]["basis"] = "probably true"
        with self.assertRaisesRegex(MODULE.ArtifactError, "basis"):
            MODULE.validate_candidate_document(basis)

        area = candidate_document(areas=["delivery"])
        del area["candidates"][0]["area"]
        with self.assertRaisesRegex(MODULE.ArtifactError, "area"):
            MODULE.validate_candidate_document(area)

    def test_atomic_subject_omits_area(self):
        document = candidate_document()
        MODULE.validate_candidate_document(document)
        document["candidates"][0]["area"] = "invented"
        with self.assertRaisesRegex(MODULE.ArtifactError, "omit area"):
            MODULE.validate_candidate_document(document)

    def test_receipt_digest_mismatch_is_detected_by_parent_revalidation(self):
        with tempfile.TemporaryDirectory() as directory:
            document = candidate_document()
            draft = self.write_json(directory, "draft.json", document)
            output = Path(directory) / "sealed.json"
            expected = self.write_expected(directory, "expected.json", document, output)
            receipt = MODULE.seal_candidate_file(draft, output, expected)
            output.write_text(output.read_text(encoding="utf-8") + " ", encoding="utf-8")
            with self.assertRaisesRegex(MODULE.ArtifactError, "receipt"):
                MODULE.accept_candidate_receipt(receipt, expected)

    def test_failed_atomic_write_leaves_no_authoritative_file(self):
        with tempfile.TemporaryDirectory() as directory:
            document = candidate_document()
            draft = self.write_json(directory, "draft.json", document)
            output = Path(directory) / "sealed.json"
            expected = self.write_expected(directory, "expected.json", document, output)
            with mock.patch.object(MODULE.os, "replace", side_effect=OSError("disk full")):
                with self.assertRaisesRegex(MODULE.ArtifactError, "write"):
                    MODULE.seal_candidate_file(draft, output, expected)
            self.assertFalse(output.exists())

    def test_projection_is_deterministic_and_preserves_source_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            document = candidate_document(paired=True)
            draft = self.write_json(directory, "draft.json", document)
            output = Path(directory) / "sealed.json"
            expected = self.write_expected(directory, "expected.json", document, output)
            MODULE.seal_candidate_file(draft, output, expected)
            first = MODULE.project_candidates(output)
            second = MODULE.project_candidates(output)
            self.assertEqual(first, second)
            self.assertEqual(len(first), 2)
            self.assertTrue(first[0]["parents"][0].startswith("frame:default-01:"))
            self.assertTrue(first[0]["candidate_id"].startswith("cand-"))

    def test_consolidated_lineage_and_verdict_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            document = candidate_document(paired=True)
            draft = self.write_json(directory, "draft.json", document)
            source = Path(directory) / "source.json"
            expected = self.write_expected(directory, "expected.json", document, source)
            MODULE.seal_candidate_file(draft, source, expected)
            projected = MODULE.project_candidates(source)
            combined = dict(projected[0])
            combined["origin"] = "synthesis"
            combined["parents"] = sorted(item["parents"][0] for item in projected)
            del combined["candidate_id"]
            consolidated_draft_document = {
                "schema_version": 1,
                "areas": [],
                "candidates": projected + [combined],
            }
            consolidated_draft = self.write_json(
                directory, "consolidated-draft.json", consolidated_draft_document
            )
            consolidated = Path(directory) / "consolidated.json"
            sources = self.write_sources(directory, "sources.json", [], projected)
            consolidated_receipt = MODULE.seal_consolidated_file(
                consolidated_draft, consolidated, sources
            )
            consolidated_document = json.loads(consolidated.read_text(encoding="utf-8"))
            self.assertTrue(consolidated_document["candidates"][-1]["candidate_id"].startswith("cand-"))

            verdicts = {
                "schema_version": 1,
                "candidate_file_sha256": consolidated_receipt["sha256"],
                "verdicts": [
                    {"candidate_id": item["candidate_id"], "verdict": "sound", "reason": "Basis holds."}
                    for item in consolidated_document["candidates"]
                ],
            }
            MODULE.validate_verdict_document(verdicts, consolidated)
            verdict_draft = self.write_json(directory, "verdict-draft.json", verdicts)
            verdict_output = Path(directory) / "verdicts.json"
            verdict_receipt = MODULE.seal_verdict_file(verdict_draft, verdict_output, consolidated)
            self.assertEqual(verdict_receipt["verdict_count"], 3)
            self.assertEqual(verdict_receipt, MODULE.verdict_receipt(verdict_output, consolidated))
            verdicts["verdicts"].pop()
            with self.assertRaisesRegex(MODULE.ArtifactError, "coverage"):
                MODULE.validate_verdict_document(verdicts, consolidated)

            consolidated_document["candidates"][-1]["parents"] = combined["parents"][:1]
            with self.assertRaisesRegex(MODULE.ArtifactError, "at least two parents"):
                MODULE.validate_consolidated_document(consolidated_document)

    def test_consolidated_areas_and_sources_are_authoritative(self):
        with tempfile.TemporaryDirectory() as directory:
            document = candidate_document(areas=["delivery"])
            draft = self.write_json(directory, "draft.json", document)
            source = Path(directory) / "source.json"
            expected = self.write_expected(directory, "expected.json", document, source)
            receipt = MODULE.seal_candidate_file(draft, source, expected)
            projected = MODULE.accept_candidate_receipt(receipt, expected)["candidates"]
            sources = self.write_sources(directory, "sources.json", ["delivery"], projected)
            valid = {"schema_version": 1, "areas": ["delivery"], "candidates": projected}
            valid_draft = self.write_json(directory, "valid-draft.json", valid)
            sealed = Path(directory) / "consolidated.json"
            MODULE.seal_consolidated_file(valid_draft, sealed, sources)

            missing_area = json.loads(json.dumps(valid))
            del missing_area["candidates"][0]["area"]
            missing_area_draft = self.write_json(
                directory, "missing-area.json", missing_area
            )
            with self.assertRaisesRegex(MODULE.ArtifactError, "area"):
                MODULE.seal_consolidated_file(missing_area_draft, sealed, sources)

            invented_area = json.loads(json.dumps(valid))
            invented_area["candidates"][0]["area"] = "invented"
            invented_area_draft = self.write_json(
                directory, "invented-area.json", invented_area
            )
            with self.assertRaisesRegex(MODULE.ArtifactError, "not declared"):
                MODULE.seal_consolidated_file(invented_area_draft, sealed, sources)

            fabricated_source = json.loads(json.dumps(valid))
            fabricated_source["candidates"][0]["parents"] = [
                "frame:default-01:" + "0" * 64 + ":999"
            ]
            del fabricated_source["candidates"][0]["candidate_id"]
            fabricated_source_draft = self.write_json(
                directory, "fabricated-source.json", fabricated_source
            )
            with self.assertRaisesRegex(MODULE.ArtifactError, "source registry"):
                MODULE.seal_consolidated_file(fabricated_source_draft, sealed, sources)

            wrong_areas_sources = self.write_sources(
                directory, "wrong-areas-sources.json", ["operations"], projected
            )
            with self.assertRaisesRegex(MODULE.ArtifactError, "areas do not match"):
                MODULE.seal_consolidated_file(valid_draft, sealed, wrong_areas_sources)

    def test_dispatch_contract_uses_small_default_fleet(self):
        contract = MODULE.load_dispatch_contract()
        modes = contract["modes"]
        self.assertEqual(len(modes["default-software"]["agents"]), 3)
        self.assertEqual(sum(len(agent) for agent in modes["default-software"]["agents"]), 6)
        self.assertEqual(len(modes["surprise-me"]["agents"]), 4)
        self.assertEqual(len(modes["go-deep"]["agents"]), 6)
        self.assertEqual(modes["issue-tracker"]["max_agents"], 2)
        self.assertEqual(modes["recovery"]["max_agents"], 1)
        self.assertEqual(modes["default-software"]["candidate_quota"], [6, 8])
        self.assertEqual(modes["default-software"]["evidence_reads_per_assignment"], 4)
        self.assertEqual(modes["issue-tracker"]["dynamic_assignments"], [3, 4])
        self.assertEqual(modes["issue-tracker"]["total_evidence_read_cap"], 20)
        self.assertEqual(modes["non-software-quick"]["agents"], [])
        self.assertEqual(len(modes["non-software-standard"]["agents"]), 3)
        self.assertEqual(len(modes["non-software-full"]["agents"]), 6)
        self.assertEqual(modes["recovery"]["max_assignments_per_agent"], 2)
        self.assertEqual(modes["recovery"]["candidate_quota"], [3, 5])
        assignments = {
            assignment
            for agent in modes["default-software"]["agents"]
            for assignment in agent
        }
        self.assertEqual(len(assignments), 6)
        self.assertEqual(len(assignments) * modes["default-software"]["candidate_quota"][0], 36)

    def test_every_dispatch_mode_seals_its_declared_minimum(self):
        modes = MODULE.load_dispatch_contract()["modes"]
        with tempfile.TemporaryDirectory() as directory:
            for mode_name in (
                "default-software",
                "surprise-me",
                "go-deep",
                "non-software-standard",
                "non-software-full",
            ):
                mode = modes[mode_name]
                minimum, maximum = mode["candidate_quota"]
                total = 0
                for index, bucket_ids in enumerate(mode["agents"]):
                    document = self.document_for_buckets(
                        kind="universal" if mode_name.startswith("non-software") else "frame",
                        assignment_id=f"{mode_name}-{index}",
                        bucket_ids=bucket_ids,
                        minimum=minimum,
                        maximum=maximum,
                    )
                    draft = self.write_json(directory, f"{mode_name}-{index}-draft.json", document)
                    output = Path(directory) / f"{mode_name}-{index}.json"
                    expected = self.write_expected(
                        directory, f"{mode_name}-{index}-expected.json", document, output
                    )
                    total += MODULE.seal_candidate_file(draft, output, expected)["candidate_count"]
                self.assertEqual(total, sum(len(agent) for agent in mode["agents"]) * minimum)

            for mode_name, kind, bucket_ids in (
                ("issue-tracker", "theme", ["theme-1", "theme-2", "theme-3", "theme-4"]),
                ("recovery", "recovery", ["missing-area-1", "missing-area-2"]),
            ):
                mode = modes[mode_name]
                minimum, maximum = mode["candidate_quota"]
                document = self.document_for_buckets(
                    kind=kind,
                    assignment_id=f"{mode_name}-01",
                    bucket_ids=bucket_ids,
                    minimum=minimum,
                    maximum=maximum,
                )
                draft = self.write_json(directory, f"{mode_name}-draft.json", document)
                output = Path(directory) / f"{mode_name}.json"
                expected = self.write_expected(
                    directory, f"{mode_name}-expected.json", document, output
                )
                self.assertEqual(
                    MODULE.seal_candidate_file(draft, output, expected)["candidate_count"],
                    len(bucket_ids) * minimum,
                )

    def test_instruction_word_budgets(self):
        skill_words = (ROOT / "skills" / "ae-ideate" / "SKILL.md").read_text(encoding="utf-8").split()
        self.assertLessEqual(len(skill_words), 2000)
        for name in ("ideation-generator.md", "ideation-verifier.md", "research-distiller.md"):
            path = ROOT / "skills" / "ae-ideate" / "references" / "agents" / name
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 700, name)

    def test_root_routes_optional_context_instead_of_embedding_it(self):
        skill = (ROOT / "skills" / "ae-ideate" / "SKILL.md").read_text(encoding="utf-8")
        for reference in (
            "intake-and-routing.md",
            "repo-grounding.md",
            "elsewhere-grounding.md",
            "research-artifacts.md",
            "divergent-ideation.md",
            "post-ideation-workflow.md",
        ):
            self.assertIn(reference, skill)
        self.assertNotIn("evidence-user-research-{slug}", skill)
        self.assertNotIn("Issue analysis unavailable", skill)


if __name__ == "__main__":
    unittest.main()
