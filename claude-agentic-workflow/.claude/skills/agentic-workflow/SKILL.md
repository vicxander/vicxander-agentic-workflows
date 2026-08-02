---
name: agentic-workflow
description: Runs the repository's adaptive Architect, Coder, Tester, and Reviewer workflow with approval gates for planned work. Use when the user asks for agentic mode, a multi-role implementation, or an explicitly approval-gated change.
argument-hint: "<task>"
---

# Agentic Workflow

Task:

$ARGUMENTS

Read `CLAUDE.md` and `.claude/AGENTIC-WORKFLOW.md`.

Act as the main-session Orchestrator:

1. Read user controls, using `Workflow depth: Auto`, `Specification mode: Native`, and
   `Efficiency profile: Balanced` when omitted. In explicit OpenSpec mode, read
   `OpenSpec change: <change-id|Auto>`, load `.claude/skills/vaw-openspec/SKILL.md`, and allow Auto
   only when exactly one active change resolves.
   Budget defaults are `Token budget: Auto` and `Validation/review/closeout reserve: 25%`. Runtime
   defaults are `Execution mode: Sequential`, `Max parallel subagents: 4`, and
   `Max retries per node: 1`.
   Integration and metrics defaults are `Integration mode: Auto` and `Local metrics: Off`.
2. Perform one capability preflight, including available `Bash`/`PowerShell` shell execution and
   background task listing, steering, and stopping. Then read the latest compact checkpoint, active
   packet, evidence fingerprints, assumptions, decisions, relevant memory, and worktree state. Load
   context delta-first and recheck capabilities only after a material change or failure. Do not
   start parallel writer work when active workers cannot be steered and stopped safely.
3. Classify `Trivial`, `Small`, `Medium`, or `Large` work and select `Direct`, `Lite`, `Standard`,
   or `Full`. Risk may raise but never silently weaken route safety; efficiency settings never
   bypass approval or mandatory gates.
4. Protect the advisory validation/review/closeout reserve. When runtime token usage is unavailable,
   report `Not measured` and use profile heuristics rather than inventing usage.
5. Apply the spawn-value gate before every delegation. Use no worker whose independence, latency,
   isolation, or specialist value does not exceed handoff and reconciliation cost.
6. For a planned route, have `architect` or an explicit Architect role transition produce the plan;
   `Direct` is limited to localized, reversible, Low-risk work with clear criteria.
7. Present the `Proposed` plan, ask the user to choose Approve, Revise, or Stop, and end the current
   turn without implementation while approval is pending. Record approval against the current plan
   revision; a material revision resets the plan to `Proposed`, while the same revision may continue
   as `In Progress`.
   In OpenSpec mode, approval also binds the change ID, schema/profile, artifact paths, and
   deterministic fingerprint or per-file hashes; material drift invalidates approval/evidence and
   returns the plan to `Proposed`.
8. After explicit approval, schedule only ready dependency nodes. Enforce exclusive write leases;
   for `Single integrator`, only the designated Coder writes while other Coders remain read-only.
9. In `Parallel`, run only valuable independent work inside one active stage as bounded background
   subagents. Respect global and role ceilings, background constraints, and non-overlapping
   ownership; wait for and reconcile every result.
10. Give each role compact references to plan, node, criteria, evidence, assumption, decision, and
    finding IDs. Do not copy full plans, source, conversation history, or logs.
11. Fingerprint evidence, build the change-impact test map, execute progressive validation, trace
    every criterion, assign stable Reviewer finding IDs, and deduplicate without losing distinct
    evidence.
12. On changed inputs or upstream decisions, mark dependent evidence stale and cancel obsolete
    queued work. Retain or quarantine each active writer's lease until safe stop/finish and
    last-write reconciliation, then release or reassign it; never integrate stale results.
    Replan/reapprove material drift.
13. Classify failures, enforce the profile/user retry limit as a hard ceiling, and stop the node
    when exhaustion, repeated failure without new evidence, or Coder/Tester cycling opens the
    circuit. A new hypothesis alone does not reset the allowance; another attempt requires either
    a user-raised ceiling or an approved plan revision that creates and budgets a materially new
    node.
14. Request adjudication only for material conflict, Low confidence, elevated risk, or required
    independent verification. Never omit mandatory security coverage.
15. Compact state at every stage boundary. End optional investigation when criteria and mandatory
    gates are complete, no material issue remains, and confidence is `High`.
16. Close out with settings, capability limitations, reserve, impact selection, fingerprints,
    retries, cancellations, findings, validation, confidence, and residual risk. Update local
    metadata only when `Local metrics: On`, and memory only with provenance and freshness.

OpenSpec explore/propose/update are Architect-only and planning-only; apply is Coder-only under a
named `In Progress` plan plus valid lease; verify supplements but never replaces Tester/Reviewer;
sync and archive are Orchestrator-only after all applicable gates. Missing setup is
`Missing dependency/tooling`; never install or initialize automatically. In Native mode, do not
scan for or invoke OpenSpec or Node.js.

Do not treat invoking this skill as approval of an implementation plan. Do not cross the approval
gate in a non-interactive run. If parallel execution is unavailable, report the fallback and
continue sequentially. Metrics are optional and local; never record prompts, source content,
secrets, personal data, or raw logs, and use `Not measured` for unavailable values. Keep
`model: inherit`, do not hardcode a model ID or effort, and never override user/session settings.

Use generic, minimal, non-sensitive inputs with external tools. Never send secrets, credentials,
access tokens, or private keys. Do not disclose proprietary source or repository content, customer
or personal data, private URLs, or sensitive identifiers through web searches, fetched URLs,
connector or MCP calls, remote APIs, or other third-party tool inputs without explicit user
authorization for that specific disclosure. Task approval or a research request is not disclosure
authorization; prefer local, redacted, or synthetic alternatives and ask first.
