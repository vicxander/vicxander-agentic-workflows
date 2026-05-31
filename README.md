# Agentic Mode Setup Guide

This folder contains project-agnostic instructions for bootstrapping a "true agentic" Codex
workflow in a new repository.

The goal is to avoid re-prompting the same setup details every time a new project starts. Copy or
reference these files from a new repository, then ask Codex to initialize agentic mode from them.

## Recommended Use

In a new project, give Codex this prompt:

```text
Read docs/agentic-mode/CODEX_AGENTIC_BOOTSTRAP.md and initialize true agentic mode for this project.
Create only the agentic coordination, agent instruction, and documentation-lane files. Do not
implement product code.
```

For an existing project, choose a bootstrap mode:

- `create`: create the agentic structure in a project that does not already have one.
- `merge`: preserve existing guidance and carefully merge missing agentic files or sections.
- `dry-run`: report what would be created or changed before editing files.

Example with an explicit mode:

```text
Read docs/agentic-mode/CODEX_AGENTIC_BOOTSTRAP.md and initialize true agentic mode for this project.
Bootstrap mode: merge. Do not implement product code.
```

If this folder is not already in the new project, copy these files first:

```text
docs/agentic-mode/README.md
docs/agentic-mode/CODEX_AGENTIC_BOOTSTRAP.md
docs/agentic-mode/AGENTIC_FILE_TEMPLATES.md
```

## What "True Agentic" Means

This setup uses a hybrid memory model:

- Shared project memory records current state, user decisions, active plans, and blockers.
- Role-specific memory records durable lessons that only one agent role needs.
- The Orchestrator controls the workflow and prevents memory drift.
- Architect creates a plan before implementation.
- The user must choose Approve, Revise, or Stop after Architect finishes the plan.
- Coder implements only after approval.
- Tester validates with explicit commands and blocked-gate reporting.
- Reviewer checks for bugs, regressions, missing tests, and plan drift.
- Runtime-backed reasoning policy is used when available, while explicit user-selected higher
  reasoning levels are preserved.

## Sample Prompts

Use this prompt for a normal agentic task:

```text
Use .codex/agents in agentic mode. Orchestrator coordinates Architect, Coder, Tester, and Reviewer.
Apply the reasoning policy from .codex/agents/README.md. Architect must create the implementation
plan first and wait for my approval before coding. Task: <task>
```

Use this prompt when add-on skills should be enforced:

```text
Use .codex/agents in agentic mode and apply relevant skills from .codex/addon-agent-skills/.
Architect must include applicable skills in the plan. Coder and Tester must satisfy or report
blockers for those skills. Task: <task>
```

Use this prompt when the task is based on requirements or user findings:

```text
Use .codex/agents in agentic mode. Read relevant files under docs/requirements/ and
docs/user-findings/ before planning. Treat user findings as evidence, not automatic root cause.
Architect must create the implementation plan first and wait for my approval. Task: <task>
```

Use this prompt when you want maximum rigor for the entire workflow:

```text
Use .codex/agents in agentic mode. Keep the whole workflow at my current reasoning level; do not
downgrade any role. Architect creates the plan first and waits for my approval. Task: <task>
```

## Generated Structure

The bootstrap creates or carefully merges this structure:

```text
AGENTS.md
docs/
  implementation-plans/
    INDEX.md
    README.md
    IP-TEMPLATE.md
  requirements/
    INDEX.md
    README.md
    REQ-TEMPLATE.md
  user-findings/
    INDEX.md
    README.md
    UF-TEMPLATE.md
.codex/
  README.md
  session-notes.md
  worklog.md
  todo.md
  addon-agent-skills/
    README.md
    SKILL-TEMPLATE.md
  agents/
    README.md
    ORCHESTRATOR.md
    ARCHITECT.md
    CODER.md
    TESTER.md
    REVIEWER.md
    memory/
      orchestrator.md
      architect.md
      coder.md
      tester.md
      reviewer.md
```

## `AGENTS.md` And `.codex/`

Use both files, but keep their responsibilities separate:

- `AGENTS.md` is durable project-wide guidance for future agents.
- `.codex/` is operational workflow, session continuity, worklog, todos, and role memory.

For a brand-new project, `AGENTS.md` should start as a conservative skeleton. It should not invent
architecture, commands, or quality gates before the codebase exists. After implementation creates
stable structure and commands, update `AGENTS.md` with those durable facts.

At task closeout, Orchestrator should check whether `AGENTS.md` needs an update. Update it only
when a durable project-wide convention, command, structure, quality gate, or instruction changed.
Do not use `AGENTS.md` for task history, temporary blockers, active plans, one-off bugs, or logs.

## Documentation Lanes

The bootstrap creates or carefully merges these documentation lanes:

- `docs/requirements/`: user-authored or user-approved requirements, acceptance criteria, product
  intent, and behavior expectations.
- `docs/implementation-plans/`: Architect-generated implementation plans. Coder implements from
  approved plans, and Reviewer checks drift against them.
- `docs/user-findings/`: user-provided evidence from testing or external systems, such as TeamCity
  logs, screenshots, QA notes, crash traces, recordings, or bug reports.

These lanes keep intent, plan, and evidence separate:

```text
requirements -> implementation plan -> implementation -> validation -> user findings -> next cycle
```

Treat `docs/user-findings/` as evidence to inspect, not as automatic root cause. Findings may be
stale, environment-specific, or incomplete, but relevant findings must be considered when planning,
testing, and reviewing.

Do not store secrets in documentation lanes. Before committing or sharing user findings, redact
tokens, credentials, private URLs, personal emails, device identifiers, customer data, and any other
sensitive information.

If raw findings contain sensitive data, keep the raw file untracked or outside the repository when
needed. Commit only a redacted finding or summary that preserves enough evidence for agents to work.

## Requirements Lifecycle

Requirements should use explicit status labels:

- `Draft`: captured but not approved.
- `Approved`: user-approved and ready to plan from.
- `Implemented`: implemented and validated.
- `Superseded`: replaced by a newer requirement or user decision.
- `Rejected`: intentionally not pursued.

Architect should plan from approved requirements when possible. If the user asks to implement from a
draft requirement, Orchestrator should surface that status before planning.

## Implementation Plan Lifecycle

Implementation plans should use explicit status labels:

- `Proposed`: Architect drafted the plan, but the user has not approved it.
- `Approved`: the user approved the plan and Coder may implement it.
- `In Progress`: implementation has started.
- `Done`: implementation and expected validation are complete.
- `Superseded`: a newer plan or user decision replaced it.
- `Abandoned`: the plan was stopped and should not be implemented.

Do not infer that the newest implementation plan is active. The active plan must be named by the
user, `.codex/session-notes.md`, or an explicit Orchestrator handoff.

## Risk Level Policy

Architect should assign every non-trivial plan a risk level:

- `Low`: localized, reversible, low blast radius.
- `Medium`: touches shared behavior, cross-module contracts, important UX, or non-trivial data
  flow.
- `High`: touches data deletion, migrations, auth, payments, secrets, encryption, permissions,
  networking, deployment, external integrations, or other high-impact behavior.

Risk level should drive validation depth. Low-risk work may use focused checks. Medium-risk work
should use targeted checks plus relevant broader gates. High-risk work should include broader
validation, explicit Reviewer focus, and rollback or recovery notes.

## Definition Of Done

Definition of Done should scale with risk:

- `Low`: scoped implementation completed, focused validation run, changed files reported.
- `Medium`: low-risk criteria plus relevant broader gates, plan status updated, unresolved findings
  documented.
- `High`: medium-risk criteria plus rollback or recovery notes, security-focused review when
  applicable, broader validation, and explicit residual-risk notes.

Blocked validation must be reported as blocked, not passed.

## Rollback And Recovery

For high-risk plans, Architect must include rollback or recovery notes. This is required for
migrations, data deletion, auth, payments, deployment, external integrations, security-sensitive
changes, or changes that could block users from core workflows.

## Naming Conventions

Use stable, sortable IDs:

- Requirements: `REQ-0001-short-title.md`
- Implementation plans: `IP-0001-short-title.md`
- User findings: `UF-0001-short-title.md`
- Add-on skills: `lowercase-kebab-skill.md`

