# IP-0000 Short Title

- Workflow contract version: 2.6.0

## Status

Proposed

Allowed statuses:

- Proposed
- Approved
- In Progress
- Done
- Superseded
- Abandoned

- Plan revision: 1

Increment the plan revision for every material change to scope, risk, acceptance criteria,
dependency-node scope, write ownership, required validation, or review coverage. Normal lifecycle,
evidence, approval-metadata, and closeout updates do not increment it. A material revision resets
status to `Proposed` and requires explicit user approval again.
If the workflow contract changes while this plan is `In Progress`, continue under its recorded
compatible version unless a material migration is reviewed and explicitly accepted.

## Risk Level

Low

Allowed risk levels:

- Low
- Medium
- High

High-risk plans require rollback or recovery notes.

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

## Efficiency And Budget Controls

- Efficiency profile: Balanced
- Token budget: Auto
- Token usage observable: Not measured
- Validation/review/closeout reserve: 25%
- Max retries per node: 1
- Local metrics: Off
- Optional work to stop first if budget tight:

Allowed efficiency profiles are `Economy`, `Balanced`, and `Thorough`. They tune optional context,
corroboration, checkpoint detail, and retry posture within the explicit ceiling but never reduce
the selected route, approval gate, mandatory validation, security coverage, or review.
`Token budget` is `Auto` or a positive integer and remains advisory. Use `Not measured` when the
runtime cannot observe usage.
`Validation/review/closeout reserve` must be an integer from `1%` through `99%`.
`Local metrics` accepts `Off` or `On` and defaults to `Off`.

`Max retries per node` is a non-negative integer and defaults to `1` retry after the initial
attempt; `0` disables retries. A retry is never required, and efficiency profiles do not silently
raise the hard ceiling. An unchanged failing action must not be repeated. Exhaustion stops the node;
a new hypothesis alone does not reset its allowance. Another attempt requires either a user-raised
ceiling or an approved plan revision that creates and budgets a materially new node.

## Runtime Capability Preflight

Run once at intake and recheck only a capability that changes or fails unexpectedly.

| Capability | Available or value | Limitation or fallback |
| --- | --- | --- |
| Custom agents |  |  |
| Concurrent workers |  |  |
| Tools and permissions |  |  |
| Version control and diff |  |  |
| Build and validation commands |  |  |
| Token observability |  |  |
| Model or reasoning controls |  |  |

Never hardcode model IDs or override explicit user settings. Route stronger reasoning only when the
runtime supports it and architecture, security, ambiguity, or conflicting evidence warrants it.

## Execution Mode

Sequential

Allowed modes:

- Sequential
- Parallel

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
- Spawn-value gate decisions:

All counts are positive-integer ceilings, not required worker counts. `Sequential` ignores the caps
and permits at most one active subagent at a time. Every optional worker must provide more expected
critical-path or specialist value than its handoff, context, coordination, lease, and merge cost.

## Integration Mode

- Integration mode: Auto
- Planned: To be selected after contention assessment
- Designated integrator:
- Selection rationale:

Allowed values are `Auto`, `Leased writers`, and `Single integrator`. Leased writers may edit only
disjoint scopes covered by exclusive leases. Use one integrator when writable scopes overlap,
changes are mechanically coupled, merge cost is high, or isolation is unreliable. Other Coders
remain read-only and return proposals.

## Source Inputs

- User request:
- Requirements:
- User findings:
- Relevant skills:

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
- Context seed:
- Authorized context-expansion conditions:
- Early-exit conditions:

All roles use this packet as the default handoff. Reopen the wider repository only when the packet
is missing required evidence, relevant files changed, or an agent records why the evidence is
stale. Handoffs reference packet, node, criterion, evidence, decision, assumption, finding, and
lease IDs instead of copying plans, prompts, source, or raw logs.

## Delta-First Context And Reference-Based Handoffs

1. Start with the task packet or latest checkpoint.
2. Inspect the current diff, changed paths, and user-named files or symbols.
3. Read the closest tests and direct dependents.
4. Expand to an affected component or wider repository only for a recorded risk, failure, evidence
   gap, or uncertainty.

- Planned context boundaries:
- Expansion trigger and decision ID:
- Handoff size or compaction constraint:

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

## Dependency Graph, Invalidation, And Write Leases

Only schedule nodes whose dependencies are complete. Each writable path may have only one active
lease. Read-only work does not require a lease. Record invalidation edges so an upstream change can
mark dependent work stale and cancel obsolete queued or active nodes safely.

Release a never-active queued node's lease immediately when cancelled. Retain or quarantine an
active writer's lease until stop or finish is confirmed and its last write state is reconciled;
only then release or reassign it. Never integrate stale results.

| Node | Stage | Task | Depends on | Invalidates on change | Owner | Read scope | Write lease | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | Coder | Example bounded change | None | AC-1, D1, input paths | Unassigned | Relevant files | `path/` | Ready |

## Fingerprinted Evidence And Decision Ledger

Check this ledger before rescanning files or rerunning commands. Reuse fresh evidence; if it is
stale or insufficient, record why before replacing it.

Do not read extra sensitive content solely to calculate a hash.

