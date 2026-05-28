# Hook Troubleshooting

**Debugging and advanced hook patterns**

This document covers common hook issues, debugging techniques, and advanced troubleshooting for the PAI hook system.

---

## Troubleshooting

### Hook Not Running

**Check:**
1. Is hook script executable? `chmod +x ${PAI_DIR}/hooks/my-hook.ts`
2. Is path correct in settings.json? Use `${PAI_DIR}/hooks/...`
3. Is settings.json valid JSON? `jq . ${PAI_DIR}/settings.json`
4. Did you restart Claude Code after editing settings.json?

**Debug:**
```bash
# Test hook directly
echo '{"session_id":"test","transcript_path":"/tmp/test.jsonl","hook_event_name":"Stop"}' | bun ${PAI_DIR}/hooks/my-hook.ts

# Check hook logs (stderr output)
tail -f ${PAI_DIR}/hooks/debug.log  # If you add logging
```

---

### Hook Hangs/Freezes Claude Code

**Cause:** Hook not exiting (infinite loop, waiting for input, blocking operation)

**Fix:**
1. Add timeouts to all blocking operations
2. Ensure `process.exit(0)` is always reached
3. Use background processes for long operations
4. Check stdin reading has timeout

**Prevention:**
```typescript
// Always use timeout
setTimeout(() => {
  console.error('Hook timeout - exiting');
  process.exit(0);
}, 5000);  // 5 second max
```

---

### History Not Capturing

**Check:**
1. Does `${PAI_DIR}/history/` directory exist?
2. Are structured sections present in response? (`📋 SUMMARY:`, `🎯 COMPLETED:`, etc.)
3. Is hook actually running? Check `${PAI_DIR}/history/raw-outputs/` for events
4. File permissions? `ls -la ${PAI_DIR}/history/sessions/`

**Debug:**
```bash
# Check recent captures
ls -lt ${PAI_DIR}/history/sessions/$(date +%Y-%m)/ | head -10
ls -lt ${PAI_DIR}/history/learnings/$(date +%Y-%m)/ | head -10

# Check raw events
tail ${PAI_DIR}/history/raw-outputs/$(date +%Y-%m)/$(date +%Y-%m-%d)_all-events.jsonl
```

**Common Issues:**
- Missing structured format → No parsing
- No `🎯 COMPLETED:` line → Capture may fail
- Learning detection too strict → Adjust `isLearningCapture()` logic

---

### Stop Event Not Firing (CRITICAL KNOWN ISSUE)

**Symptom:** Stop hook configured and working, but Stop events not firing consistently

**Evidence:**
```bash
# Check if Stop events fired today
grep '"event_type":"Stop"' ${PAI_DIR}/history/raw-outputs/$(date +%Y-%m)/$(date +%Y-%m-%d)_all-events.jsonl
# Result: 0 matches (no Stop events)

# But other hooks ARE working
grep '"event_type":"PostToolUse"' ${PAI_DIR}/history/raw-outputs/$(date +%Y-%m)/$(date +%Y-%m-%d)_all-events.jsonl
# Result: 80+ matches (PostToolUse working fine)
```

**Impact:**
- Automatic work summaries NOT captured to history (despite Stop hook logic being correct)
- Learning moments NOT auto-detected
- Manual verification and capture REQUIRED

**Root Cause:**
- Claude Code event trigger issue (external to hook system)
- Stop event not being emitted when main agent completes responses
- Hook configuration is correct, hook script works, event just never fires
- Other event types (PostToolUse, SessionEnd, UserPromptSubmit) work fine

**Workaround (MANDATORY):**

1. **Added CAPTURE field to response format** (see `${PAI_DIR}/skills/CORE/SKILL.md`)
   - MANDATORY field in every response
   - Forces verification before completing responses
   - Must document: "Auto-captured" / "Manually saved" / "N/A"

2. **Added MANDATORY VERIFICATION GATE** to file organization section
   - Before completing valuable work, MUST run verification commands
   - Check if auto-capture happened (ls -lt history directories)
   - If not, manually save to appropriate history location