Keep IDs stable after creation. If a requirement, plan, or finding is superseded, update its status
or notes instead of renaming it casually.

## Documentation Indexes

Each documentation lane may keep an index:

- `docs/requirements/INDEX.md`
- `docs/implementation-plans/INDEX.md`
- `docs/user-findings/INDEX.md`

Indexes are for navigation only. They should summarize ID, title, status, and latest note without
duplicating full content.

## Archive And Retention

Old docs should stay useful instead of becoming noise:

- Mark completed implementation plans as `Done`.
- Mark replaced plans as `Superseded`.
- Mark stopped plans as `Abandoned`.
- Mark user findings as `Open`, `Resolved`, `Stale`, or `Superseded`.
- Keep large raw logs as files, but summarize durable conclusions in the relevant finding or
  session notes only when useful.

## Security-Sensitive Work

If a task touches auth, secrets, permissions, payments, encryption, user data, networking,
deployment, external integrations, or dependency supply chain, Orchestrator should require a
security-focused review. If a relevant add-on security skill exists, it must be applied.

Security-sensitive plans should be treated as at least `High` risk unless the user explicitly scopes
them down and the codebase context supports that lower risk.

## Conflict Handling

Use this conflict model:

- The user's current request wins over older documentation.
- Code and tests describe current behavior.
- `docs/requirements/` describes desired behavior and user intent.
- `docs/implementation-plans/` describes approved or proposed execution.
- `docs/user-findings/` is evidence to inspect, not automatic root cause.
- Add-on skills are requirements only when relevant and not in conflict with explicit user
  instruction.
- When documents conflict, Orchestrator should surface the conflict before implementation.

## Version Control Safety

When the project uses version control:

- Check worktree state before implementation.
- Preserve unrelated user changes.
- Do not commit unless the user explicitly asks.
- Do not run destructive version-control commands unless the user explicitly approves.
- Report changed files at closeout.

## Dependency And Tooling Changes

Agents should not add new dependencies, services, build tools, CI changes, paid services, networked
infrastructure, or external integrations unless the approved plan explicitly includes them and the
user approves that scope.

## External Research

When external research is needed, prefer primary sources such as official documentation, standards,
source repositories, release notes, vendor docs, or original issue trackers. Summarize and cite
sources when relevant. Do not rely on secondary summaries when a primary source is available.

## Add-On Agent Skills

The bootstrap also creates `.codex/addon-agent-skills/README.md`.

Users can drop project-local skill files into `.codex/addon-agent-skills/` to add requirements
without rewriting the core agent roles. These are plain Markdown instruction files, not built-in
Codex runtime skills. They work because the generated agentic workflow tells agents to read and
apply them.

Example files:

```text
.codex/addon-agent-skills/quality-gates-skill.md
.codex/addon-agent-skills/quality-gates-skills.md
.codex/addon-agent-skills/security-review-skill.md
.codex/addon-agent-skills/release-checklist-skill.md
```

In agentic mode:

- Orchestrator scans add-on skills and identifies which ones apply.
- Architect includes relevant skills in the implementation plan.
- Coder implements in a way that satisfies relevant skills.
- Tester validates required checks from relevant skills.
- Reviewer checks whether relevant skills were followed.
- If a relevant skill cannot be satisfied, the responsible role reports it as blocked with the
  reason.

Use `.codex/addon-agent-skills/SKILL-TEMPLATE.md` as the starting point for new add-on skills.

## Reasoning Policy

Markdown instructions cannot change reasoning level by themselves. The policy applies when the
runtime supports per-agent reasoning settings. If the runtime does not support overrides, agents use
the current session reasoning level and follow the same rigor procedurally.

Default policy:

- Explicit user or session reasoning settings win.
- If the user chose a higher reasoning level for the whole workflow, do not silently downgrade any
  role.
- Architect uses `xhigh` for non-trivial implementation planning.
- Reviewer uses `xhigh` for code review and regression analysis.
- Coder uses `medium` by default, moving to `high` or `xhigh` when implementation becomes complex,
  risky, or stuck.
- Tester uses `medium` by default, moving to `high` when failures are ambiguous, flaky, or
  gate-heavy.
