# Implementation Plans

This folder stores Architect-generated implementation plans.

## Purpose

Use this folder for structured plans that describe how approved requirements or user requests will
be implemented.

## Rules

- Architect creates or updates plans here for non-trivial agentic implementation work.
- Architect records `Sequential` or `Parallel`; `Parallel` plans identify independent work,
  dependency boundaries, and non-overlapping ownership.
- Parallel plans record automatic allocation, the global maximum, optional Coder, Tester, and
  Reviewer caps, and planned workers by stage. Counts are ceilings, not targets.
- Classify work as `Trivial`, `Small`, `Medium`, or `Large` and record the resulting `Direct`,
  `Lite`, `Standard`, or `Full` route. Risk may escalate the route but never silently weaken it.
- Record the independent efficiency profile, advisory token budget,
  validation/review/closeout reserve, retry ceiling, and one-time capability-preflight result.
  Defaults are `Balanced`, `Auto`, `25%`, `1`, and current runtime capabilities.
- Treat budget controls as advisory. Reduce optional work or report a constraint; never skip
  approval, mandatory validation, security coverage, or review.
- Use the plan's shared task packet as the bounded handoff for every role.
- Load context delta-first and define when it may expand. Use compact reference-based handoffs and
  stage checkpoints.
- Model dependent work as ready/blocked graph nodes and assign one active write lease per writable
  path. Record invalidation edges, cancellation behavior, and `Leased writers` or
  `Single integrator`.
- Apply the spawn-value gate before optional splits or redundant workers.
- Maintain a fingerprinted evidence and decision ledger plus a stable-ID assumption register to
  prevent duplicate scans and stale conclusions.
- Map changed paths and symbols to impacted tests and dependents, use the progressive validation
  ladder, and trace every acceptance-criteria ID through implementation, validation, and review.
- Record retry ceilings, circuit breakers, and category-specific failure actions.
- Record planned review perspectives, stable canonical finding IDs, conditional adjudication
  triggers, stage confidence, and early-exit conditions.
- Reserve a default 25% of an observable budget for validation, review, and closeout; use
  `Not measured` when usage cannot be observed.
- Orchestrator must ask the user to Approve, Revise, or Stop after Architect finishes a plan.
- Record the plan revision and explicit approval evidence. Approval applies only to that revision.
- Orchestrator moves the approved revision to `In Progress` before the first implementation write.
- Coder writes only under the named active `In Progress` plan and matching approval record.
- Tester and Reviewer use that same active `In Progress` plan. `Done`, `Superseded`, and
  `Abandoned` plans are not executable.
- A material scope or risk revision resets status to `Proposed` and repeats approval.
- If a still-valid plan is temporarily blocked, keep it `In Progress`, record the blocker and
  unblock condition, and mark its Definition of Done `Blocked`. Use `Abandoned` only after an
  explicit stop.
- High-risk plans must include rollback or recovery notes.
- Keep `INDEX.md` updated when useful for navigation.
- Plans are not a substitute for code, tests, or current user instructions.
- After workflow-policy changes, validate applicable behavior against every installed provider's
  workflow-conformance suite.

## Suggested File Names

- `IP-0001-short-title.md`
- `IP-feature-name.md`
- `IP-fix-short-title.md`

Prefer the `IP-0001-short-title.md` pattern for new plans. Keep IDs stable after creation and use
status updates instead of renaming active plans.
