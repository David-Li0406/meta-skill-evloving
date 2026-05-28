---
name: meta:command-creator
description: Create custom slash commands for Claude Code with proper markdown structure and YAML frontmatter. Use when creating commands, generating slash commands, making workflow automations.
---

# Slash Command Creator

## Quick Start

### Step 1: Create the command

```markdown
# .claude/commands/my-command.md

---

description: Brief description of what this command does.

---

## Steps

1. First action
2. Second action
3. Final action
```

Invoke with `/my-command` in Claude Code (shows "(project)" in `/help`).

### Step 2: Validate (required)

**Always run validation after creating or modifying a command:**

```sh
uv run .claude/skills/meta-command-creator/scripts/validate-command.py .claude/commands/my-command.md
```

Fix any errors before committing.

## Command Locations

| Location                            | Invocation                | Description in /help |
| ----------------------------------- | ------------------------- | -------------------- |
| `.claude/commands/name.md`          | `/name`                   | "(project)"          |
| `.claude/commands/frontend/name.md` | `/name`                   | "(project:frontend)" |
| `~/.claude/commands/name.md`        | `/name`                   | "(user)"             |
| Plugin `commands/name.md`           | `/name` or `/plugin:name` | "(plugin-name)"      |

### Priority

When project and user commands share the same name, **project wins** and user command is silently ignored.

> **Tip**: Slash command autocomplete works anywhere in your input, not just at the beginning.

## YAML Frontmatter (Official Fields Only)

| Field                      | Purpose                     | Example                     |
| -------------------------- | --------------------------- | --------------------------- |
| `description`              | Brief description for /help | `Create a git commit`       |
| `allowed-tools`            | Tool restrictions           | `Bash(git:*), Read`         |
| `argument-hint`            | Expected arguments          | `[message]`                 |
| `model`                    | Specific model              | `claude-3-5-haiku-20241022` |
| `disable-model-invocation` | Block SlashCommand tool     | `true`                      |

```yaml
---
description: Create a conventional git commit with proper formatting.
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git status:*)
argument-hint: [commit message]
---
```

### Invalid Fields (Do Not Use)

- `name` - Inferred from filename
- `category` - Not an official field
- `tags` - Not an official field

## Special Syntax

### Bash Execution (`!` prefix)

Execute bash commands before the slash command runs. Output is included in context:

```markdown
---
allowed-tools: Bash(git:*)
description: Create a git commit
---

## Context

- Current status: !`git status`
- Current diff: !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
```

> **Important**: You MUST include `allowed-tools` with `Bash` when using `!` prefix.

### File References (`@` prefix)

Include file contents in commands:

```markdown
Review the implementation in @src/utils/helpers.js

Compare @src/old-version.js with @src/new-version.js
```

### Extended Thinking

Include extended thinking keywords to trigger deeper reasoning:

```markdown
Think carefully about the architecture implications before making changes.
```

## Command Templates

See [reference.md](reference.md) for complete templates:

- **Basic Command** - Simple steps with reference section
- **Command with Arguments** - Using `$ARGUMENTS` and `$1`, `$2`
- **Guardrailed Command** - Safety constraints for state-changing operations
- **Multi-Phase Command** - Complex workflows with distinct phases
- **Git Commit Command** - With bash execution context

## $ARGUMENTS Patterns

| Pattern    | Example        | Use Case                 |
| ---------- | -------------- | ------------------------ |
| Single     | `$ARGUMENTS`   | One value                |
| Positional | `$1`, `$2`     | Multiple specific values |
| Optional   | Check if empty | Default behavior         |

See [reference.md](reference.md) for detailed patterns.

## Organizing Commands

Use subdirectories for categorization:

```text
.claude/commands/
├── git/commit.md      # Shows "(project:git)"
├── dev/feature.md     # Shows "(project:dev)"
└── docs/update.md     # Shows "(project:docs)"
```

## SlashCommand Tool

Claude can execute custom slash commands programmatically using the `SlashCommand` tool.

