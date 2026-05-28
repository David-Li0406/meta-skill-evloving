---
name: using-skills
description: "Core skill for understanding and using the Jarvis skill system. Loaded at every session start."
type: meta
priority: critical
---

# Using Skills

<CRITICAL>
If there is even a 1% chance a skill applies to your task, you MUST invoke it using the Skill tool.
This is not optional. This is not negotiable. Skills contain critical workflows not in your base context.
</CRITICAL>

## The Rule

**Invoke relevant skills BEFORE any response or action.**

```
User message received
    |
    v
Might any skill apply? (even 1% chance)
    |
    +--> YES --> Invoke Skill tool --> Follow skill instructions
    |
    +--> NO --> Respond directly
```

## How to Access Skills

**In Claude Code:** Use the `Skill` tool. When you invoke a skill, its content is loaded for you to follow.

Never use the Read tool on skill files. Always use the Skill tool.

## Red Flags

These thoughts mean STOP - you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can handle this quickly" | Speed without skills = missed protocols. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |

## Skill Priority

When multiple skills could apply:

1. **Process skills first** (TDD, debugging, brainstorming) - determine HOW to approach
2. **Domain skills second** (git, infra, frontend) - provide specific guidance

Examples:
- "Let's build X" -> brainstorming first, then implementation skills
- "Fix this bug" -> debug first, then domain skills
- "Implement feature Y" -> TDD skill, then relevant domain skills

## Skill Types

**Rigid** (TDD, debugging): Follow exactly. Don't adapt away discipline.

**Flexible** (patterns, domain): Adapt principles to context.

The skill content tells you which.

## Core Skills

| Skill | When to Use |
|-------|-------------|
| session | Multi-step implementations, features, refactoring |
| test-driven-development | Any code that needs tests (most code) |
| debug | Errors, bugs, things not working |
| git-expert | Commits, branches, PRs, version control |
| codebase-navigation | Finding files, understanding structure |
| documentation-research | Looking up library docs, APIs |

## Session Workflow

Most significant work follows this pattern:

1. Load relevant skills
2. Create/update session file (.claude/tasks/session-*.md)
3. Execute with skill guidance
4. Commit with proper format
5. Update session status
