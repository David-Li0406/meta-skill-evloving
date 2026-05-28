---
name: slash-command-creator
description: Use this skill when creating, updating, or documenting Claude Code slash commands to automate workflows and improve efficiency.
---

# Slash Command Creator

This skill guides you through the process of creating and managing Claude Code slash commands, which are reusable workflows invoked with `/command-name` in Claude Code conversations.

## About Slash Commands

Slash commands are markdown files stored in `.claude/commands/` (project-level) or `~/.claude/commands/` (global/user-level) that expand into prompts when invoked. They are ideal for:

- Automating repetitive workflows (e.g., code review, PR submission)
- Ensuring consistency in multi-step processes
- Facilitating agent delegation patterns
- Implementing project-specific automation

## When to Use This Skill

Invoke this skill when you:

- Want to create or update a slash command
- Need to document a consistent process for reuse
- Ask about slash command syntax, frontmatter options, or best practices
- Say "I keep doing X, can we make a command for it?"

## Command Structure Overview

Every slash command is a markdown file with the following structure:

```markdown
---
description: Brief description shown in /help (required)
allowed-tools: [Bash, Read, Write]  # Optional
argument-hint: <placeholder> (optional, if command takes arguments)
---

# Command Title

[Detailed instructions for the agent to execute autonomously]
```

## Command Creation Workflow

### Step 1: Determine Location

**Auto-detect the appropriate location:**

1. Check if inside a git repository: `git rev-parse --is-inside-work-tree 2>/dev/null`
2. Default location:
   - If in a git repo → Project-level: `.claude/commands/`
   - If not in a git repo → Global: `~/.claude/commands/`
3. Allow user override:
   - If user explicitly mentions "global" or "user-level" → save accordingly.

### Step 2: Create the Command

To create a new command, initialize it with:

```bash
scripts/init_command.py <command-name> [--scope project|personal]
```

### Step 3: Validate the Command

Always run validation after creating or modifying a command:

```sh
uv run .claude/skills/meta-command-creator/scripts/validate-command.py .claude/commands/<command-name>.md
```

Fix any errors before committing.

## Examples

### Project Command

```bash
mkdir -p .claude/commands
cat > .claude/commands/my-command.md << 'EOF'
---
description: Brief description of what this command does.
allowed-tools: [Bash]
---

## Steps

1. First action
2. Second action
3. Final action
EOF
```

### Personal Command

```bash
mkdir -p ~/.claude/commands
cat > ~/.claude/commands/my-personal-command.md << 'EOF'
---
description: Brief description of what this command does.
allowed-tools: [Read]
---

## Steps

1. First action
2. Second action
3. Final action
EOF
```

## Additional Resources

This skill includes reference documentation for detailed guidance on command patterns, examples, and best practices. Load these references as needed to ensure quality and consistency in your commands.