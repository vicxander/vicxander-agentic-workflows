# Implementation Plans

This folder stores Architect-generated implementation plans.

## Rules

- Architect creates a plan here for non-trivial agentic implementation work.
- Architect records `Sequential` or `Parallel`; `Parallel` plans identify independent work,
  dependency boundaries, and non-overlapping ownership.
- Parallel plans record automatic allocation, the global maximum, optional Coder, Tester, and
  Reviewer caps, and planned workers by stage. Counts are ceilings, not targets.
- Classify work as `Trivial`, `Small`, `Medium`, or `Large` and record the resulting `Direct`,
  `Lite`, `Standard`, or `Full` route. Risk may escalate the route but never silently weaken it.
- Record the independent `Economy`, `Balanced`, or `Thorough` efficiency profile, advisory token
  budget, validation/review/closeout reserve, retry limit, integration mode, and local-metrics
  choice. Default to `Balanced`, `Auto`, 25%, one retry per node, `Auto`, and `Off`. The reserve is
  an integer from `1%` through `99%`. Integration modes are `Auto`, `Leased writers`, and
  `Single integrator`. These settings never weaken mandatory safety gates.
- Run one runtime capability preflight and record safe fallbacks. Inherit model and reasoning
  settings; describe capability needs without hardcoded model IDs.
- Use the plan's shared task packet as the bounded handoff for every role.
- Begin from a delta-first impact map of files, symbols, nearby tests, direct dependencies,
  components, and required gates. Expand only for a recorded trigger.
- Keep handoffs reference-based and compact, and create a checkpoint at every stage boundary.
- Record only material assumptions, each with an ID, owner, confidence, evidence, impact,
  invalidation condition, and status.
- Model dependent work as ready/blocked graph nodes and assign one active write lease per writable
  path.
- Apply the spawn-value gate before optional delegation. For high-contention edits, plan one
  writing integrator while other Coders provide read-only analysis or proposed patches.
- Fingerprint ledger evidence with a stable ID, repository revision, relevant inputs or hashes
  when available, exact command or method, environment details and tool version, timestamp,
  concise result digest, and invalidation condition.
- Propagate changed inputs through evidence and node dependencies, cancel obsolete queued work, and
  release its leases.
- Select impact-based tests and broaden through the progressive validation ladder only as risk,
  shared behavior, failure, uncertainty, or project gates require.
- Classify failures, require a changed hypothesis before retry, enforce retry budgets, and open a
  circuit instead of looping.
- Trace every acceptance-criteria ID through implementation, validation, and review.
- Record planned review perspectives, stable finding IDs, duplicate merging, conditional
  adjudication, stage confidence, and escalation decisions. Never omit required security coverage.
- State early-exit conditions so agents stop once criteria, mandatory checks, review, freshness, and
  High confidence are satisfied.
- Use optional local outcome metrics to propose calibration only from comparable evidence; never
  auto-weaken safety or override user settings.
- When a task changes workflow behavior, name and run or dry-run affected scenarios from every
  installed provider's workflow-conformance suite.
- New plans start as `Proposed`.
- Give every plan a stable revision. Material scope, risk, acceptance-criteria, dependency-node,
  write-ownership, required-validation, or review-coverage changes increment it and clear approval.
- Orchestrator asks the user to choose Approve, Revise, or Stop.
- Explicit approval moves a plan to `Approved`; Orchestrator records approval evidence and the
  approved revision, then moves that same revision to `In Progress` before the first implementation
  write.
- Coder may accept a startup handoff for a named active `Approved` plan, but writes only after
  Orchestrator moves it to `In Progress`. Later nodes and rework continue only while the same
  recorded approval matches the same revision. Material scope or risk drift increments the
  revision and returns it to `Proposed` for renewed approval.
- Tester validates the named active `In Progress` plan and its Definition of Done.
- Reviewer checks for defects and drift from the named active `In Progress` plan.
- If a still-valid plan is temporarily blocked, keep it `In Progress`, record the blocker and
  unblock condition, and mark its Definition of Done `Blocked`. Use `Abandoned` only after an
  explicit stop.
- High-risk plans include rollback or recovery notes.
- Do not infer that the newest plan is active.
- Keep `INDEX.md` useful for navigation.

## Naming

Prefer `IP-0001-short-title.md`, keep its ID stable, and update its lifecycle status instead of
renaming it.
