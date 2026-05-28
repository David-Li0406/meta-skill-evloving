# Hook Configuration Guide

Comprehensive guide to structuring hook configurations in Claude Code settings files.

## Configuration File Locations

**Priority Order** (later files override earlier):
1. User settings: `~/.claude/settings.json` (applies to all sessions)
2. Project settings: `.claude/settings.json` (committed to git, team-shared)
3. Local settings: `.claude/settings.local.json` (gitignored, personal overrides)

**Best Practices**:
- Team-shared hooks → `.claude/settings.json` (commit to git)
- Personal hooks → `~/.claude/settings.local.json` (add to .gitignore)
- Global hooks → `~/.claude/settings.json`

## Basic Configuration Structure

```json
{
  "hooks": {
    "HookEventName": [
      {
        "matcher": "ToolName",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script",
            "timeout": 60000
          }
        ]
      }
    ]
  }
}
```

## Hook Event Configuration

### Tool-Based Events (PreToolUse, PostToolUse)

Require `matcher` field to specify which tools trigger the hook:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/pre-write.sh"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/pre-bash.sh"
          }
        ]
      }
    ]
  }
}
```

### Lifecycle Events (SessionStart, SessionEnd)

No matcher needed:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-end.sh"
          }
        ]
      }
    ]
  }
}
```

### Agent Events (Stop, SubagentStop)

Support both command and prompt-based hooks:

**Command Hook**:
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/should-continue.sh"
          }
        ]
      }
    ]
  }
}
```

**Prompt-Based Hook** (uses Haiku for intelligent decisions):
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Analyze the last message. Should execution continue? Consider: were there errors? Is the task complete? Return JSON with 'continue': true/false and 'reasoning': string."
          }
        ]
      }
    ]
  }
}
```

### Context Events

**UserPromptSubmit**:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/inject-context.sh"
          }
        ]
      }
    ]
  }
}
```

**Notification**:
```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/notify.sh"
          }
        ]
      }
    ]
  }
}
```

**PreCompact**:
```json
{
  "hooks": {
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/pre-compact.sh"
          }
        ]
      }
    ]
  }
}
```

## Matcher Patterns

### Simple String Matcher

Match exactly one tool:
```json
"matcher": "Write"
```

Tools available: `Task`, `Bash`, `Glob`, `Grep`, `Read`, `Edit`, `Write`, `WebFetch`, `WebSearch`

### Multiple Tools Matcher

Match any of several tools using pipe (OR):
```json
"matcher": "Write|Edit"
```

Triggers on either Write or Edit tool usage.

### Regex Matcher

Use regex patterns for complex matching:
```json
"matcher": "Write|Edit|mcp__.*__write.*"
```

This matches:
- Write tool
- Edit tool
- Any MCP tool containing "write" from any server

### MCP Tool Matchers

Model Context Protocol (MCP) tools use special naming in hooks.

**MCP Tool Naming Pattern**:

MCP tools follow the format: `mcp__<server>__<tool>`

Examples:
- `mcp__memory__create_entities` - Memory server tool
- `mcp__filesystem__read_file` - Filesystem server tool
- `mcp__github__search_repositories` - GitHub server tool

**Matching Patterns**:

**Specific MCP Tool**:
```json
"matcher": "mcp__memory__store"
```
Matches only the `store` tool from `memory` MCP server.

**All Tools from MCP Server**:
```json
"matcher": "mcp__memory__.*"
```
Matches all tools from the `memory` MCP server.

**Tool Type Across All MCP Servers**:
```json
"matcher": "mcp__.*__search.*"
```
Matches any tool containing "search" from any MCP server.

**Target All Write Operations**:
```json
"matcher": "mcp__.*__write.*"
```
Matches any write operation across all MCP servers.

**Combined Pattern**:
```json
"matcher": "Read|Write|mcp__.*__read.*|mcp__.*__write.*"
```
Matches:
- Built-in Read tool
- Built-in Write tool
- Any MCP read tool
- Any MCP write tool

**Complete MCP Hook Example**:

Validate all write operations across all MCP servers:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

This hook validates all write operations from any MCP server before execution.

## Hook Types

### Command Hook

Execute a shell script or command:

```json
{
  "type": "command",
  "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script.sh",
  "timeout": 60000
}
```

**Fields**:
- `type`: Always `"command"`
- `command`: Path to executable script (use environment variables for portability)
- `timeout`: Optional, milliseconds (default: 60000)

**Path Best Practices**:
- Use `$CLAUDE_PROJECT_DIR` for project-relative paths
- Use `${CLAUDE_PLUGIN_ROOT}` for plugin paths
- Use absolute paths with caution
- Forward slashes for cross-platform compatibility

### Prompt-Based Hook

Query LLM (Haiku) for intelligent decisions:

```json
{
  "type": "prompt",
  "prompt": "Your prompt here asking for a decision"
}
```

**Supported Events**: Currently only `Stop` and `SubagentStop`

**Prompt Design**:
- Request specific output format (JSON recommended)
- Provide decision criteria
- Ask for reasoning
- Keep concise (uses Haiku for cost/speed)

**Example**:
```json
{
  "type": "prompt",
  "prompt": "Review the last response. Should we continue? Criteria: (1) No errors occurred, (2) Task is not complete, (3) User expects continuation. Return JSON: {\"continue\": boolean, \"reasoning\": string}"
}
```

## Multiple Hooks per Event

You can have multiple matchers and multiple hooks per matcher:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/audit-write.py"
          },
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format-code.sh"
          }
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/audit-edit.py"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/log-commands.py"
          }
        ]
      }
    ]
  }
}
```

