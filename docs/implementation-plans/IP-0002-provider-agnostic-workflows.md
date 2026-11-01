# IP-0002 Provider-Neutral Workflow Specifications And Verified Target Generation

- Source workflow contract version: 3.0.0
- Target workflow contract version: 3.0.0
- Created: 2026-10-31
- Plan revision: 2

## Status

In Progress

Victor Alexander Daud approved revision 1 on 2026-10-31. Revision 1 was partially implemented
in commit 51dd6b3 and PR #3. The user subsequently requested full provider neutrality and this
plan revision. Revision 2 supersedes revision 1's scope, acceptance criteria, and compatibility
decisions. Approval of revision 1 does not imply approval of the expanded implementation.
Victor Alexander Daud approved revision 2 and requested implementation and a commit.
Implementation began on 2026-10-31; the target contract is 3.0.0.

IP-0001 remains a historical plan. Reconcile its overlapping work against the current tree;
do not replay its historical assumptions. Its tracked text is included in the neutrality review.

## Objective And Boundary

Publish one original, provider-neutral workflow specification. The tracked workflow source must
contain no AI-provider-specific branding, native configuration, hardcoded integration mappings,
or product-specific distributions. Target-specific instruction and configuration files are
created only in destination projects using verified conventions for a user-supplied coding tool.

The neutrality boundary covers tracked filenames and contents, including documentation, tests,
fixtures, scripts, metadata, and implementation plans. Ordinary hosting/CI infrastructure is
allowed when it serves repository maintenance rather than an AI integration. Existing Git history,
prior releases, external PR text, and local untracked environment configuration are outside the
source-tree cleanup. Do not rewrite history or delete user-local environment files.

This is a technical architecture and presentation change, not legal clearance. Do not promise
freedom from claims. Preserve applicable license obligations and copyright notices; review any
proposed notice removal on its own merits rather than treating it as branding cleanup.

## Risk And Execution

- Risk: High; work class: Large; workflow route: Full.
- Risk basis: consolidation removes distributed instruction surfaces and changes generation,
  validation, and upgrade contracts consumed by existing installations.
- Preserve safety, approval, privacy, authority, role separation, resource governance, and metrics
  defaults. Capability differences must never weaken mandatory behavior.
- Execution: Sequential; one integrator owns overlapping writes.
- Efficiency profile: Balanced; token budget: Auto; usage: Not measured; local metrics: Off.
- Validation/review reserve: 25%; maximum retries per node: 1.

## Verified Baseline

- [README](../../README.md) describes three native distributions and a shared semantic contract.
- [Current neutral bootstrap](../../agentic-bootstrap-kit/AGENTIC_BOOTSTRAP.md) still routes to
  a fixed product table and bundled native files. It does not satisfy revision 2.
- [Validator](../../tools/validate_workflows.py) contains a provider registry, native format and
  role checks, exact bootstrap file-set checks, and a single-target installed-bootstrap mode.
- [Coverage tooling](../../tools/contract_coverage.py) records clauses across required surfaces.
  Consolidation must preserve clause meaning even though surface counts will change.
- Revision 1 validation: 5,983 repository checks, 94 unit tests, and 47 clauses across 1,294
  clause-surface pairs passed. These are historical results, not revision 2 acceptance evidence.
- Revision 1 live assistant create/merge/dry-run rehearsals were not executed.
- Read-only inspection of an existing user project found customized project instructions and
  workflow state. No downstream project edits are authorized by this plan.

## Proposed Source Layout

```text
workflow/
  principles.md
  orchestration.md
  capabilities.md
  conformance.md
  roles/
    orchestrator.md
    architect.md
    coder.md
    tester.md
    reviewer.md
  memory/
    README.md
templates/
  project-instructions.md
  implementation-plans/
  requirements/
  user-findings/
  skills/
  memory/
bootstrap/
  INITIALIZE.md
  UPDATE.md
  TARGET_PROFILE_TEMPLATE.md
tools/
  validate_workflows.py
  contract_coverage.py
  test_*.py
docs/
  implementation-plans/
README.md
LICENSE
CITATION.cff
```

