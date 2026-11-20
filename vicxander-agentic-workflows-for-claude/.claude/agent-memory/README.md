# Project Agent Memory

Claude Code project-scoped subagent memory uses:

```text
.claude/agent-memory/<agent-name>/MEMORY.md
```

Only Orchestrator enables native `memory: project`. Architect, Coder, Tester, and Reviewer remain
read-only and consult their checked-in role notes. They return provenance-bearing memory candidates;
Orchestrator is the single writer and updates a role note only after active same-role workers have
finished and the path is free of another write lease.

Memory is lower authority than user instructions, code, tests, requirements, approved plans, and
`CLAUDE.md`.

Every durable entry uses:

```text
- Lesson:
  - Source artifact or evidence ID:
  - Owner:
  - Last confirmed revision/date:
  - Invalidation or expiry condition:
```

At task startup, compare provenance with the current revision and relevant inputs. An entry whose
source changed, confirmation is too old for the claim, or invalidation condition holds is a
hypothesis to verify delta-first—not trusted context. Remove or update disproven entries rather
than layering contradictions.

Optional metadata-only workflow measurements live separately in `.claude/workflow-metrics.md`.
They are project-scoped, user-visible Markdown, not telemetry, and must never contain prompts or
source content.

Do not store secrets, sensitive raw findings, full logs, copied plans, temporary chat history, or
facts easily inspected from code. Do not copy stage checkpoints into durable memory. Keep
`MEMORY.md` concise.
