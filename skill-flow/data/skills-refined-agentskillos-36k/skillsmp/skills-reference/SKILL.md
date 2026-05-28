---
name: skills-reference
description: Claude Code skills (Agent Skills) configuration reference. Use when creating skills, understanding skill activation, SKILL.md format, user-invoked vs model-invoked skills, or skill best practices.
---

# Claude Code Skills Reference

Skills extend Claude's capabilities. They're defined as Markdown files that Claude loads when needed.

## Two Types of Skills

| Type | Trigger | Use Case |
|------|---------|----------|
| **Model-invoked** | Claude decides automatically | Reference docs, specialized knowledge |
| **User-invoked** | User types `/skill-name` | Workflows, actions with side effects |

## Skill File Structure

```
~/.claude/skills/           # User skills (all projects)
.claude/skills/             # Project skills (team shared)

skill-name/
├── SKILL.md               # Required: skill definition
├── reference.md           # Optional: additional docs
└── scripts/               # Optional: supporting files
```

## SKILL.md Format

```markdown
---
name: my-skill
description: What this skill does and when Claude should use it
user_invocable: false
model: sonnet
tools:
  - Read
  - Bash
---

# Skill Title

Instructions Claude follows when this skill is activated.

## When to Use

Describe scenarios when this skill applies.

## How to Execute

Step-by-step instructions for Claude.
```

## Frontmatter Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Skill identifier |
| `description` | Yes | string | When/why to use this skill |
| `user_invocable` | No | boolean | Allow `/skill-name` invocation |
| `model` | No | string | Model to use (haiku, sonnet, opus) |
| `tools` | No | array | Restrict available tools |
| `allowed_tools` | No | array | Alias for `tools` |

## Model-Invoked Skills

Claude automatically uses these when the task matches the description.

```markdown
---
name: python-debugging
description: Debug Python code. Use when user encounters Python errors, exceptions, or unexpected behavior.
---

# Python Debugging

When debugging Python code:
1. Read the error traceback carefully
2. Identify the failing line and function
3. Check variable types and values
...
```

## User-Invoked Skills

User explicitly triggers with `/skill-name`.

```markdown
---
name: deploy
description: Deploy to production environment
user_invocable: true
---

# Deploy Workflow

1. Run tests: `npm test`
2. Build: `npm run build`
3. Deploy: `npm run deploy`
```

## Skill with Tool Restrictions

```markdown
---
name: readonly-analyzer
description: Analyze code without modifications
tools:
  - Read
  - Glob
  - Grep
---

# Read-Only Analysis

Analyze codebase patterns without making changes.
```

## Skill Activation

**Model-invoked activation**:
- Claude checks skill descriptions against current task
- Matching skills are loaded into context
- Claude follows skill instructions

**User-invoked activation**:
- User types `/skill-name`
- Skill is loaded immediately
- Claude executes skill instructions

## Best Practices

1. **Clear descriptions**: Be specific about when the skill applies
2. **Progressive disclosure**: Keep SKILL.md concise, reference external docs
3. **Single responsibility**: One skill per task type
4. **Limit scope**: Use tool restrictions for safety
5. **Test thoroughly**: Verify skill activates correctly

## Example: Reference Skill (Model-Invoked)

```markdown
---
name: api-patterns
description: REST API design patterns. Use when designing APIs, endpoints, or discussing HTTP conventions.
---

# REST API Patterns

Quick reference for API design.

## Endpoint Naming
- Use nouns: `/users`, `/orders`
- Use plural: `/users/123` not `/user/123`
...

For complete API design guide, see [api-full.md](api-full.md).
```

## Example: Workflow Skill (User-Invoked)

```markdown
---
name: commit
description: Create git commits with conventional format
user_invocable: true
---

# Commit Workflow

1. Check status: `git status`
2. Review changes: `git diff`
3. Stage files: `git add <files>`
4. Commit with message following conventional commits
```

## Debugging Skills

```bash
# List all skills
/skills

# Check if skill is loaded
# Look for skill in available skills list

# Test skill description matching
# Ask Claude a question that should trigger the skill
```

---

For complete documentation, see:
- [skills-full.md](skills-full.md) - Complete skills reference
- [skills-best-practices.md](skills-best-practices.md) - Authoring guidelines