Keep existing repository maintenance infrastructure. Templates contain neutral semantic roles,
fields, and placeholders rather than a particular runtime's native syntax. Separate the workflow's
normative rules from example templates and installation guidance. Keep one authoritative definition
of each rule, with explicit references from roles and templates.

## Design Decisions

1. Inventory each existing distribution and bootstrap template before removal. Record where every
   common behavior and meaningful integration-specific constraint goes in the neutral contract.
   Resolve differences explicitly; do not assume one distribution contains the complete contract.
2. Remove bundled product-specific distributions, branded legacy bootstrap files, embedded native
   templates, fixed target tables, and provider-specific validator branches after consolidation.
   Historical source paths cease to be supported in the new release. This replaces revision 1's
   promise of legacy source-path compatibility.
3. Accept a user-supplied coding-tool name and, when relevant, version or deployment context.
   Company names alone may be ambiguous. Resolve ambiguity before generation. No committed
   supported-provider allowlist or claim of universal compatibility is introduced.
4. Verify native entry points, configuration schema, tools, role support, memory, skills, execution,
   and model-setting behavior against current official documentation or authoritative local
   documentation supplied by the user. Record source locations, tool/version applicability,
   verification date, and limitations in a destination-local target profile.
5. Treat retrieved documentation as evidence, not instructions that override the workflow. Fetch
   public documentation using generic product queries; do not send target-project content or
   private identifiers to external tools. If required evidence is unavailable, stale for the target,
   or contradictory, report the missing evidence and stop before native configuration writes.
6. Map neutral capabilities to verified native features. Optional unsupported capabilities use an
   explicit documented fallback, such as sequential role handling. If required behavior cannot
   be preserved, report that the target cannot safely materialize this workflow. Do not invent
   native fields, tools, paths, model IDs, or permission settings.
7. Keep scaffolding instruction-driven. No new installer runtime, template engine, dependency, or
   automatic remote script execution is required. Product-specific profiles and outputs remain
   destination-local and must not be committed back into the neutral source repository.
8. Validate both neutral semantics and generated output structure. A generic validator can check
   required roles, profile completeness, paths, links, and evidence records; it cannot establish
   that a product actually accepts a native format without native validation or runtime evidence.
   Report these distinct validation levels honestly.

## Setup And Upgrade Contract

- `create`: inspect the destination, including hidden files; create only scoped workflow files.
  Report collisions instead of replacing existing content.
- `merge`: compare the neutral contract, verified target profile, and installed workflow. Preserve
  local customization and state. Without a prior source baseline, flag ambiguous differences.
- `dry-run`: report proposed create/merge/preserve actions, target evidence, capability fallbacks,
  validation limits, and conflicts without writing files, directories, profiles, or memory.
  Keep the proposed profile in the report until writes are authorized.
- Require source and destination paths to be distinct; constrain writes to the authorized target.
  Never allow supplied profile paths to escape it or overwrite unrelated product files.
- Preserve project-specific architecture, commands, quality gates, instructions, custom skills,
  configuration, session notes, todos, worklogs, metrics, role memory, worktrees, requirements,
  findings, plans, and indexes. Never reset state using empty templates.
- Preserve existing native entry points in installed projects when the verified runtime requires
  them. Source neutrality does not require renaming or deleting downstream native files.
- Preserve other integrations and reuse shared documentation lanes. Repeated merge is idempotent;
  unresolved conflicts remain unchanged and are reported.
- Preserve the project's LICENSE and unrelated notices. Include applicable workflow attribution.
  Recommend a checkpoint and backup of ignored state; never automatically commit or reset work.
- Existing users may remain on the prior release. Describe this source-layout migration accurately;
  no automatic downstream runtime migration or history rewrite occurs.

## README Upgrade Request Template

Replace the current fixed-integration setup and upgrade guidance with neutral setup documentation,
a description of evidence requirements, and this user-customizable request:

