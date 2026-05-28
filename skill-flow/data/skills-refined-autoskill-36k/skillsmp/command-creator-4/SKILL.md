---
name: command-creator
description: Guide for creating Claude Code slash commands. Use when the user wants to create a new slash command, custom prompt shortcut, or workflow automation command for Claude Code. Helps define command structure, frontmatter, arguments, and best practices.
---

# Command Creator

Create effective Claude Code slash commands.

> **⚠️ IMPORTANT**: Before creating any command, fetch the latest official guide:
> https://code.claude.com/docs/en/slash-commands#custom-slash-commands
>
> If any guidance in this skill conflicts with the official documentation, follow the official guide unless the user explicitly requests otherwise.

## About Slash Commands

Slash commands are Markdown files that provide reusable prompts triggered by `/command-name`. They transform frequently-used prompts into quick shortcuts.

### Key Characteristics

- **Single .md file** - Simple and self-contained
- **Triggered explicitly** - User types `/command-name`
- **Supports arguments** - `$ARGUMENTS`, `$1`, `$2`, etc.
- **Supports special syntax** - `!command` for bash output, `@file` for file content

### When to Create a Command vs Skill

| Use Case | Solution |
|----------|----------|
| Frequently-used prompt | Slash Command |
| Multi-step workflow with resources | Skill |
| Quick automation trigger | Slash Command |
| Complex domain expertise | Skill |

## Command Creation Process

### Step 1: Understand the Command Purpose

Gather requirements:

1. What task does the command automate?
2. What arguments does it need?
3. What tools should it have access to?
4. Should it be project-specific or global?

### Step 2: Determine Location

| Scope | Location |
|-------|----------|
| Project (team-shared) | `.claude/commands/` |
| Personal (all projects) | `~/.claude/commands/` |

Use subdirectories for namespacing: `.claude/commands/frontend/component.md` becomes `/frontend/component`

### Step 3: Write the Command

**File Structure:**

```markdown
---
description: Brief description shown in /help
argument-hint: <arg1> [optional-arg]
allowed-tools: Tool1, Tool2(pattern:*)
model: claude-3-5-haiku-20241022
---

Your prompt content here.

Use $ARGUMENTS for all arguments.
Use $1, $2 for positional arguments.
```

**Frontmatter Fields (all optional):**

| Field | Purpose |
|-------|---------|
| `description` | Shown in `/help` output |
| `argument-hint` | Placeholder shown during autocomplete |
| `allowed-tools` | Tools the command can use without prompting |
| `model` | Override default model for this command |

See [references/format.md](references/format.md) for detailed syntax.

### Step 4: Test and Iterate

1. Run the command with various inputs
2. Verify tool permissions work as expected
3. Check edge cases and error handling
4. Refine the prompt based on results

## Best Practices

**Keep commands focused** - One command, one purpose. Combine with other commands for complex workflows.

**Use clear descriptions** - Help users understand what the command does from `/help`.

**Specify minimal permissions** - Only request tools the command actually needs.

**Handle missing arguments** - Provide sensible defaults or clear error messages.

**Prefer imperative voice** - "Analyze the code" not "This command analyzes the code".
