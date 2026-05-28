# Hook Event Types Reference

Complete reference for all 9 Claude Code hook events.

**Configuration Format:** All JSON examples use the official Claude Code hooks format. For the complete schema and requirements, see [Commands Reference - Configuration Format](./commands.md#configuration-format).

**Note:** Some examples below (UserPromptSubmit through Notification sections) may show a simplified flat format for readability. The actual `hooks.json` configuration must use the nested format with `hooks.EventName[].matcher.hooks[]` structure. See PreToolUse and PostToolUse sections for correct examples.

## Event Overview

| Event | Timing | Can Block? (Exit 2) | Common Use Cases |
|-------|--------|---------------------|------------------|
| [PreToolUse](#pretooluse) | Before tool execution | ✅ Yes (blocks tool) | Validation, access control, pre-checks |
| [PostToolUse](#posttooluse) | After tool completes | ⚠️ Partial (stderr to Claude) | Formatting, testing, logging |
| [UserPromptSubmit](#userpromptsubmit) | Before AI processes prompt | ✅ Yes (erases prompt) | Input validation, preprocessing |
| [SessionStart](#sessionstart) | Session begins/resumes | ❌ No | Environment setup, context loading |
| [SessionEnd](#sessionend) | Session terminates | ❌ No | Cleanup, reporting, archival |
| [Stop](#stop) | Claude finishes responding | ✅ Yes (blocks stoppage) | Notifications, state capture |
| [SubagentStop](#subagentstop) | Subagent completes | ✅ Yes (blocks stoppage) | Subagent result validation |
| [PreCompact](#precompact) | Before memory compaction | ✅ Yes (blocks compaction) | Save critical context |
| [Notification](#notification) | Claude sends notification | ❌ No | Custom alert routing |

**Exit Code Behavior:**
- **Exit 0**: Success; stdout shown in transcript mode (except UserPromptSubmit/SessionStart add context)
- **Exit 2**: Blocking error; stderr fed to Claude for processing or shown to user
- **Other codes**: Non-blocking error; stderr shown to user, execution continues

---

## PreToolUse

**Timing**: Before tool execution
**Can Block**: ✅ Yes (exit code 2)
**Runs Synchronously**: Yes

### Purpose

Intercept tool calls before execution. Can validate, modify context, log, or block operations.

### Use Cases

- **Validation**: Check if operation is safe
- **Access Control**: Block unauthorized file access
- **Logging**: Track commands before execution
- **Pre-checks**: Verify prerequisites exist
- **Security**: Prevent dangerous operations

### Tool Input Available

```json
{
  "tool_input": {
    "command": "git push --force",      // Bash commands
    "file_path": "src/app.ts",          // Edit/Write operations
    "description": "Force push changes", // Optional description
    ...                                  // Tool-specific fields
  }
}
```

### Blocking Operations

Exit with code 2 to block:

```python
if dangerous_operation():
    print("ERROR: Operation blocked", file=sys.stderr)
    sys.exit(2)  # Blocks the operation
```

Exit with code 0 to allow:

```python
print("Operation validated")
sys.exit(0)  # Allows the operation
```

### Examples

**Block dangerous git operations**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/git-safety.py"
          }
        ]
      }
    ]
  }
}
```

**Protect sensitive files**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/file-protection.py"
          }
        ]
      }
    ]
  }
}
```

**Enforce workflow context** (PRISM example):
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/enforce-story-context.py"
          }
        ]
      }
    ]
  }
}
```

### Best Practices

✅ **DO**:
- Keep validation logic fast (<100ms)
- Provide clear error messages
- Log blocked operations for audit
- Use specific matchers when possible

❌ **DON'T**:
- Block operations unnecessarily
- Perform slow network calls
- Modify files during validation
- Create infinite loops

---

## PostToolUse

**Timing**: After tool execution completes
**Can Block**: ❌ No
**Runs Synchronously**: Yes

### Purpose

React to completed tool operations. Process results, run additional tools, or trigger workflows.

### Use Cases

- **Formatting**: Auto-format code after edits
- **Testing**: Run tests on code changes
- **Logging**: Record completed operations
- **Cleanup**: Remove temporary files
- **Chaining**: Trigger dependent operations

### Tool Input Available

Same as PreToolUse, plus operation has completed successfully.

### Cannot Block

PostToolUse hooks cannot prevent operations (they already happened). Use PreToolUse for blocking.

### Examples

**Auto-format on save**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write ${file_path}"
          }
        ]
      }
    ]
  }
}
```

**Run tests**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm test -- ${file_path}"
          }
        ]
      }
    ]
  }
}
```

**Track workflow progress** (PRISM example):
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/track-story.py"
          }
        ]
      }
    ]
  }
}
```

### Best Practices

✅ **DO**:
- Handle errors gracefully
- Keep operations fast
- Log actions for debugging
- Use specific matchers