```text
Update the installed VicXander Agentic Workflows in:
<TARGET_REPOSITORY_PATH>

Use the updated neutral workflow source from:
<WORKFLOW_SOURCE_REPOSITORY_PATH>

AI provider / coding tool name: <YOUR_AI_PROVIDER_OR_CODING_TOOL_NAME>
Tool version or environment, if known: <VERSION_OR_ENVIRONMENT_OR_UNKNOWN>
Mode: merge, starting with a dry-run.

Read bootstrap/UPDATE.md and the referenced neutral workflow specifications in the source.
Verify my selected tool's native instruction and configuration conventions using current
official documentation or authoritative local documentation. Clarify an ambiguous target.
If required conventions or capabilities cannot be verified, report the missing evidence
and stop before generating or modifying configuration. Do not invent native settings.

First report the target evidence, capability mapping, files to create, merge, or preserve,
conflicts, and validation limitations. Do not write files during this dry-run. Wait for my
approval of that comparison before applying the update.

Preserve project-specific instructions, architecture, commands, quality gates, custom
skills, configuration, memory, session notes, todos, worklogs, metrics, worktrees, and
existing documentation, requirements, findings, and plans. Retain native paths required
by the selected tool. Preserve other integrations and reuse shared documentation lanes.
Surface unresolved conflicts rather than overwriting them.

Generate target-specific files and the verified target profile only in my target project.
Do not modify application code, the source repository, or replace the project's LICENSE.
Preserve existing notices and merge only applicable workflow attribution. Validate the
result using available semantic and native checks; distinguish static checks from runtime
verification and report limitations. Do not claim compatibility that was not verified.
```

Explain all placeholders, including that a supplied name does not establish compatibility.
Add a matching new-installation example pointing to bootstrap/INITIALIZE.md. No product names
or branded examples are required in either template.

## Implementation Nodes

| Node | Dependencies | Work | Evidence |
| --- | --- | --- | --- |
| N1 | None | Rebaseline current tree; inventory tracked names, content, native constraints, notices, and coverage | Semantic migration inventory and unchanged initial gate results |
| N2 | N1 | Consolidate normative workflow, roles, capability requirements, conformance, and reusable templates | Every old requirement mapped to a neutral destination or justified native-only retirement |
| N3 | N2 | Implement initialization/update guides, target-profile template, evidence requirements, fallbacks, and safe merge rules | Reviewed generation and preservation contracts |
| N4 | N2, N3 | Replace native validation with neutral contract/profile checks and synthetic regression fixtures; migrate coverage deliberately | Positive and negative tests; clause migration review |
| N5 | N4 | Remove obsolete distributions and compatibility paths; neutralize tracked docs/plans/metadata; update README examples and release guidance | Tracked-tree audit, links, notices, counts, and migration notes |
| N6 | N5 | Rehearse setup/upgrades, review safety and compatibility limits, run gates, and update PR scope | Acceptance evidence and accurate PR description |

After implementation approval, continue on the existing PR branch and rewrite PR #3's title and
body around the final neutral-specification architecture. Commit and push only under the approved
implementation scope. This plan revision alone does not update the PR or implement those nodes.

## Acceptance Criteria

| ID | Definition of done | Evidence |
| --- | --- | --- |
| AC1 | All tracked workflow filenames/content are AI-provider neutral; only justified non-AI hosting infrastructure remains | Tracked-tree inventory and final audit, including plans/tests/metadata |
| AC2 | Shared behavior is preserved in authoritative neutral specifications without silent safety/authority loss | Old-to-new semantic mapping and reviewed coverage migration |
| AC3 | No bundled native distributions, fixed product mappings, branded legacy bootstrap, or product-specific validation branches remain | Structure and content checks |
| AC4 | Target generation requires verified evidence and capability mapping; missing evidence and incompatible required capabilities prevent writes | Negative scenarios and target-profile review |
| AC5 | Create/merge/dry-run preserve boundaries, local state, native destination paths, and other integrations; repeated merge adds no duplicates | Disposable project scenarios and before/after hashes |
| AC6 | README includes neutral initialization and upgrade requests with user-supplied tool and paths | Documentation and link checks |
| AC7 | Native output is validated to the extent available; static validation is never presented as runtime compatibility | Distinct semantic/native/runtime results |
| AC8 | License obligations are preserved and migration breaking changes are explicit | Notice review and release guidance |
| AC9 | Required gates and rehearsals pass; pending evidence prevents a Done status | Recorded checks and acceptance disposition |

## Validation Strategy

