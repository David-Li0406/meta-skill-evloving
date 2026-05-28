---
name: skill-authoring
description: Create or update repo skills under .claude/skills. Use when adding new skills, editing SKILL.md, or deciding what should be a skill vs a spec/doc.
---

# Skill Authoring (repo conventions)

## When to use a skill

- Use skills for procedural workflows and package conventions that are not always‑on.
- Keep specs/APIs/algorithms in conventional docs; reference them from skills.

## Where skills live

- Repo skills are committed under `.claude/skills/<skill-name>/SKILL.md`.
- Do not modify `~/.claude/skills` (global).

## Authoring guidance

- Keep SKILL.md lean; move large details into `references/`.
- Avoid extra docs like README.md inside skills.

## Naming

- Use lowercase letters, digits, and hyphens.
- Name the folder exactly after the skill name.

## Editing onboarding materials (CLAUDE.md, skills)

Every future agent reads these files and acts on their content. There will be many future sessions, so errors here have high cost.

1. Always add `[proposed]` markers when editing these files
2. Show changes to Jörn; remove markers only after clear approval
3. Ambiguous responses ("sounds fine, I guess") mean "I see it" not "remove the markers"
