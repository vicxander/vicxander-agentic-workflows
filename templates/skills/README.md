# Skill Templates

The source stores skill templates in this shape; native discovery requires verified mapping:

```text
templates/skills/
  lowercase-kebab-skill-name/
    SKILL.md
    optional-scripts-or-references
```

Each `SKILL.md` uses YAML frontmatter and Markdown instructions. Native command naming and frontmatter must be verified before generation. A clear description
helps identify when a skill applies.

This source includes a workflow skill template; native activation is not assumed. To add another skill, copy
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
