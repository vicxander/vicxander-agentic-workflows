# Agent Memory

This directory is lightweight repository-managed continuity for the GitHub Copilot agentic workflow.
It is not automatically maintained by GitHub Copilot; the workflow instructs agents to update it
only when useful.

- `session-notes.md`: shared current state, active plan, blockers, and cross-role decisions
- `worklog.md`: concise completed events
- `todo.md`: short-lived operational tasks
- `<role>.md`: durable, provenance-bearing role-specific lessons
- `workflow-metrics.md`: optional metadata-only workflow measurements; never prompts or source
  content

Do not store secrets, sensitive raw findings, full logs, duplicated plans, or transient chat
history. Workflow metrics remain project-scoped, user-visible Markdown. These instructions define
no uploader, automatic export, or author-operated collection service; ordinary provider/tool
processing remains governed by the user's settings and applicable policies. Code, tests,
requirements, and approved plans outrank memory.

## Freshness And Provenance

Every durable memory entry should use this compact shape:

```text
- ID:
  Fact or lesson:
  Source:
  Applicable revision or scope:
  Owner:
  Last confirmed:
  Expiry or invalidation condition:
```

An entry without a trustworthy source, matching scope, and current confirmation is an unverified
hypothesis. Reconfirm it delta-first from authoritative files before relying on it. Do not refresh
an entry merely to keep it alive; update it only when new evidence confirms or changes the durable
lesson.

Orchestrator is the sole durable-memory writer. Other roles return provenance-bearing candidates.
Orchestrator waits for all active same-role workers to stop, reconciles the candidates, and holds
the target path's exclusive write lease before changing a durable memory file.

Session checkpoints are compact coordination state, not durable truth. They may reference the
task-packet version, repository revision, completed and ready nodes, active leases, criterion
status, fresh evidence IDs, decisions, material assumptions, blockers, budget state, confidence,
and next action. Do not paste plans, source files, prompts, or full logs into a checkpoint.

Outcome calibration may compare compatible metadata-only metric entries to identify over-routing,
avoidable scans, low-value workers, retries, or review rework. It may propose a workflow change,
but it must never automatically weaken safety gates, override user preferences, or extrapolate from
an inadequate sample. Check changes against `.github/WORKFLOW-CONFORMANCE.md`.
