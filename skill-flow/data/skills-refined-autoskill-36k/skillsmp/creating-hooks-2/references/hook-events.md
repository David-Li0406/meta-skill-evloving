---
title: Hook Events Reference
description: Comprehensive guide to all Claude Code hook event types with matchers and use cases
keywords: hooks, events, PreToolUse, PostToolUse, UserPromptSubmit, Stop, SessionStart, SubagentStop, SessionEnd, Notification, PreCompact
skill: creating-hooks
---

# Claude Code Hook Events Reference

This document provides detailed information about all available hook events in Claude Code.

## Hook Event Types

### PreToolUse

**When it runs:** After Claude creates tool parameters and before processing the tool call.

**Use cases:**
- Validate tool inputs before execution
- Auto-approve certain tool calls based on patterns
- Block dangerous operations
- Transform or sanitize tool parameters

**Common matchers:**
- `Task` - Subagent tasks
- `Bash` - Shell commands
- `Glob` - File pattern matching
- `Grep` - Content search
- `Read` - File reading
- `Edit` - File editing
- `Write` - File writing
- `WebFetch`, `WebSearch` - Web operations
- `mcp__*` - MCP tool patterns

**Key features:**
- Can block tool execution with exit code 2
- Can auto-approve with JSON output (`permissionDecision: "allow"`)
- Can force user confirmation (`permissionDecision: "ask"`)
- Receives tool name and input parameters

### PostToolUse

**When it runs:** Immediately after a tool completes successfully.

**Use cases:**
- Run formatters after file edits
- Execute tests after code changes
- Validate outputs
- Generate notifications
- Log tool usage

**Matchers:** Same as PreToolUse

**Key features:**
- Can provide feedback to Claude with `decision: "block"`
- Can add additional context for Claude to consider
- Receives both tool input and tool response
- Tool has already executed (cannot prevent execution)

### UserPromptSubmit

**When it runs:** When the user submits a prompt, before Claude processes it.

**Use cases:**
- Add contextual information (current time, git status, etc.)
- Validate prompts for sensitive information
- Block certain types of prompts
- Transform or augment user input

**Matchers:** None (no matcher field needed)

**Key features:**
- Can inject context that Claude sees (via stdout or JSON)
- Can block prompts with `decision: "block"`
- Unique behavior: stdout with exit code 0 is added to context
- Prompt is erased if blocked

### Stop

**When it runs:** When the main Claude Code agent has finished responding (not triggered by user interrupt).

**Use cases:**
- Continue execution with additional tasks
- Verify completion criteria
- Generate summary reports
- Trigger follow-up actions

**Matchers:** None

**Key features:**
- Can prevent Claude from stopping with `decision: "block"`
- Must provide reason when blocking stoppage
- `stop_hook_active` flag prevents infinite loops
- Should check flag to avoid continuous execution

### SubagentStop

**When it runs:** When a Claude Code subagent (Task tool call) has finished responding.

**Use cases:**
- Validate subagent outputs
- Continue subagent execution
- Collect subagent metrics
- Chain subagent tasks

**Matchers:** None

**Key features:**
- Same blocking mechanism as Stop
- Separate from main agent Stop hooks
- `stop_hook_active` flag available

### SessionStart

**When it runs:** When Claude Code starts a new session or resumes an existing session.

**Use cases:**
- Load development context
- Inject recent git changes
- Add environment information
- Set up session state

**Matchers:**
- `startup` - Fresh session start
- `resume` - Resume from `--resume`, `--continue`, or `/resume`
- `clear` - After `/clear` command
- `compact` - After compact operation

**Key features:**
- Can inject context via `additionalContext`
- Multiple hooks' context is concatenated
- Runs before any user interaction
- Cannot block session start

### SessionEnd

**When it runs:** When a Claude Code session ends.

**Use cases:**
- Cleanup tasks
- Log session statistics
- Save session state
- Generate reports

**Reason field values:**
- `clear` - Session cleared with /clear
- `logout` - User logged out
- `prompt_input_exit` - Exit during prompt input
- `other` - Other exit reasons

**Matchers:** None

**Key features:**
- Cannot block session termination
- Useful for cleanup and logging only
- Runs at session teardown

### Notification

**When it runs:** When Claude Code sends notifications.

**Notification triggers:**
- Claude needs permission to use a tool
- Prompt input idle for 60+ seconds

**Use cases:**
- Send external notifications
- Log notification events
- Track tool permission requests

**Matchers:** None

**Key features:**
- Cannot block or modify behavior
- Output logged to debug only (with `--debug`)
- Primarily for observability

### PreCompact

**When it runs:** Before Claude Code runs a compact operation.

**Use cases:**
- Save pre-compact state
- Add context before compaction
- Validate compact conditions
- Log compact triggers

**Matchers:**
- `manual` - User invoked via `/compact`
- `auto` - Automatic due to full context window

**Key features:**
- Cannot block compact operation
- `custom_instructions` available for manual compacts
- Useful for state preservation

## Hook Event Selection Guide

**Choose PreToolUse when:**
- Need to prevent tool execution
- Want to validate inputs before action
- Need to auto-approve certain operations
- Must sanitize or transform parameters

**Choose PostToolUse when:**
- Need to react to tool completion
- Want to run formatters/linters
- Need to validate outputs
- Want to provide Claude with feedback

**Choose UserPromptSubmit when:**
- Need to add context for every prompt
- Want to validate user input
- Must block sensitive prompts
- Need to transform user requests

**Choose Stop/SubagentStop when:**
- Need to continue execution automatically
- Want to verify completion criteria
- Must run post-completion tasks
- Need to chain multiple operations

**Choose SessionStart when:**
- Need to load initial context
- Want to set up session environment
- Must inject startup information

**Choose SessionEnd when:**
- Need cleanup on exit
- Want to log session metrics
- Must save final state

**Choose Notification when:**
- Need external notifications
- Want to track permission requests
- Must log notification events

**Choose PreCompact when:**
- Need to preserve state before compact
- Want to log compact operations
- Must add pre-compact context
