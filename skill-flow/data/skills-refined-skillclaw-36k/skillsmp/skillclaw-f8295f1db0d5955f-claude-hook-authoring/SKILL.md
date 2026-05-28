---
name: claude-hook-authoring
description: Use this skill when creating hooks to automate workflows, validate operations, or respond to Claude Code events.
---

# Skill body

## Hook Types

Two hook execution types:

| Type | Best For | Example |
|------|----------|---------|
| **prompt** | Complex reasoning, context-aware validation | LLM evaluates if action is safe |
| **command** | Deterministic checks, external tools, performance | Bash script validates paths |

**Prompt hooks** (recommended for complex logic):

```json
{
  "type": "prompt",
  "prompt": "Evaluate if this file write is safe: $TOOL_INPUT. Check for sensitive paths, credentials, path traversal. Return 'allow' or 'deny' with reason.",
  "timeout": 30
}
```

**Command hooks** (for deterministic/fast checks):

```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
  "timeout": 10
}
```

## Hook Events

| Event | When | Can Block | Common Uses |
|-------|------|-----------|-------------|
| **PreToolUse** | Before tool executes | Yes | Validate commands, check paths, enforce policies |
| **PostToolUse** | After tool succeeds | No | Auto-format, run linters, update docs |
| **PostToolUseFailure** | After tool fails | No | Error logging, retry logic, notifications |
| **PermissionRequest** | Permission dialog shown | Yes | Auto-allow/deny based on rules |
| **UserPromptSubmit** | User submits prompt | No | Add context, log activity, augment prompts |
| **Notification** | Claude sends notification | No | External alerts, logging |
| **Stop** | Main agent finishes | No | Cleanup, completion notifications |
| **SubagentStart** | Subagent spawns | No | Track subagent usage |
| **SubagentStop** | Subagent finishes | No | Log results, trigger follow-ups |
| **PreCompact** | Before context compacts | No | Backup conversation, preserve context |
| **SessionStart** | Session starts/resumes | No | Load context, show status, init resources |
| **SessionEnd** | Session ends | No | Cleanup, save state, log metrics |

See [references/hook-types.md](references/hook-types.md) for detailed documentation of each event.