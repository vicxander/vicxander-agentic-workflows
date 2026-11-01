# Workflow Metrics

This optional, user-visible Markdown log stores repository-local operational metadata that can help
improve workflow speed and reliability. It is not author-operated telemetry. The workflow contains
no uploader, automatic export, or author-operated collection service. target tool and enabled tools
may process this project file under their own policies when it is in context.

## Privacy Rules

- Record counts, statuses, durations, and workflow decisions only.
- Never record prompts, source code, file contents, secrets, credentials, personal data, raw logs,
  or external service payloads.
- Use `Not measured` when the runtime cannot observe a metric; never invent a value.
- The user may edit, delete, ignore, or decline to update this file at any time.
- Do not send this file or its contents to an external service unless the user explicitly requests
  that action.
- `Local metrics: Off` is the default. Append an entry only when the user selects `On`.

## Calibration Rules

- Consult at most the latest 20 comparable entries needed to identify routing and efficiency
  patterns. Keep older entries out of active context. Compact or archive them only with the user's
  approval, preserve metadata-only aggregates when useful, and never silently delete history.
- Look for over-routing, spawn overhead, duplicate scans, stale evidence misses, avoidable test
  reruns, retry loops, circuit-breaker activations, Reviewer rework, and escaped validation.
- Tune optional context expansion, worker allocation, retry-use posture within the configured hard
  ceiling, and impact-map heuristics only. Never change the numeric retry default or a user-selected
  ceiling.
- Never change user-selected settings, lower task risk, bypass approval, omit required security
  coverage, or weaken a mandatory quality gate.
- Keep every field aggregate or metadata-only. Do not add paths if their names are sensitive.

## Entry Template

### YYYY-MM-DD — Plan Or Task ID

- Work class:
- Local metrics: On
- Workflow route:
- Requested workflow depth:
- Risk:
- Efficiency profile:
- Token budget:
- Observed token usage:
- Validation/review/closeout reserve:
- Reserve protected:
- Requested execution mode:
- Actual execution mode:
- Requested global and role caps:
- Workers used by stage:
- Actual peak concurrency:
- Capability limitations:
- Spawn candidates accepted/rejected:
- Integration mode:
- Single integrator used:
- Retry limit:
- Retries used:
- Circuit breakers opened:
- Stage durations:
- Evidence entries reused:
- Evidence entries invalidated:
- Duplicate scans avoided:
- Commands intentionally rerun:
- Avoidable test reruns:
- Impact-selected test groups:
- Validation expansions:
- Reviewer findings requiring rework:
- Duplicate Reviewer reports merged:
- Conditional adjudications:
- Work items cancelled after invalidation:
- Early exit used:
- Memory entries refreshed or invalidated:
- Validation level reached:
- Execution-mode fallback:
- Final outcome:
- Final confidence:

## Entries

No workflow runs recorded.
