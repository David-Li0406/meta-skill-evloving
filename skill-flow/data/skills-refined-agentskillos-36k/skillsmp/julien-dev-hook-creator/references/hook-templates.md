# Hook Templates

Ready-to-use hook templates. Copy, customize, and add to your `settings.json`.

## PreToolUse Templates

### Block Sensitive Files

```bash
#!/bin/bash
# ~/.claude/scripts/protect-files.sh
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

BLOCKED_PATTERNS=(
    ".env"
    ".env.local"
    "credentials"
    "secrets"
    ".git/"
    "package-lock.json"
    "yarn.lock"
    "pnpm-lock.yaml"
    "node_modules/"
    "__pycache__/"
    ".ssh/"
    "id_rsa"
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
    if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "BLOCKED: Cannot modify files matching '$pattern'" >&2
        exit 2
    fi
done

exit 0
```

**Config:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/scripts/protect-files.sh",
        "timeout": 5
      }]
    }]
  }
}
```

---

### Validate Bash Commands

```bash
#!/bin/bash
# ~/.claude/scripts/validate-bash.sh
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block dangerous commands
DANGEROUS=(
    "rm -rf /"
    "rm -rf ~"
    "rm -rf \$HOME"
    ":(){:|:&};:"
    "mkfs"
    "dd if="
    "> /dev/sd"
    "chmod -R 777 /"
)

for pattern in "${DANGEROUS[@]}"; do
    if [[ "$CMD" == *"$pattern"* ]]; then
        echo "BLOCKED: Dangerous command detected: $pattern" >&2
        exit 2
    fi
done

exit 0
```

**Config:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/scripts/validate-bash.sh",
        "timeout": 5
      }]
    }]
  }
}
```

---

### Auto-Approve Read Operations

```bash
#!/bin/bash
# ~/.claude/scripts/auto-approve-read.sh
# Returns JSON to auto-approve read operations

cat << 'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Read operations are safe"
  }
}
EOF
exit 0
```

**Config:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Read|Glob|Grep",
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/scripts/auto-approve-read.sh"
      }]
    }]
  }
}
```

---

## PostToolUse Templates

### Auto-Format Code

```bash
#!/bin/bash
# ~/.claude/scripts/auto-format.sh
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Skip if no file path
[ -z "$FILE_PATH" ] && exit 0
[ ! -f "$FILE_PATH" ] && exit 0

# Get extension
EXT="${FILE_PATH##*.}"

case "$EXT" in
    js|jsx|ts|tsx|json|css|scss|html|md)
        npx prettier --write "$FILE_PATH" 2>/dev/null || true
        ;;
    py)
        black "$FILE_PATH" 2>/dev/null || true
        ;;
    go)
        gofmt -w "$FILE_PATH" 2>/dev/null || true
        ;;
    rs)
        rustfmt "$FILE_PATH" 2>/dev/null || true
        ;;
esac

exit 0
```

**Config:**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/scripts/auto-format.sh",
        "timeout": 30
      }]
    }]
  }
}
```

---

### Log All Tool Usage

```bash
#!/bin/bash
# ~/.claude/scripts/log-tools.sh
INPUT=$(cat)
LOG_FILE="$HOME/.claude/logs/tool-usage.log"

mkdir -p "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
TOOL=$(echo "$INPUT" | jq -r '.tool_name // "unknown"')
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name // "unknown"')

# Log summary
echo "[$TIMESTAMP] $EVENT: $TOOL" >> "$LOG_FILE"

# Log full input (optional, verbose)
# echo "$INPUT" | jq -c >> "${LOG_FILE}.jsonl"

exit 0
```

**Config:**
```json
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/scripts/log-tools.sh"
      }]
    }]
  }
}
```

---

## SessionStart Templates

### Git Sync on Start

