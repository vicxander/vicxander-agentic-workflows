# IP-0002 Provider-Agnostic Workflows And Existing-Installation Upgrades

- Workflow contract version: 2.6.0 (planning baseline)
- Created: 2026-10-31
- Plan revision: 1

## Status

In Progress

Approved by Victor Alexander Daud on 2026-10-31, revision 1. Implementation started under
that approval.

The user requested this implementation plan. Implementation has not been authorized by this
planning request. Material changes to scope, acceptance criteria, or validation require a revised
plan. This plan does not supersede IP-0001; reconcile overlapping changes against the current tree
before implementation rather than replaying that plan's historical baseline.

## Summary

Present VicXander Agentic Workflows as a provider-agnostic workflow with explicitly selected
target integrations. Neutralize general branding while preserving the native instructions,
formats, capabilities, and activation rules needed by each supported tool. Add a shared manual
bootstrap entry point and document safe upgrades of existing installations.

Provider-agnostic means a neutral workflow identity with supported integration mappings. It does
not mean every provider is supported or that provider names disappear from technical configuration.

## Risk Level And Work Classification

- Risk: High, because edits span downstream instruction templates and their validation contracts.
- Work class: Large; workflow route: Full; requested depth: Auto.
- Preserve all safety, approval, privacy, authority, and resource-governance semantics.
- Execution mode: Sequential; integration mode: Single integrator.
- Efficiency profile: Balanced; token budget: Auto; usage: Not measured; local metrics: Off.
- Reserve: 25% for validation, review, and closeout; max retries per node: 1.

## Verified Baseline And Source Inputs

- [Root README](../../README.md) already defines one shared semantic workflow contract and three
  native distributions. Installation notes require preserving existing instructions, memory,
  documentation, and third-party notices.
- [Bootstrap specification](../../agentic-bootstrap-kit/CODEX_AGENTIC_BOOTSTRAP.md) currently
  targets Codex and supports create, merge, and dry-run through agent instructions.
- [Embedded templates](../../agentic-bootstrap-kit/AGENTIC_FILE_TEMPLATES.md) are Codex-specific.
- [Validator](../../tools/validate_workflows.py) has a PROVIDERS registry, exact bootstrap file-set
  checks, Codex bootstrap-target validation, native format checks, and literal README count checks.
- [Coverage tooling](../../tools/contract_coverage.py) and its committed baseline track clauses
  across required surfaces; wording changes can affect coverage recognition.
- [Existing plan](IP-0001-context-efficiency-and-contract-enforcement.md) establishes a root-level
  plan convention. There is currently no root implementation-plan index or template.
- Read-only inspection of the user's soundvslr-win11 installation found contract version 2.6.0,
  project-specific CLAUDE.md guidance, and existing memory, skills, and worktrees. This motivates
  preservation requirements but does not authorize editing that external repository.

## Scope And Non-Goals

In scope: public workflow prose, distribution prose, bootstrap guidance, embedded-template parity,
README setup and upgrade examples, and associated validator/tests/coverage updates.

Keep the three existing distribution directory names and native output paths. Keep copyright,
license, and attribution content separate from editorial branding changes. Do not add a template
engine, runtime, CLI scaffolder, dependencies, or unsupported integrations. Do not relocate memory
into a new shared directory. Do not update downstream projects as part of this change.

## Design Decisions

1. Use neutral titles and role-based language for general workflow behavior. Keep product names
   in the supported-integration table, native configuration explanations, activation instructions,
   provider-processing disclosures, and compatibility notes. Do not use global text replacement.
2. Use `Target integration` as the setup field. Accept documented product display names and stable
   IDs for the existing three integrations: codex, claude, and github-copilot. A provider/company
   name that maps ambiguously to a product requires clarification. Unknown names produce an
   unsupported-target report before writes; never silently select a different integration.
3. Add agentic-bootstrap-kit/AGENTIC_BOOTSTRAP.md as the neutral manual entry point. Route to the
   existing distribution contents and their native setup instructions. The executing assistant
   need not be the requested target; generated files follow the explicit target selection.
4. Retain CODEX_AGENTIC_BOOTSTRAP.md and its embedded templates as a working compatibility path.
   Explain its Codex-specific scope and link to the neutral entry point. Avoid a second generic
   copy of all distribution templates. Keep standalone legacy-kit use working.
