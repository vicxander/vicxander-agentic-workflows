# 3.0.0 Semantic Migration Inventory

This checklist records proposed destinations, not completed semantic transfers.

| Clause | Existing surfaces | Proposed destination | State |
| --- | --- | --- | --- |
| external-tool-data:absolute credential exclusion | 37 | workflow/principles.md | Pending |
| external-tool-data:external-surface coverage | 37 | workflow/principles.md | Pending |
| external-tool-data:general approval is insufficient | 37 | workflow/principles.md | Pending |
| external-tool-data:generic minimal non-sensitive inputs | 37 | workflow/principles.md | Pending |
| external-tool-data:protected project-data coverage | 37 | workflow/principles.md | Pending |
| external-tool-data:safer alternatives | 37 | workflow/principles.md | Pending |
| external-tool-data:specific-disclosure authorization | 37 | workflow/principles.md | Pending |
| fingerprint:command or method | 56 | workflow/orchestration.md | Pending |
| fingerprint:environment and tool version | 38 | workflow/orchestration.md | Pending |
| fingerprint:invalidation condition | 69 | workflow/orchestration.md | Pending |
| fingerprint:relevant inputs or hashes | 47 | workflow/orchestration.md | Pending |
| fingerprint:result digest | 38 | workflow/orchestration.md | Pending |
| fingerprint:revision or worktree state | 66 | workflow/orchestration.md | Pending |
| fingerprint:timestamp | 38 | workflow/orchestration.md | Pending |
| first-run-adaptation:approval before instruction write | 17 | workflow/orchestration.md | Pending |
| first-run-adaptation:bounded repository-wide inventory | 14 | workflow/orchestration.md | Pending |
| first-run-adaptation:delta-first refresh | 14 | workflow/orchestration.md | Pending |
| first-run-adaptation:evidence-first discovery | 15 | workflow/orchestration.md | Pending |
| first-run-adaptation:explicit user trigger | 18 | workflow/orchestration.md | Pending |
| first-run-adaptation:fact provenance | 14 | workflow/orchestration.md | Pending |
| first-run-adaptation:high-value discovery sources | 14 | workflow/orchestration.md | Pending |
| first-run-adaptation:instruction-only authorization | 14 | workflow/orchestration.md | Pending |
| first-run-adaptation:post-merge validation | 28 | workflow/orchestration.md | Pending |
| first-run-adaptation:protected workflow invariants | 19 | workflow/orchestration.md | Pending |
| first-run-adaptation:revisioned exact diff | 15 | workflow/orchestration.md | Pending |
| first-run-adaptation:scan exclusions | 14 | workflow/orchestration.md | Pending |
| first-run-adaptation:unknown and conflict handling | 14 | workflow/orchestration.md | Pending |
| lease:active lease quarantine | 25 | workflow/orchestration.md | Pending |
| lease:active release waits for confirmed stop and reconciliation | 17 | workflow/orchestration.md | Pending |
| lease:exclusive write ownership | 31 | workflow/orchestration.md | Pending |
| lease:last-write reconciliation | 24 | workflow/orchestration.md | Pending |
| lease:never-active immediate release | 21 | workflow/orchestration.md | Pending |
| lease:stale results are never integrated | 17 | workflow/orchestration.md | Pending |
| retry:changed retry evidence | 37 | workflow/orchestration.md | Pending |
| retry:exhaustion stops the node | 27 | workflow/orchestration.md | Pending |
| retry:hard retry ceiling | 27 | workflow/orchestration.md | Pending |
| retry:new hypotheses do not reset exhaustion | 29 | workflow/orchestration.md | Pending |
| retry:retries after exhaustion need authority | 28 | workflow/orchestration.md | Pending |
| untrusted-content:conflict escalation | 21 | workflow/principles.md | Pending |
| untrusted-content:declared authority | 21 | workflow/principles.md | Pending |
| untrusted-content:embedded directive refusal | 18 | workflow/principles.md | Pending |
| untrusted-content:log and finding coverage | 25 | workflow/principles.md | Pending |
| untrusted-content:non-instruction classification | 21 | workflow/principles.md | Pending |
| untrusted-content:reviewed skills | 21 | workflow/principles.md | Pending |
| untrusted-content:source and comment coverage | 21 | workflow/principles.md | Pending |
| untrusted-content:untrusted-data classification | 21 | workflow/principles.md | Pending |
| untrusted-content:web and tool-output coverage | 21 | workflow/principles.md | Pending |

The baseline covers 47 clauses, not the complete workflow. Also review every role, approval,
routing, resource, memory, conformance, privacy and installation requirement before removing
source surfaces. Map native-only constraints to capability requirements or justify retirement.
Preserve the existing coverage baseline until transfers have reviewed replacements.
