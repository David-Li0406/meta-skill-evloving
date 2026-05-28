# Hook Templates Reference

Ready-to-use hook configurations for common tech stacks.

## How to Use

1. Identify project's tech stack
2. Find matching template below
3. Copy the JSON configuration
4. Merge into `.claude/settings.json`

---

## TypeScript + Biome

The most common modern TypeScript setup.

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
            "command": "npx biome check --write $CLAUDE_FILE_PATHS"
          },
          {
            "type": "command",
            "command": "npx tsc --noEmit"
          }
        ]
      }
    ]
  }
}
```

**Requirements:**
- `biome.json` configured
- `tsconfig.json` configured
- `npm install -D @biomejs/biome typescript`

---

## TypeScript + ESLint + Prettier

Classic linting and formatting combo.

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
            "command": "npx prettier --write $CLAUDE_FILE_PATHS"
          },
          {
            "type": "command",
            "command": "npx eslint --fix $CLAUDE_FILE_PATHS"
          },
          {
            "type": "command",
            "command": "npx tsc --noEmit"
          }
        ]
      }
    ]
  }
}
```

**Requirements:**
- `.eslintrc.*` configured
- `.prettierrc*` configured
- `tsconfig.json` configured

---

## JavaScript + Biome

For JavaScript projects without TypeScript.

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
            "command": "npx biome check --write $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

---

## Python + Ruff

Modern Python formatting and linting.

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
            "command": "ruff format $CLAUDE_FILE_PATHS"
          },
          {
            "type": "command",
            "command": "ruff check --fix $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

**Requirements:**
- `pip install ruff`
- `ruff.toml` or `pyproject.toml` with `[tool.ruff]`

---

## Python + Black + Flake8

Classic Python formatting setup.

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
            "command": "black $CLAUDE_FILE_PATHS"
          },
          {
            "type": "command",
            "command": "isort $CLAUDE_FILE_PATHS"
          },
          {
            "type": "command",
            "command": "flake8 $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

**Requirements:**
- `pip install black isort flake8`

---

## Python + mypy (Type Checking)

Add type checking to any Python setup.

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
            "command": "ruff format $CLAUDE_FILE_PATHS && ruff check --fix $CLAUDE_FILE_PATHS"
          },
          {
            "type": "command",
            "command": "mypy $CLAUDE_FILE_PATHS --ignore-missing-imports"
          }
        ]
      }
    ]
  }
}
```

---

## Rust

Standard Rust formatting and checking.

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
            "command": "rustfmt $CLAUDE_FILE_PATHS"
          },
          {
            "type": "command",
            "command": "cargo check"
          }
        ]
      }
    ]
  }
}
```

**Requirements:**
- `rustfmt` (installed with rustup)

---

## Go

Standard Go formatting.

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
            "command": "gofmt -w $CLAUDE_FILE_PATHS"
          },
          {
            "type": "command",
            "command": "go vet ./..."
          }
        ]
      }
    ]
  }
}
```

---

## Minimal (Format Only)

Just formatting, no linting or type checking.

### Biome
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx biome check --write $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

### Prettier
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

---

## Merging with Existing Settings

If `.claude/settings.json` already exists, merge carefully:

```javascript
// Pseudo-code for merging
function mergeSettings(existing, template) {
  return {
    ...existing,
    permissions: {
      ...existing.permissions,
      ...template.permissions
    },
    hooks: {
      ...existing.hooks,
      PostToolUse: [
        ...(existing.hooks?.PostToolUse || []),
        ...template.hooks.PostToolUse
      ]
    }
  };
}
```

**Important:** Don't duplicate hooks. Check if similar hooks already exist before adding.

---

## Testing Hooks

After configuring hooks, test them:

1. **Create a test file:**
   ```bash
   echo "const x=1" > test-hook.ts
   ```

2. **Edit it with Claude:**
   Ask Claude to add a line to `test-hook.ts`

3. **Verify hook ran:**
   - File should be formatted
   - Type check should pass
   - Check Claude's output for hook execution

4. **Clean up:**
   ```bash
   rm test-hook.ts
   ```

---

## Troubleshooting

### Hook not running

Check that:
1. `matcher` pattern matches the tool (Edit, Write)
2. Command is available in PATH
3. No syntax errors in settings.json

### Command fails

Test command manually:
```bash
npx biome check --write path/to/file.ts
```

### Too slow

Consider:
- Remove type checking hook (run manually)
- Use faster tools (Biome vs Prettier)
- Only format, don't lint

---

## Quick Reference

| Stack | Formatter | Type Checker |
|-------|-----------|--------------|
| TypeScript + Biome | `biome check --write` | `tsc --noEmit` |
| TypeScript + Prettier | `prettier --write` | `tsc --noEmit` |
| Python + Ruff | `ruff format && ruff check --fix` | `mypy` |
| Python + Black | `black && isort` | `mypy` |
| Rust | `rustfmt` | `cargo check` |
| Go | `gofmt -w` | `go vet` |
