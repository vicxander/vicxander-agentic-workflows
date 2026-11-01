# VicXander Agentic Workflows

Provider-neutral, adaptive, approval-gated workflow specifications by Victor Alexander Daud.
Workflow contract version: 3.0.0.

Read workflow/principles.md and workflow/orchestration.md for normative behavior, workflow/roles/
for responsibilities, and workflow/capabilities.md for verified target mapping. Templates contain
reusable project guidance. Native configurations are generated only after target verification.

## Initialize

Provide the source path, destination path, coding tool name/version and create or dry-run mode.
Ask the assistant to read bootstrap/INITIALIZE.md and verify the selected tool's conventions.
A supplied tool name does not establish compatibility. Missing evidence blocks configuration writes.

## Update An Existing Installation

Keep a checkpoint and backup of ignored state. Existing users may retain their prior release.
The 3.0.0 source layout removes bundled distributions and legacy bootstrap paths. Installed native
paths and project state must be preserved. Target-specific output belongs only in destination
projects. This architecture does not provide legal clearance or guarantee universal compatibility.

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

## Validation

Run python -B tools/validate_workflows.py, python -B tools/contract_coverage.py,
python -B -m unittest discover -s tools -p "test_*.py", and git diff --check.
Semantic validation is distinct from native format validation and observed runtime acceptance.

## Privacy And License

No telemetry, hosted service or uploader is provided. Optional metrics are local and off by default.
The executing tool and extensions may process data under their own terms and settings. Keep secrets
and sensitive content out of external queries and workflow memory. Preserve the outbound-data rules.

Released under the MIT License. Copyright (c) 2026 Victor Alexander Daud. See LICENSE and CITATION.cff.
