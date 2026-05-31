# Codex Agentic Mode Bootstrap Instructions

Use this file to initialize a true agentic workflow in a new project.

Audience: Codex.

Objective: create project-local agentic coordination, instruction, and documentation-lane files. Do
not modify product code, build files, application behavior, or unrelated existing project
documentation unless the user explicitly asks.

## Required Behavior

When the user asks to initialize agentic mode from this file:

1. Determine the bootstrap mode before editing files.
   - `create`: create the target structure in a project that does not already have agentic files.
   - `merge`: preserve existing guidance and carefully merge missing files or sections.
   - `dry-run`: report what would be created, updated, skipped, or conflicted without editing files.
   - If the user does not specify a mode, use `create` only when no existing agentic structure is
     present. Use `merge` for existing projects.
2. Inspect the repository lightly.
   - Identify the project name, stack, main docs, test commands, and any existing agent guidance.
   - Identify whether version control is present.
   - Prefer fast file listing and targeted reads.
   - Do not run expensive builds or tests during setup.
3. Create `.codex/`, `.codex/agents/memory/`, and `.codex/addon-agent-skills/` if they do not
   exist.
4. Create `docs/implementation-plans/`, `docs/requirements/`, and `docs/user-findings/` if they do
   not exist.
   - If equivalent project docs folders already exist, preserve them and add only missing README
     guidance when it is safe.
   - Do not move existing project docs during setup.
5. Add or update only the agentic coordination, agent instruction, documentation-lane, and template
   files listed in `AGENTIC_FILE_TEMPLATES.md`.
6. Keep the files project-agnostic where possible, but fill in obvious project-specific placeholders
   such as project name and known source-of-truth docs.
7. Create `AGENTS.md` if it does not exist.
   - If `AGENTS.md` already exists, merge carefully instead of overwriting.
   - Keep `AGENTS.md` focused on durable project-wide instructions, not session memory.
   - For new projects with no implementation yet, use a conservative skeleton and mark structure,
     commands, and quality gates as to be documented later.
   - At task closeout, Orchestrator should check whether `AGENTS.md` needs an update and edit it
     only for durable project-wide conventions, commands, structure, quality gates, or instructions.
8. Preserve existing useful `.codex` content if present.
   - Do not overwrite existing memory without first merging it carefully.
   - If there is a conflict, keep existing project facts and add the new workflow rules around them.
9. Include the reasoning policy in the generated agentic docs.
   - Explain that Markdown alone cannot change reasoning level.
   - Use per-role runtime reasoning overrides only when the runtime supports them.
   - Do not silently downgrade roles when the user explicitly selected a higher reasoning level for
     the whole workflow.
10. Finish by reporting the bootstrap mode, created or updated files, and the next recommended
    prompt.

## Target File Tree

Create this structure:

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

## Setup Rules

Use `docs/agentic-mode/AGENTIC_FILE_TEMPLATES.md` as the template source.

If that file is unavailable, create equivalent files using these rules:

- `AGENTS.md` defines durable project-wide instructions for agents, including project status,
  source-of-truth order, coding rules, project structure, commands, quality gates, and maintenance
  rules.
- `docs/requirements/README.md` explains that this folder stores user-authored or user-approved
  requirements and acceptance criteria, and that requirements use `Draft`, `Approved`,
  `Implemented`, `Superseded`, or `Rejected` status.
- `docs/requirements/INDEX.md` provides a lightweight navigation index for requirements.
- `docs/requirements/REQ-TEMPLATE.md` provides a reusable requirements template with lifecycle
  status.
- `docs/implementation-plans/README.md` explains that Architect-generated implementation plans
  belong here and Coder implements only approved plans for non-trivial agentic changes.
- `docs/implementation-plans/INDEX.md` provides a lightweight navigation index for plans and active
  status.
- `docs/implementation-plans/IP-TEMPLATE.md` provides a reusable implementation-plan template with
  lifecycle status.
