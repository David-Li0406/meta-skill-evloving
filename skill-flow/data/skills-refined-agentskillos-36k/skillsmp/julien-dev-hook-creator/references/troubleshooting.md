# Hook Troubleshooting

Common errors and solutions when working with Claude Code hooks.

## Error: "hook error" in Claude Code UI

### Symptom
Message `SessionStart:resume hook error` or similar appears.

### Common Causes

#### 1. Script Not Found
```
bash: /path/to/script.sh: No such file or directory
```

**Solution**:
```bash
# Check script exists
ls -la ~/.claude/scripts/my-hook.sh

# Create scripts directory if missing
mkdir -p ~/.claude/scripts/
```

#### 2. Script Not Executable
```
bash: /path/to/script.sh: Permission denied
```

**Solution**:
```bash
chmod +x ~/.claude/scripts/my-hook.sh
```

#### 3. Windows CRLF Line Endings
Script fails silently or has `\r` in output.

**Solution**:
```bash
# Convert to Unix line endings
sed -i 's/\r$//' ~/.claude/scripts/my-hook.sh

# Or use tr in your script
SKILLS=$(jq -r '.skills[]' config.json | tr -d '\r')
```

#### 4. Windows Path Expansion (~, $HOME, %USERPROFILE%)

On Windows, Claude Code doesn't expand `~`, `$HOME`, or `%USERPROFILE%` in hook commands.

**Symptom**:
```
python: can't open file 'C:\Users\julien\~\.claude\scripts\...'
```

**Solution**: Use inline Python with `Path.home()` for 100% portable paths:
```json
{
  "type": "command",
  "command": "python -c \"import runpy;from pathlib import Path;runpy.run_path(str(Path.home()/'.claude/scripts/my-hook.py'),run_name='__main__')\"",
  "timeout": 10
}
```

This works on Windows, macOS, and Linux without any hardcoded paths.

---

## Error: "jq: command not found"

### Symptom
Hook fails when trying to parse JSON input.

### Solution

**Windows (winget)**:
```bash
winget install jqlang.jq
```

**macOS (brew)**:
```bash
brew install jq
```

**Linux (apt)**:
```bash
sudo apt install jq
```

**Alternative without jq** (using grep/sed):
```bash
# Extract simple values without jq
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)
```

---

## Error: "Hook timeout exceeded"

### Symptom
Hook takes too long and gets killed.

### Causes
- Network operations in hook
- Large file operations
- Infinite loops

### Solutions

1. **Increase timeout** (if operation is legitimately slow):
```json
{
  "type": "command",
  "command": "bash ~/.claude/scripts/slow-hook.sh",
  "timeout": 120
}
```

2. **Run async** (don't block Claude):
```bash
#!/bin/bash
# Run in background, don't wait
nohup ~/.claude/scripts/slow-operation.sh &>/dev/null &
exit 0
```

3. **Add timeout to script**:
```bash
#!/bin/bash
timeout 10 some-slow-command || exit 0
```

---

## Error: Hook Blocks Unexpectedly

### Symptom
Operations are blocked when they shouldn't be.

### Debug Steps

1. **Test script manually**:
```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"/test/file.txt"}}' | bash ~/.claude/scripts/my-hook.sh
echo "Exit code: $?"
```

2. **Check exit codes**:
- `exit 0` = allow
- `exit 2` = block
- Make sure you're not accidentally exiting with code 2

3. **Add debug logging**:
```bash
#!/bin/bash
INPUT=$(cat)
echo "[DEBUG] Input: $INPUT" >> ~/.claude/logs/hook-debug.log
echo "[DEBUG] File: $(echo "$INPUT" | jq -r '.tool_input.file_path')" >> ~/.claude/logs/hook-debug.log

# Your logic
exit 0
```

---

## Error: Hook Doesn't Trigger

### Symptom
Hook never executes even though event should fire.

### Checklist

1. **Verify settings.json syntax**:
```bash
cat ~/.claude/settings.json | jq .
# Should parse without errors
```

2. **Check hook structure**:
```json
{
  "hooks": {
    "PreToolUse": [      // ← Array of matchers
      {
        "matcher": "Write",  // ← Optional matcher
        "hooks": [           // ← Array of hooks
          {
            "type": "command",
            "command": "..."
          }
        ]
      }
    ]
  }
}
```

3. **Verify matcher pattern**:
```json
// These are different:
"matcher": "Write"      // Exact match only
"matcher": "Write|Edit" // Either Write or Edit
"matcher": ".*"         // Any tool (regex)
```

4. **Check scope**:
- Global: `~/.claude/settings.json`
- Project: `.claude/settings.json`
- Local: `.claude/settings.local.json` (highest priority)

---

## Error: JSON Output Not Parsed

### Symptom
Advanced JSON output is ignored.

### Correct Format
```bash
#!/bin/bash
# Output JSON to stdout (not stderr!)
cat << 'EOF'
{
  "continue": true,
  "systemMessage": "Hook executed successfully"
}
EOF
exit 0  # Must exit 0 for JSON to be parsed
```

### Common Mistakes
```bash
# ❌ Wrong: JSON to stderr
echo '{"continue":true}' >&2

# ❌ Wrong: Non-zero exit
echo '{"continue":true}'
exit 1

# ❌ Wrong: Extra output before JSON
echo "Starting hook..."
echo '{"continue":true}'
```

---

## Error: Environment Variables Not Set

### Symptom
`$CLAUDE_PROJECT_DIR` or other env vars are empty.

### Available Variables
- `CLAUDE_PROJECT_DIR` - Current project directory
- `CLAUDE_CODE_REMOTE` - Remote mode indicator
- `CLAUDE_ENV_FILE` - (SessionStart only) Path to persist env vars

### SessionStart Env Persistence
```bash
#!/bin/bash
# Write to CLAUDE_ENV_FILE to persist vars
if [ -n "$CLAUDE_ENV_FILE" ]; then
    echo "MY_VAR=my_value" >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

---

## Debugging Checklist

Before reporting a bug:

- [ ] Script exists at specified path
- [ ] Script has execute permission (`chmod +x`)
- [ ] Script works when run manually
- [ ] settings.json is valid JSON
- [ ] Correct hook event name (case-sensitive)
- [ ] Correct matcher pattern
- [ ] Script outputs to correct stream (stdout vs stderr)
- [ ] Exit code is correct (0, 2, or other)
- [ ] No Windows CRLF issues
- [ ] `jq` is installed if used
- [ ] Timeout is sufficient
