#!/usr/bin/env python3
"""Validate the repository's cross-provider agentic workflow contract."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.11+ is expected.
    tomllib = None


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_CONTRACT_VERSION = "2.6.0"
GITHUB_AGENT_PROMPT_MAX_CHARACTERS = 30_000
CLAUDE_AGENT_COLORS = {
    "red",
    "blue",
    "green",
    "yellow",
    "purple",
    "orange",
    "pink",
    "cyan",
}
IGNORED_PARTS = {".git", "__pycache__"}
TEXT_NAMES = {"LICENSE", ".gitattributes"}
TEXT_SUFFIXES = {".cff", ".json", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}

PROVIDERS = {
    "codex": {
        "root": ROOT / "codex-agentic-workflow",
        "readme": "README.md",
        "core": ["AGENTS.md", ".codex/README.md", ".codex/agents/README.md"],
        "conformance": ".codex/workflow-conformance.md",
        "memory": ".codex/agents/memory",
        "role_memory": [
            ".codex/agents/memory/orchestrator.md",
            ".codex/agents/memory/architect.md",
            ".codex/agents/memory/coder.md",
            ".codex/agents/memory/tester.md",
            ".codex/agents/memory/reviewer.md",
        ],
        "metrics": ".codex/workflow-metrics.md",
        "session": ".codex/session-notes.md",
        "entrypoints": {
            "AGENTS.md": ".codex/agents/README.md",
        },
        "required": [
            "README.md",
            "THIRD_PARTY_NOTICES.md",
            "AGENTS.md",
            ".agents/skills/README.md",
            ".agents/skills/SKILL-TEMPLATE.md",
            ".codex/config.toml",
            ".codex/README.md",
            ".codex/session-notes.md",
            ".codex/todo.md",
            ".codex/workflow-conformance.md",
            ".codex/workflow-metrics.md",
            ".codex/worklog.md",
            ".codex/agents/README.md",
            ".codex/agents/orchestrator.toml",
            ".codex/agents/architect.toml",
            ".codex/agents/coder.toml",
            ".codex/agents/tester.toml",
            ".codex/agents/reviewer.toml",
            ".codex/agents/memory/orchestrator.md",
            ".codex/agents/memory/architect.md",
            ".codex/agents/memory/coder.md",
            ".codex/agents/memory/tester.md",
            ".codex/agents/memory/reviewer.md",
        ],
    },
    "github-copilot": {
        "root": ROOT / "github-copilot-agentic-workflow",
        "readme": "README.md",
        "core": [
            "AGENTS.md",
            ".github/copilot-instructions.md",
            ".github/AGENTIC-WORKFLOW.md",
        ],
        "conformance": ".github/WORKFLOW-CONFORMANCE.md",
        "memory": ".github/agent-memory",
        "role_memory": [
            ".github/agent-memory/orchestrator.md",
            ".github/agent-memory/architect.md",
            ".github/agent-memory/coder.md",
            ".github/agent-memory/tester.md",
            ".github/agent-memory/reviewer.md",
        ],
        "metrics": ".github/agent-memory/workflow-metrics.md",
        "session": ".github/agent-memory/session-notes.md",
        "entrypoints": {
            "AGENTS.md": ".github/AGENTIC-WORKFLOW.md",
            ".github/copilot-instructions.md": ".github/AGENTIC-WORKFLOW.md",
        },
        "required": [
            "README.md",
            "THIRD_PARTY_NOTICES.md",
            "AGENTS.md",
            ".github/copilot-instructions.md",
            ".github/AGENTIC-WORKFLOW.md",
            ".github/WORKFLOW-CONFORMANCE.md",
            ".github/agents/orchestrator.agent.md",
            ".github/agents/architect.agent.md",
            ".github/agents/coder.agent.md",
            ".github/agents/tester.agent.md",
            ".github/agents/reviewer.agent.md",
            ".github/skills/README.md",
            ".github/skills/SKILL-TEMPLATE.md",
            ".github/agent-memory/README.md",
            ".github/agent-memory/session-notes.md",
            ".github/agent-memory/todo.md",
            ".github/agent-memory/workflow-metrics.md",
            ".github/agent-memory/worklog.md",
            ".github/agent-memory/orchestrator.md",
            ".github/agent-memory/architect.md",
            ".github/agent-memory/coder.md",
            ".github/agent-memory/tester.md",
            ".github/agent-memory/reviewer.md",
        ],
    },
    "claude": {
        "root": ROOT / "claude-agentic-workflow",
        "readme": "README.md",
        "core": ["CLAUDE.md", ".claude/AGENTIC-WORKFLOW.md"],
        "conformance": ".claude/workflow-conformance.md",
        "memory": ".claude/agent-memory",
        "role_memory": [
            ".claude/agent-memory/orchestrator/MEMORY.md",
            ".claude/agent-memory/architect/MEMORY.md",
            ".claude/agent-memory/coder/MEMORY.md",
            ".claude/agent-memory/tester/MEMORY.md",
            ".claude/agent-memory/reviewer/MEMORY.md",
        ],
        "metrics": ".claude/workflow-metrics.md",
        "session": ".claude/session-notes.md",
        "entrypoints": {
            "CLAUDE.md": ".claude/AGENTIC-WORKFLOW.md",
        },
        "required": [
            "README.md",
            "THIRD_PARTY_NOTICES.md",
            "CLAUDE.md",
            ".claude/AGENTIC-WORKFLOW.md",
            ".claude/workflow-conformance.md",
            ".claude/session-notes.md",
            ".claude/todo.md",
            ".claude/workflow-metrics.md",
            ".claude/worklog.md",
            ".claude/agents/orchestrator.md",
            ".claude/agents/architect.md",
            ".claude/agents/coder.md",
            ".claude/agents/tester.md",
            ".claude/agents/reviewer.md",
            ".claude/skills/README.md",
            ".claude/skills/SKILL-TEMPLATE.md",
            ".claude/skills/agentic-workflow/SKILL.md",
            ".claude/agent-memory/README.md",
            ".claude/agent-memory/orchestrator/MEMORY.md",
            ".claude/agent-memory/architect/MEMORY.md",
            ".claude/agent-memory/coder/MEMORY.md",
            ".claude/agent-memory/tester/MEMORY.md",
            ".claude/agent-memory/reviewer/MEMORY.md",
        ],
    },
}

SHARED_DOCS = [
    "docs/requirements/README.md",
    "docs/requirements/INDEX.md",
    "docs/requirements/REQ-TEMPLATE.md",
    "docs/implementation-plans/README.md",
    "docs/implementation-plans/INDEX.md",
    "docs/implementation-plans/IP-TEMPLATE.md",
    "docs/user-findings/README.md",
    "docs/user-findings/INDEX.md",
    "docs/user-findings/UF-TEMPLATE.md",
]

MECHANISMS = {
    "efficiency profiles": r"efficien(?:cy|t).{0,40}profile|profile.{0,40}efficien",
    "advisory token budget": r"token budget",
    "delta-first context": r"delta[- ]first",
    "evidence fingerprints": r"(?:evidence.{0,40})?fingerprint",
    "compact handoffs": (
        r"compact (?:reference-based )?handoff|reference-based handoff|handoffs? reference|"
        r"handoffs? compact"
    ),
    "early-exit completion gate": r"early[- ]exit|completion gate",
    "retry circuit breakers": r"circuit breaker|retry.{0,100}circuit|circuit.{0,100}retry",
    "capability routing": r"capability[- ]based|capability routing|fastest capable|lowest sufficient|least costly sufficient|route .{0,80} by (?:task )?capability|model or reasoning",
    "change-impact testing": r"change[- ]impact|impact[- ]selected|impact-based|impact map",
    "reviewer deduplication": r"stable finding|deduplicat",
    "context compaction": r"context compaction|compacts? context|compact checkpoint|stage[- ]boundary|stage checkpoint",
    "outcome calibration": r"(?:outcome|local|metadata-only) calibration|calibrat",
    "spawn-value gate": r"spawn[- ]value",
    "validation reserve": r"(?:validation[/, ]+review[/, ]+(?:and )?closeout|validation) reserve",
    "capability preflight": r"capability preflight|single preflight",
    "invalidation and cancellation": r"(?=.*invalidat)(?=.*cancel)",
    "assumption register": r"assumption register|material assumption",
    "failure classification": r"failure class|failure matrix",
    "single integrator": r"single[- ]integrator|single integrator",
    "conditional adjudication": r"(?:conditional|focused) adjudicat|adjudication trigger|adjudicator",
    "memory provenance": r"memory provenance|last confirmed|last-confirmed",
    "workflow conformance": r"workflow[- ]conformance",
}

ROOT_MECHANISM_ROWS = (
    ("Efficiency profiles", r"Economy.{0,80}Balanced.{0,80}Thorough.{0,120}workflow depth"),
    (
        "Token-budget guardrails",
        r"Token budget.{0,80}advisory.{0,140}mandatory.{0,120}Not measured",
    ),
    (
        "Delta-first context",
        r"changed files.{0,100}affected symbols.{0,120}direct dependencies.{0,120}widen",
    ),
    (
        "Evidence fingerprints",
        r"revision.{0,80}inputs.{0,100}(?:command|method).{0,120}"
        r"(?:environment|tool version).{0,120}timestamp.{0,100}result digest.{0,120}invalidat",
    ),
    (
        "Compact handoffs",
        r"(?:IDs|identifiers).{0,100}(?:file|symbol) references.{0,140}"
        r"(?:not|instead of).{0,100}(?:plans|code|logs)",
    ),
    ("Early exit", r"Stop optional investigation.{0,160}completion gate"),
    (
        "Retry circuit breakers",
        r"retry ceiling.{0,80}hard.{0,120}exhaustion stops.{0,180}"
        r"new hypothesis alone.{0,160}(?:user-raised|approved)",
    ),
    (
        "Capability-based reasoning",
        r"fastest capable.{0,120}(?:model|effort).{0,180}user settings.{0,100}safety",
    ),
    (
        "Change-impact testing",
        r"tests closest.{0,120}changed behavior.{0,160}(?:expand|risk|failure|required gates)",
    ),
    (
        "Reviewer deduplication",
        r"(?:Merge|deduplicat).{0,100}duplicate findings.{0,100}stable IDs",
    ),
    (
        "Context compaction",
        r"canonical checkpoint.{0,120}stage boundaries.{0,160}references",
    ),
    (
        "Outcome calibration",
        r"metadata-only outcomes.{0,160}without storing prompts or code",
    ),
    (
        "Spawn-value gate",
        r"Delegate only when.{0,180}(?:expertise|independence|verification|latency).{0,180}"
        r"coordination cost",
    ),
    (
        "Validation/review/closeout reserve",
        r"advisory portion.{0,120}validation, review, and closeout",
    ),
    (
        "Capability preflight",
        r"(?:agent|tool).{0,100}permission.{0,100}concurrency.{0,100}observability.{0,120}"
        r"once per task",
    ),
    (
        "Invalidation and cancellation",
        r"dependent evidence stale.{0,120}stop obsolete work.{0,160}upstream input changes",
    ),
    (
        "Assumption register",
        r"owner.{0,80}confidence.{0,80}evidence.{0,120}invalidation condition",
    ),
    (
        "Failure classification",
        r"Implementation defect.{0,180}Test defect.{0,180}Flaky result.{0,180}"
        r"Environment.{0,220}Missing dependency/tooling.{0,220}Pre-existing failure"
        r".{0,180}Permission.{0,180}Unclear requirement",
    ),
    (
        "Single-integrator mode",
        r"one writer.{0,160}parallel editing.{0,160}contention",
    ),
    (
        "Conditional adjudication",
        r"only for conflicts.{0,120}Low confidence.{0,120}elevated risk.{0,160}"
        r"independent verification",
    ),
    (
        "Memory provenance",
        r"source.{0,100}revision.{0,120}last confirmation.{0,160}"
        r"(?:invalidation|review condition)",
    ),
    (
        "Workflow conformance",
        r"approval.{0,100}routing.{0,100}budgets.{0,100}retries.{0,100}"
        r"leases.{0,100}privacy.{0,100}fallback",
    ),
)

PROMPT_REQUIRED_FIELDS = (
    "Workflow depth",
    "Efficiency profile",
    "Token budget",
    "Execution mode",
    "Max parallel subagents",
    "Max retries per node",
    "Validation/review/closeout reserve",
    "Integration mode",
    "Local metrics",
    "Task",
)

PROMPT_OPTIONAL_FIELDS = ("Coder max", "Tester max", "Reviewer max")

PROMPT_VALUE_PATTERNS = {
    "Workflow depth": r"(?:Auto|Direct|Lite|Standard|Full|<Auto\|Direct\|Lite\|Standard\|Full>)",
    "Efficiency profile": r"(?:Economy|Balanced|Thorough|<Economy\|Balanced\|Thorough>)",
    "Token budget": r"(?:Auto|[1-9][0-9]*|<Auto\|positive integer>)",
    "Execution mode": r"(?:Sequential|Parallel|<Sequential\|Parallel>)",
    "Max parallel subagents": r"(?:[1-9][0-9]*|<positive integer, default 4>)",
    "Max retries per node": r"(?:[0-9]+|<non-negative integer, default 1>)",
    "Validation/review/closeout reserve": (
        r"(?:(?:[1-9]|[1-9][0-9])%|<1-99%, default 25%>)"
    ),
    "Integration mode": (
        r"(?:Auto|Leased writers|Single integrator|"
        r"<Auto\|Leased writers\|Single integrator>)"
    ),
    "Local metrics": r"(?:Off|On|<Off\|On>|<Off\|On, default Off>)",
    "Coder max": r"(?:[1-9][0-9]*|<positive integer, optional>)",
    "Tester max": r"(?:[1-9][0-9]*|<positive integer, optional>)",
    "Reviewer max": r"(?:[1-9][0-9]*|<positive integer, optional>)",
}

CANONICAL_PROMPT_DEFAULTS = {
    "Workflow depth": "Auto",
    "Efficiency profile": "Balanced",
    "Token budget": "Auto",
    "Execution mode": "<Sequential|Parallel>",
    "Max parallel subagents": "<positive integer, default 4>",
    "Max retries per node": "1",
    "Validation/review/closeout reserve": "25%",
    "Integration mode": "Auto",
    "Local metrics": "Off",
}

CANONICAL_PLAN_DEFAULTS = {
    "Requested workflow depth": "Auto",
    "Efficiency profile": "Balanced",
    "Token budget": "Auto",
    "Max parallel subagents": "4",
    "Max retries per node": "1",
    "Validation/review/closeout reserve": "25%",
    "Integration mode": "Auto",
    "Local metrics": "Off",
}

PLAN_ROLE_CAP_DEFAULTS = {
    "Coder max": "Inherit global",
    "Tester max": "Inherit global",
    "Reviewer max": "Inherit global",
}

PLAN_DEFAULT_SECTIONS = {
    "Requested workflow depth": r"Work Classification",
    "Efficiency profile": (
        r"(?:Efficiency And Budget(?: Controls)?|Resource-Efficiency Controls|Resource Controls)"
    ),
    "Token budget": (
        r"(?:Efficiency And Budget(?: Controls)?|Resource-Efficiency Controls|Resource Controls)"
    ),
    "Max retries per node": (
        r"(?:Efficiency And Budget(?: Controls)?|Resource-Efficiency Controls|Resource Controls)"
    ),
    "Validation/review/closeout reserve": (
        r"(?:Efficiency And Budget(?: Controls)?|Resource-Efficiency Controls|Resource Controls)"
    ),
    "Local metrics": (
        r"(?:Efficiency And Budget(?: Controls)?|Resource-Efficiency Controls|Resource Controls)"
    ),
    "Integration mode": (
        r"(?:Integration Mode|Execution Mode|Efficiency And Budget(?: Controls)?|"
        r"Resource-Efficiency Controls|Resource Controls)"
    ),
    "Max parallel subagents": r"Execution Mode",
    "Coder max": r"Execution Mode",
    "Tester max": r"Execution Mode",
    "Reviewer max": r"Execution Mode",
}

PLAN_CANONICAL_SECTION_GROUPS = (
    ("Work Classification", r"Work Classification", 1, 1),
    (
        "resource controls",
        r"(?:Efficiency And Budget(?: Controls)?|Resource-Efficiency Controls|Resource Controls)",
        1,
        1,
    ),
    ("Execution Mode", r"Execution Mode", 1, 1),
    ("Integration Mode", r"Integration Mode", 0, 1),
)

FAILURE_CLASSES = {
    "implementation defect": r"implementation\s+defect",
    "test defect": r"test\s+defect",
    "flaky result": r"flaky\s+result",
    "environment": r"\benvironment\b",
    "missing dependency/tooling": r"missing\s+dependency/tooling",
    "pre-existing failure": r"pre-existing\s+failure",
    "permission": r"\bpermission\b",
    "unclear requirement": r"unclear\s+requirement",
}

OBSOLETE_CONTROLS = (
    "Max retries per node: Auto",
    "Validation reserve:",
    "Write strategy:",
    "`Distributed writes`",
    "Parallelism: Auto",
    "Advisory token budget:",
)

RETRY_CONTRACT_PATTERNS = {
    "hard retry ceiling": r"hard\s+ceiling",
    "changed retry evidence": r"(?:changed|new) (?:state|input|evidence|hypothesis|code|command)",
    "exhaustion stops the node": (
        r"exhaust(?:ion|ed).{0,160}stop(?:s|ped)?\s+(?:the|that)\s+node|"
        r"stop(?:s|ped)?\s+(?:the|that)\s+node.{0,160}exhaust"
    ),
    "new hypotheses do not reset exhaustion": (
        r"new\s+hypothesis\s+alone\s+does\s+not\s+reset"
    ),
    "retries after exhaustion need authority": (
        r"user[- ]raised ceiling|approved plan revision.{0,100}materially new node"
    ),
}

CONTRACT_POLARITY_PATTERNS = {
    "negated hard retry ceiling": (
        r"\b(?:is|are|was|were|be|becomes?|remains?)\s+"
        r"(?:explicitly\s+)?(?:not|never)\s+(?:an?\s+)?"
        r"hard(?:\s+retry)?\s+ceiling\b|"
        r"\bhard(?:\s+retry)?\s+ceiling\b.{0,80}"
        r"(?:does not apply|is optional|may be ignored|can be exceeded)|"
        r"\bretry\s+(?:limit|ceiling|budget)\b.{0,40}\b"
        r"(?:is|becomes?|remains?)\s+(?:soft|optional|advisory|unenforced)\b"
    ),
    "continuation after retry exhaustion": (
        r"\b(?:after|once|upon|following)\s+(?:the\s+)?(?:retry\s+)?"
        r"exhaustion\b[^.;:\n]{0,120}\b(?:agents?|the workflow|the node|it)\b"
        r"[^.;:\n]{0,80}\b(?:may|can|should|will|shall)\b(?!\s+not\b)"
        r"[^.;:\n]{0,60}\b(?:continue|proceed|retry|resume)\b|"
        r"\b(?:retry\s+)?(?:budget|limit|ceiling)\s+is\s+exhausted\b"
        r"[^.;:\n]{0,120}\b(?:may|can|should|will|shall)\b(?!\s+not\b)"
        r"[^.;:\n]{0,60}\b(?:continue|proceed|retry|resume)\b"
    ),
    "new hypothesis resets exhausted retries": (
        r"\b(?:a\s+)?new\s+hypothesis\b"
        r"(?![^.;:\n]{0,100}\b(?:does\s+not|cannot|never)\b"
        r"[^.;:\n]{0,40}\b(?:reset|restore|refresh|renew))"
        r"[^.;:\n]{0,100}\b"
        r"(?:reset|restore|refresh|renew)(?:s|ed|ing)?\b"
        r"[^.;:\n]{0,100}\b(?:exhausted\s+)?retry\s+"
        r"(?:allowance|budget|limit|ceiling|counter)\b"
    ),
    "retry after exhaustion without authority": (
        r"\bretr(?:y|ies)\s+after\s+(?:retry\s+)?exhaustion\b"
        r"[^.;:\n]{0,100}\b(?:need|needs|require|requires)\s+no\b"
        r"[^.;:\n]{0,80}\b(?:approval|authority|revised\s+plan)\b|"
        r"\b(?:after|once|upon)\s+(?:retry\s+)?exhaustion\b"
        r"[^.;:\n]{0,120}\b(?:may|can|should|will|shall)\b(?!\s+not\b)"
        r"[^.;:\n]{0,80}\bretr(?:y|ies)\b[^.;:\n]{0,100}\bwithout\b"
        r"[^.;:\n]{0,80}\b(?:approval|authority|user-raised ceiling|"
        r"approved plan revision)\b"
    ),
}

LEASE_CONTRACT_PATTERNS = {
    "exclusive write ownership": (
        r"exclusive\s+(?:write\s+)?lease|one\s+active\s+write\s+lease"
    ),
    "never-active immediate release": (
        r"never[- ]active.{0,100}(?:release|released).{0,40}immediate|"
        r"(?:release|released).{0,40}never[- ]active.{0,40}immediate|"
        r"(?:release|released).{0,40}immediate.{0,80}never[- ]active"
    ),
    "active lease quarantine": r"(?:retain(?:ed)?|quarantin(?:e|ed)).{0,100}(?:active writer|lease)|"
    r"(?:active writer|lease).{0,100}(?:retain(?:ed)?|quarantin(?:e|ed))",
    "active release waits for confirmed stop and reconciliation": (
        r"(?:active writer|active[- ]writer|active work).{0,260}"
        r"(?:stop|finish).{0,220}(?:last(?:[- ]|\s+)write|write\s+state).{0,180}"
        r"(?:then|after.{0,80}(?:confirm|reconcil)).{0,120}"
        r"(?:release|reassign)"
    ),
    "last-write reconciliation": (
        r"last(?:[- ]|\s+)write(?:\s+state)?.{0,30}reconcil"
    ),
    "stale results are never integrated": (
        r"never\s+integrat.{0,80}(?:stale|obsolete|invalidat)|"
        r"(?:stale|obsolete|invalidat).{0,80}never\s+integrat"
    ),
}

FINGERPRINT_CONTRACT_PATTERNS = {
    "revision or worktree state": r"revision|worktree",
    "relevant inputs or hashes": r"input|hash",
    "command or method": r"command|method",
    "environment and tool version": (
        r"environment(?:\s+details?)?\s+and\s+(?:the\s+)?tool\s+version|"
        r"tool\s+version\s+and\s+(?:the\s+)?environment"
    ),
    "timestamp": r"timestamp|observation\s+time",
    "result digest": r"result\s+digest",
    "invalidation condition": r"invalidat",
}

UNTRUSTED_CONTENT_CONTRACT_PATTERNS = {
    "source and comment coverage": r"source files?.{0,80}code comments?",
    "log and finding coverage": r"logs?.{0,80}(?:user )?findings?",
    "web and tool-output coverage": r"web (?:pages?|content).{0,80}tool output",
    "untrusted-data classification": r"untrusted\s+data",
    "non-instruction classification": (
        r"not\s+(?:executable\s+|workflow\s+)?instructions"
    ),
    "declared authority": r"(?:declared )?(?:source-of-truth|authority) chain",
    "reviewed skills": r"reviewed\s+native\s+skills",
    "embedded directive refusal": r"(?:never|do not|not)\s+obey",
    "conflict escalation": r"(?:suspicious\s+instructions?|authority\s+conflicts?)",
}

EXTERNAL_TOOL_DATA_CONTRACT_PATTERNS = {
    "generic minimal non-sensitive inputs": (
        r"generic.{0,40}minimal.{0,40}non-sensitive|"
        r"generic,\s*minimal,\s*(?:and\s+)?non-sensitive"
    ),
    "absolute credential exclusion": (
        r"never.{0,80}(?:send|encode).{0,100}secrets.{0,60}credentials."
        r"{0,60}(?:access\s+)?tokens.{0,60}private\s+keys|"
        r"secrets.{0,60}credentials.{0,60}(?:access\s+)?tokens.{0,60}"
        r"private\s+keys.{0,100}never.{0,40}(?:sent|encoded)"
    ),
    "protected project-data coverage": (
        r"proprietary\s+source.{0,100}(?:repository\s+content)?.{0,120}"
        r"(?:customer\s+or\s+personal\s+data|customer\s+data.{0,40}"
        r"personal\s+data).{0,100}private\s+URLs.{0,100}sensitive\s+identifiers"
    ),
    "external-surface coverage": (
        r"(?:web(?:-search)?\s+(?:quer(?:y|ies)|search(?:es)?)|web\s+searches)"
        r".{0,140}fetched\s+URLs?.{0,140}(?:connector\s+or\s+MCP\s+calls?|"
        r"connector.{0,30}MCP).{0,140}remote\s+API.{0,140}"
        r"(?:third-party\s+tool\s+inputs?|external\s+tool\s+inputs?)"
    ),
    "specific-disclosure authorization": (
        r"user\s+explicitly\s+authorizes.{0,40}(?:that|the)\s+specific\s+disclosure|"
        r"explicit\s+user\s+authorization.{0,40}(?:that|the)\s+specific\s+disclosure"
    ),
    "general approval is insufficient": (
        r"(?:general\s+)?task\s+approval.{0,100}"
        r"(?:request\s+to\s+research|research\s+request).{0,100}"
        r"not.{0,40}disclosure\s+authorization"
    ),
    "safer alternatives": (
        r"(?:local|offline).{0,120}redact.{0,120}synthetic"
    ),
}

FIRST_RUN_ADAPTATION_CONTRACT_PATTERNS = {
    "explicit user trigger": (
        r"(?:only when|after) (?:the )?user explicitly (?:requests?|approves?)|"
        r"explicit(?:ly)?(?: user)? request"
    ),
    "bounded repository-wide inventory": (
        r"bounded.{0,140}(?:repository-wide|repo-wide).{0,140}(?:inventory|scan)"
    ),
    "evidence-first discovery": r"evidence-first",
    "high-value discovery sources": (
        r"(?=.*manifests?)(?=.*lockfiles?)(?=.*(?:CI|continuous integration))"
        r"(?=.*test\s+configuration)(?=.*representative entry points?)"
    ),
    "scan exclusions": (
        r"(?=.*\.git)(?=.*dependenc)(?=.*generated)(?=.*build\s+artifacts?)"
        r"(?=.*vendored)(?=.*binaries)(?=.*secrets)"
    ),
    "fact provenance": (
        r"(?:(?:proposed durable facts?|proposed facts?|each proposed fact|durable facts?).{0,200}"
        r"(?:repository )?source(?: path)?.{0,140}confidence|"
        r"(?:repository )?source(?: path)?.{0,140}confidence.{0,200}"
        r"(?:proposed )?durable fact)"
    ),
    "unknown and conflict handling": (
        r"unknown.{0,140}conflicting.{0,180}"
        r"(?:not guessed|instead of guessing|remain explicit|unresolved)"
    ),
    "revisioned exact diff": (
        r"(?:revisioned exact|exact .{0,80}diff.{0,100}(?:proposal )?revision)"
    ),
    "approval before instruction write": (
        r"(?=.*(?:(?:stop|stops).*(?:without|before) writing|"
        r"no instruction file is changed))"
        r"(?=.*(?:explicitly\s+approves?|explicit\s+(?:user\s+)?approval))"
    ),
    "instruction-only authorization": (
        r"(?:(?:only the displayed|apply only the displayed).{0,100}"
        r"(?:instruction-file|AGENTS\.md|CLAUDE\.md) (?:diff|changes).{0,220}"
        r"(?:never|does not|no).{0,120}product[- ]code|"
        r"adaptation approval.{0,160}(?:never authorizes?|does not authorize).{0,80}"
        r"product[- ]code)"
    ),
    "protected workflow invariants": (
        r"(?=.*(?:preserve|preserves|keeps|does not delete|do not delete|"
        r"must not delete|without deleting))"
        r"(?=.*(?:workflow.{0,20}invariants?|authority|source-of-truth))"
        r"(?=.*(?:validation|review))(?=.*(?:memory|conformance))"
    ),
    "post-merge validation": (
        r"(?:validate|validation).{0,160}(?:first-run adaptation )?"
        r"(?:scenario|workflow-conformance|Markdown)|"
        r"run.{0,220}(?:first-run adaptation )?(?:scenario|workflow-conformance)"
    ),
    "delta-first refresh": r"(?:later )?refresh.{0,180}delta-first",
}

LICENSE_NOTICE_CONTRACT_PATTERNS = {
    "creator attribution": r"Victor Alexander Daud",
    "MIT permission-notice retention": (
        r"retain(?:ing)?.{0,140}(?:MIT permission notice|complete\s+MIT notice)"
    ),
    "non-destructive third-party notice guidance": (
        r"THIRD_PARTY_NOTICES\.md.{0,220}(?:instead of|without|never|do not)"
        r".{0,120}"
        r"(?:replac|overwrit).{0,80}(?:target|project).{0,40}license|"
        r"(?:do not|never|without).{0,100}(?:replac|overwrit).{0,100}"
        r"(?:target|project).{0,40}license.{0,180}THIRD_PARTY_NOTICES\.md"
    ),
}

MIT_LICENSE_PATTERNS = {
    "MIT license label": r"^MIT License\s*$",
    "creator copyright": r"^Copyright \(c\) 2026 Victor Alexander Daud\s*$",
    "MIT permission grant": (
        r"Permission is hereby granted, free of charge, to any person obtaining a copy"
    ),
    "notice-retention condition": (
        r"The above copyright notice and this permission notice shall be included in all"
        r"\s+copies or substantial portions of the Software\."
    ),
    "warranty disclaimer": (
        r'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND'
    ),
    "liability disclaimer": (
        r"IN NO EVENT SHALL THE\s+AUTHORS OR COPYRIGHT HOLDERS BE LIABLE"
    ),
}

NOTICE_FILE_PATTERNS = {
    "document title": r"^# Third-Party Notices\s*$",
    "project name": r"^## VicXander Agentic Workflows\s*$",
    **MIT_LICENSE_PATTERNS,
}

EMBEDDED_CONFORMANCE_SCENARIOS = {
    "WF-01": r"Economy.{0,100}High-risk.{0,160}Full.{0,160}safety",
    "WF-02": r"Token budget: Auto.{0,180}Not measured",
    "WF-03": r"validation reserve.{0,180}25%",
    "WF-04": r"Direct.{0,180}localized.{0,120}reversible",
    "WF-05": r"subagent.{0,180}spawn-value",
    "WF-06": r"retry budget.{0,180}circuit breaker.{0,180}hard ceiling",
    "WF-07": r"fingerprint input changes.{0,180}Invalidate",
    "WF-08": r"dependency.{0,180}cancel.{0,240}quarantine.{0,180}last-write",
    "WF-09": r"overlapping files.{0,180}(?:exclusive leases|single-integrator)",
    "WF-10": r"same defect.{0,180}stable finding ID",
    "WF-11": r"evidence conflicts.{0,180}adjudication.{0,180}security",
    "WF-12": r"stage completes.{0,180}compact checkpoint",
    "WF-13": r"acceptance criteria.{0,180}completion gate.{0,120}exit early",
    "WF-14": r"runtime lacks.{0,180}preflight.{0,180}fallback",
    "WF-15": r"memory note.{0,180}(?:source|provenance).{0,180}stale",
    "WF-16": r"material assumption.{0,180}owner.{0,180}invalidation",
    "WF-17": r"failure occurs.{0,240}Implementation defect.{0,400}Unclear requirement",
    "WF-18": r"model or lower reasoning.{0,180}lowest sufficient capability",
    "WF-19": r"subset of tests.{0,180}changed files.{0,180}expand",
    "WF-20": r"handoff.{0,180}(?:task-packet|evidence IDs)",
    "WF-21": r"Local outcome calibration.{0,240}Local metrics.{0,180}Off.{0,240}no uploader",
    "WF-22": r"efficiency setting conflicts.{0,240}safety.{0,180}stricter",
    "WF-23": r"Sequential.{0,240}at most one active subagent.{0,240}Parallel.{0,300}waits",
    "WF-24": (
        r"Proposed.{0,180}explicit user approval.{0,180}current revision.{0,260}"
        r"In Progress.{0,220}material revision.{0,180}repeats the gate"
    ),
    "WF-25": (
        r"invalid explicit.{0,180}(?:surface|clarif).{0,180}(?:not|never).{0,100}"
        r"(?:default|reinterpret).{0,240}unsupported.{0,180}(?:fallback|report)"
    ),
    "WF-26": (
        r"source file.{0,100}code comment.{0,100}log.{0,100}user finding.{0,100}"
        r"web page.{0,100}tool output.{0,220}untrusted data.{0,160}"
        r"(?:not executable instructions|do not obey).{0,220}authority chain"
    ),
    "WF-27": (
        r"(?:external research|third-party tool).{0,180}(?:generic|minimal).{0,160}"
        r"(?:never send|never.{0,60}secrets).{0,220}proprietary source.{0,180}"
        r"(?:customer or personal data|personal data).{0,160}private URLs.{0,160}"
        r"sensitive identifiers.{0,220}(?:specific disclosure|explicitly authorizes)."
        r"{0,220}(?:task approval|research request).{0,100}not disclosure authorization"
    ),
    "WF-28": (
        r"(?=.*first-run repository adaptation)(?=.*bounded)(?=.*evidence-first)"
        r"(?=.*source)(?=.*confidence)(?=.*revisioned exact)(?=.*AGENTS\.md)"
        r"(?=.*without writing)(?=.*explicitly approves)(?=.*product-code)"
        r"(?=.*preserve)(?=.*workflow invariant)(?=.*delta-first)"
    ),
}

PROVIDER_SCENARIO_COUNTS = {
    "codex": ("CF", 27),
    "github-copilot": ("CF", 27),
    "claude": ("C", 30),
}

PROVIDER_UNTRUSTED_CONTENT_SCENARIOS = {
    "codex": "CF-25",
    "github-copilot": "CF-25",
    "claude": "C-28",
}

PROVIDER_EXTERNAL_TOOL_DATA_SCENARIOS = {
    "codex": "CF-26",
    "github-copilot": "CF-26",
    "claude": "C-29",
}

PROVIDER_FIRST_RUN_ADAPTATION_SCENARIOS = {
    "codex": "CF-27",
    "github-copilot": "CF-27",
    "claude": "C-30",
}

PROVIDER_PRIVACY_SCENARIOS = {
    "codex": "CF-20",
    "github-copilot": "CF-21",
    "claude": "C-26",
}

PROVIDER_SCENARIO_MAPS = {
    "codex": {
        "efficiency profiles": "CF-02",
        "advisory token budget": "CF-05",
        "delta-first context": "CF-07",
        "evidence fingerprints": "CF-08",
        "compact handoffs": "CF-09",
        "early-exit completion gate": "CF-10",
        "retry circuit breakers": "CF-11",
        "capability routing": "CF-12",
        "change-impact testing": "CF-13",
        "reviewer deduplication": "CF-14",
        "context compaction": "CF-20",
        "outcome calibration": "CF-22",
        "spawn-value gate": "CF-16",
        "validation reserve": "CF-05",
        "capability preflight": "CF-01",
        "invalidation and cancellation": "CF-17",
        "assumption register": "CF-18",
        "failure classification": "CF-11",
        "single integrator": "CF-19",
        "conditional adjudication": "CF-14",
        "memory provenance": "CF-21",
        "workflow conformance": "CF-24",
    },
    "github-copilot": {
        "efficiency profiles": "CF-03",
        "advisory token budget": "CF-03",
        "delta-first context": "CF-11",
        "evidence fingerprints": "CF-12",
        "compact handoffs": "CF-11",
        "early-exit completion gate": "CF-19",
        "retry circuit breakers": "CF-15",
        "capability routing": "CF-06",
        "change-impact testing": "CF-14",
        "reviewer deduplication": "CF-17",
        "context compaction": "CF-13",
        "outcome calibration": "CF-22",
        "spawn-value gate": "CF-08",
        "validation reserve": "CF-03",
        "capability preflight": "CF-06",
        "invalidation and cancellation": "CF-12",
        "assumption register": "CF-23",
        "failure classification": "CF-16",
        "single integrator": "CF-10",
        "conditional adjudication": "CF-17",
        "memory provenance": "CF-20",
        "workflow conformance": "CF-22",
    },
    "claude": {
        "efficiency profiles": "C-01",
        "advisory token budget": "C-02",
        "delta-first context": "C-03",
        "evidence fingerprints": "C-05",
        "compact handoffs": "C-04",
        "early-exit completion gate": "C-07",
        "retry circuit breakers": "C-08",
        "capability routing": "C-09",
        "change-impact testing": "C-10",
        "reviewer deduplication": "C-11",
        "context compaction": "C-06",
        "outcome calibration": "C-12",
        "spawn-value gate": "C-13",
        "validation reserve": "C-14",
        "capability preflight": "C-15",
        "invalidation and cancellation": "C-16",
        "assumption register": "C-17",
        "failure classification": "C-18",
        "single integrator": "C-19",
        "conditional adjudication": "C-20",
        "memory provenance": "C-21",
        "workflow conformance": "C-22",
    },
}

CLAUDE_COVERAGE_MAP = (
    ("Efficiency profiles and advisory budget", ("C-01", "C-02")),
    ("Delta-first context and compact handoffs", ("C-03", "C-04")),
    ("Fingerprinted evidence and checkpoints", ("C-05", "C-06")),
    ("Early exit and retry circuit breaker", ("C-07", "C-08")),
    ("Capability-based model/reasoning routing", ("C-09",)),
    ("Change-impact test selection", ("C-10",)),
    ("Reviewer deduplication and conditional adjudication", ("C-11", "C-20")),
    ("Local outcome calibration", ("C-12",)),
    (
        "Spawn-value gate and validation/review/closeout reserve",
        ("C-13", "C-14"),
    ),
    ("Capability preflight", ("C-15",)),
    ("Invalidation/cancellation and assumptions", ("C-16", "C-17")),
    ("Failure classification", ("C-18",)),
    ("Single integrator mode", ("C-19",)),
    ("Memory provenance and freshness", ("C-21",)),
    ("Workflow conformance itself", ("C-22",)),
    (
        "Existing approval, route, concurrency, privacy, and control-input invariants",
        ("C-23", "C-24", "C-25", "C-26", "C-27"),
    ),
    ("Untrusted-content boundary", ("C-28",)),
    ("External-tool data minimization", ("C-29",)),
    ("Approval-gated first-run repository adaptation", ("C-30",)),
)

PROVIDER_BASE_SCENARIOS = {
    "codex": {
        "CF-01": {
            "omitted defaults": (
                r"omits optional.{0,220}Balanced.{0,180}Auto.{0,220}25%.{0,180}"
                r"Sequential.{0,180}Off"
            ),
            "invalid control clarification": (
                r"invalid explicit.{0,120}clarif|clarif.{0,120}invalid explicit"
            ),
            "unsupported-control fallback": (
                r"(?:valid.{0,80})?unsupported.{0,160}(?:safe )?fallback"
            ),
            "no silent reinterpretation": (
                r"(?:instead of|rather than|never|not|do not).{0,100}"
                r"silent(?:ly)?.{0,40}reinterpret"
            ),
        },
        "CF-03": {
            "Direct route safety": (
                r"localized.{0,120}reversible.{0,120}Low-risk.{0,260}"
                r"no subagents.{0,260}impact-based validation.{0,260}"
                r"(?:scope|risk|uncertainty).{0,180}reclassif"
            ),
        },
        "CF-04": {
            "approval revision lifecycle": (
                r"Proposed.{0,220}explicitly chooses Approve.{0,220}current plan revision"
                r".{0,280}In Progress.{0,260}material.{0,160}Proposed.{0,160}"
                r"(?:repeat|approval)"
            ),
        },
        "CF-06": {
            "unobservable usage remains unmeasured": (
                r"no token-use counter.{0,220}Not measured.{0,180}planning ratio"
                r".{0,180}(?:safety|quality) gates remain unchanged"
            ),
        },
        "CF-15": {
            "mandatory security coverage": (
                r"security coverage.{0,180}explicit.{0,220}never omitted.{0,180}"
                r"(?:cap|budget|profile|adjudication)"
            ),
        },
        "CF-23": {
            "execution modes and caps": (
                r"Sequential.{0,180}at most one subagent.{0,220}caps are ignored"
                r".{0,240}Parallel.{0,260}configured ceilings.{0,220}waits"
                r".{0,140}reconciles"
            ),
        },
    },
    "github-copilot": {
        "CF-01": {
            "safe Direct route": (
                r"localized.{0,120}reversible.{0,120}Low-risk.{0,300}"
                r"impact-targeted validation.{0,180}does not claim.{0,140}subagents"
            ),
        },
        "CF-02": {
            "unsafe Direct escalation": (
                r"High-risk.{0,260}escalates to `Full`.{0,180}security review"
                r".{0,180}does not start before approval"
            ),
        },
        "CF-04": {
            "approval revision lifecycle": (
                r"Proposed.{0,220}Approve, Revise, or Stop.{0,220}current plan revision"
                r".{0,220}In Progress.{0,260}material.{0,180}Proposed.{0,180}"
                r"(?:repeat|gate)"
            ),
        },
        "CF-05": {
            "two-task cloud approval": (
                r"(?:planning-only|planning stage).{0,160}Proposed"
                r".{0,240}later Orchestrator task"
                r".{0,220}user-approved.{0,180}commit.{0,180}"
                r".{0,400}never approves the plan"
            ),
            "Orchestrator owns planning lease": (
                r"first task uses Orchestrator.{0,160}pre-plan lease"
            ),
            "direct role bounds": (
                r"Direct Architect.{0,120}pre-plan lease.{0,220}"
                r"direct Coder.{0,180}In Progress.{0,180}"
                r"Orchestrator-issued write lease"
            ),
        },
        "CF-07": {
            "sequential serialization": (
                r"at most one subagent.{0,160}caps are ignored.{0,180}"
                r"integrated before the next worker"
            ),
        },
        "CF-09": {
            "exclusive writer lease": (
                r"does not grant simultaneous leases.{0,180}"
                r"(?:serializes|Single integrator).{0,180}"
                r"without a valid lease refuses to write"
            ),
        },
        "CF-18": {
            "mandatory security coverage": (
                r"security-sensitive.{0,220}explicit disposition.{0,220}"
                r"never remove mandatory security review"
            ),
        },
        "CF-24": {
            "omitted-only defaults": r"Only the omitted control.{0,100}default",
            "invalid control surfaced": (
                r"surfaces? the explicit invalid|explicit invalid.{0,100}(?:surface|clarif)"
            ),
            "no silent default": r"instead of silently.{0,100}(?:default|substitut)",
            "unsupported-control fallback": r"valid but unsupported.{0,180}(?:safe )?fallback",
        },
    },
    "claude": {
        "C-20": {
            "mandatory security coverage": (
                r"security review.{0,180}(?:still occurs|required|mandatory)"
            ),
        },
        "C-23": {
            "Direct route restriction": (
                r"(?:non-localized|irreversible).{0,220}Direct.{0,180}"
                r"escalates.{0,180}planned route"
            ),
        },
        "C-24": {
            "approval revision lifecycle": (
                r"Proposed.{0,260}explicit user approval.{0,180}plan revision"
                r".{0,240}In Progress.{0,220}material revision.{0,180}"
                r"Proposed.{0,160}approval again"
            ),
            "separate Orchestrator runs": (
                r"separate Orchestrator planning and.{0,80}implementation runs"
            ),
            "direct Coder bounds": (
                r"Direct\s+Coder.{0,160}bounded node.{0,100}In Progress"
                r".{0,160}Orchestrator-issued lease"
            ),
        },
        "C-25": {
            "execution modes and caps": (
                r"Sequential.{0,140}at most one active subagent.{0,180}Parallel"
                r".{0,220}within all ceilings.{0,180}waits.{0,120}reconciles"
            ),
        },
        "C-27": {
            "invalid control surfaced": (
                r"invalid explicit.{0,100}(?:surface|clarif)|"
                r"(?:surface|clarif).{0,100}invalid explicit"
            ),
            "no silent default": r"never silently.{0,100}default",
            "unsupported-control fallback": (
                r"valid-but-unsupported.{0,180}(?:safe|supported) fallback"
            ),
        },
    },
}

PROVIDER_ROLE_FILES = {
    "codex": {
        role: f".codex/agents/{role}.toml"
        for role in ("orchestrator", "architect", "coder", "tester", "reviewer")
    },
    "github-copilot": {
        role: f".github/agents/{role}.agent.md"
        for role in ("orchestrator", "architect", "coder", "tester", "reviewer")
    },
    "claude": {
        role: f".claude/agents/{role}.md"
        for role in ("orchestrator", "architect", "coder", "tester", "reviewer")
    },
}

PROVIDER_FAILURE_AUTHORITIES = {
    "codex": ".codex/agents/README.md",
    "github-copilot": ".github/AGENTIC-WORKFLOW.md",
    "claude": ".claude/AGENTIC-WORKFLOW.md",
}

EXPECTED_ROLES = {"orchestrator", "architect", "coder", "tester", "reviewer"}


errors: list[str] = []
checks = 0


def fail(message: str) -> None:
    errors.append(message)


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        fail(message)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def repository_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not IGNORED_PARTS.intersection(path.relative_to(ROOT).parts)
    ]


def is_text_file(path: Path) -> bool:
    return path.name in TEXT_NAMES or path.suffix.lower() in TEXT_SUFFIXES


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"{relative(path)} is not readable UTF-8 text: {exc}")
        return ""


def check_text_hygiene(paths: list[Path], *, require_lf: bool = False) -> None:
    for path in paths:
        if not is_text_file(path):
            continue
        text = read_text(path)
        if not text:
            continue
        check(text.endswith("\n"), f"{relative(path)} must end with a newline")
        if require_lf:
            check(
                b"\r\n" not in path.read_bytes(),
                f"{relative(path)} must use LF line endings, "
                "matching .gitattributes eol=lf",
            )
        for number, line in enumerate(text.splitlines(), start=1):
            if line.endswith((" ", "\t")):
                fail(f"{relative(path)}:{number} has trailing whitespace")


FENCE_PATTERN = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def fence_open(line: str) -> tuple[str, int, str] | None:
    """Return a valid CommonMark fence marker and info string."""
    match = FENCE_PATTERN.match(line)
    if not match:
        return None
    marker = match.group(1)
    info = match.group(2).strip()
    if marker[0] == "`" and "`" in info:
        return None
    return marker[0], len(marker), info


def is_fence_close(line: str, marker: str, minimum_length: int) -> bool:
    return (
        re.fullmatch(
            rf" {{0,3}}{re.escape(marker)}{{{minimum_length},}}[ \t]*",
            line,
        )
        is not None
    )


def fenced_blocks(text: str) -> list[tuple[str, str, int]]:
    """Return (info string, body, one-based opening line) for valid fenced blocks."""
    blocks: list[tuple[str, str, int]] = []
    marker: str | None = None
    minimum_length = 0
    info = ""
    opening_line = 0
    body: list[str] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if marker is None:
            opened = fence_open(line)
            if opened is None:
                continue
            marker, minimum_length, info = opened
            opening_line = number
            body = []
            continue
        if is_fence_close(line, marker, minimum_length):
            blocks.append((info, "\n".join(body), opening_line))
            marker = None
            minimum_length = 0
            info = ""
            opening_line = 0
            body = []
        else:
            body.append(line)
    return blocks


def unclosed_fence(text: str) -> tuple[str, int, int] | None:
    """Return an unclosed marker, its minimum length, and opening line."""
    marker: str | None = None
    minimum_length = 0
    opening_line = 0
    for number, line in enumerate(text.splitlines(), start=1):
        if marker is None:
            opened = fence_open(line)
            if opened is not None:
                marker, minimum_length, _ = opened
                opening_line = number
        elif is_fence_close(line, marker, minimum_length):
            marker = None
            minimum_length = 0
            opening_line = 0
    if marker is None:
        return None
    return marker, minimum_length, opening_line


def check_fences(paths: list[Path]) -> None:
    for path in paths:
        if path.suffix.lower() != ".md":
            continue
        unclosed = unclosed_fence(
            markdown_without_html_comments(read_text(path))
        )
        check(
            unclosed is None,
            (
                f"{relative(path)}:{unclosed[2]} has an unclosed "
                f"{unclosed[0] * unclosed[1]} fence"
                if unclosed is not None
                else f"{relative(path)} has balanced fences"
            ),
        )


def table_pipe_count(line: str) -> int:
    """Count structural table pipes, ignoring escapes and inline-code pipes."""
    count = 0
    index = 0
    code_fence = 0
    while index < len(line):
        character = line[index]
        if character == "\\":
            index += 2
            continue
        if character == "`":
            run = 1
            while index + run < len(line) and line[index + run] == "`":
                run += 1
            if code_fence == 0:
                code_fence = run
            elif run == code_fence:
                code_fence = 0
            index += run
            continue
        if character == "|" and code_fence == 0:
            count += 1
        index += 1
    return count


def check_markdown_tables(paths: list[Path]) -> None:
    delimiter = re.compile(
        r"^\s*\|(?:\s*:?-{3,}:?\s*\|){2,}\s*$"
    )
    for path in paths:
        if path.suffix.lower() != ".md":
            continue
        lines = markdown_contract_text(read_text(path)).splitlines()
        for index, line in enumerate(lines):
            if not delimiter.match(line):
                continue
            expected = table_pipe_count(line)
            check(
                index > 0 and table_pipe_count(lines[index - 1]) == expected,
                f"{relative(path)}:{index + 1} table header/delimiter column mismatch",
            )
            row = index + 1
            while row < len(lines) and lines[row].lstrip().startswith("|"):
                check(
                    table_pipe_count(lines[row]) == expected,
                    f"{relative(path)}:{row + 1} table row has the wrong column count",
                )
                row += 1


def path_has_exact_case(path: Path) -> bool:
    """Return whether every path component uses the filesystem's stored casing."""
    normalized = Path(os.path.abspath(os.path.normpath(str(path))))
    current = Path(normalized.anchor)
    for part in normalized.parts[1:]:
        try:
            names = {child.name for child in current.iterdir()}
        except OSError:
            return False
        if part not in names:
            return False
        current /= part
    return True


