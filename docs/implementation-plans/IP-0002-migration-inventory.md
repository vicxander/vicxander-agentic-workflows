# 3.0.0 Semantic Migration Inventory

This checklist records proposed destinations, not completed semantic transfers.

| Clause | Existing surfaces | Proposed destination | State |
| --- | --- | --- | --- |
| external-tool-data:absolute credential exclusion | 37 | workflow/principles.md | Preserved; consolidated source check passes |
| external-tool-data:external-surface coverage | 37 | workflow/principles.md | Preserved; consolidated source check passes |
| external-tool-data:general approval is insufficient | 37 | workflow/principles.md | Preserved; consolidated source check passes |
| external-tool-data:generic minimal non-sensitive inputs | 37 | workflow/principles.md | Preserved; consolidated source check passes |
| external-tool-data:protected project-data coverage | 37 | workflow/principles.md | Preserved; consolidated source check passes |
| external-tool-data:safer alternatives | 37 | workflow/principles.md | Preserved; consolidated source check passes |
| external-tool-data:specific-disclosure authorization | 37 | workflow/principles.md | Preserved; consolidated source check passes |
| fingerprint:command or method | 56 | workflow/orchestration.md | Preserved; consolidated source check passes |
| fingerprint:environment and tool version | 38 | workflow/orchestration.md | Preserved; consolidated source check passes |
| fingerprint:invalidation condition | 69 | workflow/orchestration.md | Preserved; consolidated source check passes |
| fingerprint:relevant inputs or hashes | 47 | workflow/orchestration.md | Preserved; consolidated source check passes |
| fingerprint:result digest | 38 | workflow/orchestration.md | Preserved; consolidated source check passes |
| fingerprint:revision or worktree state | 66 | workflow/orchestration.md | Preserved; consolidated source check passes |
| fingerprint:timestamp | 38 | workflow/orchestration.md | Preserved; consolidated source check passes |
| first-run-adaptation:approval before instruction write | 17 | workflow/orchestration.md | Preserved; consolidated source check passes |
| first-run-adaptation:bounded repository-wide inventory | 14 | workflow/orchestration.md | Preserved; consolidated source check passes |
| first-run-adaptation:delta-first refresh | 14 | workflow/orchestration.md | Preserved; consolidated source check passes |
| first-run-adaptation:evidence-first discovery | 15 | workflow/orchestration.md | Preserved; consolidated source check passes |
| first-run-adaptation:explicit user trigger | 18 | workflow/orchestration.md | Preserved; consolidated source check passes |
| first-run-adaptation:fact provenance | 14 | workflow/orchestration.md | Preserved; consolidated source check passes |
| first-run-adaptation:high-value discovery sources | 14 | workflow/orchestration.md | Preserved; consolidated source check passes |
| first-run-adaptation:instruction-only authorization | 14 | workflow/orchestration.md | Preserved; consolidated source check passes |
| first-run-adaptation:post-merge validation | 28 | workflow/orchestration.md | Preserved; consolidated source check passes |
| first-run-adaptation:protected workflow invariants | 19 | workflow/orchestration.md | Preserved; consolidated source check passes |
| first-run-adaptation:revisioned exact diff | 15 | workflow/orchestration.md | Preserved; consolidated source check passes |
| first-run-adaptation:scan exclusions | 14 | workflow/orchestration.md | Preserved; consolidated source check passes |
| first-run-adaptation:unknown and conflict handling | 14 | workflow/orchestration.md | Preserved; consolidated source check passes |
| lease:active lease quarantine | 25 | workflow/orchestration.md | Preserved; consolidated source check passes |
| lease:active release waits for confirmed stop and reconciliation | 17 | workflow/orchestration.md | Preserved; consolidated source check passes |
| lease:exclusive write ownership | 31 | workflow/orchestration.md | Preserved; consolidated source check passes |
| lease:last-write reconciliation | 24 | workflow/orchestration.md | Preserved; consolidated source check passes |
| lease:never-active immediate release | 21 | workflow/orchestration.md | Preserved; consolidated source check passes |
| lease:stale results are never integrated | 17 | workflow/orchestration.md | Preserved; consolidated source check passes |
| retry:changed retry evidence | 37 | workflow/orchestration.md | Preserved; consolidated source check passes |
| retry:exhaustion stops the node | 27 | workflow/orchestration.md | Preserved; consolidated source check passes |
| retry:hard retry ceiling | 27 | workflow/orchestration.md | Preserved; consolidated source check passes |
| retry:new hypotheses do not reset exhaustion | 29 | workflow/orchestration.md | Preserved; consolidated source check passes |
| retry:retries after exhaustion need authority | 28 | workflow/orchestration.md | Preserved; consolidated source check passes |
| untrusted-content:conflict escalation | 21 | workflow/principles.md | Preserved; consolidated source check passes |
| untrusted-content:declared authority | 21 | workflow/principles.md | Preserved; consolidated source check passes |
| untrusted-content:embedded directive refusal | 18 | workflow/principles.md | Preserved; consolidated source check passes |
| untrusted-content:log and finding coverage | 25 | workflow/principles.md | Preserved; consolidated source check passes |
| untrusted-content:non-instruction classification | 21 | workflow/principles.md | Preserved; consolidated source check passes |
| untrusted-content:reviewed skills | 21 | workflow/principles.md | Preserved; consolidated source check passes |
| untrusted-content:source and comment coverage | 21 | workflow/principles.md | Preserved; consolidated source check passes |
| untrusted-content:untrusted-data classification | 21 | workflow/principles.md | Preserved; consolidated source check passes |
| untrusted-content:web and tool-output coverage | 21 | workflow/principles.md | Preserved; consolidated source check passes |

The baseline covers 47 clauses, not the complete workflow. Also review every role, approval,
routing, resource, memory, conformance, privacy and installation requirement before removing
source surfaces. Map native-only constraints to capability requirements or justify retirement.
Preserve the existing coverage baseline until transfers have reviewed replacements.

## Final Migration Disposition (2026-11-01)

All 47 prior clause patterns are retained in tools/contract_rules.json. Twenty core workflow
invariants extend coverage to approval, revision, lifecycle, risk, routes, traceability, confidence,
review, testing, leases, budget, cancellation, metrics, state, authority and permissions. Native
syntax/color/frontmatter/runtime field checks are retired because the source generates no native
configuration. Capability verification and destination-native checks replace those obligations.
Role prose and planning templates retain role boundaries and detailed control defaults. Duplicate
safety boundaries now resolve to workflow/principles.md. Source component paths are explicitly
logical mappings; generated destinations must rewrite references to installed local contracts.
Historical file links to removed distributions are labelled retired rather than left broken.

The old 1,294 clause/surface pairs represented duplicated native surfaces; the new checker retains
all 47 clause definitions across consolidated normative/template text, with 20 added core checks.
No claim is made that the retired 94 tests are equivalent to the 18 replacement tests. Native tests
are no longer applicable; regression scope now includes neutral semantic and generation boundaries.