5. The neutral entry point requires the selected distribution to be available with the kit;
   document how to supply the repository/source path. If source files are missing, report the
   missing dependency without inventing templates or fetching unspecified remote sources.
6. Preserve create, merge, and dry-run meanings. Dry-run must list source, target, proposed file
   actions, conflicts, and validation limitations without writes. Upgrading means merge; existing
   content must never be overwritten merely because it differs from the distribution.

## Implementation Nodes And Dependencies

| Node | Depends on | Changes and ownership | Completion evidence |
| --- | --- | --- | --- |
| N1 | None | Inventory provider mentions and native exceptions across README, three distributions, and bootstrap kit; capture baseline validation | Reviewed classification of editorial vs technical occurrences |
| N2 | N1 | Neutralize general titles, descriptions, task prompts, and role prose; preserve native semantics and mirror relevant embedded template edits | Diff review and contract coverage comparison |
| N3 | N2 | Add neutral bootstrap routing, supported-name mapping, source requirements, safe merge rules, and legacy compatibility guidance | Create/merge/dry-run scenarios for all three targets |
| N4 | N3 | Update root and distribution README setup/upgrade guidance, including the exact generic template below | Working relative links and examples matching actual supported behavior |
| N5 | N2, N3, N4 | Update validator bootstrap file-set, README wording/count checks, target-specific checks, and affected unit tests/coverage baseline | Full repository gates plus negative regression tests |
| N6 | N5 | Review native-format preservation, safety coverage, upgrade preservation, compatibility, and release metadata | Acceptance traceability and recorded validation results |

One integrator owns all writes. Nodes are sequential because prose, embedded templates, and
validator expectations overlap. No parallel worker allocation is required.

## Existing-Installation Upgrade Contract

- Recommend a Git checkpoint and a separate backup of ignored/untracked state before applying
  an upgrade; do not automatically commit, delete, or reset user work.
- Compare source distribution files against the installed workflow. Without a previous source
  baseline, do not claim that differences are exclusively local edits; flag ambiguous conflicts.
- Merge workflow sections while retaining project-specific architecture, commands, quality gates,
  authority rules, and custom instructions. Explicitly report conflicts instead of guessing.
- Preserve session notes, todos, worklogs, metrics, role memory, custom skills, worktrees, and
  existing plans, requirements, findings, and documentation indexes. Merge template guidance only
  where appropriate; do not reset existing state from empty distribution templates.
- Preserve native entry points and config paths for the selected target, unrelated config keys,
  and other installed integrations. Share existing documentation lanes; do not duplicate them.
- Merge required notices without replacing the target project's LICENSE or unrelated notices.
- Report changed, skipped, and conflicted files and available validation evidence. Branding-only
  adoption is optional and must not be presented as a required runtime migration.

## README Update: Proposed Exact Upgrade Request Template

Add an "Update an existing installation" section to the root README. Explain the preservation
rules above, link to the neutral bootstrap guide and supported integrations, and include:

```text
Update the installed VicXander Agentic Workflows in:
<TARGET_REPOSITORY_PATH>

Use the updated workflow source from:
<WORKFLOW_SOURCE_REPOSITORY_PATH>

AI provider / coding tool name: <YOUR_AI_PROVIDER_OR_CODING_TOOL_NAME>
Mode: merge, starting with a dry-run.

Read agentic-bootstrap-kit/AGENTIC_BOOTSTRAP.md in the workflow source repository.
Resolve my supplied name to a documented supported target integration. If the name is
ambiguous or unsupported, explain what is needed before making changes. Do not switch
integrations or invent configuration for an unsupported target.

First produce a dry-run comparison listing files to create, merge, preserve, and any
conflicts. Wait for my approval of that comparison before applying the update.

Preserve project-specific instructions, architecture, commands, quality gates, custom
skills, configuration, memory, session notes, todos, worklogs, metrics, worktrees, and
existing documentation, requirements, findings, and plans. Keep the selected integration's
native instruction filenames and configuration directories. Preserve other integrations
and reuse shared documentation lanes. Surface unresolved conflicts rather than overwriting.

Do not modify application code or replace the project's LICENSE. Preserve existing notices
and merge only missing workflow notices. After applying the approved update, validate the
workflow using available target-appropriate checks and report changes and limitations.
```

The approval pause above is part of the proposed reusable downstream request, not a requirement
to pause creation of this implementation plan. Tell README readers to replace all three
placeholders and consult the integration table; entering a name does not add provider support.
Link distribution READMEs to this central procedure rather than duplicating the full template.

