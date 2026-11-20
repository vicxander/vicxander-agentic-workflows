# Codex Project Skills

Codex discovers repository skills from `.agents/skills/<skill-name>/SKILL.md`.

## Add A Skill

1. Copy `SKILL-TEMPLATE.md` to `.agents/skills/<skill-name>/SKILL.md`.
2. Replace the placeholder `name` and `description`.
3. Keep the directory and frontmatter `name` in descriptive lowercase kebab case.
4. Make the description state when the skill should and should not trigger.
5. Add only the instructions, references, assets, or scripts the workflow needs.
6. Review the skill before trusting the repository or granting tool permissions.

Codex can activate a skill when the user mentions it explicitly or when its description matches the
task. A README or template file at the root of this directory is not itself an active skill.

Useful project skills can cover quality gates, security review, release checks, accessibility,
performance budgets, compliance, or framework-specific conventions. Architect includes applicable
skill requirements in the plan; Coder follows them; Tester runs required checks; Reviewer treats a
missed relevant skill as a finding.

