# IP-0000 Short Title

- Workflow contract version: 2.6.0

## Status

Proposed

Allowed: `Proposed`, `Approved`, `In Progress`, `Done`, `Superseded`, or `Abandoned`.

- Plan revision: 1

Increment the plan revision for every material change to scope, risk, acceptance criteria,
dependency-node scope, write ownership, required validation, or review coverage. Lifecycle,
evidence, approval-metadata, and closeout updates do not increment it. A material revision clears
approval, resets status to `Proposed`, and requires explicit user approval again.
If the workflow contract changes while this plan is `In Progress`, continue under its recorded
compatible version unless a material migration is reviewed and explicitly accepted.

## Risk Level

Low

Allowed: `Low`, `Medium`, or `High`.

## Work Classification

- Work class: Small
- Workflow route: Lite
- Requested workflow depth: Auto
- Classification rationale:
- Risk override applied: No

Allowed work classes are `Trivial`, `Small`, `Medium`, and `Large`. Allowed routes are `Direct`,
`Lite`, `Standard`, and `Full`. Medium risk requires at least `Standard`; High risk and
security-sensitive work require `Full`. A user may request a more rigorous route, but agents must
not silently downgrade a safety-required route.

## Resource-Efficiency Controls

- Efficiency profile: Balanced
- Token budget: Auto
- Token usage observability: Not measured
- Validation/review/closeout reserve: 25%
- Max retries per node: 1
- Integration mode: Auto
- Local metrics: Off
- Effective integration mode:
- Optional worker spawn-value rule:
- Early-exit rule:

Allowed profiles are `Economy`, `Balanced`, and `Thorough`; `Balanced` is the default. Token budget
is `Auto` or a positive integer and remains advisory. Use `Not measured` when consumption is not
observable. These controls may reduce optional context, redundancy, or retries, but never mandatory
approval, validation, security review, or repository quality gates. Integration mode is `Auto`,
`Leased writers`, or `Single integrator`; escalate `Leased writers` when non-overlapping writes
cannot be guaranteed. The reserve is an integer from `1%` through `99%`. Local metrics accepts
`Off` or `On` and defaults to `Off`. Defaults apply only to omitted controls; clarify invalid
explicit values rather than silently replacing them.

## Runtime Capability Preflight

Run once per task and recheck only after a material runtime change.

| Capability | Requested | Available | Fallback or constraint |
| --- | --- | --- | --- |
| Delegation and concurrency |  |  |  |
| Tools and commands |  |  |  |
| Permissions and write access |  |  |  |
| Version-control operations |  |  |  |
| Context or budget observability |  |  |  |
| Model or reasoning controls | Inherit user/session |  | Do not hardcode model IDs |

## Execution Mode

Sequential

Allowed: `Sequential` or `Parallel`.

For `Parallel`, list independent work items, dependency boundaries, and non-overlapping ownership.
For planned routes, Architect, approval, Coder, Tester, and Reviewer still run in order.

- Max parallel subagents: 4
- Coder max: Inherit global
- Tester max: Inherit global
- Reviewer max: Inherit global
- Parallel work items:
- Ownership boundaries:
- Planned workers by stage:
- Sequential fallback condition:

All counts are positive-integer ceilings, not required worker counts. `Sequential` ignores the caps
and permits at most one active subagent at a time.

## Source Inputs

- User request:
- Requirements:
- User findings:
- Relevant native skills:

## Shared Task Packet

- Task-packet revision: 1
- Objective:
- Acceptance criteria IDs:
- Relevant files and symbols:
- Constraints:
- Non-goals:
- Approved decisions:
- Required skills:
- Exact validation commands:
- Applicable workflow conformance scenarios:
- Evidence baseline or revision:
- Delta-first impact set:
- Compact handoff fields:
- Current checkpoint:

All roles use this packet as the default handoff. Reopen the wider repository only when the packet
is missing required evidence, relevant files changed, or an agent records why the evidence is
stale.

## Summary

Short description of the planned change.

## Scope

- In scope.

## Non-Goals

- Out of scope.

## Proposed Changes

- Change 1.
- Change 2.

## Files Or Areas Likely To Change

- Path or area.

## Delta-First Impact Map

Start with planned or changed files and symbols, nearby tests, direct consumers and dependencies,
affected components, and required gates. Add wider context only with a reason.

