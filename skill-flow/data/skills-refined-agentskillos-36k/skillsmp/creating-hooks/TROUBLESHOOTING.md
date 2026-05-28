# Hook Troubleshooting Guide

Diagnose and fix common Claude Code hook issues.

## Quick Diagnostics

Run these commands first:

```bash
# Check if hook is registered
claude --print-hooks

# Run with debug output
claude --debug

# Test script independently
echo '{"tool_name":"Write","tool_input":{"file_path":"/test.txt"}}' | ./your-hook.sh

# Check script permissions
ls -la ./your-hook.sh
```

## Symptom-Cause-Solution Table

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Hook never runs | JSON syntax error | Validate JSON with `jq` |
| Hook never runs | Matcher does not match | Check case sensitivity, use regex |
| Hook never runs | Script not executable | `chmod +x script.sh` |
| Hook never runs | Wrong path | Use absolute path or `$CLAUDE_PROJECT_DIR` |
| Hook runs but no effect | Exit code wrong | 0=success, 2=block, other=warning |
| Hook runs but no effect | stdout/stderr swapped | Errors to stderr, data to stdout |
| Hook blocks unexpectedly | Exit code 2 | Only use exit 2 for intentional blocks |
| Hook does not block | Exit code not 2 | Exit 2 is the only blocking code |
| Environment vars missing | Wrong hook event | `CLAUDE_ENV_FILE` only in SessionStart |
| Matcher not matching | Regex not enabled | Use `|` for OR, `.*` for wildcards |
| MCP tools not matching | Wrong pattern | Use `mcp__server__tool` format |

## Issue: Hook Not Running

### Check 1: Validate JSON Syntax

Common JSON errors break the entire hooks configuration:

```bash
# Validate settings file
cat ~/.claude/settings.json | jq .

# Common errors:
# - Trailing comma after last array element
# - Unescaped quotes in command strings
# - Missing closing brackets
```

**Bad JSON (trailing comma):**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          { "type": "command", "command": "echo done" },  // <-- trailing comma
        ]
      }
    ]
  }
}
```

**Good JSON:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          { "type": "command", "command": "echo done" }
        ]
      }
    ]
  }
}
```

### Check 2: Verify Matcher Pattern

Matchers are **case-sensitive** and support regex:

| Pattern | Matches | Does NOT Match |
|---------|---------|----------------|
| `Write` | `Write` only | `write`, `WRITE`, `WriteFile` |
| `Write\|Edit` | `Write`, `Edit` | `write`, `edit` |
| `Write.*` | `Write`, `WriteFile` | `write` |
| `mcp__.*` | All MCP tools | Built-in tools |
| `*` or `""` | All tools | - |

**Debugging matchers:**
```bash
# See what tools Claude uses
claude --debug 2>&1 | grep "tool_name"

# Common tool names:
# Write, Edit, Read, Bash, Glob, Grep, WebFetch, WebSearch, Task
# mcp__memory__create_entities, mcp__filesystem__read_file
```

### Check 3: Script Permissions

Scripts must be executable:

```bash
# Check permissions
ls -la /path/to/script.sh
# Should show: -rwxr-xr-x

# Fix permissions
chmod +x /path/to/script.sh
```

### Check 4: Use Absolute Paths

Relative paths fail because hooks run from Claude's current directory:

**Bad:**
```json
{
  "command": "./hooks/format.sh"
}
```

**Good (project-relative):**
```json
{
  "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format.sh"
}
```

**Good (absolute):**
```json
{
  "command": "/Users/me/scripts/format.sh"
}
```

Note the escaped quotes around `$CLAUDE_PROJECT_DIR` - this handles spaces in paths.

### Check 5: Configuration Location

Hooks can be in multiple locations (all are merged):

| File | Scope |
|------|-------|
| `~/.claude/settings.json` | User (all projects) |
| `.claude/settings.json` | Project (committed) |
| `.claude/settings.local.json` | Local (not committed) |

Use `/hooks` command in Claude Code to see all registered hooks.

## Issue: Hook Runs But Has No Effect

### Check 1: Exit Code Semantics

| Exit Code | Meaning | Behavior |
|-----------|---------|----------|
| 0 | Success | stdout parsed for JSON, shown in verbose mode |
| 2 | Block | stderr shown to Claude, action blocked |
| Other | Warning | stderr shown in verbose mode, continues |

