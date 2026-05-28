# Command Hooks (Bash-Based)

> **Pattern**: Deterministic validation with fast, predictable execution
> **Use For**: All events - validation, security checks, guardrails
> **Philosophy**: Fail fast with `exit 2` to block dangerous operations

## Overview

Command hooks execute bash scripts for **fast, deterministic** validation and automation. They work with **all event types** and are the recommended approach for project guardrails.

**Key Principle**: Use `exit 2` to **immediately block** dangerous operations.

## Common Patterns

### 1. Path Safety Guardrail

**Event**: `PreToolUse`
**Purpose**: Block writes to sensitive files

```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "guard-paths.sh \"$FILE_PATH\""
    }]
  }]
}
```

**Script Template** (`guard-paths.sh`):
```bash
#!/bin/bash
FILE_PATH="$1"

# Block environment files
if [[ "$FILE_PATH" == *".env"* ]] || [[ "$FILE_PATH" == *".env."* ]]; then
  echo "❌ BLOCKED: .env files require explicit approval"
  exit 2
fi

# Block configuration with secrets
if [[ "$FILE_PATH" =~ \.(aws|docker|gcp)/.* ]] && [[ "$FILE_PATH" =~ (credentials|config)$ ]]; then
  echo "❌ BLOCKED: Sensitive config files"
  exit 2
fi

# Block deletion of protected directories
if [[ "$COMMAND" =~ rm.*-r.* ]] && [[ "$FILE_PATH" =~ (node_modules|\.git|vendor) ]]; then
  echo "❌ BLOCKED: Protected directory deletion"
  exit 2
fi

exit 0
```

### 2. Command Validation

**Event**: `PreToolUse`
**Purpose**: Validate bash commands before execution

```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "guard-commands.sh"
    }]
  }]
}
```

**Script Template** (`guard-commands.sh`):
```bash
#!/bin/bash
COMMAND="$1"

# Extract the base command
BASE_CMD=$(echo "$COMMAND" | awk '{print $1}')

# Block dangerous commands
case "$BASE_CMD" in
  rm)
    if [[ "$COMMAND" =~ -rf ]] || [[ "$COMMAND" =~ -r ]] && [[ "$COMMAND" =~ -f ]]; then
      echo "❌ BLOCKED: Dangerous rm command"
      exit 2
    fi
    ;;
  sudo)
    echo "❌ BLOCKED: sudo commands require approval"
    exit 2
    ;;
  chmod)
    echo "❌ BLOCKED: chmod commands require approval"
    exit 2
    ;;
  chown)
    echo "❌ BLOCKED: chown commands require approval"
    exit 2
    ;;
esac

exit 0
```

### 3. Quality Gate Hook

**Event**: `PreToolUse`
**Purpose**: Run tests/validation before deployment

```yaml
---
name: deploy-skill
description: "Deploys to production"
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: "run-tests.sh"
---
```

**Script Template** (`run-tests.sh`):
```bash
#!/bin/bash
echo "🔍 Running pre-deployment checks..."

# Run unit tests
echo "Running tests..."
npm test
if [ $? -ne 0 ]; then
  echo "❌ FAILED: Unit tests"
  exit 2
fi

# Run security scan
echo "Running security scan..."
npm audit --audit-level high
if [ $? -ne 0 ]; then
  echo "❌ FAILED: Security audit"
  exit 2
fi

# Check code format
echo "Checking code format..."
npm run lint
if [ $? -ne 0 ]; then
  echo "❌ FAILED: Code format check"
  exit 2
fi

echo "✅ All checks passed"
exit 0
```

### 4. Session State Save

**Event**: `Stop`
**Purpose**: Persist development decisions

```json
{
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "save-state.sh"
    }]
  }]
}
```

**Script Template** (`save-state.sh`):
```bash
#!/bin/bash
# Save current session decisions to .claude/STATE.md
# See session-persistence.md for full implementation

STATE_FILE=".claude/STATE.md"
mkdir -p .claude

# Append timestamp and key decisions
echo "" >> "$STATE_FILE"
echo "---" >> "$STATE_FILE"
echo "**Last Updated**: $(date -Iseconds)" >> "$STATE_FILE"

# Extract and save decisions from conversation context
# (Implementation depends on your workflow)

exit 0
```

### 5. Environment Initialization

**Event**: `SessionStart`
**Purpose**: Initialize project environment

```json
{
  "SessionStart": [{
    "matcher": "startup",
    "hooks": [{
      "type": "command",
      "command": "init-env.sh"
    }]
  }]
}
```

**Script Template** (`init-env.sh`):
```bash
#!/bin/bash
echo "🚀 Initializing project environment..."

# Check required tools
for cmd in npm node; do
  if ! command -v "$cmd" &> /dev/null; then
    echo "❌ Missing required tool: $cmd"
    exit 2
  fi
done

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install
fi

# Validate environment
if [ ! -f ".env.example" ]; then
  echo "⚠️  Missing .env.example file"
fi

echo "✅ Environment ready"
exit 0
```

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | Operation continues |
| `1` | Non-blocking error | Logged but doesn't block |
| `2` | Blocking error | **Stops operation** (use for guardrails) |

**For guardrails, ALWAYS use `exit 2`**.

## Best Practices

### DO ✅
- Always quote variables: `"$VAR"` not `$VAR`
- Use `set -euo pipefail` for safer scripts
- Validate ALL inputs before processing
- Use specific error messages (what was blocked and why)
- Test with intentionally dangerous operations
- Keep scripts fast (<10 seconds)

### DON'T ❌
- Don't use `exit 1` for blocking (use `exit 2`)
- Don't skip validation
- Don't use wildcards without quoting
- Don't trust input paths without checking
- Don't create infinite loops
- Don't use prompt hooks for validation (use commands)

## Script Organization

**Recommended project structure**:
```
.claude/
├── hooks.json              # Hook configuration
└── scripts/
    ├── guard-paths.sh      # Path safety
    ├── guard-commands.sh   # Command validation
    ├── run-tests.sh        # Quality gate
    ├── save-state.sh       # State persistence
    └── init-env.sh         # Environment setup
```

## Testing Your Guardrails

```bash
# Test 1: Blocked operation
echo "test" > .env  # Should fail with exit 2

# Test 2: Allowed operation
echo "test" > test.txt  # Should succeed

# Test 3: Dangerous command
rm -rf node_modules  # Should be blocked

# Verify hook is registered
/hooks  # Check hook status
```

## Reference

- **Hooks Guide**: https://code.claude.com/docs/en/hooks
- **Session Persistence**: [session-persistence.md](session-persistence.md)
- **Security Patterns**: [security-patterns.md](security-patterns.md)
