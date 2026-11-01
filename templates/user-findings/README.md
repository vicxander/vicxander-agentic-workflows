# User Findings

This folder stores user-provided findings and validation evidence such as CI logs, QA notes,
screenshots, crash traces, recordings, profiler output, and bug reports.

## Rules

- Treat findings as evidence, not automatic root cause.
- Use status `Open`, `Resolved`, `Stale`, or `Superseded`.
- Findings may be stale, incomplete, environment-specific, or caused by setup issues.
- Redact secrets, credentials, tokens, private URLs, personal identifiers, and customer data.
- Keep sensitive raw evidence untracked or outside the repository when needed.
- Keep large logs as files and record only concise conclusions in agent memory.
- Do not paste full logs into responses.
- Architect considers relevant findings, Tester uses them for reproduction and validation, and
  Reviewer checks whether they were addressed without overfitting.
- Keep `INDEX.md` useful for navigation.

## Naming

Prefer `UF-0001-short-title.md` and keep its ID stable.