3. **Verification Commands:**
   ```bash
   # Check if auto-captured (should happen, but often doesn't due to Stop event bug)
   ls -lt ${PAI_DIR}/history/sessions/$(date +%Y-%m)/ | head -5
   ls -lt ${PAI_DIR}/history/learnings/$(date +%Y-%m)/ | head -5

   # If 0 results or doesn't match current work → Manual capture required
   ```

**Status:** UNRESOLVED (Claude Code issue, not hook configuration)
**Mitigation:** Structural enforcement via response format (cannot complete valuable work without verification)
**Tracking:** Documented in `${PAI_DIR}/skills/CORE/SKILL.md` (History Capture System section)

**Long-term Fix:**
- Report to Anthropic (Claude Code team) as Stop event reliability issue
- Monitor future Claude Code updates for fix
- Keep workaround in place until Stop events fire reliably

---

### Agent Detection Failing

**Check:**
1. Is `${PAI_DIR}/agent-sessions.json` writable?
2. Is `[AGENT:type]` tag in `🎯 COMPLETED:` line?
3. Is agent running from correct directory? (`/agents/name/`)

**Debug:**
```bash
# Check session mappings
cat ${PAI_DIR}/agent-sessions.json | jq .

# Check subagent-stop debug log
tail -f ${PAI_DIR}/hooks/subagent-stop-debug.log
```

**Fix:**
- Ensure agents include `[AGENT:type]` in completion line
- Verify Task tool passes `subagent_type` parameter
- Check cwd includes `/agents/` in path

---

### Observability Dashboard Not Receiving Events

**Check:**
1. Is dashboard server running? `curl http://localhost:4000/health`
2. Are hooks sending events? Check `sendEventToObservability()` calls
3. Network issues? `netstat -an | grep 4000`

**Debug:**
```bash
# Start dashboard server
cd ${PAI_DIR}/skills/system/observability/dashboard/apps/server
bun run dev

# Check server logs
# Events should appear in real-time
```

**Note:** Hooks fail silently if dashboard offline (by design). Not critical for operation.

---

### Context Loading Issues (SessionStart)

**Check:**
1. Does `${PAI_DIR}/skills/CORE/SKILL.md` exist?
2. Is `load-core-context.ts` executable?
3. Is `PAI_DIR` env variable set correctly?

**Debug:**
```bash
# Test context loading directly
bun ${PAI_DIR}/hooks/load-core-context.ts

# Should output <system-reminder> with SKILL.md content
```

**Common Issues:**
- Subagent sessions loading main context → Fixed (subagent detection in hook)
- File not found → Check `PAI_DIR` environment variable
- Permission denied → `chmod +x ${PAI_DIR}/hooks/load-core-context.ts`

---

## Advanced Topics

### Hook Performance Optimization

**Profiling Hooks:**
```typescript
// Add timing to hooks
const startTime = Date.now();

// ... hook logic ...

const duration = Date.now() - startTime;
console.error(`Hook completed in ${duration}ms`);
```

**Target Times:**
- SessionStart: < 100ms (critical path)
- Stop/SubagentStop: < 500ms
- Tool hooks: < 50ms (high frequency)
- SessionEnd: < 2000ms (not critical)

**Optimization Strategies:**
1. Move slow operations to background processes
2. Cache frequently accessed data (agent sessions, config)
3. Use streaming for large file operations
4. Batch dashboard events instead of one-by-one

---

### Custom Event Processing

**Pattern:** Create specialized hooks for specific tool combinations

**Example: Track Git Operations**
```json
{
  "PostToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "${PAI_DIR}/hooks/git-operation-tracker.ts"
        }
      ]
    }
  ]
}
```

```typescript
// git-operation-tracker.ts
async function main() {
  const data = JSON.parse(await Bun.stdin.text());

  if (data.tool_name === 'Bash' &&
      data.tool_input?.command?.includes('git')) {
    // Track git operations
    logGitOperation(data);
  }

  process.exit(0);
}
```

---

### State Management Between Hook Invocations

**Pattern:** Use shared state file for coordination