| ID | Type | Result digest or decision digest | Revision | File inputs or hashes | Command or method | Environment and tool version | Timestamp | Owner | Invalidation condition | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | Evidence | Concise result digest |  |  |  |  |  | Unassigned | Input, decision, or environment change | Fresh |
| D1 | Decision | Concise decision digest |  | Not applicable | User or plan approval |  |  | Unassigned | Superseding decision | Active |

## Assumption Register

Investigate only assumptions capable of changing scope, correctness, risk, or validation. A
Low-confidence material assumption blocks advancement.

| ID | Assumption | Owner | Confidence | Evidence IDs | Impact if wrong | Invalidation condition | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 |  |  |  |  |  |  | Open |

## Change-Impact Map

Use this map to select the smallest sufficient validation set, then broaden for shared interfaces,
elevated risk, failure diagnosis, uncertain impact, or mandatory project gates.

| Changed path or symbol | Direct dependents | Criteria | Closest tests | Broader gates and trigger |
| --- | --- | --- | --- | --- |
|  |  | AC-1 |  |  |

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

## Retry Circuit Breakers And Failure Actions

- Retry counter unit: Dependency node
- Circuit opens when:
- Re-entry requires:

| Failure class | Planned response | Retry eligible | Evidence ID or status |
| --- | --- | --- | --- |
| Implementation defect | Return bounded node to Coder and invalidate dependent checks | After correction |  |
| Test defect | Correct within scope or revise plan before changing test intent | After correction |  |
| Flaky result | Retain all outcomes and retry only with evidence of transience | Within ceiling |  |
| Environment | Diagnose without product-code churn; approved workaround or Blocked | Only after state change |  |
| Missing dependency/tooling | Seek approval; do not install or add silently | Only after state change |  |
| Pre-existing failure | Establish baseline and isolate change impact | Diagnostic only |  |
| Permission | Request necessary access or mark Blocked | Only after access change |  |
| Unclear requirement | Clarify or revise plan before implementation | No |  |

Classify an unavailable external service as `Environment` unless `Missing dependency/tooling` is
more accurate. Map missing user input to `Unclear requirement` or `Permission` according to the
authority needed.

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

Typical allocation is one general Reviewer for Low risk, one or two targeted perspectives for
Medium risk, and correctness, security when applicable, and regression perspectives for High risk.
Required perspectives may be combined when caps or runtime capacity require fewer workers, but
must not be silently omitted.

## Canonical Findings And Adjudication

Reviewer deduplication uses stable finding IDs in the `F-*` form. Merge reports with the same root
cause and affected scope into one canonical finding with linked perspectives and evidence.

| Finding ID | Severity | Root cause and scope | Reporter perspectives | Evidence IDs | Disposition |
| --- | --- | --- | --- | --- | --- |
| F1 |  |  |  |  | Open |

- Adjudication trigger: None
- Adjudicator:
- Adjudication result:

Invoke adjudication only for a material evidence conflict, Low confidence, elevated risk, or
required independent verification. Security-sensitive work still requires explicit Security
coverage even when no adjudicator is needed.

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

## Stage Checkpoints And Compact Handoffs

At each stage boundary, record only references and current state.

| Checkpoint | Packet and repository revision | Criteria and node state | Leases and cancellations | Fresh evidence, assumptions, and findings | Confidence | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| CP1 |  |  |  |  |  |  |

Do not copy plans, prompts, source content, secrets, personal data, or raw logs into checkpoints or
handoffs.

## Durable Memory Candidates

Create an entry only for a reusable project fact or decision.

| Memory ID | Fact or decision | Source | Scope | Confidence | Last-confirmed revision or date | Expiry or invalidation condition |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

Expired or invalidated entries are hypotheses until current evidence reconfirms them.

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
- Relevant security skills:

## Approval

- Status: waiting for user approval.
- Approved by:
- Approval date:
- Approved plan revision:
- Explicit approval evidence reference:

Approval applies only to the recorded plan revision. Orchestrator changes that same revision from
`Approved` to `In Progress` before the first implementation write without clearing the approval
record. A material revision clears approval, resets status to `Proposed`, and repeats the gate.

## Closeout

- Final status:
- Definition of Done status:
- Validation completed:
- Acceptance criteria traceability complete:
- Review perspectives completed:
- Final confidence:
- Efficiency profile:
- Token budget and observed usage:
- Validation/review/closeout reserve disposition:
- Retry ceiling, retries used, and circuits opened:
- Requested parallelism caps:
- Worker counts used by stage:
- Actual peak concurrency:
- Execution-mode fallback:
- Requested and actual integration mode:
- Designated integrator:
- Spawn-value decisions:
- Evidence reused or invalidated:
- Context expansion boundaries:
- Stage checkpoints:
- Assumptions resolved or left open:
- Work invalidated or cancelled:
- Commands or scans intentionally rerun:
- Failure classifications:
- Change-impact coverage:
- Reviewer findings requiring rework:
- Duplicate findings merged:
- Adjudication:
- Early-exit status:
- Local metrics requested:
- Metrics recorded locally:
- Local calibration recommendation:
- Durable memory updates and freshness:
- Applicable installed provider workflow-conformance scenarios run for workflow-policy changes:
- User findings addressed:
- Residual risks:
- Follow-ups:
