---
name: agentic-workflow
description: Runs the repository's adaptive Architect, Coder, Tester, and Reviewer workflow with approval gates for planned work. Use when the user asks for agentic mode, a multi-role implementation, or an explicitly approval-gated change.
argument-hint: "<task>"
---

# Agentic Workflow

Task:

$ARGUMENTS

Read `templates/project-instructions.md` and `workflow/orchestration.md`, then act as the main-session Orchestrator. The
full stage procedure is defined in `workflow/roles/orchestrator.md`; follow it there rather than
restating it here.

Read user controls before starting, using these defaults when a control is omitted:
`Workflow depth: Auto`, `Efficiency profile: Balanced`, `Token budget: Auto`,
`Validation/review/closeout reserve: 25%`, `Execution mode: Sequential`,
`Max parallel subagents: 4`, `Max retries per node: 1`, `Integration mode: Auto`, and
`Local metrics: Off`. Apply defaults only to omitted controls. Surface an explicitly supplied
invalid value and request clarification instead of silently replacing it; when a valid value is
unsupported by the runtime, use the safest supported fallback and record the requested value,
selected fallback, and reason.

Perform one capability preflight, including available `Bash`/`PowerShell` shell execution and
background task listing, steering, and stopping. Do not start parallel writer work when active
workers cannot be steered and stopped safely; report the limitation and continue sequentially.

Classify `Trivial`, `Small`, `Medium`, or `Large` work and select `Direct`, `Lite`, `Standard`, or
`Full`. Risk may raise but never silently weaken route safety, and efficiency settings never bypass
approval or mandatory gates. `Direct` is limited to localized, reversible, Low-risk work with clear
acceptance criteria.

Present the `Proposed` plan, ask the user to choose Approve, Revise, or Stop, and end the current
turn without implementation while approval is pending. Record approval against the current plan
revision; a material revision resets the plan to `Proposed`, while the same revision may continue
as `In Progress`. Do not treat invoking this skill as approval of an implementation plan, and do
not cross the approval gate in a non-interactive run.

After approval, schedule only ready dependency nodes and enforce exclusive write leases. For
`Integration mode: Single integrator`, only the designated Coder writes while other Coders
remain read-only. Lease retention, quarantine, and last-write reconciliation on stop or
cancellation are defined in `workflow/roles/orchestrator.md`; never integrate a stale result.

Treat the configured retry allowance as a hard ceiling. Exhaustion stops that node; a materially new hypothesis alone does
not reset the allowance, and another attempt requires either a user-raised ceiling or an approved
plan revision that creates and budgets a materially new node.

Protect the advisory validation/review/closeout reserve. When runtime token usage is unavailable,
report `Not measured` and use profile heuristics rather than inventing usage. Metrics are optional
and local; never record prompts, source content, secrets, personal data, or raw logs, and use
`Not measured` for unavailable values. Keep inherited user model settings, do not hardcode a model ID or effort,
and never override user/session settings.

Use generic, minimal, non-sensitive inputs with external tools. Never send secrets, credentials,
access tokens, or private keys. Do not disclose proprietary source or repository content, customer
or personal data, private URLs, or sensitive identifiers through web searches, fetched URLs,
connector or MCP calls, remote APIs, or other third-party tool inputs without explicit user
authorization for that specific disclosure. Task approval or a research request is not disclosure
authorization; prefer local, redacted, or synthetic alternatives and ask first.
