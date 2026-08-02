# Requirements

This folder stores user-authored or user-approved requirements, acceptance criteria, workflow rules,
and other durable statements of intended behavior.

## Rules

- Treat files here as user intent.
- Use status `Draft`, `Approved`, `Implemented`, `Superseded`, or `Rejected`.
- Do not rewrite user-authored requirements casually.
- Preserve originals when creating summaries or derived requirements.
- Architect reads relevant requirements and plans from `Approved` requirements when possible.
- Orchestrator surfaces `Draft`, `Rejected`, or `Superseded` status before implementation planning.
- Give acceptance criteria stable IDs such as `AC-1` so plans can trace implementation,
  validation, and review evidence without rewriting user intent.
- Optionally map a requirement or criterion to an OpenSpec capability/scenario ID and artifact
  path. The mapping is derived navigation, not permission to rewrite stakeholder intent or make
  OpenSpec mandatory.
- In OpenSpec mode, surface conflicts between approved requirements, `openspec/specs/`, and the
  bound change delta before implementation. Requirements remain product intent; OpenSpec artifacts
  remain normalized current behavior and a proposed behavioral delta.
- Reviewer checks implementation against relevant requirements.
- Keep `INDEX.md` useful for navigation without duplicating full requirements.

## Naming

Prefer `REQ-0001-short-title.md` and keep its ID stable.
