---
name: resolve-unknown-patterns
description: Resolve unknown patterns by converting them into concrete reskin instructions and removing the unknown-patterns entry.
---

# Resolve Unknown Patterns

Use this skill when the goal is to eliminate one or more entries in `docs/refactor-plan/unknown-patterns/` by turning them into concrete reskin instructions.

## Workflow

1) Identify the target pattern(s)
- Read `docs/refactor-plan/unknown-patterns/README.md` and open the specific pattern file(s).
- Confirm the “Difference summary” and the affected services/repos.

2) Choose where instructions should live
- Prefer `docs/refactor-plan/gl-ap-playbooks.md` for service/repository patterns.
- Use `docs/refactor-plan/refactor-plan.md` or `docs/refactor-plan/reskin-definition.md` for cross-cutting rules.
- If the pattern affects agent behavior, update `.github/copilot-instructions.md` as well.

3) Write concrete, actionable instructions
- Add a new playbook or subsection with explicit steps and constraints.
- Call out required base DTOs/interfaces and boundaries (MVC shim vs. core) when relevant.
- Keep examples short and path-specific.

4) Validate coverage
- Ensure the new instructions directly address the unknown pattern’s “Difference summary.”
- Keep the guidance minimal but unambiguous.

5) Remove the unknown pattern entry
- Delete the pattern file.
- Remove the entry from `docs/refactor-plan/unknown-patterns/README.md`.

6) Report
- List updated docs and removed files.

## Guardrails
- Do not delete an unknown pattern unless the new instructions clearly resolve it.
- Avoid creating new documentation unless existing reskin docs are a poor fit.
- Keep instructions aligned with AGENTS/Copilot and reskin standards.
