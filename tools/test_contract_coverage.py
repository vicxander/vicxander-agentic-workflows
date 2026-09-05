"""Tests for the contract-clause coverage gate."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from tools import contract_coverage as coverage
from tools import validate_workflows as validator


class ClauseIdentifierTests(unittest.TestCase):
    def test_every_covered_registry_contributes_clauses(self) -> None:
        for registry, patterns in coverage.COVERED_REGISTRIES.items():
            with self.subTest(registry=registry):
                self.assertTrue(patterns, f"{registry} registry is empty")

    def test_clause_identifiers_are_unique(self) -> None:
        identifiers = coverage.clause_ids()
        self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_pattern_lookup_resolves_every_identifier(self) -> None:
        for identifier in coverage.clause_ids():
            with self.subTest(identifier=identifier):
                self.assertIsNotNone(coverage._pattern_for(identifier))

    def test_unknown_identifier_resolves_to_none(self) -> None:
        self.assertIsNone(coverage._pattern_for("nonexistent:clause"))
        self.assertIsNone(coverage._pattern_for("untrusted-content:no such clause"))


class BaselineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.baseline = coverage.load_baseline()

    def test_baseline_exists_and_is_populated(self) -> None:
        self.assertTrue(self.baseline, "coverage baseline is missing or empty")

    def test_baseline_clause_names_match_the_registries(self) -> None:
        self.assertEqual(sorted(self.baseline), sorted(coverage.clause_ids()))

    def test_every_clause_is_carried_by_at_least_one_surface(self) -> None:
        orphans = sorted(name for name, found in self.baseline.items() if not found)
        self.assertEqual(orphans, [], f"clauses recorded with no carrier: {orphans}")

    def test_repository_currently_satisfies_the_baseline(self) -> None:
        self.assertEqual(coverage.verify(self.baseline), [])


class RegressionDetectionTests(unittest.TestCase):
    """The gate must fail when a recorded clause stops holding."""

    def test_removed_clause_is_reported(self) -> None:
        identifier = "untrusted-content:embedded directive refusal"
        with mock.patch.object(
            coverage, "surfaces", return_value={"fake.md": "Nothing relevant here."}
        ):
            problems = coverage.verify({identifier: ["fake.md"]})
        self.assertEqual(len(problems), 1)
        self.assertIn("no longer present in fake.md", problems[0])

    def test_present_clause_is_not_reported(self) -> None:
        identifier = "untrusted-content:embedded directive refusal"
        carrier = validator.read_text(
            validator.ROOT / "claude-agentic-workflow" / "CLAUDE.md"
        )
        with mock.patch.object(coverage, "surfaces", return_value={"fake.md": carrier}):
            self.assertEqual(coverage.verify({identifier: ["fake.md"]}), [])

    def test_missing_surface_is_reported(self) -> None:
        identifier = "untrusted-content:embedded directive refusal"
        with mock.patch.object(coverage, "surfaces", return_value={}):
            problems = coverage.verify({identifier: ["gone.md"]})
        self.assertEqual(len(problems), 1)
        self.assertIn("recorded for missing surface gone.md", problems[0])

    def test_unknown_clause_in_baseline_is_reported(self) -> None:
        with mock.patch.object(
            coverage, "surfaces", return_value={"fake.md": "text"}
        ):
            problems = coverage.verify({"untrusted-content:invented": ["fake.md"]})
        self.assertEqual(len(problems), 1)
        self.assertIn("unknown contract clause", problems[0])

    def test_verify_pairs_reports_one_result_per_recorded_pair(self) -> None:
        baseline = {"untrusted-content:embedded directive refusal": ["a.md", "b.md"]}
        with mock.patch.object(
            coverage, "surfaces", return_value={"a.md": "x", "b.md": "y"}
        ):
            results = coverage.verify_pairs(baseline)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(problem is not None for _, _, problem in results))


class ValidatorIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        validator.errors.clear()
        validator.checks = 0

    def test_coverage_check_is_importable_under_the_package_path(self) -> None:
        """Guards the lazy import: the gate must work when imported as ``tools.*`` too."""
        validator.check_contract_coverage()
        self.assertEqual(validator.errors, [])
        self.assertGreater(validator.checks, 1)

    def test_coverage_check_reports_a_regression_as_an_error(self) -> None:
        identifier = "untrusted-content:embedded directive refusal"
        with mock.patch.object(
            coverage, "load_baseline", return_value={identifier: ["fake.md"]}
        ), mock.patch.object(
            coverage, "surfaces", return_value={"fake.md": "Nothing relevant."}
        ):
            validator.check_contract_coverage()
        self.assertEqual(len(validator.errors), 1)
        self.assertIn("no longer present", validator.errors[0])

    def test_missing_baseline_is_reported(self) -> None:
        with mock.patch.object(coverage, "load_baseline", return_value={}):
            validator.check_contract_coverage()
        self.assertEqual(len(validator.errors), 1)
        self.assertIn("baseline is missing", validator.errors[0])


class BaselineLoadingTests(unittest.TestCase):
    """A present-but-unusable baseline must be reported, never crash the run."""

    def setUp(self) -> None:
        validator.errors.clear()
        validator.checks = 0

    def _with_baseline(self, data: bytes):
        import tempfile
        directory = tempfile.mkdtemp()
        path = Path(directory) / "baseline.json"
        path.write_bytes(data)
        return mock.patch.object(coverage, "BASELINE_PATH", path)

    def test_malformed_json_raises_baseline_error(self) -> None:
        with self._with_baseline(b"{ not json"):
            with self.assertRaises(coverage.BaselineError) as caught:
                coverage.load_baseline()
        self.assertIn("not valid JSON", str(caught.exception))

    def test_missing_coverage_key_is_distinguished_from_absent(self) -> None:
        with self._with_baseline(b'{"comment": "no coverage key"}'):
            with self.assertRaises(coverage.BaselineError) as caught:
                coverage.load_baseline()
        self.assertIn("no 'coverage' mapping", str(caught.exception))

    def test_absent_baseline_returns_empty(self) -> None:
        import tempfile
        directory = tempfile.mkdtemp()
        with mock.patch.object(coverage, "BASELINE_PATH", Path(directory) / "absent.json"):
            self.assertEqual(coverage.load_baseline(), {})

    def test_malformed_baseline_is_a_check_failure_not_a_crash(self) -> None:
        """Raising here would abort main() before the accumulated report prints."""
        with self._with_baseline(b"{ not json"):
            validator.check_contract_coverage()
        self.assertEqual(len(validator.errors), 1)
        self.assertIn("not valid JSON", validator.errors[0])


class SurfaceSelectionTests(unittest.TestCase):
    def test_plan_instances_are_excluded_in_every_subtree(self) -> None:
        scanned = coverage.surfaces()
        instances = [s for s in scanned if coverage.PLAN_INSTANCE_PATTERN.search(s)]
        self.assertEqual(instances, [], f"plan instances scanned as contract surfaces: {instances}")

    def test_plan_templates_remain_in_scope(self) -> None:
        """Templates carry contract text that is materialised into user repositories."""
        scanned = coverage.surfaces()
        templates = [s for s in scanned if s.endswith("docs/implementation-plans/IP-TEMPLATE.md")]
        self.assertTrue(templates, "plan templates must stay in scope")

    def test_pattern_matches_instances_but_not_templates(self) -> None:
        search = coverage.PLAN_INSTANCE_PATTERN.search
        self.assertTrue(search("docs/implementation-plans/IP-0001-title.md"))
        self.assertTrue(search("claude-agentic-workflow/docs/implementation-plans/IP-0007-x.md"))
        self.assertIsNone(search("codex-agentic-workflow/docs/implementation-plans/IP-TEMPLATE.md"))
        self.assertIsNone(search("codex-agentic-workflow/docs/implementation-plans/INDEX.md"))


if __name__ == "__main__":
    unittest.main()