```typescript
// State file: ${PAI_DIR}/hooks/.state/session-state.json
interface SessionState {
  [sessionId: string]: {
    startTime: number;
    toolCount: number;
    lastTool?: string;
  };
}

function getSessionState(sessionId: string): SessionState[string] {
  const statePath = join(process.env.PAI_DIR, 'hooks', '.state', 'session-state.json');
  const state = existsSync(statePath)
    ? JSON.parse(readFileSync(statePath, 'utf-8'))
    : {};
  return state[sessionId] || { startTime: Date.now(), toolCount: 0 };
}

function updateSessionState(sessionId: string, update: Partial<SessionState[string]>) {
  const statePath = join(process.env.PAI_DIR, 'hooks', '.state', 'session-state.json');
  const state = existsSync(statePath)
    ? JSON.parse(readFileSync(statePath, 'utf-8'))
    : {};

  state[sessionId] = { ...state[sessionId], ...update };
  writeFileSync(statePath, JSON.stringify(state, null, 2));
}
```

**Use Cases:**
- Track cumulative metrics across session
- Implement rate limiting or throttling
- Coordinate between multiple hooks

---

### Advanced Error Handling

**Pattern:** Structured error logging with context

```typescript
interface HookError {
  timestamp: string;
  hookName: string;
  sessionId: string;
  error: string;
  context?: any;
}

function logHookError(error: Error, context: any) {
  const errorLog: HookError = {
    timestamp: new Date().toISOString(),
    hookName: 'my-hook',
    sessionId: context.session_id,
    error: error.message,
    context: {
      stack: error.stack,
      hookData: context
    }
  };

  const errorLogPath = join(
    process.env.PAI_DIR!,
    'hooks',
    '.logs',
    'errors.jsonl'
  );

  appendFileSync(
    errorLogPath,
    JSON.stringify(errorLog) + '\n'
  );
}
```

---

### Testing Hooks in Isolation

**Pattern:** Create test harness for hook development

```typescript
// test-hook.ts
import { spawn } from 'bun';

interface TestCase {
  name: string;
  input: any;
  expectedBehavior: string;
}

const testCases: TestCase[] = [
  {
    name: 'SessionStart',
    input: {
      session_id: 'test-123',
      transcript_path: '/tmp/test.jsonl',
      hook_event_name: 'SessionStart'
    },
    expectedBehavior: 'Should load context and exit cleanly'
  }
];

async function testHook(hookPath: string, testCase: TestCase) {
  console.log(`Testing: ${testCase.name}`);

  const proc = spawn(['bun', hookPath], {
    stdin: 'pipe',
    stdout: 'pipe',
    stderr: 'pipe'
  });

  proc.stdin.write(JSON.stringify(testCase.input));
  proc.stdin.end();

  const exitCode = await proc.exited;

  if (exitCode === 0) {
    console.log(`✅ ${testCase.name} passed`);
  } else {
    console.error(`❌ ${testCase.name} failed with exit code ${exitCode}`);
  }
}

// Run tests
for (const testCase of testCases) {
  await testHook('./my-hook.ts', testCase);
}
```

---

### Debugging with Transcript Analysis

**Pattern:** Analyze transcript to understand hook context

```typescript
function analyzeTranscript(transcriptPath: string) {
  const lines = readFileSync(transcriptPath, 'utf-8')
    .split('\n')
    .filter(line => line.trim())
    .map(line => JSON.parse(line));

  const lastUserMessage = lines
    .reverse()
    .find(line => line.role === 'user');

  const lastAssistantMessage = lines
    .reverse()
    .find(line => line.role === 'assistant');

  const recentTools = lines
    .filter(line => line.type === 'tool_use')
    .slice(-5);

  return {
    lastUserMessage,
    lastAssistantMessage,
    recentTools,
    totalMessages: lines.length
  };
}
```

---

## See Also
- [hook-system.md](hook-system.md) - Main hook guide and best practices
- [hook-reference.md](hook-reference.md) - Complete hook types reference
- [hook-quickref.md](hook-quickref.md) - Quick reference card

---

**Last Updated:** 2025-11-01
**Status:** Production - Troubleshooting guide active
**Maintainer:** Jean-Marc Giorgi (maintainer@example.com)
