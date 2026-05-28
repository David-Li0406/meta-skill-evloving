# Debugging Guide

Troubleshooting when hook output is not visible to Claude.

## Symptom: Hook Runs But Claude Doesn't See Output

This is the most common issue. Work through this checklist:

### Step 1: Verify Hook Executes

Add debug logging to your hook:

```bash
/usr/bin/env bash << 'DEBUGGING_GUIDE_SCRIPT_EOF'
#!/usr/bin/env bash
set -euo pipefail

# Debug log
echo "$(date): Hook fired" >> /tmp/my-hook-debug.log
echo "PAYLOAD: $(cat)" >> /tmp/my-hook-debug.log

# ... rest of hook
DEBUGGING_GUIDE_SCRIPT_EOF
```

After editing a matching file, check:

```bash
cat /tmp/my-hook-debug.log
```

If no log entry: Hook is not being triggered (check matcher pattern).

### Step 2: Verify JSON Format

Test your JSON output manually:

```bash
echo '{"tool_input":{"file_path":"~/.gitconfig"}}' | ./your-hook.sh | jq .
```

If jq fails: Your hook is outputting invalid JSON.

### Step 3: Confirm decision:block Present

Your output MUST include:

```json
{
  "decision": "block",
  "reason": "Your message"
}
```

Common mistakes:

- `"decision": "blocked"` (wrong value)
- `"decision": true` (wrong type)
- Missing `decision` field entirely
- Outputting plain text instead of JSON

### Step 4: Check Exit Code

Your hook MUST exit with code 0 for JSON output to be processed:

```bash
echo '{"tool_input":{"file_path":"~/.gitconfig"}}' | ./your-hook.sh; echo "Exit: $?"
```

- Exit 0: JSON processed, decision:block required for visibility
- Exit 2: JSON ignored, stderr shown instead
- Other: Output ignored

### Step 5: Verify Matcher Pattern

In hooks.json or settings.json:

```json
{
  "matcher": "Edit|Write",
  "hooks": [...]
}
```

The matcher is a regex. Common issues:

- `"Edit"` won't match `"Write"`
- Missing `|` for OR patterns
- Case sensitivity (use `Edit`, not `edit`)

### Step 6: Restart Claude Code

Hooks are loaded at session start. After any changes to:

- Hook script
- hooks.json
- settings.json

You MUST restart Claude Code for changes to take effect.

## Common Pitfalls

### Pitfall 1: Plain Text Output

```bash
# WRONG - Not visible to Claude
echo "File is tracked by chezmoi"
```

```bash
# CORRECT - Visible to Claude
jq -n --arg reason "File is tracked" '{decision: "block", reason: $reason}'
```

### Pitfall 2: JSON Without decision:block

```bash
# WRONG - Not visible to Claude
echo '{"message": "File is tracked"}'
```

```bash
# CORRECT - Visible to Claude
echo '{"decision": "block", "reason": "File is tracked"}'
```

### Pitfall 3: Using Exit Code 2 with JSON

```bash
# WRONG - JSON ignored with exit 2
jq -n --arg reason "Message" '{decision: "block", reason: $reason}'
exit 2  # JSON ignored, stderr used instead
```

```bash
# CORRECT for soft reminder - JSON processed
jq -n --arg reason "Message" '{decision: "block", reason: $reason}'
exit 0
```

```bash
# CORRECT for hard block - stderr used
echo "BLOCKED: Dangerous operation" >&2
exit 2
```

### Pitfall 4: Silent Failures

```bash
/usr/bin/env bash << 'DEBUGGING_GUIDE_SCRIPT_EOF_2'
# WRONG - jq error silently swallowed
PAYLOAD=$(cat)
FILE_PATH=$(echo "$PAYLOAD" | jq -r '.wrong.path')  # Returns empty, no error
DEBUGGING_GUIDE_SCRIPT_EOF_2
```

```bash
/usr/bin/env bash << 'DEBUGGING_GUIDE_SCRIPT_EOF_3'
# BETTER - Explicit error handling
FILE_PATH=$(echo "$PAYLOAD" | jq -r '.tool_input.file_path // empty')
[[ -z "$FILE_PATH" ]] && exit 0
DEBUGGING_GUIDE_SCRIPT_EOF_3
```

### Pitfall 5: Not Handling Missing Fields

```bash
/usr/bin/env bash << 'DEBUGGING_GUIDE_SCRIPT_EOF_4'
# WRONG - Fails if file_path missing
FILE_PATH=$(echo "$PAYLOAD" | jq -r '.tool_input.file_path')
DEBUGGING_GUIDE_SCRIPT_EOF_4
```

```bash
/usr/bin/env bash << 'DEBUGGING_GUIDE_SCRIPT_EOF_5'
# CORRECT - Graceful fallback
FILE_PATH=$(echo "$PAYLOAD" | jq -r '.tool_input.file_path // empty')
[[ -z "$FILE_PATH" ]] && exit 0
DEBUGGING_GUIDE_SCRIPT_EOF_5
```

## Quick Diagnostic Script

Save as `test-hook.sh`:

```bash
/usr/bin/env bash << 'DEBUGGING_GUIDE_SCRIPT_EOF_6'
#!/usr/bin/env bash
# Test a hook manually

HOOK_PATH="$1"
TEST_FILE="$2"

if [[ -z "$HOOK_PATH" ]] || [[ -z "$TEST_FILE" ]]; then
    echo "Usage: test-hook.sh <hook-path> <test-file-path>"
    exit 1
fi

# Simulate PostToolUse:Edit payload
PAYLOAD=$(jq -n --arg path "$TEST_FILE" '{
    tool_name: "Edit",
    tool_input: {file_path: $path}
}')

echo "=== Testing: $HOOK_PATH ==="
echo "=== Payload: $PAYLOAD ==="
echo "=== Output: ==="

OUTPUT=$(echo "$PAYLOAD" | "$HOOK_PATH")
EXIT_CODE=$?

echo "$OUTPUT"
echo "=== Exit Code: $EXIT_CODE ==="

if [[ $EXIT_CODE -eq 0 ]] && echo "$OUTPUT" | jq -e '.decision == "block"' >/dev/null 2>&1; then
    echo "=== PASS: decision:block found, exit 0 ==="
else
    echo "=== FAIL: Missing decision:block or wrong exit code ==="
fi
DEBUGGING_GUIDE_SCRIPT_EOF_6
```

Usage:

```bash
chmod +x test-hook.sh
./test-hook.sh ./my-hook.sh ~/.gitconfig
```

## Reference

- [Visibility Patterns](./visibility-patterns.md) - Full exit code and JSON schema
- [ADR: PostToolUse Hook Visibility](../../../../../docs/adr/2025-12-17-posttooluse-hook-visibility.md)
