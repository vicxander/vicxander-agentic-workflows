# IP-VAW-0001 Enhance VicXander Agentic Workflows With OpenSpec

## Status

Done

- Plan revision: 1
- Prepared: 2026-08-02
- Repository baseline: `b84f2ef`
- Branch at planning time: `feature/VAW-0001_Enhance_with_open_spec_tools`
- Target workflow contract version: `2.5.0`
- Approval status: Approved; implementation completed
- Approved by: Victor Alexander Daud
- Approver role: Project Owner/Developer
- Approval date: 2026-08-02
- Approved plan revision: 1
- Completed: 2026-08-02
- Approval evidence: User message, "Approve: Approved **IP-VAW-0001** plan by Victor Alexander
  Daud - Project Owner/Developer"

Approval applies only to this revision. Any material change to scope, specification authority,
provider coverage, licensing, privacy behavior, dependency policy, validation, or review coverage
increments the revision, resets the plan to `Proposed`, and requires approval again.

## Executive Summary

Enhance VicXander Agentic Workflows (VAW) with an optional, OpenSpec-compatible specification mode
that adopts OpenSpec's lightweight proposal, specification-delta, design, task, synchronization,
and archive lifecycle while preserving VAW's existing Orchestrator, Architect, Coder, Tester, and
Reviewer coordination contract.

VAW remains the sole execution authority. OpenSpec supplies specification artifacts and lifecycle
operations; it must not bypass VAW's task classification, explicit plan approval, write leases,
role ordering, progressive validation, security review, or closeout rules. Existing installations
remain valid because `Specification mode: Native` is the default and OpenSpec is never installed,
initialized, invoked, or granted instruction authority implicitly.

The implementation is repository-wide. It must update the shared semantic contract, all three
provider materializations, the Codex bootstrap kit, documentation templates, license notices,
static validators, unit tests, and behavioral conformance suites as one versioned change.

## Work Classification

- Work class: Large
- Workflow route: Full
- Risk level: Medium
- Classification rationale: The change affects the shared workflow contract, three provider
  distributions, bootstrap generation, source-of-truth rules, approval binding, third-party
  licensing, privacy disclosures, and validator behavior. It has broad compatibility impact but
  does not itself alter authentication, secrets, payments, deployment, or user data.
- Execution mode: Parallel after shared-contract decisions are integrated
- Integration mode: Single integrator for shared semantics and validation; leased writers may work
  on provider-specific materializations after the canonical contract is stable
- Validation/review/closeout reserve: 25%
- Max retries per node: 1
- Local metrics: Off

## Source Inputs And Baseline Evidence

### Repository evidence

- The repository contains three distributable provider workflows, one Codex bootstrap kit, and a
  dependency-free Python validator/test suite.
- Before the explicit version-alignment change, the root and provider/validator contract markers
  disagreed.
- All active workflow-contract, provider-template, bootstrap, validator, plan-target, and citation
  markers are now aligned to `2.5.0`.
- The implementation phase must preserve that alignment while adding OpenSpec support.
- Baseline `python -B -m unittest discover -s tools -p "test_*.py"` result: 57 tests passed.
- The worktree was clean before this plan file was created.

The version mismatch is a pre-existing failure and must be resolved as the first implementation
node rather than attributed to OpenSpec integration.

### OpenSpec adoption baseline

- Repository: <https://github.com/Fission-AI/OpenSpec>
- Pinned planning baseline commit: `45cca5db6137ed209117cc70510eb3e057fb981b`
- Published npm package observed during planning: `@fission-ai/openspec@1.7.0`
- License: MIT, copyright 2024 OpenSpec Contributors
- License source: <https://github.com/Fission-AI/OpenSpec/blob/45cca5db6137ed209117cc70510eb3e057fb981b/LICENSE>
- Conceptual workflow baseline: `explore -> propose -> apply -> sync/archive`, with proposal,
  specification deltas, design, and tasks as change-scoped artifacts
- OpenSpec is an optional third-party tool. Its package, generated skills, command syntax,
  telemetry behavior, and artifact schemas may change independently of VAW.

Implementation must record the actual OpenSpec version and commit used. If they differ from this
planning baseline, Architect must review the delta. A material semantic or licensing change
requires a plan revision before copied or adapted material is integrated.

## Goals

1. Add a fast OpenSpec specification path without weakening VAW coordination or safety.
2. Preserve one unambiguous authority model across user requirements, OpenSpec artifacts, VAW
   plans, code/tests, findings, and operational instructions.
3. Make OpenSpec support optional, local, explicit, and backward compatible.
4. Prevent upstream OpenSpec `apply`, `verify`, `sync`, or `archive` actions from bypassing VAW's
   approval, role, validation, and closeout gates.
5. Reduce planning ceremony for appropriate routes by allowing OpenSpec artifacts to supply
   proposal, behavior delta, design, and task content instead of duplicating that content in a
   VAW implementation plan.
6. Maintain semantic parity across Codex, GitHub Copilot, Claude Code, and the Codex bootstrap kit.
7. Preserve VAW's dependency-free, no-telemetry default and offline repository validator.
8. Meet MIT attribution obligations for every copied or substantially adapted OpenSpec portion.

## Non-Goals

- Forking, vendoring, or reimplementing the complete OpenSpec CLI.
- Adding Node.js, npm, OpenSpec, MCP, a network service, telemetry, CI, or another runtime
  dependency to VAW's default installation or validation commands.
