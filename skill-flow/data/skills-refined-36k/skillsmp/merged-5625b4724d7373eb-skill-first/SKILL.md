---
name: skill-first
description: Use this skill to ensure relevant skills are checked and applied before starting any task.
---

# Skill-First Discipline

Before responding to any user request, check if a matching skill exists.

## Checklist

1. **Scan available skills** - Review the skills in `.claude/skills/`.
2. **Match request to skill** - Determine if any skill covers the task type.
3. **Load if matched** - Use the Skill tool to load the identified skill.
4. **Announce usage** - Inform the user: "I'm using [skill-name] to [action]."
5. **Follow exactly** - Execute the skill's guidance without deviation.

## Rationalizations to Reject

Avoid these thoughts that may lead to skipping skill usage:

- "This is simple, I don't need a skill."
- "I'll just do this quickly."
- "The skill is overkill."
- "I already know how to do this."

If a skill exists for your task, use it.

## When to Skip

You may skip skill usage only when:

- Answering factual questions (no task involved).
- Providing simple clarifications.
- The user explicitly declines skill usage.

For all other scenarios, skill-first is mandatory.

## Why Use Skills

Skills represent tested approaches that:

- Provide consistent patterns across projects.
- Include important safety checks.
- Prevent common mistakes.
- Save time by avoiding rework.

## Skill Categories

### Core Workflow
- `brainstorming` - Discuss approach before implementation.
- `writing-plans` - Break work into tasks.
- `executing-plans` - Execute with verification.
- `code-review` - Review before completing.

### Safety
- `database-backup` - Backup before database operations.
- `verification-before-completion` - Final checks before declaring done.

### Testing
- `test-driven-development` - Write tests first.
- `condition-based-waiting` - Avoid flaky tests.
- `testing-anti-patterns` - Common mistakes to avoid.

### Workflow
- `git-workflow` - Branching and commits.
- `git-worktrees` - Parallel development.

## Skill Discovery

| Task | Relevant Skills |
|------|-----------------|
| Starting a new feature | brainstorming → writing-plans |
| Running tests/migrations | database-backup |
| Adding functionality | test-driven-development |
| Finishing work | code-review → verification-before-completion |
| Multiple features | git-worktrees |

## Tips

- Read the skill file rather than relying on memory.
- Announce which skill you're using for transparency.
- Follow the skill's checklist if it has one.
- Skills work best when used consistently.

## Discovering Available Skills

To list skills programmatically:
```bash
find ~/.claude -path "*/skills/*/SKILL.md" 2>/dev/null | xargs -I{} grep "^name:" {}
```

For a complete list of available skills, see `.claude/skills/README.md`.