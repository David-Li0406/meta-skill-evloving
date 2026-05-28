---
title: Hook Input/Output Schemas
description: Complete JSON schemas for hook inputs and outputs with tool-specific examples
keywords: hooks, schemas, JSON, input, output, exit codes, tool patterns
skill: creating-hooks
---

# Hook Input/Output Schemas Reference

This document provides comprehensive JSON schemas for hook inputs and outputs.

## Common Input Fields

All hooks receive these common fields via stdin:

```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "hook_event_name": "string"
}
```

## Hook-Specific Input Schemas

### PreToolUse Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "hook_event_name": "PreToolUse",
  "tool_name": "ToolName",
  "tool_input": {
    // Tool-specific parameters
    // Examples:
    // For Write: { "file_path": "...", "content": "..." }
    // For Bash: { "command": "...", "description": "..." }
    // For Read: { "file_path": "...", "offset": 0, "limit": 100 }
  }
}
```

### PostToolUse Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "hook_event_name": "PostToolUse",
  "tool_name": "ToolName",
  "tool_input": {
    // Same as PreToolUse
  },
  "tool_response": {
    // Tool-specific response
    // Examples:
    // For Write: { "filePath": "...", "success": true }
    // For Bash: { "stdout": "...", "stderr": "...", "exitCode": 0 }
    // For Read: { "content": "...", "lineCount": 100 }
  }
}
```

### UserPromptSubmit Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "User's prompt text here"
}
```

### Stop Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

### SubagentStop Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false
}
```

### SessionStart Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "hook_event_name": "SessionStart",
  "source": "startup" // or "resume", "clear", "compact"
}
```

### SessionEnd Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "hook_event_name": "SessionEnd",
  "reason": "exit" // or "clear", "logout", "prompt_input_exit", "other"
}
```

### Notification Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "hook_event_name": "Notification",
  "message": "Notification message text"
}
```

### PreCompact Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "hook_event_name": "PreCompact",
  "trigger": "manual", // or "auto"
  "custom_instructions": "Optional instructions for manual compact"
}
```

## Hook Output Methods

### Simple: Exit Codes

Hooks communicate through exit codes:

- **Exit code 0**: Success
  - stdout shown in transcript (Ctrl-R)
  - Exception: UserPromptSubmit/SessionStart add stdout to context
- **Exit code 2**: Blocking error
  - stderr fed to Claude automatically
  - Behavior varies by event type (see table below)
- **Other exit codes**: Non-blocking error
  - stderr shown to user
  - Execution continues

#### Exit Code 2 Behavior Table

| Event             | Behavior                                                  |
|-------------------|-----------------------------------------------------------|
| PreToolUse        | Blocks tool call, shows stderr to Claude                  |
| PostToolUse       | Shows stderr to Claude (tool already ran)                 |
| UserPromptSubmit  | Blocks prompt, erases prompt, shows stderr to user only   |
| Stop              | Blocks stoppage, shows stderr to Claude                   |
| SubagentStop      | Blocks stoppage, shows stderr to Claude subagent          |
| Notification      | N/A, shows stderr to user only                            |
| SessionStart      | N/A, shows stderr to user only                            |
| SessionEnd        | N/A, shows stderr to user only                            |
| PreCompact        | N/A, shows stderr to user only                            |

### Advanced: JSON Output

Hooks can return structured JSON for more control.

#### Common JSON Output Fields

All hooks can use these optional fields:

```json
{
  "continue": true,              // Whether Claude continues (default: true)
  "stopReason": "string",        // Shown to user when continue=false
  "suppressOutput": true,        // Hide stdout from transcript (default: false)
  "systemMessage": "string"      // Optional warning to user
}
```

#### PreToolUse JSON Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",  // or "deny" or "ask"
    "permissionDecisionReason": "Reason for decision"
  },
  "continue": true,
  "suppressOutput": false
}
```

**permissionDecision values:**
- `"allow"` - Bypass permission system (reason shown to user only)
- `"deny"` - Block tool execution (reason shown to Claude)
- `"ask"` - Prompt user for confirmation (reason shown to user only)

#### PostToolUse JSON Output

```json
{
  "decision": "block",  // or undefined
  "reason": "Explanation for Claude",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Extra context for Claude"
  }
}
```

#### UserPromptSubmit JSON Output

```json
{
  "decision": "block",  // or undefined
  "reason": "Shown to user if blocked",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Added to context if not blocked"
  }
}
```

#### Stop/SubagentStop JSON Output

```json
{
  "decision": "block",  // or undefined
  "reason": "Must be provided when blocking - tells Claude how to proceed"
}
```

#### SessionStart JSON Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Context injected at session start"
  }
}
```

**Note:** Multiple SessionStart hooks have their `additionalContext` concatenated.

## Tool-Specific Input Examples

### Bash Tool Input/Response

```json
// Input
{
  "tool_input": {
    "command": "ls -la",
    "description": "List files in directory",
    "timeout": 120000
  }
}

// Response
{
  "tool_response": {
    "stdout": "file1.txt\nfile2.txt",
    "stderr": "",
    "exitCode": 0
  }
}
```

### Write Tool Input/Response

```json
// Input
{
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "File contents here"
  }
}

// Response
{
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  }
}
```

### Edit Tool Input/Response

```json
// Input
{
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "old_string": "old text",
    "new_string": "new text",
    "replace_all": false
  }
}

// Response
{
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true,
    "replacementCount": 1
  }
}
```

### Read Tool Input/Response

```json
// Input
{
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "offset": 0,
    "limit": 100
  }
}

// Response
{
  "tool_response": {
    "content": "File contents...",
    "lineCount": 50,
    "truncated": false
  }
}
```

## MCP Tool Patterns

MCP tools follow the naming pattern: `mcp__<server>__<tool>`

Examples:
- `mcp__memory__create_entities`
- `mcp__filesystem__read_file`
- `mcp__github__search_repositories`

Hook matchers can target MCP tools:
- `mcp__memory__.*` - All memory server tools
- `mcp__.*__write.*` - All write operations across MCP servers
- `mcp__github__.*` - All GitHub server tools

## Environment Variables

Hooks have access to:
- `$CLAUDE_PROJECT_DIR` - Project root directory (where Claude Code started)
- `${CLAUDE_PLUGIN_ROOT}` - Plugin directory (for plugin hooks only)
- All standard environment variables

## Output Visibility

Where hook output appears:

| Event             | stdout (exit 0)              | stderr (exit 2)         | JSON output          |
|-------------------|------------------------------|-------------------------|----------------------|
| PreToolUse        | Transcript (Ctrl-R)          | Fed to Claude           | Controls permission  |
| PostToolUse       | Transcript (Ctrl-R)          | Fed to Claude           | Adds context         |
| UserPromptSubmit  | **Added to context**         | Shown to user only      | Controls blocking    |
| Stop              | Transcript (Ctrl-R)          | Fed to Claude           | Controls stoppage    |
| SubagentStop      | Transcript (Ctrl-R)          | Fed to Claude subagent  | Controls stoppage    |
| SessionStart      | **Added to context**         | Shown to user only      | Injects context      |
| SessionEnd        | Debug only                   | Shown to user only      | No effect            |
| Notification      | Debug only                   | Shown to user only      | No effect            |
| PreCompact        | Debug only                   | Shown to user only      | No effect            |
