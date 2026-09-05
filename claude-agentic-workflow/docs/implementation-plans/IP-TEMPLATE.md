# IP-0000 Short Title

- Workflow contract version: 2.5.0

## Status

Proposed

Allowed: `Proposed`, `Approved`, `In Progress`, `Done`, `Superseded`, or `Abandoned`.

- Plan revision: 1

Increment the plan revision for every material change to scope, risk, acceptance criteria,
dependency-graph structure or node scope, write ownership, required validation strategy, or review
coverage. Normal plan/node lifecycle status, evidence, approval-metadata, and closeout updates do
not increment it. A material revision resets status to `Proposed` and requires explicit user
approval again.
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

Populate only the systems required by the selected route, risk, repository gates, and user
instructions. Mark an inactive section `Not applicable` with a concise reason; do not execute all
sections as a serial ceremony.

## Efficiency And Budget

- Efficiency profile: Balanced
- Token budget: Auto
- Token usage observable: Not measured
- Validation/review/closeout reserve: 25%
- Max retries per node: 1
- Local metrics: Off

Allowed profiles are `Economy`, `Balanced`, and `Thorough`. The profile changes optional context,
handoff size, redundancy, and retry-use posture within the explicit numeric ceiling; it never
changes the default or user-selected ceiling or weakens route safety, approval, required security
coverage, or mandatory quality gates. `Token budget` accepts `Auto` or a positive integer; the token
budget and reserve are advisory. `Local metrics` accepts `Off` or `On` and defaults to `Off`. When
runtime usage is unavailable, use `Not measured` and never invent consumption. An explicit reserve
must be an integer from `1%` through `99%`.

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
- Integration mode: Auto
- Designated integrator: Not applicable

All counts are positive-integer ceilings, not required worker counts. `Sequential` ignores the caps
and permits at most one active subagent at a time. Allowed integration modes are:
`Auto`, `Leased writers`, and `Single integrator`.

## Capability Preflight

Perform once per task and repeat only when a material capability change or failure invalidates it.

| Capability | Available or limit | Evidence | Consequence or fallback |
| --- | --- | --- | --- |
| Custom subagents |  |  |  |
| Background execution |  |  |  |
| Background task listing, steering, and stopping |  |  | Required before parallel writer work; otherwise use read-only parallelism or Sequential |
| Tools and permissions |  |  |  |
| Shell execution (`Bash` and/or `PowerShell`) |  |  | Select an available shell; block shell-dependent gates if neither is available |
| Build and test commands |  |  |  |
| Context/token observability |  |  |  |
| Capability-based model/reasoning routing | Inherited or unavailable |  | Never override user/session settings |
| Safe parallel write capacity |  |  |  |

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
- Evidence baseline or revision:
- Delta-first context:
- Compact handoffs:

All roles use this packet as the default handoff. Reopen the wider repository only when the packet
is missing required evidence, relevant files changed, or an agent records why the evidence is
stale. For `Direct`, keep an equivalent transient packet rather than creating this persistent plan.

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

## Dependency Graph And Write Leases

Only schedule nodes whose dependencies are complete. Each writable path may have only one active
lease. Read-only work does not require a lease.

Release a never-active queued node's lease immediately when cancelled. Retain or quarantine an
active writer's lease until stop or finish is confirmed and its last write state is reconciled;
only then release or reassign it. Never integrate stale results.

| Node | Stage | Task | Depends on | Owner | Read scope | Write lease | Spawn value | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | Coder | Example bounded change | None | Unassigned | Relevant files | `path/` | Benefit exceeds coordination cost because… | Ready |

For `Single integrator`, only the designated Coder receives write leases. Other Coders are
read-only analysts and return references or proposed patch descriptions.

## Evidence And Decision Ledger

Check this ledger before rescanning files or rerunning commands. Reuse fresh evidence; if it is
stale or insufficient, record why before replacing it.

Each evidence fingerprint records a stable ID, revision or worktree state, relevant inputs or
hashes, command or method, environment and tool version, timestamp, result digest, and invalidation
condition.

Do not read extra sensitive content solely to calculate a hash.

| ID | Type | Revision/worktree | Inputs or hashes | Command or method | Environment and tool version | Timestamp | Result digest/decision | Invalidation condition | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | Evidence | Revision | Relevant paths/hashes or `Not measured` | Method | Version or environment | Date/time | Concise result | Input or environment changes | Fresh |

Use `Fresh`, `Stale`, or `Invalidated`. Do not copy source or full logs into the ledger.

