# Hooks Configuration Component

This component handles configuring Claude Code hooks for automatic formatting, linting, type checking, and workflow automation.

## What Are Hooks?

Hooks are shell commands that run automatically in response to Claude Code events. They enable:

- **Auto-formatting**: Format code after Claude edits files
- **Type checking**: Verify types after edits
- **Linting**: Check code quality automatically
- **Workflow enforcement**: Block unwanted actions, remind about best practices
- **Custom actions**: Run any command in response to events

## Hook Types

| Type | When | Blocking | Use Cases |
|------|------|----------|-----------|
| PreToolUse | Before tool runs | Yes | Block actions, validate, warn |
| PostToolUse | After tool completes | No | Auto-fix, validate, notify |
| Notification | User notifications | No | Alerts, reminders |

### PreToolUse
Runs **before** a tool is executed. Can block the tool if exit code is non-zero.

**Use cases:**
- Block creation of unwanted files
- Warn about risky operations
- Validate preconditions

### PostToolUse
Runs **after** a tool completes successfully. Most common for formatting/linting.

**Use cases:**
- Format files after Write/Edit
- Run type checker after code changes
- Detect code smells (console.log)

### Notification
Runs when a notification is triggered. Non-blocking.

**Use cases:**
- Log actions
- Send system alerts

---

## Hook Configuration Structure

Hooks are configured in `.claude/settings.json`:

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'About to write file'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "biome check --write $CLAUDE_FILE_PATHS 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `matcher` | Regex pattern matching tool names (Edit, Write, Bash, etc.) |
| `hooks` | Array of hook actions to run |
| `type` | Hook type: "command" for shell commands |
| `command` | Shell command to execute |

### Environment Variables

Available in hook commands:

| Variable | Description |
|----------|-------------|
| `$CLAUDE_FILE_PATHS` | Space-separated list of files affected |
| `$CLAUDE_TOOL_NAME` | Name of the tool that was used |

---

## Essential Hooks

### 1. Format on Save (Most Important)

Auto-format files after Claude edits them.

**TypeScript + Biome (Recommended)**:
```json
{
  "matcher": "Edit|Write",
  "hooks": [
    {
      "type": "command",
      "command": "biome check --write $CLAUDE_FILE_PATHS 2>/dev/null || true"
    }
  ]
}
```

**Python + Ruff**:
```json
{
  "matcher": "Edit|Write",
  "hooks": [
    {
      "type": "command",
      "command": "ruff format $CLAUDE_FILE_PATHS && ruff check --fix $CLAUDE_FILE_PATHS 2>/dev/null || true"
    }
  ]
}
```

### 2. Type Check After Edits

```json
{
  "matcher": "Edit|Write",
  "hooks": [
    {
      "type": "command",
      "command": "npx tsc --noEmit 2>&1 | head -20 || true"
    }
  ]
}
```

### 3. Console.log Warning

Warn when console.log is added:

```json
{
  "matcher": "Edit|Write",
  "hooks": [
    {
      "type": "command",
      "command": "grep -l 'console.log' $CLAUDE_FILE_PATHS 2>/dev/null && echo '[Hook] console.log detected - remove before commit' >&2 || true"
    }
  ]
}
```

### 4. tmux Reminder for Long Commands

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "if [ -z \"$TMUX\" ]; then echo '[Hook] Consider tmux for long-running commands' >&2; fi; exit 0"
    }
  ]
}
```

### 5. Block Markdown File Creation

Prevent accidental .md creation (except README/CLAUDE):

```json
{
  "matcher": "Write",
  "hooks": [
    {
      "type": "command",
      "command": "for f in $CLAUDE_FILE_PATHS; do if [[ \"$f\" == *.md ]] && [[ ! \"$f\" =~ (README|CLAUDE) ]]; then echo '[Hook] Blocked .md file creation' >&2; exit 1; fi; done; exit 0"
    }
  ]
}
```

### 6. Review Before Git Push

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "if echo \"$*\" | grep -q 'git push'; then echo '[Hook] About to push - have you reviewed?' >&2; fi; exit 0"
    }
  ]
}
```

---

## Configuration Interview Flow

### Step 1: Detect Available Tools

```bash
# Check for formatter/linter config files
ls biome.json biome.jsonc .eslintrc* .prettierrc* pyproject.toml ruff.toml 2>/dev/null
```

### Step 2: Interview User

