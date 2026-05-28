---
name: creating-skills
description: Create high-quality Claude Code skills with proper structure, effective descriptions, and best practices. Use when creating a new skill, writing SKILL.md files, setting up skill directories, or asking how to make skills.
allowed-tools: Read, Write, Bash(mkdir:*), Glob
---

# Creating Claude Code Skills

A meta-skill for creating well-structured, discoverable, and effective Claude Code skills.

## Overview

Claude Skills are markdown files that teach Claude specialized knowledge. They're **automatically discovered** based on their description, so writing effective descriptions is critical.

## Quick Start

1. **Choose location** based on scope:
   - Personal: `~/.claude/skills/your-skill/`
   - Project: `.claude/skills/your-skill/`

2. **Create directory and SKILL.md**:
   ```bash
   mkdir -p .claude/skills/your-skill
   ```

3. **Write SKILL.md** with required frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: [Trigger-rich description]
   ---
   ```

4. **Validate** using [CHECKLIST.md](CHECKLIST.md)

## The Golden Rule: Description Is Everything

Claude uses the `description` field to decide when to apply your skill. A poor description means your skill never triggers.

### Description Formula

```
[What it does] + [Specific capabilities] + [Trigger phrases]
```

### Bad vs Good Descriptions

| Bad | Good |
|-----|------|
| "Helps with testing" | "Write and run unit tests for TypeScript. Use when creating tests, mocking dependencies, or improving test coverage." |
| "Database helper" | "Generate SQL migrations and queries for PostgreSQL. Use when creating tables, writing queries, or migrating schemas." |
| "Code review" | "Review code for bugs, security issues, and style violations. Use when reviewing PRs, auditing code, or checking for vulnerabilities." |

## Skill Structure

### Minimal (Single File)

```
your-skill/
└── SKILL.md
```

### Standard (With Supporting Docs)

```
your-skill/
├── SKILL.md           # Overview + quick start (< 500 lines)
├── REFERENCE.md       # Detailed documentation
├── EXAMPLES.md        # Usage examples
└── CHECKLIST.md       # Validation checklist
```

### Advanced (With Scripts)

```
your-skill/
├── SKILL.md
├── docs/
│   ├── api.md
│   └── patterns.md
└── scripts/
    ├── setup.sh       # Executed, not loaded as context
    └── validate.py
```

## SKILL.md Template

See [TEMPLATES.md](TEMPLATES.md) for ready-to-use templates.

```yaml
---
name: skill-name              # Lowercase, hyphens only (max 64 chars)
description: [description]    # Max 1024 chars - MOST IMPORTANT FIELD
allowed-tools: Read, Grep     # Optional - restrict tool access
---

# Skill Name

## Overview
[1-2 sentence summary of what this skill does]

## When to Use
[Specific scenarios, triggers, and use cases]

## Instructions
[Step-by-step guidance - numbered for clarity]

## Examples
[Concrete usage examples with expected outcomes]

## Resources
[Links to supporting files if applicable]
```

## Tool Restrictions

Use `allowed-tools` to limit Claude's capabilities when the skill is active:

```yaml
# Read-only skill
allowed-tools: Read, Grep, Glob

# Python automation only
allowed-tools: Bash(python:*)

# Multiple specific commands
allowed-tools: Read, Bash(git:*, npm:*, pnpm:*)
```

**When to restrict:**
- Read-only analysis (prevent accidental writes)
- Specific tooling (Python scripts, Git operations)
- Security-sensitive workflows

## Progressive Disclosure

Keep SKILL.md focused. Link to supporting files for detail:

```markdown
## Quick Reference
[Essential info here]

## Detailed Documentation
For complete API reference, see [REFERENCE.md](REFERENCE.md).
For troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
```

**Why it matters:**
- Claude loads SKILL.md first
- Supporting files load on-demand
- Keeps context focused for better performance
- Scripts execute without consuming tokens

## Common Mistakes to Avoid

1. **Vague descriptions** - Include specific trigger keywords
2. **Too broad scope** - One skill = one purpose
3. **Missing dependencies** - Document required packages
4. **No examples** - Always include concrete usage
5. **Monolithic SKILL.md** - Use progressive disclosure for >500 lines
6. **Similar descriptions** - Make each skill's description distinct

## Quality Checklist

Use [CHECKLIST.md](CHECKLIST.md) to validate your skill before committing.

## Examples

See [EXAMPLES.md](EXAMPLES.md) for complete, production-ready skill examples.
