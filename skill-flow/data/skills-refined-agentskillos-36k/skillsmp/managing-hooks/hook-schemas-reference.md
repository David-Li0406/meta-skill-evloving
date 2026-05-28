# Hook Input/Output Schema Reference

Complete reference for hook input and output schemas for all 9 Claude Code hook event types.

## Common Fields (All Hook Types)

Every hook input contains these base fields:

```json
{
  "session_id": "abc123def456",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/project/root",
  "permission_mode": "default",
  "hook_event_name": "EventName"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | Unique session identifier |
| `transcript_path` | string | Path to conversation transcript (JSONL format) |
| `cwd` | string | Current working directory |
| `permission_mode` | string | One of: "default", "plan", "acceptEdits", "bypassPermissions" |
| `hook_event_name` | string | Name of the triggering event |

---

## Hook Event Schemas

### 1. PreToolUse

**When It Runs**: After Claude creates tool parameters, before tool is called

**Purpose**: Block, allow, or modify tool calls

**Matcher**: Yes (tool name pattern)

#### Input Schema

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",

  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content here"
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `tool_name` | string | Name of tool being called (e.g., "Write", "Bash", "Edit") |
| `tool_input` | object | Parameters for the tool (varies by tool type) |
| `tool_use_id` | string | Unique ID for this tool use |

#### Output Schema

**Command Hook Exit Codes**:
- `0`: Allow tool call
- `2`: Block tool call (show stderr to Claude)
- Other: Non-blocking error (show in verbose mode)

**JSON Output** (exit 0):
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow" | "deny" | "ask",
    "permissionDecisionReason": "Why this decision",
    "updatedInput": {
      "file_path": "/new/path.txt"
    }
  }
}
```

| Field | Options | Description |
|-------|---------|-------------|
| `permissionDecision` | "allow" \| "deny" \| "ask" | "allow": bypass permission, "deny": block, "ask": show permission dialog |
| `permissionDecisionReason` | string | Shown to user (for "deny"), Claude (for "allow"/"ask") |
| `updatedInput` | object | Modified tool input (optional, only with "allow") |

#### Tool Input Examples

**Write**:
```json
{"file_path": "/path/file.txt", "content": "text"}
```

**Bash**:
```json
{"command": "ls -la", "description": "List files"}
```

**Edit**:
```json
{"file_path": "/path/file.txt", "old_string": "old", "new_string": "new"}
```

**Glob**:
```json
{"pattern": "**/*.js"}
```

**Grep**:
```json
{"pattern": "search.*pattern", "type": "js"}
```

---

### 2. PermissionRequest

**When It Runs**: When Claude requests permission (dialog shown to user)

**Purpose**: Allow or deny permission on behalf of user

**Matcher**: Yes (matches tool name like PreToolUse)