def markdown_fragments(text: str) -> set[str]:
    """Return GitHub-style fragments for ATX headings and explicit HTML anchors."""
    fragments: set[str] = set()
    counts: Counter[str] = Counter()
    for line in markdown_contract_text(text).splitlines():
        heading = re.match(r"^ {0,3}#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$", line)
        if heading is not None:
            label = re.sub(r"<[^>]+>", "", heading.group(1))
            label = re.sub(r"[^\w\- ]", "", label.lower(), flags=re.UNICODE)
            base = re.sub(r"[ \t]+", "-", label.strip())
            if base:
                suffix = counts[base]
                fragment = base if suffix == 0 else f"{base}-{suffix}"
                counts[base] += 1
                fragments.add(fragment)
        for anchor in re.findall(
            r"<a\s+(?:name|id)=[\"']([^\"']+)[\"'][^>]*>",
            line,
            re.IGNORECASE,
        ):
            fragments.add(anchor)
    return fragments


def check_local_links(paths: list[Path]) -> None:
    """Validate local inline, image, and reference-link destinations."""
    for path in paths:
        if path.suffix.lower() != ".md":
            continue
        for raw_target in markdown_link_destinations(read_text(path)):
            target = raw_target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            path_part, separator, raw_fragment = target.partition("#")
            if re.match(r"^[a-z][a-z0-9+.-]*:", path_part, re.IGNORECASE):
                continue
            decoded_path = unquote(path_part.strip())
            fragment = unquote(raw_fragment.strip()) if separator else ""
            if not decoded_path:
                candidate = path
            elif decoded_path.startswith("/"):
                candidate = Path(decoded_path)
            else:
                candidate = path.parent / decoded_path
            exists = candidate.exists()
            check(exists, f"{relative(path)} links to missing local target {raw_target!r}")
            if exists:
                check(
                    path_has_exact_case(candidate),
                    (
                        f"{relative(path)} local link has non-portable path casing "
                        f"{raw_target!r}"
                    ),
                )
                fragment_source = (
                    candidate / "README.md"
                    if candidate.is_dir() and (candidate / "README.md").is_file()
                    else candidate
                )
                if fragment:
                    check(
                        fragment_source.is_file()
                        and fragment_source.suffix.lower() == ".md"
                        and fragment in markdown_fragments(read_text(fragment_source)),
                        (
                            f"{relative(path)} links to missing Markdown fragment "
                            f"{fragment!r} in {raw_target!r}"
                        ),
                    )