**Common mistake - using exit 1 to block:**
```bash
#!/bin/bash
# WRONG: exit 1 only shows a warning
echo "Blocked!" >&2
exit 1  # This does NOT block
```

```bash
#!/bin/bash
# CORRECT: exit 2 blocks the action
echo "Blocked: reason here" >&2
exit 2  # This blocks
```

### Check 2: stdout vs stderr

- **stdout**: Parsed for JSON response, shown in verbose mode
- **stderr**: Error messages shown to user or Claude

**For blocking (exit 2):**
```bash
#!/bin/bash
# stderr is shown to Claude as the block reason
echo "Cannot write to protected file" >&2
exit 2
```

**For JSON responses (exit 0):**
```bash
#!/bin/bash
# stdout contains JSON response
echo '{"decision":"block","reason":"File is protected"}' >&1
exit 0
```

### Check 3: Test Script Independently

Test your script with the exact input Claude sends:

```bash
# Create test input
cat > /tmp/test-input.json << 'EOF'
{
  "session_id": "test123",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
EOF

# Run your script
cat /tmp/test-input.json | /path/to/your-hook.sh
echo "Exit code: $?"
```

## Issue: Hook Blocks When It Should Not

### Exit Code 2 Only Blocks

Only exit code 2 blocks actions. All other non-zero codes are warnings:

```bash
#!/bin/bash
# DON'T: This blocks unnecessarily
if some_check; then
  echo "Check passed"
else
  exit 2  # Blocks even for non-critical failures
fi
```

```bash
#!/bin/bash
# DO: Only block when truly necessary
if critical_security_check; then
  exit 0
else
  echo "Security violation: $reason" >&2
  exit 2
fi

# For non-critical issues, use exit 1 (warning only)
if style_check; then
  exit 0
else
  echo "Style issue (non-blocking): $issue" >&2
  exit 1
fi
```

### JSON Decision Field

When using JSON output, the `decision` field controls behavior:

| JSON Output | Effect |
|-------------|--------|
| `{"decision": "block", "reason": "..."}` | Blocks action |
| `{"decision": "approve", "reason": "..."}` | Allows action |
| No decision field | Continues normally |

## Issue: Environment Variables Not Available

### Available Environment Variables

| Variable | Available In | Description |
|----------|--------------|-------------|
| `CLAUDE_PROJECT_DIR` | All hooks | Absolute path to project root |
| `CLAUDE_ENV_FILE` | SessionStart only | Path to persist env vars |
| `CLAUDE_PLUGIN_ROOT` | Plugin hooks | Path to plugin directory |
| `CLAUDE_CODE_REMOTE` | All hooks | `"true"` if remote/web |

### SessionStart Environment Persistence

Only SessionStart hooks can persist environment variables:

```bash
#!/bin/bash
# This only works in SessionStart hooks

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export MY_VAR=value' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:/custom/bin"' >> "$CLAUDE_ENV_FILE"
fi
```

### Debugging Environment

```bash
#!/bin/bash
# Debug script - add to hook temporarily

echo "CLAUDE_PROJECT_DIR=$CLAUDE_PROJECT_DIR" >> /tmp/hook-debug.log
echo "CLAUDE_ENV_FILE=$CLAUDE_ENV_FILE" >> /tmp/hook-debug.log
echo "PWD=$(pwd)" >> /tmp/hook-debug.log
env >> /tmp/hook-debug.log

exit 0
```

## Issue: Matcher Not Matching

### Regex Support

Matchers support regex, not glob patterns:

| Pattern Type | Syntax | Example |
|--------------|--------|---------|
| Exact match | `Write` | Matches `Write` only |
| OR | `Write\|Edit` | Matches `Write` or `Edit` |
| Wildcard | `.*` | Any characters |
| Start with | `^Bash` | Starts with `Bash` |
| End with | `File$` | Ends with `File` |

### MCP Tool Patterns

