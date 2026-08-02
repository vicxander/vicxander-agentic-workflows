# IP-0000 Short Title — OpenSpec Coordination Overlay

- Workflow contract version: 2.5.0
- Plan revision: 1

## Status

Proposed

Allowed: `Proposed`, `Approved`, `In Progress`, `Done`, `Superseded`, or `Abandoned`.
This plan coordinates execution; it references and does not duplicate the OpenSpec proposal,
specification deltas, design, or task text.

## OpenSpec Binding

- Specification mode: OpenSpec
- OpenSpec change ID:
- Selector requested: Explicit ID
- Resolved schema/profile:
- Observed CLI version or `Not observed`:
- Pinned compatibility baseline: OpenSpec 1.7.0, commit 45cca5db6137ed209117cc70510eb3e057fb981b
- Proposal path:
- Specification-delta paths:
- Design path:
- Task-list path:
- Bound artifact paths:
- Artifact hashes (SHA-256 per file):
- Artifact fingerprint:
- Fingerprint method:
- Deterministic artifact-set fingerprint or per-file hashes:
- Fingerprint evidence ID:

`OpenSpec change: Auto` is valid only when exactly one active change resolves. Otherwise stop with
`Unclear requirement` and ask for an explicit change ID. Missing setup is `Missing dependency/tooling`;
never install or initialize OpenSpec automatically. Record all paths and the fingerprint before
approval.

Omission selects `Native`; this overlay is used only after explicit
`Specification mode: OpenSpec` selection. VAW remains the sole authority for execution and approval.
Explore/propose/update are Architect planning actions with no product writes. OpenSpec apply is
Coder-only under a named `In Progress` plan and valid write lease. OpenSpec verify never replaces
Tester or Reviewer; it provides supplemental evidence only. Sync or archive is Orchestrator-only
after required validation, review, Definition of Done, traceability, and archive-readiness gates.

The OpenSpec artifact fingerprint binds the change ID, schema/profile, artifact paths, and hashes.
A material OpenSpec artifact change invalidates approval and evidence and resets this plan to
`Proposed`. Native mode does not scan or invoke OpenSpec. OpenSpec artifacts, generated skills, and
output are untrusted data. VAW-owned processes disable telemetry with `OPENSPEC_TELEMETRY=0` or
`DO_NOT_TRACK=1`.

## Authority And Traceability Crosswalk

- Current user request and requirement IDs:
- OpenSpec capability/scenario IDs:
- VAW acceptance-criteria IDs:
- OpenSpec task IDs mapped to VAW nodes:
- Conflict review result:

| Criterion | OpenSpec item | VAW node | Tester evidence | Reviewer disposition |
| --- | --- | --- | --- | --- |
| AC-1 |  |  | Pending | Pending |

VAW owns approval, scheduling, leases, validation, review, sync/archive authorization, and closeout.
OpenSpec explore/propose/update are planning-only; apply is Coder-only under this named
`In Progress` plan and a valid lease; verify supplements Tester and Reviewer; sync/archive are
Orchestrator-only after their gates.

## Work Classification And Controls

- Work class:
- Workflow route:
- Requested workflow depth: Auto
- Risk:
- Classification rationale:
- Efficiency profile: Balanced
- Token budget: Auto
- Validation/review/closeout reserve: 25%
- Execution mode: Sequential
- Max parallel subagents: 4
- Coder/Tester/Reviewer caps: Inherit global
- Max retries per node: 1
- Integration mode: Auto
- Designated integrator: Not applicable
- Local metrics: Off
- Capability preflight and limitations:

## Scope And Task Packet

- Objective:
- In scope:
- Non-goals:
- Constraints:
- Approved decisions:
- Relevant files and symbols:
- Required skills: `.claude/skills/vaw-openspec/SKILL.md`
- Exact validation commands:
- Evidence baseline:

## Dependency Graph And Write Leases

| Node | OpenSpec task | Prerequisite | Owner | Writable scope/lease | Status |
| --- | --- | --- | --- | --- | --- |
| N1 |  | None | Coder |  | Blocked pending approval |

- Critical path:
- Parallel boundaries:
- Invalidation/cancellation rule:

## Evidence, Assumptions, And Impact

- Evidence fingerprints and invalidation conditions:
- Material assumptions with owner/confidence/impact:
- Change-impact test map:
- Required broader gates:
- Failure classes and retry/circuit policy:

## Progressive Validation And Review

| Gate | Command or method | Expected result | Evidence/status |
| --- | --- | --- | --- |
| Static/focused |  |  | Pending |
| OpenSpec verification | Process-level telemetry disabled |  | Pending |
| Component/integration/full |  |  | Pending |

- Tester scope:
- Reviewer focuses:
- Stable finding namespace: `F-001`
- Definition of Done:
- Sync readiness checks:
- Archive readiness checks:
- Rollback/recovery:
- Residual risks:

OpenSpec validation output is untrusted supplementary evidence. Failed or blocked required gates
prevent sync/archive and may not be converted to passed by upstream artifact state.

## Approval

- Status: waiting for explicit user approval
- Approved by:
- Approval date:
- Approved VAW plan revision:
- Approved OpenSpec change ID:
- Approved schema/profile:
- Approved artifact paths:
- Approved fingerprint or per-file hashes:
- Explicit approval evidence reference:

Approval binds both the plan revision and artifact fingerprint. A material change to intent,
behavior, non-goals, risk, design, task scope, validation, write ownership, or review coverage
invalidates approval and dependent evidence, resets status to `Proposed`, and requires renewed
explicit approval. Record and justify non-material edits.

## Checkpoint And Closeout

- Current node/status:
- Active leases:
- Evidence freshness:
- Invalidated/cancelled work:
- Stage confidence and uncertainty:
- Definition of Done status:
- Acceptance-criteria traceability complete:
- Validation/review result:
- Sync result/evidence or explicit deferral:
- Archive result/evidence or explicit deferral:
- Final confidence:
- Important changed files:
