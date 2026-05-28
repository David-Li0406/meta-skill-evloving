---
name: create-command
description: Create new Claude Code slash commands. Use when the user wants to create a new slash command, add a custom command, or automate a workflow with a /command.
allowed-tools:
  - Read
  - Write
  - Bash(mkdir:*)
  - Glob
---

# Creating Claude Code Slash Commands

## Overview

Slash commands are Markdown files with optional YAML frontmatter that define reusable prompts.

## File Locations

| Type | Location | Scope |
|------|----------|-------|
| Project commands | `.claude/commands/` | Shared with team via version control |
| Personal commands | `~/.claude/commands/` | Private, available in all projects |

Command name derives from filename: `optimize.md` → `/optimize`

## Template

```markdown
---
allowed-tools: Tool1, Tool2(pattern:*)
argument-hint: [expected-input]
description: Brief description shown in /help
---

## Context
[Dynamic content providing current state]

## Constraints
[Rules and limitations]

## Task
[Clear, specific instructions]
```

## Frontmatter Fields

| Field | Purpose | Default |
|-------|---------|---------|
| `allowed-tools` | Tools the command can use | Inherits from session |
| `argument-hint` | Hint shown in autocomplete | None |
| `description` | One-line description for `/help` | First line of content |
| `model` | Model to use (e.g., `claude-sonnet-4-20250514`) | Inherits from session |
| `context` | Set to `fork` for isolated sub-agent | Inline |
| `agent` | Agent type when `context: fork` | `general-purpose` |

## Arguments

### `$ARGUMENTS` - All Input
Use for free-form or variable-length input:
```markdown
Search the codebase for: $ARGUMENTS
```
Usage: `/search auth flow` → `$ARGUMENTS` = `"auth flow"`

### `$1`, `$2`, `$3` - Positional
Use for distinct, ordered parameters:
```markdown
Create component `$1` with variant `$2`.
```
Usage: `/component Button primary` → `$1` = `"Button"`, `$2` = `"primary"`

## Dynamic Content

### Bash Execution: `!`backticks
```markdown
- **Branch**: !`git branch --show-current`
- **Status**: !`git status --short`
```

### File References: `@path`
```markdown
@package.json
@src/config.ts
```

## Tool Permission Patterns

| Pattern | Meaning |
|---------|---------|
| `Read` | Allow all file reads |
| `Edit` | Allow all file edits |
| `Bash(git:*)` | Allow git commands only |
| `Bash(npm test:*)` | Allow npm test variations |
| `Read, Grep, Glob` | Multiple read-only tools |

## Best Practices

1. **Always include `description`** - Makes commands discoverable
2. **Use `allowed-tools` for safety** - Restrict to necessary tools only
3. **Use `argument-hint`** - Helps users understand expected input
4. **Be specific with Bash** - `Bash(git status:*)` safer than `Bash`
5. **Handle errors in bash** - Use `|| echo "fallback"`

## Workflow

1. Ask where to create the command (project or personal)
2. Ask for the command name and purpose
3. Determine required tools and arguments
4. Create the file with appropriate frontmatter and prompt content
5. Test with `chezmoi cat` if in chezmoi repo, or verify file exists