- `docs/user-findings/README.md` explains that user-provided evidence such as CI logs, QA notes,
  screenshots, crash traces, and exported test artifacts belongs here, and that sensitive raw
  findings should stay untracked or outside the repository when needed.
- `docs/user-findings/INDEX.md` provides a lightweight navigation index for findings and resolution
  status.
- `docs/user-findings/UF-TEMPLATE.md` provides a reusable user-finding template with evidence and
  sensitivity sections.
- `.codex/README.md` explains the project-local Codex memory area, source-of-truth order, startup
  checklist, memory placement rules, and agentic activation.
- `.codex/session-notes.md` stores shared continuity notes for current or recent tasks.
- `.codex/worklog.md` stores concise completed work entries.
- `.codex/todo.md` stores short-lived operational todos only.
- `.codex/addon-agent-skills/README.md` explains how users can add project-local skill files such
  as quality gates, security review rules, or release checklists.
- `.codex/addon-agent-skills/SKILL-TEMPLATE.md` provides a reusable add-on skill template.
- `.codex/agents/README.md` defines the agentic workflow and approval gate.
- `.codex/agents/ORCHESTRATOR.md` defines coordination, plan approval, role handoff, and memory
  update responsibilities.
- `.codex/agents/ARCHITECT.md` defines planning responsibilities and forbids implementation.
- `.codex/agents/CODER.md` defines implementation responsibilities after approval.
- `.codex/agents/TESTER.md` defines validation responsibilities and blocked-gate reporting.
- `.codex/agents/REVIEWER.md` defines review responsibilities.
- `.codex/agents/memory/*.md` files start empty except for role-specific memory rules.

## True Agentic Contract

The generated workflow must enforce this contract:

- Orchestrator coordinates the work.
- If runtime subagents are available, Orchestrator may delegate bounded role work to actual
  subagents. If not, Codex simulates the roles sequentially while preserving the approval gate.
- When delegating to real subagents, Orchestrator assigns clear ownership and write scopes, avoids
  overlapping edits unless explicitly coordinated, and prevents agents from reverting user or other
  agents' changes.
- When version control exists, Orchestrator checks worktree state before implementation and reports
  changed files at closeout.
- Orchestrator checks relevant `docs/requirements/` and `docs/user-findings/` files before planning
  when the user's task references requirements or findings.
- Orchestrator checks requirement status before planning and surfaces `Draft`, `Rejected`, or
  `Superseded` requirements instead of silently treating them as approved.
- Orchestrator scans `.codex/addon-agent-skills/` and identifies relevant add-on skills.
- Orchestrator applies the reasoning policy when runtime-backed per-agent reasoning is available.
- Architect creates the implementation plan first for non-trivial changes.
- Architect writes substantial implementation plans to `docs/implementation-plans/`.
- Architect assigns an explicit implementation-plan status and does not rely on the newest plan as
  active by default.
- Architect assigns a risk level of `Low`, `Medium`, or `High` to non-trivial plans.
- Architect defines Definition of Done criteria that scale with the plan risk level.
- Architect includes rollback or recovery notes for high-risk plans.
- Architect treats `docs/requirements/` as user intent and `docs/user-findings/` as evidence to
  evaluate.
- Architect plans from `Approved` requirements when possible. If the user asks to implement from a
  `Draft` requirement, Orchestrator must surface that status before implementation planning
  proceeds.
- Architect includes relevant add-on skills in the plan.
- Orchestrator asks the user to choose Approve, Revise, or Stop after Architect finishes the plan.
- Approve means proceed with the implementation plan.
- Revise means ask the user what needs to be revised, then return the plan to Architect.
- Stop means stop and cancel the agentic workflow.
- After Revise, Architect updates the plan and Orchestrator presents the revised plan again with
  the same Approve, Revise, or Stop options.
- Active implementation plans must be named by the user, `.codex/session-notes.md`, or an explicit
  Orchestrator handoff.
