# Workflow Metrics

This optional, user-visible Markdown log stores repository-local operational metadata that can help
improve workflow speed and reliability. It is not telemetry: these instructions define no
uploader, backend, author-operated collection, or automatic export. GitHub Copilot may process this
project file as repository context under GitHub's terms, settings, and organization controls.

## Privacy Rules

- Record counts, statuses, durations, and workflow decisions only.
- `Local metrics: Off` is the default. Append an entry only when the user selects `On`.
- Never record prompts, source code, file contents, secrets, credentials, personal data, raw logs,
  or external service payloads.
- Use `Not measured` when the runtime cannot observe a metric; never invent a value.
- The user may edit, delete, ignore, or decline to update this file at any time.
- Do not intentionally publish or export this file beyond normal provider processing under the
  user's account and organization settings unless the user explicitly requests that action.
- Record only results for the current repository. Do not use cross-repository identifiers or
  attempt to profile people.
- Calibration may compare compatible entries, but it must never automatically weaken safety gates
  or override user preferences.
- Read at most the latest 20 comparable entries for routine calibration. Keep older entries out of
  active context. Compact or archive them only with the user's approval, preserve metadata-only
  aggregates when useful, and never silently delete history.

## Entry Template

### YYYY-MM-DD — Plan Or Task ID

- Work class:
- Specification mode:
- OpenSpec change ID: Not applicable
- OpenSpec artifact fingerprint/evidence ID: Not applicable
- OpenSpec schema/profile and CLI version: Not applicable
- OpenSpec artifact invalidation reason: None
- OpenSpec sync/archive state: Not applicable
- OpenSpec third-party telemetry disabled: Not applicable
- Local metrics: On
- Workflow route:
- Requested workflow depth:
- Risk:
- Efficiency profile:
- Token budget:
- Token usage: Not measured
- Validation/review/closeout reserve:
- Reserve respected: Not measured
- Max retries per node:
- Requested execution mode:
- Actual execution mode:
- Requested global and role caps:
- Workers used by stage:
- Actual peak concurrency:
- Optional workers considered:
- Optional workers rejected by spawn-value gate:
- Integration mode:
- Actual integration mode:
- Capability preflight limitations:
- Stage durations:
- Stage checkpoints created:
- Initial impact-set size:
- Context expansions and reasons:
- Evidence entries reused:
- Evidence entries invalidated:
- Duplicate scans avoided:
- Commands intentionally rerun:
- Retry count:
- Circuit-breaker events:
- Failure classifications:
- Obsolete nodes cancelled:
- Avoidable test reruns:
- Validation/review/closeout reserve consumed: Not measured
- Reviewer findings requiring rework:
- Duplicate Reviewer findings merged:
- Conditional adjudications:
- Validation level reached:
- Execution-mode fallback:
- Early-exit condition reached:
- Final outcome:
- Final confidence:

Never store OpenSpec artifact bodies, prompts, paths, identifiers, generated instructions, CLI raw
logs, or remote payloads in metrics. These optional fields are metadata only.

## Calibration Record Template

Use only after enough comparable entries exist. Keep conclusions provisional and validate proposed
contract changes against `.github/WORKFLOW-CONFORMANCE.md`.

### YYYY-MM-DD — Calibration ID

- Comparable task cohort:
- Entry count:
- Over-routing signal:
- Avoidable context-expansion signal:
- Low-value spawn signal:
- Retry or rerun signal:
- Validation/review/closeout reserve signal:
- Reviewer rework signal:
- Proposed heuristic change:
- Safety gates unchanged:
- User preferences unchanged:
- Conformance scenarios to rerun:
- Decision: Proposed, Accepted, Rejected, or Not enough evidence

## Entries

No workflow runs recorded.
