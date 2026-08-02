# IP-0000 Short Title

- Workflow contract version: 2.5.0
- Plan revision: 1
- Status: Proposed

## Work Classification

- Work class: Small
- Workflow route: Lite
- Requested workflow depth: Auto
- Risk: Low

## Specification Mode

- Specification mode: Native
- OpenSpec change: Not applicable

`Specification mode` accepts `Native` or `OpenSpec` and defaults to `Native`. If OpenSpec is used,
replace this template with `IP-OPENSPEC-TEMPLATE.md` unless the change is demonstrably Small and
all OpenSpec binding fields are added without weakening any gate.

## Efficiency And Budget Controls

- Efficiency profile: Balanced
- Token budget: Auto
- Token usage observable: Not measured
- Validation/review/closeout reserve: 25%
- Max retries per node: 1
- Local metrics: Off

## Execution Mode

- Execution mode: Sequential
- Max parallel subagents: 4
- Coder max: Inherit global
- Tester max: Inherit global
- Reviewer max: Inherit global
- Integration mode: Auto

Parallel work still obeys stage order and non-overlapping leases. Counts are ceilings, not targets.

## Objective And Scope

- Objective:
- In scope:
- Non-goals:
- Relevant requirements or findings:
- Applicable skills:

## Acceptance Criteria

- `AC-1`:

## Task Packet And Ownership

- Task-packet revision: 1
- Evidence baseline or repository revision:
- Context seed:
- Coder write lease:
- Exact validation commands:
- Reviewer focus: General
- Early-exit conditions:

| Node | Stage | Task | Depends on | Owner | Write lease | Status |
| --- | --- | --- | --- | --- | --- | --- |
| N1 | Coder |  | None | Unassigned |  | Ready |
| N2 | Tester | Validate `AC-1` | N1 | Unassigned | Read only | Blocked |
| N3 | Reviewer | Review `AC-1` | N2 | Unassigned | Read only | Blocked |

## Evidence, Assumptions, And Impact

| ID | Type | Digest | Inputs or hashes | Method | Invalidation condition | Status |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | Evidence |  |  |  | Relevant input changes | Fresh |

| ID | Assumption | Confidence | Impact if wrong | Invalidation condition | Status |
| --- | --- | --- | --- | --- | --- |
| A1 |  |  |  |  | Open |

| Changed path or symbol | Direct dependents | Criterion | Focused check | Broader trigger |
| --- | --- | --- | --- | --- |
|  |  | AC-1 |  | Shared behavior, risk, or failure |

## Validation And Review

| Level | Check | Required | Status | Evidence |
| --- | --- | --- | --- | --- |
| V1 | Format/static | Yes | Pending |  |
| V2 | Focused tests | Yes | Pending |  |
| V3+ | Broader gates | When impact or risk requires | Pending |  |

| Criterion | Implementation evidence | Validation evidence | Reviewer disposition |
| --- | --- | --- | --- |
| AC-1 |  |  | Pending |

- Retry circuit opens when:
- Failure actions:
- Canonical findings:
- Confidence or unresolved uncertainty:

## Approval

- Status: waiting for user approval
- Approved by:
- Approval date:
- Approved plan revision:
- Explicit approval evidence reference:

Coder starts only after Orchestrator records explicit approval for this revision and changes it to
`In Progress`. A material scope, risk, criterion, ownership, validation, or review change increments
the revision, clears approval, and returns status to `Proposed`.

## Definition Of Done And Closeout

- Scoped implementation complete.
- Focused validation complete or honestly blocked.
- Reviewer disposition recorded for every criterion.
- Changed files and residual risk reported.
- Final status:
- Final confidence:
- Validation evidence:
- Reviewer findings:
- Retries or circuits:
- Actual execution/integration mode and worker counts:
- Metrics recorded locally: No unless `Local metrics: On`