| File or symbol | Nearby tests | Direct consumers or dependencies | Component or integration boundary | Specialized gate | Expansion trigger |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Material Assumption Register

Record only assumptions capable of changing scope, safety, correctness, validation, or a decision.

| ID | Assumption | Owner | Confidence | Evidence | Impact if false | Invalidation condition | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 |  |  |  |  |  |  | Open |

Allowed statuses: `Open`, `Confirmed`, `Rejected`, or `Superseded`. Outcome-changing Open
assumptions and Low confidence block the affected node.

## Dependency Graph And Write Leases

Only schedule nodes whose dependencies are complete. Each writable path may have only one active
lease. Read-only work does not require a lease.

| Node | Stage | Task | Depends on | Owner | Read scope | Write lease | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | Coder | Example bounded change | None | Unassigned | Relevant files | `path/` | Ready |

### Invalidation And Cancellation

| Changed input or upstream decision | Evidence, criteria, or nodes invalidated | Queued work to cancel | Active lease quarantine and reconciliation | Replacement action |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Release a never-active queued node's lease immediately when cancelled. Retain or quarantine an
active writer's lease until stop or finish is confirmed and its last write state is reconciled;
only then release or reassign it. Never integrate stale results.

In `Single integrator` mode, exactly one designated Coder owns shared write leases. Other Coders
return read-only analysis or proposed patches with evidence references.

## Evidence And Decision Ledger

Check this ledger before rescanning files or rerunning commands. Reuse fresh evidence; if it is
stale or insufficient, record why before replacing it.

Each reusable evidence fingerprint records a stable ID, repository revision, relevant inputs or
hashes, exact command or method, environment details and tool version, timestamp, concise result
digest, and invalidation condition.

| ID | Type | Revision and relevant inputs or hashes | Command or method | Environment and tool version | Timestamp | Result digest or decision | Dependents | Invalidation condition | Status | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | Evidence | Revision and paths | Command or inspection | Runtime and tool version | Date/time | Concise digest | Node or AC ID | Relevant input changes | Fresh | Unassigned |

Do not read extra sensitive content solely to calculate a hash. `Fresh`, `Stale`, `Superseded`, and
`Blocked` are valid evidence states.

## Progressive Validation Ladder

Run the cheapest applicable level first and stop on failure unless another command is needed to
diagnose it. Mark non-applicable levels `Skipped` with a reason and unavailable required levels
`Blocked`, never passed.

| Level | Scope | Command or method | Required when | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| V1 | Format, syntax, and static checks |  | Applicable | Pending |  |
| V2 | Tests closest to changed files |  | Applicable | Pending |  |
| V3 | Affected package or component |  | Medium/High or shared behavior | Pending |  |
| V4 | Integration or end-to-end |  | Cross-component or High risk | Pending |  |
| V5 | Full suite, security, performance, or deployment gates |  | High risk or required quality gate | Pending |  |

Broaden validation only for shared behavior, risk, failure, uncertain impact, a repository gate, or
Low confidence. Reserve the stated share of observable budget for validation, review, and closeout;
block rather than silently skip a required gate.

## Failure Classification And Retry Budget

| Node or gate | Attempt | Classification | New hypothesis or changed input | Retry used | Circuit state | Next action |
| --- | --- | --- | --- | --- | --- | --- |
|  | 1 |  |  | 0 | Closed |  |

Classifications are implementation defect, test defect, flaky result, environment, missing
dependency/tooling, pre-existing failure, permission, and unclear requirement. Classify an
unavailable external service as `Environment`; map missing user input to `Unclear requirement` or
`Permission` according to the authority needed. A retry within the hard ceiling requires a changed
hypothesis, code or input, command, or environment. Open the circuit and stop the node after an
unchanged repeated failure, exhausted budget, or Coder/Tester oscillation without new evidence. A
new hypothesis alone does not reset the allowance; another attempt requires either a user-raised
ceiling or an approved plan revision that creates and budgets a materially new node.

## Acceptance-Criteria Traceability

Every applicable criterion must have implementation evidence, validation evidence, and a Reviewer
disposition before completion.

| Criterion | Implementation evidence | Validation evidence | Reviewer disposition |
| --- | --- | --- | --- |
| AC-1 |  |  | Pending |

## Review Allocation

