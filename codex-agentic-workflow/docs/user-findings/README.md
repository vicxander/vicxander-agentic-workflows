# User Findings

This folder stores user-provided findings and validation evidence.

## Purpose

Use this folder for files the user provides after testing or external validation, such as CI logs,
TeamCity exports, QA notes, screenshots, crash traces, recordings, profiler output, or bug reports.

## Rules

- Treat files here as evidence to inspect, not automatic root cause.
- Use statuses `Open`, `Resolved`, `Stale`, or `Superseded`.
- Findings may be stale, environment-specific, incomplete, or caused by setup issues.
- Redact secrets, tokens, credentials, private URLs, personal emails, device identifiers, customer
  data, and other sensitive information before committing or sharing findings.
- If raw findings contain sensitive data, keep the raw file untracked or outside the repository
  when needed. Commit only a redacted finding or summary that preserves enough evidence for agents
  to work.
- Keep large logs as files; summarize only the relevant conclusions in provider-specific session
  notes when useful.
- Do not paste full logs into chat responses; summarize relevant excerpts and reference the source
  file.
- Architect considers relevant findings before planning fixes.
- Tester uses relevant findings for reproduction and validation.
- Reviewer checks whether the change addresses the evidence without overfitting to it.
- Keep `INDEX.md` updated when useful for navigation.
- In OpenSpec mode, findings remain evidence rather than specification or execution authority.
  Map relevant evidence to the selected change and VAW plan without copying secrets or raw logs
  into OpenSpec artifacts.

## Suggested File Names

- `UF-0001-teamcity-quality-gates-failure.md`
- `UF-0002-crash-log-short-title.txt`
- `UF-0003-qa-notes-short-title.md`

Prefer the `UF-0001-short-title.md` pattern for new findings. Keep IDs stable after creation.