## Assumption Register

Record only assumptions capable of changing scope, safety, implementation, validation, or
closeout.

| ID | Assumption | Owner | Confidence | Evidence IDs | Material impact | Invalidation condition | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 |  |  |  |  |  |  | Open |

## Change-Impact Test Map

Start with closest tests and expand only for shared behavior, elevated risk, failure, stale
evidence, or a required project gate.

| Changed path/component | Closest tests | Direct dependents | Shared boundary/risk trigger | Broader required gates |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

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

## Failure Classification And Retry Policy

- Profile/user retry limit:
- Current circuit state: Closed
- Circuit opens when: retry limit exhausted; same fingerprinted failure repeats without new
  evidence; or Coder/Tester work oscillates

| Failure ID | Node | Class | Fingerprint/evidence | Changed state or new hypothesis | Retry count | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| FL-1 |  | Implementation defect / Test defect / Flaky result / Environment / Missing dependency/tooling / Pre-existing failure / Permission / Unclear requirement |  |  | 0 |  |

The initial attempt is not a retry. An identical command and fingerprint is not repeated merely in
hope of a different result, except one permitted flaky or transient confirmation within the hard
ceiling. Exhaustion stops the node; a new hypothesis alone does not reset the allowance. Another
attempt requires either a user-raised ceiling or an approved plan revision that creates and
budgets a materially new node.

Classify an unavailable external service as `Environment` unless `Missing dependency/tooling` is
more accurate. Map missing user input to `Unclear requirement` or `Permission` according to the
authority needed.

## Invalidation, Cancellation, And Checkpoints

| Trigger | Dependent nodes/evidence | Invalidation action | Work to cancel or stop | Lease action | Reapproval needed |
| --- | --- | --- | --- | --- | --- |
| Requirement, decision, upstream node, file fingerprint, or environment changes |  |  |  |  |  |

For active work, the lease action must record quarantine, confirmed stop or finish, last-write
reconciliation, and only then release or reassignment.

At each stage boundary, record a compact checkpoint:

- Plan and revision:
- Node statuses:
- Decisions and assumptions:
- Evidence IDs and freshness:
- Lease registry:
- Invalidated or cancelled work:
- Unresolved findings:
- Reserve status:
- Next action:

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
- Stable finding ID namespace: `F-001`
- Deduplication rule: merge the same root cause, impact, and location while preserving evidence
- Adjudication trigger: conflicting material evidence, Low confidence, elevated risk, or required
  independent verification

Typical allocation is one general Reviewer for Low risk, one or two targeted perspectives for
Medium risk, and correctness, security when applicable, and regression perspectives for High risk.
Required perspectives may be combined when caps or runtime capacity require fewer workers, but
must not be silently omitted.

Conditional adjudication never replaces mandatory security coverage.

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

## Early Exit

Optional investigation or redundant confirmation may stop only when:

- every applicable acceptance criterion has fresh implementation, validation, and review evidence
- all mandatory validation and risk-required review are complete
- no material finding, conflict, or invalidated assumption remains
- final confidence is `High`

Early exit never skips approval, security coverage, or a mandatory project gate.

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
- Durable memory updates:
- Memory source and applicable revision/date:
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

Approval applies only to the recorded plan revision. Transitioning that same revision from
`Approved` to `In Progress` retains the approval record. Any material revision clears the approval
record, resets status to `Proposed`, and repeats the approval gate.

## Closeout

- Final status:
- Definition of Done status:
- Validation completed:
- Acceptance criteria traceability complete:
- Review perspectives completed:
- Final confidence:
- Final efficiency profile:
- Final token budget:
- Observed token usage or `Not measured`:
- Validation/review/closeout reserve protected:
- Capability-preflight limitations:
- Spawn decisions:
- Integration mode and designated integrator:
- Retry limit, retries used, and circuit state:
- Requested parallelism caps:
- Worker counts used by stage:
- Actual peak concurrency:
- Execution-mode fallback:
- Impact-selected tests and expansion triggers:
- Evidence fingerprints reused or invalidated:
- Assumptions resolved or remaining:
- Work invalidated or cancelled:
- Commands or scans intentionally rerun:
- Stable Reviewer findings, deduplication, and adjudication:
- Early-exit decision:
- Workflow conformance scenarios run:
- Local metrics requested:
- Outcome-calibration recommendation:
- Metrics recorded locally:
- Durable-memory update and provenance:
- Stage checkpoints updated:
- User findings addressed:
- Residual risks:
- Follow-ups:
