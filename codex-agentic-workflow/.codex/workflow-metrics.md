# Workflow Metrics

This optional, user-visible Markdown log stores repository-local operational metadata that can help
improve workflow speed and reliability. It is not author-operated telemetry. The workflow contains
no uploader, automatic export, or author-operated collection service.

## Privacy Rules

- Record counts, statuses, durations, and workflow decisions only.
- `Local metrics: Off` is the default. Append an entry only when the user selects `On`.
- Never record prompts, source code, file contents, secrets, credentials, personal data, raw logs,
  or external service payloads.
- Use `Not measured` when the runtime cannot observe a metric; never invent a value.
- The user may edit, delete, ignore, or decline to update this file at any time.
- Do not send this file or its contents to an external service unless the user explicitly requests
  that action.
- Do not record evidence fingerprints that expose file contents; record only opaque evidence IDs,
  counts, freshness outcomes, or hash values when already available and safe.

## Calibration Rules

- Calibration is optional and local. Review aggregate patterns only when enough comparable entries
  exist to make a conclusion useful.
- Read at most the latest 20 comparable entries for routine calibration. Keep older entries out of
  active context. Compact or archive them only with the user's approval, preserve metadata-only
  aggregates when useful, and never silently delete history.
- Look for over-routing, unnecessary context expansion, low evidence reuse, avoidable retries,
  circuit-breaker frequency, worker overhead, validation churn, and Reviewer rework.
- Treat conclusions as recommendations for human review. Never automatically reduce a safety
  floor, approval gate, required validation, or security coverage.
- Do not derive personal or source-content profiles. Codex or enabled tools may process this
  project file under their own policies when it is in context.

## Entry Template

### YYYY-MM-DD — Plan Or Task ID

- Work class:
- Local metrics: On
- Specification mode:
- OpenSpec selection method:
- OpenSpec change ID (non-sensitive identifier only):
- OpenSpec fingerprint freshness (status only):
- OpenSpec lifecycle actions (counts/status only):
- OpenSpec process telemetry opt-out:
- Workflow route:
- Requested workflow depth:
- Risk:
- Efficiency profile:
- Token budget:
- Token usage observed:
- Validation/review/closeout reserve requested:
- Reserve remaining at validation start:
- Token observability:
- Capability preflight limitations:
- Requested execution mode:
- Actual execution mode:
- Requested integration mode:
- Actual integration mode:
- Designated integrator used:
- Requested global and role caps:
- Optional spawn candidates:
- Spawns accepted by value gate:
- Spawns rejected by value gate:
- Workers used by stage:
- Actual peak concurrency:
- Stage durations:
- Context expansion boundaries:
- Stage checkpoints written:
- Evidence entries reused:
- Evidence entries invalidated:
- Evidence cache hit rate:
- Duplicate scans avoided:
- Commands intentionally rerun:
- Avoidable test reruns:
- Retries by failure class:
- Circuit breakers opened:
- Work items cancelled after invalidation:
- Impact-selected checks:
- Broader checks triggered:
- Reviewer findings requiring rework:
- Duplicate findings merged:
- Adjudications triggered:
- Validation level reached:
- Early exit used:
- Execution-mode fallback:
- Final outcome:
- Final confidence:
- Calibration note:

Do not record OpenSpec artifact bodies, file contents, private identifiers, CLI output, or raw
manifests here. Native-mode entries use `Not applicable` for OpenSpec fields.

## Entries

No workflow runs recorded.
