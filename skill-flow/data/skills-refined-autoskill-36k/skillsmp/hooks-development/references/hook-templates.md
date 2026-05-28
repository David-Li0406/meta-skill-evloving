# Hook Templates

Copy-paste templates for common hook patterns.

## PostToolUse: Non-Blocking Reminder

Use when you want Claude to see a message but NOT block the operation.

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
#!/usr/bin/env bash
# PostToolUse hook - non-blocking reminder
# Trigger: PostToolUse on Edit|Write (configure in hooks.json)

set -euo pipefail

# Read JSON payload from stdin
PAYLOAD=$(cat)

# Extract file path from tool input
FILE_PATH=$(echo "$PAYLOAD" | jq -r '.tool_input.file_path // empty')

# Exit silently if no file path
[[ -z "$FILE_PATH" ]] && exit 0

# Your condition check here
if [[ "$FILE_PATH" == *"some_pattern"* ]]; then
    # Output JSON with decision:block - REQUIRED for Claude visibility
    jq -n \
        --arg reason "[HOOK_NAME] Your message to Claude here" \
        '{decision: "block", reason: $reason}'
fi

exit 0
PREFLIGHT_EOF
```

### hooks.json Entry

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": "$HOME/.claude/plugins/.../hooks/your-hook.sh",
          "timeout": 5000
        }
      ]
    }
  ]
}
```

## PreToolUse: Blocking Guard

Use when you want to STOP an operation from proceeding.

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF_2'
#!/usr/bin/env bash
# PreToolUse hook - blocking guard
# Trigger: PreToolUse on Bash (configure in hooks.json)

set -euo pipefail

PAYLOAD=$(cat)

# Extract command being executed
COMMAND=$(echo "$PAYLOAD" | jq -r '.tool_input.command // empty')

[[ -z "$COMMAND" ]] && exit 0

# Check for dangerous pattern
if [[ "$COMMAND" == *"rm -rf"* ]]; then
    # Exit code 2 = hard block, stderr shown to Claude
    echo "BLOCKED: Dangerous rm -rf command detected" >&2
    exit 2
fi

exit 0
PREFLIGHT_EOF_2
```

### hooks.json Entry

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "$HOME/.claude/plugins/.../hooks/guard.sh",
          "timeout": 15
        }
      ]
    }
  ]
}
```

## PostToolUse: With Cache for Performance

Use when you need to check against a list that's expensive to generate.

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF_3'
#!/usr/bin/env bash
# PostToolUse hook with caching

set -euo pipefail

PAYLOAD=$(cat)
FILE_PATH=$(echo "$PAYLOAD" | jq -r '.tool_input.file_path // empty')

[[ -z "$FILE_PATH" ]] && exit 0

# Expand ~ to absolute path
ABSOLUTE_PATH=$(eval echo "$FILE_PATH")

# Cache with 5-minute TTL
CACHE_FILE="${TMPDIR:-/tmp}/my-hook-cache.txt"

if [[ ! -f "$CACHE_FILE" ]] || [[ $(find "$CACHE_FILE" -mmin +5 2>/dev/null) ]]; then
    # Regenerate cache (expensive operation)
    generate_list_command > "$CACHE_FILE" || exit 0
fi

# Check against cached list
if grep -qxF "$ABSOLUTE_PATH" "$CACHE_FILE" 2>/dev/null; then
    jq -n \
        --arg reason "[HOOK] File is in tracked list: $ABSOLUTE_PATH" \
        '{decision: "block", reason: $reason}'
fi

exit 0
PREFLIGHT_EOF_3
```

## Bash Boilerplate

Common patterns used across hooks:

```bash
/usr/bin/env bash << 'HOOK_TEMPLATES_SCRIPT_EOF'
#!/usr/bin/env bash
set -euo pipefail

# Read payload
PAYLOAD=$(cat)

# Common extractions
FILE_PATH=$(echo "$PAYLOAD" | jq -r '.tool_input.file_path // empty')
COMMAND=$(echo "$PAYLOAD" | jq -r '.tool_input.command // empty')
TOOL_NAME=$(echo "$PAYLOAD" | jq -r '.tool_name // empty')

# Path expansion
ABSOLUTE_PATH=$(eval echo "$FILE_PATH")
REL_PATH="${ABSOLUTE_PATH/#$HOME/~}"

# Safe JSON output with jq
jq -n \
    --arg reason "Your message" \
    --arg context "Extra info" \
    '{
        decision: "block",
        reason: $reason,
        hookSpecificOutput: {
            additionalContext: $context
        }
    }'
HOOK_TEMPLATES_SCRIPT_EOF
```

## Testing Your Hook

1. Make hook executable:

   ```bash
   chmod +x your-hook.sh
   ```

2. Add to settings.json (or hooks.json for plugins):

   ```json
   {
     "hooks": {
       "PostToolUse": [
         {
           "matcher": "Edit",
           "hooks": [{ "type": "command", "command": "/path/to/your-hook.sh" }]
         }
       ]
     }
   }
   ```

3. Restart Claude Code session

4. Edit a file that matches your condition

5. Check for system-reminder in conversation