MCP tools follow `mcp__<server>__<tool>` naming:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [{ "type": "command", "command": "..." }]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [{ "type": "command", "command": "..." }]
      }
    ]
  }
}
```

### Case Sensitivity

Matchers are case-sensitive:

```json
{
  "matcher": "write"  // Never matches - tool is "Write"
}
```

```json
{
  "matcher": "Write"  // Correct
}
```

### Debugging Matcher Issues

```bash
# Run Claude with debug to see tool names
claude --debug 2>&1 | grep -E "(tool_name|Matched.*hooks)"
```

Look for lines like:
```
[DEBUG] Getting matching hook commands for PreToolUse with query: Write
[DEBUG] Matched 1 hooks for query "Write"
```

## Debugging Commands

### Essential Commands

```bash
# Check registered hooks
claude --print-hooks

# Run with full debug output
claude --debug

# View hook execution in verbose mode
# Press Ctrl+O in Claude Code to toggle verbose mode

# Validate JSON settings
jq . ~/.claude/settings.json
jq . .claude/settings.json
```

### Debug Output Interpretation

```
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: /path/to/hook.sh with timeout 60000ms
[DEBUG] Hook command completed with status 0: output here
```

| Line | Meaning |
|------|---------|
| `Executing hooks for X:Y` | Hook event X triggered for tool Y |
| `Found N hook matchers` | N matchers defined in settings |
| `Matched N hooks` | N matchers matched this tool |
| `completed with status N` | Exit code was N |

### Script Testing Template

```bash
#!/bin/bash
# test-hook.sh - Test hook script in isolation

# Create sample input
INPUT='{
  "session_id": "test-session",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/test/file.txt",
    "content": "test content"
  }
}'

# Run hook and capture output
echo "$INPUT" | /path/to/your-hook.sh
EXIT_CODE=$?

echo "---"
echo "Exit code: $EXIT_CODE"
echo "Meaning: $(case $EXIT_CODE in
  0) echo "Success (continue)" ;;
  2) echo "Block action" ;;
  *) echo "Warning (continue)" ;;
esac)"
```

## Common JSON Syntax Errors

### Error: Unescaped Quotes

```json
// BAD: Unescaped quotes break JSON
{
  "command": "echo "hello""
}

// GOOD: Escape inner quotes
{
  "command": "echo \"hello\""
}

// BETTER: Use single quotes in command
{
  "command": "echo 'hello'"
}
```

### Error: Trailing Commas

```json
// BAD: Trailing comma
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Write", "hooks": [] },  // <-- trailing comma
    ]
  }
}

// GOOD: No trailing comma
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Write", "hooks": [] }
    ]
  }
}
```

### Error: Single Quotes

```json
// BAD: JSON requires double quotes
{
  'hooks': {
    'PostToolUse': []
  }
}

// GOOD: Use double quotes
{
  "hooks": {
    "PostToolUse": []
  }
}
```

### Error: Comments in JSON

```json
// BAD: JSON doesn't support comments
{
  "hooks": {
    // This is a comment
    "PostToolUse": []
  }
}

// GOOD: Remove comments
{
  "hooks": {
    "PostToolUse": []
  }
}
```

## Debugging Checklist

Use this checklist when hooks are not working:

### Configuration
- [ ] JSON is valid (`jq . settings.json` succeeds)
- [ ] No trailing commas in arrays/objects
- [ ] All quotes properly escaped
- [ ] Hook appears in `/hooks` command output

### Script
- [ ] Script is executable (`chmod +x`)
- [ ] Script uses absolute path or `$CLAUDE_PROJECT_DIR`
- [ ] Script runs successfully in isolation
- [ ] Script reads JSON from stdin correctly
- [ ] Script returns correct exit code (0, 2, or other)

### Matcher
- [ ] Matcher is case-sensitive match for tool name
- [ ] Regex syntax is correct (use `|` not `,` for OR)
- [ ] MCP tools use `mcp__server__tool` format
- [ ] Debug output shows "Matched N hooks"

### Output
- [ ] Blocking uses exit code 2 with stderr message
- [ ] JSON output uses exit code 0
- [ ] stdout/stderr are used correctly
- [ ] JSON output is valid (`echo '{}' | jq .`)

### Environment
- [ ] `CLAUDE_PROJECT_DIR` is used for project-relative paths
- [ ] `CLAUDE_ENV_FILE` only used in SessionStart hooks
- [ ] Debug logging to file for troubleshooting

## Getting Help

If issues persist:

1. Run `claude --debug` and capture full output
2. Check Claude Code logs for error messages
3. Test hook script independently with sample JSON input
4. Validate all JSON files with `jq`
5. Review hook configuration with `/hooks` command
