# Hook Types Reference

Complete specifications for all 10 Claude Code hook event types.

## Hook Event Categories

**Tool-Based Events**: Require matcher to specify which tools trigger the hook
- PreToolUse
- PermissionRequest
- PostToolUse

**Lifecycle Events**: Trigger at session boundaries, no matcher needed
- SessionStart
- SessionEnd

**Agent Events**: Trigger after agent responses, support intelligent continuation
- Stop
- SubagentStop

**Context Events**: Trigger during specific context operations
- UserPromptSubmit
- Notification
- PreCompact

## PreToolUse

**Trigger**: Runs after Claude creates tool parameters and before processing the tool call

**Purpose**: Validate, modify, or block tool calls before execution

**Requires Matcher**: Yes

**Available Matchers**:
- `Task`: Subagent launches
- `Bash`: Shell commands
- `Glob`: File pattern searches
- `Grep`: Content searches
- `Read`: File reads
- `Edit`: File edits
- `Write`: File writes
- `WebFetch`: Web content fetching
- `WebSearch`: Web searches
- MCP tools: `mcp__<server>__<tool>`

**Input Fields** (via stdin JSON):
```json
{
  "session_id": "unique-session-identifier",
  "transcript_path": "/path/to/transcript",
  "cwd": "/current/working/directory",
  "permission_mode": "auto|manual",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file",
    "content": "file content"
  }
}
```

**Output**:
- **Exit code 0**: Allow operation to proceed
- **Exit code 2**: Block operation with error message
- **Other exit codes**: Non-blocking error (operation proceeds with warning)

**Optional JSON Output**:
```json
{
  "decision": "allow|block",
  "permissionDecision": "approve|reject|prompt",
  "updatedInput": {
    "file_path": "/modified/path",
    "content": "modified content"
  },
  "additionalContext": "Information to inject into Claude's context"
}
```

**Use Cases**:
- Block writes to protected files
- Validate file paths and content
- Prevent dangerous bash commands
- Enforce security policies
- Modify tool inputs before execution
- Add warnings or context to Claude

**Example**: Pre-write safety check that warns before modifying `.env` or `requirements.txt`

## PermissionRequest

**Trigger**: Runs when the user is shown a permission dialog

**Purpose**: Allow or deny permissions on behalf of the user

**Requires Matcher**: Yes

**Available Matchers**: Same as PreToolUse

**Input Fields** (via stdin JSON):
```json
{
  "session_id": "unique-session-identifier",
  "transcript_path": "/path/to/transcript",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf dist/",
    "description": "Remove build directory"
  }
}
```

**Output**:
- **Exit code 0**: Let normal permission flow proceed
- **Exit code 2**: Deny permission
- **Other exit codes**: Non-blocking error

