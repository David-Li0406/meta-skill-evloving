---
name: hook-creator
description: Creates Claude Code hooks from descriptions. Use when the user wants to create a hook, add automation, set up pre/post tool actions, auto-format code, block commands, or add notifications.
allowed-tools: WebSearch, WebFetch, Write, Read, Glob, Edit
---

# Hook Creator

Create well-structured Claude Code hooks from natural language descriptions.

## Purpose

Generate production-ready Claude Code hook configurations that follow best practices and integrate seamlessly into the user's workflow.

## Instructions

When the user describes a hook they want to create, follow these steps:

### Step 1: Understand the Request

Parse the user's description to identify:
- What event should trigger the hook (PreToolUse, PostToolUse, UserPromptSubmit, etc.)
- What tools/actions should be matched
- What the hook should do (block, format, notify, log, etc.)
- Whether it should be user-wide or project-specific

### Step 2: Research Best Practices

Use WebSearch to find:
- Latest Claude Code hooks documentation and examples
- Best practices for the specific hook type requested
- Shell command patterns for the desired functionality
- Security considerations for the hook's domain

Search query suggestions:
- "Claude Code hooks [hook-type] best practices"
- "Claude Code [functionality] hook example"

Summarize 2-3 key insights that should inform the hook design.

### Step 3: Select Hook Event

Choose the appropriate hook event:

| Event | When It Runs | Use Cases |
|-------|--------------|-----------|
| `PreToolUse` | Before tool execution | Block edits, validate commands, protect files |
| `PostToolUse` | After tool completes | Auto-format, run tests, lint, log actions |
| `UserPromptSubmit` | User submits prompt | Add context, validate input, suggest skills |
| `PermissionRequest` | Permission dialog shown | Auto-allow safe operations, audit requests |
| `Notification` | Notification sent | Custom alerts, sound notifications, desktop notifications |
| `Stop` | Agent finishes responding | Cleanup, summaries, continuation logic |
| `SubagentStop` | Subagent completes | Aggregate results, trigger follow-ups |
| `PreCompact` | Before compaction | Save context, export data |
| `SessionStart` | Session begins/resumes | Set up environment, load preferences |
| `SessionEnd` | Session terminates | Cleanup, save state, generate reports |

### Step 4: Design the Matcher

Configure what triggers the hook:

| Matcher Pattern | Matches |
|-----------------|---------|
| `"Bash"` | Only Bash tool |
| `"Edit\|Write"` | Edit OR Write tools |
| `"*"` | All tools |
| `""` | All events for that hook type |

### Step 5: Write the Hook Command

Design the shell command following these patterns:

**Reading tool input (via stdin JSON):**
```bash
jq -r '.tool_input.file_path'
```

**Available environment variables:**
- `$CLAUDE_PROJECT_DIR` - Project root directory
- Standard shell environment

**Exit codes:**
- `0` = Success (allow action)
- `2` = Block action (PreToolUse only)
- Other = Non-blocking error

**Response JSON fields (output to stdout):**
```json
{
  "block": true,
  "message": "User-facing explanation",
  "feedback": "Non-blocking notification",
  "suppressOutput": true,
  "continue": false
}
```

### Step 6: Create the Configuration

Generate the hook JSON structure:

```json
{
  "hooks": {
    "[HookEvent]": [
      {
        "matcher": "[pattern]",
        "hooks": [
          {
            "type": "command",
            "command": "[shell-command]",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Step 7: Validate with Checklist

Before presenting, verify ALL items:

**Configuration**
- [ ] Correct hook event selected for the use case
- [ ] Matcher pattern is specific enough (avoid `*` unless needed)
- [ ] Timeout is set (default 5 seconds, increase for slow operations)
- [ ] Command handles JSON input correctly (uses jq or proper parsing)

**Security**
- [ ] No hardcoded credentials or secrets
- [ ] Input is validated/sanitized
- [ ] File paths are quoted properly
- [ ] No command injection vulnerabilities

**Robustness**
- [ ] Command handles missing/null fields gracefully
- [ ] Exit codes are correct (0 for success, 2 for blocking)
- [ ] Error messages are helpful to the user

**Integration**
- [ ] Works with user's existing tools (prettier, eslint, etc.)
- [ ] Doesn't conflict with other hooks
- [ ] Storage location is appropriate (user vs project settings)

### Step 8: Present and Save

1. Show the complete hook configuration
2. Explain what the hook does and when it triggers
3. Display the completed checklist
4. Ask where to save:
   - User settings: `~/.claude/settings.json` (applies to all projects)
   - Project settings: `.claude/settings.json` (project-specific)
5. Use Read tool to check existing settings.json
6. Use Edit tool to merge the hook into existing configuration, or Write if creating new

## Output Format

Present hooks in this format:

```
## Hook: [Descriptive Name]

**Event:** [HookEvent]
**Matcher:** [pattern]
**Purpose:** [One sentence description]

### Configuration

[JSON code block]

### How It Works

[Step-by-step explanation]

### Checklist

[Completed validation checklist]
```

## Best Practices

- Keep hooks simple and focused on one task
- Use `jq` for reliable JSON parsing
- Set appropriate timeouts to prevent hanging
- Test commands in terminal before adding to hooks
- Use project settings for team-shared hooks, user settings for personal preferences
- Document complex hooks with inline comments
- Prefer exit codes over JSON responses for simple pass/fail logic

## Common Hook Patterns

### Auto-format on file save
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | xargs -I {} sh -c 'npx prettier --write \"{}\" 2>/dev/null || true'"
      }]
    }]
  }
}
```

### Block edits on protected branch
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "branch=$(git branch --show-current 2>/dev/null); if [ \"$branch\" = \"main\" ] || [ \"$branch\" = \"master\" ]; then echo '{\"block\":true,\"message\":\"Cannot edit files on protected branch\"}'; exit 2; fi"
      }]
    }]
  }
}
```

### Log all bash commands
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
      }]
    }]
  }
}
```

## Example

**User:** "Create a hook that runs ESLint on any JavaScript file after Claude edits it"

**Result:** Researches ESLint integration best practices, creates a PostToolUse hook matching Edit|Write tools, filters for .js/.jsx files, runs eslint --fix, validates configuration, and saves to project settings.
