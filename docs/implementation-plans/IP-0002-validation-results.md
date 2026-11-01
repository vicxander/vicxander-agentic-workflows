# IP-0002 Validation Results

Date: 2026-11-01. Contract: 3.0.0.

## Source Review

Consolidated principles, routing, role separation, explicit revision approval, risk floors,
resource governance, traceability, memory ownership and privacy requirements are retained.
Removed native activation/model/memory/discovery assumptions. Native format assertions were
retired with their product distributions; verified capabilities now govern destination formats.
Semantic and path/profile validation is read-only and does not install or execute external code.
License and author attribution remain. Prior source paths are intentionally breaking changes.

## Disposable Rehearsals

Two materially different documented entrypoints were verified against official documentation,
then generated and merged in temporary directories. Product names and URLs remained outside
tracked source. Scenario A used a root Markdown instruction entrypoint; B used a hidden-directory
Markdown entrypoint. Both used sequential role transitions rather than asserting native delegation.
For both: evidence/profile validation passed; read-only phase hashes stayed unchanged; workflow
contracts were copied locally; customized project command and local memory were preserved;
repeated merge produced one installed section; destination profile remained local.
These were assistant-driven file-materialization rehearsals, not executions of a bundled installer.
Native runtimes were not invoked: authentication/session execution was unavailable in this test.
Accordingly runtime acceptance is unavailable, not passed. These scenarios verify documented
entrypoint layout and file preservation only, not all possible runtime versions or settings.

## Automated Checks

- 67 semantic rules pass: 47 carried clauses plus 20 core invariants.
- 18 tests pass: missing roles, deleted semantics, missing profile fields, path traversal,
  missing/stale/contradictory evidence, mandatory capability failure, optional fallback,
  source overlap, read-only validation, removed bootstrap safeguards and broken links.
- Neutral source validation, coverage command and git diff --check pass.
- Current tracked-source name/content audit finds no known provider branding; local untracked
  environment configuration and historical Git objects are excluded by the approved boundary.

## Acceptance Disposition

AC1-AC9 satisfied for the published instruction-driven source and recorded validation limits.
AC7 specifically distinguishes observed file materialization from unavailable native runtime
acceptance. No universal compatibility, enforcement guarantee, or legal clearance is claimed.
Downstream user repositories were not modified.