### Enabling Automatic Invocation

Reference commands by name in your prompts or CLAUDE.md:

```text
Run /write-unit-test when you are about to start writing tests.
```

### Requirements

- Command MUST have `description` frontmatter (used for context)
- Built-in commands (`/compact`, `/init`, etc.) are NOT supported
- Only custom user-defined commands work

### Disabling

```sh
# Disable all SlashCommand tool invocations
/permissions
# Add to deny rules: SlashCommand

# Disable specific command only
```

Add to command frontmatter:

```yaml
disable-model-invocation: true
```

### Permission Rules

- Exact match: `SlashCommand:/commit` (only `/commit`, no args)
- Prefix match: `SlashCommand:/review-pr:*` (allows any args)

### Character Budget

Default: 15,000 characters for command descriptions. Set custom limit:

```sh
SLASH_COMMAND_TOOL_CHAR_BUDGET=20000
```

When exceeded, shows "M of N commands" warning in `/context`.

## Skills vs Commands

| Aspect         | Slash Commands        | Agent Skills                        |
| -------------- | --------------------- | ----------------------------------- |
| **Complexity** | Simple prompts        | Complex capabilities                |
| **Structure**  | Single .md file       | Directory with SKILL.md + resources |
| **Discovery**  | Explicit (`/command`) | Automatic (based on context)        |
| **Files**      | One file only         | Multiple files, scripts, templates  |

### When to Use Each

**Use slash commands when:**

- You invoke the same prompt repeatedly
- The prompt fits in a single file
- You want explicit control over when it runs

**Use Skills when:**

- Claude should discover the capability automatically
- Multiple files or scripts are needed
- Complex workflows with validation steps
- Team needs standardized, detailed guidance

## Common Mistakes

| Mistake                           | Impact                | Correct Pattern                     |
| --------------------------------- | --------------------- | ----------------------------------- |
| Using `name` field                | Ignored               | Name inferred from filename         |
| Missing `description`             | Won't appear in /help | Add description frontmatter         |
| Using `category`/`tags`           | Ignored               | Use subdirectories for organization |
| $ARGUMENTS without handling empty | Runtime errors        | Check if empty first                |
| `!` bash without `allowed-tools`  | Won't execute         | Add `allowed-tools: Bash(...)`      |
| Expecting priority over project   | User command ignored  | Project commands always win         |

## Validation

Run the validator to check command structure:

```sh
uv run .claude/skills/meta-command-creator/scripts/validate-command.py .claude/commands/my-command.md
```

### Checklist

- [ ] File location: `.claude/commands/<name>.md`
- [ ] YAML frontmatter has `description`
- [ ] Steps are numbered and actionable
- [ ] $ARGUMENTS handled correctly (if used)
- [ ] `allowed-tools` included if using `!` bash execution
- [ ] All code blocks have language specifiers
- [ ] Guardrails section for state-changing commands
- [ ] Output format specified

## Built-in Commands Reference

Key built-in commands (cannot be overridden):

| Command        | Purpose                 |
| -------------- | ----------------------- |
| `/help`        | Get usage help          |
| `/compact`     | Compact conversation    |
| `/memory`      | Edit CLAUDE.md files    |
| `/init`        | Initialize CLAUDE.md    |
| `/permissions` | View/update permissions |
| `/agents`      | Manage subagents        |
| `/mcp`         | Manage MCP servers      |

Full list: Run `/help` in Claude Code.

## Delegation

- **After creating/modifying commands**: Run `uv run .claude/skills/meta-command-creator/scripts/validate-command.py <command.md>`
- **Pattern discovery**: For existing command patterns, use `Explore` agent

## References

- Official Docs: [code.claude.com/docs/en/slash-commands.md](https://code.claude.com/docs/en/slash-commands.md)
- Existing commands: `.claude/commands/openspec/`
- Skills comparison: [code.claude.com/docs/en/skills.md](https://code.claude.com/docs/en/skills.md)