## Acceptance Criteria And Traceability

| ID | Definition of done | Nodes / evidence |
| --- | --- | --- |
| AC1 | General workflow branding is neutral; remaining product names have technical, compatibility, disclosure, or attribution purposes | N1, N2; occurrence review |
| AC2 | Neutral entry point documents explicit target routing for all three existing integrations and rejects ambiguous/unsupported targets before writes | N3, N5; routing scenarios |
| AC3 | Native entry points, role sets, tool declarations, model inheritance, memory behavior, and safety clauses are preserved | N2, N5, N6; native checks and coverage diff |
| AC4 | Create, merge, and dry-run work as documented; dry-run is read-only and a repeated merge introduces no duplicate sections | N3, N5; disposable fixture comparisons |
| AC5 | Upgrades preserve local instructions and state, other integrations, shared docs, config, and notices; conflicts are surfaced | N3, N5; populated upgrade fixtures |
| AC6 | README contains the provider-neutral request template with user-supplied target/source paths and provider/tool name | N4; documentation review |
| AC7 | Existing Codex bootstrap invocation remains valid and missing neutral-bootstrap source files fail clearly | N3, N5; compatibility scenarios |
| AC8 | Required gates pass without dropping contract coverage to conceal regressions | N5, N6; command results and coverage review |

## Validation Strategy

Capture current results before editing; do not assume historical plan results still apply.

```text
python -B tools/validate_workflows.py
python -B -m unittest discover -s tools -p "test_*.py"
python -B tools/contract_coverage.py
git diff --check
```

Use disposable repositories for each integration: empty create, populated merge with local
customizations, repeated merge, dry-run with before/after file hashes, conflicting instructions,
missing source distribution, unsupported target, and coexistence with another integration.
Seed ignored memory and custom skills so preservation is observable. Validate generated native
formats and required files using target-specific checks factored from the existing registry.
Keep the existing --bootstrap-target Codex validation compatible; do not imply it validates
other integrations without extending and testing that interface explicitly.

The scaffolding remains instruction-driven. Automated static tests validate routing declarations,
preservation rules, and file contracts; they do not prove an assistant executed a merge correctly.
Record manual disposable-project scenario results separately and report any unexecuted scenario.
Add negative tests for missing mappings, accidental native-path replacement, weakened preservation
clauses, and stale bootstrap-file expectations. Review coverage baseline changes individually;
never regenerate the baseline solely to make failures disappear.

## Release, Rollback, And Closeout

Assess versioning after the final diff: editorial-only changes do not imply changed runtime
semantics, but a revised bootstrap contract must be documented and all declared contract versions
kept consistent if bumped. Update file counts and release metadata only to verified values.

Rollback upstream through normal version-control reversal; keep legacy paths functional during
the migration. Downstream rollback uses the user's checkpoint plus backup for ignored state.
Report acceptance results, changed files, unresolved limitations, and compatibility guarantees.
No external installation is updated by completing this plan.

## Planning Validation

Repository/source inspection completed. Implementation tests and disposable upgrade scenarios
have not run; those belong to implementation. The pre-existing untracked .codex directory is
outside this plan's changes and must be preserved.

## Implementation Evidence (2026-10-31)

N1-N5 implemented: neutral public branding and task prompts; shared manual bootstrap with three
explicit integration mappings; legacy compatibility; central README upgrade template and links;
validator routing/preservation guards with negative regression tests. Native config and agent
frontmatter were retained. Editorial integration names remain where they explain compatibility.
No contract version bump: native behavioral semantics remain at 2.6.0; the neutral entry point
adds setup guidance. Bootstrap source-file count is now four.

Validation: 5,983 repository checks passed; 94 unit tests passed; 47 contract clauses across
1,294 recorded clause-surface pairs retained; git diff --check passed. Diff review corrected an
encoding conversion before the final checks. The coverage baseline required no changes.

N6 limitation: live assistant create/merge/dry-run rehearsals in disposable projects were not
executed. Automated tests cover the documented mapping and preservation contract, including
negative cases; they do not prove actual merge behavior. AC4/AC5 operational scenario evidence
remains pending, so this plan stays In Progress rather than claiming complete acceptance.
The PR is reviewable with this explicit limitation. No downstream repository was modified.