❌ **DON'T**:
- Assume tool succeeded (check context)
- Block Claude's next action
- Perform destructive operations without checks
- Ignore exit codes

---

## UserPromptSubmit

**Timing**: When user submits prompt, before AI processes it
**Can Block**: ✅ Yes (exit code 2)
**Runs Synchronously**: Yes

### Purpose

Intercept and validate user prompts before Claude processes them.

### Use Cases

- **Security**: Check for sensitive data in prompts
- **Validation**: Ensure required context is present
- **Preprocessing**: Add context to prompts
- **Logging**: Track user requests
- **Rate Limiting**: Control API usage

### Tool Input Available

```json
{
  "prompt": "User's prompt text",
  "context": "Additional context information"
}
```

### Blocking Prompts

```python
if contains_sensitive_data(prompt):
    print("ERROR: Prompt contains sensitive data", file=sys.stderr)
    sys.exit(2)  # Blocks prompt processing
```

### Examples

**Check for secrets**:
```json
{
  "event": "UserPromptSubmit",
  "matcher": "*",
  "command": "python hooks/check-secrets.py"
}
```

**Add project context**:
```json
{
  "event": "UserPromptSubmit",
  "matcher": "*",
  "command": "python hooks/add-context.py"
}
```

### Best Practices

✅ **DO**:
- Validate quickly (<50ms)
- Provide helpful error messages
- Log blocked prompts
- Check for obvious issues only

❌ **DON'T**:
- Modify prompt content
- Perform slow operations
- Block legitimate prompts
- Access external APIs

---

## SessionStart

**Timing**: When Claude Code session starts or resumes
**Can Block**: ❌ No
**Runs Synchronously**: Yes

### Purpose

Initialize environment, load context, or restore state when session begins.

### Use Cases

- **Environment Setup**: Load configuration
- **Context Loading**: Restore workflow state
- **Logging**: Mark session start
- **Initialization**: Prepare resources
- **Validation**: Check prerequisites

### Tool Input Available

```json
{
  "session_id": "unique-session-identifier",
  "resumed": true  // or false for new session
}
```

### Examples

**Load workflow context**:
```json
{
  "event": "SessionStart",
  "matcher": "*",
  "command": "python hooks/session-start.py"
}
```

**Check prerequisites**:
```json
{
  "event": "SessionStart",
  "matcher": "*",
  "command": "bash hooks/check-env.sh"
}
```

### Best Practices

✅ **DO**:
- Keep initialization fast
- Log session start
- Validate environment
- Restore saved state

❌ **DON'T**:
- Perform slow operations
- Block Claude startup
- Modify project files
- Require user interaction

---

## SessionEnd

**Timing**: When Claude Code session terminates
**Can Block**: ❌ No
**Runs Synchronously**: Yes

### Purpose

Clean up resources, save state, or generate reports when session ends.

### Use Cases

- **Cleanup**: Remove temporary files
- **State Saving**: Persist workflow state
- **Reporting**: Generate session summary
- **Logging**: Mark session end
- **Backup**: Save unsaved work

### Tool Input Available

```json
{
  "session_id": "unique-session-identifier",
  "duration": 3600  // Session duration in seconds
}
```

### Examples

**Save workflow state**:
```json
{
  "event": "SessionEnd",
  "matcher": "*",
  "command": "python hooks/session-end.py"
}
```

**Generate report**:
```json
{
  "event": "SessionEnd",
  "matcher": "*",
  "command": "bash hooks/session-report.sh"
}
```

### Best Practices

✅ **DO**:
- Clean up resources
- Save state quickly
- Log session end
- Handle errors gracefully

❌ **DON'T**:
- Take too long (blocks shutdown)
- Modify project files
- Require user interaction
- Fail silently

---

## Stop

**Timing**: When Claude finishes responding
**Can Block**: ❌ No
**Runs Synchronously**: Yes

### Purpose

Trigger notifications or actions when Claude completes a response.

### Use Cases

- **Notifications**: Alert user of completion
- **State Capture**: Save current context
- **Logging**: Record response completion
- **Chaining**: Trigger follow-up actions
- **Monitoring**: Track response times

### Tool Input Available

```json
{
  "response_length": 1234,  // Characters in response
  "tools_used": ["Bash", "Edit", "Write"]
}
```

### Examples

**Desktop notification**:
```json
{
  "event": "Stop",
  "matcher": "*",
  "command": "notify-send 'Claude Code' 'Ready for input'"
}
```

**Play sound**:
```json
{
  "event": "Stop",
  "matcher": "*",
  "command": "afplay /System/Library/Sounds/Glass.aiff"
}
```

### Best Practices

✅ **DO**:
- Keep notifications brief
- Log completions
- Run async when possible
- Handle errors

