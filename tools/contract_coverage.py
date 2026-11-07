#!/usr/bin/env python3
"""Compute and compare the contract-clause coverage baseline.

The validator names every contract clause it enforces in a pattern registry. This module records
which repository surface carries which clause, so that moving or deduplicating contract prose
cannot silently drop a clause from a surface that is required to state it.

Run directly to inspect coverage, or with ``--write`` to record a deliberate change:

    python tools/contract_coverage.py
    python tools/contract_coverage.py --write
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:  # Importable both as ``tools.contract_coverage`` and as a script inside ``tools``.
    from tools import validate_workflows as vw
except ImportError:  # pragma: no cover - exercised by the direct-script path.
    import validate_workflows as vw

ROOT = vw.ROOT
BASELINE_PATH = ROOT / "tools" / "contract_clause_coverage.json"

# Registries whose clauses are contract prose carried by repository surfaces. License and notice
# registries are deliberately excluded: they are verified against fixed legal text by dedicated
# checks and are not subject to the deduplication work this baseline guards.
COVERED_REGISTRIES = {
    "untrusted-content": vw.UNTRUSTED_CONTENT_CONTRACT_PATTERNS,
    "external-tool-data": vw.EXTERNAL_TOOL_DATA_CONTRACT_PATTERNS,
    "first-run-adaptation": vw.FIRST_RUN_ADAPTATION_CONTRACT_PATTERNS,
    "fingerprint": vw.FINGERPRINT_CONTRACT_PATTERNS,
    "retry": vw.RETRY_CONTRACT_PATTERNS,
    "lease": vw.LEASE_CONTRACT_PATTERNS,
}

EMBEDDED_PREFIX = "agentic-bootstrap-kit/AGENTIC_FILE_TEMPLATES.md::"

# Matches a concrete plan such as docs/implementation-plans/IP-0001-title.md, in any
# provider subtree, but never IP-TEMPLATE.md, INDEX.md, or README.md.
PLAN_INSTANCE_PATTERN = re.compile(r"(?:^|/)docs/implementation-plans/IP-\d+-")


def clause_ids() -> list[str]:
    """Return every covered clause identifier as ``registry:clause``."""
    return [
        f"{registry}:{clause}"
        for registry, patterns in COVERED_REGISTRIES.items()
        for clause in patterns
    ]


def _matches(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.DOTALL | re.IGNORECASE) is not None


def surfaces() -> dict[str, str]:
    """Return every scanned surface name mapped to its text.

    Real Markdown files are scanned by repository-relative path. The bootstrap bundle is scanned
    per embedded target instead of as one document, because a clause present in one embedded file
    must not satisfy coverage for a different embedded file.
    """
    result: dict[str, str] = {}
    for path in vw.repository_files():
        if path.suffix.lower() != ".md":
            continue
        relative = vw.relative(path)
        if PLAN_INSTANCE_PATTERN.search(relative):
            # A plan instance records work against the contract; it does not carry the contract.
            # Plan templates and their READMEs do carry contract text that is materialised into
            # user repositories, so they deliberately remain in scope.
            continue
        if relative == "agentic-bootstrap-kit/AGENTIC_FILE_TEMPLATES.md":
            continue
        result[relative] = vw.read_text(path)

    template_path = ROOT / "agentic-bootstrap-kit" / "AGENTIC_FILE_TEMPLATES.md"
    if template_path.is_file():
        for target, _info, body, _line in vw.extract_template_targets(template_path):
            result[f"{EMBEDDED_PREFIX}{target}"] = body
    return result


def compute() -> dict[str, list[str]]:
    """Return each clause identifier mapped to the sorted surfaces that carry it."""
    coverage: dict[str, list[str]] = {identifier: [] for identifier in clause_ids()}
    for surface, text in surfaces().items():
        if not text:
            continue
        for registry, patterns in COVERED_REGISTRIES.items():
            for clause, pattern in patterns.items():
                if _matches(pattern, text):
                    coverage[f"{registry}:{clause}"].append(surface)
    return {identifier: sorted(found) for identifier, found in coverage.items()}


class BaselineError(Exception):
    """The baseline file exists but cannot be used."""


def load_baseline() -> dict[str, list[str]]:
    """Return the recorded baseline, or an empty mapping when none exists yet.

    Raises ``BaselineError`` when the file is present but unreadable or malformed, so callers can
    report that distinctly from a baseline that was never recorded.
    """
    if not BASELINE_PATH.is_file():
        return {}
    try:
        raw = BASELINE_PATH.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise BaselineError(f"coverage baseline is unreadable: {exc}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BaselineError(f"coverage baseline is not valid JSON: {exc}") from exc
    if not isinstance(data, dict) or "coverage" not in data:
        raise BaselineError("coverage baseline has no 'coverage' mapping")
    coverage = data["coverage"]
    if not isinstance(coverage, dict):
        raise BaselineError("coverage baseline 'coverage' is not a mapping")
    return coverage


def _pattern_for(identifier: str) -> str | None:
    registry, _, clause = identifier.partition(":")
    return COVERED_REGISTRIES.get(registry, {}).get(clause)


def verify_pairs(baseline: dict[str, list[str]]) -> list[tuple[str, str, str | None]]:
    """Return ``(identifier, surface, problem)`` for every recorded clause-surface pair.

    ``problem`` is ``None`` when the pair still holds. Callers that report per-assertion counts use
    this; ``verify`` wraps it for the plain command-line path.
    """
    results: list[tuple[str, str, str | None]] = []
    available = surfaces()
    for identifier, expected in sorted(baseline.items()):
        pattern = _pattern_for(identifier)
        for surface in expected:
            if pattern is None:
                problem = (
                    f"baseline records unknown contract clause {identifier!r}; "
                    "regenerate the baseline"
                )
            elif surface not in available:
                problem = (
                    f"contract clause {identifier!r} recorded for missing surface {surface}"
                )
            elif not _matches(pattern, available[surface]):
                problem = f"contract clause {identifier!r} is no longer present in {surface}"
            else:
                problem = None
            results.append((identifier, surface, problem))
    return results


def verify(baseline: dict[str, list[str]]) -> list[str]:
    """Return one message per recorded clause-surface pair that no longer holds.

    Only the pairs the baseline records are re-tested. A regression is by definition the loss of a
    pair that used to hold, so a surface carrying no clause cannot produce one. That makes this the
    sound fast path; the exhaustive scan in ``compute`` is reserved for ``--write``.
    """
    return [problem for _, _, problem in verify_pairs(baseline) if problem is not None]


def write_baseline(coverage: dict[str, list[str]]) -> None:
    """Record coverage as the new baseline."""
    payload = {
        "comment": (
            "Contract-clause coverage baseline. Regenerate with "
            "'python tools/contract_coverage.py --write' only when a clause is deliberately "
            "removed from a surface, and review the resulting diff as security evidence."
        ),
        "coverage": coverage,
    }
    # Written as bytes so the platform's newline translation cannot reintroduce CRLF into a
    # repository that declares `eol=lf`.
    BASELINE_PATH.write_bytes(
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="record current coverage as the baseline",
    )
    arguments = parser.parse_args(argv)

    if arguments.write:
        current = compute()
        write_baseline(current)
        print(f"recorded {len(current)} clauses to {vw.relative(BASELINE_PATH)}")
        return 0

    baseline = load_baseline()
    if not baseline:
        print("no baseline recorded; run with --write")
        return 1
    problems = verify(baseline)
    if problems:
        print(f"contract coverage regressed: {len(problems)} issue(s).")
        for problem in problems:
            print(f"- {problem}")
        return 1
    carried = sum(len(found) for found in baseline.values())
    print(
        f"contract coverage holds: {len(baseline)} clauses across "
        f"{carried} clause-surface pairs."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