- Coder does not implement until the user explicitly approves the plan.
- Coder implements in a way that satisfies relevant add-on skills.
- Coder implements from the approved plan for non-trivial agentic changes.
- Coder preserves unrelated user changes and does not commit unless the user explicitly asks.
- Agents must not run destructive version-control commands unless the user explicitly approves.
- Agents must not add dependencies, services, build tools, CI changes, paid services, networked
  infrastructure, or external integrations unless the approved plan explicitly includes them and the
  user approves that scope.
- Tester reports exact commands, pass/fail status, blocked gates, and manual validation gaps.
- Tester reports blocked work or validation as blocked, never passed.
- Tester validates the Definition of Done for the approved plan risk level.
- Tester validates requirements from relevant add-on skills.
- Tester uses relevant `docs/user-findings/` files as reproduction or validation evidence.
- Tester classifies blocked validation as environment, missing user input, external service,
  dependency/tooling, test failure, permissions, or unclear requirement.
- Reviewer reports defects first, ordered by severity, with file and line references when available.
- Reviewer checks whether relevant add-on skills were followed.
- Reviewer checks drift against the approved implementation plan and relevant requirements.
- Reviewer checks whether the Definition of Done was met or honestly reported as blocked.
- Reviewer checks whether relevant user findings were addressed or explicitly left unresolved.
- Security-sensitive work touching auth, secrets, permissions, payments, encryption, user data,
  networking, deployment, external integrations, or dependency supply chain requires
  security-focused review and any relevant security add-on skill.
- If a relevant add-on skill cannot be satisfied, the responsible role reports it as blocked with
  the reason.
- Orchestrator applies the conflict model before implementation when guidance conflicts:
  current user request, code/tests as current behavior, requirements as desired behavior,
  implementation plans as execution intent, user findings as evidence, and add-on skills as
  relevant requirements.
- Orchestrator ensures findings and logs do not get copied into memory or `AGENTS.md`; only concise
  durable conclusions should be summarized when useful.
- Orchestrator ensures sensitive raw findings remain untracked or outside the repository when
  needed; committed findings should be redacted summaries or safe evidence only.
- Orchestrator and role agents do not paste full logs into chat responses; they summarize relevant
  excerpts and reference the source file.
- When external research is needed, agents prefer primary sources such as official documentation,
  standards, source repositories, release notes, vendor docs, or original issue trackers.
- Requirements, plans, and findings use stable sortable IDs:
  - `REQ-0001-short-title.md`
  - `IP-0001-short-title.md`
  - `UF-0001-short-title.md`
  - add-on skills use `lowercase-kebab-skill.md`
- Requirements use explicit lifecycle statuses: `Draft`, `Approved`, `Implemented`, `Superseded`,
  or `Rejected`.
- At task closeout, Orchestrator checks whether `AGENTS.md` needs a durable project-wide update.
- Orchestrator completes the closeout checklist:
  - update implementation plan status if a plan was used
  - state whether the Definition of Done was met, failed, or blocked
  - report tests, quality gates, blocked checks, and manual validation gaps
  - state whether relevant user findings were addressed or left unresolved
  - report changed files
  - update documentation indexes when useful
  - check whether `AGENTS.md` needs a durable project-wide update
  - update `.codex/session-notes.md`, `.codex/worklog.md`, or `.codex/todo.md` only when useful
  - update role memories only for durable role-specific lessons
- Orchestrator final response includes implemented/not implemented/blocked status, changed files,
  Definition of Done status, validation run and blocked checks, plan status when relevant,
  unresolved findings or follow-ups, and whether `AGENTS.md` or memory was updated.

## Definition Of Done

Generated agentic docs must define Done by risk level:

- `Low`: scoped implementation completed, focused validation run, changed files reported.
- `Medium`: low-risk criteria plus relevant broader gates, plan status updated, unresolved findings
  documented.
