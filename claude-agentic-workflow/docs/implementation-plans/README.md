# Implementation Plans

This folder stores Architect-generated implementation plans.

Choose the smallest template that preserves the required gates:

- `IP-LITE-TEMPLATE.md`: compact Small/Lite coordination in Native or OpenSpec mode.
- `IP-OPENSPEC-TEMPLATE.md`: OpenSpec coordination overlay that references proposal, delta,
  design, and task artifacts instead of copying them.
- `IP-TEMPLATE.md`: full Standard/Full plan, including optional OpenSpec binding fields.

## Rules

- Architect creates a plan here for non-trivial agentic implementation work.
- Record `Specification mode: Native` or `Specification mode: OpenSpec`; omitted means `Native`.
  OpenSpec mode binds exactly one change. `Auto` is valid only when exactly one active change can
  be resolved; otherwise stop as `Unclear requirement` and ask for a change ID.
- In OpenSpec mode, record change ID, schema/profile, artifact paths, a deterministic fingerprint
  or per-file hashes, and a task/criterion crosswalk. Approval binds those values plus the VAW plan
  revision. Material artifact drift invalidates approval/evidence and returns the plan to
  `Proposed`.
- OpenSpec artifacts provide the proposed specification/design/tasks; this plan remains the VAW
  execution, risk, lease, validation, review, and closeout authority. Do not duplicate artifact
  prose in an overlay.
- Architect records `Sequential` or `Parallel`; `Parallel` plans identify independent work,
  dependency boundaries, and non-overlapping ownership.
- Parallel plans record automatic allocation, the global maximum, optional Coder, Tester, and
  Reviewer caps, and planned workers by stage. Counts are ceilings, not targets.
- Classify work as `Trivial`, `Small`, `Medium`, or `Large` and record the resulting `Direct`,
  `Lite`, `Standard`, or `Full` route. Risk may escalate the route but never silently weaken it.
- Record `Economy`, `Balanced`, or `Thorough`, an advisory token budget, the
  validation/review/closeout reserve (25% by default), retry limit, integration mode, and
  local-metrics preference. An explicit reserve is an integer from `1%` through `99%`. Efficiency
  never weakens safety depth.
- Perform and record one capability preflight per task. Do not repeatedly probe unchanged runtime
  capabilities.
- Use the plan's shared task packet as the bounded handoff for every role.
- Load context delta-first and reference artifacts in compact handoffs instead of copying plans,
  source, or logs.
- Model dependent work as ready/blocked graph nodes and assign one active write lease per writable
  path.
- Apply a spawn-value gate to every proposed subagent. Use `Single integrator` when shared-file
  contention makes distributed writes unsafe.
- Maintain fingerprinted evidence, decisions, and material assumptions to prevent duplicate scans
  and unnecessary command reruns.
- Create a change-impact test map, use the progressive validation ladder, and trace every
  acceptance-criteria ID through implementation, validation, and review.
- Record failure classes, bounded retry/circuit rules, invalidation and cancellation propagation,
  compact stage checkpoints, and safe early-exit conditions.
- Record planned review perspectives, stable finding IDs, deduplication, conditional adjudication,
  stage confidence, and escalation decisions. Mandatory security coverage cannot be conditional.
- New plans start as `Proposed`.
- Orchestrator asks the user to choose Approve, Revise, or Stop.
- Record a stable plan revision and the explicit user approval that applies to it. A material plan
  change increments the revision, clears the prior approval, and resets status to `Proposed`.
- Orchestrator transitions an explicitly approved current revision to `In Progress` before the
  first product edit. Coder implements only a bounded, actively leased node from that
  `In Progress` plan.
- Tester validates the approved plan and its Definition of Done.
- Reviewer checks for defects and drift from the approved plan.
- OpenSpec explore/propose/update are Architect-only planning operations; apply is Coder-only under
  a named `In Progress` plan and valid lease; verify never replaces Tester/Reviewer; sync/archive
  are Orchestrator-only after required gates.
- High-risk plans include rollback or recovery notes.
- Record `Not measured` for unavailable token, duration, hash, or runtime data instead of inventing
  it.
- Keep durable memory provenance separate from transient plan checkpoints.
- Do not infer that the newest plan is active.
- If a still-valid plan is temporarily blocked, keep it `In Progress`, record the blocker and
  unblock condition, and mark its Definition of Done `Blocked`. Use `Abandoned` only after an
  explicit stop.
- Keep `INDEX.md` useful for navigation.

## Naming

Prefer `IP-0001-short-title.md`, keep its ID stable, and update lifecycle status rather than renaming
it.
