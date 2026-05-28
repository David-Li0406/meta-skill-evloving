---
name: creating-hooks
description: Guide for creating Claude Code hooks that respond to events during execution. This skill should be used when users want to create or configure hooks for validation, automation, context injection, or workflow control. Triggers on "create a hook", "add a hook", "configure hooks", or "set up automation".
---

# Creating Claude Code Hooks

This skill guides the creation of Claude Code hooks that respond to events during Claude's execution, enabling automation, validation, context injection, and workflow customization.

## Table of Contents

- [What Are Claude Code Hooks?](#what-are-claude-code-hooks)
- [When to Use Hooks vs Skills/Commands](#when-to-use-hooks-vs-skillscommands)
- [Hook Creation Workflow](#hook-creation-workflow)
  - [Step 1: Determine Hook Location](#step-1-determine-hook-location)
  - [Step 2: Choose Hook Event Type](#step-2-choose-hook-event-type)
  - [Step 3: Design Hook Matcher](#step-3-design-hook-matcher-if-applicable)
  - [Step 4: Write Hook Script](#step-4-write-hook-script)
  - [Step 5: Configure Hook in Settings](#step-5-configure-hook-in-settings)
  - [Step 6: Make Script Executable](#step-6-make-script-executable)
  - [Step 7: Test the Hook](#step-7-test-the-hook)
- [Hook Best Practices](#hook-best-practices)
- [Common Hook Patterns](#common-hook-patterns)
- [Debugging Hooks](#debugging-hooks)
- [Resources](#resources)
- [Quick Reference](#quick-reference)

## What Are Claude Code Hooks?

Hooks are executable commands (typically scripts) that run in response to specific Claude Code events. They enable:

- **Validation**: Block or approve tool calls based on custom logic
- **Automation**: Run formatters, linters, or tests automatically
- **Context injection**: Add information to prompts or sessions
- **Workflow control**: Prevent Claude from stopping until criteria are met
- **Observability**: Log events, send notifications, track usage

## When to Use Hooks vs Skills/Commands

**Use hooks for:**
- Event-driven automation (run when specific events occur)
- Cross-cutting concerns (apply to all projects or all tool calls)
- Real-time validation and approval workflows
- Context injection that happens automatically

**Use skills for:**
- Complex workflows requiring specialized knowledge
- Capabilities that Claude discovers and uses proactively
- Bundled resources (scripts, references, assets)

**Use commands for:**
- Explicit, user-invoked workflows
- Quick tasks with manual triggers
- Repeatable operations with preflight checks

## Hook Creation Workflow

Follow this workflow to create hooks effectively.

### Step 1: Determine Hook Location

Determine whether this should be a project hook (shared with team) or personal hook (just for you).

If unclear, ask: "Should this be a project hook (shared with team) or personal hook (just for you)?"

**Project hooks** (`.claude/settings.json`):
- Shared via git with the team
- Project-specific automation (e.g., run project tests, format with project tools)
- Located in project's `.claude/` directory

**Personal hooks** (`~/.claude/settings.json`):
- Available across all projects for this user
- Personal preferences (e.g., notification style, personal validation rules)
- Located in user's home directory

**Default behavior if not specified:**
- If in a git repository with `.claude/` directory → Project hook
- Otherwise → Personal hook

### Step 2: Choose Hook Event Type

Based on the user's goal, select the appropriate hook event:

**Common Events:**
- **PreToolUse** - Validate/block tool calls before execution (matchers: tool names)
- **PostToolUse** - Run automation after tool completes (matchers: tool names)
- **UserPromptSubmit** - Inject context or validate prompts (no matcher)
- **Stop** - Verify completion before allowing Claude to stop (no matcher)
- **SessionStart** - Load context at session start (matchers: `startup`, `resume`, `clear`, `compact`)

**Additional Events:**
- **SubagentStop** - Control subagent completion (no matcher)
- **SessionEnd** - Cleanup on session end (no matcher)
- **Notification** - Observe notification events (no matcher)
- **PreCompact** - Save state before compaction (matchers: `manual`, `auto`)

**See `references/hook-events.md` for complete event details, use cases, and selection guidance.**

### Step 3: Design Hook Matcher (if applicable)

For PreToolUse and PostToolUse events, specify which tools trigger the hook:

**Exact match**: `"matcher": "Write"` - Only Write tool
**Multiple tools**: `"matcher": "Write|Edit"` - Write or Edit tools
**Pattern match**: `"matcher": "Notebook.*"` - All Notebook tools
**All tools**: `"matcher": "*"` or `"matcher": ""` - Every tool
**MCP tools**: `"matcher": "mcp__github__.*"` - All GitHub MCP tools

For SessionStart: Use `"matcher": "startup|resume"` for specific sources
For PreCompact: Use `"matcher": "manual"` or `"matcher": "auto"`

Other events don't use matchers - omit the matcher field entirely.

### Step 4: Write Hook Script

Create the hook script that implements the desired behavior.

**Script structure:**
1. Read JSON input from stdin
2. Implement validation/automation logic
3. Output results via stdout/stderr or JSON
4. Exit with appropriate code

**Exit codes:**
- `0` - Success (stdout shown in transcript, except UserPromptSubmit/SessionStart which adds to context)
- `2` - Blocking error (stderr fed to Claude automatically)
- Other - Non-blocking error (stderr shown to user, execution continues)

**Example script structure:**
```python
#!/usr/bin/env python3
import json
import sys

# Read input
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

# Get event-specific data
hook_event = input_data.get("hook_event_name", "")

# Implement logic based on event type
# ...

# Output results
# For simple cases: use stdout/stderr with exit codes
# For advanced control: output JSON

sys.exit(0)  # or 2 for blocking
```

**Advanced JSON output for fine-grained control:**
- PreToolUse: `permissionDecision` ("allow", "deny", "ask")
- PostToolUse: `decision: "block"` with reason, plus `additionalContext`
- UserPromptSubmit: `decision: "block"` or `additionalContext` for injection
- Stop/SubagentStop: `decision: "block"` to prevent stopping
- SessionStart: `additionalContext` for context injection

**See `references/hook-schemas.md` for complete input/output schemas and JSON examples.**
**See `references/examples.md` for 8 complete, working hook examples.**

### Step 5: Configure Hook in Settings

Add hook configuration to the appropriate settings.json file.

**Basic structure:**
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",  // Only for PreToolUse/PostToolUse/SessionStart/PreCompact
        "hooks": [
          {
            "type": "command",
            "command": "path/to/script.py",
            "timeout": 60  // Optional, defaults to 60 seconds
          }
        ]
      }
    ]
  }
}
```

**For project hooks**, use `$CLAUDE_PROJECT_DIR`:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format.py"
          }
        ]
      }
    ]
  }
}
```

**For personal hooks**, use absolute paths:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/inject_context.py"
          }
        ]
      }
    ]
  }
}
```

**Use the validation script to check configuration:**
```bash
# Personal skill installation:
python3 ~/.claude/skills/creating-hooks/scripts/validate_hook.py '<json>'

# Project skill installation:
python3 .claude/skills/creating-hooks/scripts/validate_hook.py '<json>'
```

**Use the helper script to add hooks safely:**
```bash
# Personal skill installation:
python3 ~/.claude/skills/creating-hooks/scripts/add_hook_to_settings.py \
  <settings_path> <event_name> '<config_json>'

# Project skill installation:
python3 .claude/skills/creating-hooks/scripts/add_hook_to_settings.py \
  <settings_path> <event_name> '<config_json>'
```

### Step 6: Make Script Executable

Ensure the hook script has execute permissions:

```bash
chmod +x /path/to/hook/script.py
```

For project hooks:
```bash
chmod +x .claude/hooks/script.py
```

For personal hooks:
```bash
chmod +x ~/.claude/hooks/script.py
```

### Step 7: Test the Hook

Test the hook before relying on it:

**1. Test script directly with sample input:**
```bash
echo '{"session_id":"test","hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"grep foo"}}' | python3 .claude/hooks/script.py
```

**2. Test in debug mode:**
```bash
claude --debug
# Trigger the hook in conversation
# Check debug output for execution details
```

**3. Verify registration:**
```bash
# In Claude Code session
/hooks
# Check that hook appears in list
```

## Hook Best Practices

**Performance:**
- Keep hooks fast (<1 second when possible)
- Use timeouts for external commands
- Optimize expensive operations

**Error Handling:**
- Always catch exceptions
- Handle missing dependencies gracefully
- Provide clear error messages

**Security:**
- Validate and sanitize all inputs
- Use absolute paths or `$CLAUDE_PROJECT_DIR`
- Quote shell variables: `"$VAR"` not `$VAR`
- Avoid sensitive files (.env, credentials, keys)

**Reliability:**
- Check `stop_hook_active` flag in Stop/SubagentStop hooks
- Make hooks idempotent (safe to run multiple times)
- Test with edge cases (empty inputs, missing files)

**Communication:**
- Use stderr for errors (visible to user)
- Use stdout for output/context
- Use JSON output for advanced control
- Exit codes: 0=success, 2=blocking, other=non-blocking error

## Common Hook Patterns

**Pattern 1: Validation with suggestions**
```python
# PreToolUse hook that validates and suggests alternatives
if problematic_pattern_found:
    print("Issue: ...\nSuggestion: ...", file=sys.stderr)
    sys.exit(2)  # Block with feedback to Claude
```

**Pattern 2: Auto-approval**
```python
# PreToolUse hook that bypasses permissions for safe operations
if safe_operation:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Safe operation auto-approved"
        },
        "suppressOutput": True
    }
    print(json.dumps(output))
```

**Pattern 3: Context injection**
```python
# UserPromptSubmit or SessionStart hook that adds context
context_info = get_relevant_context()
print(context_info)  # Added to context automatically
sys.exit(0)
```

**Pattern 4: Post-execution automation**
```python
# PostToolUse hook that runs formatters
if file_was_modified:
    run_formatter(file_path)
    print(f"Formatted {file_path}")
```

**Pattern 5: Completion verification**
```python
# Stop hook that ensures tests pass
if input_data.get("stop_hook_active"):
    sys.exit(0)  # Prevent infinite loops

if not tests_passing():
    output = {
        "decision": "block",
        "reason": "Tests failing. Please fix:\n" + test_output
    }
    print(json.dumps(output))
```

## Debugging Hooks

**Common issues:**

1. **Hook not executing**
   - Check `/hooks` to verify registration
   - Verify script is executable (`chmod +x`)
   - Check matcher pattern (case-sensitive)
   - Validate settings.json syntax

2. **Hook timing out**
   - Default timeout: 60 seconds
   - Increase: `"timeout": 120` in config
   - Optimize script performance
   - Add timeout to subprocess calls

3. **Wrong output behavior**
   - Review exit codes (0=success, 2=blocking)
   - Check stdout vs stderr usage
   - Verify JSON structure matches schemas
   - Test script with sample input

4. **Infinite loops**
   - Check `stop_hook_active` flag in Stop hooks
   - Ensure Stop hooks eventually allow stopping
   - Use debug mode to trace execution

**Debug with `--debug` flag:**
```bash
claude --debug
# Shows detailed hook execution:
# - Which hooks match
# - Commands executed
# - Exit codes and output
# - Timing information
```

## Resources

### scripts/

**validate_hook.py** - Validates hook configuration JSON structure before adding to settings. Checks event names, matcher patterns, and configuration format.

**add_hook_to_settings.py** - Safely adds hook configuration to settings.json files. Handles JSON formatting, creates necessary directories, and preserves existing settings.

Usage:
```bash
# Validate configuration (adjust path based on skill installation location)
python3 ~/.claude/skills/creating-hooks/scripts/validate_hook.py '<json>'  # Personal
python3 .claude/skills/creating-hooks/scripts/validate_hook.py '<json>'    # Project

# Add to settings (adjust path based on skill installation location)
python3 ~/.claude/skills/creating-hooks/scripts/add_hook_to_settings.py <settings_path> <event_name> '<config_json>'  # Personal
python3 .claude/skills/creating-hooks/scripts/add_hook_to_settings.py <settings_path> <event_name> '<config_json>'    # Project
```

### references/

**hook-events.md** - Comprehensive reference for all hook events including when they run, use cases, matchers, and selection guidance.

**hook-schemas.md** - Complete JSON schemas for hook inputs and outputs, including event-specific fields, tool-specific examples, and output visibility.

**examples.md** - Eight complete working examples demonstrating different hook types:
1. PreToolUse: Bash command validation
2. PostToolUse: Auto-format after file edits
3. UserPromptSubmit: Inject git context
4. PreToolUse: Auto-approve documentation reads
5. SessionStart: Load recent changes
6. Stop: Verify test passage
7. PostToolUse: Block sensitive file writes
8. UserPromptSubmit: Block prompts with secrets

## Quick Reference

**Hook events that can block execution:**
- PreToolUse (exit 2 or `permissionDecision: "deny"`)
- PostToolUse (exit 2 or `decision: "block"`)
- UserPromptSubmit (exit 2 or `decision: "block"`)
- Stop (`decision: "block"`)
- SubagentStop (`decision: "block"`)

**Hook events that inject context:**
- UserPromptSubmit (stdout with exit 0, or `additionalContext`)
- SessionStart (stdout with exit 0, or `additionalContext`)
- PostToolUse (`additionalContext`)

**Hook events that only observe:**
- SessionEnd (cannot block termination)
- Notification (logged to debug only)
- PreCompact (cannot block compaction)

**Environment variables available:**
- `$CLAUDE_PROJECT_DIR` - Project root directory (available in all hooks, expands to absolute path)
- `${CLAUDE_PLUGIN_ROOT}` - Plugin directory (plugin hooks only)
