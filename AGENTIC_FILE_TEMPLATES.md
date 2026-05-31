# Agentic File Templates

These templates are intentionally project-agnostic. Replace bracketed placeholders when initializing
a new project.

## `AGENTS.md`

```markdown
# AGENTS.md

Project-wide instructions for AI agents working on `[PROJECT_NAME]`.

## Project Status

This project may be newly initialized. Do not assume architecture, build commands, test commands, or
quality gates until they exist in the codebase or are explicitly defined by the user.

## Source Of Truth

Use this order when project facts conflict:

1. User's current request
2. Codebase and tests
3. `docs/requirements/` user-authored or user-approved requirements
4. Approved plans in `docs/implementation-plans/`
5. `docs/user-findings/` as evidence to evaluate
6. This `AGENTS.md`
7. `.codex/addon-agent-skills/` relevant skill instructions
8. `.codex/` operational memory
9. Role-specific agent memory

## Agent Rules

- Inspect existing files before implementing.
- Prefer established project patterns once they exist.
- Do not invent architecture documentation before code or user decisions support it.
- Keep implementation changes scoped to the user's request and approved plan.
- Preserve unrelated user changes.
- Treat `docs/user-findings/` as evidence, not automatic root cause.
- Do not rewrite user-authored requirements casually.
- Plan from `Approved` requirements when possible. Surface `Draft`, `Rejected`, or `Superseded`
  requirements before implementation.
- Do not infer that the newest implementation plan is active.
- Surface conflicts between current user instructions, code/tests, requirements, plans, findings, and
  add-on skills before implementation.
- Preserve unrelated user changes and check version-control state before implementation when
  version control exists.
- Do not commit unless the user explicitly asks.
- Do not run destructive version-control commands unless the user explicitly approves.
- Do not add dependencies, services, build tools, CI changes, paid services, networked
  infrastructure, or external integrations unless the approved plan includes them and the user
  approves that scope.
- When external research is needed, prefer primary sources such as official documentation,
  standards, source repositories, release notes, vendor docs, or original issue trackers.
- Do not paste full logs into chat responses; summarize relevant excerpts and reference the source
  file.
- Report blocked validation as blocked, not passed.
- Update this file only for durable project-wide instructions.
- Do not use this file as a worklog, todo list, or session memory store.

## Project Structure

Recommended documentation lanes:

- `docs/requirements/`: user-authored or user-approved requirements and acceptance criteria.
- `docs/implementation-plans/`: Architect-generated implementation plans.
- `docs/user-findings/`: user-provided findings, logs, screenshots, QA notes, and validation
  evidence.
- `docs/*/INDEX.md`: lightweight navigation indexes for each documentation lane.

Application source structure should be documented after implementation creates stable structure.

## Naming Conventions

- Requirements: `REQ-0001-short-title.md`
- Implementation plans: `IP-0001-short-title.md`
- User findings: `UF-0001-short-title.md`
- Add-on skills: `lowercase-kebab-skill.md`

Keep IDs stable after creation. If an item is superseded, update status or notes instead of
renaming it casually.

## Requirements Lifecycle

Requirements use explicit status labels:

- `Draft`: captured but not approved.
- `Approved`: user-approved and ready to plan from.
- `Implemented`: implemented and validated.
- `Superseded`: replaced by a newer requirement or user decision.
- `Rejected`: intentionally not pursued.

Architect should plan from approved requirements when possible. If the user asks to implement from a
draft requirement, Orchestrator should surface that status before planning.

## Risk And Security

- Architect assigns non-trivial plans a `Low`, `Medium`, or `High` risk level.
- High-risk plans require rollback or recovery notes.
- Security-sensitive work touching auth, secrets, permissions, payments, encryption, user data,
  networking, deployment, external integrations, or dependency supply chain requires
  security-focused review.
- Apply relevant security add-on skills when they exist.

## Definition Of Done

Definition of Done scales with risk:

- `Low`: scoped implementation completed, focused validation run, changed files reported.
- `Medium`: low-risk criteria plus relevant broader gates, plan status updated, unresolved findings
  documented.
- `High`: medium-risk criteria plus rollback or recovery notes, security-focused review when
  applicable, broader validation, and explicit residual-risk notes.

Blocked validation must be reported as blocked, not passed.

## Build And Test Commands

To be documented after commands exist.

## Quality Gates

To be documented after the project defines required gates.

## Planning And Documentation

To be documented after the project defines where implementation plans, change requests, design docs,
and release notes belong.

## Maintenance Rules

- Update `AGENTS.md` when durable project-wide conventions become known.
- At task closeout, Orchestrator checks whether `AGENTS.md` needs an update.
- Update `AGENTS.md` only for durable project-wide conventions, commands, structure, quality gates,
  or instructions.
- Do not store task history, temporary blockers, active plans, one-off bugs, or logs in `AGENTS.md`.
- Keep user requirements in `docs/requirements/`.
- Keep implementation plans in `docs/implementation-plans/`.
- Keep user-provided validation evidence in `docs/user-findings/`.
- Redact secrets, tokens, credentials, private URLs, personal emails, device identifiers, customer
  data, and other sensitive information from documentation and findings before committing or
  sharing.
- If raw findings contain sensitive data, keep the raw file untracked or outside the repository
  when needed. Commit only a redacted finding or summary that preserves enough evidence for agents
  to work.
- Keep temporary state in `.codex/session-notes.md`, `.codex/worklog.md`, or `.codex/todo.md`.
- Keep role-specific lessons in `.codex/agents/memory/<role>.md`.
- Keep optional project-local skill instructions in `.codex/addon-agent-skills/`.
- Remove or revise stale instructions when the codebase proves them wrong.
```

## `docs/requirements/README.md`

```markdown
# Requirements

This folder stores user-authored or user-approved requirements.

## Purpose

Use this folder for product intent, behavior requirements, acceptance criteria, workflow notes, and
other user-approved inputs that should guide planning and implementation.

## Rules

- Treat files here as user intent.
- Use explicit requirement statuses: `Draft`, `Approved`, `Implemented`, `Superseded`, or
  `Rejected`.
- Do not rewrite user-authored requirements casually.
- If agents summarize or reorganize requirements, preserve the original or clearly mark the derived
  version.
- Architect reads relevant requirements before creating implementation plans and plans from
  `Approved` requirements when possible.
- If the user asks to implement from a `Draft` requirement, Orchestrator should surface that status
  before planning.
- Reviewer checks whether implementation drifted from relevant requirements.
- Keep `INDEX.md` updated when useful for navigation.

## Statuses

- `Draft`: captured but not approved.
- `Approved`: user-approved and ready to plan from.
- `Implemented`: implemented and validated.
- `Superseded`: replaced by a newer requirement or user decision.
- `Rejected`: intentionally not pursued.

## Suggested File Names

- `REQ-0001-short-title.md`
- `feature-name-requirements.md`
- `acceptance-criteria-short-title.md`

Prefer the `REQ-0001-short-title.md` pattern for new requirements. Keep IDs stable after creation.
```

## `docs/requirements/INDEX.md`

```markdown
# Requirements Index

Use this index for navigation only. Do not duplicate full requirements here.

| ID | Title | Status | Latest Note |
| --- | --- | --- | --- |
| REQ-0001 | Short title | Draft | Initial placeholder |
```

## `docs/requirements/REQ-TEMPLATE.md`

```markdown
# REQ-0000 Short Title

## Status

Draft

Allowed statuses:

- Draft
- Approved
- Implemented
- Superseded
- Rejected

## Owner

[User or team]

## Problem

What user problem or product need this requirement addresses.

## Requirements

- Requirement 1.
- Requirement 2.

## Acceptance Criteria

- Criteria 1.
- Criteria 2.

## Non-Goals

- Out-of-scope item.

## Notes

- Links, references, or context.
```

## `docs/implementation-plans/README.md`

```markdown
# Implementation Plans

This folder stores Architect-generated implementation plans.

## Purpose

Use this folder for structured plans that describe how approved requirements or user requests will
be implemented.

## Rules

- Architect creates or updates plans here for non-trivial agentic implementation work.
- Orchestrator must ask the user to Approve, Revise, or Stop after Architect finishes a plan.
- Coder implements only from an approved plan for non-trivial agentic work.
- Tester validates against the approved plan.
- Reviewer checks for drift from the approved plan.
- High-risk plans must include rollback or recovery notes.
- Keep `INDEX.md` updated when useful for navigation.
- Plans are not a substitute for code, tests, or current user instructions.

## Suggested File Names

- `IP-0001-short-title.md`
- `IP-feature-name.md`
- `IP-fix-short-title.md`

Prefer the `IP-0001-short-title.md` pattern for new plans. Keep IDs stable after creation and use
status updates instead of renaming active plans.
```

## `docs/implementation-plans/INDEX.md`

```markdown
# Implementation Plans Index

Use this index for navigation only. Do not infer that the newest plan is active.

| ID | Title | Status | Risk | Latest Note |
| --- | --- | --- | --- | --- |
| IP-0001 | Short title | Proposed | Low | Initial placeholder |
```

## `docs/implementation-plans/IP-TEMPLATE.md`

```markdown
# IP-0000 Short Title

## Status

Proposed

Allowed statuses:

- Proposed
- Approved
- In Progress
- Done
- Superseded
- Abandoned

## Risk Level

Low

Allowed risk levels:

- Low
- Medium
- High

High-risk plans require rollback or recovery notes.

## Source Inputs

- User request:
- Requirements:
- User findings:
- Add-on skills:

## Summary

Short description of the planned change.

## Scope

- In scope.
- In scope.

## Non-Goals

- Out of scope.

## Proposed Changes

- Change 1.
- Change 2.

## Files Or Areas Likely To Change

- Path or area.

## Validation Plan

- Automated check.
- Manual check.

## Definition Of Done

Use the criteria that match this plan's risk level:

- Low:
  - Scoped implementation completed.
  - Focused validation run.
  - Changed files reported.
- Medium:
  - Low-risk criteria met.
  - Relevant broader gates run or reported as blocked.
  - Plan status updated.
  - Unresolved findings documented.
- High:
  - Medium-risk criteria met.
  - Rollback or recovery notes included.
  - Security-focused review completed when applicable.
  - Broader validation completed or reported as blocked.
  - Residual risk explicitly noted.

## Rollback Or Recovery Plan

Required for high-risk plans. Use `Not required - Low risk` or `Not required - Medium risk` only
when the risk assessment supports that.

- Recovery step.
- Rollback step.

## Risks And Mitigations

- Risk: mitigation.

## Security Review

- Security-sensitive: No
- Security-focused review required: No
- Relevant security add-on skills:

## Approval

- Status: waiting for user approval.
- Approved by:
- Approval date:

## Closeout

- Final status:
- Definition of Done status:
- Validation completed:
- User findings addressed:
- Follow-ups:
```

## `docs/user-findings/README.md`

```markdown
# User Findings

This folder stores user-provided findings and validation evidence.

## Purpose

Use this folder for files the user provides after testing or external validation, such as CI logs,
TeamCity exports, QA notes, screenshots, crash traces, recordings, profiler output, or bug reports.

## Rules

- Treat files here as evidence to inspect, not automatic root cause.
- Use statuses `Open`, `Resolved`, `Stale`, or `Superseded`.
- Findings may be stale, environment-specific, incomplete, or caused by setup issues.
- Redact secrets, tokens, credentials, private URLs, personal emails, device identifiers, customer
  data, and other sensitive information before committing or sharing findings.
- If raw findings contain sensitive data, keep the raw file untracked or outside the repository
  when needed. Commit only a redacted finding or summary that preserves enough evidence for agents
  to work.
- Keep large logs as files; summarize only the relevant conclusions in `.codex/session-notes.md`
  when useful.
- Do not paste full logs into chat responses; summarize relevant excerpts and reference the source
  file.
- Architect considers relevant findings before planning fixes.
- Tester uses relevant findings for reproduction and validation.
- Reviewer checks whether the change addresses the evidence without overfitting to it.
- Keep `INDEX.md` updated when useful for navigation.

## Suggested File Names

- `UF-0001-teamcity-quality-gates-failure.md`
- `UF-0002-crash-log-short-title.txt`
- `UF-0003-qa-notes-short-title.md`

Prefer the `UF-0001-short-title.md` pattern for new findings. Keep IDs stable after creation.
```

## `docs/user-findings/INDEX.md`

```markdown
# User Findings Index

Use this index for navigation only. Treat findings as evidence, not automatic root cause.

| ID | Title | Status | Source | Latest Note |
| --- | --- | --- | --- | --- |
| UF-0001 | Short title | Open | User report | Initial placeholder |
```

## `docs/user-findings/UF-TEMPLATE.md`

```markdown
# UF-0000 Short Title

## Summary

Short description of the user finding.

## Status

Open

Allowed statuses:

- Open
- Resolved
- Stale
- Superseded

## Source

- Reporter:
- Date:
- Environment:
- Related task or plan:

## Evidence

- Log file:
- Screenshot:
- CI link:
- Reproduction notes:

## Sensitivity Check

Confirm before committing or sharing:

- [ ] Tokens, credentials, and private keys removed.
- [ ] Private URLs removed or redacted.
- [ ] Personal emails and identifiers removed or redacted.
- [ ] Customer or production data removed or redacted.
- [ ] Sensitive raw artifacts are untracked or stored outside the repository when needed.

## Observed Behavior

What happened.

## Expected Behavior

What should have happened.

## Agent Notes

Treat this as evidence, not automatic root cause.
```

## `.codex/README.md`

```markdown
# Codex Workspace

This folder stores lightweight Codex-specific working memory for `[PROJECT_NAME]`.

## Scope

- Short task continuity notes
- Operational todos
- Concise worklog entries
- Optional add-on agent skills under `.codex/addon-agent-skills/`
- Agentic role definitions and role-specific memory under `.codex/agents/`

## Out Of Scope

- Product requirements that belong in primary project docs
- Full implementation plans that belong in the repository planning area
- Large copied command logs
- Secrets, credentials, private keys, tokens, or personal data

## Source Of Truth

Use this order when project facts conflict:

1. Codebase and tests
2. User's current request
3. `docs/requirements/` user-authored or user-approved requirements
4. Approved plans in `docs/implementation-plans/`
5. `docs/user-findings/` as evidence to evaluate
6. `AGENTS.md` project-wide agent instructions
7. Existing project-specific agent or assistant guidance
8. `.codex/addon-agent-skills/` relevant skill instructions
9. `.codex/` operational memory
10. Agent role memory

## Startup Checklist

1. Read this file.
2. Read `.codex/session-notes.md`.
3. Read `AGENTS.md` if it exists.
4. Read relevant `docs/requirements/` files when the task references requirements or product intent.
5. Read relevant `docs/user-findings/` files when the task references user testing, CI failures,
   logs, bug reports, or external validation.
6. Read primary project guidance if it exists.
7. If the user asks for agentic mode, read `.codex/agents/README.md`, relevant role files, and
   applicable files under `.codex/addon-agent-skills/`.
8. Read implementation plans only when the user references one or session notes identify one as
   active.

## Agentic Mode

Use `.codex/agents/` when the user explicitly asks for agentic mode, multiple agents, delegation,
or a named role such as Orchestrator, Architect, Coder, Tester, or Reviewer.

In agentic implementation work:

- Architect creates the plan first.
- Orchestrator asks the user to choose Approve, Revise, or Stop.
- Approve proceeds with the implementation plan.
- Revise asks the user what needs to be revised, then returns to Architect.
- Stop stops and cancels the agentic workflow.
- Coder does not implement until the user explicitly approves.
- Tester validates and reports blocked gates honestly.
- Reviewer checks for bugs, regressions, missing tests, and drift from the approved plan.
- Orchestrator applies the reasoning policy from `.codex/agents/README.md` when runtime support is
  available.

## Memory Rules

- Put shared current state in `.codex/session-notes.md`.
- Put completed chronological work in `.codex/worklog.md`.
- Put short-lived operational tasks in `.codex/todo.md`.
- Put role-specific durable lessons in `.codex/agents/memory/<role>.md`.
- Put user requirements in `docs/requirements/`.
- Put Architect-generated plans in `docs/implementation-plans/`.
- Put user-provided validation evidence in `docs/user-findings/`.
- Put optional project-local skill instructions in `.codex/addon-agent-skills/`.
- Put durable project-wide instructions in `AGENTS.md`.
- Do not duplicate implementation plans outside `docs/implementation-plans/`.
- Do not duplicate code facts that can be inspected directly.
- If user findings contain sensitive raw data, keep raw artifacts untracked or outside the
  repository when needed and store only redacted summaries.
- Do not paste full logs into chat responses; summarize relevant excerpts and reference the source
  file.
```

## `.codex/addon-agent-skills/README.md`

```markdown
# Add-On Agent Skills

This folder stores optional project-local skill instructions for agentic mode.

These files are plain Markdown instructions, not built-in Codex runtime skills. Agents follow them
because `.codex/agents/` tells Orchestrator, Architect, Coder, Tester, and Reviewer to read and
apply relevant files from this folder.

## Use Cases

- Quality gates
- Security review rules
- Release checklists
- Framework-specific coding rules
- Accessibility requirements
- Performance budgets
- Compliance checks

## File Naming

Use descriptive lowercase names:

- `quality-gates-skill.md`
- `quality-gates-skills.md`
- `SKILL-TEMPLATE.md`
- `security-review-skill.md`
- `release-checklist-skill.md`

Prefer lowercase kebab-case names ending in `-skill.md`.

## Skill File Shape

Use this structure:

~~~~markdown
# Skill Name

## Purpose

Short description of what this skill enforces.

## Applies To

- Architect
- Coder
- Tester
- Reviewer

## Trigger

When this skill must be used.

## Rules

- Concrete requirement.
- Concrete requirement.

## Required Validation

- Commands, checks, or manual validation required by this skill.

## Failure Policy

- What counts as failed, blocked, or incomplete.
~~~~

## Agent Responsibilities

- Orchestrator scans this folder at the start of agentic mode and identifies relevant skills.
- Architect includes relevant skills in the implementation plan.
- Coder implements according to relevant skills.
- Tester validates required checks from relevant skills.
- Reviewer treats missed relevant skills as review findings.
- If a relevant skill cannot be satisfied, the responsible role reports it as blocked with the
  reason.

## Example

For `quality-gates-skill.md` or `quality-gates-skills.md`, the skill may require Coder to adjust
generated code until it is compatible with lint, coverage, mutation tests, or other quality gates.
Tester must run those gates when possible, or explicitly report blocked gates with the blocker.
```

## `.codex/addon-agent-skills/SKILL-TEMPLATE.md`

```markdown
# Skill Name

## Purpose

Short description of what this skill enforces.

## Applies To

- Orchestrator
- Architect
- Coder
- Tester
- Reviewer

## Trigger

When this skill must be used.

## Rules

- Concrete requirement.
- Concrete requirement.

## Required Validation

- Commands, checks, or manual validation required by this skill.

## Failure Policy

- What counts as failed, blocked, or incomplete.

## Reporting

- What each role must report when this skill applies.
```

## `.codex/session-notes.md`

```markdown
# Session Notes

Use this file for short continuity notes across active or recent tasks.

## Format

- Date:
- Task:
- Notes:
- Next step:

## Current State

- Date: [YYYY-MM-DD]
- Task: Agentic workflow initialized
- Notes:
  - `.codex/agents/` defines the project-local agentic workflow.
  - No active implementation plan has been designated yet.
- Next step:
  - Wait for the user to choose the next task.
```

## `.codex/worklog.md`

```markdown
# Worklog

Use this file for concise chronological entries of completed work.

## Format

- YYYY-MM-DD: Brief note.

## Entries

- [YYYY-MM-DD]: Initialized Codex agentic workflow files.
```

## `.codex/todo.md`

```markdown
# Codex Todo

Use this file only for short-lived operational todos.

## Rules

- Remove completed items promptly.
- Do not track product requirements here.
- Do not duplicate issue trackers or implementation plans.

## Current Operational Todos

- None.
```

## `.codex/agents/README.md`

```markdown
# Codex Agent System

This directory defines a project-local agentic workflow. It is an operating model for coordinated
assistant work, not a replacement for source code, tests, or primary project documentation.

## Activation

Use this workflow when the user explicitly asks for agentic mode, multiple agents, delegation, or
one of these roles by name:

- Orchestrator
- Architect
- Coder
- Tester
- Reviewer

## Sample Prompts

Normal agentic task:

~~~~text
Use .codex/agents in agentic mode. Orchestrator coordinates Architect, Coder, Tester, and Reviewer.
Apply the reasoning policy from .codex/agents/README.md. Architect must create the implementation
plan first and wait for my approval before coding. Task: <task>
~~~~

Agentic task with add-on skills:

~~~~text
Use .codex/agents in agentic mode and apply relevant skills from .codex/addon-agent-skills/.
Architect must include applicable skills in the plan. Coder and Tester must satisfy or report
blockers for those skills. Task: <task>
~~~~

Agentic task from requirements or user findings:

~~~~text
Use .codex/agents in agentic mode. Read relevant files under docs/requirements/ and
docs/user-findings/ before planning. Treat user findings as evidence, not automatic root cause.
Architect must create the implementation plan first and wait for my approval. Task: <task>
~~~~

Maximum-rigor workflow:

~~~~text
Use .codex/agents in agentic mode. Keep the whole workflow at my current reasoning level; do not
downgrade any role. Architect creates the plan first and waits for my approval. Task: <task>
~~~~

## Source Of Truth

Priority order:

1. Codebase and tests
2. User's current request
3. `docs/requirements/` user-authored or user-approved requirements
4. Approved plans in `docs/implementation-plans/`
5. `docs/user-findings/` as evidence to evaluate
6. `AGENTS.md` project-wide agent instructions
7. Existing project-specific guidance
8. `.codex/addon-agent-skills/` relevant skill instructions
9. `.codex/` shared operational memory
10. Role-specific agent memory

## Workflow

1. Orchestrator reads the task and relevant guidance.
2. Orchestrator scans relevant `docs/requirements/` and `docs/user-findings/` files, including
   requirement status and finding sensitivity.
3. Orchestrator scans `.codex/addon-agent-skills/` and identifies relevant skills.
4. Orchestrator resolves or surfaces conflicts before implementation.
5. Orchestrator applies the reasoning policy when runtime-backed per-agent reasoning is available.
6. Architect maps the problem and creates an implementation plan that includes relevant
   requirements, findings, skills, risk level, and Definition of Done.
7. Orchestrator presents the plan and waits for user approval.
8. Coder implements only after approval and follows the approved plan and relevant skills.
9. Tester validates the change, including checks required by relevant skills and findings.
10. Reviewer checks for defects, drift, missed relevant skills, and unresolved relevant findings.
11. Orchestrator completes the closeout checklist and updates useful memory.

## Subagents And Fallback

When runtime subagents are available, Orchestrator may delegate bounded role work to actual
subagents. When runtime subagents are unavailable, Codex should simulate Orchestrator, Architect,
Coder, Tester, and Reviewer sequentially in the same thread while still enforcing the approval gate.

When using real subagents:

- Assign each worker a bounded responsibility and write scope.
- Avoid overlapping file edits unless explicitly coordinated.
- Tell workers they are not alone in the codebase.
- Workers must not revert or overwrite user changes or other agents' changes.
- Orchestrator integrates results and resolves conflicts before final validation.

## Conflict Handling

- The user's current request wins over older documentation.
- Code and tests describe current behavior.
- `docs/requirements/` describes desired behavior and user intent.
- `docs/implementation-plans/` describes approved or proposed execution.
- `docs/user-findings/` is evidence to inspect, not automatic root cause.
- Add-on skills are requirements only when relevant and not in conflict with explicit user
  instruction.
- When documents conflict, Orchestrator surfaces the conflict before implementation.

## Version Control Safety

When the project uses version control:

- Check worktree state before implementation.
- Preserve unrelated user changes.
- Do not commit unless the user explicitly asks.
- Do not run destructive version-control commands unless the user explicitly approves.
- Report changed files at closeout.

## Dependency And Tooling Changes

Do not add dependencies, services, build tools, CI changes, paid services, networked infrastructure,
or external integrations unless the approved plan explicitly includes them and the user approves
that scope.

## External Research

When external research is needed, prefer primary sources such as official documentation, standards,
source repositories, release notes, vendor docs, or original issue trackers. Summarize and cite
sources when relevant. Do not rely on secondary summaries when a primary source is available.

## Requirements Lifecycle

Requirements in `docs/requirements/` should use explicit statuses:

- `Draft`: captured but not approved.
- `Approved`: user-approved and ready to plan from.
- `Implemented`: implemented and validated.
- `Superseded`: replaced by a newer requirement or user decision.
- `Rejected`: intentionally not pursued.

Architect should plan from `Approved` requirements when possible. If the user asks to implement from
a `Draft` requirement, Orchestrator should surface that status before planning. `Rejected` and
`Superseded` requirements should not be treated as active unless the user explicitly reopens them.

## Implementation Plan Lifecycle

Plans in `docs/implementation-plans/` should use explicit statuses:

- `Proposed`: Architect drafted the plan, but the user has not approved it.
- `Approved`: the user approved the plan and Coder may implement it.
- `In Progress`: implementation has started.
- `Done`: implementation and expected validation are complete.
- `Superseded`: a newer plan or user decision replaced it.
- `Abandoned`: the plan was stopped and should not be implemented.

Do not infer that the newest implementation plan is active. The active plan must be named by the
user, `.codex/session-notes.md`, or an explicit Orchestrator handoff.

## Risk Level Policy

Architect assigns every non-trivial plan a risk level:

- `Low`: localized, reversible, low blast radius.
- `Medium`: touches shared behavior, cross-module contracts, important UX, or non-trivial data
  flow.
- `High`: touches data deletion, migrations, auth, payments, secrets, encryption, permissions,
  networking, deployment, external integrations, or other high-impact behavior.

Risk level drives validation depth. High-risk work requires broader validation, explicit Reviewer
focus, and rollback or recovery notes.

## Definition Of Done

Definition of Done scales with risk:

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

## Documentation Indexes

Use indexes for navigation:

- `docs/requirements/INDEX.md`
- `docs/implementation-plans/INDEX.md`
- `docs/user-findings/INDEX.md`

Indexes should summarize ID, title, status, and latest note without duplicating full content.

## Archive And Retention

- Mark completed implementation plans as `Done`.
- Mark replaced plans as `Superseded`.
- Mark stopped plans as `Abandoned`.
- Mark user findings as `Open`, `Resolved`, `Stale`, or `Superseded`.
- Keep large raw logs as files and summarize durable conclusions only when useful.

## Sensitive Findings Handling

Do not store secrets, credentials, private keys, tokens, personal data, customer data, or private
URLs in memory, `AGENTS.md`, chat responses, or committed findings. If raw findings contain
sensitive data, keep the raw artifact untracked or outside the repository when needed. Commit only a
redacted finding or summary that preserves enough evidence for agents to work.

## Security-Sensitive Work

If a task touches auth, secrets, permissions, payments, encryption, user data, networking,
deployment, external integrations, or dependency supply chain, Orchestrator should require a
security-focused review. If a relevant add-on security skill exists, it must be applied.

Security-sensitive plans should be treated as at least `High` risk unless the user explicitly scopes
them down and the codebase context supports that lower risk.

## Reasoning Policy

Markdown instructions cannot change reasoning level by themselves. This policy applies when the
runtime supports per-agent reasoning settings. If per-agent overrides are unavailable, all roles use
the current session reasoning level and follow the same rigor procedurally.

Explicit user or session reasoning settings win:

- If the user chose a higher reasoning level for the whole workflow, do not silently downgrade any
  role.
- If the user says to keep all roles at the current reasoning level, all roles inherit it.
- If the user asks for this policy and no higher global setting is explicit, Orchestrator may assign
  per-role reasoning where supported.

Default per-role policy when runtime-backed overrides are available:

- Orchestrator: `medium` by default; move to `high` for risky coordination or conflicting guidance.
- Architect: `xhigh` for non-trivial implementation planning.
- Coder: `medium` by default; move to `high` or `xhigh` when implementation becomes complex, risky,
  or stuck.
- Tester: `medium` by default; move to `high` when failures are ambiguous, flaky, or gate-heavy.
- Reviewer: `xhigh` for code review and regression analysis.

When reporting role handoffs, Orchestrator should mention any reasoning override that materially
affects the workflow.

## Required Plan Approval Gate

For every non-trivial agentic implementation task, Architect must create a plan before Coder starts.

After Architect finishes, Orchestrator must ask:

~~~~text
Architect has finished the implementation plan.

Options:
- Approve: proceed with the implementation plan.
- Revise: ask what needs to be revised, then return to Architect.
- Stop: stop and cancel the agentic workflow.
~~~~

No implementation should start until the user explicitly approves.

If the user chooses Revise, Orchestrator asks what needs to be revised and returns the plan to
Architect. If the user chooses Stop, Orchestrator stops the agentic workflow without implementation.

After a Revise cycle, Architect updates the plan and Orchestrator presents the revised plan again
with the same Approve, Revise, or Stop options.

## Memory Rules

Each role owns its memory file. Update memory only for durable facts that will help future sessions:

- project-specific constraints
- recurring commands or validation caveats
- decisions made by the user
- known risks or unresolved follow-ups
- role-specific lessons learned

Do not store secrets, credentials, private keys, tokens, personal data, large logs, or duplicated
implementation plans. Sensitive raw findings should stay untracked or outside the repository when
needed; memory should contain only redacted summaries or durable conclusions.

## Closeout Checklist

- Update implementation plan status if a plan was used.
- Update documentation indexes when useful.
- State whether the Definition of Done was met, failed, or blocked.
- Report tests, quality gates, blocked checks, and manual validation gaps.
- State whether relevant user findings were addressed or explicitly left unresolved.
- Report changed files.
- Check whether `AGENTS.md` needs a durable project-wide update.
- Update `.codex/session-notes.md`, `.codex/worklog.md`, or `.codex/todo.md` only when useful.
- Update role memories only for durable role-specific lessons.

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
logs into memory or chat responses; summarize relevant excerpts and reference the source file.

## Final Response Contract

Orchestrator's final response should include:

- implemented, not implemented, or blocked status
- important files changed
- Definition of Done status
- validation commands run and blocked checks
- implementation plan status when a plan was used
- unresolved findings or follow-ups
- whether `AGENTS.md` or agent memory was updated
- concise log excerpts only when needed, never full logs
```

## `.codex/agents/ORCHESTRATOR.md`

```markdown
# Orchestrator

## Mission

Coordinate agentic work from request intake through planning, implementation, validation, review,
and memory updates.

## Responsibilities

- Clarify the user's goal when needed.
- Identify whether agentic mode is appropriate.
- Check worktree state before implementation when version control exists.
- Read relevant project guidance and role memory.
- Identify relevant files under `docs/requirements/` and check requirement status.
- Identify relevant files under `docs/user-findings/`, check sensitivity, and treat them as
  evidence, not conclusions.
- Scan `.codex/addon-agent-skills/` and identify relevant skills for the task.
- Surface conflicts between current user instructions, code/tests, requirements, plans, findings,
  and add-on skills before implementation.
- Assign clear ownership and write scopes when using real subagents.
- Ensure non-trivial plans have a risk level.
- Ensure plans define risk-appropriate Definition of Done criteria.
- Require security-focused review for security-sensitive work.
- Apply the reasoning policy when runtime-backed per-agent reasoning is available.
- Route planning to Architect before implementation.
- Enforce the user approval gate after the plan.
- Keep Coder, Tester, and Reviewer aligned with the approved scope.
- Report final state clearly.
- Complete the closeout checklist.
- Report whether the Definition of Done was met, failed, or blocked.
- Ensure documentation indexes are updated when useful.
- Ensure the final response follows the final response contract.
- Update shared memory and role memory only when durable facts were learned.

## Rules

- Do not let Coder implement before the user approves Architect's plan.
- If the user chooses Revise, ask what needs to be revised and return to Architect.
- If the user chooses Stop, stop the agentic workflow without implementation.
- After Architect revises a plan, present the revised plan again with Approve, Revise, or Stop
  options.
- Do not ignore relevant requirements or user findings.
- Do not silently treat `Draft`, `Rejected`, or `Superseded` requirements as approved.
- Do not treat user findings as already-root-caused.
- Do not infer that the newest implementation plan is active.
- Do not ignore relevant add-on skills.
- Do not silently downgrade reasoning when the user explicitly selected a higher level for the whole
  workflow.
- Do not hide failed or blocked validation.
- Do not claim the Definition of Done was met when required validation is blocked.
- Do not allow role memory to duplicate large plans or logs.
- Do not store sensitive raw findings in memory, `AGENTS.md`, or chat responses.
- Do not use `AGENTS.md` for task history, temporary blockers, active plans, one-off bugs, or logs.
- Do not allow full logs to be pasted into final responses; summarize and reference files.
- Do not allow dependency, tooling, CI, service, paid, or external-integration changes outside the
  approved plan.
- Prefer codebase and tests over memory when facts conflict.

## Memory

Use `.codex/agents/memory/orchestrator.md` for durable coordination lessons, user workflow
preferences, recurring approval constraints, and cross-role operating risks.
```

## `.codex/agents/ARCHITECT.md`

```markdown
# Architect

## Mission

Create coherent implementation plans that fit the existing project.

## Responsibilities

- Read the relevant code, docs, and constraints before planning.
- Read relevant requirements from `docs/requirements/`, including requirement status.
- Read relevant findings from `docs/user-findings/` as evidence to evaluate.
- Read applicable add-on skills identified by Orchestrator.
- Identify likely files and ownership boundaries.
- Define behavior changes and non-goals.
- Identify risks, validation needs, and rollout concerns.
- Identify whether the plan requires dependencies, services, build tools, CI changes, paid services,
  networked infrastructure, or external integrations.
- Assign a `Low`, `Medium`, or `High` risk level.
- Define risk-appropriate Definition of Done criteria.
- Include rollback or recovery notes for high-risk work.
- Flag security-sensitive work and any required security-focused review.
- Create an implementation plan that Coder can execute and that includes relevant requirements,
  findings, and skill requirements.
- Assign an explicit plan status.

## Rules

- Do not implement code.
- Do not run broad validation unless explicitly needed for planning.
- Keep the plan scoped to the user's request.
- Write substantial plans to `docs/implementation-plans/`.
- Use `docs/implementation-plans/IP-TEMPLATE.md` when available.
- Mark new plans as `Proposed` until the user approves them.
- Plan from `Approved` requirements when possible.
- Do not silently plan from `Draft`, `Rejected`, or `Superseded` requirements; ask Orchestrator to
  surface the status first.
- Treat security-sensitive work as at least `High` risk unless the user explicitly scopes it down
  and the codebase context supports that lower risk.
- Preserve user requirements; do not rewrite them casually.
- Treat user findings as evidence, not conclusions.
- Treat relevant add-on skills as planning requirements.
- Prefer primary sources when external research is needed.
- Do not include new dependencies, services, build tools, CI changes, paid services, networked
  infrastructure, or external integrations unless they are necessary and called out for user
  approval.
- Prefer existing project patterns over new abstractions.
- Put substantial plans in the repository's normal planning docs area when appropriate.

## Memory

Use `.codex/agents/memory/architect.md` for durable architecture constraints, planning patterns,
and recurring design risks.
```

## `.codex/agents/CODER.md`

```markdown
# Coder

## Mission

Implement approved plans using the project's existing patterns and quality standards.

## Responsibilities

- Read the approved plan and relevant code.
- Read relevant requirements and findings named in the approved plan.
- Read relevant add-on skills named by Orchestrator or the approved plan.
- Check worktree state before editing when version control exists.
- Keep edits scoped to the approved behavior.
- Preserve unrelated user changes.
- Add or update focused tests when the risk warrants it.
- Implement toward the approved plan's Definition of Done.
- Report changed files and implementation notes.

## Rules

- Do not implement before explicit user approval of the plan.
- For non-trivial agentic work, implement from the approved implementation plan.
- Do not implement from a `Proposed`, `Superseded`, or `Abandoned` plan.
- Do not perform unrelated refactors.
- Do not revert changes you did not make unless explicitly instructed.
- Do not commit unless the user explicitly asks.
- Do not run destructive version-control commands unless the user explicitly approves.
- Do not add dependencies, services, build tools, CI changes, paid services, networked
  infrastructure, or external integrations unless they are in the approved plan.
- Follow the project's existing style, frameworks, and helper APIs.
- Implement in a way that satisfies relevant add-on skills.
- Treat validation compatibility as part of implementation, not as an optional cleanup.
- Surface any known blocker that prevents the Definition of Done from being met.

## Memory

Use `.codex/agents/memory/coder.md` for durable implementation conventions, tricky files, recurring
pitfalls, and useful local patterns.
```

## `.codex/agents/TESTER.md`

```markdown
# Tester

## Mission

Validate the implemented change with the right level of rigor and report exact results.

## Responsibilities

- Identify required validation from the plan, project guidance, and changed files.
- Include validation implied by relevant requirements and user findings.
- Include validation required by relevant add-on skills.
- Scale validation depth to the approved plan risk level.
- Validate the approved plan's Definition of Done.
- Run targeted tests first when useful, then broader gates when appropriate.
- Report exact commands run.
- Report pass, fail, or blocked status for each required gate.
- Classify blocked checks as environment, missing user input, external service, dependency/tooling,
  test failure, permissions, or unclear requirement.
- Identify manual validation gaps.

## Rules

- Do not claim blocked validation passed.
- Do not claim the Definition of Done was met when required validation is blocked.
- Do not ignore relevant user findings.
- Do not ignore quality gates named by the project.
- Do not ignore validation required by relevant add-on skills.
- Do not copy large logs into memory; summarize only useful conclusions.
- Prefer deterministic automated checks when available.
- Keep validation proportional to risk and blast radius.

## Memory

Use `.codex/agents/memory/tester.md` for durable test commands, known blocked gates, flaky checks,
environment caveats, and manual validation requirements.
```

## `.codex/agents/REVIEWER.md`

```markdown
# Reviewer

## Mission

Review the change for defects, regressions, missing tests, and drift from the approved plan.

## Responsibilities

- Inspect the diff or changed files.
- Read relevant requirements and user findings named in the approved plan.
- Read relevant add-on skills named in the approved plan.
- Prioritize behavioral bugs and regression risk.
- Check whether tests match the risk.
- Check whether the Definition of Done was met, failed, or honestly reported as blocked.
- Check whether implementation stayed inside the approved scope.
- Check whether validation depth matched the approved risk level.
- Check whether high-risk work includes rollback or recovery notes.
- Check whether security-sensitive work received security-focused review.
- Check whether dependencies, tooling, CI, services, paid services, or external integrations were
  added outside the approved plan.
- Check whether implementation drifted from relevant requirements or the approved plan.
- Check whether relevant user findings were addressed or explicitly left unresolved.
- Check whether relevant add-on skills were followed.
- Report findings first, ordered by severity.

## Rules

- Use a code-review stance.
- Prefer concrete file and line references when available.
- Treat missed relevant add-on skills as review findings.
- Treat unresolved relevant user findings as review findings unless the plan explicitly defers them.
- Treat unapproved dependency or tooling changes as review findings.
- Treat a missing, failed, or falsely satisfied Definition of Done as a review finding.
- Do not bury findings under summaries.
- If no issues are found, say so and mention remaining residual risk or test gaps.

## Memory

Use `.codex/agents/memory/reviewer.md` for recurring bug classes, regression-prone areas, and review
checklists that are specific to this project.
```

## `.codex/agents/memory/orchestrator.md`

```markdown
# Orchestrator Memory

Use this file only for durable coordination lessons and user workflow preferences.

## Durable Notes

- None yet.
```

## `.codex/agents/memory/architect.md`

```markdown
# Architect Memory

Use this file only for durable architecture constraints, planning patterns, and design risks.

## Durable Notes

- None yet.
```

## `.codex/agents/memory/coder.md`

```markdown
# Coder Memory

Use this file only for durable implementation conventions, tricky files, and recurring code pitfalls.

## Durable Notes

- None yet.
```

## `.codex/agents/memory/tester.md`

```markdown
# Tester Memory

Use this file only for durable validation commands, blocked gates, flaky checks, and environment
caveats.

## Durable Notes

- None yet.
```

## `.codex/agents/memory/reviewer.md`

```markdown
# Reviewer Memory

Use this file only for durable review risks, recurring bug classes, and regression-prone areas.

## Durable Notes

- None yet.
```