- `High`: medium-risk criteria plus rollback or recovery notes, security-focused review when
  applicable, broader validation, and explicit residual-risk notes.

Blocked validation must be reported as blocked, not passed.

## Reasoning Policy

Generated agentic docs must include this policy:

- Explicit user or session reasoning settings win.
- If the user chose a higher reasoning level for the whole workflow, do not silently downgrade any
  role.
- When runtime-backed per-agent reasoning overrides are available:
  - Architect uses `xhigh` for non-trivial implementation planning.
  - Reviewer uses `xhigh` for code review and regression analysis.
  - Coder uses `medium` by default, moving to `high` or `xhigh` when implementation becomes
    complex, risky, or stuck.
  - Tester uses `medium` by default, moving to `high` when failures are ambiguous, flaky, or
    gate-heavy.
  - Orchestrator uses `medium` by default, moving to `high` for risky coordination or conflicting
    guidance.
- If per-agent overrides are unavailable, all roles use the current session reasoning level and
  follow the same rigor procedurally.

## Memory Decision Table

Use this table when deciding where to write memory:

| Information type | File |
| --- | --- |
| Durable project-wide agent instructions | `AGENTS.md` |
| User-authored or user-approved requirements | `docs/requirements/` |
| Requirements index | `docs/requirements/INDEX.md` |
| Requirements template | `docs/requirements/REQ-TEMPLATE.md` |
| Architect-generated implementation plans | `docs/implementation-plans/` |
| Implementation plan index | `docs/implementation-plans/INDEX.md` |
| Implementation plan template | `docs/implementation-plans/IP-TEMPLATE.md` |
| User-provided findings, logs, screenshots, and validation evidence | `docs/user-findings/` |
| User findings index | `docs/user-findings/INDEX.md` |
| User finding template | `docs/user-findings/UF-TEMPLATE.md` |
| Optional project-local agent skill instructions | `.codex/addon-agent-skills/*.md` |
| Add-on skill template | `.codex/addon-agent-skills/SKILL-TEMPLATE.md` |
| Current state, active plan, blockers, cross-role decisions | `.codex/session-notes.md` |
| Completed chronological events | `.codex/worklog.md` |
| Short-lived operational tasks | `.codex/todo.md` |
| Coordination rules and user workflow preferences | `.codex/agents/memory/orchestrator.md` |
| Architecture constraints and planning risks | `.codex/agents/memory/architect.md` |
| Implementation conventions and recurring code pitfalls | `.codex/agents/memory/coder.md` |
| Validation commands, blocked gates, flaky checks | `.codex/agents/memory/tester.md` |
| Recurring review risks and regression-prone areas | `.codex/agents/memory/reviewer.md` |
| Product or technical implementation plan | Repository planning docs, not agent memory |
| Source-of-truth behavior | Code and tests |

## Recommended Final Message

After setup, report:

- Bootstrap mode used.
- Files created or updated.
- Any existing project guidance that was detected.
- The activation prompts to use next:

```text
Use .codex/agents in agentic mode. Orchestrator coordinates Architect, Coder, Tester, and Reviewer.
Apply the reasoning policy from .codex/agents/README.md. Architect must create the implementation
plan first and wait for my approval before coding. Task: <task>
```

```text
Use .codex/agents in agentic mode and apply relevant skills from .codex/addon-agent-skills/.
Architect must include applicable skills in the plan. Coder and Tester must satisfy or report
blockers for those skills. Task: <task>
```

```text
Use .codex/agents in agentic mode. Read relevant files under docs/requirements/ and
docs/user-findings/ before planning. Treat user findings as evidence, not automatic root cause.
Architect must create the implementation plan first and wait for my approval. Task: <task>
```

```text
Use .codex/agents in agentic mode. Keep the whole workflow at my current reasoning level; do not
downgrade any role. Architect creates the plan first and waits for my approval. Task: <task>
```
