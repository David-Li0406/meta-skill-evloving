---
name: create-subagent
description: Use this skill when you want to create custom subagents for specialized AI tasks, such as configuring task-specific agents or domain-specific assistants with tailored prompts.
---

# Creating Custom Subagents

This skill guides you through creating custom subagents for Cursor. Subagents are specialized AI assistants that run in isolated contexts with custom system prompts.

## When to Use Subagents

Subagents help you:
- **Preserve context** by isolating exploration from your main conversation.
- **Specialize behavior** with focused system prompts for specific domains.
- **Reuse configurations** across projects with user-level subagents.

### Inferring from Context

If you have previous conversation context, infer the subagent's purpose and behavior from what was discussed. Create the subagent based on specialized tasks or workflows that emerged in the conversation.

## Subagent Locations

| Location | Scope | Priority |
|----------|-------|----------|
| `.cursor/agents/` | Current project | Higher |
| `~/.cursor/agents/` | All your projects | Lower |

When multiple subagents share the same name, the higher-priority location wins.

**Project subagents** (`.cursor/agents/`): Ideal for codebase-specific agents. Check into version control to share with your team.

**User subagents** (`~/.cursor/agents/`): Personal agents available across all your projects.

## Subagent File Format

Create a `.md` file with YAML frontmatter and a markdown body (the system prompt):

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
---

You are a code reviewer. When invoked, analyze the code and provide specific, actionable feedback on quality, security, and best practices.
```

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier (lowercase letters and hyphens only). |
| `description` | When to delegate to this subagent (be specific!). |

## Writing Effective Descriptions

The description is **critical** - the AI uses it to decide when to delegate.

```yaml
# ❌ Too vague
description: Helps with code

# ✅ Specific and actionable
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
```

Include "use proactively" to encourage automatic delegation.

## Example Subagents

### Code Reviewer
```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
---
```