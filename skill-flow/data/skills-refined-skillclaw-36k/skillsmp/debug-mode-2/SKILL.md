---
name: debug-mode
description: Debug runtime issues using hypothesis-based methodology. Use when debugging bugs, async issues, race conditions, state problems, or when the user says "debug this", "help me debug", "find this bug", "why isn't this working", "trace through the code".
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Hypothesis-Based Debug Mode

A systematic, evidence-based debugging approach that avoids guesswork. NEVER fix code without collecting runtime data first.

## Core Principle

**Runtime evidence is mandatory.** Code analysis alone is insufficient. Traditional approaches often "fix" with confidence but fail without actual runtime data. This methodology ensures every fix is data-driven.

## Debug Workflow

### Phase 1: Hypothesis Generation

Before any instrumentation, generate **3-5 specific hypotheses** about the bug:

```
Hypothesis A: [Input/parameter related issue]
Hypothesis B: [Logic/conditional branch issue]
Hypothesis C: [State/data transformation issue]
Hypothesis D: [Async/timing/race condition]
Hypothesis E: [Type/edge case issue]
```

Each hypothesis must be **testable** via logs.

### Phase 2: Code Instrumentation

Create debug infrastructure and instrument the code.

**Step 1: Create and auto-start debug server** (for JS/TS projects):
Write to `.claude-logs/server.js`:

```javascript
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3947;
const LOG_DIR = '.claude-logs';
const LOG_FILE = path.join(LOG_DIR, 'debug.ndjson');

// Auto-create directory and empty log file on startup
if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
fs.writeFileSync(LOG_FILE, '');

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }
  if (req.url === '/health') { res.writeHead(200); res.end('ok'); return; }

  // Clear logs endpoint
  if (req.url === '/clear' && req.method === 'POST') {
    fs.writeFileSync(LOG_FILE, '');
    res.writeHead(200); res.end('cleared');
    return;
  }

  if (req.url === '/debug' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const data = JSON.parse(body);
        data.id = `log_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`;
        fs.appendFileSync(LOG_FILE, JSON.stringify(data) + '\n');
        res.writeHead(200); res.end('ok');
      } catch (e) { res.writeHead(400); res.end('bad json'); }
    });
    return;
  }
  res.writeHead(404); res.end();
});

server.listen(PORT, () => console.log(`Debug server running on port ${PORT}`));
process.on('SIGINT', () => { server.close(); process.exit(0); });
```

**Step 2: Start server in background automatically:**
After writing the server file, start it in the background using Bash with `run_in_background: true`:
```bash
node .claude-logs/server.js
```

**IMPORTANT:** The agent MUST start the server automatically before asking the user to reproduce. Never ask the user to start the server manually.

**Step 3: Instrument code** with hypothesis-tagged logs.

Use `// #region agent log` markers for easy cleanup:

```javascript
// #region agent log - Hypothesis A
fetch('http://127.0.0.1:3947/debug', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    location: 'filename.js:LINE',
    message: 'Description of what is being logged',
    data: { relevantVariables },
    timestamp: Date.now(),
    sessionId: 'SESSION_ID',
    runId: 'initial',
    hypothesisId: 'A'
  })
}).catch(() => {});
// #endregion
```

**What to log:**
- Function entry: parameters and their types
- Before conditionals: the values being tested
- Inside branches: which branch executed and why
- Before returns: the return value
- State changes: before and after values
- Error catches: error message and stack

For non-JS languages, see `${CLAUDE_PLUGIN_ROOT}/skills/debug-mode/references/instrumentation-templates.md`.

### Phase 3: Reproduction

Tell the user:
> "I've added debug instrumentation and started the debug server. Please reproduce the issue now, then let me know when done."

Wait for user confirmation before proceeding.

### Phase 4: Log Analysis & Hypothesis Evaluation

Read logs: `cat .claude-logs/debug.ndjson`

Evaluate each hypothesis:

| Status | Meaning |
|--------|---------|
| **CONFIRMED** | Logs prove this hypothesis is the root cause |
| **REJECTED** | Logs prove this hypothesis is NOT the cause |
| **INCONCLUSIVE** | Need more instrumentation to determine |

Present findings in table format:

```
## Hypothesis Evaluation

| Hypothesis | Status | Evidence |
|------------|--------|----------|
| A: Input validation | REJECTED | Log #3: params valid (a=5, b=3) |
| B: Condition bug | CONFIRMED | Log #6: returns undefined when a===0 |
| C: Calculation error | REJECTED | Log #4: math correct (5+3=8) |

**Root Cause:** Hypothesis B - condition `a === 0` incorrectly returns undefined.
```

If all hypotheses are INCONCLUSIVE:
1. Generate 3-5 new hypotheses based on log insights
2. Add more targeted instrumentation
3. **Clear logs before next reproduction:** `curl -X POST http://127.0.0.1:3947/clear`
4. Request reproduction again

**IMPORTANT:** Always clear logs before requesting a new reproduction to avoid re-reading old data and save context.

### Phase 5: Fix Application

**Rules:**
- Only fix when root cause is CONFIRMED
- Keep ALL instrumentation in place
- Make the minimal targeted fix
- Change `runId` to `"post-fix"` in existing logs

Apply the fix while preserving debug instrumentation.

### Phase 6: Verification

**Before asking user to verify:**
1. Clear logs: `curl -X POST http://127.0.0.1:3947/clear`

Then tell the user:
> "Fix applied. Please reproduce the original scenario to verify the fix works."

Compare logs:
- Only `runId: "post-fix"` logs will be present (fresh run)

Verify the confirmed hypothesis no longer shows buggy behavior.

### Phase 7: Cleanup

**Only after user confirms fix works:**

1. Remove all `// #region agent log` blocks from code
2. Stop debug server: `pkill -f ".claude-logs/server.js"`
3. Remove debug directory: `rm -rf .claude-logs/`

## Critical Rules

1. **NEVER** fix code without runtime evidence
2. **NEVER** remove instrumentation before fix is verified
3. **NEVER** use setTimeout/sleep as a "fix"
4. **ALWAYS** tag logs with `hypothesisId`
5. **ALWAYS** wait for user to reproduce before analyzing
6. **ALWAYS** use `#region agent log` markers
7. **ALWAYS** start debug server automatically (never ask user)
8. **ALWAYS** clear logs before each new reproduction request

## Log Schema

```json
{
  "id": "log_1733456789_abc1",
  "timestamp": 1733456789000,
  "location": "file.js:15",
  "message": "Human-readable description",
  "data": { "variable": "value" },
  "sessionId": "debug-uuid",
  "runId": "initial|post-fix",
  "hypothesisId": "A|B|C|D|E"
}
```

## Quick Reference

| Phase | Action | Output |
|-------|--------|--------|
| 1 | Generate hypotheses | 3-5 testable hypotheses |
| 2 | Instrument code + auto-start server | Logs at critical points |
| 3 | User reproduces | Runtime data collected |
| 4 | Analyze logs (clear if retrying) | Hypothesis table |
| 5 | Apply fix | Targeted code change |
| 6 | Clear logs + user verifies | Post-fix logs |
| 7 | Cleanup | Remove instrumentation |
