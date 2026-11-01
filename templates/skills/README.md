# target tool Project Skills

target tool discovers project skills in this shape:

```text
templates/skills/
  lowercase-kebab-skill-name/
    SKILL.md
    optional-scripts-or-references
```

Each `SKILL.md` uses YAML frontmatter and Markdown instructions. The directory name becomes the
slash command. A clear `description` helps target tool decide when the skill applies.

This sample includes the active `/agentic-workflow` skill. To add another skill, copy
`SKILL-TEMPLATE.md` into a new lowercase kebab-case directory as `SKILL.md`, then replace every
placeholder.

Use skills for detailed task-specific guidance such as:

- quality gates
- security review
- release checklists
- accessibility
- performance budgets
- framework conventions
- compliance checks

Durable rules relevant to nearly every task belong in `templates/project-instructions.md`, not a skill.

## Safety

- Review third-party skills, scripts, and references before use.
- Omit `allowed-tools` unless pre-approval is intentional and necessary.
- Never pre-approve shell execution for an untrusted skill.
- Do not place secrets in skills or supporting files.
- Use `disable-model-invocation: true` for sensitive task skills that only the user should invoke.

## Role Responsibilities

- Orchestrator discovers relevant skills.
- Architect lists them in the plan.
- Coder implements their requirements.
- Tester performs their validation.
- Reviewer reports missed relevant requirements.