#### Input Schema

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/project",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",

  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/*"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `tool_name` | string | Tool requesting permission |
| `tool_input` | object | Tool parameters |

#### Output Schema

**JSON Output** (exit 0):
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow" | "deny",
      "message": "Optional: Why permission was denied"
    }
  }
}
```

Or simplified:
```json
{
  "decision": "approve" | "block",
  "reason": "Explanation"
}
```

| Field | Value | Description |
|-------|-------|-------------|
| `behavior` | "allow" | Grant permission |
| `behavior` | "deny" | Deny permission, stop execution |
| `message` | string | Explanation for denial (shown to user) |

---

### 3. PostToolUse

**When It Runs**: Immediately after tool completes successfully

**Purpose**: React to tool results, provide feedback to Claude

**Matcher**: Yes (tool name pattern)

#### Input Schema

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/project",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",

  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/file.txt",
    "content": "content"
  },
  "tool_response": {
    "filePath": "/path/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `tool_name` | string | Tool that executed |
| `tool_input` | object | Parameters sent to tool |
| `tool_response` | object | Result from tool (varies by tool) |
| `tool_use_id` | string | Unique ID for this tool use |

#### Output Schema

**JSON Output** (exit 0):
```json
{
  "decision": "block" | undefined,
  "reason": "Why to block/continue",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Extra info for Claude"
  }
}
```

| Field | Description |
|-------|-------------|
| `decision` | "block" to provide feedback, undefined/omit to allow silently |
| `reason` | Shown to Claude with "block" decision |
| `additionalContext` | Extra context added discretely |

#### Exit Codes

- `0`: Success, tool result accepted
- `2`: Block (show stderr as error)
- Other: Non-blocking error (shown in verbose mode)

---

### 4. Notification

**When It Runs**: When Claude Code sends notifications

**Purpose**: React to notifications (permission prompts, idle messages, etc.)

**Matcher**: Yes (notification type)

#### Input Schema

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/project",
  "permission_mode": "default",
  "hook_event_name": "Notification",

  "message": "Claude needs your permission to use Bash",
  "notification_type": "permission_prompt"
}
```

| Field | Value | Description |
|-------|-------|-------------|
| `notification_type` | "permission_prompt" | Permission dialog |
| `notification_type` | "idle_prompt" | Claude idle (60+ sec) |
| `notification_type` | "auth_success" | Authentication success |
| `notification_type` | "elicitation_dialog" | MCP tool needs input |

#### Common Notification Types

**permission_prompt**: Permission dialog shown
```json
{"message": "Claude needs permission to use Bash", "notification_type": "permission_prompt"}
```

**idle_prompt**: Claude waiting for input
```json
{"message": "Claude is waiting for your input", "notification_type": "idle_prompt"}
```

#### Output Schema

No structured output expected. Hook can perform side effects (log, send alert, etc.)

---

### 5. UserPromptSubmit

**When It Runs**: Before Claude processes user's input

**Purpose**: Validate prompts, inject context, block inappropriate prompts

**Matcher**: No (no matcher needed)

#### Input Schema

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/project",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",

  "prompt": "Write a function to calculate factorial"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `prompt` | string | User's input text |

#### Output Schema

**Simple (Plain Text)** - exit 0:
```
Additional context to add to conversation
```

**JSON (Structured)** - exit 0:
```json
{
  "decision": "block" | undefined,
  "reason": "Why prompt blocked",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Context to add"
  }
}
```

| Field | Description |
|-------|-------------|
| `decision` | "block" to prevent prompt processing |
| `reason` | Explanation shown to user (only with "block") |
| `additionalContext` | Context injected into conversation |

#### Exit Codes

- `0`: Accept prompt (plain text or JSON output added as context)
- `2`: Block prompt (stderr message shown, prompt erased)
- Other: Non-blocking error

---

### 6. Stop

**When It Runs**: When Claude finishes responding

**Purpose**: Decide if Claude should continue or stop

**Matcher**: No (no matcher needed)

#### Input Schema

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "permission_mode": "default",
  "hook_event_name": "Stop",

  "stop_hook_active": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `stop_hook_active` | boolean | True if Stop hook already ran (prevent infinite loops) |

**Note**: No `cwd` field in Stop hook input.

#### Output Schema

**JSON Output** (exit 0):
```json
{
  "decision": "block" | undefined,
  "reason": "Why Claude must continue"
}
```

| Field | Description |
|-------|-------------|
| `decision` | "block" to prevent Claude from stopping (continue) |
| `reason` | Explanation for Claude (required with "block") |
| undefined | Allow Claude to stop |

#### Special Handling

**Prevent Infinite Loops**: Check `stop_hook_active`:
```bash
if [ "$STOP_ACTIVE" = "true" ]; then
  exit 0  # Allow stop to prevent loop
fi
```

---

### 7. SubagentStop

**When It Runs**: When subagent (Task tool) finishes

**Purpose**: Decide if subagent should continue or stop

**Matcher**: No (no matcher needed)

#### Input Schema

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",

  "stop_hook_active": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `stop_hook_active` | boolean | True if already ran (prevent loops) |

#### Output Schema

**JSON Output** (exit 0):
```json
{
  "decision": "block" | undefined,
  "reason": "Why subagent must continue"
}
```

Similar to Stop hook. Block = continue, undefined = stop.

---

### 8. PreCompact

**When It Runs**: Before context compaction (manual or automatic)

**Purpose**: Prepare for context compaction

**Matcher**: Yes (manual/auto trigger)

#### Input Schema

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/project",
  "permission_mode": "default",
  "hook_event_name": "PreCompact",

  "trigger": "manual" | "auto",
  "custom_instructions": "User's compact message"
}
```

| Field | Value | Description |
|-------|-------|-------------|
| `trigger` | "manual" | Triggered by `/compact` command |
| `trigger` | "auto" | Triggered by automatic compaction |
| `custom_instructions` | string | User's message with `/compact` (if manual) |

#### Output Schema

No structured output expected. Hook can perform preparation tasks.

---

### 9. SessionStart

**When It Runs**: When new session starts or resumed

**Purpose**: Setup environment, load context, verify dependencies

**Matcher**: Yes (startup/resume/clear/compact)

#### Input Schema

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/project",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",

  "source": "startup" | "resume" | "clear" | "compact"
}
```

| Field | Value | Description |
|-------|-------|-------------|
| `source` | "startup" | Session just started |
| `source` | "resume" | Session resumed (--resume flag) |
| `source` | "clear" | Session cleared (/clear command) |
| `source` | "compact" | Session after compaction |

#### Special Environment Variable

**${CLAUDE_ENV_FILE}**: Path to environment persistence file (SessionStart only)

Persist variables for all subsequent bash commands:
```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export API_KEY=...' >> "$CLAUDE_ENV_FILE"
fi
```

#### Output Schema

**JSON Output** (exit 0):
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Context to inject"
  }
}
```

Or plain text context - both appended to session context.

---

### 10. SessionEnd

**When It Runs**: When session terminates

**Purpose**: Cleanup, logging, archiving

**Matcher**: No (no matcher needed)

#### Input Schema

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/project",
  "permission_mode": "default",
  "hook_event_name": "SessionEnd",

  "reason": "exit" | "logout" | "prompt_input_exit" | "other"
}
```

| Field | Value | Description |
|-------|-------|-------------|
| `reason` | "clear" | Session cleared with /clear |
| `reason` | "logout" | User logged out |
| `reason` | "prompt_input_exit" | Exited during prompt input |
| `reason` | "other" | Other exit reasons |

#### Output Schema

No structured output expected. Hook performs cleanup/logging.

---

## Response Format Summary

### Common Response Fields

All JSON responses can include:

```json
{
  "continue": false,              // Stop entire Claude execution
  "stopReason": "message",        // Message shown to user (with continue: false)
  "suppressOutput": true,         // Hide stdout from transcript
  "systemMessage": "warning"      // Additional message to user
}
```

### Hook-Specific Response Fields

**PreToolUse**:
- `hookSpecificOutput.permissionDecision`
- `hookSpecificOutput.updatedInput`

**PermissionRequest**:
- `hookSpecificOutput.decision`

**PostToolUse**:
- `hookSpecificOutput.additionalContext`

**UserPromptSubmit**:
- `hookSpecificOutput.additionalContext`

**Stop/SubagentStop**:
- `decision` (block/undefined)
- `reason`

**SessionStart**:
- `hookSpecificOutput.additionalContext`

---

## Exit Code Behaviors by Event

| Event | Exit 0 | Exit 2 | Other |
|-------|--------|--------|-------|
| **PreToolUse** | Allow tool | Block tool | Non-block error |
| **PermissionRequest** | Allow/deny | N/A | Non-block error |
| **PostToolUse** | Accept result | Block (feedback) | Non-block error |
| **Notification** | Process | N/A | Log error |
| **UserPromptSubmit** | Accept/block | Block prompt | Non-block error |
| **Stop** | Continue/stop | N/A | Non-block error |
| **SubagentStop** | Continue/stop | N/A | Non-block error |
| **PreCompact** | Proceed | N/A | Log error |
| **SessionStart** | Inject context | N/A | Log error |
| **SessionEnd** | Cleanup | N/A | Log error |

---

## Testing Hook Schemas

### Manual Testing

Create test JSON file `test-input.json`:

```json
{
  "session_id": "test123",
  "transcript_path": "/tmp/test.jsonl",
  "cwd": "/tmp",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {"file_path": "/tmp/test.txt", "content": "test"},
  "tool_use_id": "test123"
}
```

Test hook script:
```bash
cat test-input.json | ./my-hook.sh
echo $?  # Check exit code
```

### Debugging with --debug

Enable debug mode to see all hook input/output:

```bash
claude --debug
# Now run interactions to trigger hooks
```

Look for lines like:
```
[DEBUG] Hook input: {...}
[DEBUG] Hook output: {...}
```

---

## See Also

- **SKILL.md**: Hook management overview
- **prompt-hooks-guide.md**: Prompt-based hook schemas
- **plugin-hooks-guide.md**: Plugin hook structure
- **script-examples.md**: Implementing hooks with various schemas