- Orchestrator uses `medium` by default, moving to `high` for risky coordination or conflicting
  guidance.

## Subagents And Fallback

When runtime subagents are available, Orchestrator may delegate bounded role work to actual
subagents. When runtime subagents are unavailable, Codex should simulate Orchestrator, Architect,
Coder, Tester, and Reviewer sequentially in the same thread while still enforcing the Architect
approval gate.

When using real subagents, Orchestrator must assign clear ownership:

- Each worker gets a bounded responsibility and write scope.
- Parallel workers should not edit the same files unless explicitly coordinated.
- Workers must not revert or overwrite changes made by the user or other agents.
- Orchestrator integrates results and resolves conflicts before final validation.

## Blocked Work Policy

When work or validation is blocked, report it as blocked rather than passed. Classify the blocker:

- environment
- missing user input
- external service
- dependency/tooling
- test failure
- permissions
- unclear requirement

Record only useful blocker state in `.codex/session-notes.md` or `.codex/todo.md`. Do not copy full
logs into memory or chat responses; summarize the relevant lines and point to the source file.

## Memory Placement Rules

Use these rules to keep agentic memory useful:

- Put durable project-wide agent instructions in `AGENTS.md`.
- Put user requirements in `docs/requirements/`.
- Put Architect-generated plans in `docs/implementation-plans/`.
- Put user-provided validation evidence in `docs/user-findings/`.
- Put optional project-local agent skills in `.codex/addon-agent-skills/`.
- Put facts all future agents need in `.codex/session-notes.md`.
- Put completed chronological events in `.codex/worklog.md`.
- Put short-lived operational tasks in `.codex/todo.md`.
- Put role-specific durable lessons in `.codex/agents/memory/<role>.md`.
- Put substantial implementation plans in `docs/implementation-plans/` unless the project already
  has an explicitly established equivalent.
- Keep actual technical truth in the codebase, tests, and primary docs.

## What Not To Store

Do not store:

- Secrets, credentials, private keys, tokens, or personal data.
- Large command logs.
- Full copies of source files.
- Duplicated implementation plans.
- Worklog entries or temporary todos in `AGENTS.md`.
- Routine observations that will not help a future session.
- Stale guesses about code behavior when the code can be inspected directly.

## Expected Operating Flow

For non-trivial agentic work:

1. Orchestrator reads the request and relevant project guidance.
2. Orchestrator scans relevant requirements, user findings, and add-on skills.
3. Architect produces an implementation plan, stored in `docs/implementation-plans/` when the work
   is substantial.
4. Orchestrator asks the user to choose one of three options:
   - Approve: proceed with the implementation plan.
   - Revise: ask the user what needs to be revised, then return to Architect.
   - Stop: stop and cancel the agentic workflow.
   If the user chooses Revise, Architect updates the plan and Orchestrator presents the revised
   plan again with the same Approve, Revise, or Stop options.
5. Coder implements only after explicit approval.
6. Tester runs or identifies the required validation.
7. Reviewer reviews for defects, plan drift, and unresolved relevant findings.
8. Orchestrator completes the closeout checklist.

Closeout checklist:

- Update implementation plan status if a plan was used.
- Update documentation indexes when useful.
- State whether the Definition of Done was met, failed, or blocked.
- Report tests, quality gates, blocked checks, and manual validation gaps.
- State whether relevant user findings were addressed or explicitly left unresolved.
- Report changed files.
- Check whether `AGENTS.md` needs a durable project-wide update.
- Update `.codex/session-notes.md`, `.codex/worklog.md`, or `.codex/todo.md` only when useful.
- Update role memories only for durable role-specific lessons.

Final response contract:

- State whether the task was implemented, not implemented, or blocked.
- List important files changed.
- State the Definition of Done status.
- Report validation commands run and blocked checks.
- State the implementation plan status when a plan was used.
- Note unresolved findings or follow-ups.
- Mention whether `AGENTS.md` or agent memory was updated.
- Do not paste full logs; summarize relevant excerpts and reference the file.

For trivial tasks, the Orchestrator may skip roles, but should record why when operating in
agentic mode.

## Attribution

Authored by Victor Alexander Daud. Copyright (c) 2026.
Co-authored with Codex.
