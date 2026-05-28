# Hooks Reference

Detailed guide for creating event-driven automation.

> **📘 New to hooks?** Start with [COMPONENTS.md](COMPONENTS.md#hook-templates) for complete templates with examples.
>
> **This file provides:** All hook event types, event-specific patterns, side effects documentation, and best practices.

## Quick Links

- [File Format](#file-format)
- [Available Hook Events](#available-hook-events)
- [Hook Types](#hook-types)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

## File Format

`hooks/event-type/hook-name.md`

## Available Hook Events

| Event | Directory | When it Triggers | Use For |
|-------|-----------|------------------|---------|
| PreToolUse | `pre-tool-use/` | Before tool execution | Validation, safety checks, blocking |
| PostToolUse | `post-tool-use/` | After tool completes | Logging, cleanup, follow-up |
| Stop | `stop/` | When agent/session stops | Cleanup, final reports |
| SubagentStop | `subagent-stop/` | When subagent completes | Result processing |
| SessionStart | `session-start/` | When session begins | Initialization, welcome |
| SessionEnd | `session-end/` | When session ends | Cleanup, session summary |
| UserPromptSubmit | `user-prompt-submit/` | After user submits prompt | Input validation, preprocessing |
| PreCompact | `pre-compact/` | Before context compaction | Preserve important context |
| Notification | `notification/` | On system notifications | Alert handling |

## Template

```markdown
---
description: What this hook does (max 1024 chars)
---

# Hook Title

Instructions for what to do when this event occurs.

## Behavior

[What the hook should do]

## Conditions

[When to act - optional filtering]

## Side Effects

[Any side effects - optional]
```

## Hook Types

### 1. PreToolUse Hooks

**Directory:** `hooks/pre-tool-use/`

**When:** Before any tool execution

**Use for:** Validation, safety checks, blocking operations

**Can block execution:** Yes

```markdown
---
description: Prevent dangerous git operations like force push to main
---

# Git Safety Hook

Before executing a Bash tool that contains git commands:

1. Check if command includes "git push --force"
2. Check if target branch is main/master
3. If both true, block the operation and warn user

## Behavior

If tool is Bash and command matches dangerous pattern:
- Block the tool execution
- Show warning message
- Suggest safer alternative

## Conditions

Only check git commands, ignore other tools.
```

**Examples:**

- Prevent destructive operations (rm, git push --force)
- Validate file paths before Read/Write
- Check API keys before external calls
- Enforce code review requirements

### 2. PostToolUse Hooks

**Directory:** `hooks/post-tool-use/`

**When:** After tool completes

**Use for:** Logging, cleanup, non-blocking follow-up

**Can block execution:** No

```markdown
---
description: Log all file write operations for audit trail
---

# File Write Logger

After any Write tool execution:

1. Log the file path
2. Log the write action
3. Append to audit log

## Behavior

When Write tool completes:
- Extract file path from tool result
- Append to ${CLAUDE_PLUGIN_ROOT}/../audit.log
- Include timestamp and action summary
```

**Examples:**

- Log file operations
- Track API calls
- Update metrics
- Trigger notifications
- Post-processing

### 3. Stop Hooks

**Directory:** `hooks/stop/`

**When:** When agent or session stops

**Use for:** Cleanup, state saving, final reports

```markdown
---
description: Save session state on stop
---

# Session State Saver

When the session stops:

1. Collect session context
2. Save to state file
3. Prepare summary

## Behavior

On stop:
- Save working directory
- Save recent files
- Save task status
- Write to ${CLAUDE_PLUGIN_ROOT}/../session-state.json
```

**Examples:**

- Save session state
- Generate reports
- Clean up temporary files
- Send notifications
- Close connections

### 4. SubagentStop Hooks

**Directory:** `hooks/subagent-stop/`

**When:** When a subagent completes

**Use for:** Processing subagent results

```markdown
---
description: Process and summarize subagent results
---

# Subagent Result Processor

When a subagent stops:

1. Collect the subagent's output
2. Extract key results
3. Add to parent context

## Behavior

On subagent completion:
- Read the subagent's final message
- Extract actionable results
- Format for parent agent
- Add to conversation summary
```

**Examples:**

- Aggregate results from multiple subagents
- Extract key findings
- Format summaries
- Update parent context

### 5. SessionStart Hooks

**Directory:** `hooks/session-start/`

**When:** When session begins

**Use for:** Initialization, welcome messages

```markdown
---
description: Show welcome message and initialize environment
---

# Session Initializer

When session starts:

1. Load user preferences
2. Show welcome message
3. Check environment

## Behavior

On session start:
- Read ${CLAUDE_PLUGIN_ROOT}/../preferences.local.md
- Display personalized greeting
- Verify dependencies are installed
- Show available commands
```

**Examples:**

- Load user preferences
- Display welcome messages
- Check environment setup
- Load context from previous session

### 6. SessionEnd Hooks

**Directory:** `hooks/session-end/`

**When:** When session ends

**Use for:** Final cleanup, session summaries

```markdown
---
description: Generate session summary and cleanup
---

# Session Cleaner

When session ends:

1. Generate session summary
2. Clean up temporary files
3. Save statistics

## Behavior

On session end:
- Count commands used
- List files modified
- Generate summary report
- Clean temp files
- Save to ${CLAUDE_PLUGIN_ROOT}/../sessions/summary-{timestamp}.md
```

**Examples:**

- Generate session reports
- Clean temporary files
- Update statistics
- Save session history

### 7. UserPromptSubmit Hooks

**Directory:** `hooks/user-prompt-submit/`

**When:** After user submits prompt

**Use for:** Input validation, preprocessing

```markdown
---
description: Validate and preprocess user input
---

# Input Validator

When user submits a prompt:

1. Check for sensitive information
2. Validate command format
3. Add context hints

## Behavior

On user prompt:
- Scan for API keys, passwords
- If found, warn user and suggest removal
- Check for command syntax
- Add helpful context if command detected
```

**Examples:**

- Sanitize input
- Detect sensitive data
- Pre-process commands
- Add helpful context
- Validate syntax

### 8. PreCompact Hooks

**Directory:** `hooks/pre-compact/`

**When:** Before context compaction

**Use for:** Preserving important context

```markdown
---
description: Preserve important context before compaction
---

# Context Preserver

Before context compaction:

1. Identify important messages
2. Mark for preservation
3. Create summary

## Behavior

On pre-compact:
- Find messages with key decisions
- Find messages with file operations
- Mark as important
- Create summary of key context
```

**Examples:**

- Preserve key decisions
- Keep file operation history
- Maintain conversation flow
- Create context summaries

### 9. Notification Hooks

**Directory:** `hooks/notification/`

**When:** On system notifications

**Use for:** Alert handling, status updates

```markdown
---
description: Handle and display system notifications
---

# Notification Handler

When notification arrives:

1. Parse notification type
2. Format for display
3. Take action if needed

## Behavior

On notification:
- Check notification type (error, warning, info)
- Format appropriately
- Display to user
- Trigger follow-up if critical
```

**Examples:**

- Display system alerts
- Handle error notifications
- Show status updates
- Trigger alerts on critical events

## Best Practices

### PreToolUse Hooks

- **Keep fast**: Don't slow down tool execution
- **Be specific**: Only block when necessary
- **Provide alternatives**: Suggest safer options
- **Clear messaging**: Explain why blocked

### PostToolUse Hooks

- **Non-blocking**: Should never fail the tool
- **Log efficiently**: Don't add too much overhead
- **Handle errors**: Hook failures shouldn't break workflow

### Stop/SessionEnd Hooks

- **Save state**: Preserve important context
- **Clean up**: Remove temporary files
- **Generate reports**: Create useful summaries

### All Hooks

- **Document side effects**: Clearly state what the hook does
- **Keep focused**: Single responsibility per hook
- **Test thoroughly**: Hooks can break workflows
- **Handle errors**: Gracefully degrade on errors

## Common Patterns

### Pattern 1: Validation Chain

```markdown
<!-- hooks/pre-tool-use/validate-input.md -->
---
description: Validate user input before execution
---

Check all user-provided input for:
- SQL injection patterns
- XSS vectors
- Path traversal

Block if unsafe patterns found.
```

### Pattern 2: Logging

```markdown
<!-- hooks/post-tool-use/log-operations.md -->
---
description: Log all operations to audit trail
---

After any tool:
- Log tool type
- Log target (file, command, etc.)
- Log result status
- Append to audit.log
```

### Pattern 3: Safety Net

```markdown
<!-- hooks/pre-tool-use/dangerous-operations.md -->
---
description: Block dangerous operations
---

Before executing:
- Check for destructive commands
- Verify user intent
- Block if confirmation needed
```

### Pattern 4: Context Manager

```markdown
<!-- hooks/pre-compact/preserve-context.md -->
---
description: Mark important context for preservation
---

Before compaction:
- Identify decision points
- Mark file operations
- Create summary
```

### Pattern 5: Automation Chain

```markdown
<!-- hooks/post-tool-use/trigger-followup.md -->
---
description: Trigger follow-up actions
---

After specific tools:
- Check result
- If success, trigger follow-up
- Continue workflow
```

## Validation Checklist

- [ ] Hook in correct event directory
- [ ] YAML frontmatter valid
- [ ] Description is clear
- [ ] Side effects documented
- [ ] Error handling included
- [ ] Tested with actual events
- [ ] Performance considered (fast execution)
- [ ] Doesn't break workflows

## Troubleshooting

### Hook Not Executing

1. Verify hook is in correct event directory
2. Check hook is listed in .plugin.json
3. Ensure file name matches manifest
4. Check YAML frontmatter is valid

### Hook Blocking Workflow

1. Review hook logic
2. Check error handling
3. Add logging to debug
4. Consider making it non-blocking

### Performance Issues

1. Profile hook execution time
2. Optimize expensive operations
3. Use caching where appropriate
4. Consider async processing
