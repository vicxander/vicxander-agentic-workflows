# Agentic Workflow Bootstrap

Initialize or update VicXander Agentic Workflows using an explicit target integration.
This is a manual instruction-driven procedure, not an executable installer.

## Inputs And Supported Integrations

Require a target repository path, workflow source repository path, target integration, and mode.
Resolve product names case-insensitively using this table. The executing assistant may differ
from the selected target. A company name alone is ambiguous: ask which coding tool is intended.
Unsupported names must produce an unsupported-target report before any writes; never invent a
configuration or silently switch targets.

| Target ID | Accepted product name | Source distribution | Native entry point |
| --- | --- | --- | --- |
| codex | Codex | codex-agentic-workflow | AGENTS.md and .codex/config.toml |
| claude | Claude Code | claude-agentic-workflow | CLAUDE.md and .claude/ |
| github-copilot | GitHub Copilot | github-copilot-agentic-workflow | .github/copilot-instructions.md |

The selected distribution must be available alongside this kit in the supplied source repository.
If it is missing, report the missing source and stop before writes. Do not fetch unspecified
remote sources or generate substitute templates. Read the distribution README and native files.

## Modes

- `create`: initialize a repository without an existing workflow; report existing destination
  collisions rather than overwrite them. Inspect hidden directories too.
- `merge`: compare the source with an existing installation and carefully merge missing workflow
  files or sections. Use this mode for upgrades. Repeating a merge must not duplicate sections.
- `dry-run`: inspect and report only. Do not write files, create directories, or update memory.
  List source and destination, proposed creates/merges/preserved files, conflicts, and available
  validation. Specify whether the proposed operation is create or merge.

If no mode is supplied, use create only when no workflow exists; otherwise use merge. Respect
any user-requested approval of a dry-run before applying changes.

## Preservation And Upgrade Rules

1. Inspect project guidance and available version-control state. Recommend a Git checkpoint and
   backup of ignored/untracked workflow state before applying upgrades. Never commit or reset
   user changes automatically.
2. Use the selected distribution's contents as a project root, retaining native filenames,
   formats, role sets, tool declarations, model inheritance, and activation rules. Do not copy its
   README over the target's README. Keep application code and unrelated build files untouched.
3. Preserve project-specific instructions, architecture, commands, quality gates, authority rules,
   and custom skills. Merge workflow sections, not entire customized instruction files. Without
   a prior upstream baseline, report ambiguous differences as conflicts; do not assume they are
   local customizations or resolve them by replacement. Leave unresolved files unchanged.
4. Preserve session notes, todos, worklogs, metrics, role memory, worktrees, active plans,
   requirements, findings, and documentation indexes. Never reset state from empty templates.
5. Preserve unrelated configuration keys and other integrations. Reuse existing shared docs lanes;
   merge missing template guidance without overwriting project documents or duplicating lanes.
6. Preserve the project's LICENSE and all unrelated notices. Create or merge only the missing
   workflow entry into THIRD_PARTY_NOTICES.md as instructed by the distribution README.
7. Preserve the semantic workflow contract: safety, approval, privacy, authority, routing,
   validation, resource governance, and opt-in metrics. Neutral branding never changes capability.

## Validation And Report

Review instruction links, required native files, role names, configuration syntax, and workflow
conformance scenarios from the selected distribution. Use disposable repositories to rehearse
merges when needed. Report changed, preserved, skipped, and conflicted files and checks performed.
Do not claim unexecuted checks passed or that static checks prove an assistant merged correctly.

From the source repository, python -B tools/validate_workflows.py checks the distributions.
Its --bootstrap-target option validates only Codex materializations; it does not validate arbitrary
Claude Code or GitHub Copilot installations. Use their native format checks and conformance
scenarios and report the absence of a general installed-target validator.

Branding-only adoption is optional. Keep native paths during upgrades; no runtime migration is
required. The legacy CODEX_AGENTIC_BOOTSTRAP.md and embedded templates remain a standalone
Codex-specific compatibility path.