def markdown_without_fenced_code(text: str) -> str:
    """Mask fenced-code bodies while preserving line boundaries."""
    output: list[str] = []
    marker: str | None = None
    minimum_length = 0
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        ending = line[len(content) :]
        if marker is None:
            opened = fence_open(content)
            if opened is not None:
                marker, minimum_length, _ = opened
                output.append(ending)
            else:
                output.append(line)
            continue
        if is_fence_close(content, marker, minimum_length):
            marker = None
            minimum_length = 0
        output.append(ending)
    return "".join(output)


def markdown_without_code(text: str) -> str:
    """Mask fenced and inline code while preserving offsets and line boundaries."""
    visible = markdown_without_fenced_code(text)
    masked = list(visible)
    runs = list(re.finditer(r"`+", visible))
    run_index = 0
    while run_index < len(runs):
        opening = runs[run_index]
        closing_index = run_index + 1
        while (
            closing_index < len(runs)
            and len(runs[closing_index].group(0)) != len(opening.group(0))
        ):
            closing_index += 1
        if closing_index >= len(runs):
            run_index += 1
            continue
        closing = runs[closing_index]
        for index in range(opening.start(), closing.end()):
            if masked[index] not in "\r\n":
                masked[index] = " "
        run_index = closing_index + 1
    return "".join(masked)


def markdown_without_html_comments(text: str) -> str:
    """Mask HTML comments while preserving offsets and line boundaries."""
    masked = list(text)
    for match in re.finditer(r"<!--[\s\S]*?(?:-->|\Z)", text):
        for index in range(match.start(), match.end()):
            if masked[index] not in "\r\n":
                masked[index] = " "
    return "".join(masked)


def character_is_escaped(text: str, index: int) -> bool:
    """Return whether the character at index has an odd backslash prefix."""
    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def commonmark_destination_prefix(value: str) -> str:
    """Extract one CommonMark destination, excluding any optional title."""
    value = value.lstrip()
    if not value:
        return ""
    if value.startswith("<"):
        cursor = 1
        while cursor < len(value):
            if value[cursor] == ">" and not character_is_escaped(value, cursor):
                return value[: cursor + 1]
            cursor += 1
        return ""

    depth = 0
    cursor = 0
    while cursor < len(value):
        character = value[cursor]
        if character == "\\" and cursor + 1 < len(value):
            cursor += 2
            continue
        if character.isspace() and depth == 0:
            break
        if character == "(":
            depth += 1
        elif character == ")":
            if depth == 0:
                break
            depth -= 1
        cursor += 1
    return value[:cursor]


def inline_markdown_destinations(text: str) -> list[str]:
    """Extract inline-link destinations with balanced nested parentheses."""
    destinations: list[str] = []
    cursor = 0
    while cursor < len(text) - 1:
        close_label = text.find("](", cursor)
        if close_label < 0:
            break
        if character_is_escaped(text, close_label):
            cursor = close_label + 2
            continue
        open_label = text.rfind("[", 0, close_label)
        if open_label < 0 or character_is_escaped(text, open_label):
            cursor = close_label + 2
            continue

        content_start = close_label + 2
        depth = 1
        position = content_start
        destination_start = content_start
        while (
            destination_start < len(text)
            and text[destination_start] in " \t\r\n"
        ):
            destination_start += 1
        inside_angle_destination = (
            destination_start < len(text) and text[destination_start] == "<"
        )
        while position < len(text):
            character = text[position]
            if character == "\\" and position + 1 < len(text):
                position += 2
                continue
            if inside_angle_destination:
                if character == ">":
                    inside_angle_destination = False
                position += 1
                continue
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    raw = commonmark_destination_prefix(text[content_start:position])
                    if raw:
                        destinations.append(raw)
                    position += 1
                    break
            position += 1
        cursor = max(close_label + 2, position)
    return destinations


def reference_markdown_destinations(text: str) -> list[str]:
    """Extract destinations from CommonMark reference-link definitions."""
    destinations: list[str] = []
    definition = re.compile(r"^ {0,3}\[([^\]]+)\]:[ \t]*(.*)$")
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = definition.match(line)
        if match is None or match.group(1).startswith("^"):
            continue
        remainder = match.group(2)
        if not remainder.strip() and index + 1 < len(lines):
            continued = re.match(r"^[ \t]{1,3}(\S.*)$", lines[index + 1])
            if continued is not None:
                remainder = continued.group(1)
        raw = commonmark_destination_prefix(remainder)
        if raw:
            destinations.append(raw)
    return destinations


def markdown_link_destinations(text: str) -> list[str]:
    """Return CommonMark inline/image and reference-definition destinations."""
    visible = markdown_without_html_comments(markdown_without_code(text))
    return [
        *inline_markdown_destinations(visible),
        *reference_markdown_destinations(visible),
    ]


def parse_frontmatter_fields(label: str, text: str) -> dict[str, str] | None:
    """Parse the supported string-only flat-YAML subset and reject every other line."""
    lines = text.splitlines()
    check(bool(lines) and lines[0] == "---", f"{label} must start with YAML frontmatter")
    if not lines or lines[0] != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        fail(f"{label} has no closing YAML frontmatter delimiter")
        return None
    fields: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip():
            continue
        match = re.fullmatch(r"([a-z][a-z0-9_-]*):\s*(.*)", line)
        check(
            match is not None,
            (
                f"{label}:{number} is outside the supported flat-YAML frontmatter "
                "subset (`lowercase-key: string`)"
            ),
        )
        if match is None:
            continue
        key = match.group(1)
        check(key not in fields, f"{label} repeats frontmatter field {key!r}")
        value = match.group(2).strip()
        parsed_value: str | None = None
        if value.startswith('"'):
            try:
                decoded = json.loads(value)
            except json.JSONDecodeError:
                decoded = None
            if isinstance(decoded, str):
                parsed_value = decoded
        elif value.startswith("'"):
            if re.fullmatch(r"'(?:[^']|'')*'", value) is not None:
                parsed_value = value[1:-1].replace("''", "'")
        elif value.startswith("["):
            if re.fullmatch(
                r"\[\s*(?:[A-Za-z][A-Za-z0-9_-]*"
                r"(?:\s*,\s*[A-Za-z][A-Za-z0-9_-]*)*)?\s*\]",
                value,
            ) is not None:
                parsed_value = value
        elif value:
            implicit_non_string = re.fullmatch(
                r"(?:null|~|true|false|yes|no|on|off|"
                r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[-+]?\d+)?|"
                r"\d{4}-\d{2}-\d{2})",
                value,
                re.IGNORECASE,
            )
            has_yaml_structure = (
                value[0] in "-?:,{}#&*!|>'\"%@`"
                or re.search(r":[ \t]|[ \t]#", value) is not None
                or "\t" in value
            )
            if implicit_non_string is None and not has_yaml_structure:
                parsed_value = value
        check(
            parsed_value is not None,
            (
                f"{label}:{number} must use a valid string in the supported "
                "flat-YAML subset"
            ),
        )
        if parsed_value is not None and key not in fields:
            fields[key] = parsed_value
    return fields


def check_frontmatter_text(label: str, text: str) -> None:
    fields = parse_frontmatter_fields(label, text)
    if fields is None:
        return
    for field in ("name", "description"):
        check(bool(fields.get(field)), f"{label} frontmatter needs a non-empty {field}")


def check_frontmatter(path: Path) -> None:
    check_frontmatter_text(relative(path), read_text(path))


def activation_prompts(text: str) -> list[tuple[str, int]]:
    """Return every fenced block that looks like a workflow activation prompt."""
    field_names = (*PROMPT_REQUIRED_FIELDS, *PROMPT_OPTIONAL_FIELDS)

    def anchored(field: str, body: str) -> bool:
        return (
            re.search(
                rf"(?<![A-Za-z0-9_]){re.escape(field)}:[ \t]*",
                body,
            )
            is not None
        )

    def is_candidate(body: str) -> bool:
        return any(
            anchored(anchor, body)
            and any(
                anchored(field, body)
                for field in field_names
                if field != anchor
            )
            for anchor in ("Workflow depth", "Task")
        )

    return [
        (body, opening_line)
        for info, body, opening_line in fenced_blocks(
            markdown_without_html_comments(text)
        )
        if info.lower() in {"", "text"}
        and is_candidate(body)
    ]


def declared_prompt_fields(prompt: str) -> dict[str, list[str]]:
    """Parse exact prompt declarations that each occupy one complete line."""
    field_names = (*PROMPT_REQUIRED_FIELDS, *PROMPT_OPTIONAL_FIELDS)
    pattern = re.compile(
        r"^[ \t]*("
        + "|".join(
            re.escape(field) for field in sorted(field_names, key=len, reverse=True)
        )
        + r"):[ \t]*(.*?)[ \t]*$"
    )
    values: dict[str, list[str]] = {field: [] for field in field_names}
    for line in prompt.splitlines():
        match = pattern.fullmatch(line)
        if match is None:
            continue
        value = match.group(2).strip()
        if value.endswith("."):
            value = value[:-1].rstrip()
        values[match.group(1)].append(value)
    return values


def check_activation_prompts(label: str, text: str) -> None:
    prompts = activation_prompts(text)
    check(bool(prompts), f"{label} needs at least one fenced activation prompt")
    auto_prompts = 0
    for prompt, opening_line in prompts:
        field_anchor = re.compile(
            r"(?<![A-Za-z0-9_])(?:"
            + "|".join(
                re.escape(field)
                for field in sorted(
                    (*PROMPT_REQUIRED_FIELDS, *PROMPT_OPTIONAL_FIELDS),
                    key=len,
                    reverse=True,
                )
            )
            + r"):[ \t]*"
        )
        declaration_line = re.compile(
            r"^[ \t]*(?:"
            + "|".join(
                re.escape(field)
                for field in sorted(
                    (*PROMPT_REQUIRED_FIELDS, *PROMPT_OPTIONAL_FIELDS),
                    key=len,
                    reverse=True,
                )
            )
            + r"):[ \t]*.*$"
        )
        for line_number, line in enumerate(prompt.splitlines(), start=opening_line + 1):
            if field_anchor.search(line):
                check(
                    declaration_line.fullmatch(line) is not None,
                    (
                        f"{label}:{line_number} workflow control declarations "
                        "must occupy complete lines"
                    ),
                )
        fields = declared_prompt_fields(prompt)
        for field in PROMPT_REQUIRED_FIELDS:
            check(
                len(fields[field]) == 1,
                (
                    f"{label}:{opening_line} activation prompt must declare "
                    f"{field!r} exactly once"
                ),
            )
        for field in PROMPT_OPTIONAL_FIELDS:
            check(
                len(fields[field]) <= 1,
                (
                    f"{label}:{opening_line} activation prompt declares optional "
                    f"{field!r} more than once"
                ),
            )

        for field, pattern in PROMPT_VALUE_PATTERNS.items():
            for value in fields[field]:
                check(
                    re.fullmatch(pattern, value) is not None,
                    (
                        f"{label}:{opening_line} activation prompt has invalid "
                        f"{field!r} value {value!r}"
                    ),
                )
        for task in fields["Task"]:
            check(
                bool(task.strip()),
                f"{label}:{opening_line} activation prompt has an empty task",
            )

        canonical = all(
            fields[field] == [expected]
            for field, expected in CANONICAL_PROMPT_DEFAULTS.items()
        )
        if canonical:
            auto_prompts += 1
    check(auto_prompts > 0, f"{label} needs at least one canonical Auto activation prompt")


def markdown_h2_sections(text: str, heading_pattern: str) -> list[str]:
    """Return the bodies of all matching level-two Markdown sections."""
    visible = markdown_contract_text(text)
    headings = list(re.finditer(r"^##[ \t]+(.+?)[ \t]*$", visible, re.MULTILINE))
    sections: list[str] = []
    for index, heading in enumerate(headings):
        if re.fullmatch(
            heading_pattern,
            heading.group(1).strip(),
            re.IGNORECASE,
        ) is None:
            continue
        end = (
            headings[index + 1].start()
            if index + 1 < len(headings)
            else len(visible)
        )
        sections.append(visible[heading.end() : end])
    return sections


TARGET_AGENTS_POLICY_HEADINGS = (
    "Source Of Truth",
    "Untrusted Content Boundary",
    "External Tool Data Boundary",
    "Agent Rules",
    "Execution Modes",
    "Adaptive Work Routing And Efficiency",
    "Resource Governance",
    "First-Run Repository Adaptation",
    "Risk And Security",
    "Definition Of Done",
)


def target_agents_policy_text(label: str, text: str) -> str:
    """Extract only canonical workflow-policy sections from a merged AGENTS file."""
    sections: list[str] = []
    for heading in TARGET_AGENTS_POLICY_HEADINGS:
        matches = markdown_h2_sections(text, re.escape(heading))
        check(
            len(matches) == 1,
            f"{label} must contain exactly one {heading!r} section",
        )
        sections.extend(matches)
    return "\n\n".join(sections)


def target_agents_contradiction_text(text: str) -> str:
    """Return strict workflow sections plus explicit instructions from merged prose."""
    strict_sections = [
        section
        for heading in TARGET_AGENTS_POLICY_HEADINGS
        if heading != "Risk And Security"
        for section in markdown_h2_sections(text, re.escape(heading))
    ]
    strict_sections.append(workflow_instruction_text(text))
    return "\n\n".join(strict_sections)


def check_plan_defaults(label: str, text: str) -> None:
    """Require each canonical default exactly once in its authoritative section."""
    text = markdown_contract_text(text)
    for section_name, pattern, minimum, maximum in PLAN_CANONICAL_SECTION_GROUPS:
        count = len(markdown_h2_sections(text, pattern))
        check(
            minimum <= count <= maximum,
            (
                f"{label} canonical {section_name!r} section must occur "
                f"{minimum if minimum == maximum else f'{minimum}-{maximum}'} time(s); "
                f"found {count}"
            ),
        )
    for field, expected in {**CANONICAL_PLAN_DEFAULTS, **PLAN_ROLE_CAP_DEFAULTS}.items():
        global_values = [
            match.group(1).strip()
            for match in re.finditer(
                rf"^[ \t]*-[ \t]*{re.escape(field)}:[ \t]*(.*?)[ \t]*$",
                text,
                re.MULTILINE,
            )
            if match.group(1).strip()
        ]
        check(
            len(global_values) == 1,
            f"{label} must declare exactly one non-empty {field!r} default",
        )
        canonical_sections = markdown_h2_sections(text, PLAN_DEFAULT_SECTIONS[field])
        check(
            bool(canonical_sections),
            (
                f"{label} lacks the canonical section for {field!r}: "
                f"{PLAN_DEFAULT_SECTIONS[field]}"
            ),
        )
        section = "\n".join(canonical_sections)
        section_values = [
            match.group(1).strip()
            for match in re.finditer(
                rf"^[ \t]*-[ \t]*{re.escape(field)}:[ \t]*(.*?)[ \t]*$",
                section,
                re.MULTILINE,
            )
            if match.group(1).strip()
        ]
        check(
            len(section_values) == 1,
            f"{label} must declare {field!r} once in its canonical section",
        )
        if len(global_values) == 1 and len(section_values) == 1:
            check(
                global_values[0] == expected and section_values[0] == expected,
                (
                    f"{label} has {field!r} default {global_values[0]!r}; "
                    f"expected {expected!r}"
                ),
            )
    execution_headings = list(
        re.finditer(r"^## Execution Mode[ \t]*$", text, re.MULTILINE)
    )
    check(
        len(execution_headings) == 1,
        f"{label} must contain exactly one 'Execution Mode' section",
    )
    if len(execution_headings) == 1:
        start = execution_headings[0].end()
        next_heading = re.search(r"^##\s+", text[start:], re.MULTILINE)
        end = start + next_heading.start() if next_heading is not None else len(text)
        body_lines = [line.strip() for line in text[start:end].splitlines() if line.strip()]
        selected = body_lines[0] if body_lines else ""
        check(
            selected == "Sequential",
            f"{label} initial execution-mode selection must be bare 'Sequential'",
        )


def check_core_default_contract(
    label: str,
    text: str,
    *,
    check_declarations: bool = True,
) -> None:
    """Reject contradictory defaults in authoritative runtime instructions."""
    visible = markdown_contract_text(text)
    canonical_lines = {
        "Workflow depth": r"Auto",
        "Efficiency profile": r"Balanced",
        "Token budget": r"Auto",
        "Validation/review/closeout reserve": r"25%",
        "Max retries per node": r"1",
        "Execution mode": r"Sequential",
        "Integration mode": r"Auto",
        "Local metrics": r"Off",
        "Max parallel subagents": r"4",
    }
    if check_declarations:
        declaration = re.compile(
            r"^[ \t]*(?:[-*][ \t]+)?("
            + "|".join(re.escape(field) for field in canonical_lines)
            + r"):[ \t]*(`[^`\n]+`|[^`\n]+?)[ \t]*$",
            re.MULTILINE | re.IGNORECASE,
        )
        for match in declaration.finditer(visible):
            field = next(
                name
                for name in canonical_lines
                if name.lower() == match.group(1).lower()
            )
            value = match.group(2).strip().strip("`")
            check(
                re.fullmatch(canonical_lines[field], value, re.IGNORECASE) is not None,
                (
                    f"{label} declares contradictory default-like field "
                    f"{field!r}: {value!r}"
                ),
            )

    contradictions = {
        "workflow depth": (
            r"Workflow depth.{0,50}(?:defaults?\s+to|default\s+is)"
            r".{0,30}(?:Direct|Lite|Standard|Full)|"
            r"(?:Direct|Lite|Standard|Full)\s+is\s+the\s+default"
            r"(?:\s+workflow\s+depth)?|"
            r"default(?:\s+workflow)?\s+depth(?:\s+is|:)?"
            r".{0,20}(?:Direct|Lite|Standard|Full)"
        ),
        "efficiency profile": (
            r"Efficiency profile.{0,50}(?:defaults?\s+to|default\s+is)"
            r".{0,30}(?:Economy|Thorough)|"
            r"(?:Economy|Thorough)\s+is\s+the\s+default"
            r"(?:\s+efficiency\s+profile)?|"
            r"default(?:\s+efficiency)?\s+profile(?:\s+is|:)?"
            r".{0,20}(?:Economy|Thorough)"
        ),
        "token budget": (
            r"Token budget.{0,50}(?:defaults?\s+to|default\s+is)"
            r".{0,30}(?!Auto\b)(?:[1-9]\d*)"
        ),
        "validation reserve": (
            r"(?:Validation/review/closeout reserve|reserve).{0,60}"
            r"(?:defaults?\s+to|default\s+is|by\s+default).{0,30}"
            r"(?<!\d)(?!25%(?!\d))\d{1,2}%|"
            r"(?:Validation/review/closeout reserve|reserve).{0,30}"
            r"(?<!\d)(?!25%(?!\d))\d{1,2}%.{0,30}"
            r"(?:is\s+the\s+default|by\s+default)"
        ),
        "retry ceiling": (
            r"Max retries per node.{0,50}(?:defaults?\s+to|default\s+is|"
            r"is\s+the\s+default).{0,20}(?!1\b)\d+|"
            r"Max retries per node.{0,20}(?!1\b)\d+.{0,30}"
            r"(?:is\s+the\s+default|by\s+default)"
        ),
        "execution mode": (
            r"Execution mode.{0,50}(?:defaults?\s+to|default\s+is).{0,20}Parallel|"
            r"Parallel.{0,30}(?:is\s+the\s+default|default execution mode)|"
            r"default execution mode(?:\s+is|:)?\s*Parallel"
        ),
        "integration mode": (
            r"Integration mode.{0,50}(?:defaults?\s+to|default\s+is).{0,30}"
            r"(?:Leased writers|Single integrator)|"
            r"(?:Leased writers|Single integrator).{0,30}"
            r"(?:is\s+the\s+default|default integration mode)"
        ),
        "local metrics": (
            r"Local metrics.{0,50}(?:defaults?\s+to|default\s+is).{0,20}On|"
            r"Local metrics:\s*On.{0,30}(?:is\s+the\s+default|by\s+default)|"
            r"(?:by\s+default|default)\s*,?\s+local metrics\s+"
            r"(?:are|is|:)\s*On"
        ),
        "parallel cap": (
            r"(?:Max parallel subagents|default global maximum).{0,50}"
            r"(?:defaults?\s+to|default\s+is|is).{0,20}(?!4\b)\d+|"
            r"Max parallel subagents.{0,20}(?!4\b)\d+.{0,30}"
            r"(?:is\s+the\s+default|by\s+default)"
        ),
    }
    for contract, pattern in contradictions.items():
        unsafe_matches = [
            match
            for match in re.finditer(pattern, visible, re.IGNORECASE)
            if not product_only_statement(
                containing_prose_clause(visible, match.start(), match.end())
            )
        ]
        check(
            not unsafe_matches,
            f"{label} contains a contradictory {contract} default",
        )


FINGERPRINT_DEFINITION_START = re.compile(
    r"^[ \t]*(?:(?:[-*+]|\d+[.)])[ \t]+)?"
    r"(?:(?:one|each|every|an?|the|reusable|evidence)[ \t]+)*"
    r"fingerprint(?:[ \t]+[A-Za-z0-9_-]+)?[ \t]+"
    r"(?:records?|contains?|includes?|captures?|keys?|must\b|has\b|is\b)",
    re.IGNORECASE,
)


def split_fingerprint_definitions(paragraph: str) -> list[str]:
    """Split adjacent definitions while retaining one definition's nested field list."""
    chunks: list[list[str]] = []
    current: list[str] = []
    current_has_definition = False
    for line in paragraph.splitlines():
        starts_definition = FINGERPRINT_DEFINITION_START.search(line) is not None
        if starts_definition and current and current_has_definition:
            chunks.append(current)
            current = []
            current_has_definition = False
        current.append(line)
        current_has_definition = current_has_definition or starts_definition
    if current:
        chunks.append(current)

    sections: list[str] = []
    for chunk in chunks:
        value = "\n".join(chunk)
        sentence_parts = re.split(
            r"(?<=[.!?;])[ \t]+(?="
            r"(?:(?:one|each|every|an?|the|reusable|evidence)[ \t]+)*"
            r"fingerprint(?:[ \t]+[A-Za-z0-9_-]+)?[ \t]+"
            r"(?:records?|contains?|includes?|captures?|keys?|must\b|has\b|is\b)"
            r")",
            value,
            flags=re.IGNORECASE,
        )
        sections.extend(part for part in sentence_parts if re.search(r"fingerprint", part))
    return sections


