# Hook System

**Event-Driven Automation Infrastructure**

**Location:** `${PAI_DIR}/hooks/`
**Configuration:** `${PAI_DIR}/settings.json`
**Status:** Active - All hooks running in production

---

## Overview

The PAI hook system is an event-driven automation infrastructure built on Claude Code's native hook support. Hooks are executable scripts (TypeScript/Python) that run automatically in response to specific events during Claude Code sessions.

**Core Capabilities:**
- **Session Management** - Auto-load context, capture summaries, manage state
- **History Capture** - Automatic work/learning documentation to `${PAI_DIR}/history/`
- **Multi-Agent Support** - Agent-specific hooks for task tracking
- **Observability** - Real-time event streaming to dashboard
- **Tab Titles** - Dynamic terminal tab updates with task context

**Key Principle:** Hooks run asynchronously and fail gracefully. They enhance the user experience but never block Claude Code's core functionality.

---

## Configuration

### Location
**File:** `${PAI_DIR}/settings.json`
**Section:** `"hooks": { ... }`

### Environment Variables
Hooks have access to all environment variables from `${PAI_DIR}/settings.json` `"env"` section:

```json
{
  "env": {
    "PAI_DIR": "/Users/daniel/.claude",
    "DA": "Qara",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "64000"
  }
}
```

**Key Variables:**
- `PAI_DIR` - PAI installation directory (always `/Users/daniel/.claude`)
- `DA` - Digital Assistant name ("Qara")
- Hook scripts reference `${PAI_DIR}` in command paths

### Hook Configuration Structure

```json
{
  "hooks": {
    "HookEventName": [
      {
        "matcher": "pattern",  // Optional: filter which tools/events trigger hook
        "hooks": [
          {
            "type": "command",
            "command": "${PAI_DIR}/hooks/my-hook.ts --arg value"
          }
        ]
      }
    ]
  }
}
```

**Fields:**
- `HookEventName` - One of: SessionStart, SessionEnd, UserPromptSubmit, Stop, SubagentStop, PreToolUse, PostToolUse, PreCompact
- `matcher` - Pattern to match (use `"*"` for all tools, or specific tool names)
- `type` - Always `"command"` (executes external script)
- `command` - Path to executable hook script (TypeScript/Python/Bash)

### Hook Input (stdin)
All hooks receive JSON data on stdin:

```typescript
{
  session_id: string;         // Unique session identifier
  transcript_path: string;    // Path to JSONL transcript
  hook_event_name: string;    // Event that triggered hook
  prompt?: string;            // User prompt (UserPromptSubmit only)
  tool_name?: string;         // Tool name (PreToolUse/PostToolUse)
  tool_input?: any;           // Tool parameters (PreToolUse)
  tool_output?: any;          // Tool result (PostToolUse)
  // ... event-specific fields
}
```

---

## Common Patterns

### 1. History Capture (UOCS Pattern)

**Pattern:** Parse structured response → Save to appropriate history directory

**File Naming Convention:**
```
YYYY-MM-DD-HHMMSS_TYPE_description.md
```

**Types:**
- `WORK` - General task completions
- `LEARNING` - Problem-solving learnings
- `SESSION` - Session summaries
- `RESEARCH` - Research findings (from agents)
- `FEATURE` - Feature implementations (from agents)
- `DECISION` - Architectural decisions (from agents)

**Example from stop-hook.ts:**
```typescript
const structured = extractStructuredSections(lastMessage);
const isLearning = isLearningCapture(text, structured);
const captureType = isLearning ? 'LEARNING' : 'WORK';

const targetDir = isLearning
  ? join(baseDir, 'history', 'learnings', yearMonth)
  : join(baseDir, 'history', 'sessions', yearMonth);

const filename = generateFilename(description, captureType);
writeFileSync(join(targetDir, filename), content);
```

**Structured Sections Parsed:**
- `📋 SUMMARY:` - Brief overview
- `🔍 ANALYSIS:` - Key findings
- `⚡ ACTIONS:` - Steps taken
- `✅ RESULTS:` - Outcomes
- `📊 STATUS:` - Current state
- `➡️ NEXT:` - Follow-up actions
- `🎯 COMPLETED:` - **Completion summary line**

---

### 2. Agent Type Detection

**Pattern:** Identify which agent is executing → Route appropriately

```typescript
// From capture-all-events.ts
let agentName = getAgentForSession(sessionId);

// Detect from Task tool
if (hookData.tool_name === 'Task' && hookData.tool_input?.subagent_type) {
  agentName = hookData.tool_input.subagent_type;
  setAgentForSession(sessionId, agentName);
}

// Detect from CLAUDE_CODE_AGENT env variable
else if (process.env.CLAUDE_CODE_AGENT) {
  agentName = process.env.CLAUDE_CODE_AGENT;
}

// Detect from path (subagents run in /agents/name/)
else if (hookData.cwd && hookData.cwd.includes('/agents/')) {
  const agentMatch = hookData.cwd.match(/\/agents\/([^\/]+)/);
  if (agentMatch) agentName = agentMatch[1];
}
```

**Session Mapping:** `${PAI_DIR}/agent-sessions.json`
```json
{
  "session-id-abc123": "engineer",
  "session-id-def456": "researcher"
}
```

---

### 3. Observability Integration

**Pattern:** Send event to dashboard → Fail silently if offline

```typescript
import { sendEventToObservability, getCurrentTimestamp, getSourceApp } from './lib/observability';

await sendEventToObservability({
  source_app: getSourceApp(),           // 'PAI' or agent name
  session_id: hookInput.session_id,
  hook_event_type: 'Stop',
  timestamp: getCurrentTimestamp(),
  transcript_path: hookInput.transcript_path,
  summary: completionMessage,
  // ... additional fields
}).catch(() => {
  // Silently fail - dashboard may not be running
});
```

**Dashboard URLs:**
- Server: `http://localhost:4000`
- Client: `http://localhost:5173`

---

### 4. Async Non-Blocking Execution

**Pattern:** Hook executes quickly → Launch background processes for slow operations

```typescript
// update-tab-titles.ts pattern
// Set immediate tab title (fast)
execSync(`printf '\\033]0;${titleWithEmoji}\\007' >&2`);

// Launch background process for Haiku summary (slow)
Bun.spawn(['bun', `${paiDir}/hooks/update-tab-title.ts`, prompt], {
  stdout: 'ignore',
  stderr: 'ignore',
  stdin: 'ignore'
});

process.exit(0);  // Exit immediately
```

**Key Principle:** Hooks must never block Claude Code. Always exit quickly, use background processes for slow work.

---

### 5. Graceful Failure

**Pattern:** Wrap everything in try/catch → Log errors → Exit successfully

```typescript
async function main() {
  try {
    // Hook logic here
  } catch (error) {
    // Log but don't fail
    console.error('Hook error:', error);
  }

  process.exit(0);  // Always exit 0
}
```

**Why:** If hooks crash, Claude Code may freeze. Always exit cleanly.

---

## Creating Custom Hooks

### Step 1: Choose Hook Event
Decide which event should trigger your hook (SessionStart, Stop, PostToolUse, etc.)

### Step 2: Create Hook Script
**Location:** `${PAI_DIR}/hooks/my-custom-hook.ts`

**Template:**
```typescript
#!/usr/bin/env bun

interface HookInput {
  session_id: string;
  transcript_path: string;
  hook_event_name: string;
  // ... event-specific fields
}

async function main() {
  try {
    // Read stdin
    const input = await Bun.stdin.text();
    const data: HookInput = JSON.parse(input);

    // Your hook logic here
    console.log(`Hook triggered: ${data.hook_event_name}`);

    // Example: Read transcript
    const fs = require('fs');
    const transcript = fs.readFileSync(data.transcript_path, 'utf-8');

    // Do something with the data

  } catch (error) {
    // Log but don't fail
    console.error('Hook error:', error);
  }

  process.exit(0);  // Always exit 0
}

main();
```

### Step 3: Make Executable
```bash
chmod +x ${PAI_DIR}/hooks/my-custom-hook.ts
```

### Step 4: Add to settings.json
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${PAI_DIR}/hooks/my-custom-hook.ts"
          }
        ]
      }
    ]
  }
}
```

### Step 5: Test
```bash
# Test hook directly
echo '{"session_id":"test","transcript_path":"/tmp/test.jsonl","hook_event_name":"Stop"}' | bun ${PAI_DIR}/hooks/my-custom-hook.ts
```

### Step 6: Restart Claude Code
Hooks are loaded at startup. Restart to apply changes.

---

## Hook Development Best Practices

### 1. **Fast Execution**
- Hooks should complete in < 500ms
- Use background processes for slow work (Haiku API calls, file processing)
- Exit immediately after launching background work

### 2. **Graceful Failure**
- Always wrap in try/catch
- Log errors to stderr (available in hook debug logs)
- Always `process.exit(0)` - never throw or exit(1)

### 3. **Non-Blocking**
- Never wait for external services (unless they respond quickly)
- Use `.catch(() => {})` for async operations
- Fail silently if optional services are offline

### 4. **Stdin Reading**
- Use timeout when reading stdin (Claude Code may not send data immediately)
- Handle empty/invalid input gracefully

```typescript
const decoder = new TextDecoder();
const reader = Bun.stdin.stream().getReader();

const timeoutPromise = new Promise<void>((resolve) => {
  setTimeout(() => resolve(), 500);  // 500ms timeout
});

await Promise.race([readPromise, timeoutPromise]);
```

### 5. **File I/O**
- Check `existsSync()` before reading files
- Create directories with `{ recursive: true }`
- Use PST timestamps for consistency

### 6. **Environment Access**
- All `settings.json` env vars available via `process.env`
- Use `${PAI_DIR}` in settings.json for portability
- Access in code via `process.env.PAI_DIR`

### 7. **Observability**
- Send events to dashboard for visibility
- Include all relevant metadata (session_id, tool_name, etc.)
- Use `.catch(() => {})` - dashboard may be offline

---

## See Also
- [hook-reference.md](hook-reference.md) - Complete hook types reference
- [hook-troubleshooting.md](hook-troubleshooting.md) - Debugging and advanced patterns
- [hook-quickref.md](hook-quickref.md) - Quick reference card
- **Agent Architecture:** `${PAI_DIR}/skills/CORE/agent-guide.md`
- **History/UOCS:** `${PAI_DIR}/skills/CORE/history-system.md`
- **Observability Dashboard:** `${PAI_DIR}/skills/system-observability/`

---

**Last Updated:** 2025-11-01
**Status:** Production - All hooks active and tested
**Maintainer:** Jean-Marc Giorgi (maintainer@example.com)
