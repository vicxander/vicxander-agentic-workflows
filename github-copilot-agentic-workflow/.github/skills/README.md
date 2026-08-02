# GitHub Copilot Project Skills

GitHub Copilot discovers project skills in this shape:

```text
.github/skills/
  lowercase-kebab-skill-name/
    SKILL.md
    optional-scripts-or-references
```

Each `SKILL.md` requires YAML frontmatter containing a lowercase `name` and a `description` that
states what the skill does and when Copilot should use it. Copy `SKILL-TEMPLATE.md` into a new skill
directory as `SKILL.md`, then replace every placeholder.

Use skills for detailed, task-specific guidance such as:

- quality gates
- security review
- release checklists
- accessibility
- performance budgets
- framework conventions
- compliance checks

Repository-wide rules belong in `AGENTS.md` or `.github/copilot-instructions.md`, not in a skill.

The distribution includes `.github/skills/vaw-openspec/SKILL.md`, a VAW-owned adapter used only
when `Specification mode: OpenSpec` is explicitly selected. It maps OpenSpec artifact intents to
VAW roles and gates; it does not install or initialize OpenSpec and remains authoritative over any
upstream generated `openspec-*` skill for end-to-end coordination.

## Safety

- Review third-party skills before installing them.
- Skills may contain scripts or prompt instructions.
- Omit `allowed-tools` unless automatic tool approval is genuinely necessary.
- Never pre-approve shell execution for an untrusted skill.
- Do not place secrets in skills, scripts, examples, or references.

## Agent Responsibilities

- Orchestrator discovers relevant skills.
- Architect lists applicable skills in the implementation plan.
- Coder implements their requirements.
- Tester performs their required validation.
- Reviewer reports missed relevant skill requirements.
- A relevant skill that cannot be satisfied is a blocker, not an implicit waiver.
