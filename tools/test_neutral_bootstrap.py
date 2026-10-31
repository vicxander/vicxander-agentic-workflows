"""Negative regressions for the instruction-driven integration bootstrap."""

import unittest

from tools import validate_workflows as validator


class NeutralBootstrapTests(unittest.TestCase):
    def setUp(self):
        validator.errors.clear()
        validator.checks = 0
        self.guide = (validator.ROOT / "agentic-bootstrap-kit" / "AGENTIC_BOOTSTRAP.md").read_text()

    def test_current_guide(self):
        validator.check_neutral_bootstrap(self.guide)
        self.assertEqual([], validator.errors)

    def test_missing_target_and_replaced_native_path_fail(self):
        for old, new in (("| claude |", "| unknown |"), ("CLAUDE.md", "AGENTS.md")):
            with self.subTest(old=old):
                validator.errors.clear()
                validator.check_neutral_bootstrap(self.guide.replace(old, new))
                self.assertTrue(validator.errors)

    def test_missing_preservation_and_routing_rules_fail(self):
        for clause in (
            "Leave unresolved files unchanged",
            "Never reset state from empty templates",
            "Unsupported names must produce an unsupported-target report before any writes",
            "Do not write files, create directories, or update memory",
            "If it is missing, report the missing source and stop before writes",
        ):
            with self.subTest(clause=clause):
                validator.errors.clear()
                validator.check_neutral_bootstrap(self.guide.replace(clause, "Rule removed"))
                self.assertTrue(validator.errors)
