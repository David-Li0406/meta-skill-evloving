---
name: register-hook
description: Use this skill when you need to create and register hook scripts with proper error handling and settings in a JSON configuration.
---

# Register Hook Skill

**Purpose**: Create hook scripts with mandatory error handling patterns and register them in settings.json with proper matcher syntax.

**Performance**: Ensures hooks work correctly, prevents registration errors, enforces restart requirement.

## When to Use This Skill

### ✅ Use register-hook When:

- Creating a new hook script from scratch.
- Registering a hook in settings.json.
- Ensuring proper error handling patterns.
- Setting up a hook with a specific trigger event.

### ❌ Do NOT Use When:

- Modifying an existing hook (use Edit tool).
- The hook is already registered (verify first).
- Testing hook behavior (use manual execution).

## What This Skill Does

### 1. Creates Hook Script

```bash
# Creates script with mandatory pattern:
#!/bin/bash
set -euo pipefail

# Error handler - output helpful message to stderr on failure
trap 'echo "ERROR in <script-name>.sh at line $LINENO: Command failed: $BASH_COMMAND" >&2; exit 1' ERR

# Hook logic...
```

### 2. Sets Permissions

```bash
chmod +x ~/.claude/hooks/{hook-name}.sh
```

### 3. Registers in settings.json

```json
{
  "hooks": {
    "{TriggerEvent}": [
      {
        "matcher": "{tool-pattern}",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/{hook-name}.sh"
          }
        ]
      }
    ]
  }
}
```

### 4. Warns About Restart

```markdown
⚠️ Please restart Claude Code for hook changes to take effect.
```

### 5. Provides Test Instructions

```markdown
After restart, test the hook with:
[specific command to trigger hook]
```

## Trigger Events

### Available Events

**SessionStart**: Runs when the session starts or resumes after compaction.
```json
"SessionStart": [
  {
    "hooks": [{"type": "command", "command": "~/.claude/hooks/my-hook.sh"}]
  }
]
```

**UserPromptSubmit**: Runs when the user submits a prompt.
```json
"UserPromptSubmit": [
  {
    "hooks": [{"type": "command", "command": "~/.claude/hooks/my-hook.sh"}]
  }
]
```

**PreToolUse**: Runs before tool execution (supports matchers).
```json
"PreToolUse": [
  {
    "matcher": "Bash",
    "hooks": [{"type": "command", "command": "~/.claude/hooks/my-hook.sh"}]
  }
]
```

**PostToolUse**: Runs after tool execution (supports matchers).
```json
"PostToolUse": [
  {
    "matcher": "Write|Edit",
    "hooks": [{"type": "command", "command": "~/.claude/hooks/my-hook.sh"}]
  }
]
```