**Execution**: All matching hooks run in parallel.

## Timeout Configuration

Control how long hooks can run:

```json
{
  "type": "command",
  "command": "/path/to/slow-script.sh",
  "timeout": 120000
}
```

**Units**: Milliseconds
**Default**: 60000 (60 seconds)
**Maximum**: Typically limited by Claude Code (check documentation)

**Guidelines**:
- Fast validation: 5000-10000ms (5-10s)
- Normal operations: 30000-60000ms (30-60s)
- Slow operations: 90000-120000ms (90-120s)
- Avoid: >120000ms (consider async alternatives)

## Environment Variables in Configuration

Use environment variables for portable paths:

**Available Variables**:
- `$CLAUDE_PROJECT_DIR`: Project root directory
- `${CLAUDE_PLUGIN_ROOT}`: Plugin directory
- `$HOME`: User home directory (use `~/.claude/` instead)

**Examples**:
```json
{
  "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script.sh"
}
```

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/plugin-hook.sh"
}
```

**Best Practice**: Always use `$CLAUDE_PROJECT_DIR` for project hooks to ensure they work regardless of project location.

## Complete Configuration Example

Real-world example with multiple hooks:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/pre-write.sh",
            "timeout": 10000
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/pre-bash.sh",
            "timeout": 10000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/report-tracker.py",
            "timeout": 15000
          },
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format-code.sh",
            "timeout": 30000
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script-usage-logger.py",
            "timeout": 10000
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review the last message. If there were errors or the task is incomplete, return {\"continue\": true}. Otherwise return {\"continue\": false}."
          }
        ]
      }
    ]
  }
}
```

## Configuration Validation

Before deploying, validate:

**JSON Syntax**:
- [ ] Valid JSON (no trailing commas, proper quotes)
- [ ] Proper nesting and brackets
- [ ] No syntax errors

**Structure**:
- [ ] `hooks` top-level object exists
- [ ] Event names correctly spelled
- [ ] Tool-based events have `matcher` fields
- [ ] All hooks arrays contain valid hook objects

**Hook Objects**:
- [ ] `type` field present (`command` or `prompt`)
- [ ] `command` field present for command hooks
- [ ] `prompt` field present for prompt hooks
- [ ] `timeout` is number if present

**Paths**:
- [ ] Scripts exist at specified paths
- [ ] Scripts have execute permissions
- [ ] Paths use forward slashes
- [ ] Environment variables used appropriately

**Matchers**:
- [ ] Tool names valid
- [ ] Regex patterns syntactically correct
- [ ] MCP patterns follow naming convention

## Debugging Configuration

**Test JSON validity**:
```bash
python -m json.tool .claude/settings.json
```

**Check hook registration**:
```
/hooks
```
In Claude Code to list all registered hooks.

**Enable debug mode**:
```bash
claude --debug
```
Shows detailed hook execution information.

## Configuration Tips

1. **Start Simple**: Add one hook at a time and test
2. **Use Local Settings**: Test in `.claude/settings.local.json` before committing
3. **Version Control**: Commit `.claude/settings.json` but gitignore `.claude/settings.local.json`
4. **Document Hooks**: Add comments in adjacent README or CLAUDE.md file
5. **Team Communication**: Notify team when adding project hooks
6. **Regular Review**: Periodically review hooks for obsolete configurations
7. **Monitor Performance**: Watch for slow hooks that impact workflow
8. **Security First**: Always validate hook scripts before deployment
