# Requirements

This folder stores user-authored or user-approved requirements.

## Purpose

Use this folder for product intent, behavior requirements, acceptance criteria, workflow notes, and
other user-approved inputs that should guide planning and implementation.

## Rules

- Treat files here as user intent.
- Use explicit requirement statuses: `Draft`, `Approved`, `Implemented`, `Superseded`, or
  `Rejected`.
- Do not rewrite user-authored requirements casually.
- If agents summarize or reorganize requirements, preserve the original or clearly mark the derived
  version.
- Architect reads relevant requirements before creating implementation plans and plans from
  `Approved` requirements when possible.
- If the user asks to implement from a `Draft` requirement, Orchestrator should surface that status
  before planning.
- Give acceptance criteria stable IDs such as `AC-1` so plans can trace implementation,
  validation, and review evidence without rewriting user intent.
- Reviewer checks whether implementation drifted from relevant requirements.
- Keep `INDEX.md` updated when useful for navigation.

## Statuses

- `Draft`: captured but not approved.
- `Approved`: user-approved and ready to plan from.
- `Implemented`: implemented and validated.
- `Superseded`: replaced by a newer requirement or user decision.
- `Rejected`: intentionally not pursued.

## Suggested File Names

- `REQ-0001-short-title.md`
- `feature-name-requirements.md`
- `acceptance-criteria-short-title.md`

Prefer the `REQ-0001-short-title.md` pattern for new requirements. Keep IDs stable after creation.