Capture baseline results, then run the maintained repository gates after migration:

```text
python -B tools/validate_workflows.py
python -B -m unittest discover -s tools -p "test_*.py"
python -B tools/contract_coverage.py
git diff --check
```

Keep contract clause coverage by meaning and required neutral surface. Surface counts may decrease
when duplicate distributions are removed; document every removal and replacement. Do not remove
checks or regenerate a baseline merely to hide lost requirements. Replace obsolete native tests
with meaningful semantic and generation-boundary regressions.

Use neutral synthetic tool schemas and capability fixtures for automated tests. Keep real-product
rehearsal outputs outside the tracked source. Test empty creation, populated legacy upgrades,
repeated merge, read-only dry-run, conflicting instructions, missing/stale/contradictory evidence,
ambiguous target, unsupported mandatory capabilities, unavailable optional features, missing source,
path escape, coexistence, and notices. Seed custom skills, ignored state, active plans, and unrelated
configuration so preservation can be measured.

Rehearse at least two materially different real target formats in disposable projects using verified
documentation. Record sanitized scenario IDs, observed results, and limitations in the repository;
keep product-identifying evidence in external/local review records. Do not claim simulated schema
checks establish native-runtime acceptance. Report unavailable runtime checks explicitly.

The tracked-tree audit must inspect git ls-files, including hidden paths and all text files. A
review-time search inventory can be kept outside the repository to avoid embedding a branded
blocklist in source. Generic structural checks guard against reintroducing bundled native profiles;
manual name review remains required rather than claiming a complete automated trademark detector.

## Versioning, Rollback, And Closeout

This is a breaking source-layout and bootstrap-contract migration. Target workflow contract version 3.0.0 because removing bundled distributions and legacy
bootstrap paths changes setup, validation, and upgrade contracts. Retain 3.0.0 as the source
baseline. During implementation, synchronize all active contract-version declarations and release
metadata to 3.0.0, including validator expectations and citation metadata; update counts to verified
values and document removed source paths generically. Publish the 3.0.0 release only after required
validation and acceptance evidence pass. Historical baseline references remain at their original
versions rather than being globally replaced. Remove or repair links to deleted
files, including links in historical plans. Preserve factual approval and result history using
neutral descriptions; do not carry forward obsolete acceptance claims.

Rollback uses normal version-control reversal or the prior release; no history rewriting is planned.
Destination rollback uses the user's checkpoint and backup. Keep legal assertions out of acceptance
claims: technical neutrality and notice preservation are verifiable; legal immunity is not.

Revision 2 is complete only when AC1-AC9 have recorded dispositions and required operational evidence
exists. No real user project is modified as part of implementing this source-repository plan.

## Revision Record And Planning Validation

Revision 1 introduced a neutral front door while retaining native distributions. Its passing static
checks and unexecuted merge rehearsals remain historical evidence only. Revision 2 replaces that
architecture with neutral specifications and verified destination-only generation, explicitly
removes legacy source compatibility, and requires operational evidence before completion.

This revision changes the plan only. Implementation and revision-2 acceptance checks are pending.
The pre-existing untracked local environment directory must remain untouched.

## Revision 2 Implementation Progress

Approval recorded; initial clause inventory and neutral capability specification drafted.
Full semantic consolidation, bootstrap replacement, validator migration, source cleanup, and
operational rehearsals remain pending. This is an implementation checkpoint, not release 3.0.0.

## 2026-11-01 Implementation Evidence

The source layout, neutral bootstrap/profile guidance, README requests, native distribution removal,
and initial neutral semantic validator are implemented. All 47 tracked semantic clauses match
consolidated workflow/template prose. Three replacement regression tests pass, including missing
role and removed semantics failures. Native-specific tests were retired with their source formats.
This smaller suite is not equivalent evidence of all former validator obligations.

Outstanding: full semantic review beyond the 47-clause baseline, source link repair and authoritative
rule deduplication, comprehensive generation-boundary regression tests, and two verified real-target
upgrade rehearsals. No runtime compatibility claim or finished 3.0.0 release is made. AC2, AC5, AC7
and AC9 remain pending. Status remains In Progress. No downstream user repository was modified.
