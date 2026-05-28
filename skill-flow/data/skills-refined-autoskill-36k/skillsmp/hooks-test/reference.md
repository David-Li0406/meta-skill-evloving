# Hook Payload Reference

Complete JSON schemas for Claude Code hook events.

---

## Common Fields (All Events)

```json
{
  "session_id": "string",
  "transcript_path": "string (absolute path to .jsonl)",
  "cwd": "string (absolute path)",
  "permission_mode": "default|plan|acceptEdits|bypassPermissions",
  "hook_event_name": "string (event type)"
}
```

---

## Event Payloads

### PreToolUse

```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Write|Edit|Bash|Read|Glob|Grep|WebFetch|Task|...",
  "tool_input": { /* tool-specific */ },
  "tool_use_id": "toolu_..."
}
```

**Tool Input Examples:**

```json
// Bash
{"command": "npm test", "description": "Run tests"}

// Write
{"file_path": "/abs/path/file.ts", "content": "..."}

// Edit
{"file_path": "/abs/path", "old_string": "...", "new_string": "..."}

// Read
{"file_path": "/abs/path", "offset": 0, "limit": 2000}

// Glob
{"pattern": "**/*.ts", "path": "/optional/base"}

// Grep
{"pattern": "regex", "path": "/search/path", "glob": "*.ts"}
```

---

### PostToolUse

```json
{
  "hook_event_name": "PostToolUse",
  "tool_name": "string",
  "tool_input": { /* same as PreToolUse */ },
  "tool_response": { /* tool-specific result */ },
  "tool_use_id": "toolu_..."
}
```

**Tool Response Examples:**

```json
// Write
{"filePath": "/abs/path", "success": true}

// Bash
{"stdout": "...", "stderr": "...", "exit_code": 0}

// Read
{"content": "file contents..."}
```

---

### UserPromptSubmit

```json
{
  "hook_event_name": "UserPromptSubmit",
  "prompt": "string (user input)"
}
```

---

### Notification

```json
{
  "hook_event_name": "Notification",
  "message": "string",
  "notification_type": "permission_prompt|idle_prompt|auth_success|elicitation_dialog"
}
```

---

### Stop

```json
{
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

**Note:** `stop_hook_active=true` means Claude is already continuing from a previous stop hook (prevents infinite loops).

---

### SubagentStop

```json
{
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false
}
```

---

### PreCompact

```json
{
  "hook_event_name": "PreCompact",
  "trigger": "manual|auto",
  "custom_instructions": "string (empty for auto)"
}
```

---

### SessionStart

```json
{
  "hook_event_name": "SessionStart",
  "source": "startup|resume|clear|compact"
}
```

**Additional env var:** `CLAUDE_ENV_FILE` - path to write persistent env vars.

---

### SessionEnd

```json
{
  "hook_event_name": "SessionEnd",
  "reason": "clear|logout|prompt_input_exit|other"
}
```

---

## Environment Variables

| Variable | Available | Description |
|----------|-----------|-------------|
| `CLAUDE_PROJECT_DIR` | Always | Absolute path to project root |
| `CLAUDE_CODE_REMOTE` | Always | `"true"` if remote, empty if local |
| `CLAUDE_ENV_FILE` | SessionStart only | Path for persistent env vars |

---

## Output Formats

### Exit Codes

| Code | Behavior |
|------|----------|
| 0 | Success. stdout parsed as JSON. |
| 2 | Block. stderr shown to Claude. stdout ignored. |
| Other | Non-blocking error. stderr shown to user. |

---

### JSON Output (Exit 0)

**Common fields:**

```json
{
  "continue": true,
  "stopReason": "string (when continue=false)",
  "suppressOutput": false,
  "systemMessage": "string (warning to user)",
  "hookSpecificOutput": { /* event-specific */ }
}
```

---

### PreToolUse Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "string",
    "updatedInput": {
      "field": "modified value"
    }
  }
}
```

---

### PostToolUse Output

```json
{
  "decision": "block",
  "reason": "string (shown to Claude)",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "string"
  }
}
```

---

### UserPromptSubmit Output

**Plain text:** Any non-JSON stdout is added as context.

**JSON:**

```json
{
  "decision": "block",
  "reason": "string (shown to user, NOT Claude)",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "string"
  }
}
```

---

### Stop/SubagentStop Output

```json
{
  "decision": "block",
  "reason": "string (tells Claude how to proceed)"
}
```

---

### SessionStart Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "string"
  }
}
```

---

### PermissionRequest Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": { "field": "value" },
      "message": "string (for deny)",
      "interrupt": false
    }
  }
}
```

---

## MCP Tool Matching

MCP tools use pattern: `mcp__<server>__<tool>`

```json
{"matcher": "mcp__memory__create_entities"}
{"matcher": "mcp__filesystem__.*"}
{"matcher": "mcp__.*__write.*"}
```

---

## Hook Execution

| Property | Value |
|----------|-------|
| Timeout | 60s default, configurable via `"timeout"` |
| Parallelization | All matching hooks run in parallel |
| Deduplication | Identical commands auto-deduplicated |
| Input | JSON via stdin |
| Config reload | Requires `/hooks` menu after external edits |
