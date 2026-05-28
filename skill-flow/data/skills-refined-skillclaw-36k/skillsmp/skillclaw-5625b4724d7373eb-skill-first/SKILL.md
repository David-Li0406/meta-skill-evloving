---
name: skill-first
description: Use this skill when starting any task to ensure you are leveraging existing skills for effective and consistent work.
---

# Skill-First Discipline

Before responding to any user request, check if a matching skill exists.

## Checklist

1. **Scan available skills** - Review the skills listed in your skills directory.
2. **Match request to skill** - Determine if any skill covers the task type.
3. **Load if matched** - Use the `Skill` tool to load the relevant skill.
4. **Announce usage** - Inform the user: "I'm using [skill-name] to [action]."
5. **Follow exactly** - Execute the skill's guidance without deviation.

## Rationalizations to Reject

If you find yourself considering the following, stop and check for skills:

- "This is simple, I don't need a skill."
- "I'll just do this quickly."
- "The skill is overkill."
- "I already know how to do this."

These are failure modes. If a skill exists for your task, use it.

## Discovering Available Skills

To list skills programmatically, use:
```bash
find ~/.claude -path "*/skills/*/SKILL.md" 2>/dev/null | xargs -I{} grep "^name:" {}
```

## When to Skip

Skip skill usage only when:
- Answering factual questions (no task involved).
- Providing simple clarifications.
- The user explicitly declines skill usage.

For everything else, skill-first is mandatory.