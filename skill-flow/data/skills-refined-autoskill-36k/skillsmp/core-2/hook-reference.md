# Hook Reference

**Complete reference for all Claude Code hook types**

This document provides detailed information about all available hook types in the PAI hook system, including when they fire, their use cases, current implementations, and data payloads.

---

## Available Hook Types

Claude Code supports the following hook events (from `${PAI_DIR}/hooks/lib/observability.ts`):

### 1. **SessionStart**
**When:** Claude Code session begins (new conversation)
**Use Cases:**
- Load PAI context from `skills/CORE/SKILL.md`
- Initialize session state
- Capture session metadata

**Current Hooks:**
```json
{
  "SessionStart": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/load-core-context.ts"
        },
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/initialize-pai-session.ts"
        },
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/capture-all-events.ts --event-type SessionStart"
        }
      ]
    }
  ]
}
```

**What They Do:**
- `load-core-context.ts` - Reads `skills/CORE/SKILL.md` and injects PAI context as `<system-reminder>` at session start
- `initialize-pai-session.ts` - Sets up session state and environment
- `capture-all-events.ts` - Logs event to `${PAI_DIR}/history/raw-outputs/YYYY-MM/YYYY-MM-DD_all-events.jsonl`

**Data Payload:**
```typescript
{
  session_id: string;
  transcript_path: string;
  hook_event_name: "SessionStart";
  cwd: string;
}
```

---

### 2. **SessionEnd**
**When:** Claude Code session terminates (conversation ends)
**Use Cases:**
- Generate session summaries
- Save session metadata
- Cleanup temporary state

**Current Hooks:**
```json
{
  "SessionEnd": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/capture-session-summary.ts"
        },
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/capture-all-events.ts --event-type SessionEnd"
        }
      ]
    }
  ]
}
```

**What They Do:**
- `capture-session-summary.ts` - Analyzes session activity and creates summary document in `${PAI_DIR}/history/sessions/YYYY-MM/`
- Captures: files changed, commands executed, tools used, session focus, duration

**Data Payload:**
```typescript
{
  conversation_id: string;  // Note: different field name
  timestamp: string;
}
```

---

### 3. **UserPromptSubmit**
**When:** User submits a new prompt to Claude
**Use Cases:**
- Update UI indicators
- Pre-process user input
- Capture prompts for analysis

**Current Hooks:**
```json
{
  "UserPromptSubmit": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/update-tab-titles.ts"
        },
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/capture-all-events.ts --event-type UserPromptSubmit"
        }
      ]
    }
  ]
}
```

**What They Do:**
- `update-tab-titles.ts` - Updates Kitty terminal tab title with task summary
- Launches background Haiku summarization for better tab titles
- Sets `♻️` emoji prefix to indicate processing

**Data Payload:**
```typescript
{
  session_id: string;
  transcript_path: string;
  hook_event_name: "UserPromptSubmit";
  prompt: string;  // The user's prompt text
}
```

---

### 4. **Stop**
**When:** Main agent (Qara) completes a response
**Use Cases:**
- Capture work summaries and learnings
- Update terminal tab with completion status
- Log completion events

**Current Hooks:**
```json
{
  "Stop": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/stop-hook.ts"
        },
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/capture-all-events.ts --event-type Stop"
        }
      ]
    }
  ]
}
```

**What They Do:**
- `stop-hook.ts` - THE CRITICAL HOOK for main agent completions
  - Extracts `🎯 COMPLETED:` line from response
  - Captures work summaries to `${PAI_DIR}/history/sessions/YYYY-MM/` or learnings to `${PAI_DIR}/history/learnings/YYYY-MM/`
  - Updates Kitty tab with `✅` prefix
  - Sends event to observability dashboard

**Learning Detection:** Automatically identifies learning moments (2+ indicators: problem/issue/bug, fixed/solved, troubleshoot/debug, lesson/takeaway)

**Data Payload:**
```typescript
{
  session_id: string;
  transcript_path: string;
  hook_event_name: "Stop";
}
```

---

### 5. **SubagentStop**
**When:** Subagent (Task tool) completes execution
**Use Cases:**
- Capture agent outputs
- Track multi-agent workflows
- Log subagent completions

**Current Hooks:**
```json
{
  "SubagentStop": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/subagent-stop-hook.ts"
        },
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/capture-all-events.ts --event-type SubagentStop"
        }
      ]
    }
  ]
}
```

**What They Do:**
- `subagent-stop-hook.ts` - Agent-specific completion handling
  - Waits for Task tool result in transcript
  - Extracts `[AGENT:type]` tag and completion message
  - Captures agent output to appropriate history category
  - Sends to observability dashboard

**Data Payload:**
```typescript
{
  session_id: string;
  transcript_path: string;
  hook_event_name: "SubagentStop";
}
```

---

### 6. **PreToolUse**
**When:** Before Claude executes any tool
**Use Cases:**
- Tool usage analytics
- Pre-execution validation
- Performance monitoring

**Current Hooks:**
```json
{
  "PreToolUse": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/capture-all-events.ts --event-type PreToolUse"
        }
      ]
    }
  ]
}
```

**What They Do:**
- Captures tool name, input parameters, timestamp
- Logs to daily events file for analysis

**Data Payload:**
```typescript
{
  session_id: string;
  transcript_path: string;
  hook_event_name: "PreToolUse";
  tool_name: string;
  tool_input: any;  // Tool parameters
}
```

---

### 7. **PostToolUse**
**When:** After Claude executes any tool
**Use Cases:**
- Capture tool outputs
- Error tracking
- Performance metrics

**Current Hooks:**
```json
{
  "PostToolUse": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/capture-all-events.ts --event-type PostToolUse"
        }
      ]
    }
  ]
}
```

**What They Do:**
- Captures tool output, execution time, success/failure
- Logs to `${PAI_DIR}/history/raw-outputs/YYYY-MM/YYYY-MM-DD_all-events.jsonl`
- Powers observability dashboard

**Data Payload:**
```typescript
{
  session_id: string;
  transcript_path: string;
  hook_event_name: "PostToolUse";
  tool_name: string;
  tool_input: any;
  tool_output: any;  // Tool result
  error?: string;    // If tool failed
}
```

---

### 8. **PreCompact**
**When:** Before Claude compacts context (long conversations)
**Use Cases:**
- Preserve important context
- Log compaction events
- Pre-compaction cleanup

**Current Hooks:**
```json
{
  "PreCompact": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/context-compression-hook.ts"
        },
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/capture-all-events.ts --event-type PreCompact"
        }
      ]
    }
  ]
}
```

**What They Do:**
- `context-compression-hook.ts` - Handles context preservation before compaction
- Captures metadata about compaction events

**Data Payload:**
```typescript
{
  session_id: string;
  transcript_path: string;
  hook_event_name: "PreCompact";
  cwd: string;
}
```

---

## Matcher Patterns

`"matcher"` field filters which events trigger hook:

```json
{
  "PostToolUse": [
    {
      "matcher": "Bash",  // Only Bash tool executions
      "hooks": [...]
    },
    {
      "matcher": "*",     // All tool executions
      "hooks": [...]
    }
  ]
}
```

**Patterns:**
- `"*"` - All events
- `"Bash"` - Specific tool name
- `""` - Empty (all events, same as `*`)

---

## Multi-Hook Execution Order

Hooks in same event execute **sequentially** in order defined in settings.json:

```json
{
  "Stop": [
    {
      "hooks": [
        { "command": "${PAI_DIR}/hooks/stop-hook.ts" },      // Runs first
        { "command": "${PAI_DIR}/hooks/capture-all-events.ts" }  // Runs second
      ]
    }
  ]
}
```

**Note:** If first hook hangs, second won't run. Keep hooks fast!

---

## See Also
- [hook-system.md](hook-system.md) - Main hook guide and best practices
- [hook-troubleshooting.md](hook-troubleshooting.md) - Debugging and advanced patterns
- [hook-quickref.md](hook-quickref.md) - Quick reference card

---

**Last Updated:** 2025-11-01
**Status:** Production - All hook types documented
**Maintainer:** Jean-Marc Giorgi (maintainer@example.com)
