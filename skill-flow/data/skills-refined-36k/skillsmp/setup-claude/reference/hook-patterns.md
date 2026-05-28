# Hook Patterns Reference

Enhanced hook patterns from real-world usage and community best practices.

## Core Concepts

### Hook Types

| Type | When | Use Case |
|------|------|----------|
| PreToolUse | Before tool runs | Block, warn, modify |
| PostToolUse | After tool completes | Auto-fix, validate |
| Notification | User notifications | Alerts, reminders |

### Environment Variables

Hooks have access to these variables:

| Variable | Description | Available In |
|----------|-------------|--------------|
| `$CLAUDE_FILE_PATHS` | Space-separated file paths | PostToolUse (Edit/Write) |
| `$CLAUDE_TOOL_NAME` | Name of the tool | All hooks |

---

## Essential Hook Patterns

### 1. Format on Save (Most Important)

Auto-format files after Claude edits them.

**TypeScript + Biome (Recommended)**:
```json
{
  "hooks": {
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

**TypeScript + Prettier**:
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
          }
        ]
      }
    ]
  }
}
```

**Python + Ruff**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "ruff format $CLAUDE_FILE_PATHS && ruff check --fix $CLAUDE_FILE_PATHS 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### 2. Type Check After Edits

Catch type errors immediately.

**TypeScript**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx tsc --noEmit 2>&1 | head -20 || true"
          }
        ]
      }
    ]
  }
}
```

**Python + mypy**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "mypy $CLAUDE_FILE_PATHS --ignore-missing-imports 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### 3. Console.log Warning

Warn when console.log is added to code.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "grep -l 'console.log' $CLAUDE_FILE_PATHS 2>/dev/null && echo '[Hook] console.log detected - remove before commit' >&2 || true"
          }
        ]
      }
    ]
  }
}
```

### 4. tmux Reminder for Long Commands

Remind to use tmux for potentially long-running commands.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if [ -z \"$TMUX\" ]; then echo '[Hook] Consider using tmux for long-running commands' >&2; fi; exit 0"
          }
        ]
      }
    ]
  }
}
```

### 5. Block Markdown File Creation

Prevent accidental documentation file creation (except README/CLAUDE).

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "for f in $CLAUDE_FILE_PATHS; do if [[ \"$f\" == *.md ]] && [[ ! \"$f\" =~ (README|CLAUDE) ]]; then echo '[Hook] Blocked: .md file creation (use README.md or CLAUDE.md)' >&2; exit 1; fi; done; exit 0"
          }
        ]
      }
    ]
  }
}
```

### 6. Review Before Git Push

Pause before pushing to remind about review.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$*\" | grep -q 'git push'; then echo '[Hook] About to push - have you reviewed the changes?' >&2; fi; exit 0"
          }
        ]
      }
    ]
  }
}
```

### 7. Lint Check

Run linter after edits.

**ESLint**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
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

### 8. Test Related Files

Run tests for edited files.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "for f in $CLAUDE_FILE_PATHS; do test_file=\"${f%.ts}.test.ts\"; [ -f \"$test_file\" ] && npm test -- \"$test_file\" 2>/dev/null; done || true"
          }
        ]
      }
    ]
  }
}
```

---

## Combined Configurations

### TypeScript + Biome (Recommended)

Complete configuration for TypeScript projects using Biome:

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

For projects using ESLint and Prettier:

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
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

For Python projects:

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
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
          },
          {
            "type": "command",
            "command": "mypy $CLAUDE_FILE_PATHS --ignore-missing-imports 2>/dev/null | head -10 || true"
          }
        ]
      }
    ]
  }
}
```

### Rust

For Rust projects:

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
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

For Go projects:

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
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

## Advanced Patterns

### File-Type Specific Hooks

Different actions for different file types:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "for f in $CLAUDE_FILE_PATHS; do case \"$f\" in *.ts|*.tsx) biome check --write \"$f\";; *.py) ruff format \"$f\";; *.json) prettier --write \"$f\";; esac; done 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### Conditional Hooks

Only run if certain conditions are met:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "[ -f biome.json ] && biome check --write $CLAUDE_FILE_PATHS 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### Notification Hooks

Show notifications for important events:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "task_complete",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Task completed\" with title \"Claude\"' 2>/dev/null || true"
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

Add `2>/dev/null || true` to prevent hook failures from blocking work:

```bash
# Good
biome check --write $CLAUDE_FILE_PATHS 2>/dev/null || true

# Bad - will fail if biome not installed
biome check --write $CLAUDE_FILE_PATHS
```

### 2. Limit Output

Use `head` to prevent verbose output:

```bash
# Good - shows first 20 lines
npx tsc --noEmit 2>&1 | head -20 || true

# Bad - could output thousands of lines
npx tsc --noEmit
```

### 3. Use Appropriate Matchers

Be specific about when hooks run:

```json
// Good - only on file edits
"matcher": "Edit|Write"

// Bad - runs on every tool use
"matcher": "*"
```

### 4. Test Hooks Before Using

Verify hooks work correctly:

```bash
# Test format hook
echo "const x = 1" > test.ts
biome check --write test.ts
rm test.ts
```

### 5. Document Hook Behavior

Add comments in settings.json:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        // Format TypeScript files with Biome
        "matcher": "Edit|Write",
        "hooks": [...]
      }
    ]
  }
}
```

---

## Troubleshooting

### Hook Not Running

1. Check matcher syntax
2. Verify tool is installed
3. Check file permissions

### Hook Blocking Work

1. Add error suppression (`|| true`)
2. Check for infinite loops
3. Reduce hook scope

### Hook Too Slow

1. Limit output with `head`
2. Run on specific files only
3. Consider async execution

### Hook Output Not Visible

1. Use `>&2` for stderr output
2. Check Claude Code settings
3. Verify hook is executing