```bash
#!/bin/bash
# ~/.claude/scripts/session-start-sync.sh

# Sync marketplace
MARKETPLACE="$HOME/.claude/plugins/marketplaces/claude-skills-marketplace"
if [ -d "$MARKETPLACE/.git" ]; then
    cd "$MARKETPLACE" && git pull --quiet origin master 2>/dev/null || true
fi

# Sync core skills
CONFIG="$MARKETPLACE/skills/julien-workflow-sync-personal-skills/sync-config.json"
SKILLS_DIR="$HOME/.claude/skills"

if [ -f "$CONFIG" ]; then
    mkdir -p "$SKILLS_DIR"
    SKILLS=$(jq -r '.skills_to_sync[]' "$CONFIG" 2>/dev/null | tr -d '\r')
    for skill in $SKILLS; do
        src="$MARKETPLACE/skills/$skill"
        [ -d "$src" ] && rm -rf "$SKILLS_DIR/$skill" && cp -r "$src" "$SKILLS_DIR/"
    done
fi

exit 0
```

---

### Load Project Context

```bash
#!/bin/bash
# ~/.claude/scripts/load-context.sh
# stdout becomes context for the session

echo "=== Project Context ==="

# Git info
if [ -d ".git" ]; then
    echo "Branch: $(git branch --show-current 2>/dev/null)"
    echo "Last commit: $(git log -1 --oneline 2>/dev/null)"
    echo "Status: $(git status --short 2>/dev/null | wc -l) changed files"
fi

# Node.js project
if [ -f "package.json" ]; then
    echo "Node project: $(jq -r '.name // "unnamed"' package.json)"
    echo "Version: $(jq -r '.version // "0.0.0"' package.json)"
fi

# Python project
if [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    echo "Python project detected"
    [ -f ".python-version" ] && echo "Python: $(cat .python-version)"
fi

exit 0
```

**Config:**
```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/scripts/load-context.sh",
        "timeout": 10
      }]
    }]
  }
}
```

---

## SessionEnd Templates

### Auto-Commit Changes

```bash
#!/bin/bash
# ~/.claude/scripts/session-end-commit.sh

MARKETPLACE="$HOME/.claude/plugins/marketplaces/claude-skills-marketplace"

[ ! -d "$MARKETPLACE/.git" ] && exit 0

cd "$MARKETPLACE" || exit 0

if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    git add -A
    git commit -m "Auto-sync: $(date +%Y-%m-%d_%H:%M)" 2>/dev/null || true
    git push origin master 2>/dev/null || true
fi

exit 0
```

---

## UserPromptSubmit Templates

### Add Timestamp to Prompts

```bash
#!/bin/bash
# ~/.claude/scripts/add-timestamp.sh
echo "Current time: $(date '+%Y-%m-%d %H:%M:%S %Z')"
exit 0
```

---

### Inject Environment Info

```bash
#!/bin/bash
# ~/.claude/scripts/env-info.sh
echo "=== Environment ==="
echo "OS: $(uname -s)"
echo "PWD: $(pwd)"
echo "User: $(whoami)"
[ -n "$VIRTUAL_ENV" ] && echo "Venv: $VIRTUAL_ENV"
[ -n "$NVM_DIR" ] && echo "Node: $(node -v 2>/dev/null)"
exit 0
```

---

## Stop Hook Templates (LLM-based)

### Task Completion Check

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Review the conversation and determine if Claude should stop. Check: 1) Were all user requests addressed? 2) Are there pending todos? 3) Did Claude ask a question that needs an answer? Respond with 'approve' to stop or 'block' to continue.",
        "timeout": 30
      }]
    }]
  }
}
```

---

## Combined Configuration Example

Full `~/.claude/settings.json` with multiple hooks:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/scripts/session-start-sync.sh",
        "timeout": 30
      }]
    }],
    "SessionEnd": [{
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/scripts/session-end-commit.sh",
        "timeout": 30
      }]
    }],
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "bash ~/.claude/scripts/protect-files.sh",
          "timeout": 5
        }]
      },
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "bash ~/.claude/scripts/validate-bash.sh",
          "timeout": 5
        }]
      }
    ],
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/scripts/auto-format.sh",
        "timeout": 30
      }]
    }],
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/scripts/env-info.sh",
        "timeout": 5
      }]
    }]
  }
}
```
