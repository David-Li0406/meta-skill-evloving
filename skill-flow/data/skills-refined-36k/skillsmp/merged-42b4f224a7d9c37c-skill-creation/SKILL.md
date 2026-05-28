---
name: skill-creation
description: Use this skill when the user asks to create a new skill, add a command, or extend Claude capabilities.
---

# How to Create Skills and Agents in Claude Code

Skills and agents are capabilities that Claude uses based on context relevance and user requests.

## Directory Structure

```
.claude/skills/<skill-name>/SKILL.md
```

- Each skill lives in its own subdirectory.
- The file MUST be named exactly `SKILL.md` (case-sensitive).
- The directory name can be anything descriptive.

## Required Format for Skills

Every SKILL.md must have YAML frontmatter:

```markdown
---
name: my-skill-name
description: Use this skill when [describe triggers]. [What it does].
---

# Skill Title

[Instructions for Claude on how to use this skill]
```

### YAML Frontmatter Fields

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Identifier for the skill (kebab-case) |
| `description` | Yes | Tells Claude WHEN to auto-trigger this skill |

### The Description Field is Critical

The `description` determines when Claude automatically uses the skill. Write it as:
- "Use this skill when [specific triggers]"
- Be specific about contexts that should activate it
- Include key phrases the user might say

## Quick Start for Creating a Skill

1. **Create directory**: `.claude/skills/<skill-name>/`
2. **Add SKILL.md** with YAML frontmatter and instructions.
3. **Test**: Invoke with `/skill-name` or describe the trigger scenario.

### Example: Creating a New Skill

To create a skill for database operations:

1. Create directory: `.claude/skills/database-ops/`
2. Create file: `.claude/skills/database-ops/SKILL.md`
3. Add content:

```markdown
---
name: database-operations
description: Use this skill when working with database queries, migrations, or schema changes in this project.
---

# Database Operations

## When to Use
- Running migrations
- Writing queries
- Modifying schema

## Instructions
[Detailed instructions for Claude...]
```

4. Restart Claude Code to load the skill.

## Creating an Agent

1. **Create file**: `.claude/agents/<agent-name>.md`
2. **Add YAML frontmatter** with name, description (with examples), and tools.
3. **Write system prompt** defining persona, responsibilities, and output format.

### Skill Template

```markdown
---
name: skill-name
description: This skill should be used when the user asks to "trigger phrase 1", "trigger phrase 2", or "trigger phrase 3". Be specific about when to activate.
disable-model-invocation: true # Set true for side effects (deploy, commit)
allowed-tools: Read, Grep, Glob # Restrict tools if needed
---

# /skill-name

Brief description of what this skill does.

## Instructions

1. First step - what to do
2. Second step - what to do
3. Third step - what to do

## Examples

Input: `$ARGUMENTS`
Expected output: ...
```

## Best Practices Checklist

**Skills:**

- [ ] Description uses third-person ("This skill should be used when...")
- [ ] Includes exact trigger phrases in quotes.
- [ ] Has `disable-model-invocation: true` if it has side effects.
- [ ] Instructions are step-by-step and actionable.
- [ ] Under 500 lines (use supporting files for details).

**Agents:**

- [ ] Description includes `<example>` blocks with `<commentary>`.
- [ ] Tools array contains only what's needed.
- [ ] System prompt uses second person ("You are...").
- [ ] Defines clear output format.
- [ ] Has quality criteria or success conditions.

## Common Mistakes to Avoid

1. **Wrong filename**: Must be `SKILL.md`, not `skill.md` or `<name>.md`.
2. **Missing frontmatter**: The `---` YAML block is required.
3. **File in wrong location**: Must be in a subdirectory, not directly in `.claude/skills/`.
4. **Vague description**: Be specific about when to trigger.
5. **Forgetting to restart**: Claude Code needs restart to load new skills.

## Reference

See `.claude/AGENT_CLAUDE.md` for comprehensive guidelines on skill and agent development.