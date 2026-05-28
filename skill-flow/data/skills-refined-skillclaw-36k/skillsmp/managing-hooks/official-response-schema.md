# Official Hook Response Schema

Complete reference for the official Claude Code hook response schema based on https://code.claude.com/docs/en/hooks#response-schema

## Complete Schema Structure

All hooks can return this complete response structure:

```json
{
  "continue": true,
  "stopReason": "string",
  "suppressOutput": false,
  "systemMessage": "string",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart|PreCompact|PostToolUse|etc",
    "additionalContext": "string"
  }
}
```

## Common Fields (Available to ALL Hook Types)

These fields are available regardless of hook event type:

### `continue` (boolean, default: true)
Controls whether execution should proceed after the hook runs.
- `true`: Allow normal execution flow
- `false`: Halt execution (show `stopReason` to user)

**Use cases:**
- Prevent compaction in PreCompact hooks
- Block tool execution in PreToolUse hooks
- Stop session in SessionStart if validation fails

### `stopReason` (string, optional)
Message displayed to user when `continue` is false.

**Example:**
```json
{
  "continue": false,
  "stopReason": "Missing required API key. Please configure ANTHROPIC_API_KEY."
}
```

### `suppressOutput` (boolean, default: false)
Controls whether hook stdout appears in transcript logs.
- `false`: Hook output visible in logs (default)
- `true`: Hide hook output from transcript (useful for sensitive operations)

**Use cases:**
- Hide sensitive validation checks
- Suppress verbose logging
- Keep transcript clean for audit hooks

### `systemMessage` (string, optional)
User-facing notification message shown via OS/desktop notifications or console warnings.

**Purpose:** External notification for user who may not be looking at terminal

**Examples:**
- "Found quicksave.md from previous session"
- "Context compaction imminent - consider saving state"
- "File write logged to audit trail"

## Hook-Specific Output

### `hookSpecificOutput` (object, optional)

Contains event-specific data that varies by hook type.

#### `hookEventName` (string, required in hookSpecificOutput)
Identifies the hook event type. Useful for:
- Generic wrappers that handle multiple hook types
- Notification systems that route based on event
- Logging and audit systems

**Valid values:** `SessionStart`, `SessionEnd`, `PreCompact`, `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `Notification`

#### `additionalContext` (string, optional)
Information injected directly into Claude's conversation context. Claude receives this in `<system-reminder>` tags.

**Purpose:** Provide instructions, context, or structured data for Claude to act upon

**Format:** Can be plain text or JSON string (see Advanced Usage section)

## Complete Examples by Hook Type

### SessionStart Hook
```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Found quicksave.md from previous session",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "User has unfinished work from previous session. Inform them about /quicksave-load."
  }
}
```

### PreCompact Hook
```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Context compaction imminent - consider saving state",
  "hookSpecificOutput": {
    "hookEventName": "PreCompact",
    "additionalContext": "Critical: Context will be compacted. Check for unfinished work and recommend /quicksave if needed."
  }
}
```

### PostToolUse Hook
```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "File write logged to audit trail",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "File modified: src/main.py. Logged at 2025-01-15T10:30:00Z."
  }
}
```

### PreToolUse Hook (Blocking)
```json
{
  "continue": false,
  "stopReason": "Cannot write to protected file: .env",
  "systemMessage": "Write operation blocked - protected file",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "Write to .env file was blocked by security policy."
  }
}
```

## Advanced Usage: Structured JSON in additionalContext

For complex hooks that need to provide precise, structured instructions to Claude, store a **JSON string** inside the `additionalContext` field.

### Why Use Structured JSON?

**Benefits for Claude:**
- Reliable parsing without string manipulation
- Clear semantic meaning for each field
- Programmatic access to severity, action types, and instructions
- Conditional logic based on structured data
- Future-proof extensibility

**Benefits for Hook Authors:**
- Explicit contract and documentation
- Type-safe structure
- Easy validation and testing
- Clear separation of concerns

### Recommended Structure

```json
{
  "severity": "info|warning|critical",
  "assistant_action": "inform_and_wait|evaluate_and_recommend|inform_only",
  "assistant_instruction": "Detailed instructions for Claude's behavior",
  "user_message": "Message Claude should display to user",
  "checks_required": ["check1", "check2"],
  "suggested_commands": ["/command1"],
  "metadata": {}
}
```

### Complete Example with Structured additionalContext

```python
import json

# Build structured data for Claude
additional_context_data = {
    "severity": "critical",
    "assistant_action": "evaluate_and_recommend",
    "assistant_instruction": "Check if there are unfinished todos, active errors, or mid-implementation work. If YES: STRONGLY recommend /quicksave before continuing. If NO: Inform user about compaction and let them decide.",
    "user_message": "Context is full and will be compacted. Run /quicksave if you have unfinished work to preserve.",
    "checks_required": [
        "unfinished_todos",
        "active_errors",
        "mid_implementation"
    ]
}

# Build complete response with official schema
response = {
    "continue": True,
    "suppressOutput": False,
    "systemMessage": "Context compaction imminent - consider saving state",
    "hookSpecificOutput": {
        "hookEventName": "PreCompact",
        "additionalContext": json.dumps(additional_context_data)
    }
}

# Output to stdout
print(json.dumps(response, ensure_ascii=False))
```

### Field Purpose Guide: No Redundancy

Each field serves a distinct, non-overlapping purpose:

| Field | Purpose | Audience | Context |
|-------|---------|----------|---------|
| `systemMessage` | External notification | User | Desktop/OS notification (user may not be looking at terminal) |
| `additionalContext` → `user_message` | In-conversation message | User | Chat message during active conversation with Claude |
| `additionalContext` → `assistant_instruction` | Behavior guidance | Claude | Detailed instructions on how Claude should act |
| `additionalContext` → `assistant_action` | Behavior type | Claude | Programmatic check for action category |
| `additionalContext` → `severity` | Urgency level | Claude | Tone and priority (info/warning/critical) |

**Key Distinction:**
- `systemMessage`: Notification delivered via OS (async, user away from terminal)
- `user_message`: Message in active Claude conversation (sync, user engaged)

Both are needed because they serve different UX contexts and timing.

## Field Reference Summary

| Field | Type | Required | Default | Purpose |
|-------|------|----------|---------|---------|
| `continue` | boolean | No | true | Control execution flow |
| `stopReason` | string | No | - | Message when halting |
| `suppressOutput` | boolean | No | false | Hide stdout from transcript |
| `systemMessage` | string | No | - | User notification |
| `hookSpecificOutput` | object | No | - | Event-specific data |
| `hookSpecificOutput.hookEventName` | string | Yes* | - | Hook event type |
| `hookSpecificOutput.additionalContext` | string | No | - | Context for Claude |

\* Required if `hookSpecificOutput` is present

## Migration Guide: Plain Text to Structured

### Before (Plain Text)
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Assistant: Inform user about quicksave.\nUser: A quicksave file exists. Type /quicksave-load to restore it."
  }
}
```

### After (Structured JSON)
```json
{
  "systemMessage": "Found quicksave.md from previous session",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "{\"severity\":\"info\",\"assistant_action\":\"inform_and_wait\",\"assistant_instruction\":\"Inform the user that a quicksave exists. Wait for them to decide if they want to load it.\",\"user_message\":\"A quicksave file exists. Type /quicksave-load to restore it, or continue without loading.\"}"
  }
}
```

**Improvements:**
- ✅ Separate notification channel via `systemMessage`
- ✅ Programmatic access to `severity` and `assistant_action`
- ✅ No string parsing or regex needed
- ✅ Clear separation of concerns
- ✅ Extensible structure

## Working Examples

See these scripts for complete implementations:
- `~/.claude/hooks/sessionstart-quicksave-check.py` - Info-level with inform_and_wait
- `~/.claude/hooks/precompact-quicksave-reminder.py` - Critical-level with evaluate_and_recommend
- `~/.claude/hooks/hook-wrapper-with-notification.py` - Wrapper that extracts systemMessage

## Validation

Before deploying a hook that uses the official schema:

- [ ] Valid JSON output (test with `python script.py | python -m json.tool`)
- [ ] `hookEventName` matches actual hook event type
- [ ] `systemMessage` is concise (< 100 chars) for desktop notifications
- [ ] `additionalContext` contains information Claude needs to act
- [ ] If using structured JSON in `additionalContext`, it's properly stringified
- [ ] `continue` field used appropriately (false only when halting is needed)
- [ ] Exit code aligns with intent (0 for success, 2 for block in PreToolUse)
