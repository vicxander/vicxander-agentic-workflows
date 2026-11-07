"""Tests for the line-ending half of the text-hygiene gate."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import contract_coverage
from tools import validate_workflows as validator

CR = b"\x0d"
CRLF = b"\x0d\x0a"


class LineEndingGuardTests(unittest.TestCase):
    """`.gitattributes` declares `* text=auto eol=lf`; the gate must enforce it."""

    def setUp(self) -> None:
        validator.errors.clear()
        validator.checks = 0

    def _check(self, data: bytes, **kwargs) -> None:
        """Run the hygiene gate over one temporary file rooted inside the validator's ROOT."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "sample.md"
            path.write_bytes(data)
            with mock.patch.object(validator, "ROOT", root):
                validator.check_text_hygiene([path], **kwargs)

    def test_crlf_is_reported_when_lf_is_required(self) -> None:
        self._check(b"# Title" + CRLF + CRLF + b"Body." + CRLF, require_lf=True)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn("must use LF line endings", validator.errors[0])

    def test_lf_only_content_passes(self) -> None:
        self._check(b"# Title\n\nBody.\n", require_lf=True)
        self.assertEqual(validator.errors, [])

    def test_crlf_is_tolerated_when_lf_is_not_required(self) -> None:
        """Bootstrap targets are other people's repositories; do not impose our convention."""
        self._check(b"# Title" + CRLF + CRLF + b"Body." + CRLF)
        self.assertEqual(validator.errors, [])

    def test_default_does_not_require_lf(self) -> None:
        self._check(b"# Title" + CRLF)
        self._check(b"# Title" + CRLF, require_lf=False)
        self.assertEqual(validator.errors, [])

    def test_json_is_inside_the_hygiene_gate(self) -> None:
        """The coverage baseline is JSON and is the file most likely to regain CRLF."""
        self.assertIn(".json", validator.TEXT_SUFFIXES)
        baseline = validator.ROOT / "tools" / "contract_clause_coverage.json"
        self.assertTrue(validator.is_text_file(baseline))

    def test_baseline_writer_emits_lf(self) -> None:
        """Regression: write_text applied the platform's newline translation on Windows."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            with mock.patch.object(contract_coverage, "BASELINE_PATH", path):
                contract_coverage.write_baseline(
                    {"untrusted-content:declared authority": ["a.md"]}
                )
            written = path.read_bytes()
        self.assertNotIn(CR, written)
        self.assertTrue(written.endswith(b"\n"))

    def test_repository_itself_is_lf_only(self) -> None:
        textual = {".cff", ".json", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}
        offenders = [
            validator.relative(path)
            for path in validator.repository_files()
            if (validator.is_text_file(path) or path.suffix.lower() in textual)
            and CRLF in path.read_bytes()
        ]
        self.assertEqual(offenders, [], f"CRLF found in tracked text files: {offenders}")


if __name__ == "__main__":
    unittest.main()
