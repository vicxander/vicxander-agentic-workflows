# IP-0000 Short Title — Lite

- Workflow contract version: 2.5.0
- Plan revision: 1

## Status

Proposed

Allowed: `Proposed`, `Approved`, `In Progress`, `Done`, `Superseded`, or `Abandoned`.
Every material revision increments the revision, invalidates and clears approval, resets the plan
to `Proposed`, and requires explicit user approval again.

## Specification Mode

- Specification mode: Native
- OpenSpec change: Not applicable
- OpenSpec schema/profile: Not applicable
- OpenSpec artifact paths: Not applicable
- OpenSpec fingerprint or per-file hashes: Not applicable

Allowed modes are `Native` and `OpenSpec`; omitted means `Native`. In OpenSpec mode, use one named
change (`Auto` only when exactly one active change resolves) and complete every binding field before
approval.

## Work Classification

- Work class: Small
- Workflow route: Lite
- Requested workflow depth: Auto
- Risk: Low
- Classification rationale:

## Acceptance Criteria And Compact Task Packet

- Task-packet revision: 1
- Objective:
- Acceptance criteria IDs:
- Scope and relevant paths:
- Constraints and non-goals:
- Approved decisions:
- Required skills:
- Exact validation commands:

## Efficiency And Budget

- Efficiency profile: Balanced
- Token budget: Auto
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
- Capability limitations:
- Write ownership: one active write lease per writable path

## Changes, Ownership, And Evidence

| Node | Change | Prerequisite | Writable lease | Acceptance criteria | Evidence |
| --- | --- | --- | --- | --- | --- |
| N1 |  | None |  |  | Pending |

- Material assumptions:
- Risk and mitigation:
- Rollback/recovery: Not applicable for Low risk unless repository evidence requires it
- Change-impact expansion trigger:

## Validation And Review

| Level | Command or method | Expected result | Status/evidence |
| --- | --- | --- | --- |
| Static/focused |  |  | Pending |

- Tester coverage:
- Reviewer focus: General
- Reviewer disposition:
- OpenSpec verify evidence: Not applicable
- Sync/archive readiness: Not applicable until every required gate passes
- Definition of Done: implementation complete; focused validation passed; changed files reported

## Approval

- Status: waiting for explicit user approval
- Approved by:
- Approval date:
- Approved plan revision:
- Explicit approval evidence reference:
- Approved OpenSpec change/fingerprint: Not applicable

Approval binds this revision and, in OpenSpec mode, the exact artifact fingerprint. Material drift
returns the plan to `Proposed`. OpenSpec apply is Coder-only under `In Progress` plus a valid lease;
verify never replaces Tester/Reviewer; sync/archive remain Orchestrator-only after their gates.

## Closeout

- Final status:
- Definition of Done status:
- Validation and review evidence:
- Acceptance-criteria traceability:
- Final confidence:
- Residual risks or blockers:
- OpenSpec sync/archive result or deferral:
- Important changed files:
