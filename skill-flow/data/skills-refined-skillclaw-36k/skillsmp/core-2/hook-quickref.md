# Hook System Quick Reference

**Hook System Quick Reference**

Fast reference card for PAI hook system essentials.

---

## Hook Lifecycle

```
1. Event occurs (SessionStart, Stop, etc.)
2. Claude Code writes hook data to stdin
3. Hook script executes
4. Hook reads stdin (with timeout)
5. Hook performs actions (capture, logging, etc.)
6. Hook exits 0 (always succeeds)
7. Claude Code continues
```

---

## Key Files

```
${PAI_DIR}/settings.json           Hook configuration
${PAI_DIR}/hooks/                  Hook scripts
${PAI_DIR}/hooks/lib/observability.ts   Helper library
${PAI_DIR}/history/raw-outputs/    Event logs (JSONL)
${PAI_DIR}/history/sessions/       Work summaries
${PAI_DIR}/history/learnings/      Learning captures
${PAI_DIR}/agent-sessions.json     Session→Agent mapping
```

---

## Critical Hooks

```
stop-hook.ts          History capture (main agent)
subagent-stop-hook.ts History capture (subagents)
load-core-context.ts  PAI context loading
capture-all-events.ts Universal event logger
```

---

## Hook Events

| Event | When | Primary Use |
|-------|------|-------------|
| SessionStart | Session begins | Load context, initialize state |
| SessionEnd | Session terminates | Generate summaries, cleanup |
| UserPromptSubmit | User sends prompt | Update UI, capture prompts |
| Stop | Main agent completes | Capture work/learnings |
| SubagentStop | Subagent completes | Capture agent outputs |
| PreToolUse | Before tool execution | Analytics, validation |
| PostToolUse | After tool execution | Capture outputs, metrics |
| PreCompact | Before context compression | Preserve context |

---

## Configuration Template

```json
{
  "hooks": {
    "HookEventName": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "${PAI_DIR}/hooks/my-hook.ts"
          }
        ]
      }
    ]
  }
}
```

---

## Hook Script Template

```typescript
#!/usr/bin/env bun

interface HookInput {
  session_id: string;
  transcript_path: string;
  hook_event_name: string;
}

async function main() {
  try {
    const input = await Bun.stdin.text();
    const data: HookInput = JSON.parse(input);

    // Your hook logic here

  } catch (error) {
    console.error('Hook error:', error);
  }

  process.exit(0);  // Always exit 0
}

main();
```

---

## Essential Patterns

### 1. Fast Execution
```typescript
// Launch background work
Bun.spawn(['bun', 'slow-task.ts'], {
  stdout: 'ignore',
  stderr: 'ignore',
  stdin: 'ignore'
});
process.exit(0);  // Exit immediately
```

### 2. Graceful Failure
```typescript
try {
  // Hook logic
} catch (error) {
  console.error('Error:', error);
}
process.exit(0);  // Always succeed
```

### 3. Timeout Protection
```typescript
setTimeout(() => {
  console.error('Hook timeout');
  process.exit(0);
}, 5000);  // 5 second max
```

### 4. Stdin Reading with Timeout
```typescript
const timeoutPromise = new Promise<void>((resolve) => {
  setTimeout(() => resolve(), 500);
});
await Promise.race([readPromise, timeoutPromise]);
```

---

## File Naming Convention

```
YYYY-MM-DD-HHMMSS_TYPE_description.md
```

**Types:**
- `WORK` - General completions
- `LEARNING` - Problem-solving learnings
- `SESSION` - Session summaries
- `RESEARCH` - Research findings
- `FEATURE` - Feature implementations
- `DECISION` - Architectural decisions

---

## Structured Response Sections

```
📋 SUMMARY:    Brief overview
🔍 ANALYSIS:   Key findings
⚡ ACTIONS:    Steps taken
✅ RESULTS:    Outcomes
📊 STATUS:     Current state
➡️ NEXT:       Follow-up actions
🎯 COMPLETED:  Completion summary (REQUIRED)
```

---

## Debugging Commands

```bash
# Test hook directly
echo '{"session_id":"test","transcript_path":"/tmp/test.jsonl","hook_event_name":"Stop"}' | \
  bun ${PAI_DIR}/hooks/my-hook.ts

# Check if hook is executable
ls -la ${PAI_DIR}/hooks/my-hook.ts

# Validate settings.json
jq . ${PAI_DIR}/settings.json

# Check recent captures
ls -lt ${PAI_DIR}/history/sessions/$(date +%Y-%m)/ | head -5

# Check raw events
tail ${PAI_DIR}/history/raw-outputs/$(date +%Y-%m)/$(date +%Y-%m-%d)_all-events.jsonl

# Search for specific event type
grep '"event_type":"Stop"' ${PAI_DIR}/history/raw-outputs/$(date +%Y-%m)/$(date +%Y-%m-%d)_all-events.jsonl
```

---

## Observability

```
Server: http://localhost:4000
Client: http://localhost:5173
Events: All hooks send to /events endpoint
```

---

## Performance Targets

```
SessionStart:    < 100ms (critical path)
Stop/SubagentStop: < 500ms
Tool hooks:      < 50ms (high frequency)
SessionEnd:      < 2000ms (not critical)
```

---

## Common Issues Quick Fix

| Issue | Quick Fix |
|-------|-----------|
| Hook not running | `chmod +x hook.ts`, restart Claude Code |
| Hook hangs | Add timeout, ensure exit(0) |
| History not capturing | Check structured format, verify `🎯 COMPLETED:` line |
| Agent detection failing | Check `[AGENT:type]` tag, verify agent-sessions.json |
| Dashboard not receiving | Check server running: `curl localhost:4000/health` |

---

## Environment Variables

```typescript
process.env.PAI_DIR           // PAI installation directory
process.env.DA                // Digital Assistant name
process.env.CLAUDE_CODE_AGENT // Current agent type (if subagent)
```

---

## See Also
- [hook-system.md](hook-system.md) - Main hook guide and best practices
- [hook-reference.md](hook-reference.md) - Complete hook types reference
- [hook-troubleshooting.md](hook-troubleshooting.md) - Debugging guide

---

**Last Updated:** 2025-11-01
**Status:** Production Quick Reference
**Maintainer:** Jean-Marc Giorgi (maintainer@example.com)