def fingerprint_definition_sections(text: str) -> list[str]:
    """Return atomic definition blocks without joining distinct fingerprints."""
    lowered = markdown_contract_text(text).lower()
    sections: list[str] = []

    def heading_context_blocks(block: str) -> list[str]:
        """Split independently asserted list items or scenario contracts."""
        lines = block.splitlines()
        label_start = re.compile(
            r"^[ \t]*\*\*(?:Given|When|Expected):\*\*[ \t]*",
            re.IGNORECASE,
        )
        label_indexes = [
            index for index, line in enumerate(lines) if label_start.match(line)
        ]
        if label_indexes:
            starts = [0, *label_indexes] if label_indexes[0] != 0 else label_indexes
            return [
                "\n".join(lines[start:end]).strip()
                for start, end in zip(starts, [*starts[1:], len(lines)])
                if "\n".join(lines[start:end]).strip()
            ]

        list_start = re.compile(r"^([ \t]*)(?:[-*+]|\d+[.)])[ \t]+")
        first_item = next(
            (
                (index, match)
                for index, line in enumerate(lines)
                if (match := list_start.match(line)) is not None
            ),
            None,
        )
        if first_item is None or any(line.strip() for line in lines[: first_item[0]]):
            return [block]
        base_indent = len(first_item[1].group(1).expandtabs(4))
        items: list[list[str]] = []
        current: list[str] = []
        for line in lines[first_item[0] :]:
            match = list_start.match(line)
            starts_top_level_item = (
                match is not None
                and len(match.group(1).expandtabs(4)) <= base_indent
            )
            if starts_top_level_item and current:
                items.append(current)
                current = []
            current.append(line)
        if current:
            items.append(current)
        return ["\n".join(item).strip() for item in items]

    # Explicit definitions stand on their own. In particular, two consecutive
    # definitions must not satisfy the contract by contributing complementary
    # fields to one combined paragraph.
    paragraphs = re.split(r"\n[ \t]*\n", lowered)
    for paragraph_index, paragraph in enumerate(paragraphs):
        if not re.search(r"fingerprint", paragraph):
            continue
        lines = paragraph.splitlines()
        if any(line.lstrip().startswith("|") for line in lines):
            sections.extend(
                line
                for line in lines
                if line.lstrip().startswith("|") and "fingerprint" in line
            )
        else:
            definitions = split_fingerprint_definitions(paragraph)
            can_have_nested_fields = (
                bool(definitions)
                and definitions[-1].rstrip().endswith(":")
                and FINGERPRINT_DEFINITION_START.search(
                    definitions[-1].splitlines()[0]
                )
                is not None
            )
            if can_have_nested_fields:
                field_lists: list[str] = []
                following_index = paragraph_index + 1
                while following_index < len(paragraphs):
                    following = paragraphs[following_index].strip()
                    following_lines = following.splitlines()
                    is_field_list = (
                        bool(following_lines)
                        and re.match(
                            r"^[ \t]*(?:[-*+]|\d+[.)])[ \t]+",
                            following_lines[0],
                        )
                        is not None
                        and all(
                            re.match(
                                r"^[ \t]*(?:(?:[-*+]|\d+[.)])[ \t]+|"
                                r"(?:[ ]{2,}|\t+)\S)",
                                line,
                            )
                            is not None
                            for line in following_lines
                            if line.strip()
                        )
                        and not any(
                            FINGERPRINT_DEFINITION_START.search(line) is not None
                            for line in following_lines
                        )
                    )
                    if not is_field_list:
                        break
                    field_lists.append(following)
                    following_index += 1
                if field_lists:
                    definitions[-1] = "\n".join([definitions[-1], *field_lists])
            sections.extend(definitions)

    # Some canonical artifacts use a fingerprint-named heading and put the
    # actual definition in a following Given block or ledger header. Prefix the
    # heading to each *individual* body block or table row; never concatenate
    # separate blocks. This preserves heading context without allowing fields
    # from adjacent definitions to aggregate.
    headings = list(
        re.finditer(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", lowered, re.MULTILINE)
    )
    for index, heading in enumerate(headings):
        if "fingerprint" not in heading.group(2):
            continue
        level = len(heading.group(1))
        end = len(lowered)
        for following in headings[index + 1 :]:
            if len(following.group(1)) <= level:
                end = following.start()
                break
        heading_text = heading.group(2).strip()
        body = lowered[heading.end() : end]
        for block in re.split(r"\n[ \t]*\n", body):
            block = block.strip()
            if not block:
                continue
            block_lines = block.splitlines()
            if any(line.lstrip().startswith("|") for line in block_lines):
                candidates = [
                    line.strip()
                    for line in block_lines
                    if line.lstrip().startswith("|")
                    and re.search(r"[A-Za-z0-9]", line)
                    and re.fullmatch(r"[|: \t-]+", line) is None
                ]
            elif "fingerprint" in block:
                candidates = split_fingerprint_definitions(block) or [block]
            else:
                candidates = heading_context_blocks(block)
            sections.extend(f"{heading_text}\n{candidate}" for candidate in candidates)

    # Avoid repeated diagnostics when an explicit definition is also inside a
    # fingerprint-named section.
    return list(dict.fromkeys(sections))


def fingerprint_contract_complete(text: str) -> bool:
    """Return whether one bounded definition contains every canonical field."""
    return any(
        all(
            re.search(pattern, section, re.DOTALL) is not None
            for pattern in FINGERPRINT_CONTRACT_PATTERNS.values()
        )
        for section in fingerprint_definition_sections(text)
    )


def check_fingerprint_contract(label: str, text: str) -> None:
    """Require one bounded fingerprint definition containing every freshness field."""
    sections = fingerprint_definition_sections(text)
    check(bool(sections), f"{label} lacks an evidence-fingerprint definition")
    if not sections:
        return
    check(
        fingerprint_contract_complete(text),
        (
            f"{label} lacks one evidence-fingerprint definition containing every "
            "canonical field"
        ),
    )
    for field, pattern in FINGERPRINT_CONTRACT_PATTERNS.items():
        check(
            any(re.search(pattern, section, re.DOTALL) is not None for section in sections),
            f"{label} evidence-fingerprint definition lacks {field}",
        )


def containing_prose_clause(text: str, start: int, end: int) -> str:
    """Return the sentence-like clause containing a regex match."""
    left = max(
        text.rfind(delimiter, 0, start)
        for delimiter in (".", ";", ":", "\n")
    )
    right_candidates = [
        position
        for delimiter in (".", ";", ":", "\n")
        if (position := text.find(delimiter, end)) >= 0
    ]
    right = min(right_candidates) if right_candidates else len(text)
    return text[left + 1 : right]


def product_only_statement(text: str) -> bool:
    """Distinguish project-product facts from instructions governing the workflow."""
    product_subject = re.search(
        r"\b(?:the\s+|this\s+|our\s+|its\s+)?"
        r"(?:product|application|service|template engine|runtime component)\b",
        text,
        re.IGNORECASE,
    )
    workflow_subject = re.search(
        r"\b(?:agents?|workflow|roles?|Orchestrator|Architect|Coder|Tester|"
        r"Reviewer|Codex|Copilot|Claude|local metrics|workflow metrics)\b",
        text,
        re.IGNORECASE,
    )
    return product_subject is not None and workflow_subject is None


def workflow_instruction_text(text: str) -> str:
    """Keep explicit workflow instructions while excluding ordinary product prose."""
    visible = markdown_contract_text(text)
    clauses = re.split(r"(?<=[.!?;])\s+|\n+", visible)
    workflow_subject = re.compile(
        r"\b(?:agents?|subagents?|workers?|roles?|Orchestrator|Architect|Coder|"
        r"Tester|Reviewer|Codex|Copilot|Claude|agentic workflow|the workflow|"
        r"this workflow|workflow depth|efficiency profile|token budget|"
        r"validation/review/closeout reserve|max retries per node|"
        r"execution mode|integration mode|local metrics|workflow metrics|"
        r"task approval|plan approval|explicit user approval|"
        r"In Progress plan|retry exhaustion|hard retry ceiling|spawn-value|"
        r"write lease|role memory)\b",
        re.IGNORECASE,
    )
    imperative = re.compile(
        r"^[ \t]*(?:[-*+]\s+|\d+[.)]\s+)?"
        r"(?:(?:always|never|routinely)\s+|(?:do|does|must|will|shall)\s+not\s+)?"
        r"(?:collect|record|store|capture|upload|export|send|transmit|include|"
        r"retain|persist|write|log|disclose|encode|paste|attach|obey|follow|"
        r"execute|promote|treat|classify|trust|accept|implement|edit|modify|"
        r"retry|continue|proceed|delegate|spawn)\b",
        re.IGNORECASE,
    )
    high_signal_policy = re.compile(
        r"^[ \t]*(?:[-*+]\s+|\d+[.)]\s+)?(?:"
        r"(?:web pages?|web content|untrusted content|source files?|code comments?|"
        r"logs?|tool output)\b[^.;:\n]{0,140}\b"
        r"(?:trusted|authoritative|executable)\b[^.;:\n]{0,60}\binstructions?\b|"
        r"(?:secrets?|credentials?|access tokens?|private keys?|proprietary source|"
        r"source code|repository content|customer data|personal data|private URLs?|"
        r"sensitive identifiers?)\b[^.;:\n]{0,180}\b"
        r"(?:may|can|should|must|will|shall)\b[^.;:\n]{0,80}\b"
        r"(?:be\s+)?(?:sent|included|disclosed|encoded|transmitted|pasted|"
        r"attached|uploaded)\b|"
        r"(?:Economy|Direct|token budget|worker caps?|efficiency profile)\b"
        r"[^.;:\n]{0,160}\b(?:omit|skip|leave out|disable|bypass)\b|"
        r"(?:a\s+)?new hypothesis\b[^.;:\n]{0,140}\b"
        r"(?:reset(?:s|ting|ted)?|restore(?:s|d|ing)?|"
        r"refresh(?:es|ed|ing)?|renew(?:s|ed|ing)?)\b|"
        r"(?:the\s+)?retry (?:limit|ceiling|budget)\b[^.;:\n]{0,80}\b"
        r"(?:soft|optional|advisory|continue|proceed|reset)\b|"
        r"(?:a\s+)?hard(?: retry)? ceiling\b[^.;:\n]{0,100}\b"
        r"(?:can be exceeded|may be ignored|is optional)\b|"
        r"(?:after|once|upon) (?:retry )?exhaustion\b[^.;:\n]{0,140}\b"
        r"(?:continue|proceed|retry|resume)\b|"
        r"retries after (?:retry )?exhaustion\b[^.;:\n]{0,100}\b"
        r"(?:need|require) no\b)",
        re.IGNORECASE,
    )
    return "\n".join(
        clause.strip()
        for clause in clauses
        if clause.strip()
        and not product_only_statement(clause)
        and (
            workflow_subject.search(clause) is not None
            or imperative.search(clause) is not None
            or high_signal_policy.search(clause) is not None
        )
    )


def contract_polarity_contradictions(text: str) -> list[str]:
    """Return reversed safety contracts that keyword-presence checks could miss."""
    violations: list[str] = []
    for description, pattern in CONTRACT_POLARITY_PATTERNS.items():
        if any(
            not product_only_statement(
                containing_prose_clause(text, match.start(), match.end())
            )
            for match in re.finditer(
                pattern,
                text,
                re.DOTALL | re.IGNORECASE,
            )
        ):
            violations.append(description)

    for match in re.finditer(
        r"\bsilent(?:ly)?\b[^.;:\n]{0,60}\b"
        r"(?:default|defaulted|defaulting|coerce|coerced|coercing|"
        r"reinterpret|reinterpreted|reinterpreting|"
        r"substitute|substituted|substituting)\b",
        text,
        re.IGNORECASE,
    ):
        if product_only_statement(
            containing_prose_clause(text, match.start(), match.end())
        ):
            continue
        before = text[max(0, match.start() - 140) : match.start()]
        protected = re.search(
            r"\b(?:do not|does not|must not|will not|never|without|"
            r"rather\s+than|instead\s+of|refuse(?:s|d)? to|forbid(?:s|den)?|"
            r"avoid(?:s|ed|ing)?|prevent(?:s|ed|ing)?|"
            r"refrain(?:s|ed|ing)?\s+from)\b"
            r"[^.;:\n]{0,120}$",
            before,
            re.IGNORECASE,
        )
        after = text[match.end() : match.end() + 100]
        prohibited_after = re.search(
            r"^[^.;:\n]{0,80}\b(?:is|are|was|were)\s+(?:strictly\s+)?"
            r"(?:prohibited|forbidden|prevented|never allowed)\b",
            after,
            re.IGNORECASE,
        )
        if protected is None and prohibited_after is None:
            violations.append("affirmative silent default or reinterpretation")
            break
    return list(dict.fromkeys(violations))


def check_contract_polarity(label: str, text: str) -> None:
    """Reject text that reverses retry-ceiling or fallback safety semantics."""
    for description in contract_polarity_contradictions(text):
        check(False, f"{label} contains {description}")


def safety_invariant_contradictions(text: str) -> list[str]:
    """Return affirmative reversals of approval, mandatory-gate, or risk floors."""
    patterns = {
        "implementation permitted before approval or In Progress": (
            r"\b(?:Coder|Orchestrator|agents?)\b[^.;:\n]{0,100}"
            r"\b(?:may|can|should|will|shall|is allowed to|is permitted to)\b"
            r"(?!\s+not\b)[^.;:\n]{0,80}\b(?:implement|write|edit|modify|"
            r"(?:begin|start)\s+(?:coding|implementation|writing|editing))\b"
            r"[^.;:\n]{0,100}\b(?:before|without)\b[^.;:\n]{0,80}"
            r"\b(?:explicit(?: user)? approval|plan approval|In Progress)\b|"
            r"\b(?:implementation|coding|repository writes?)\b[^.;:\n]{0,80}"
            r"\b(?:is|are)\s+(?:allowed|permitted)\b[^.;:\n]{0,100}"
            r"\b(?:before|without)\b[^.;:\n]{0,80}"
            r"\b(?:explicit(?: user)? approval|plan approval|In Progress)\b|"
            r"\b(?:before|without)\b[^.;:\n]{0,80}"
            r"\b(?:explicit(?: user)? approval|plan approval|In Progress)\b"
            r"[^.;:\n]{0,100}\b(?:Coder|Orchestrator|agents?)\b"
            r"[^.;:\n]{0,60}\b(?:may|can|should|will|shall|"
            r"is allowed to|is permitted to)\b(?!\s+not\b)"
            r"[^.;:\n]{0,60}\b(?:implement|write|edit|modify|"
            r"(?:begin|start)\s+(?:coding|implementation|writing|editing))\b"
        ),
        "efficiency setting permitted to omit a mandatory gate": (
            r"\b(?:Economy|Direct|token budget|worker caps?|efficiency (?:profile|setting))"
            r"\b[^.;:\n]{0,120}\b(?:may|can|allows?|permits?)\b(?!\s+not\b)"
            r"[^.;:\n]{0,80}\b(?:omit(?:s|ted|ting)?|skipp(?:ed|ing)|skip|"
            r"disable(?:s|d|ing)?|bypass(?:es|ed|ing)?|"
            r"leav(?:e|es|ing)\s+out)\b"
            r"[^.;:\n]{0,100}\b(?:required|mandatory)?\s*"
            r"(?:validation|security review|security coverage)\b"
        ),
        "user preference permitted to lower the security floor": (
            r"\b(?:user preference|user request|requested route|requested workflow depth)"
            r"\b[^.;:\n]{0,120}\b(?:may|can|allows?|permits?)\b(?!\s+not\b)"
            r"[^.;:\n]{0,100}\b(?:lower|downgrade|route)\b"
            r"[^.;:\n]{0,120}\b(?:security-sensitive|high-risk)\b"
            r"[^.;:\n]{0,80}\b(?:Direct|Lite|lower risk)\b|"
            r"\b(?:security-sensitive|high-risk)\b[^.;:\n]{0,100}"
            r"\b(?:may|can)\b(?!\s+not\b)[^.;:\n]{0,80}"
            r"\b(?:be\s+)?(?:lowered|downgraded|routed|treated|classified|handled)\b"
            r"[^.;:\n]{0,80}(?:\bas\b[^.;:\n]{0,30}\b"
            r"(?:Direct|Lite|lower risk)\b[^.;:\n]{0,50})?"
            r"\b(?:at|by|because of)\s+(?:a\s+)?user "
            r"(?:preference|request)\b"
        ),
    }

    def match_has_affirmative_permission(match: re.Match[str]) -> bool:
        matched = match.group(0)
        permission_pattern = (
            r"(?:may|can|should|will|shall|allow(?:s|ed|ing)?|"
            r"permit(?:s|ted|ting)?)"
        )
        for permission in re.finditer(
            rf"\b{permission_pattern}\b",
            matched,
            re.IGNORECASE,
        ):
            before = matched[max(0, permission.start() - 50) : permission.start()]
            after = matched[permission.end() : permission.end() + 20]
            if re.search(
                r"\b(?:do not|does not|did not|must not|will not|shall not|"
                r"never|cannot|can't)\b[^.;:\n]{0,40}$",
                before,
                re.IGNORECASE,
            ) is not None:
                continue
            if re.match(r"\s+not\b", after, re.IGNORECASE) is not None:
                continue
            return True
        return False

    violations: list[str] = []
    for description, pattern in patterns.items():
        if any(
            match_has_affirmative_permission(match)
            for match in re.finditer(pattern, text, re.IGNORECASE)
        ):
            violations.append(description)
    return violations


def check_safety_invariants(label: str, text: str) -> None:
    """Reject explicit prose that grants unsafe exceptions to workflow gates."""
    for description in safety_invariant_contradictions(text):
        check(False, f"{label} contains {description}")


def untrusted_content_contradictions(text: str) -> list[str]:
    """Return directives that grant instruction authority to untrusted content."""
    target = (
        r"(?:embedded directives?|directives? embedded in untrusted content|"
        r"untrusted content|source files?|code comments?|logs?|user findings?|"
        r"web (?:pages?|content)|tool output)"
    )
    violations: list[str] = []

    def match_has_affirmative_directive_action(match: re.Match[str]) -> bool:
        matched = match.group(0)
        action_pattern = (
            r"(?:obey(?:s|ed|ing)?|follow(?:s|ed|ing)?|"
            r"execut(?:e|es|ed|ing)|promot(?:e|es|ed|ing)|"
            r"treat(?:s|ed|ing)?|classif(?:y|ies|ied|ying)|"
            r"us(?:e|es|ed|ing)|trust(?:s|ed|ing)?|accept(?:s|ed|ing)?)"
        )
        for action in re.finditer(rf"\b{action_pattern}\b", matched, re.IGNORECASE):
            before = matched[max(0, action.start() - 80) : action.start()]
            after = matched[action.end() : action.end() + 20]
            if re.search(
                r"\b(?:do not|does not|did not|must not|will not|shall not|"
                r"never|cannot|can't)\b[^.;:\n]{0,60}$",
                before,
                re.IGNORECASE,
            ) is not None:
                continue
            if re.match(r"\s+not\b", after, re.IGNORECASE) is not None:
                continue
            return True
        return False

    for match in re.finditer(
        rf"\b(?:obey|follow|execute|promote)\b[^.;:\n]{{0,160}}\b{target}\b",
        text,
        re.IGNORECASE,
    ):
        if product_only_statement(
            containing_prose_clause(text, match.start(), match.end())
        ):
            continue
        if not match_has_affirmative_directive_action(match):
            continue
        before = text[max(0, match.start() - 100) : match.start()]
        if re.search(
            r"\b(?:do not|does not|must not|will not|never|cannot|can't|"
            r"refuse(?:s|d)? to|avoid(?:s|ed|ing)?)\b[^.;:\n]{0,80}$",
            before,
            re.IGNORECASE,
        ) is None:
            violations.append("untrusted content granted instruction authority")
            break

    authority_patterns = (
        (
            rf"\b{target}\b[^.;:\n]{{0,120}}\b"
            r"(?:must|should|may|can|will|shall|always)\s+(?:be\s+)?"
            r"(?:obeyed|followed|executed|promoted)\b"
        ),
        (
            r"\b(?:agents?|workflow|roles?|Orchestrator|Architect|Coder|Tester|"
            r"Reviewer)\b[^.;:\n]{0,100}\b"
            r"(?:trust|accept|use)(?:s|ed|ing)?\b[^.;:\n]{0,100}\b"
            r"instructions?\b[^.;:\n]{0,100}\b(?:found|embedded|contained)\b"
            rf"[^.;:\n]{{0,80}}\b{target}\b"
        ),
    )
    if any(
        not product_only_statement(
            containing_prose_clause(text, match.start(), match.end())
        )
        and match_has_affirmative_directive_action(match)
        for pattern in authority_patterns
        for match in re.finditer(pattern, text, re.IGNORECASE)
    ):
        violations.append("untrusted content granted instruction authority")

    classified_matches = re.finditer(
        rf"\b(?:treat|classify|use)\b[^.;:\n]{{0,120}}\b{target}\b"
        r"[^.;:\n]{0,80}\bas\s+(?:executable\s+|workflow\s+)?instructions\b",
        text,
        re.IGNORECASE,
    )
    if any(
        not product_only_statement(
            containing_prose_clause(text, match.start(), match.end())
        )
        and match_has_affirmative_directive_action(match)
        for match in classified_matches
    ):
        violations.append("untrusted content classified as instructions")
    trusted_matches = re.finditer(
        rf"\b{target}\b[^.;:\n]{{0,100}}\b(?:is|are|be|becomes?)\s+"
        r"(?:a\s+)?(?:trusted|authoritative)(?:\s+source\s+of)?\s+instructions\b",
        text,
        re.IGNORECASE,
    )
    if any(
        not product_only_statement(
            containing_prose_clause(text, match.start(), match.end())
        )
        for match in trusted_matches
    ):
        violations.append("untrusted content classified as trusted instructions")
    return list(dict.fromkeys(violations))


def untrusted_content_contract_complete(text: str) -> bool:
    """Return whether text defines the complete untrusted-content boundary."""
    return (
        all(
            re.search(pattern, text, re.DOTALL | re.IGNORECASE) is not None
            for pattern in UNTRUSTED_CONTENT_CONTRACT_PATTERNS.values()
        )
        and not untrusted_content_contradictions(text)
    )


def check_untrusted_content_contract(
    label: str,
    text: str,
    *,
    contradiction_text: str | None = None,
) -> None:
    """Require source/tool data to remain outside the instruction authority chain."""
    for contract, pattern in UNTRUSTED_CONTENT_CONTRACT_PATTERNS.items():
        check(
            re.search(pattern, text, re.DOTALL | re.IGNORECASE) is not None,
            f"{label} untrusted-content boundary lacks {contract}",
        )
    for contradiction in untrusted_content_contradictions(
        text if contradiction_text is None else contradiction_text
    ):
        check(False, f"{label} contains {contradiction}")


def external_tool_data_contradictions(text: str) -> list[str]:
    """Return statements that reverse the minimal-disclosure egress boundary."""
    sensitive = (
        r"(?:secrets?|credentials?|access\s+tokens?|private\s+keys?|proprietary\s+"
        r"(?:source|code|repository\s+content)|source\s+code|repository\s+content|"
        r"customer\s+(?:or\s+)?personal\s+data|customer\s+data|personal\s+data|"
        r"private\s+URLs?|sensitive\s+identifiers?)"
    )
    external = (
        r"(?:web(?:-search)?\s+(?:queries|searches)|fetched\s+URLs?|connectors?|"
        r"MCP\s+calls?|remote\s+APIs?|third-party\s+tools?|external\s+tools?)"
    )
    disclose = (
        r"(?:send(?:s|ing)?|sent|includ(?:e|es|ed|ing)|"
        r"disclos(?:e|es|ed|ing)|encod(?:e|es|ed|ing)|"
        r"transmit(?:s|ted|ting)?|past(?:e|es|ed|ing)|"
        r"attach(?:es|ed|ing)?|upload(?:s|ed|ing)?)"
    )
    modal = r"(?:always|routinely|may|can|should|must|will|shall)"
    violations: list[str] = []

    def has_specific_authorization(clause: str) -> bool:
        return re.search(
            r"\b(?:only\s+)?(?:after|if|when|with|unless)\b"
            r"[^.;:\n]{0,120}\buser\b[^.;:\n]{0,80}\bexplicitly\b"
            r"[^.;:\n]{0,80}\bauthoriz(?:es|ed|ation)\b"
            r"[^.;:\n]{0,60}\bspecific disclosure\b",
            clause,
            re.IGNORECASE,
        ) is not None

    def match_has_affirmative_action(match: re.Match[str]) -> bool:
        action_pattern = (
            rf"(?:{disclose}|use(?:s|d|ing)?|put(?:s|ting)?|plac(?:e|es|ed|ing)|"
            r"receive(?:s|d|ing)?|contain(?:s|ed|ing)?)"
        )
        matched = match.group(0)
        for action in re.finditer(rf"\b{action_pattern}\b", matched, re.IGNORECASE):
            before = matched[max(0, action.start() - 80) : action.start()]
            after = matched[action.end() : action.end() + 20]
            if re.search(
                r"\b(?:do not|does not|did not|must not|will not|shall not|"
                r"never|cannot|can't)\b[^.;:\n]{0,60}$",
                before,
                re.IGNORECASE,
            ) is not None:
                continue
            if re.match(r"\s+not\b", after, re.IGNORECASE) is not None:
                continue
            return True
        return False

    credential = r"(?:secrets?|credentials?|access\s+tokens?|private\s+keys?)"
    found_unsafe_disclosure = False
    for pattern in (
        rf"\b{modal}\s+{disclose}\b[^.;:\n]{{0,180}}\b{sensitive}\b"
        rf"[^.;:\n]{{0,180}}\b{external}\b",
        rf"\b{modal}\s+(?:use|put|place)\b[^.;:\n]{{0,180}}\b{sensitive}\b"
        rf"[^.;:\n]{{0,180}}\b{external}\b",
        rf"\b{external}\b[^.;:\n]{{0,180}}\b{modal}\s+"
        rf"(?:receive|include|contain|use)\b[^.;:\n]{{0,140}}\b{sensitive}\b",
        rf"\b(?:it\s+is\s+)?(?:allowed|permitted)\s+to\s+{disclose}\b"
        rf"[^.;:\n]{{0,180}}\b{sensitive}\b[^.;:\n]{{0,180}}\b{external}\b",
        rf"\b{sensitive}\b[^.;:\n]{{0,160}}\b(?:may|can|should|must)\s+"
        rf"(?:be\s+)?(?:disclosed|sent|encoded|transmitted|pasted|uploaded)\b"
        rf"[^.;:\n]{{0,160}}\b{external}\b",
        rf"\b(?:agents?|workflow|roles?|Orchestrator|Architect|Coder|Tester|"
        rf"Reviewer)\b[^.;:\n]{{0,100}}\b{disclose}\b"
        rf"[^.;:\n]{{0,180}}\b{sensitive}\b[^.;:\n]{{0,180}}\b{external}\b",
    ):
        for match in re.finditer(pattern, text, re.IGNORECASE):
            clause = containing_prose_clause(text, match.start(), match.end())
            if product_only_statement(clause):
                continue
            if not match_has_affirmative_action(match):
                continue
            if (
                re.search(rf"\b{credential}\b", clause, re.IGNORECASE) is None
                and has_specific_authorization(clause)
            ):
                continue
            found_unsafe_disclosure = True
            break
        if found_unsafe_disclosure:
            violations.append("affirmative sensitive disclosure to an external tool")
            break

    if re.search(
        r"\b(?:general\s+)?(?:task\s+approval|request\s+to\s+research|"
        r"research\s+request)\b[^.;:\n]{0,100}\b"
        r"(?:is(?!\s+not\b)|counts\s+as|serves\s+as|provides|grants)\b"
        r"[^.;:\n]{0,100}\b(?:disclosure\s+authorization|authorization\s+to\s+"
        r"disclose|authorization\s+to\s+send)\b",
        text,
        re.IGNORECASE,
    ) is not None:
        violations.append("general task or research approval treated as disclosure authorization")

    credential_matches = re.finditer(
        r"\b(?:secrets?|credentials?|access\s+tokens?|private\s+keys?)\b"
        r"[^.;:\n]{0,100}\b(?:may|can|should|must)\s+(?:be\s+)?(?:sent|encoded|"
        r"uploaded|included)\b[^.;:\n]{0,100}\b(?:approval|authoriz)",
        text,
        re.IGNORECASE,
    )
    if any(
        not product_only_statement(
            containing_prose_clause(text, match.start(), match.end())
        )
        for match in credential_matches
    ):
        violations.append("credential disclosure made conditional instead of prohibited")

    return list(dict.fromkeys(violations))


def external_tool_data_contract_complete(text: str) -> bool:
    """Return whether text defines the complete outbound-tool data boundary."""
    return (
        all(
            re.search(pattern, text, re.DOTALL | re.IGNORECASE) is not None
            for pattern in EXTERNAL_TOOL_DATA_CONTRACT_PATTERNS.values()
        )
        and not external_tool_data_contradictions(text)
    )


def check_external_tool_data_contract(
    label: str,
    text: str,
    *,
    contradiction_text: str | None = None,
) -> None:
    """Require minimal disclosure and explicit authorization for external-tool inputs."""
    for contract, pattern in EXTERNAL_TOOL_DATA_CONTRACT_PATTERNS.items():
        check(
            re.search(pattern, text, re.DOTALL | re.IGNORECASE) is not None,
            f"{label} external-tool data boundary lacks {contract}",
        )
    for contradiction in external_tool_data_contradictions(
        text if contradiction_text is None else contradiction_text
    ):
        check(False, f"{label} contains {contradiction}")


def first_run_adaptation_contract_complete(text: str) -> bool:
    """Return whether text defines the complete guarded instruction-adaptation flow."""
    return all(
        re.search(pattern, text, re.DOTALL | re.IGNORECASE) is not None
        for pattern in FIRST_RUN_ADAPTATION_CONTRACT_PATTERNS.values()
    )


def check_first_run_adaptation_contract(label: str, text: str) -> None:
    """Require bounded discovery, revision approval, protected merges, and validation."""
    for contract, pattern in FIRST_RUN_ADAPTATION_CONTRACT_PATTERNS.items():
        check(
            re.search(pattern, text, re.DOTALL | re.IGNORECASE) is not None,
            f"{label} first-run repository adaptation lacks {contract}",
        )


def check_notice_file(label: str, text: str) -> None:
    """Require a self-contained MIT notice suitable for copied workflow material."""
    for contract in ("document title", "project name"):
        pattern = NOTICE_FILE_PATTERNS[contract]
        check(
            re.search(pattern, text, re.DOTALL | re.MULTILINE) is not None,
            f"{label} lacks {contract}",
        )
    check_mit_license(label, text)


def check_mit_license(label: str, text: str) -> None:
    """Require the complete canonical grant, condition, and disclaimers."""
    for contract, pattern in MIT_LICENSE_PATTERNS.items():
        check(
            re.search(pattern, text, re.DOTALL | re.MULTILINE) is not None,
            f"{label} lacks {contract}",
        )
    for contradiction, pattern in (
        ("all-rights-reserved restriction", r"\ball rights reserved\b"),
        (
            "permission denial",
            r"\bpermission\s+is\s+(?:not|never)\s+granted\b",
        ),
        (
            "redistribution prohibition",
            r"\b(?:copying|modification|distribution|redistribution)\s+"
            r"(?:is|are)\s+(?:prohibited|forbidden)\b",
        ),
    ):
        check(
            re.search(pattern, text, re.IGNORECASE) is None,
            f"{label} contains {contradiction}",
        )


def normalize_failure_class(value: str) -> str:
    """Normalize one failure-class label for exact-set comparison."""
    return re.sub(r"\s+", " ", value.strip().strip("`*_ ")).lower()


def declared_failure_class_sets(text: str) -> list[list[str]]:
    """Extract authoritative failure-class tables and exact-set declarations."""
    sets: list[list[str]] = []
    visible = markdown_contract_text(text)
    lines = visible.splitlines()
    header = re.compile(
        r"^\|\s*(Failure class|Class|Classification)\s*\|",
        re.IGNORECASE,
    )
    delimiter = re.compile(r"^\|\s*:?-{3,}:?\s*\|")
    heading = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
    active_headings: dict[int, str] = {}
    for index, line in enumerate(lines):
        heading_match = heading.match(line)
        if heading_match is not None:
            level = len(heading_match.group(1))
            active_headings = {
                active_level: title
                for active_level, title in active_headings.items()
                if active_level < level
            }
            active_headings[level] = heading_match.group(2).strip()
            continue

        header_match = header.match(line)
        if header_match is None:
            continue
        header_name = header_match.group(1).lower()
        in_failure_classification = any(
            re.search(
                r"\bfailure\b.*\bclass(?:ification|es)?\b|"
                r"\bclass(?:ification|es)?\b.*\bfailure\b",
                title,
                re.IGNORECASE,
            )
            is not None
            for title in active_headings.values()
        )
        local_context = "\n".join(lines[max(0, index - 4) : index])
        has_explicit_failure_context = (
            re.search(
                r"\bfailure\b.{0,120}\bclass(?:ification|ify|es)?\b|"
                r"\bclass(?:ification|ify|es)?\b.{0,120}\bfailure\b",
                local_context,
                re.IGNORECASE | re.DOTALL,
            )
            is not None
        )
        if (
            header_name in {"class", "classification"}
            and not in_failure_classification
            and not has_explicit_failure_context
        ):
            continue
        if index + 1 >= len(lines) or not delimiter.match(lines[index + 1]):
            continue
        values: list[str] = []
        row = index + 2
        while row < len(lines) and lines[row].lstrip().startswith("|"):
            cells = lines[row].strip().strip("|").split("|")
            if cells:
                values.append(normalize_failure_class(cells[0]))
            row += 1
        sets.append(values)

    marker = re.compile(
        r"^\*\*Canonical failure classes \(exact set\):\*\*\s*(.+)$",
        re.MULTILINE | re.IGNORECASE,
    )
    for match in marker.finditer(visible):
        values = [
            normalize_failure_class(value)
            for value in re.findall(r"`([^`]+)`", match.group(1))
        ]
        sets.append(values)
    return sets


def check_exact_failure_classes(label: str, text: str) -> None:
    """Require one or more declarations to contain exactly the canonical eight classes."""
    expected = set(FAILURE_CLASSES)
    declarations = declared_failure_class_sets(text)
    check(bool(declarations), f"{label} lacks an exact failure-class declaration")
    for index, values in enumerate(declarations, start=1):
        counts = Counter(values)
        actual = set(values)
        check(
            actual == expected,
            (
                f"{label} failure-class declaration {index} differs from the exact set; "
                f"missing={sorted(expected - actual)}, extra={sorted(actual - expected)}"
            ),
        )
        duplicates = sorted(value for value, count in counts.items() if count != 1)
        check(
            not duplicates,
            (
                f"{label} failure-class declaration {index} contains duplicates: "
                f"{duplicates}"
            ),
        )

    for match in re.finditer(
        r"(?im)^\s*(?:[-*]\s*)?(?:[A-Za-z]+\s+class|failure\s+class)\s*:"
        r"\s*`?([A-Za-z][A-Za-z /-]*?)`?\s*$",
        markdown_contract_text(text),
    ):
        declared = normalize_failure_class(match.group(1))
        check(
            declared in expected,
            f"{label} declares non-canonical failure class {declared!r}",
        )


def markdown_contract_text(text: str) -> str:
    """Mask fenced code and HTML comments before interpreting contract headings."""
    visible = markdown_without_html_comments(markdown_without_fenced_code(text))
    masked = list(visible)
    for match in re.finditer(r"^(?: {4,}|\t).*$", visible, re.MULTILINE):
        for index in range(match.start(), match.end()):
            if masked[index] not in "\r\n":
                masked[index] = " "
    return "".join(masked)


def scenario_sections(text: str) -> tuple[list[str], dict[str, str]]:
    """Return scenario IDs and sections bounded by the next level 1-3 heading."""
    visible = markdown_contract_text(text)
    matches = list(
        re.finditer(
            r"^ {0,3}###(?!#)[ \t]+((?:CF|C)-\d+)\b[^\n]*",
            visible,
            re.MULTILINE,
        )
    )
    headings = [match.group(1) for match in matches]
    sections: dict[str, str] = {}
    boundary = re.compile(r"^ {0,3}#{1,3}(?!#)[ \t]+", re.MULTILINE)
    for match in matches:
        next_heading = boundary.search(visible, match.end())
        end = next_heading.start() if next_heading is not None else len(visible)
        sections.setdefault(match.group(1), visible[match.start() : end])
    return headings, sections


def claude_coverage_rows(text: str) -> tuple[list[tuple[str, tuple[str, ...]]], int]:
    """Parse exact mechanism-to-scenario associations from the Claude coverage map."""
    visible = markdown_contract_text(text)
    coverage_match = re.search(
        r"^ {0,3}##(?!#)[ \t]+Coverage Map[ \t]*$"
        r"([\s\S]*?)(?=^ {0,3}#{1,2}(?!#)[ \t]+|\Z)",
        visible,
        re.MULTILINE,
    )
    if coverage_match is None:
        return [], 1
    rows: list[tuple[str, tuple[str, ...]]] = []
    malformed = 0
    for line in coverage_match.group(1).splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if (
            len(cells) == 2
            and cells[0].lower() == "mechanism"
            and cells[1].lower() == "scenarios"
        ):
            continue
        if len(cells) == 2 and all(
            re.fullmatch(r":?-{3,}:?", cell) is not None for cell in cells
        ):
            continue
        if len(cells) != 2 or not cells[0]:
            malformed += 1
            continue
        scenario_cell = cells[1]
        if re.fullmatch(r"C-\d{2}(?:\s*,\s*C-\d{2})*", scenario_cell) is None:
            malformed += 1
            continue
        rows.append(
            (
                re.sub(r"\s+", " ", cells[0]),
                tuple(
                    item.strip()
                    for item in scenario_cell.split(",")
                ),
            )
        )
    return rows, malformed


def scenario_contract_fields(section: str, label: str) -> list[str]:
    """Return label values bounded by the next scenario label or Markdown heading."""
    label_pattern = re.compile(
        rf"^ {{0,3}}\*\*{re.escape(label)}:\*\*[ \t]*",
        re.MULTILINE | re.IGNORECASE,
    )
    boundary_pattern = re.compile(
        r"^ {0,3}(?:\*\*(?:Given|When|Expected):\*\*|#{1,6}[ \t]+)",
        re.MULTILINE | re.IGNORECASE,
    )
    values: list[str] = []
    for match in label_pattern.finditer(section):
        boundary = boundary_pattern.search(section, match.end())
        end = boundary.start() if boundary is not None else len(section)
        values.append(section[match.end() : end].strip())
    return values


def check_provider_conformance(name: str, label: str, text: str) -> None:
    """Validate exact scenario IDs and each mechanism in its assigned scenario."""
    check_contract_polarity(label, text)
    prefix, count = PROVIDER_SCENARIO_COUNTS[name]
    expected_ids = {f"{prefix}-{index:02d}" for index in range(1, count + 1)}
    headings, sections = scenario_sections(text)
    actual_ids = set(headings)
    check(
        len(headings) == len(actual_ids),
        f"{label} contains duplicate scenario IDs",
    )
    check(
        actual_ids == expected_ids,
        (
            f"{label} scenario IDs differ from the exact contract; "
            f"missing={sorted(expected_ids - actual_ids)}, "
            f"unexpected={sorted(actual_ids - expected_ids)}"
        ),
    )
    if name == "claude":
        coverage_rows, malformed_rows = claude_coverage_rows(text)
        coverage_ids = [
            scenario_id
            for _, scenario_ids in coverage_rows
            for scenario_id in scenario_ids
        ]
        check(
            malformed_rows == 0,
            f"{label} has a missing or malformed Claude coverage-map row",
        )
        check(
            tuple(coverage_rows) == CLAUDE_COVERAGE_MAP,
            f"{label} coverage map has incorrect mechanism-to-scenario associations",
        )
        check(
            set(coverage_ids) == expected_ids,
            (
                f"{label} coverage map differs from scenario IDs; "
                f"missing={sorted(expected_ids - set(coverage_ids))}, "
                f"unexpected={sorted(set(coverage_ids) - expected_ids)}"
            ),
        )
        check(
            len(coverage_ids) == len(set(coverage_ids)),
            f"{label} coverage map contains duplicate scenario IDs",
        )
    for scenario_id in sorted(expected_ids):
        section = sections.get(scenario_id, "")
        given = scenario_contract_fields(section, "Given")
        expected = scenario_contract_fields(section, "Expected")
        check(
            bool(given) and all(given),
            f"{label} scenario {scenario_id} needs a non-empty Given contract",
        )
        check(
            bool(expected) and all(expected),
            f"{label} scenario {scenario_id} needs a non-empty Expected contract",
        )
    mapping = PROVIDER_SCENARIO_MAPS[name]
    check(
        set(mapping) == set(MECHANISMS),
        f"{label} does not map exactly all 22 mechanisms",
    )
    for mechanism, scenario_id in mapping.items():
        section = sections.get(scenario_id, "")
        check(
            re.search(
                MECHANISMS[mechanism],
                section,
                re.DOTALL | re.IGNORECASE,
            )
            is not None,
            f"{label} scenario {scenario_id} does not cover {mechanism}",
        )
    for scenario_id, contracts in PROVIDER_BASE_SCENARIOS[name].items():
        for contract, pattern in contracts.items():
            check(
                re.search(
                    pattern,
                    sections.get(scenario_id, ""),
                    re.DOTALL | re.IGNORECASE,
                )
                is not None,
                f"{label} scenario {scenario_id} lacks base contract {contract}",
            )

    untrusted_id = PROVIDER_UNTRUSTED_CONTENT_SCENARIOS[name]
    check_untrusted_content_contract(
        f"{label} scenario {untrusted_id}",
        sections.get(untrusted_id, ""),
    )

    external_tool_id = PROVIDER_EXTERNAL_TOOL_DATA_SCENARIOS[name]
    check_external_tool_data_contract(
        f"{label} scenario {external_tool_id}",
        sections.get(external_tool_id, ""),
    )

    adaptation_id = PROVIDER_FIRST_RUN_ADAPTATION_SCENARIOS[name]
    check_first_run_adaptation_contract(
        f"{label} scenario {adaptation_id}",
        sections.get(adaptation_id, ""),
    )

    retry_id = mapping["retry circuit breakers"]
    for contract, pattern in RETRY_CONTRACT_PATTERNS.items():
        check(
            re.search(
                pattern,
                sections.get(retry_id, ""),
                re.DOTALL | re.IGNORECASE,
            )
            is not None,
            f"{label} scenario {retry_id} lacks retry contract {contract}",
        )

    fingerprint_id = mapping["evidence fingerprints"]
    check_fingerprint_contract(
        f"{label} scenario {fingerprint_id}",
        sections.get(fingerprint_id, ""),
    )

    failure_id = mapping["failure classification"]
    for failure_class, pattern in FAILURE_CLASSES.items():
        check(
            re.search(pattern, sections.get(failure_id, ""), re.IGNORECASE) is not None,
            f"{label} scenario {failure_id} lacks failure class {failure_class!r}",
        )
    check_exact_failure_classes(
        f"{label} scenario {failure_id}",
        sections.get(failure_id, ""),
    )

    lease_sections = "\n".join(
        sections.get(mapping[mechanism], "")
        for mechanism in ("invalidation and cancellation", "single integrator")
    )
    for contract, pattern in LEASE_CONTRACT_PATTERNS.items():
        check(
            re.search(pattern, lease_sections, re.DOTALL | re.IGNORECASE) is not None,
            f"{label} lease scenarios lack {contract}",
        )

    privacy_id = PROVIDER_PRIVACY_SCENARIOS[name]
    privacy = sections.get(privacy_id, "")
    for contract, pattern in (
        ("protected-content exclusion", r"(?:no|never|do not).{0,100}(?:prompts?|source content)"),
        ("no uploader", r"no uploader"),
        ("provider-processing caveat", r"(?:provider|codex|copilot|claude).{0,120}(?:process|polic)"),
    ):
        check(
            re.search(pattern, privacy, re.DOTALL | re.IGNORECASE) is not None,
            f"{label} privacy scenario {privacy_id} lacks {contract}",
        )
    check_privacy_contradictions(f"{label} privacy scenario {privacy_id}", privacy)


def privacy_contradictions(text: str) -> list[str]:
    """Return unsafe collection/export claims with action-scoped polarity."""
    sensitive = (
        r"(?:prompts?|source (?:code|content)|file contents?|secrets?|credentials?|"
        r"personal data|raw logs?|external payloads?)"
    )
    actions = (
        r"(?:record(?:s|ed|ing)?|stor(?:e|es|ed|ing)|collect(?:s|ed|ing)?|"
        r"captur(?:e|es|ed|ing)|upload(?:s|ed|ing)?|export(?:s|ed|ing)?|"
        r"send(?:s|ing)?|sent|transmit(?:s|ted|ting)?|includ(?:e|es|ed|ing)|"
        r"retain(?:s|ed|ing)?|persist(?:s|ed|ing)?|"
        r"writ(?:e|es|ten|ing)|wrote|log(?:s|ged|ging)?)"
    )
    violations: list[str] = []

    # Split at sentence and predicate boundaries so one coordinated predicate cannot inherit
    # another predicate's negation (for example, "do not store code and may upload credentials").
    predicate_start = (
        rf"(?:{actions}\b|"
        rf"(?:may|can|should|must|shall|will|always|automatically)\s+{actions}\b|"
        rf"(?:agents?|the workflow|the system|metrics?|we|you|it)\s+"
        rf"(?:may|can|should|must|shall|will|always|automatically|{actions})\b|"
        rf"{sensitive}\b[^,.;:\n]{{0,50}}\b"
        rf"(?:is|are|was|were|may|can|should|must|shall|will)\b)"
    )
    clauses = re.split(
        rf"(?:[.!?;]+(?:\s+|$)|\s*,?\s+\b(?:but|however|except)\b\s+|"
        rf"\s*,?\s+\b(?:and|while|whereas|yet)\b\s+(?={predicate_start})|"
        rf",\s*(?={predicate_start})|"
        rf"\n[ \t]*\n+|\n(?=[ \t]*(?:(?:[-*]|\d+\.)[ \t]+|#{{1,6}}[ \t]+|\|)))",
        text,
        flags=re.IGNORECASE,
    )
    for clause in clauses:
        if product_only_statement(clause):
            continue
        sensitive_matches = list(re.finditer(rf"\b{sensitive}\b", clause, re.IGNORECASE))
        action_matches = [
            action
            for action in re.finditer(rf"\b{actions}\b", clause, re.IGNORECASE)
            if not any(
                action.start() < protected.end() and protected.start() < action.end()
                for protected in sensitive_matches
            )
            and not (
                action.group(0).lower().startswith("log")
                and re.search(
                    r"(?:\b(?:raw|large|full|workflow|command|or|and)\s+|,\s*)$",
                    clause[max(0, action.start() - 20) : action.start()],
                    re.IGNORECASE,
                )
                is not None
            )
            and not (
                action.group(0).lower().startswith("stor")
                and re.search(
                    r"\b(?:dependency|package|artifact|cache)\s+$",
                    clause[max(0, action.start() - 24) : action.start()],
                    re.IGNORECASE,
                )
                is not None
            )
        ]
        if not action_matches or not sensitive_matches:
            continue
        unsafe_pair = False
        for action in action_matches:
            before_action = clause[max(0, action.start() - 260) : action.start()]
            action_is_negated = (
                re.search(
                    r"\b(?:no|not|never|without|nothing|cannot|can't|"
                    r"do not|does not|must not|will not|"
                    r"forbid(?:s|den)?|exclude(?:s|d)?|"
                    r"avoid(?:s|ed|ing)?|refrain(?:s|ed|ing)?\s+from|"
                    r"prohibit(?:s|ed|ing)?|prevent(?:s|ed|ing)?|"
                    r"impossible\s+to)\b[^:;]{0,240}$",
                    before_action,
                    re.IGNORECASE,
                )
                is not None
            )
            for protected in sensitive_matches:
                if action_is_negated:
                    continue
                if protected.start() >= action.end():
                    between = clause[action.end() : protected.start()]
                else:
                    between = clause[protected.end() : action.start()]
                target_is_negated = (
                    re.search(
                        r"\b(?:no|not|never|without|cannot|can't|"
                        r"forbid(?:s|den)?|exclude(?:s|d)?|"
                        r"avoid(?:s|ed|ing)?|refrain(?:s|ed|ing)?\s+from|"
                        r"prohibit(?:s|ed|ing)?|prevent(?:s|ed|ing)?)\b"
                        r"[^:;]{0,200}$",
                        between,
                        re.IGNORECASE,
                    )
                    is not None
                )
                pair_end = max(action.end(), protected.end())
                pair_is_prohibited = (
                    re.search(
                        r"^\s*(?:is|are|was|were)\s+(?:strictly\s+)?"
                        r"(?:prohibited|forbidden|prevented|impossible)\b",
                        clause[pair_end:],
                        re.IGNORECASE,
                    )
                    is not None
                )
                if not target_is_negated and not pair_is_prohibited:
                    unsafe_pair = True
                    break
            if unsafe_pair:
                break
        if unsafe_pair:
            violations.append("affirmative collection of protected content")
            break

    forbidden = [
        (
            r"\bautomatic export\s+(?:is\s+)?(?:enabled|active|performed|run|"
            r"sends?|uploads?|transmits?|forwards?|publishes?|occurs?)\b|"
            r"\boperational metrics\b[^\n.]{0,100}\b(?:are\s+)?automatically\s+exported\b",
            "automatic metrics export",
        ),
        (
            r"\b(?:this|it|the workflow|the system|the service)\s+is\s+"
            r"(?:an?\s+)?author-operated collection\b|"
            r"\b(?:use|enable|perform|run|provide)s?\s+(?:an?\s+)?"
            r"author-operated collection\b",
            "affirmative author-operated collection",
        ),
        (
            rf"\b(?:may|can|should|must|shall|will|always|automatically)\s+"
            rf"{actions}\b[^\n.]{{0,180}}"
            rf"(?:victor(?:'s|’s)?|author(?:'s|’s)?|author-operated)\s+"
            rf"(?:service|backend|server|endpoint|collection)",
            "upload or collection by an author-operated service",
        ),
        (
            r"\b(?:do not|does not|never)\s+send data anywhere\b",
            "absolute no-processing claim",
        ),
        (
            r"\b(?:your data|the data|all data|user data|personal data|"
            r"repository contents?|source code|everything)\s+"
            r"(?:never|does not|cannot)\s+leave(?:s)?\s+"
            r"(?:your|the)\s+(?:machine|computer|repository|repo)\b|"
            r"\b(?:your data|the data|all data|user data|personal data|"
            r"repository contents?|source code|everything)\s+"
            r"(?:always\s+)?(?:remains|stays)\s+"
            r"(?:only\s+)?(?:on|in)\s+(?:your|the)\s+"
            r"(?:machine|computer|repository|repo)\b|"
            r"\b(?:nothing|no data)\s+(?:ever\s+)?leaves\s+"
            r"(?:your|the)\s+(?:machine|computer|repository|repo)\b",
            "absolute locality claim",
        ),
    ]
    for pattern, description in forbidden:
        for match in re.finditer(pattern, text, re.DOTALL | re.IGNORECASE):
            if product_only_statement(
                containing_prose_clause(text, match.start(), match.end())
            ):
                continue
            violations.append(description)
            break
    return list(dict.fromkeys(violations))


def check_privacy_contradictions(label: str, text: str) -> None:
    """Reject permissive, imperative, passive, or automatic collection claims."""
    for description in privacy_contradictions(text):
        check(False, f"{label} contains {description}")


def check_metrics_policy(label: str, text: str) -> None:
    metrics = text.lower()
    for pattern, requirement in (
        (r"not (?:author-operated )?telemetry", "not telemetry"),
        (r"no\s+uploader", "no uploader"),
        (
            r"(?:no|without).{0,80}automatic export|"
            r"automatic export.{0,80}(?:disabled|not enabled|not defined)",
            "no automatic export",
        ),
        (
            r"(?:no|without).{0,100}author-operated collection|"
            r"author-operated collection.{0,80}(?:does not exist|is not enabled)",
            "no author-operated collection",
        ),
        (
            r"(?:never|do not|must not).{0,60}"
            r"(?:record|store|include|write|log).{0,140}prompts",
            "prompt exclusion",
        ),
        (
            r"(?:never|do not|must not).{0,60}"
            r"(?:record|store|include|write|log).{0,180}source code",
            "source-code exclusion",
        ),
        (
            r"(?:never|do not|must not).{0,60}"
            r"(?:record|store|include|write|log).{0,220}secrets",
            "secret exclusion",
        ),
        (
            r"(?:never|do not|must not).{0,60}"
            r"(?:record|store|include|write|log).{0,280}raw logs",
            "raw-log exclusion",
        ),
        (r"not measured", "Not measured"),
        (r"local metrics: off.{0,100}default", "default Off"),
        (r"append.{0,100}only when.{0,40}(?:selects? )?`?on`?", "append only when On"),
        (r"local metrics: on", "On entry marker"),
        (r"(?:latest|at most).{0,40}20 comparable entries", "bounded calibration window"),
        (
            r"(?:compact|archive|delete).{0,140}"
            r"(?:only with|only after)\s+(?:explicit\s+)?(?:the\s+)?"
            r"user(?:'s)?\s+approval",
            "user-controlled retention",
        ),
        (r"never\s+silently\s+delete", "no silent history deletion"),
        (r"(?:provider|codex|copilot|claude).{0,100}(?:process|polic)", "provider-processing caveat"),
    ):
        check(
            re.search(pattern, metrics, re.DOTALL) is not None,
            f"{label} lacks {requirement!r}",
        )
    check_privacy_contradictions(label, text)


def markdown_body(text: str) -> str:
    """Remove a leading frontmatter block from a Markdown role profile."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return text
    try:
        end = lines.index("---", 1)
    except ValueError:
        return text
    return "\n".join(lines[end + 1 :])


def check_provider_entrypoints(
    name: str,
    provider_root: Path,
    entrypoints: dict[str, str],
    policy_overrides: dict[str, str] | None = None,
    contradiction_overrides: dict[str, str] | None = None,
) -> None:
    """Check critical runtime rules in each automatically loaded instruction file."""
    policy_overrides = policy_overrides or {}
    contradiction_overrides = contradiction_overrides or {}
    for entrypoint, authority in entrypoints.items():
        text = read_text(provider_root / entrypoint)
        policy_text = policy_overrides.get(entrypoint, text)
        contradiction_text = contradiction_overrides.get(entrypoint, text)
        lowered = text.lower()
        check_contract_polarity(
            f"{name}: runtime entrypoint {entrypoint}",
            contradiction_text,
        )
        check(
            authority.lower() in lowered,
            f"{name}: {entrypoint} does not reference authoritative {authority}",
        )
        for contract, pattern in (
            (
                "current-revision approval lifecycle",
                r"(?:explicit(?:-user| user)|user explicitly|explicitly).{0,120}"
                r"approv.{0,500}(?:current|approved).{0,80}revision|"
                r"(?:current|approved).{0,80}revision.{0,500}"
                r"(?:explicit(?:-user| user)|user explicitly|explicitly).{0,120}approv",
            ),
            (
                "In Progress write gate",
                r"In\s+Progress.{0,180}(?:first|implementation|write)|"
                r"(?:first|implementation|write).{0,180}In\s+Progress",
            ),
            (
                "execution modes",
                r"Sequential.{0,400}Parallel|Parallel.{0,400}Sequential",
            ),
            ("hard retry ceiling", r"hard(?:\s+retry)?\s+ceiling"),
            (
                "omitted-only defaults",
                r"(?:default|defaults).{0,100}omitted|omitted.{0,100}"
                r"(?:default|defaults)",
            ),
            (
                "invalid explicit control handling",
                r"invalid.{0,100}(?:surface|clarif)|(?:surface|clarif).{0,100}invalid",
            ),
            (
                "unsupported-control fallback",
                r"unsupported.{0,180}(?:safe|safest|supported)\s+"
                r"(?:supported\s+)?(?:runtime\s+)?fallback|"
                r"(?:safe|safest|supported)\s+(?:supported\s+)?(?:runtime\s+)?fallback"
                r".{0,180}unsupported",
            ),
            (
                "mandatory security coverage",
                r"(?:mandatory|required).{0,100}security|security.{0,100}"
                r"(?:mandatory|required|never omit)",
            ),
            ("default local metrics", r"Local metrics: Off"),
            (
                "protected-content privacy boundary",
                r"(?:no|not|never|do not|must not).{0,140}"
                r"(?:prompts?|source (?:code|content)|raw logs?)",
            ),
        ):
            check(
                re.search(pattern, policy_text, re.DOTALL | re.IGNORECASE)
                is not None,
                f"{name}: runtime entrypoint {entrypoint} lacks {contract}",
            )
        check_untrusted_content_contract(
            f"{name}: runtime entrypoint {entrypoint}",
            policy_text,
            contradiction_text=contradiction_text,
        )
        check_external_tool_data_contract(
            f"{name}: runtime entrypoint {entrypoint}",
            policy_text,
            contradiction_text=contradiction_text,
        )
        if entrypoint in policy_overrides:
            full_label = f"{name}: full runtime entrypoint {entrypoint}"
            check_safety_invariants(full_label, contradiction_text)
            check_privacy_contradictions(full_label, contradiction_text)
            check_core_default_contract(
                full_label,
                contradiction_text,
                check_declarations=False,
            )


def check_provider_roles(name: str, provider_root: Path) -> None:
    """Check lifecycle, evidence, retry, and read-only role contracts directly."""
    role_texts = {
        role: markdown_body(read_text(provider_root / relative_path))
        for role, relative_path in PROVIDER_ROLE_FILES[name].items()
    }
    for role, text in role_texts.items():
        check_contract_polarity(f"{name}: {role} role", text)
        check_external_tool_data_contract(f"{name}: {role} role", text)
    orchestrator = role_texts["orchestrator"]
    for contract, pattern in (
        (
            "single memory writer",
            r"(?:sole|single).{0,50}(?:durable[- ]memory|role-memory|memory)"
            r".{0,30}writer|single writer.{0,100}role-memory",
        ),
        (
            "same-role worker quiescence",
            r"active same-role workers?.{0,80}"
            r"(?:(?:has|have)\s+)?(?:stop|stopped|finish|finished)",
        ),
        (
            "memory write lease",
            r"(?:exclusive write lease|path(?:'s)? exclusive write lease)",
        ),
    ):
        check(
            re.search(pattern, orchestrator, re.DOTALL | re.IGNORECASE) is not None,
            f"{name}: orchestrator role lacks {contract}",
        )
    if name == "claude":
        for role in ("architect", "coder"):
            text = role_texts[role]
            check(
                re.search(r"read-only.{0,120}memory|memory.{0,120}read-only", text, re.DOTALL | re.IGNORECASE)
                is not None,
                f"{name}: {role} role must treat role memory as read-only",
            )
            check(
                re.search(
                    r"Orchestrator\s+is\s+the\s+sole\s+memory\s+writer",
                    text,
                    re.IGNORECASE,
                )
                is not None,
                f"{name}: {role} role must return memory candidates to the sole writer",
            )
        coder = role_texts["coder"]
        for contract, pattern in (
            (
                "In Progress-only implementation",
                r"Implement only.{0,140}`In Progress` plan",
            ),
            (
                "Approved-state refusal",
                r"plan is `Approved`.{0,180}stop.{0,100}Do not implement",
            ),
            (
                "Orchestrator-issued active lease",
                r"active.{0,80}lease issued by Orchestrator|"
                r"active Orchestrator-issued leases?",
            ),
        ):
            check(
                re.search(pattern, coder, re.DOTALL | re.IGNORECASE) is not None,
                f"{name}: coder role lacks {contract}",
            )
        check(
            re.search(
                r"Coder may perform.{0,80}status-only update|"
                r"named main-session agent.{0,120}transition",
                coder,
                re.DOTALL | re.IGNORECASE,
            )
            is None,
            f"{name}: coder role must not self-transition Approved to In Progress",
        )
    if name in {"codex", "github-copilot"}:
        for role in ("architect", "coder", "tester", "reviewer"):
            text = role_texts[role]
            check(
                re.search(
                    r"memory candidates?.{0,120}Orchestrator|"
                    r"Orchestrator.{0,120}memory candidates?",
                    text,
                    re.DOTALL | re.IGNORECASE,
                )
                is not None,
                f"{name}: {role} role must return memory candidates to Orchestrator",
            )
    if name == "codex":
        for role in ("architect", "coder", "tester", "reviewer"):
            check(
                re.search(
                    r"(?:do not|must not|never).{0,40}"
                    r"(?:spawn|invoke|delegate).{0,80}subagents?",
                    role_texts[role],
                    re.DOTALL | re.IGNORECASE,
                )
                is not None,
                f"{name}: {role} role must prohibit nested subagent delegation",
            )
    for role in ("orchestrator", "architect"):
        check(
            re.search(r"pre-plan lease", role_texts[role], re.IGNORECASE) is not None,
            f"{name}: {role} role lacks pre-plan write ownership",
        )
    check(
        re.search(
            r"read-only evidence contributor",
            role_texts["architect"],
            re.IGNORECASE,
        )
        is not None,
        f"{name}: architect role lacks read-only parallel contributor behavior",
    )
    for role in ("tester", "reviewer"):
        text = role_texts[role]
        for contract, pattern in (
            ("named active plan", r"named active.{0,120}plan|named.{0,120}active plan"),
            ("In Progress status", r"In\s+Progress"),
            (
                "matching current-revision explicit approval",
                r"explicit(?:-user| user).{0,80}approv.{0,120}current.{0,80}revision"
                r"|current.{0,80}revision.{0,120}explicit(?:-user| user).{0,80}approv",
            ),
        ):
            check(
                re.search(pattern, text, re.DOTALL | re.IGNORECASE) is not None,
                f"{name}: {role} role lacks {contract}",
            )
        for refused in (
            "Proposed",
            "Approved",
            "Done",
            "Superseded",
            "Abandoned",
            "missing",
            "ambiguous",
            "revision-mismatched",
        ):
            check(
                refused.lower() in text.lower(),
                f"{name}: {role} role does not refuse {refused!r} plan state",
            )
    for role in ("tester", "reviewer"):
        text = role_texts[role]
        for contract, pattern in (
            (
                "generated-artifact reporting",
                r"(?:generated|transient)\s+artifacts?.{0,180}report|"
                r"report.{0,180}(?:generated|transient)\s+artifacts?",
            ),
            (
                "orchestrator-owned cleanup",
                r"(?:cleanup|retention|clean|retain).{0,180}Orchestrator|"
                r"Orchestrator.{0,180}(?:cleanup|retention|clean|retain)",
            ),
            (
                "isolated mutable command outputs",
                r"(?:parallel|concurrent).{0,180}(?:share|shared|same).{0,80}"
                r"(?:output|cache).{0,180}(?:isolat|avoid|do not)",
            ),
        ):
            check(
                re.search(pattern, text, re.DOTALL | re.IGNORECASE) is not None,
                f"{name}: {role} role lacks {contract}",
            )

    for role in ("orchestrator", "architect", "coder", "tester", "reviewer"):
        check_fingerprint_contract(f"{name}: {role} role", role_texts[role])

    for role in ("coder", "tester"):
        text = role_texts[role]
        for contract, pattern in (
            ("hard retry ceiling", r"hard(?:\s+retry)?\s+ceiling"),
            (
                "retry exhaustion stop",
                r"exhaust.{0,140}stop|stop.{0,140}exhaust|"
                r"(?:ceiling|limit).{0,120}(?:reached|used).{0,100}stop",
            ),
            (
                "no hypothesis-only reset",
                r"new hypothesis alone.{0,100}(?:does not|cannot).{0,80}reset",
            ),
        ):
            check(
                re.search(pattern, text, re.DOTALL | re.IGNORECASE) is not None,
                f"{name}: {role} role lacks {contract}",
            )


def check_provider(name: str, config: dict[str, object]) -> None:
    provider_root = config["root"]
    assert isinstance(provider_root, Path)
    required = list(config["required"]) + SHARED_DOCS

    check(provider_root.is_dir(), f"{relative(provider_root)} is missing")
    for item in required:
        check((provider_root / item).is_file(), f"{name}: missing required file {item}")

    actual_files = [
        path
        for path in provider_root.rglob("*")
        if path.is_file() and not IGNORED_PARTS.intersection(path.relative_to(provider_root).parts)
    ]
    check(
        len(actual_files) == 32,
        f"{name}: expected 32 distribution files, found {len(actual_files)}",
    )
    check_notice_file(
        f"{name}: THIRD_PARTY_NOTICES.md",
        read_text(provider_root / "THIRD_PARTY_NOTICES.md"),
    )

    readme_path = provider_root / str(config["readme"])
    readme = read_text(readme_path)
    readme_lower = readme.lower()
    check("## install into a project" in readme_lower, f"{name}: README lacks installation steps")
    check("no telemetry" in readme_lower, f"{name}: README lacks a no-telemetry statement")
    check("source code" in readme_lower, f"{name}: README privacy text must mention source code")
    check(
        "author-operated service" in readme_lower,
        f"{name}: README must say data is not sent to an author-operated service",
    )
    for notice_contract, pattern in LICENSE_NOTICE_CONTRACT_PATTERNS.items():
        check(
            re.search(pattern, readme, re.DOTALL | re.IGNORECASE) is not None,
            f"{name}: README lacks {notice_contract}",
        )
    check(
        sum(
            info.lower() == "mermaid"
            for info, _, _ in fenced_blocks(
                markdown_without_html_comments(readme)
            )
        )
        >= 3,
        f"{name}: README should retain at least three explanatory Mermaid diagrams",
    )
    _, scenario_count = PROVIDER_SCENARIO_COUNTS[name]
    check(
        re.search(
            rf"current\s+suite\s+contains\s+{scenario_count}\s+scenarios",
            readme,
            re.IGNORECASE,
        )
        is not None,
        (
            f"{name}: README must state the current conformance-suite count "
            f"({scenario_count})"
        ),
    )
    check_activation_prompts(f"{name} README", readme)
    check_external_tool_data_contract(f"{name}: README", readme)
    check_first_run_adaptation_contract(f"{name}: README", readme)
    primary_instruction = {
        "codex": "AGENTS.md",
        "github-copilot": "AGENTS.md",
        "claude": "CLAUDE.md",
    }[name]
    check_first_run_adaptation_contract(
        f"{name}: {primary_instruction}",
        read_text(provider_root / primary_instruction),
    )
    if name == "github-copilot":
        copilot_instructions = read_text(
            provider_root / ".github/copilot-instructions.md"
        )
        for contract, pattern in (
            ("explicit maintenance operation", r"explicit.{0,80}approval-gated"),
            ("no silent rewrite", r"never rewrite.{0,100}silently"),
            ("evidence-first inventory", r"bounded.{0,80}evidence-first inventory"),
            ("revisioned exact diff", r"revisioned exact diff"),
            ("approval before write", r"stop before writing.{0,100}approved"),
            ("product-code exclusion", r"no product-code changes"),
            ("conformance validation", r"first-run adaptation scenario"),
        ):
            check(
                re.search(
                    pattern,
                    copilot_instructions,
                    re.DOTALL | re.IGNORECASE,
                )
                is not None,
                (
                    "github-copilot: .github/copilot-instructions.md first-run "
                    f"adaptation lacks {contract}"
                ),
            )
    authority = next(iter(dict(config["entrypoints"]).values()))
    for document_label, document in (
        ("README", readme),
        (authority, read_text(provider_root / authority)),
    ):
        check(
            f"Workflow contract version: {WORKFLOW_CONTRACT_VERSION}" in document,
            (
                f"{name}: {document_label} must declare workflow contract version "
                f"{WORKFLOW_CONTRACT_VERSION}"
            ),
        )
    if name == "github-copilot":
        bounded_flow_docs = (
            (
                "README cloud-agent approval section",
                "\n".join(
                    markdown_h2_sections(
                        readme,
                        r"Copilot Cloud-Agent Approval Gate",
                    )
                ),
            ),
            (
                "authority activation section",
                "\n".join(
                    markdown_h2_sections(
                        read_text(provider_root / authority),
                        r"Activation",
                    )
                ),
            ),
        )
    elif name == "claude":
        bounded_flow_docs = (
            (
                "README non-interactive section",
                "\n".join(
                    markdown_h2_sections(
                        readme,
                        r"Non-Interactive Approval Gate",
                    )
                ),
            ),
            (
                "authority non-interactive section",
                "\n".join(
                    markdown_h2_sections(
                        read_text(provider_root / authority),
                        r"Non-Interactive Runs",
                    )
                ),
            ),
        )
    else:
        bounded_flow_docs = ()
    for flow_label, flow in bounded_flow_docs:
        for contract, pattern in (
            (
                "Orchestrator-owned planning run",
                r"(?:select|use|run)\s+`orchestrator`.{0,180}planning-only|"
                r"(?:select|use|run)\s+`orchestrator`.{0,220}planning stage|"
                r"(?:prepare|produce).{0,80}plan.{0,120}"
                r"(?:select|use|run)\s+`orchestrator`",
            ),
            ("pre-plan lease ownership", r"pre-plan\s+lease"),
            (
                "later Orchestrator implementation run",
                r"(?:later|separate).{0,180}`orchestrator`.{0,220}"
                r"(?:Approved|implementation|end-to-end|names?|naming)",
            ),
        ):
            check(
                re.search(pattern, flow, re.DOTALL | re.IGNORECASE) is not None,
                f"{name}: {flow_label} lacks {contract}",
            )
        check(
            re.search(
                r"(?:select|use|run)\s+`architect`.{0,120}planning-only",
                flow,
                re.DOTALL | re.IGNORECASE,
            )
            is None,
            f"{name}: {flow_label} incorrectly starts planning with direct Architect",
        )
        check(
            re.search(
                r"(?:later|separate)\s+`orchestrator`\s+or\s+`coder`",
                flow,
                re.IGNORECASE,
            )
            is None,
            f"{name}: {flow_label} lets direct Coder own the end-to-end run",
        )
    check_provider_entrypoints(name, provider_root, dict(config["entrypoints"]))
    check_provider_roles(name, provider_root)
    check_exact_failure_classes(
        f"{name}: authoritative failure matrix",
        read_text(provider_root / PROVIDER_FAILURE_AUTHORITIES[name]),
    )

    core_text = "\n".join(read_text(provider_root / path) for path in config["core"]).lower()
    for mechanism, pattern in MECHANISMS.items():
        check(
            re.search(pattern, core_text, re.DOTALL | re.IGNORECASE) is not None,
            f"{name}: core instructions do not cover {mechanism}",
        )
    for invariant in (
        "approve",
        "sequential",
        "parallel",
        "security",
        "not measured",
        "25%",
    ):
        check(invariant in core_text, f"{name}: core instructions lack invariant {invariant!r}")
    check_untrusted_content_contract(f"{name}: core instructions", core_text)
    check_external_tool_data_contract(f"{name}: core instructions", core_text)
    check_core_default_contract(f"{name}: core instructions", core_text)
    for contract, pattern in {**RETRY_CONTRACT_PATTERNS, **LEASE_CONTRACT_PATTERNS}.items():
        check(
            re.search(pattern, core_text, re.DOTALL | re.IGNORECASE) is not None,
            f"{name}: core instructions lack {contract}",
        )
    check_fingerprint_contract(f"{name}: core instructions", core_text)
    check(
        "pre-plan lease" in core_text,
        f"{name}: core instructions lack pre-plan Architect write ownership",
    )
    for local_metrics_contract, pattern in (
        ("Off value", r"local metrics: off"),
        ("default Off", r"(?:defaults? to|is the default).{0,20}`?off`?"),
        (
            "append only when On",
            r"(?:only when|when).{0,60}user selects `?on`?|"
            r"append.{0,60}only when.{0,40}local metrics: on",
        ),
    ):
        check(
            re.search(pattern, core_text, re.DOTALL | re.IGNORECASE) is not None,
            f"{name}: core instructions lack local-metrics rule {local_metrics_contract!r}",
        )

    conformance_path = provider_root / str(config["conformance"])
    conformance = read_text(conformance_path)
    check_provider_conformance(name, f"{name}: conformance suite", conformance)
    for term in ("approval", "privacy", "security", "blocked"):
        check(term in conformance.lower(), f"{name}: conformance suite lacks {term} coverage")

    plan_template = read_text(provider_root / "docs/implementation-plans/IP-TEMPLATE.md")
    for mechanism, pattern in MECHANISMS.items():
        check(
            re.search(pattern, plan_template, re.DOTALL | re.IGNORECASE) is not None,
            f"{name}: implementation-plan template does not represent {mechanism}",
        )
    check_plan_defaults(f"{name}: implementation-plan template", plan_template)
    check_fingerprint_contract(f"{name}: implementation-plan template", plan_template)
    for plan_contract, pattern in (
        (
            "contract version",
            rf"Workflow contract version:\s*{re.escape(WORKFLOW_CONTRACT_VERSION)}",
        ),
        ("task-packet revision", r"Task-packet (?:revision|version):\s*1"),
        (
            "contract migration rule",
            r"contract changes.{0,180}In Progress.{0,220}(?:review|explicitly accepted)",
        ),
        (
            "sensitive-hash read minimization",
            r"do not.{0,80}read.{0,80}sensitive.{0,80}solely.{0,80}"
            r"(?:calculate|compute).{0,40}(?:a )?hash",
        ),
    ):
        check(
            re.search(pattern, plan_template, re.DOTALL | re.IGNORECASE) is not None,
            f"{name}: implementation-plan template lacks {plan_contract}",
        )
    plan_readme = read_text(
        provider_root / "docs/implementation-plans/README.md"
    )
    for lifecycle_contract, pattern in (
        (
            "blocked-plan status",
            r"temporarily blocked.{0,140}In Progress.{0,180}unblock condition",
        ),
        (
            "explicit-stop abandonment",
            r"Abandoned.{0,100}explicit stop|explicit stop.{0,100}Abandoned",
        ),
    ):
        check(
            re.search(pattern, plan_readme, re.DOTALL | re.IGNORECASE) is not None,
            f"{name}: implementation-plan guidance lacks {lifecycle_contract}",
        )
    for allowed_contract, pattern in (
        ("efficiency profiles", r"`Economy`.{0,80}`Balanced`.{0,80}`Thorough`"),
        ("positive token budget", r"token budget.{0,80}`Auto` or a positive integer"),
        (
            "execution modes",
            r"`Sequential` or `Parallel`|`Sequential`.{0,40}`Parallel`|"
            r"allowed(?: modes)?:.{0,80}Sequential.{0,40}Parallel",
        ),
        (
            "integration modes",
            r"`Auto`.{0,80}`Leased writers`.{0,80}`Single integrator`",
        ),
        ("local metrics values", r"local metrics.{0,80}`Off` or `On`"),
    ):
        check(
            re.search(pattern, plan_template, re.DOTALL | re.IGNORECASE) is not None,
            f"{name}: implementation-plan template lacks allowed {allowed_contract}",
        )
    failure_contract = "\n".join((core_text, plan_template.lower(), conformance.lower()))
    for failure_class, pattern in FAILURE_CLASSES.items():
        check(
            re.search(pattern, failure_contract, re.IGNORECASE) is not None,
            f"{name}: failure matrix lacks canonical class {failure_class!r}",
        )

    provider_text = "\n\n".join(
        read_text(path) for path in actual_files if is_text_file(path)
    )
    for obsolete in OBSOLETE_CONTROLS:
        check(obsolete not in provider_text, f"{name}: obsolete control spelling remains: {obsolete}")
    check_privacy_contradictions(f"{name}: provider distribution", provider_text)
    check_contract_polarity(f"{name}: provider distribution", provider_text)
    check_safety_invariants(f"{name}: provider distribution", provider_text)
    check(
        re.search(
            r"security-sensitive.{0,180}unless the user explicitly scopes.{0,180}lower risk",
            provider_text,
            re.DOTALL | re.IGNORECASE,
        )
        is None,
        f"{name}: provider distribution permits preference-based security-risk downgrade",
    )

    session_text = read_text(provider_root / str(config["session"]))
    check(
        f"Workflow contract version: {WORKFLOW_CONTRACT_VERSION}" in session_text,
        f"{name}: session state lacks workflow contract version",
    )
    check(
        re.search(r"Task-packet (?:revision|version):", session_text) is not None,
        f"{name}: session state lacks task-packet revision",
    )
    check(
        re.search(r"Active plan status:", session_text) is not None,
        f"{name}: session state lacks active plan status",
    )
    check(
        re.search(r"(?:Explicit )?Approval evidence reference:", session_text, re.IGNORECASE)
        is not None,
        f"{name}: session state lacks explicit approval-evidence reference",
    )

    memory_root = provider_root / str(config["memory"])
    memory_readme_path = memory_root / "README.md"
    memory_readme = read_text(memory_readme_path).lower() if memory_readme_path.is_file() else ""
    for role_path_text in config["role_memory"]:
        role_path = provider_root / str(role_path_text)
        role_memory = read_text(role_path).lower()
        has_inline_contract = (
            "source" in role_memory
            and re.search(r"last[- ]confirmed", role_memory) is not None
            and "invalidation" in role_memory
        )
        references_shared_contract = (
            "memory/readme.md" in role_memory
            and "provenance" in role_memory
            and "source" in memory_readme
            and re.search(r"last[- ]confirmed", memory_readme) is not None
            and "invalidation" in memory_readme
        )
        check(
            has_inline_contract or references_shared_contract,
            f"{name}: {role_path_text} lacks or does not reference the provenance contract",
        )

    check_metrics_policy(
        f"{name}: workflow metrics policy",
        read_text(provider_root / str(config["metrics"])),
    )


FORBIDDEN_CODEX_MODEL_KEYS = {
    "model",
    "model_reasoning_effort",
    "default_subagent_model",
    "default_subagent_reasoning_effort",
    "default_subagent_model_reasoning_effort",
}


def nested_forbidden_keys(data: object, prefix: str = "") -> list[str]:
    """Return paths to model/effort keys that would override user or runtime settings."""
    found: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            key_text = str(key)
            path = f"{prefix}.{key_text}" if prefix else key_text
            if key_text in FORBIDDEN_CODEX_MODEL_KEYS:
                found.append(path)
            found.extend(nested_forbidden_keys(value, path))
    elif isinstance(data, list):
        for index, value in enumerate(data):
            found.extend(nested_forbidden_keys(value, f"{prefix}[{index}]"))
    return found


def check_codex_toml_data(
    label: str,
    data: dict[str, object],
    expected_name: str | None,
    *,
    strict_shape: bool = True,
) -> str | None:
    """Validate config or role semantics after successful TOML parsing."""
    forbidden = (
        []
        if expected_name is None and not strict_shape
        else nested_forbidden_keys(data)
    )
    check(
        not forbidden,
        f"{label} hardcodes model or reasoning settings: {', '.join(forbidden)}",
    )
    if expected_name is None:
        agents = data.get("agents")
        if strict_shape:
            check(
                set(data) == {"agents"},
                (
                    f"{label} top-level keys must be exactly ['agents']; "
                    f"found {sorted(str(key) for key in data)}"
                ),
            )
            check(
                isinstance(agents, dict) and set(agents) == {"enabled"},
                (
                    f"{label} [agents] keys must be exactly ['enabled']; found "
                    f"{sorted(str(key) for key in agents) if isinstance(agents, dict) else []}"
                ),
            )
        check(
            isinstance(agents, dict) and agents.get("enabled") is True,
            f"{label} must set [agents].enabled = true",
        )
        return None

    required_fields = {"name", "description", "developer_instructions"}
    check(
        set(data) == required_fields
        if strict_shape
        else required_fields.issubset(data),
        (
            f"{label} keys must "
            f"{'be exactly' if strict_shape else 'include'} "
            f"{sorted(required_fields)}; "
            f"found {sorted(str(key) for key in data)}"
        ),
    )
    for field in sorted(required_fields):
        value = data.get(field)
        check(
            isinstance(value, str) and bool(value.strip()),
            f"{label} needs a non-empty {field}",
        )
    name = data.get("name")
    check(name == expected_name, f"{label} name must be {expected_name!r}")
    return name.strip() if isinstance(name, str) else None


def check_codex_toml_root(
    root: Path,
    label_prefix: str,
    *,
    strict_config_shape: bool = True,
    strict_role_shape: bool = True,
) -> None:
    """Validate one Codex workflow tree's project config and five role profiles."""
    if tomllib is None:
        fail("Python 3.11+ is required to validate TOML")
        return
    toml_paths = [
        root / ".codex/config.toml",
        *[
            root / f".codex/agents/{role}.toml"
            for role in sorted(EXPECTED_ROLES)
        ],
    ]
    names: set[str] = set()
    for path in toml_paths:
        if not path.is_file():
            continue
        try:
            data = tomllib.loads(read_text(path))
        except tomllib.TOMLDecodeError as exc:
            fail(f"{relative(path)} is invalid TOML: {exc}")
            continue
        if path.parent.name == "agents":
            name = check_codex_toml_data(
                relative(path),
                data,
                path.stem,
                strict_shape=strict_role_shape,
            )
            if name is not None:
                check(name not in names, f"duplicate Codex agent name {name!r}")
                names.add(name)
        else:
            check_codex_toml_data(
                relative(path),
                data,
                None,
                strict_shape=strict_config_shape,
            )
    check(
        names == {"orchestrator", "architect", "coder", "tester", "reviewer"},
        f"{label_prefix} Codex agent names are incomplete: {sorted(names)}",
    )


def check_codex_toml() -> None:
    check_codex_toml_root(
        ROOT / "codex-agentic-workflow",
        "repository distribution",
    )


def has_exact_role_set(names: set[str]) -> bool:
    """Return whether agent filenames name exactly the five canonical roles."""
    return names == EXPECTED_ROLES


def split_top_level_commas(value: str) -> list[str]:
    """Split a flat tool list without splitting commas inside parentheses."""
    items: list[str] = []
    start = 0
    depth = 0
    for index, character in enumerate(value):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth < 0:
                return []
        elif character == "," and depth == 0:
            item = value[start:index].strip()
            if item:
                items.append(item)
            start = index + 1
    if depth != 0:
        return []
    final = value[start:].strip()
    if final:
        items.append(final)
    return items


def check_exact_tool_allowlist(
    label: str,
    actual: set[str],
    expected: set[str] | None,
) -> None:
    """Require a role's parsed tool set to equal its canonical allowlist."""
    check(
        expected is not None and actual == expected,
        f"{label} tools must be the canonical role allowlist; found {sorted(actual)}",
    )


def check_exact_frontmatter_keys(
    label: str,
    fields: dict[str, str],
    expected: set[str],
) -> None:
    """Reject misspelled, ignored, or unsupported provider frontmatter keys."""
    check(
        set(fields) == expected,
        (
            f"{label} frontmatter fields must be exactly {sorted(expected)}; "
            f"found {sorted(fields)}"
        ),
    )


def check_github_agent_prompt_length(label: str, text: str) -> None:
    """Enforce GitHub Copilot's custom-agent Markdown prompt-body limit."""
    body_length = len(markdown_body(text))
    check(
        body_length <= GITHUB_AGENT_PROMPT_MAX_CHARACTERS,
        (
            f"{label} prompt body has {body_length} characters; GitHub Copilot "
            f"allows at most {GITHUB_AGENT_PROMPT_MAX_CHARACTERS}"
        ),
    )


def check_claude_agent_color(label: str, color: str) -> None:
    """Require one of Claude Code's documented subagent color values."""
    check(
        color in CLAUDE_AGENT_COLORS,
        (
            f"{label} color must be one of {sorted(CLAUDE_AGENT_COLORS)}; "
            f"found {color!r}"
        ),
    )


def check_frontmatter_files() -> None:
    github_agents = sorted(
        (ROOT / "github-copilot-agentic-workflow/.github/agents").glob("*.agent.md")
    )
    claude_agents = sorted((ROOT / "claude-agentic-workflow/.claude/agents").glob("*.md"))
    paths = [
        *github_agents,
        ROOT / "github-copilot-agentic-workflow/.github/skills/SKILL-TEMPLATE.md",
        *claude_agents,
        ROOT / "claude-agentic-workflow/.claude/skills/SKILL-TEMPLATE.md",
        ROOT / "claude-agentic-workflow/.claude/skills/agentic-workflow/SKILL.md",
        ROOT / "codex-agentic-workflow/.agents/skills/SKILL-TEMPLATE.md",
    ]
    fields_by_path: dict[Path, dict[str, str]] = {}
    for path in paths:
        check(path.is_file(), f"missing frontmatter file {relative(path)}")
        if path.is_file():
            fields = parse_frontmatter_fields(relative(path), read_text(path))
            if fields is not None:
                fields_by_path[path] = fields
                for field in ("name", "description"):
                    check(
                        bool(fields.get(field)),
                        f"{relative(path)} frontmatter needs a non-empty {field}",
                    )
                if path in github_agents:
                    expected_fields = {"name", "description", "tools"}
                elif path in claude_agents:
                    expected_fields = {
                        "name",
                        "description",
                        "tools",
                        "model",
                        "color",
                    }
                    if path.stem == "orchestrator":
                        expected_fields.add("memory")
                elif "claude-agentic-workflow" in path.parts:
                    expected_fields = {"name", "description", "argument-hint"}
                else:
                    expected_fields = {"name", "description"}
                check_exact_frontmatter_keys(
                    relative(path),
                    fields,
                    expected_fields,
                )

    github_names = {path.name.removesuffix(".agent.md") for path in github_agents}
    claude_names = {path.stem for path in claude_agents}
    check(
        has_exact_role_set(github_names),
        (
            "GitHub Copilot agent filenames must be the exact canonical role set; "
            f"found {sorted(github_names)}"
        ),
    )
    check(
        has_exact_role_set(claude_names),
        (
            "Claude agent filenames must be the exact canonical role set; "
            f"found {sorted(claude_names)}"
        ),
    )
    for path in [*github_agents, *claude_agents]:
        fields = fields_by_path.get(path, {})
        declared = fields.get("name", "")
        expected = path.name.removesuffix(".agent.md") if path.name.endswith(".agent.md") else path.stem
        check(declared == expected, f"{relative(path)} name must match filename {expected!r}")

    github_tool_sets = {
        "orchestrator": {"read", "search", "edit", "execute", "agent", "web"},
        "architect": {"read", "search", "edit", "web"},
        "coder": {"read", "search", "edit", "execute"},
        "tester": {"read", "search", "execute"},
        "reviewer": {"read", "search", "execute", "web"},
    }
    for path in github_agents:
        fields = fields_by_path.get(path, {})
        name = path.name.removesuffix(".agent.md")
        check_github_agent_prompt_length(relative(path), read_text(path))
        raw_tools = fields.get("tools", "")
        match = re.fullmatch(r"\[\s*(.*?)\s*\]", raw_tools)
        tools = (
            {item.strip() for item in match.group(1).split(",") if item.strip()}
            if match is not None
            else set()
        )
        expected_tools = github_tool_sets.get(name)
        check_exact_tool_allowlist(
            relative(path),
            tools,
            expected_tools,
        )
        check(
            "model" not in fields,
            f"{relative(path)} must inherit the user/runtime model rather than pinning one",
        )

    claude_tool_sets = {
        "orchestrator": {
            "Agent(architect, coder, tester, reviewer)",
            "SendMessage",
            "TaskList",
            "TaskStop",
            "Read",
            "Glob",
            "Grep",
            "Bash",
            "PowerShell",
            "Edit",
            "Write",
            "Skill",
            "WebSearch",
            "WebFetch",
        },
        "architect": {
            "Read",
            "Glob",
            "Grep",
            "Edit",
            "Write",
            "Skill",
            "WebSearch",
            "WebFetch",
        },
        "coder": {
            "Read",
            "Glob",
            "Grep",
            "Bash",
            "PowerShell",
            "Edit",
            "Write",
            "Skill",
        },
        "tester": {"Read", "Glob", "Grep", "Bash", "PowerShell", "Skill"},
        "reviewer": {
            "Read",
            "Glob",
            "Grep",
            "Bash",
            "PowerShell",
            "Skill",
            "WebSearch",
            "WebFetch",
        },
    }
    for path in claude_agents:
        fields = fields_by_path.get(path, {})
        name = path.stem
        check_claude_agent_color(relative(path), fields.get("color", ""))
        tools = set(split_top_level_commas(fields.get("tools", "")))
        expected_tools = claude_tool_sets.get(name)
        check_exact_tool_allowlist(
            relative(path),
            tools,
            expected_tools,
        )
        check(
            fields.get("model") == "inherit",
            f"{relative(path)} must use model: inherit",
        )
        if name == "orchestrator":
            check(
                fields.get("memory") == "project",
                f"{relative(path)} must use project-scoped coordinator memory",
            )
        else:
            check(
                "memory" not in fields,
                (
                    f"{relative(path)} must omit memory so parallel same-role workers "
                    "cannot race on Claude-managed memory"
                ),
            )


def extract_template_targets(
    template_path: Path,
) -> list[tuple[str, str, str, int]]:
    """Extract path, fence info, body, and heading line from the bootstrap bundle."""
    lines = read_text(template_path).splitlines()
    records: list[tuple[str, str, str, int]] = []
    index = 0
    while index < len(lines):
        match = re.fullmatch(r"## `([^`]+)`\s*", lines[index])
        if match is None:
            index += 1
            continue
        target = match.group(1)
        heading_line = index + 1
        fence_index = index + 1
        while fence_index < len(lines) and not lines[fence_index].strip():
            fence_index += 1
        opened = fence_open(lines[fence_index]) if fence_index < len(lines) else None
        if opened is None:
            fail(
                f"{relative(template_path)}:{heading_line} target {target!r} "
                "must be followed by a fenced body"
            )
            index += 1
            continue
        marker, minimum_length, info = opened
        closing_index = fence_index + 1
        while closing_index < len(lines) and not is_fence_close(
            lines[closing_index], marker, minimum_length
        ):
            closing_index += 1
        if closing_index >= len(lines):
            fail(
                f"{relative(template_path)}:{fence_index + 1} target {target!r} "
                "has an unclosed body"
            )
            break
        body = "\n".join(lines[fence_index + 1 : closing_index])
        records.append((target, info, body, heading_line))
        index = closing_index + 1
    return records


def check_embedded_toml(label: str, text: str, expected_name: str | None = None) -> None:
    if tomllib is None:
        fail("Python 3.11+ is required to validate embedded TOML")
        return
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        fail(f"{label} is invalid TOML: {exc}")
        return
    check_codex_toml_data(label, data, expected_name)


def check_bootstrap_role_contracts(
    label: str,
    role_texts: dict[str, str],
) -> None:
    """Validate the intentionally compact Codex roles generated by the manual kit."""
    contracts = {
        "orchestrator": {
            "current-revision approval gate": (
                r"explicit-user approval evidence.{0,120}approved plan revision"
                r".{0,220}In Progress"
            ),
            "pre-plan write ownership": r"pre-plan lease",
            "hard retry ceiling": r"hard retry ceiling",
            "single active writer": r"one active writer per file or overlapping path",
            "single memory writer": r"sole durable-memory writer",
            "same-role worker quiescence": (
                r"active same-role workers?.{0,80}"
                r"(?:(?:has|have)\s+)?(?:stop|stopped|finish|finished)"
            ),
            "memory write lease": r"memory path.{0,80}exclusive write lease",
        },
        "architect": {
            "pre-plan write ownership": r"pre-plan lease",
            "read-only contributor": r"read-only evidence contributor",
            "no implementation": r"Do not implement code",
            "Proposed lifecycle": r"Mark new plans as `Proposed`",
            "no nested delegation": (
                r"Do not spawn, invoke, or delegate to subagents"
            ),
            "memory candidate handoff": (
                r"provenance-bearing (?:memory )?candidates?.{0,80}Orchestrator"
            ),
        },
        "coder": {
            "current-revision approval gate": (
                r"explicit-user approval record matches the.{0,80}current revision"
                r".{0,120}In Progress|"
                r"explicit user approval of the current revision.{0,120}In Progress"
            ),
            "refused inactive lifecycle states": (
                r"Proposed.{0,80}Approved.{0,80}Done.{0,80}"
                r"Superseded.{0,80}Abandoned.{0,80}missing.{0,80}ambiguous"
                r".{0,80}revision-mismatched"
            ),
            "retry exhaustion": r"retry budget\s+is\s+exhausted",
            "no hypothesis-only reset": (
                r"new hypothesis alone\s+does not\s+reset an exhausted retry allowance"
            ),
            "no nested delegation": (
                r"Do not spawn, invoke, or delegate to subagents"
            ),
            "memory candidate handoff": (
                r"provenance-bearing (?:memory )?candidates?.{0,80}Orchestrator"
            ),
        },
        "tester": {
            "current-revision approval gate": (
                r"named active `In Progress` plan.{0,120}explicit[- ]user approval record"
                r".{0,80}current revision"
            ),
            "read-only validation": r"This is a read-only role",
            "hard retry ceiling": r"hard retry ceiling",
            "no hypothesis-only reset": (
                r"new hypothesis alone does not reset the allowance"
            ),
            "isolated parallel validation": (
                r"parallel.{0,160}share.{0,120}(?:output|cache).{0,180}isolated"
            ),
            "artifact reporting": (
                r"(?:transient|generated)\s+artifacts?.{0,120}report|"
                r"report.{0,120}(?:transient|generated)\s+artifacts?"
            ),
            "no nested delegation": (
                r"Do not spawn, invoke, or delegate to subagents"
            ),
            "memory candidate handoff": (
                r"provenance-bearing (?:memory )?candidates?.{0,80}Orchestrator"
            ),
        },
        "reviewer": {
            "current-revision approval gate": (
                r"named active `In Progress` plan.{0,120}explicit[- ]user approval record"
                r".{0,80}current revision"
            ),
            "read-only review": r"This is a read-only role",
            "stable finding IDs": r"stable ID",
            "mandatory security coverage": r"Never omit mandatory security review",
            "no nested delegation": (
                r"Do not spawn, invoke, or delegate to subagents"
            ),
            "memory candidate handoff": (
                r"provenance-bearing (?:memory )?candidates?.{0,80}Orchestrator"
            ),
            "generated-artifact reporting": (
                r"(?:generated|transient)\s+artifacts?.{0,180}report|"
                r"report.{0,180}(?:generated|transient)\s+artifacts?"
            ),
            "orchestrator-owned cleanup": (
                r"(?:cleanup|retention|clean|retain).{0,180}Orchestrator|"
                r"Orchestrator.{0,180}(?:cleanup|retention|clean|retain)"
            ),
            "isolated mutable command outputs": (
                r"(?:parallel|concurrent).{0,180}(?:share|shared|same).{0,80}"
                r"(?:output|cache).{0,180}(?:isolat|avoid|do not)"
            ),
        },
    }
    check(
        set(role_texts) == EXPECTED_ROLES,
        f"{label} role set must be exactly {sorted(EXPECTED_ROLES)}",
    )
    for role, role_contracts in contracts.items():
        text = role_texts.get(role, "")
        check_safety_invariants(f"{label} {role} role", text)
        check_external_tool_data_contract(f"{label} {role} role", text)
        check_fingerprint_contract(f"{label} {role} role", text)
        for contract, pattern in role_contracts.items():
            check(
                re.search(pattern, text, re.DOTALL | re.IGNORECASE) is not None,
                f"{label} {role} role lacks {contract}",
            )
    tester = role_texts.get("tester", "")
    for failure_class, pattern in FAILURE_CLASSES.items():
        check(
            re.search(pattern, tester, re.IGNORECASE) is not None,
            f"{label} tester role lacks failure class {failure_class!r}",
        )


def check_embedded_conformance(label: str, conformance: str) -> None:
    """Validate the table-based conformance suite shipped by the bootstrap kit."""
    visible = markdown_contract_text(conformance)
    rows = {
        match.group(1): match.group(0)
        for match in re.finditer(
            r"^\|\s*(WF-\d+)\s*\|.*\|\s*$",
            visible,
            re.MULTILINE,
        )
    }
    headings = re.findall(r"^\|\s*(WF-\d+)\s*\|", visible, re.MULTILINE)
    expected_ids = set(EMBEDDED_CONFORMANCE_SCENARIOS)
    check(
        set(headings) == expected_ids,
        (
            f"{label} scenario IDs differ from the exact contract; "
            f"missing={sorted(expected_ids - set(headings))}, "
            f"unexpected={sorted(set(headings) - expected_ids)}"
        ),
    )
    check(
        len(headings) == len(set(headings)),
        f"{label} contains duplicate scenario IDs",
    )
    for scenario_id, pattern in EMBEDDED_CONFORMANCE_SCENARIOS.items():
        check(
            re.search(
                pattern,
                rows.get(scenario_id, ""),
                re.DOTALL | re.IGNORECASE,
            )
            is not None,
            f"{label} row {scenario_id} does not implement its contract",
        )
    check_external_tool_data_contract(
        f"{label} row WF-27",
        rows.get("WF-27", ""),
    )
    check_first_run_adaptation_contract(
        f"{label} row WF-28",
        rows.get("WF-28", ""),
    )
    failure_values = [
        normalize_failure_class(value)
        for value in re.findall(r"`([^`]+)`", rows.get("WF-17", ""))
    ]
    failure_counts = Counter(failure_values)
    expected_failures = set(FAILURE_CLASSES)
    check(
        set(failure_values) == expected_failures,
        (
            f"{label} row WF-17 differs from the exact failure-class set; "
            f"missing={sorted(expected_failures - set(failure_values))}, "
            f"extra={sorted(set(failure_values) - expected_failures)}"
        ),
    )
    check(
        all(count == 1 for count in failure_counts.values())
        and len(failure_values) == len(expected_failures),
        f"{label} row WF-17 contains duplicate failure classes",
    )
    for failure_class, pattern in FAILURE_CLASSES.items():
        check(
            re.search(pattern, rows.get("WF-17", ""), re.IGNORECASE) is not None,
            f"{label} row WF-17 lacks canonical class {failure_class!r}",
        )


def check_bootstrap_templates() -> None:
    kit_root = ROOT / "agentic-bootstrap-kit"
    expected_kit_files = {
        "README.md",
        "CODEX_AGENTIC_BOOTSTRAP.md",
        "AGENTIC_FILE_TEMPLATES.md",
    }
    actual_kit_files = {
        path.relative_to(kit_root).as_posix()
        for path in kit_root.rglob("*")
        if path.is_file()
        and not IGNORED_PARTS.intersection(path.relative_to(kit_root).parts)
    }
    check(
        actual_kit_files == expected_kit_files,
        (
            "agentic-bootstrap-kit file set differs from the exact contract; "
            f"missing={sorted(expected_kit_files - actual_kit_files)}, "
            f"unexpected={sorted(actual_kit_files - expected_kit_files)}"
        ),
    )
    for legacy in ("AGENTIC_FILE_TEMPLATES.md", "CODEX_AGENTIC_BOOTSTRAP.md"):
        check(
            not (ROOT / legacy).exists(),
            f"legacy root-level bootstrap file must remain absent: {legacy}",
        )
    template_path = kit_root / "AGENTIC_FILE_TEMPLATES.md"
    records = extract_template_targets(template_path)
    target_counts = Counter(target for target, _, _, _ in records)
    duplicates = sorted(target for target, count in target_counts.items() if count != 1)
    check(
        not duplicates,
        f"bootstrap templates contain duplicate targets: {', '.join(duplicates)}",
    )

    expected_targets = (
        (set(PROVIDERS["codex"]["required"]) - {"README.md"}) | set(SHARED_DOCS)
    )
    actual_targets = set(target_counts)
    missing = sorted(expected_targets - actual_targets)
    unexpected = sorted(actual_targets - expected_targets)
    check(not missing, f"bootstrap templates omit Codex targets: {', '.join(missing)}")
    check(
        not unexpected,
        f"bootstrap templates contain unexpected targets: {', '.join(unexpected)}",
    )
    check(
        len(records) == len(expected_targets),
        (
            "bootstrap templates need exactly one body per expected target; "
            f"found {len(records)} for {len(expected_targets)} targets"
        ),
    )

    targets = {target: (info, body, line) for target, info, body, line in records}
    for target, (info, body, heading_line) in targets.items():
        expected_info = "toml" if target.endswith(".toml") else "markdown"
        check(
            info.lower() == expected_info,
            (
                f"{relative(template_path)}:{heading_line} target {target!r} "
                f"must use a {expected_info!r} fence"
            ),
        )
        if expected_info == "markdown":
            unclosed = unclosed_fence(body)
            check(
                unclosed is None,
                (
                    f"embedded target {target}:{unclosed[2]} has an unclosed "
                    f"{unclosed[0] * unclosed[1]} fence"
                    if unclosed is not None
                    else f"embedded target {target} has balanced fences"
                ),
            )
        else:
            expected_name = (
                Path(target).stem if target.startswith(".codex/agents/") else None
            )
            check_embedded_toml(f"embedded target {target}", body, expected_name)

    notice_target = "THIRD_PARTY_NOTICES.md"
    if notice_target in targets:
        check_notice_file(
            "embedded THIRD_PARTY_NOTICES.md",
            targets[notice_target][1],
        )

    skill_target = ".agents/skills/SKILL-TEMPLATE.md"
    if skill_target in targets:
        check_frontmatter_text(f"embedded target {skill_target}", targets[skill_target][1])

    agents_target = "AGENTS.md"
    if agents_target in targets:
        check_first_run_adaptation_contract(
            "embedded AGENTS.md",
            targets[agents_target][1],
        )

    plan_target = "docs/implementation-plans/IP-TEMPLATE.md"
    if plan_target in targets:
        plan_template = targets[plan_target][1]
        for mechanism, pattern in MECHANISMS.items():
            check(
                re.search(pattern, plan_template, re.DOTALL | re.IGNORECASE) is not None,
                f"embedded implementation-plan template does not represent {mechanism}",
            )
        check_plan_defaults("embedded implementation-plan template", plan_template)
        check_fingerprint_contract(
            "embedded implementation-plan template",
            plan_template,
        )
        for plan_contract, pattern in (
            (
                "workflow contract version",
                rf"Workflow contract version:\s*{re.escape(WORKFLOW_CONTRACT_VERSION)}",
            ),
            ("task-packet revision", r"Task-packet revision:\s*1"),
            (
                "contract migration rule",
                r"contract changes.{0,180}In Progress.{0,220}"
                r"(?:review|explicitly accepted)",
            ),
            (
                "sensitive-hash read minimization",
                r"do not.{0,80}read.{0,80}sensitive.{0,80}solely.{0,80}"
                r"(?:calculate|compute).{0,40}(?:a )?hash",
            ),
        ):
            check(
                re.search(pattern, plan_template, re.DOTALL | re.IGNORECASE)
                is not None,
                f"embedded implementation-plan template lacks {plan_contract}",
            )

    agents_readme_target = ".codex/agents/README.md"
    if agents_readme_target in targets:
        embedded_authority = targets[agents_readme_target][1]
        check_activation_prompts(
            "embedded .codex/agents/README.md",
            embedded_authority,
        )
        check(
            f"Workflow contract version: {WORKFLOW_CONTRACT_VERSION}"
            in embedded_authority,
            (
                "embedded .codex/agents/README.md must declare workflow contract "
                f"version {WORKFLOW_CONTRACT_VERSION}"
            ),
        )
        for authority_contract, pattern in (
            ("pre-plan write ownership", r"pre-plan lease"),
            (
                "blocked-plan status",
                r"temporarily blocked.{0,160}In Progress.{0,180}unblock\s+condition",
            ),
            (
                "category-specific failure responses",
                r"category-specific response.{0,180}Failure class.{0,120}Default response",
            ),
        ):
            check(
                re.search(
                    pattern,
                    embedded_authority,
                    re.DOTALL | re.IGNORECASE,
                )
                is not None,
                f"embedded .codex/agents/README.md lacks {authority_contract}",
            )
        check_untrusted_content_contract(
            "embedded .codex/agents/README.md",
            embedded_authority,
        )
        check_external_tool_data_contract(
            "embedded .codex/agents/README.md",
            embedded_authority,
        )
        check_exact_failure_classes(
            "embedded .codex/agents/README.md failure matrix",
            embedded_authority,
        )

    session_target = ".codex/session-notes.md"
    if session_target in targets:
        session = targets[session_target][1]
        check(
            f"Workflow contract version: {WORKFLOW_CONTRACT_VERSION}" in session,
            "embedded session state lacks workflow contract version",
        )
        check(
            re.search(r"Task-packet (?:revision|version):", session) is not None,
            "embedded session state lacks task-packet revision",
        )

    for role, contracts in {
        "architect": {
            "pre-plan write ownership": r"pre-plan lease",
            "read-only contributor": r"read-only evidence contributor",
        },
        "tester": {
            "isolated parallel validation": (
                r"parallel.{0,160}share.{0,120}(?:output|cache).{0,180}isolated"
            ),
            "artifact reporting": (
                r"(?:transient|generated)\s+artifacts?.{0,120}report|"
                r"report.{0,120}(?:transient|generated)\s+artifacts?"
            ),
        },
    }.items():
        target = f".codex/agents/{role}.toml"
        if target not in targets:
            continue
        role_text = targets[target][1]
        for contract, pattern in contracts.items():
            check(
                re.search(pattern, role_text, re.DOTALL | re.IGNORECASE)
                is not None,
                f"embedded {target} lacks {contract}",
            )

    check_bootstrap_role_contracts(
        "embedded bootstrap",
        {
            role: targets[f".codex/agents/{role}.toml"][1]
            for role in EXPECTED_ROLES
            if f".codex/agents/{role}.toml" in targets
        },
    )

    embedded_core = "\n".join(
        targets[target][1]
        for target in ("AGENTS.md", ".codex/README.md", ".codex/agents/README.md")
        if target in targets
    )
    for mechanism, pattern in MECHANISMS.items():
        check(
            re.search(pattern, embedded_core, re.DOTALL | re.IGNORECASE) is not None,
            f"embedded core instructions do not cover {mechanism}",
        )
    for contract, pattern in {**RETRY_CONTRACT_PATTERNS, **LEASE_CONTRACT_PATTERNS}.items():
        check(
            re.search(pattern, embedded_core, re.DOTALL | re.IGNORECASE) is not None,
            f"embedded core instructions lack {contract}",
        )
    check_fingerprint_contract("embedded core instructions", embedded_core)
    check_untrusted_content_contract("embedded core instructions", embedded_core)
    check_external_tool_data_contract("embedded core instructions", embedded_core)
    check_core_default_contract("embedded core instructions", embedded_core)
    for contract, pattern in (
        (
            "omitted-only defaults",
            r"(?:default|defaults).{0,80}omitted",
        ),
        (
            "invalid-control clarification",
            r"invalid explicit.{0,160}(?:surface|clarif)|"
            r"(?:surface|clarif).{0,160}invalid explicit",
        ),
        (
            "unsupported-control fallback",
            r"unsupported.{0,180}(?:safe )?fallback",
        ),
    ):
        check(
            re.search(pattern, embedded_core, re.DOTALL | re.IGNORECASE) is not None,
            f"embedded core instructions lack {contract}",
        )

    conformance_target = ".codex/workflow-conformance.md"
    if conformance_target in targets:
        check_embedded_conformance(
            "embedded conformance suite",
            targets[conformance_target][1],
        )

    metrics_target = ".codex/workflow-metrics.md"
    if metrics_target in targets:
        check_metrics_policy(
            "embedded workflow metrics policy",
            targets[metrics_target][1],
        )

    for role in ("orchestrator", "architect", "coder", "tester", "reviewer"):
        memory_target = f".codex/agents/memory/{role}.md"
        if memory_target not in targets:
            continue
        memory = targets[memory_target][1].lower()
        for term in ("source", "last confirmed", "invalidation"):
            check(
                term in memory,
                f"embedded {memory_target} lacks {term!r} provenance",
            )

    embedded_text = "\n\n".join(body for _, _, body, _ in records)
    for obsolete in OBSOLETE_CONTROLS:
        check(
            obsolete not in embedded_text,
            f"bootstrap embedded templates retain obsolete control spelling: {obsolete}",
        )
    check_privacy_contradictions("bootstrap embedded templates", embedded_text)
    check_contract_polarity("bootstrap embedded templates", embedded_text)
    check_safety_invariants("bootstrap embedded templates", embedded_text)
    check(
        re.search(
            r"security-sensitive.{0,180}unless the user explicitly scopes.{0,180}lower risk",
            embedded_text,
            re.DOTALL | re.IGNORECASE,
        )
        is None,
        "bootstrap embedded templates permit preference-based security-risk downgrade",
    )

    bootstrap_readme = read_text(kit_root / "README.md")
    bootstrap_spec = read_text(kit_root / "CODEX_AGENTIC_BOOTSTRAP.md")
    check_activation_prompts("bootstrap README", bootstrap_readme)
    check_activation_prompts("bootstrap specification", bootstrap_spec)
    for document_label, document in (
        ("bootstrap README", bootstrap_readme),
        ("bootstrap specification", bootstrap_spec),
    ):
        check(
            f"Workflow contract version: {WORKFLOW_CONTRACT_VERSION}" in document,
            (
                f"{document_label} must declare workflow contract version "
                f"{WORKFLOW_CONTRACT_VERSION}"
            ),
        )
        for mechanism, pattern in MECHANISMS.items():
            check(
                re.search(pattern, document, re.DOTALL | re.IGNORECASE) is not None,
                f"{document_label} does not cover {mechanism}",
            )
        for obsolete in OBSOLETE_CONTROLS:
            check(
                obsolete not in document,
                f"{document_label} retains obsolete control spelling: {obsolete}",
            )
        check_privacy_contradictions(document_label, document)
        check_contract_polarity(document_label, document)
        check_safety_invariants(document_label, document)
        check_untrusted_content_contract(document_label, document)
        check_external_tool_data_contract(document_label, document)
        check_first_run_adaptation_contract(document_label, document)
        check(
            "--bootstrap-target" in document,
            f"{document_label} lacks the target-scoped validator command",
        )
        for notice_contract, pattern in LICENSE_NOTICE_CONTRACT_PATTERNS.items():
            check(
                re.search(pattern, document, re.DOTALL | re.IGNORECASE) is not None,
                f"{document_label} lacks {notice_contract}",
            )
    for verification_contract, pattern in (
        ("exact target-tree audit", r"Compare the resulting tree.{0,100}exact target list"),
        ("TOML validation", r"Parse every generated TOML"),
        ("Markdown validation", r"Markdown fences, tables, and local links"),
        ("scope audit", r"no product code, build file, or unlisted path changed"),
        ("merge preservation", r"merge.{0,120}existing content was preserved"),
        (
            "target-scoped validator and fallback",
            r"validate_workflows\.py.{0,240}--bootstrap-target.{0,420}"
            r"Otherwise.{0,180}target-scoped checks",
        ),
    ):
        check(
            re.search(
                pattern,
                bootstrap_spec,
                re.DOTALL | re.IGNORECASE,
            )
            is not None,
            f"bootstrap specification lacks post-bootstrap {verification_contract}",
        )


def bootstrap_target_names() -> set[str]:
    """Return the exact workflow files generated or merged by the Codex bootstrap."""
    return (
        (set(PROVIDERS["codex"]["required"]) - {"README.md"})
        | set(SHARED_DOCS)
    )


def check_bootstrap_target(target_root: Path) -> list[Path]:
    """Validate a materialized Codex bootstrap inside an arbitrary project root."""
    global ROOT
    original_root = ROOT
    target_root = target_root.resolve()
    ROOT = target_root
    try:
        check(target_root.is_dir(), f"bootstrap target is not a directory: {target_root}")
        if not target_root.is_dir():
            return []

        expected = bootstrap_target_names()
        missing = sorted(
            item for item in expected if not (target_root / item).is_file()
        )
        check(
            not missing,
            f"bootstrap target omits required workflow files: {', '.join(missing)}",
        )
        files = sorted(
            target_root / item
            for item in expected
            if (target_root / item).is_file()
        )
        check_text_hygiene(files)
        check_fences(files)
        check_markdown_tables(files)
        check_local_links(files)
        if missing:
            return files

        check_notice_file(
            "bootstrap target THIRD_PARTY_NOTICES.md",
            read_text(target_root / "THIRD_PARTY_NOTICES.md"),
        )
        check_codex_toml_root(
            target_root,
            "bootstrap target",
            strict_config_shape=False,
            strict_role_shape=False,
        )

        skill_path = target_root / ".agents/skills/SKILL-TEMPLATE.md"
        skill_fields = parse_frontmatter_fields(
            relative(skill_path),
            read_text(skill_path),
        )
        if skill_fields is not None:
            check_exact_frontmatter_keys(
                relative(skill_path),
                skill_fields,
                {"name", "description"},
            )
            for field in ("name", "description"):
                check(
                    bool(skill_fields.get(field)),
                    f"{relative(skill_path)} frontmatter needs a non-empty {field}",
                )

        authority_path = target_root / ".codex/agents/README.md"
        authority = read_text(authority_path)
        agents_text = read_text(target_root / "AGENTS.md")
        agents_policy = target_agents_policy_text(
            "bootstrap target AGENTS.md",
            agents_text,
        )
        agents_strict_contradiction_sections = "\n\n".join(
            section
            for heading in TARGET_AGENTS_POLICY_HEADINGS
            if heading != "Risk And Security"
            for section in markdown_h2_sections(agents_text, re.escape(heading))
        )
        agents_contradictions = target_agents_contradiction_text(agents_text)
        check_activation_prompts("bootstrap target authority", authority)
        check(
            f"Workflow contract version: {WORKFLOW_CONTRACT_VERSION}" in authority,
            "bootstrap target authority lacks the workflow contract version",
        )
        check_provider_entrypoints(
            "bootstrap target",
            target_root,
            {"AGENTS.md": ".codex/agents/README.md"},
            {"AGENTS.md": agents_policy},
            {"AGENTS.md": agents_contradictions},
        )
        check_provider_roles("codex", target_root)
        check_exact_failure_classes(
            "bootstrap target authoritative failure matrix",
            authority,
        )

        core = "\n".join(
            (
                agents_policy,
                read_text(target_root / ".codex/README.md"),
                authority,
            )
        )
        core_contradictions = "\n".join(
            (
                agents_contradictions,
                read_text(target_root / ".codex/README.md"),
                authority,
            )
        )
        core_default_text = "\n".join(
            (
                agents_strict_contradiction_sections,
                read_text(target_root / ".codex/README.md"),
                authority,
            )
        )
        core_lower = core.lower()
        for mechanism, pattern in MECHANISMS.items():
            check(
                re.search(pattern, core, re.DOTALL | re.IGNORECASE) is not None,
                f"bootstrap target core instructions do not cover {mechanism}",
            )
        for invariant in (
            "approve",
            "sequential",
            "parallel",
            "security",
            "not measured",
            "25%",
            "pre-plan lease",
        ):
            check(
                invariant in core_lower,
                f"bootstrap target core instructions lack invariant {invariant!r}",
            )
        for contract, pattern in {
            **RETRY_CONTRACT_PATTERNS,
            **LEASE_CONTRACT_PATTERNS,
        }.items():
            check(
                re.search(pattern, core, re.DOTALL | re.IGNORECASE) is not None,
                f"bootstrap target core instructions lack {contract}",
            )
        check_fingerprint_contract("bootstrap target core instructions", core)
        check_untrusted_content_contract(
            "bootstrap target core instructions",
            core,
            contradiction_text=core_contradictions,
        )
        check_external_tool_data_contract(
            "bootstrap target core instructions",
            core,
            contradiction_text=core_contradictions,
        )
        check_first_run_adaptation_contract(
            "bootstrap target AGENTS.md",
            agents_text,
        )
        check_core_default_contract(
            "bootstrap target core instructions",
            core_default_text,
        )

        plan = read_text(
            target_root / "docs/implementation-plans/IP-TEMPLATE.md"
        )
        for mechanism, pattern in MECHANISMS.items():
            check(
                re.search(pattern, plan, re.DOTALL | re.IGNORECASE) is not None,
                f"bootstrap target plan template does not represent {mechanism}",
            )
        check_plan_defaults("bootstrap target plan template", plan)
        check_fingerprint_contract("bootstrap target plan template", plan)
        for contract, pattern in (
            (
                "workflow contract version",
                rf"Workflow contract version:\s*{re.escape(WORKFLOW_CONTRACT_VERSION)}",
            ),
            ("task-packet revision", r"Task-packet revision:\s*1"),
            (
                "contract migration",
                r"contract changes.{0,180}In Progress.{0,220}"
                r"(?:review|explicitly accepted)",
            ),
            (
                "sensitive-hash read minimization",
                r"do not.{0,80}read.{0,80}sensitive.{0,80}solely.{0,80}"
                r"(?:calculate|compute).{0,40}(?:a )?hash",
            ),
        ):
            check(
                re.search(pattern, plan, re.DOTALL | re.IGNORECASE) is not None,
                f"bootstrap target plan template lacks {contract}",
            )

        check_embedded_conformance(
            "bootstrap target conformance suite",
            read_text(target_root / ".codex/workflow-conformance.md"),
        )
        check_metrics_policy(
            "bootstrap target workflow metrics policy",
            read_text(target_root / ".codex/workflow-metrics.md"),
        )

        session = read_text(target_root / ".codex/session-notes.md")
        for contract, pattern in (
            (
                "workflow contract version",
                rf"Workflow contract version:\s*{re.escape(WORKFLOW_CONTRACT_VERSION)}",
            ),
            ("task-packet revision", r"Task-packet (?:revision|version):"),
            ("active plan status", r"Active plan status:"),
            (
                "approval evidence reference",
                r"(?:Explicit )?Approval evidence reference:",
            ),
        ):
            check(
                re.search(pattern, session, re.IGNORECASE) is not None,
                f"bootstrap target session state lacks {contract}",
            )

        for role in sorted(EXPECTED_ROLES):
            memory_path = target_root / f".codex/agents/memory/{role}.md"
            memory = read_text(memory_path).lower()
            for term in ("source", "last confirmed", "invalidation"):
                check(
                    term in memory,
                    f"{relative(memory_path)} lacks {term!r} provenance",
                )

        target_policy_text = "\n\n".join(
            (
                agents_contradictions,
                read_text(target_root / ".codex/README.md"),
                authority,
                *[
                    read_text(target_root / f".codex/agents/{role}.toml")
                    for role in sorted(EXPECTED_ROLES)
                ],
                read_text(target_root / ".codex/workflow-metrics.md"),
                read_text(target_root / ".codex/workflow-conformance.md"),
            )
        )
        target_contradiction_text = "\n\n".join(
            (
                agents_contradictions,
                read_text(target_root / ".codex/README.md"),
                authority,
                *[
                    read_text(target_root / f".codex/agents/{role}.toml")
                    for role in sorted(EXPECTED_ROLES)
                ],
                read_text(target_root / ".codex/workflow-metrics.md"),
                read_text(target_root / ".codex/workflow-conformance.md"),
            )
        )
        for obsolete in OBSOLETE_CONTROLS:
            check(
                obsolete not in target_policy_text,
                f"bootstrap target retains obsolete control spelling: {obsolete}",
            )
        check_privacy_contradictions("bootstrap target", target_contradiction_text)
        check_contract_polarity("bootstrap target", target_contradiction_text)
        check_safety_invariants("bootstrap target", target_contradiction_text)
        return files
    finally:
        ROOT = original_root


def check_repository_metadata() -> None:
    root_readme = read_text(ROOT / "README.md")
    root_visible = markdown_contract_text(root_readme)
    check(
        sum(
            info.lower() == "mermaid"
            for info, _, _ in fenced_blocks(
                markdown_without_html_comments(root_readme)
            )
        )
        >= 4,
        "top-level README needs four Mermaid diagrams",
    )
    check_activation_prompts("top-level README", root_readme)
    check("Victor Alexander Daud" in root_readme, "top-level README must credit Victor Alexander Daud")
    check("VicXander" in root_readme, "top-level README must use VicXander casing")
    check("no telemetry" in root_readme.lower(), "top-level README lacks privacy assurance")
    check("22 resource-governance mechanisms" in root_readme, "top-level README lacks the 22-mechanism contract")
    check(
        f"Workflow contract version: {WORKFLOW_CONTRACT_VERSION}" in root_readme,
        (
            "top-level README must declare workflow contract version "
            f"{WORKFLOW_CONTRACT_VERSION}"
        ),
    )
    check(
        "Python 3.11 or newer" in root_readme,
        "top-level README must document the validator's Python 3.11+ requirement",
    )
    check(
        "flat-YAML" in root_readme,
        "top-level README must document the supported frontmatter subset",
    )
    check(
        "--bootstrap-target" in root_readme,
        "top-level README must document target-scoped bootstrap validation",
    )
    check_untrusted_content_contract("top-level README", root_readme)
    check_external_tool_data_contract("top-level README", root_readme)
    check_first_run_adaptation_contract("top-level README", root_readme)
    for notice_contract, pattern in LICENSE_NOTICE_CONTRACT_PATTERNS.items():
        check(
            re.search(pattern, root_readme, re.DOTALL | re.IGNORECASE) is not None,
            f"top-level README lacks {notice_contract}",
        )
    for suite in (
        "test_validate_workflows.py",
        "test_validate_security_contracts.py",
        "test_validate_structure_contracts.py",
    ):
        check(
            (ROOT / "tools" / suite).is_file(),
            f"documented validator unit suite tools/{suite} is missing",
        )
    check(
        re.search(
            r"python\s+-B\s+-m\s+unittest\s+discover\s+-s\s+tools\s+-p\s+"
            r"[\"']test_\*\.py[\"']",
            root_readme,
        )
        is not None,
        "top-level README must document discovery of every validator unit suite",
    )
    mechanism_section = (
        root_visible.split("The 22 resource-governance mechanisms are:", 1)[1].split(
            "\nDefaults:",
            1,
        )[0]
        if "The 22 resource-governance mechanisms are:" in root_visible
        and "\nDefaults:" in root_visible
        else ""
    )
    mechanism_ids = [
        int(value)
        for value in re.findall(r"^\|\s*([0-9]+)\s*\|", mechanism_section, re.MULTILINE)
    ]
    check(
        mechanism_ids == list(range(1, 23)),
        (
            "top-level README mechanism table must contain ordered IDs 1 through 22 "
            f"exactly once; found {mechanism_ids}"
        ),
    )
    rows = [
        (int(match.group(1)), match.group(2).strip(), match.group(3).strip())
        for match in re.finditer(
            r"^\|\s*([0-9]+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$",
            mechanism_section,
            re.MULTILINE,
        )
        if match.group(1).isdigit()
    ]
    check(
        len(rows) == len(ROOT_MECHANISM_ROWS),
        "top-level README mechanism table must have 22 parseable contract rows",
    )
    for index, (expected_name, contract_pattern) in enumerate(
        ROOT_MECHANISM_ROWS,
        start=1,
    ):
        row = next((item for item in rows if item[0] == index), None)
        check(row is not None, f"top-level README mechanism row {index} is missing")
        if row is None:
            continue
        check(
            row[1] == expected_name,
            (
                f"top-level README mechanism row {index} is named {row[1]!r}; "
                f"expected {expected_name!r}"
            ),
        )
        check(
            re.search(contract_pattern, row[2], re.DOTALL | re.IGNORECASE) is not None,
            f"top-level README mechanism row {index} has a non-canonical contract",
        )
    check_privacy_contradictions("top-level README", root_readme)
    check_contract_polarity("top-level README", root_readme)
    check_safety_invariants("top-level README", root_readme)
    for provider_label in ("Codex", "GitHub Copilot", "Claude Code"):
        check(
            f"- {provider_label} workflow: 32 files" in root_readme,
            f"top-level README has a stale {provider_label} file count",
        )

    citation = read_text(ROOT / "CITATION.cff")
    for pattern, label in (
        (r"^cff-version:\s*1\.2\.0\s*$", "cff-version"),
        (r'^title:\s*"VicXander Agentic Workflows"\s*$', "title"),
        (r'family-names:\s*"Daud"', "family name"),
        (r'given-names:\s*"Victor Alexander"', "given names"),
        (
            rf'^version:\s*"{re.escape(WORKFLOW_CONTRACT_VERSION)}"\s*$',
            "version",
        ),
        (r"^date-released:\s*2026-07-26\s*$", "release date"),
        (r"^license:\s*MIT\s*$", "license"),
    ):
        check(
            re.search(pattern, citation, re.MULTILINE) is not None,
            f"CITATION.cff lacks valid {label}",
        )
    check_mit_license("root LICENSE", read_text(ROOT / "LICENSE"))
    gitignore = read_text(ROOT / ".gitignore")
    for ignored in ("__pycache__/", "*.py[cod]"):
        check(ignored in gitignore, f".gitignore must exclude {ignored}")

    for path in ROOT.rglob("*"):
        if path.is_dir() and not IGNORED_PARTS.intersection(path.relative_to(ROOT).parts):
            check("-system" not in path.name.lower(), f"stale -system directory name: {relative(path)}")


def check_contract_coverage() -> None:
    """Require every recorded contract clause to remain present on its recorded surface.

    The coverage baseline pins which surface carries which named contract clause, so relocating or
    deduplicating contract prose cannot silently drop a clause. Deliberate removals are recorded by
    regenerating the baseline, which makes the baseline diff the reviewable evidence.
    """
    # Imported lazily: contract_coverage imports this module, and by the time this runs the module
    # is already initialised, so the lazy import avoids a circular import at load time.
    try:
        from tools import contract_coverage
    except ImportError:  # pragma: no cover - exercised by the direct-script path.
        import contract_coverage

    try:
        baseline = contract_coverage.load_baseline()
    except contract_coverage.BaselineError as exc:
        # Reported as an ordinary check failure: raising here would abort main() before the
        # accumulated report prints, hiding every other finding behind a traceback.
        check(False, f"{exc}; regenerate with 'python tools/contract_coverage.py --write'")
        return
    check(
        bool(baseline),
        "contract-clause coverage baseline is missing; "
        "run 'python tools/contract_coverage.py --write'",
    )
    if not baseline:
        return
    for _identifier, _surface, problem in contract_coverage.verify_pairs(baseline):
        check(problem is None, problem or "")


def main(argv: list[str] | None = None) -> int:
    global checks
    errors.clear()
    checks = 0
    parser = argparse.ArgumentParser(
        description="Validate VicXander agentic workflow contracts.",
    )
    parser.add_argument(
        "--bootstrap-target",
        type=Path,
        help=(
            "validate a materialized Codex bootstrap at this project root "
            "instead of validating the distribution repository"
        ),
    )
    arguments = parser.parse_args(argv)

    if arguments.bootstrap_target is not None:
        target = arguments.bootstrap_target.resolve()
        files = check_bootstrap_target(target)
        if errors:
            print(
                "Bootstrap target validation failed: "
                f"{len(errors)} issue(s) across {checks} checks."
            )
            for item in errors:
                print(f"- {item}")
            return 1
        print(
            "Bootstrap target validation passed: "
            f"{checks} checks across {len(files)} workflow files under {target}."
        )
        return 0

    files = repository_files()
    check_text_hygiene(files, require_lf=True)
    check_fences(files)
    check_markdown_tables(files)
    check_local_links(files)
    check_repository_metadata()
    for provider_name, provider_config in PROVIDERS.items():
        check_provider(provider_name, provider_config)
    check_codex_toml()
    check_frontmatter_files()
    check_bootstrap_templates()
    check_contract_coverage()

    if errors:
        print(f"Workflow validation failed: {len(errors)} issue(s) across {checks} checks.")
        for item in errors:
            print(f"- {item}")
        return 1
    print(f"Workflow validation passed: {checks} checks across {len(files)} repository files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