- Automatically running `npm install`, `npx`, `openspec init`, `openspec update`, or any command
  that changes a consuming repository.
- Replacing VAW's explicit user approval gate with OpenSpec artifact completion.
- Replacing Orchestrator, Architect, Coder, Tester, or Reviewer with OpenSpec commands.
- Deleting or automatically migrating existing `docs/requirements/`,
  `docs/implementation-plans/`, active plans, findings, memory, or generated OpenSpec artifacts.
- Publishing a VAW schema or plugin to an OpenSpec community catalog in this change.
- Claiming official affiliation with, endorsement by, or ownership of the OpenSpec name or brand.
- Adding a product runtime, package-manager configuration, hosted service, or analytics system.

## Architectural Decisions

### AD-1: Optional adapter, not a second coordinator

VAW will support OpenSpec through provider-native adapter skills and shared contract rules.
OpenSpec owns specification artifacts and artifact lifecycle operations. VAW owns classification,
approval, execution scheduling, agents, write leases, validation, review, and closeout.

The adapter must never hand an end-to-end task directly to an upstream `apply` skill in a way that
allows implementation before VAW approval.

### AD-2: Native mode remains the default

Add one workflow control:

```text
Specification mode: <Native|OpenSpec>
```

- Default when omitted: `Native`
- `Native`: existing `docs/requirements/` and `docs/implementation-plans/` behavior remains
  unchanged.
- `OpenSpec`: VAW binds one named OpenSpec change to the active VAW coordination plan.

Add an optional selector:

```text
OpenSpec change: <change-id|Auto>
```

`Auto` is allowed only when exactly one active change can be resolved. Multiple plausible active
changes are an `Unclear requirement` blocker; Orchestrator must ask the user to name one.

### AD-3: No automatic installation or initialization

In OpenSpec mode, capability preflight checks whether the project contains the expected OpenSpec
configuration/artifacts and whether an approved local CLI is available when a CLI operation is
required. Missing setup is classified as `Missing dependency/tooling`; VAW reports the exact
unblock condition and does not install or initialize anything without explicit authorization.

Native mode must work when OpenSpec and Node.js are absent.

### AD-4: Separate product intent, behavioral specification, and execution authority

Use the following semantic roles:

| Source | Meaning | Mutation authority |
| --- | --- | --- |
| Current user request | Current intent and task authority | User |
| Code and tests | Current implemented behavior | Approved Coder work |
| `docs/requirements/` | Stakeholder/product intent and stable acceptance criteria | User-authored or user-approved |
| `openspec/specs/` | Normalized current behavioral specification | OpenSpec sync/archive after VAW closeout |
| Approved `openspec/changes/<id>/` artifacts | Proposed behavioral delta, design, and tasks | Architect before approval; controlled revision after approval |
| Active VAW implementation plan | Execution envelope, coordination, risk, validation, and approval authority | Architect and Orchestrator |
| `docs/user-findings/` | Evidence to investigate | User or evidence workflow |

OpenSpec artifacts do not automatically outrank the current user request or approved product
requirements. Conflicts among requirements, OpenSpec specs/deltas, code/tests, and the active plan
must be surfaced before implementation.

### AD-5: Use a coordination overlay rather than duplicate OpenSpec artifacts

In OpenSpec mode, the VAW implementation plan must reference rather than repeat:

- the OpenSpec proposal
- delta specifications and scenarios
- design decisions
- task list

The VAW plan remains responsible for:

- plan revision and explicit approval evidence
- OpenSpec change ID, schema/profile, artifact paths, and fingerprint
- task/criterion crosswalk
- work classification and risk
- dependency graph and write leases
- integration mode and worker allocation
- evidence and assumption registers
- progressive validation and review allocation
- rollback/recovery when required
- closeout and archive readiness

Add a compact OpenSpec coordination-overlay template. Keep the existing full plan template for
Native Standard/Full work, and add a compact Lite template so route selection produces materially
different planning overhead.

### AD-6: Approval binds both plan revision and OpenSpec artifact fingerprint

An OpenSpec-mode approval record must identify:

- VAW plan ID and revision
- OpenSpec change ID
- resolved schema/profile
- proposal, spec-delta, design, and task artifact paths
- a deterministic artifact-set fingerprint or per-file hashes
- concise explicit-user approval evidence

Changing intent, behavior, non-goals, risk, design, task scope, validation, write ownership, or
review coverage after approval invalidates the bound fingerprint, marks dependent evidence stale,
returns the VAW plan to `Proposed`, and requires renewed approval. Cosmetic or non-material edits
must be recorded and justified if they do not trigger reapproval.

### AD-7: Map OpenSpec actions onto VAW stages

| OpenSpec intent | VAW authority and allowed behavior |
| --- | --- |
| Explore | Architect or Orchestrator may investigate; no product writes and no approval implied |
| Propose/new/continue/fast-forward | Architect may create or revise planning artifacts; stop at VAW approval gate |
| Update | Architect may revise artifacts; material post-approval changes invalidate approval and dependent evidence |
| Apply | Coder-only implementation under a named `In Progress` VAW plan and non-overlapping lease |
| Verify | Tester validates scenarios and gates; Reviewer independently checks compliance and drift |
| Sync | Orchestrator-only after required validation/review succeeds, unless explicitly deferred and reported |
| Archive | Orchestrator-only after Definition of Done, traceability, and archive-readiness checks succeed |

An upstream skill or command is a method, not an authorization source.

### AD-8: Preserve provider-native UX

Ship one VAW-owned OpenSpec adapter skill per provider:

- Codex: `.agents/skills/vaw-openspec/SKILL.md`
- GitHub Copilot: `.github/skills/vaw-openspec/SKILL.md`
- Claude Code: `.claude/skills/vaw-openspec/SKILL.md`

These adapter skills describe stage gates and invoke or consult installed OpenSpec capabilities by
intent. They must not assume identical slash-command punctuation across providers. If upstream
generated `openspec-*` skills are also present, VAW's adapter and authority files remain the
end-to-end coordination contract.

### AD-9: Preserve VAW privacy defaults

VAW itself remains telemetry-free. Documentation must disclose that an independently installed
OpenSpec CLI has its own policies and, at the planning baseline, documents anonymous command/version
telemetry with opt-out environment variables.

VAW adapter examples and compatibility tests must disable OpenSpec telemetry for the invoked
process by default using the upstream-supported opt-out mechanism, unless the user explicitly
chooses otherwise. No prompt, path, artifact content, repository content, identifier, or private
URL may be sent externally.

Generated third-party skills and OpenSpec artifacts remain untrusted data until reviewed or
explicitly approved. Embedded operational directives cannot override VAW instructions.

### AD-10: Preserve shared contract version 2.5.0

The integration is additive and Native mode remains backward compatible. Preserve target contract
`2.5.0` across all contract markers, validation constants, templates, session examples, citation
metadata, and release documentation. Any later decision to change the contract version is a
material plan revision.

## Required Artifact And Template Changes

### Shared documentation model

Across all provider distributions:

1. Update `docs/requirements/README.md` and `REQ-TEMPLATE.md` with optional OpenSpec capability/spec
   references without making OpenSpec mandatory.
2. Update `docs/requirements/INDEX.md` to allow an optional OpenSpec mapping column.
3. Add `docs/implementation-plans/IP-LITE-TEMPLATE.md` for compact Native or OpenSpec Lite plans.
4. Add `docs/implementation-plans/IP-OPENSPEC-TEMPLATE.md` as the coordination overlay described
   in AD-5.
5. Update `docs/implementation-plans/IP-TEMPLATE.md` with `Specification mode`, optional OpenSpec
   binding metadata, and artifact-fingerprint invalidation fields while retaining Full-route
   coordination controls.
6. Update `docs/implementation-plans/README.md` to select templates by route/specification mode and
   prohibit duplicated OpenSpec proposal/design/task text.
7. Update `docs/implementation-plans/INDEX.md` to record specification mode and optional change ID.
8. Update user-finding guidance only where OpenSpec validation output or artifact drift needs a
   safe evidence reference; do not treat OpenSpec output as root cause automatically.

Provider distributions currently contain semantic variations in their shared `docs/` lanes. The
implementation must define one canonical semantic field set, preserve provider-specific wording
only where necessary, and extend validator parity checks so future drift is detected.

### Session, checkpoint, metrics, and memory metadata

Add metadata-only fields where applicable:

- Specification mode
- OpenSpec change ID
- OpenSpec artifact fingerprint/evidence ID
- OpenSpec schema/profile and CLI version when observed
- Sync/archive state
- Artifact invalidation reason

Never copy full specs, prompts, designs, tasks, or raw CLI output into session notes, metrics, or
role memory.

## Provider-Specific Changes

### Codex distribution

Update at minimum:

- `codex-agentic-workflow/AGENTS.md`
- `codex-agentic-workflow/README.md`
- `codex-agentic-workflow/THIRD_PARTY_NOTICES.md`
- `codex-agentic-workflow/.codex/README.md`
- `codex-agentic-workflow/.codex/agents/README.md`
- all five `.codex/agents/*.toml` role definitions
- `.agents/skills/README.md`
- new `.agents/skills/vaw-openspec/SKILL.md`
- `.codex/session-notes.md`, `.codex/worklog.md`, `.codex/todo.md`, and
  `.codex/workflow-metrics.md` where new metadata belongs
- `.codex/workflow-conformance.md`
- the three documentation lanes and implementation-plan templates

Do not add OpenSpec MCP configuration or global prompt files to `.codex/config.toml`. Update that
file only if a provider-native capability declaration is actually required and supported.

### GitHub Copilot distribution

Update at minimum:

- `github-copilot-agentic-workflow/AGENTS.md`
- `github-copilot-agentic-workflow/README.md`
- `github-copilot-agentic-workflow/THIRD_PARTY_NOTICES.md`
- `.github/copilot-instructions.md`
- `.github/AGENTIC-WORKFLOW.md`
- all five `.github/agents/*.agent.md` role definitions
- `.github/skills/README.md`
- new `.github/skills/vaw-openspec/SKILL.md`
- `.github/agent-memory/` session, worklog, todo, metrics, and applicable role-memory guidance
- `.github/WORKFLOW-CONFORMANCE.md`
- the three documentation lanes and implementation-plan templates

Account for the two-task approval pattern on Copilot cloud agents: planning/OpenSpec proposal work
must be committed or otherwise present in the second task's baseline, and the second task must name
the approved VAW plan revision and OpenSpec artifact fingerprint.

### Claude Code distribution

Update at minimum:

- `claude-agentic-workflow/CLAUDE.md`
- `claude-agentic-workflow/README.md`
- `claude-agentic-workflow/THIRD_PARTY_NOTICES.md`
- `.claude/AGENTIC-WORKFLOW.md`
- all five `.claude/agents/*.md` role definitions
- `.claude/skills/README.md`
- `.claude/skills/agentic-workflow/SKILL.md`
- new `.claude/skills/vaw-openspec/SKILL.md`
- `.claude/session-notes.md`, `.claude/worklog.md`, `.claude/todo.md`, and
  `.claude/workflow-metrics.md` where new metadata belongs
