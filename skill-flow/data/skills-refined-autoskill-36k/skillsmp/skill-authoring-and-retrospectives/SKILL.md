---
name: skill-authoring-and-retrospectives
description: How to write/update .claude/skills and capture durable OpenEvent learnings via retrospectives.
---

## When to use
- Creating or updating any `.claude/skills/*/SKILL.md` in this repo.
- Finishing a non-trivial change and needing to capture durable workflow learnings.

## What goes where (rubric)
- Skill: durable, repo-specific guidance (canonical vocabulary, file maps, stable commands, recurring pitfalls, debugging playbooks).
- CLAUDE.md: short policy and pointers to Skills, no detailed workflow content.
- Docs: longer explanations, architecture, and team-wide narrative (link from Skills).

## Naming + description rules
- Skill folder name and `name` must match and use lowercase letters, digits, and hyphens.
- `description` should include user keywords (e.g., "email workflow", "offer", "HIL") to help trigger usage.
- Keep SKILL.md concise; use progressive disclosure by linking to existing docs or code.

## Retrospective protocol
After meaningful work, extract reusable learnings into Skills:
1) Prefer updating an existing Skill with a new note or pitfall.
2) Create a new Skill only if the guidance will be reused.
3) Use the automated path when possible:
   - `python scripts/skills/retrospective.py --skill <existing-skill> --input <note.md> --write`
   - `cat note.md | python scripts/skills/retrospective.py --skill <existing-skill> --write`
   - For new skills: `python scripts/skills/retrospective.py --new-skill <name> --description "..." --input <note.md> --write`
4) Validate before committing: `python scripts/skills/validate_skills.py`.

## Durable learning definition
- Stable commands or test lanes (not one-off debug commands).
- Recurring pitfalls or regressions and how to avoid them.
- Repo-specific conventions (workflow step names, HIL gating rules, data contracts).
- Debugging playbooks or minimal repro paths tied to canonical files.

## Retrospective Notes
- Add durable learnings here via `scripts/skills/retrospective.py`.
