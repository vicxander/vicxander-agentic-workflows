"""Tests for the validator's command-line entry points.

`main` had no coverage: neither the default repository scan nor the documented
`--bootstrap-target` mode was exercised through the CLI, so argument handling and exit codes were
unverified.
"""

from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools import validate_workflows as validator


def _materialise(target_root: Path) -> None:
    """Write every embedded bootstrap target into a scratch project."""
    template = validator.ROOT / "agentic-bootstrap-kit" / "AGENTIC_FILE_TEMPLATES.md"
    for name, _info, body, _line in validator.extract_template_targets(template):
        destination = target_root / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((body.rstrip("\n") + "\n").encode("utf-8"))


class ValidatorCliTests(unittest.TestCase):
    def setUp(self) -> None:
        validator.errors.clear()
        validator.checks = 0

    def test_repository_scan_exits_zero(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = validator.main([])
        self.assertEqual(code, 0, buffer.getvalue())
        self.assertIn("Workflow validation passed", buffer.getvalue())

    def test_bootstrap_target_mode_exits_zero(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            _materialise(target)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = validator.main(["--bootstrap-target", str(target)])
        self.assertEqual(code, 0, buffer.getvalue())
        self.assertIn("Bootstrap target validation passed", buffer.getvalue())

    def test_bootstrap_target_mode_reports_a_broken_target(self) -> None:
        """A target-only requirement must fail through the CLI, not just in-process."""
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            _materialise(target)
            agents = target / "AGENTS.md"
            agents.write_bytes(
                agents.read_bytes().replace(
                    b"## Resource Governance", b"## Resource Notes", 1
                )
            )
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = validator.main(["--bootstrap-target", str(target)])
        self.assertEqual(code, 1)
        self.assertIn("Bootstrap target validation failed", buffer.getvalue())

    def test_missing_bootstrap_target_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "absent"
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = validator.main(["--bootstrap-target", str(missing)])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