- `.claude/workflow-conformance.md`
- the three documentation lanes and implementation-plan templates

Preserve Claude Code's interactive and non-interactive approval rules. An OpenSpec proposal in a
non-interactive run may prepare artifacts but cannot self-approve or cross into implementation.

## Bootstrap Kit Changes

Update all three bootstrap-kit sources:

- `agentic-bootstrap-kit/README.md`
- `agentic-bootstrap-kit/CODEX_AGENTIC_BOOTSTRAP.md`
- `agentic-bootstrap-kit/AGENTIC_FILE_TEMPLATES.md`

Required behavior:

1. Add `Specification mode` parsing and Native default.
2. Materialize the Codex VAW OpenSpec adapter skill and new plan templates.
3. Add OpenSpec authority, approval-binding, privacy, failure, validation, sync, and archive rules
   to generated files.
4. Preserve create, merge, and dry-run behavior.
5. Never run OpenSpec installation or initialization as a bootstrap side effect.
6. In merge mode, preserve existing `openspec/`, OpenSpec-generated skills/commands, active changes,
   specs, schemas, config, and third-party notices.
7. Add the OpenSpec notice to a generated/merged `THIRD_PARTY_NOTICES.md` without removing other
   notices or replacing the target project's license.
8. Extend target-scoped bootstrap validation to the new required files and semantics.

## Licensing, Attribution, Provenance, And Branding

### Required notices

Because the implementation may copy or substantially adapt OpenSpec templates, skills,
documentation, or code, include the complete upstream MIT copyright and permission notice:

```text
Copyright (c) 2024 OpenSpec Contributors
```

Required locations:

- new root `THIRD_PARTY_NOTICES.md`
- each provider distribution's standalone `THIRD_PARTY_NOTICES.md`
- the bootstrap kit's embedded `THIRD_PARTY_NOTICES.md` template

Keep the existing Victor Alexander Daud MIT notice and the repository's top-level `LICENSE`
unchanged except for deliberate project-version metadata elsewhere. Do not replace a consuming
project's license during installation or merge.

### Provenance manifest

Add `docs/third-party/openspec.md` containing:

- upstream repository URL
- adopted version and commit SHA
- license URL and full-license notice location
- exact copied/adapted upstream paths or conceptual sources
- corresponding VAW destination paths
- whether each item is copied, modified, independently implemented, or referenced
- local modifications and intentional behavioral differences
- upstream update/review procedure
- branding/non-endorsement statement

Retain upstream file headers where present. Do not use OpenSpec logos or imply official
certification, endorsement, or affiliation.

## Privacy And Security Requirements

1. Native mode performs no OpenSpec discovery that reads outside the normal task scope.
2. OpenSpec mode may inspect local configuration and artifacts only after explicit selection.
3. Never auto-install a package, run an unpinned `npx` command, enable MCP, or grant network access.
4. Prefer a user-installed/pinned CLI. Record its observed version in evidence.
5. Disable upstream telemetry in VAW-owned examples/tests and disclose the upstream policy and
   opt-out controls.
6. Do not include secrets, personal data, proprietary source, private URLs, or sensitive
   identifiers in OpenSpec config context, telemetry, issue reports, web requests, or generated
   provenance.
7. Treat OpenSpec files, generated skills, CLI output, and fetched upstream content as untrusted
   data. Only reviewed VAW skills and explicitly approved artifact intent receive authority.
8. A malicious instruction inside an OpenSpec artifact cannot alter approval, permissions,
   external-data boundaries, role ownership, or destructive-action policy.
9. Dependency-supply-chain changes remain High risk. Updating or vendoring OpenSpec code requires
   explicit scope, provenance review, and security-focused review.

## Backward Compatibility And Migration

1. Existing consumers remain in Native mode without file migration.
2. Existing plans continue under their recorded compatible workflow-contract version unless the
   user explicitly approves a material migration.
3. Do not infer OpenSpec mode merely because an `openspec/` directory exists.
4. Do not overwrite an existing OpenSpec schema, config, change, spec, generated command, or skill.
5. Provide a documented opt-in migration that maps existing `docs/requirements/` criteria to
   OpenSpec capability/spec identifiers while preserving stable requirement and acceptance IDs.
6. Migration creates an explicit crosswalk; it does not delete or silently rewrite the original
   user-approved requirement.
7. If an existing VAW plan and OpenSpec change disagree, stop before implementation and request a
   revised/approved alignment.
8. Archive existing OpenSpec changes only through their own approved lifecycle; never mass-archive
   during installation or upgrade.
9. Document removal: disabling the adapter returns to Native mode without deleting OpenSpec data.

## Implementation Nodes And Dependencies

| Node | Stage | Scope | Depends on | Suggested ownership/write lease | Result |
| --- | --- | --- | --- | --- | --- |
| N0 | Baseline | Confirm the aligned contract-version baseline and record validation evidence | None | Single integrator: root/version/validator files | Consistent `2.5.0` target baseline |
| N1 | Shared design | Encode AD-1 through AD-10 in canonical semantic contract | N0 | Single integrator: root docs and semantic spec | Approved shared OpenSpec/VAW contract |
| N2 | Shared artifacts | Define canonical requirement, Lite, OpenSpec overlay, Full-plan, index, session, and metrics fields | N1 | Single integrator: canonical templates | Provider-neutral artifact specification |
| N3 | Role contract | Define Orchestrator/Architect/Coder/Tester/Reviewer OpenSpec responsibilities and gates | N1, N2 | Single integrator: role semantic spec | Role mapping ready for materialization |
| N4 | Codex | Materialize contract, adapter skill, docs, roles, and conformance | N2, N3 | Codex distribution lease | Codex OpenSpec-compatible distribution |
| N5 | Copilot | Materialize contract, adapter skill, docs, roles, and conformance | N2, N3 | Copilot distribution lease | Copilot OpenSpec-compatible distribution |
| N6 | Claude | Materialize contract, adapter skill, docs, roles, and conformance | N2, N3 | Claude distribution lease | Claude OpenSpec-compatible distribution |
| N7 | Bootstrap | Update bootstrap instructions/templates and merge safeguards | N2, N3, N4 | Bootstrap-kit lease | OpenSpec-ready Codex bootstrap |
| N8 | Licensing | Add notices, provenance, telemetry disclosure, and non-endorsement language | N1; coordinate with N4-N7 | Single integrator for canonical notice; provider writers copy exactly | MIT-compliant distribution |
| N9 | Validator | Extend required-file sets, prompt controls, template parity, provider parity, notices, privacy, and OpenSpec invariants | N2-N8 | `tools/validate_workflows.py` lease | Static contract validation |
| N10 | Tests | Add mutation tests, adapter/fixture tests, target bootstrap tests, and conformance coverage checks | N9 | `tools/test_*.py` and fixtures lease | Regression suite |
| N11 | User docs | Update root/provider/bootstrap usage, migration, examples, version, citation, counts, and troubleshooting | N4-N10 | Single integrator for root; provider doc leases | Complete installation/usage guidance |
| N12 | Integration | Run offline validation, provider conformance dry runs, optional pinned OpenSpec E2E, review, and closeout | N0-N11 | Single integrator | Release-ready evidence |

N4, N5, and N6 may run in parallel only after N1-N3 are integrated. N7 should use the final Codex
semantics rather than independently inventing them. N8's canonical license text has one writer;
provider copies must match it. N9-N12 operate on an integrated baseline.

## Validator And Test Changes

### Static validator

Extend `tools/validate_workflows.py` to verify:

- one consistent workflow-contract version across root, providers, templates, bootstrap, session
  files, and citation metadata
- new adapter-skill files in each provider's exact required set
- new Lite/OpenSpec templates in `SHARED_DOCS` and bootstrap target names
- `Specification mode` value validation and default `Native`
- optional `OpenSpec change` syntax and ambiguity policy
- source-of-truth placement for product requirements, OpenSpec specs/deltas, and VAW plans
- prohibition on OpenSpec apply before approval
- artifact-fingerprint binding and invalidation language
- role-specific apply/verify/sync/archive ownership
- Native-mode independence from OpenSpec/Node.js
- no auto-install, auto-init, unpinned `npx`, or implicit network behavior
- complete OpenSpec MIT notice in root, providers, and bootstrap template
- privacy/telemetry disclosure and opt-out examples without weakening VAW's no-telemetry claim
- provider semantic parity for the integration contract
- CommonMark links and provenance-manifest targets
- bootstrap create/merge/dry-run preservation of existing OpenSpec files

Do not make the default validator invoke Node.js, npm, OpenSpec, or the network.

### Unit and mutation tests

Extend the existing test modules and add focused tests where clearer:

- mutate Native default to OpenSpec and require failure
- remove the approval gate from an apply path and require failure
- allow archive before Tester/Reviewer and require failure
- remove artifact fingerprint or invalidation language and require failure
- omit a provider adapter or notice and require failure
- introduce conflicting provider source-of-truth order and require failure
- allow auto-install/init or unpinned network invocation and require failure
- remove telemetry disclosure/opt-out and require failure
- bootstrap merge fixture containing existing OpenSpec data; verify it is preserved
- bootstrap target without OpenSpec; verify Native mode remains valid
- multiple active change fixture; verify explicit selection is required
- post-approval artifact mutation fixture; verify approval/evidence becomes stale
- provider frontmatter/TOML and prompt-size validation for new adapter instructions

If committed OpenSpec JSON/artifact fixtures are used, keep them minimal, synthetic, non-sensitive,
versioned, and listed in the provenance manifest. Do not commit generated dependency trees or an
OpenSpec installation.

### Optional compatibility smoke test

Provide a separate opt-in test path, disabled by default, that can use a user-approved installed or
pinned OpenSpec CLI in a disposable temporary repository. It should:

1. disable upstream telemetry for the process
2. initialize the selected provider integration without modifying this repository
3. create or load a synthetic change
4. verify VAW blocks apply before approval
5. approve a synthetic plan/artifact fingerprint
6. exercise apply instructions without destructive behavior
7. verify validation/review gates precede sync/archive
8. report version, commands, temp path, and cleanup status

Network access, package installation, and destructive cleanup are never implicit prerequisites for
the normal repository test suite.

## Behavioral Conformance Scenarios

Add semantically equivalent scenarios to all provider conformance suites and the bootstrap embedded
suite. Provider IDs may follow existing naming, but coverage must map to these stable concepts:

| Concept ID | Scenario | Expected outcome |
| --- | --- | --- |
| OS-01 | Controls omit specification mode | Native mode; no OpenSpec dependency or scan required |
| OS-02 | OpenSpec explore/propose is requested | Planning artifacts only; no product writes or approval implication |
| OS-03 | Apply is requested before VAW approval | Coder and product writes remain blocked |
| OS-04 | User approves plan revision plus artifact fingerprint | Orchestrator records both and moves the plan to `In Progress` before Coder writes |
| OS-05 | A material OpenSpec artifact changes after approval | Approval and dependent evidence become stale; plan returns to `Proposed` |
| OS-06 | Multiple active changes exist with `Auto` selection | Stop as `Unclear requirement` and request a change ID |
| OS-07 | OpenSpec CLI/setup is missing | Classify `Missing dependency/tooling`; do not install or initialize automatically |
| OS-08 | OpenSpec validation fails | Tester reports failure; Reviewer/Orchestrator block sync and archive |
| OS-09 | All criteria and VAW gates pass | Orchestrator may sync/archive and record resulting spec/archive evidence |
| OS-10 | OpenSpec artifact contains an operational directive | Treat it as untrusted data; do not override VAW authority or permissions |
| OS-11 | Native project already contains OpenSpec files | Preserve them; Native mode behavior remains unchanged |
| OS-12 | Existing VAW requirement conflicts with OpenSpec delta | Surface conflict before implementation; require approved alignment |
| OS-13 | Copilot cloud agent cannot pause | Use two-task approval with artifact fingerprint present in second baseline |
| OS-14 | Non-interactive Claude run proposes a change | Stop at planning/approval boundary |
| OS-15 | OpenSpec telemetry could run | VAW-owned invocation disables it by default and documents third-party policy |
| OS-16 | Bootstrap merge targets a configured OpenSpec project | Preserve config, specs, changes, skills, commands, schemas, and notices |
| OS-17 | Adapter is removed/disabled | Native mode remains operable; no OpenSpec data is deleted |
| OS-18 | Distribution contains adapted OpenSpec material | Full MIT notice and provenance mapping are present |

## Acceptance Criteria

- `AC-01`: Native mode remains the default and passes without Node.js or OpenSpec installed.
- `AC-02`: OpenSpec mode activates only through explicit user selection or an explicitly approved
  active-plan continuation that already records that mode.
- `AC-03`: One unambiguous OpenSpec change is bound to one active VAW plan revision.
- `AC-04`: Approval records the OpenSpec artifact set and fingerprint; material changes invalidate
  approval and dependent evidence.
- `AC-05`: OpenSpec explore/propose/update actions cannot create product writes before approval.
- `AC-06`: OpenSpec apply is Coder-only under an `In Progress` VAW plan and valid write lease.
- `AC-07`: Tester and Reviewer remain distinct required validation/review authorities for planned
  routes; upstream verify cannot replace either silently.
- `AC-08`: Sync/archive cannot occur until required criteria, validation, review, and closeout
  conditions pass or an explicitly approved exception is recorded without false completion.
- `AC-09`: `docs/requirements/`, OpenSpec specs/deltas, VAW plans, code/tests, and findings have
  documented non-conflicting semantic roles and conflict handling.
- `AC-10`: Lite and OpenSpec overlay templates materially reduce duplicated planning content while
  Full mode retains current safety controls.
- `AC-11`: Codex, GitHub Copilot, and Claude Code ship provider-native VAW OpenSpec adapter skills
  with semantically equivalent gates.
- `AC-12`: The bootstrap kit creates/merges the new Codex integration files without running or
  overwriting OpenSpec.
- `AC-13`: Existing OpenSpec configuration, specs, changes, generated files, schemas, and notices
  survive provider installation, bootstrap merge, update, and removal paths.
- `AC-14`: The repository and every standalone distribution retain complete OpenSpec and VicXander
  MIT notices when adapted material is distributed.
- `AC-15`: A provenance manifest maps every copied or adapted OpenSpec source to VAW destinations
  and records the pinned upstream baseline.
- `AC-16`: VAW remains telemetry-free; OpenSpec telemetry behavior is disclosed and disabled in
  VAW-owned invocations/examples unless the user explicitly opts in.
- `AC-17`: No default command installs packages, initializes OpenSpec, uses an unpinned network
  source, or requires network access.
- `AC-18`: All contract-version markers and citation/release metadata consistently identify
  `2.5.0`.
- `AC-19`: The dependency-free validator covers new files and semantic invariants without invoking
  OpenSpec or the network.
- `AC-20`: Unit/mutation tests cover all OS-01 through OS-18 concepts, provider parity, bootstrap
  preservation, licensing, privacy, and approval invalidation.
- `AC-21`: Root/provider/bootstrap documentation explains installation, controls, lifecycle,
  migration, removal, troubleshooting, and third-party policy boundaries.
- `AC-22`: Existing Native projects and active plans have a documented no-migration compatibility
  path.
- `AC-23`: The normal validator and complete unit suite pass from a clean worktree; optional
  OpenSpec E2E is either passed with pinned evidence or reported as blocked, never implied.
- `AC-24`: No provider prompt/agent exceeds its supported format or size limits, and all Markdown
  links, TOML, and flat-YAML frontmatter remain valid.

## Acceptance-Criteria Traceability Plan

| Criteria | Primary implementation evidence | Validation/review evidence |
| --- | --- | --- |
| AC-01, AC-02, AC-17, AC-22 | control parsing, docs, adapter activation rules | Native-no-OpenSpec fixtures; auto-install mutation tests |
| AC-03-AC-08 | plan fields, role contracts, adapter skills, lifecycle rules | OS-02 through OS-09 conformance; fingerprint mutation tests |
| AC-09, AC-10 | source-of-truth docs and route-specific templates | provider parity checks; plan-template semantic tests |
| AC-11, AC-24 | three provider materializations | required-file, frontmatter, TOML, link, and prompt-size validation |
| AC-12, AC-13 | bootstrap sources/templates | bootstrap create/merge/dry-run and preservation fixtures |
| AC-14, AC-15 | notices and provenance manifest | exact-license and source/destination mapping checks |
| AC-16 | privacy contract, examples, adapter invocation rules | telemetry-polarity/adversarial tests and privacy review |
| AC-18 | version markers and citation metadata | repository-wide version consistency validator |
| AC-19, AC-20, AC-23 | validator and tests | normal validation commands plus optional pinned E2E report |
| AC-21 | root/provider/bootstrap documentation | CommonMark/local-link checks and documentation review |

## Validation Ladder

### V1: Static text and format checks

- Verify only intended files changed.
- Validate Markdown fences and local links.
- Parse Codex TOML and provider frontmatter.
- Search for stale contract-version markers, obsolete OpenSpec command assumptions, prohibited
  auto-install/init behavior, incomplete notices, and duplicated authority statements.

### V2: Focused validator tests

Run focused unit tests for:

- contract control parsing
- plan templates
- provider required-file sets
- role/approval contracts
- bootstrap materialization/merge
- privacy/security polarity
- OpenSpec-specific mutations and fixtures

### V3: Full offline repository validation

```shell
python -B tools/validate_workflows.py
python -B -m unittest discover -s tools -p "test_*.py"
```

Both commands must pass. The pre-existing contract-version failure must no longer exist.

### V4: Provider behavioral conformance

Run or inspect every new OS scenario plus affected existing approval, privacy, external-data,
invalidation, failure-classification, provider-fallback, first-run adaptation, and bootstrap
scenarios for Codex, GitHub Copilot, and Claude Code.

### V5: Optional OpenSpec interoperability smoke test

With explicit approval, a pinned CLI, telemetry disabled, and a disposable synthetic project, run
the optional compatibility test. Record blocked runtime/network/tool conditions honestly.

### V6: Final review

Review perspectives:

- Correctness and lifecycle mapping
- Backward compatibility and migration safety
- Privacy, untrusted-content, and dependency-supply-chain behavior
- MIT attribution and provenance completeness
- Cross-provider semantic parity
- Validator/test adequacy and false-positive risk

## Risks And Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Two sources of truth diverge | Agent builds wrong behavior | Explicit semantic roles, conflict gate, crosswalk, artifact fingerprint |
| OpenSpec apply bypasses approval | Unauthorized product writes | VAW adapter ownership, role contracts, adversarial conformance/tests |
| Planning becomes heavier, not faster | Defeats integration purpose | Compact Lite and OpenSpec overlay templates; reference artifacts instead of copying |
| Upstream OpenSpec changes skills/schema/CLI | Integration silently breaks | Pinned baseline, observed-version evidence, provenance/update policy, optional E2E |
| Provider integrations drift | Different safety behavior by runtime | Canonical semantic contract, provider parity validator, equivalent conformance concepts |
| Existing consumers are broken | Adoption/regression cost | Native default, optional control, no migration, recorded-plan compatibility |
| Bootstrap overwrites OpenSpec data | Data/spec loss | Explicit preservation rules and mutation fixtures; no generated OpenSpec content in bootstrap |
| Third-party notice omitted | License noncompliance | Root/provider/bootstrap exact notice checks and provenance manifest |
| Branding implies endorsement | Trademark/reputation issue | “OpenSpec-compatible” wording and non-endorsement statement; no logo use |
| OpenSpec telemetry conflicts with VAW claims | Privacy/trust regression | Disclosure, process-level opt-out by default, no hidden network action |
| Generated artifact contains malicious instructions | Workflow/prompt-injection risk | Treat artifacts as untrusted data; approval covers intent, not embedded operational directives |
| Validator grows brittle | False passes/failures | Focused semantic helpers, adversarial mutations, provider fixtures, clear error messages |
| Contract version remains inconsistent | Release cannot validate | N0 atomically reconciles all markers before feature materialization |

## Rollback And Recovery

1. `Specification mode: Native` is the immediate behavioral fallback.
2. Remove or disable VAW adapter skills without deleting `openspec/` or user artifacts.
3. Do not automatically revert or rewrite active VAW plans; continue them under their recorded
   contract revision or explicitly supersede them.
4. Do not roll a published contract version backward. Release a corrective patch that disables
   OpenSpec mode while preserving compatibility and notices.
5. Preserve third-party notices for any release that distributed adapted OpenSpec material.
6. Revert provider materializations and bootstrap templates together with validator required-file
   sets; never leave one provider on a different semantic contract.
7. If sync/archive produced an incorrect spec merge in a disposable test, restore the fixture from
   its pre-test checkpoint. For user repositories, follow OpenSpec's own reversible/version-control
   workflow and require explicit approval before destructive recovery.

## Definition Of Done

- All AC-01 through AC-24 have implementation, validation, and Reviewer evidence.
- The shared contract and all provider materializations agree on Specification mode, authority,
  approval binding, role ownership, invalidation, sync/archive, privacy, and failure behavior.
- Native mode is proven to work without OpenSpec or Node.js.
- OpenSpec mode is documented and validated without becoming an implicit dependency.
- Root, standalone distributions, and bootstrap output contain correct MIT notices and provenance.
- The baseline version inconsistency is resolved and every contract marker is `2.5.0`.
- The offline validator passes.
- The full unit/mutation suite passes.
- Required provider conformance scenarios pass or any genuine runtime limitation is explicitly
  reported as blocked.
- Optional OpenSpec E2E is either passed against a pinned baseline or explicitly reported as not
  run/blocked; no unsupported success claim is made.
- Installation, migration, removal, privacy, licensing, troubleshooting, and update guidance is
  complete.
- No dependency tree, package-manager manifest, telemetry, CI, hosted service, secret, raw log, or
  generated OpenSpec project data is accidentally added.
- Changed-file, provenance, residual-risk, and compatibility reports are complete.

## Approval Record

Victor Alexander Daud, Project Owner/Developer, explicitly approved revision 1 on 2026-08-02.
The plan transitioned from `Proposed` to `In Progress`, authorizing implementation under the scope,
controls, acceptance criteria, and change-control rules recorded in this document.

## Implementation Closeout

- Final workflow contract: `2.5.0`
- OpenSpec compatibility baseline: npm `1.7.0`, commit
  `45cca5db6137ed209117cc70510eb3e057fb981b`
- Requested/actual execution: `Parallel`; three provider workers ran concurrently, for an actual
  peak of three subagents, followed by single-integrator reconciliation
- Requested/actual integration: `Single integrator` for shared semantics, bootstrap, validator,
  tests, and closeout; provider roots used non-overlapping leases
- Changed inventory: 80 existing files modified and 11 files added; each provider distribution now
  contains exactly 35 files and the repository contains 120 validated files
- Intentionally unchanged: the top-level `LICENSE`, product dependencies/manifests, CI,
  provider/runtime model settings, user OpenSpec project data, and release tags/publication state
- Provider conformance: Codex, GitHub Copilot, and Claude each contain exactly OS-01 through OS-18;
  the static validator verifies every scenario's expected behavior
- Bootstrap: 34 generated targets are contract-parity checked against the finalized Codex source;
  target-scoped materialization is exercised by the unit suite
- Validation: `python -B tools/validate_workflows.py` passed 5,628 checks across 120 repository
  files; `python -B -m unittest discover -s tools -p "test_*.py"` passed 62 tests;
  `git diff --check` passed
- Optional pinned OpenSpec CLI E2E: not run because this plan did not authorize installation,
  network use, or execution of the third-party CLI. No OpenSpec process ran and no telemetry was
  emitted; any later VAW-owned run must set `OPENSPEC_TELEMETRY=0` or `DO_NOT_TRACK=1`
- Licensing/provenance: full VicXander and OpenSpec MIT notices are present at root, in every
  standalone provider, and in bootstrap output; `docs/third-party/openspec.md` records the source
  mapping, intentional differences, update procedure, and non-endorsement statement
- Compatibility: Native remains the no-migration default; no Node.js/OpenSpec dependency or scan
  is required, existing active plans keep their recorded contract, and merge/removal rules preserve
  all existing `openspec/` data
- Canonical findings/adjudication: provider wording and validator patterns were reconciled to the
  approved semantics; no unresolved finding or adjudication remains
- Blocked checks: only the optional CLI E2E, as described above; it is not required for offline
  completion and is not reported as passed
- Residual risk: future OpenSpec releases may change artifacts, lifecycle, or telemetry; the pinned
  provenance review procedure and optional authorized compatibility smoke test are the mitigation
- Follow-up: commit, tag, release, and publication work remains user-owned and was not performed

### Final Acceptance-Criteria Traceability

| Criteria | Implementation evidence | Validation/review disposition |
| --- | --- | --- |
| AC-01, AC-02, AC-17, AC-22 | Native-default controls, provider adapters, no-setup rules, migration guidance | Prompt/control mutations, no runtime-manifest changes, full validator pass |
| AC-03-AC-08 | OpenSpec overlay/full plans, five role contracts per provider, fingerprint invalidation, lifecycle gates | OS-02 through OS-09 semantic checks and adapter/overlay mutation tests passed |
| AC-09, AC-10 | Artifact-authority guidance plus Lite and OpenSpec templates in all providers/bootstrap | Provider file/parity checks and template contract tests passed |
| AC-11, AC-24 | Three provider-native `vaw-openspec` skills and bounded native agent formats | Required-file, TOML/frontmatter, prompt-size, Markdown, and link checks passed |
| AC-12, AC-13 | Bootstrap instructions and exact 34-target bundle with preservation rules | Materialized bootstrap target tests and parity checks passed |
| AC-14, AC-15 | Root/provider/bootstrap MIT notices and OpenSpec provenance manifest | Exact notice and provenance checks, including notice mutation, passed |
| AC-16 | Telemetry-free VAW policy, process-local OpenSpec opt-out, external-data boundaries | Privacy/security polarity and unsafe-rule mutations passed |
| AC-18 | Repository-wide contract/citation alignment at `2.5.0` | No stale `1.0.0`, `2.0.0`, or `2.1.0` contract marker remains |
| AC-19, AC-20, AC-23 | Dependency-free OpenSpec validators and 62-test adversarial suite | Both required offline commands passed; optional CLI E2E honestly not run |
| AC-21 | Root, provider, and bootstrap install/use/migration/removal/privacy/license/troubleshooting docs | CommonMark, local-link, content, and provider parity review passed |
