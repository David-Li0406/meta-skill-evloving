# Optional Hooks for Task Management

## Overview

This document describes optional hooks you can enable to automate or enhance task management workflows.

## Test Completion Reminder Hook

Automatically reminds you to complete a task when all tests pass.

### How It Works

When you run tests via Bash (pytest, go test, npm test, make test) and they all pass, you'll see a reminder:

```
⚠️  All tests passed! Consider completing the task with: /task-complete <task-id>
```

### Installation

Add this to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r 'if (.tool_input.command | contains(\"pytest\") or contains(\"go test\") or contains(\"npm test\") or contains(\"make test\")) and (.exit_code == 0) then \"\\n⚠️  All tests passed! Consider completing the task with: /task-complete <task-id>\\n\" else \"\" end'",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Customization

You can customize the hook to:

**Add more test commands:**
```bash
# Add "cargo test" for Rust projects
... or contains(\"cargo test\") ...
```

**Change the message:**
```bash
# More specific message
\"\\n✅ Tests green! Time to wrap up this task.\\n\"
```

**Add additional conditions:**
```bash
# Only remind if in project directory
if (.tool_input.command | contains(\"test\")) and (.exit_code == 0) and (env.PWD | contains(\"shark-task-manager\")) then ...
```

## Auto-Start Hook (Advanced)

**⚠️ Warning:** This hook automatically starts tasks, which may not be desired in all workflows.

Automatically starts a task when you begin implementation by reading a file from a task directory.

### How It Works

When you read a task file (e.g., `docs/plan/.../tasks/T-*.md`), it extracts the task ID and starts it automatically.

### Installation

Add this to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/auto-start-task.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Create the script at `.claude/hooks/auto-start-task.sh`:

```bash
#!/bin/bash
# Auto-start tasks when reading task files

# Read the hook input
input=$(cat)

# Extract file path
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Check if it's a task file
if [[ "$file_path" =~ /tasks/(T-[A-Z0-9]+-[A-Z0-9]+-[0-9]+)\.md$ ]]; then
    task_id="${BASH_REMATCH[1]}"

    # Check if task is already in-progress or completed
    status=$(shark --json task get "$task_id" 2>/dev/null | jq -r '.status // empty')

    if [[ "$status" == "todo" ]]; then
        echo "🚀 Auto-starting task: $task_id"
        shark task start "$task_id"
    fi
fi
```

Make the script executable:
```bash
chmod +x .claude/hooks/auto-start-task.sh
```

## Task Validation Hook

Validates that tasks are started before making file edits in implementation directories.

### How It Works

When you edit implementation files (src/, internal/, cmd/), it checks if you have an active task.

### Installation

Create the script at `.claude/hooks/validate-active-task.sh`:

```bash
#!/bin/bash
# Validate that a task is active before editing implementation files

input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Check if editing implementation files
if [[ "$file_path" =~ ^(src/|internal/|cmd/|pkg/) ]]; then
    # Get currently active tasks
    active_tasks=$(shark --json task list --status=in-progress 2>/dev/null | jq -r '.[] | .key')

    if [[ -z "$active_tasks" ]]; then
        echo "⚠️  No active task found. Start a task with: /task-start <task-id>"
        echo "Or continue without task tracking."
        exit 0  # Warning only, don't block
    fi
fi
```

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-active-task.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

## Best Practices

### When to Use Hooks

**Use hooks when:**
- You want consistent reminders across all work sessions
- You need deterministic automation
- The action should happen every time (not just sometimes)

**Use slash commands when:**
- You want explicit control
- You need to decide when to run the action
- Different contexts require different handling

### Hook Safety

1. **Test hooks thoroughly** before enabling
2. **Use warnings instead of blocking** when possible
3. **Set reasonable timeouts** (5-10 seconds for most hooks)
4. **Log hook executions** during development
5. **Document hook behavior** for team members

### Debugging Hooks

Enable verbose logging:
```bash
# In your hook script
echo "DEBUG: Hook triggered for $file_path" >&2
```

Check hook execution:
```bash
# Review Claude's tool output for hook messages
```

## See Also

- [Hooks Reference](https://code.claude.com/docs/en/hooks-reference) - Complete hooks documentation
- [Hooks Getting Started](https://code.claude.com/docs/en/hooks-guide) - Quickstart guide
- [Slash Commands](../../../docs/CLI.md) - Direct task management commands