**Optional JSON Output**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": {
        "command": "modified command"
      },
      "message": "reason for denial",
      "interrupt": true
    }
  }
}
```

**Use Cases**:
- Auto-approve safe operations (reading documentation files)
- Auto-deny dangerous operations (force push, rm -rf)
- Modify commands before approval (add safety flags)
- Implement time-based or context-aware permission policies

**Example**: Auto-approve Read operations for .md files, deny destructive Bash commands

## PostToolUse

**Trigger**: Executes after successful tool completion

**Purpose**: Process results, log operations, trigger follow-up actions

**Requires Matcher**: Yes

**Available Matchers**: Same as PreToolUse

**Input Fields**:
```json
{
  "session_id": "unique-session-identifier",
  "transcript_path": "/path/to/transcript",
  "cwd": "/current/working/directory",
  "permission_mode": "auto|manual",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file",
    "content": "file content"
  },
  "tool_response": {
    "success": true,
    "output": "Tool execution result"
  }
}
```

**Output**:
- **Exit code 0**: Success
- **Exit code 2**: No blocking effect (tool already executed)
- **Other exit codes**: Non-blocking error

**Optional JSON Output**:
```json
{
  "additionalContext": "Information to inject into Claude's context after tool execution"
}
```

**Use Cases**:
- Log tool usage for compliance
- Track file modifications
- Trigger automated formatting (prettier, gofmt)
- Send desktop notifications
- Update audit trails
- Generate reports

**Example**: Track all file writes to maintain audit history with timestamps and word counts

## UserPromptSubmit

**Trigger**: Activates when users submit prompts

**Purpose**: Validate input, inject context, enforce policies before processing

**Requires Matcher**: No

**Input Fields**:
```json
{
  "session_id": "unique-session-identifier",
  "transcript_path": "/path/to/transcript",
  "cwd": "/current/working/directory",
  "permission_mode": "auto|manual",
  "user_prompt": "The user's submitted prompt text"
}
```

**Output**:
- **Exit code 0**: Allow prompt processing
- **Exit code 2**: Block prompt and show error to user
- **Other exit codes**: Non-blocking error

**Optional JSON Output**:
```json
{
  "decision": "allow|block",
  "updatedInput": "Modified prompt text",
  "additionalContext": "Context to inject before processing prompt"
}
```

**Use Cases**:
- Check for sensitive information in prompts
- Inject project-specific context automatically
- Enforce prompt templates or formats
- Add compliance headers
- Validate request types
- Add current system state to context

**Example**: Automatically inject current git branch and status into every prompt

## SessionStart

**Trigger**: Runs at session initialization or resumption

**Purpose**: Environment setup, validation, initialization

**Requires Matcher**: No

**Input Fields**:
```json
{
  "session_id": "unique-session-identifier",
  "transcript_path": "/path/to/transcript",
  "cwd": "/current/working/directory",
  "permission_mode": "auto|manual"
}
```

**Special Environment Variable**:
- `$CLAUDE_ENV_FILE`: File path for persisting environment variables across session

**Output**:
- **Exit code 0**: Successful initialization
- **Other exit codes**: Non-blocking error (session continues)

**Optional JSON Output**:
```json
{
  "additionalContext": "Information to add to session initialization context"
}
```

**Use Cases**:
- Verify dependencies installed
- Check API keys configured
- Validate virtual environment
- Display project status
- Create necessary directories
- Load environment variables
- Show warnings about environment

**Example**: Check for Anthropic SDK installation, API key configuration, and display current project phase

## SessionEnd

**Trigger**: Executes at session termination

**Purpose**: Cleanup, final logging, state persistence

**Requires Matcher**: No

**Input Fields**:
```json
{
  "session_id": "unique-session-identifier",
  "transcript_path": "/path/to/transcript",
  "cwd": "/current/working/directory",
  "permission_mode": "auto|manual"
}
```

**Output**:
- **Exit code 0**: Successful cleanup
- **Other exit codes**: Non-blocking error

**Use Cases**:
- Save session state
- Final logging
- Cleanup temporary files
- Generate session summaries
- Update metrics
- Archive artifacts

**Example**: Generate summary of files modified during session and save to history

## Stop

**Trigger**: Runs when Claude Code finishes responding (main agent)

**Purpose**: Decide whether execution should continue or stop

**Requires Matcher**: No

**Supports Prompt-Based Hooks**: Yes (query Haiku for intelligent continuation decision)

**Input Fields**:
```json
{
  "session_id": "unique-session-identifier",
  "transcript_path": "/path/to/transcript",
  "cwd": "/current/working/directory",
  "permission_mode": "auto|manual",
  "last_message": "Claude's last response message"
}
```

**Output**:
- **Exit code 0**: Allow normal flow
- **Exit code 2**: Force stop

**Optional JSON Output**:
```json
{
  "continue": true,
  "additionalContext": "Context to add if continuing"
}
```

**Command Hook**:
```json
{
  "type": "command",
  "command": "/path/to/script.sh"
}
```

**Prompt-Based Hook**:
```json
{
  "type": "prompt",
  "prompt": "Should execution continue? Return JSON with continue: true/false"
}
```

**Use Cases**:
- Auto-continue after specific operations
- Stop after error conditions
- Intelligent continuation based on context
- Enforce workflow steps
- Implement multi-step automation

**Example**: Continue automatically after running tests if they all pass

## SubagentStop

**Trigger**: Triggers when subagent tasks complete

**Purpose**: Control continuation after Task tool completions

**Requires Matcher**: No

**Supports Prompt-Based Hooks**: Yes

**Input Fields**:
```json
{
  "session_id": "unique-session-identifier",
  "transcript_path": "/path/to/transcript",
  "cwd": "/current/working/directory",
  "permission_mode": "auto|manual",
  "subagent_result": "The result returned by the subagent"
}
```

**Output**: Same as Stop hook

**Use Cases**:
- Validate subagent results
- Decide on next steps after exploration
- Chain subagent tasks
- Quality control on subagent output

**Example**: Continue only if subagent successfully found the target file

## Notification

**Trigger**: Activates during notification events (permission requests, waiting messages)

**Purpose**: Respond to or customize notifications

**Requires Matcher**: No

**Input Fields**:
```json
{
  "session_id": "unique-session-identifier",
  "transcript_path": "/path/to/transcript",
  "cwd": "/current/working/directory",
  "permission_mode": "auto|manual",
  "notification_type": "permission_request|waiting",
  "notification_message": "The notification message content"
}
```

**Output**:
- **Exit code 0**: Success
- **Other exit codes**: Non-blocking error

**Use Cases**:
- Desktop notifications
- Slack/Discord integration
- Custom logging
- Alert systems
- UI customization

**Example**: Send desktop notification when Claude requests permission

## PreCompact

**Trigger**: Runs before context compaction operations

**Purpose**: Prepare for or prevent compaction, save state

**Requires Matcher**: No

**Input Fields**:
```json
{
  "session_id": "unique-session-identifier",
  "transcript_path": "/path/to/transcript",
  "cwd": "/current/working/directory",
  "permission_mode": "auto|manual",
  "context_size": 123456,
  "compaction_reason": "Approaching context limit"
}
```

**Output**:
- **Exit code 0**: Allow compaction
- **Exit code 2**: Attempt to prevent compaction (not guaranteed)
- **Other exit codes**: Non-blocking error

**Use Cases**:
- Save important context before compaction
- Log compaction events
- Warn about context usage
- Archive conversation state

**Example**: Save current conversation context to file before compaction occurs

## Matcher Patterns

**Simple String**: Exact match
```json
"matcher": "Bash"
```

**Multiple Tools**: OR logic with pipe separator
```json
"matcher": "Write|Edit"
```

**Regex Pattern**: Complex matching
```json
"matcher": "mcp__.*__write.*"
```
Matches all write-related tools across all MCP servers

**MCP Tool Patterns**:
- Specific tool: `"mcp__memory__store"`
- All tools from server: `"mcp__memory__.*"`
- Tool type across servers: `"mcp__.*__search.*"`

## Parallel Execution

All matching hooks run in parallel with these characteristics:
- Default timeout: 60 seconds (configurable per hook)
- Identical commands are deduplicated
- Failures in one hook don't block others (except exit code 2 for PreToolUse)
- Output from all hooks is collected and processed

## Hook Snapshots

Security feature: Hooks are captured at session startup to prevent malicious mid-session modifications. Changes to hooks require Claude Code restart to take effect.
