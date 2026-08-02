# IP-0000 Short Title

## Status

Proposed

## Plan Metadata

- Plan revision: 1
- Task-packet revision: 1
- Workflow contract version: 2.5.0
- Source request:
- Risk: Low

## Work Classification

- Work class: Small
- Workflow route: Lite
- Requested workflow depth: Auto
- Classification rationale:

## Specification Mode

- Specification mode: Native
- OpenSpec change ID: Not applicable
- OpenSpec artifact fingerprint: Not applicable

## Resource-Efficiency Controls

- Efficiency profile: Balanced
- Token budget: Auto
- Validation/review/closeout reserve: 25%
- Max retries per node: 1
- Integration mode: Auto
- Local metrics: Off

## Execution Mode

Sequential

- Max parallel subagents: 4
- Coder max: Inherit global
- Tester max: Inherit global
- Reviewer max: Inherit global
- Planned workers by stage: One per required Lite stage
- Ownership boundaries:
- Sequential fallback condition:

## Objective And Scope

- Objective:
- In scope:
- Non-goals:
- Constraints:
- Required skills:

## Acceptance Criteria And Impact

| ID | Criterion | Files or symbols | Focused validation | Reviewer disposition |
| --- | --- | --- | --- | --- |
| AC-1 |  |  |  | Pending |

## OpenSpec Binding (Only When Selected)

- Resolved schema/profile:
- Proposal path:
- Specification-delta paths:
- Design path:
- Task path:
- Artifact-set fingerprint or per-file hashes:
- Observed OpenSpec CLI version: Not observed
- Task/criterion crosswalk:
- Material-change invalidation condition:

Reference these artifacts; do not duplicate their proposal, design, specification, or task bodies.
`OpenSpec change: Auto` is valid only when exactly one active change resolves. A material artifact
change clears approval and dependent evidence, increments this plan revision, and returns the plan
to `Proposed`.

## Implementation And Ownership

| Node | Task | Depends on | Owner | Write lease | Status |
| --- | --- | --- | --- | --- | --- |
| N1 |  | None | Coder |  | Ready after approval |

## Validation And Review

- Exact focused commands or methods:
- Required OpenSpec validation: Not applicable
- Tester evidence:
- Reviewer focus: General
- Failure classification and retry ceiling: Canonical matrix; 1 retry per node
- Definition of Done: Scoped implementation, focused validation, one general review, changed files reported

## Approval Binding

- Approved by:
- Approval date:
- Approved plan revision:
- Explicit approval evidence reference:
- Approved OpenSpec change ID: Not applicable
- Approved artifact fingerprint: Not applicable
- Implementation started:

Only explicit user approval authorizes Orchestrator to move this same revision to `In Progress`.
Coder writes only under that named active plan and a valid lease. OpenSpec apply cannot bypass this
gate; verify cannot replace Tester or Reviewer; sync/archive remains Orchestrator-only after
Definition of Done.

## Closeout

- Final status:
- Validation result:
- Final confidence:
- Sync/archive state: Not applicable
- Residual risks and follow-ups:
