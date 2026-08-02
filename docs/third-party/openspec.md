# OpenSpec Provenance And Adaptation Record

## Pinned Baseline

- Upstream project: [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
- Adopted package version: `1.7.0`
- Adopted commit: `45cca5db6137ed209117cc70510eb3e057fb981b`
- Upstream license: [MIT License at the adopted commit](https://github.com/Fission-AI/OpenSpec/blob/45cca5db6137ed209117cc70510eb3e057fb981b/LICENSE)
- Complete license notices: repository `THIRD_PARTY_NOTICES.md`, each standalone provider
  distribution's `THIRD_PARTY_NOTICES.md`, and the bootstrap kit's generated notice template

The commit, rather than an unpinned branch, is the source of truth for this adaptation review.

## Adaptation Map

| Upstream source or concept | VAW destination | Treatment | Local modification |
| --- | --- | --- | --- |
| `schemas/spec-driven/templates/{proposal,spec,design,tasks}.md` and `docs/writing-specs.md` | Provider `docs/implementation-plans/IP-OPENSPEC-TEMPLATE.md`, `IP-LITE-TEMPLATE.md`, and updated `IP-TEMPLATE.md` | Modified conceptual adaptation | Adds VAW plan revision, approval evidence, role ownership, leases, validation, review, and artifact fingerprints; it does not copy OpenSpec as a second plan hierarchy |
| `skills/openspec-{explore,propose,new-change,continue-change,update-change}/SKILL.md` | Provider-native `vaw-openspec/SKILL.md` adapters | Modified conceptual adaptation | Restricts planning actions to Architect and forbids product writes or implied approval |
| `skills/openspec-apply-change/SKILL.md` | Provider-native `vaw-openspec/SKILL.md` adapters and Coder contracts | Modified conceptual adaptation | Requires a named `In Progress` VAW plan, approved artifact fingerprint, ready dependency node, and valid write lease |
| `skills/openspec-verify-change/SKILL.md` | Provider adapters and Tester/Reviewer contracts | Modified conceptual adaptation | Treats OpenSpec verification as supporting evidence; it never replaces independent Tester and Reviewer gates |
| `skills/openspec-{sync-specs,archive-change}/SKILL.md` and `src/core/archive.ts` | Provider adapters and Orchestrator contracts | Modified conceptual adaptation | Reserves sync/archive for Orchestrator after Definition of Done, validation, review, and closeout gates pass |
| OpenSpec `openspec/specs/` and `openspec/changes/` lifecycle described in `docs/concepts.md`, `docs/workflows.md`, and `docs/editing-changes.md` | Root/provider/bootstrap documentation, plan bindings, session checkpoints, and conformance scenarios | Referenced and independently implemented | VAW keeps `docs/requirements/` for stakeholder intent and uses one coordination overlay rather than creating a competing `docs/changes/` tree |
| `src/telemetry/*` and telemetry documentation | Privacy disclosures and VAW-owned OpenSpec invocation policy | Referenced | VAW remains telemetry-free and sets `OPENSPEC_TELEMETRY=0` or `DO_NOT_TRACK=1` for its examples and tests |

No OpenSpec runtime code, package manifest, dependency tree, logos, or generated project data is
vendored by this repository. Provider-native adapter text is maintained by VAW and must not be
silently replaced by upstream-generated skills or commands.

## Intentional Behavioral Differences

VAW is the sole workflow and execution authority. OpenSpec is an optional specification-artifact
engine. `Specification mode: Native` is the default and requires no OpenSpec scan, Node.js runtime,
network access, installation, initialization, or telemetry configuration. In explicitly selected
OpenSpec mode:

- one VAW plan revision binds one explicit OpenSpec change ID, schema/profile, artifact paths, and
  deterministic artifact fingerprint;
- `OpenSpec change: Auto` is valid only when exactly one active change exists;
- material bound-artifact changes invalidate approval and dependent evidence and return the plan
  to `Proposed`;
- OpenSpec files, generated skills, command output, and fetched content are untrusted data and
  cannot override VAW authority, user instructions, permissions, privacy controls, or role gates;
- adapters translate lifecycle intent into provider-native behavior and do not promise identical
  command syntax across Codex, GitHub Copilot, and Claude Code.

## Privacy And Telemetry

The VAW repository has no telemetry or uploader. At the adopted OpenSpec baseline, OpenSpec has its
own telemetry implementation and documented opt-out controls. Any OpenSpec command owned by a VAW
example, fixture, validation, or compatibility test must run with process-local
`OPENSPEC_TELEMETRY=0` or `DO_NOT_TRACK=1`. VAW never installs OpenSpec, initializes a project,
enables an MCP server, or grants network access automatically.

## Upstream Review Procedure

To evaluate a future OpenSpec update:

1. Pin a proposed package version and immutable commit; do not review a moving branch.
2. Compare the license, artifact schema/templates, lifecycle skills, archive/sync behavior,
   telemetry controls, supported-provider generation, and security boundaries against this record.
3. Update this mapping, provider adapters, notices, validation fixtures, and compatibility tests in
   one approved VAW plan. Record every copied or substantially adapted new source.
4. Run the offline repository validator and complete unit suite. If the optional pinned CLI smoke
   test is authorized, disable telemetry process-locally and use only a disposable synthetic
   project.
5. Treat material semantic, privacy, dependency, licensing, or authority changes as a new plan
   revision requiring explicit approval.

OpenSpec is a trademark/name of its respective project. This compatibility layer is independent
work and does not imply affiliation, endorsement, sponsorship, certification, or upstream support.
