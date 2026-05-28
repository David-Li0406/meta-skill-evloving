# Subagent Configuration Reference

Complete reference for subagent configuration options, including all frontmatter fields, permission modes, and hooks.

## Frontmatter Fields

All subagent files use YAML frontmatter for configuration. Only `name` and `description` are required.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier using lowercase letters and hyphens (e.g., `code-reviewer`, `db-reader`) |
| `description` | string | When Claude should delegate to this subagent. Include specific triggers and use cases. |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `tools` | array | Tools the subagent can use. Inherits all tools if omitted. |
| `disallowedTools` | array | Tools to deny, removed from inherited or specified list. |
| `model` | string | Model to use: `sonnet`, `opus`, `haiku`, or `inherit`. Defaults to `sonnet`. |
| `permissionMode` | string | Permission mode: `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, or `plan`. |
| `skills` | array | Skills to load into the subagent's context at startup. |
| `hooks` | object | Lifecycle hooks scoped to this subagent. |

## Tool Access Control

### Available Tools

Subagents can use any of Claude Code's internal tools. By default, subagents inherit all tools from the main conversation, including MCP tools.

**Common tools:**
- `Read` - Read file contents
- `Write` - Write new files
- `Edit` - Edit existing files
- `Grep` - Search file contents
- `Glob` - Find files by pattern
- `Bash` - Execute terminal commands
- `AskUserQuestion` - Ask the user clarifying questions
- `Task` - Spawn other subagents (not available to subagents)

### Restricting Tools

Use the `tools` field (allowlist) or `disallowedTools` field (denylist):

```yaml
---
# Allowlist approach: only these tools
tools: Read, Grep, Glob, Bash

# Denylist approach: all tools except these
tools: Read, Write, Edit
disallowedTools: Bash

# Combined: inherit tools, then deny specific ones
disallowedTools: Write, Edit
---
```

## Permission Modes

The `permissionMode` field controls how the subagent handles permission prompts.

| Mode | Behavior |
|------|----------|
| `default` | Standard permission checking with prompts |
| `acceptEdits` | Auto-accept file edits |
| `dontAsk` | Auto-deny permission prompts (explicitly allowed tools still work) |
| `bypassPermissions` | Skip all permission checks (use with caution) |
| `plan` | Plan mode (read-only exploration) |

**Warning:** Use `bypassPermissions` with caution. It skips all permission checks, allowing the subagent to execute any operation without approval.

## Model Selection

The `model` field controls which AI model the subagent uses:

| Value | Description |
|-------|-------------|
| `sonnet` | Balanced capability and speed (default for subagents) |
| `opus` | Highest capability for complex reasoning |
| `haiku` | Fastest model for simple, routine tasks |
| `inherit` | Use the same model as the main conversation |

**Omitted field:** Defaults to `sonnet` if not specified.

## Skills in Subagents

The `skills` field loads skills into the subagent's context at startup. The full skill content is injected, not just made available for invocation. Subagents don't inherit skills from the parent conversation.

```yaml
---
skills:
  - postgresql
  - api-design-principles
---
```

## Hooks

Subagents can define hooks that run during the subagent's lifecycle.

### Hooks in Frontmatter

Define hooks directly in the subagent's markdown file. These hooks only run while that specific subagent is active.

| Event | Matcher | When it fires |
|-------|---------|---------------|
| `PreToolUse` | Tool name | Before the subagent uses a tool |
| `PostToolUse` | Tool name | After the subagent uses a tool |
| `Stop` | (none) | When the subagent finishes |

**Example:**

```yaml
---
name: code-reviewer
description: Review code with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

`Stop` hooks in frontmatter are automatically converted to `SubagentStop` events.

### Project-Level Hooks

Configure hooks in `settings.json` that respond to subagent lifecycle events in the main session.

| Event | Matcher | When it fires |
|-------|---------|---------------|
| `SubagentStart` | Agent type name | When a subagent begins execution |
| `SubagentStop` | Agent type name | When a subagent completes |

**Example:**

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db.sh" }
        ]
      }
    ]
  }
}
```

### Hook Input Format

For `PreToolUse` and `PostToolUse` hooks, Claude Code passes JSON input via stdin with the following structure:

```json
{
  "tool": "Bash",
  "tool_input": {
    "command": "echo 'hello'"
  },
  "context": {
    "working_directory": "/path/to/project"
  }
}
```

For Bash commands, extract the command using:

```bash
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
```

### Hook Exit Codes

| Exit Code | Behavior |
|-----------|----------|
| 0 | Allow the operation to proceed |
| 1 | Operation fails with error message |
| 2 | Block the operation (for PreToolUse) |

## Subagent Scope and Priority

Subagents are loaded from different locations with different priorities. When multiple subagents share the same name, the higher-priority location wins.

| Location | Scope | Priority | How to Create |
|----------|-------|----------|---------------|
| `--agents` CLI flag | Current session | 1 (highest) | Pass JSON when launching Claude Code |
| `.claude/agents/` | Current project | 2 | Interactive or manual |
| `~/.claude/agents/` | All your projects | 3 | Interactive or manual |
| Plugin's `agents/` directory | Where plugin is enabled | 4 (lowest) | Installed with plugins |

### Project Subagents

Store in `.claude/agents/` for project-specific subagents. Check them into version control for team collaboration.

### User Subagents

Store in `~/.claude/agents/` for personal subagents available in all projects.

### CLI-Defined Subagents

Pass as JSON when launching Claude Code. These exist only for that session and aren't saved to disk:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

## Disabling Specific Subagents

Prevent Claude from using specific subagents by adding them to the `deny` array in settings:

```json
{
  "permissions": {
    "deny": ["Task(Explore)", "Task(my-custom-agent)"]
  }
}
```

Or use the `--disallowedTools` CLI flag:

```bash
claude --disallowedTools "Task(Explore)"
```