```
AskUserQuestion: "Which hooks to enable?"
(Multi-select)

├── Format on save (biome check --write) [Recommended]
│   Runs formatter after Claude edits files
│
├── Type check after edits (tsc --noEmit)
│   Runs type checker to catch errors early
│
├── Lint check (eslint --fix)
│   Runs linter for code quality
│
├── tmux reminder for long commands
│   Reminds to use tmux for npm/build commands
│
├── Block .md file creation (except README/CLAUDE)
│   Prevents accidental documentation creation
│
├── Console.log warning
│   Warns when console.log is detected
│
├── Review before git push
│   Reminds to review before pushing
│
└── None - I'll configure manually
```

### Step 3: Generate settings.json

Based on selections, generate appropriate configuration:

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "hooks": {
    "PreToolUse": [
      // tmux reminder, md blocking, push review
    ],
    "PostToolUse": [
      // format, typecheck, lint, console.log warning
    ]
  }
}
```

### Step 4: Merge with Existing

If `.claude/settings.json` exists:
1. Create backup: `cp settings.json settings.json.backup`
2. Merge new hooks with existing
3. Write updated file

---

## Hooks by Tech Stack

### TypeScript + Biome (Recommended)

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "for f in $CLAUDE_FILE_PATHS; do if [[ \"$f\" == *.md ]] && [[ ! \"$f\" =~ (README|CLAUDE) ]]; then echo '[Hook] Blocked .md creation' >&2; exit 1; fi; done; exit 0"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "biome check --write $CLAUDE_FILE_PATHS 2>/dev/null || true"
          },
          {
            "type": "command",
            "command": "grep -l 'console.log' $CLAUDE_FILE_PATHS 2>/dev/null && echo '[Hook] console.log detected' >&2 || true"
          }
        ]
      }
    ]
  }
}
```

### TypeScript + ESLint + Prettier

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS 2>/dev/null || true"
          },
          {
            "type": "command",
            "command": "eslint --fix $CLAUDE_FILE_PATHS 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### Python + Ruff

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "ruff format $CLAUDE_FILE_PATHS 2>/dev/null || true"
          },
          {
            "type": "command",
            "command": "ruff check --fix $CLAUDE_FILE_PATHS 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### Rust

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "rustfmt $CLAUDE_FILE_PATHS 2>/dev/null || true"
          },
          {
            "type": "command",
            "command": "cargo check 2>&1 | head -20 || true"
          }
        ]
      }
    ]
  }
}
```

### Go

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "gofmt -w $CLAUDE_FILE_PATHS 2>/dev/null || true"
          },
          {
            "type": "command",
            "command": "go vet ./... 2>&1 | head -10 || true"
          }
        ]
      }
    ]
  }
}
```

---

## Best Practices

### 1. Always Use Error Suppression

Prevent hook failures from blocking work:

```bash
# Good
biome check --write $CLAUDE_FILE_PATHS 2>/dev/null || true

# Bad - will fail if biome not installed
biome check --write $CLAUDE_FILE_PATHS
```

### 2. Limit Output

Use `head` to prevent verbose output:

```bash
# Good
npx tsc --noEmit 2>&1 | head -20 || true

# Bad
npx tsc --noEmit
```

### 3. Test Hooks First

Run commands manually before adding as hooks:

```bash
# Test format hook
echo "const x = 1" > test.ts
biome check --write test.ts
rm test.ts
```

### 4. Start Minimal

Enable just formatting first, add more later as needed.

### 5. Document in CLAUDE.md

Note which hooks are configured so Claude knows what's automatic.

---

## Troubleshooting

### Hook Not Running

1. Check matcher regex matches tool name
2. Verify tool is installed
3. Check file permissions
4. Test command manually

### Hook Blocking Work

1. Add error suppression (`|| true`)
2. Check for infinite loops
3. Reduce hook scope

### Hook Too Slow

1. Limit output with `head`
2. Run only on specific files
3. Use faster alternatives (Biome vs Prettier)

### Formatter Conflicts

1. Pick one primary formatter
2. Disable others in config
3. Or chain them carefully

---

## hookify Plugin

For easier hook creation, suggest the hookify plugin:

```
Tip: Use /hookify to create custom hooks conversationally.

Example:
User: "Add a hook that runs tests after editing test files"
hookify: [generates appropriate hook configuration]
```

---

## Reference

For complete hook configurations, see:
- `reference/hook-patterns.md` - Enhanced hook patterns
- `reference/hook-templates.md` - Ready-to-use configurations by tech stack