❌ **DON'T**:
- Block next user action
- Show intrusive notifications
- Perform slow operations
- Require user interaction

---

## SubagentStop

**Timing**: When subagent task completes
**Can Block**: ❌ No
**Runs Synchronously**: Yes

### Purpose

React to subagent completion, validate results, or trigger follow-up actions.

### Use Cases

- **Validation**: Check subagent results
- **Logging**: Track subagent completion
- **Chaining**: Trigger dependent subagents
- **Reporting**: Summarize subagent work
- **Error Handling**: Detect subagent failures

### Tool Input Available

```json
{
  "subagent_id": "unique-subagent-id",
  "subagent_type": "code-reviewer",
  "status": "completed",
  "duration": 120
}
```

### Examples

**Log subagent completion**:
```json
{
  "event": "SubagentStop",
  "matcher": "*",
  "command": "python hooks/log-subagent.py"
}
```

**Validate results**:
```json
{
  "event": "SubagentStop",
  "matcher": "*",
  "command": "python hooks/validate-subagent.py"
}
```

### Best Practices

✅ **DO**:
- Log subagent results
- Validate outputs
- Handle failures
- Keep processing fast

❌ **DON'T**:
- Block main agent
- Modify subagent results
- Take too long
- Fail silently

---

## PreCompact

**Timing**: Before memory compaction
**Can Block**: ✅ Yes (exit code 2)
**Runs Synchronously**: Yes

### Purpose

Save critical context before Claude compacts memory to free space.

### Use Cases

- **Context Saving**: Preserve important information
- **State Backup**: Save workflow state
- **Logging**: Mark compaction events
- **Validation**: Check if safe to compact
- **Warning**: Alert about memory pressure

### Tool Input Available

```json
{
  "memory_usage": 80,  // Percentage
  "context_size": 150000  // Tokens
}
```

### Blocking Compaction

```python
if critical_context_unsaved():
    print("ERROR: Cannot compact - critical context", file=sys.stderr)
    sys.exit(2)  # Blocks compaction
```

### Examples

**Save workflow state**:
```json
{
  "event": "PreCompact",
  "matcher": "*",
  "command": "python hooks/save-context.py"
}
```

**Warn user**:
```json
{
  "event": "PreCompact",
  "matcher": "*",
  "command": "bash hooks/compact-warning.sh"
}
```

### Best Practices

✅ **DO**:
- Save quickly (<200ms)
- Log compaction events
- Preserve critical context
- Allow compaction usually

❌ **DON'T**:
- Block unnecessarily
- Perform slow operations
- Ignore memory pressure
- Fail to save state

---

## Notification

**Timing**: When Claude sends notification (needs permission, etc.)
**Can Block**: ❌ No
**Runs Synchronously**: Yes

### Purpose

Route or augment Claude's notifications to custom channels.

### Use Cases

- **Custom Routing**: Send to Slack/Teams/Email
- **Formatting**: Customize notification appearance
- **Logging**: Track all notifications
- **Filtering**: Suppress certain notifications
- **Enrichment**: Add additional context

### Tool Input Available

```json
{
  "notification_type": "permission_needed",
  "message": "Claude needs permission to proceed",
  "severity": "warning"
}
```

### Examples

**Send to Slack**:
```json
{
  "event": "Notification",
  "matcher": "*",
  "command": "python hooks/slack-notify.py"
}
```

**Custom desktop alert**:
```json
{
  "event": "Notification",
  "matcher": "*",
  "command": "bash hooks/custom-notify.sh"
}
```

### Best Practices

✅ **DO**:
- Route notifications appropriately
- Log all notifications
- Handle errors gracefully
- Keep processing fast

❌ **DON'T**:
- Block notification delivery
- Spam notification channels
- Ignore notification severity
- Fail silently

---

## Event Selection Guide

**Choose PreToolUse when**:
- Need to validate before action
- Want to block unsafe operations
- Require pre-checks or prerequisites

**Choose PostToolUse when**:
- Want to react to completed actions
- Need to run follow-up operations
- Want to format/test/cleanup after changes

**Choose UserPromptSubmit when**:
- Need to validate user input
- Want to preprocess prompts
- Require security checks on input

**Choose SessionStart when**:
- Need to initialize environment
- Want to load saved state
- Require setup on session start

**Choose SessionEnd when**:
- Need to cleanup resources
- Want to save state
- Require session reports

**Choose Stop when**:
- Want to notify on completion
- Need to capture final state
- Require completion logging

**Choose SubagentStop when**:
- Working with subagents
- Need to validate subagent results
- Want to chain subagent tasks

**Choose PreCompact when**:
- Need to save context
- Want to prevent compaction
- Require state preservation

**Choose Notification when**:
- Want custom notification routing
- Need to augment notifications
- Require notification logging

---

**Version**: 1.0.0
**Last Updated**: 2025-10-24