- Planned Reviewer count:
- Review focuses: General
- Allocation rationale:
- Combined perspectives due to cap or runtime limit:
- Stable finding-ID prefix: F-
- Conditional adjudication trigger:

Typical allocation is one general Reviewer for Low risk, one or two targeted perspectives for
Medium risk, and correctness, security when applicable, and regression perspectives for High risk.
Required perspectives may be combined when caps or runtime capacity require fewer workers, but
must not be silently omitted.

### Review Finding Registry

| Finding ID | Severity | Underlying defect | Locations | Evidence IDs | Perspectives | Status |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 |  |  |  |  |  | Open |

Merge duplicate reports under one ID without losing evidence, severity, locations, or perspectives.
Use an additional adjudicator only for material conflict, Low confidence, elevated risk, or
required independent verification. Security-focused coverage remains mandatory when applicable.

## Confidence And Escalation

| Stage | Confidence | Basis | Uncertainty or conflict | Escalation |
| --- | --- | --- | --- | --- |
| Architect |  |  |  |  |
| Coder |  |  |  |  |
| Tester |  |  |  |  |
| Reviewer |  |  |  |  |

Allowed confidence values are `High`, `Medium`, and `Low`. Low confidence, conflicting evidence, or
an unresolved material assumption blocks stage advancement until investigated, clarified with the
user, or explicitly reported as blocked.

## Stage Checkpoints And Context Compaction

At each planned stage boundary, retain compact references instead of replaying full context.

| Checkpoint | Task-packet version and revision | Completed and ready nodes | Leases | Criteria and fresh evidence IDs | Decisions and material assumptions | Blockers and budget state | Confidence and next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CP-1 |  |  |  |  |  |  |  |

## Definition Of Done

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

## Rollback Or Recovery

Required for high-risk plans.

- Recovery step.
- Rollback step.

## Risks And Mitigations

- Risk: mitigation.

## Security Review

- Security-sensitive: No
- Security-focused review required: No
- Relevant security skills:

## Outcome Calibration, Memory Provenance, And Conformance

- Local outcome calibration requested: No
- Calibration evidence window or `Not applicable`:
- Calibration recommendation or `Not applicable`:
- Durable memory entry ID:
- Durable memory updates:
- Memory source and applicable revision or scope:
- Memory owner and last-confirmed date:
- Memory invalidation or review condition:
- Workflow conformance scenarios selected:
- Workflow conformance result:

Calibration uses only opt-in metadata when `Local metrics: On`; it never weakens approval,
security, validation, privacy, or user-selected controls. Durable memory updates require current
provenance and an explicit invalidation or review condition.

## Approval

- Status: waiting for user approval
- Approved by:
- Approval date:
- Approved plan revision:
- Explicit approval evidence reference:
- Active-plan reference:
- Implementation started:

Only explicit user approval moves `Proposed` to `Approved`. Orchestrator records these fields and
moves the active plan to `In Progress` before the first implementation write. Coder may accept the
startup handoff while it is `Approved`, but must not write before that transition. Later nodes,
testing, review, and rework use `In Progress` only while approval matches the same plan revision.
Material scope or risk drift increments the revision, clears approval, returns the plan to
`Proposed`, and repeats the gate.

## Closeout

- Final status:
- Definition of Done status:
- Validation completed:
- Acceptance criteria traceability complete:
- Review perspectives completed:
- Final confidence:
- Efficiency profile:
- Advisory budget and measured usage:
- Validation/review/closeout reserve outcome:
- Capability fallback:
- Requested parallelism caps:
- Worker counts used by stage:
- Actual peak concurrency:
- Execution-mode fallback:
- Requested and actual integration mode:
- Optional workers rejected by spawn-value gate:
- Context expansions and reasons:
- Evidence reused or invalidated:
- Commands or scans intentionally rerun:
- Retry counts and circuit-breaker events:
- Failure classifications:
- Obsolete nodes cancelled:
- Reviewer findings requiring rework:
- Duplicate findings merged:
- Conditional adjudication:
- Final checkpoint:
- Early-exit conditions met:
- Workflow conformance scenarios run:
- Local metrics requested:
- Outcome-calibration recommendation:
- Metrics recorded locally:
- Durable-memory update and provenance:
- User findings addressed:
- Residual risks:
- Follow-ups:
