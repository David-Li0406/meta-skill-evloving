---
name: browser-verification
description: Verify browser-based acceptance criteria using ExecuteAutomation Playwright MCP with multi-tool fallback chain.
---

# Browser Verification Skill

Verify UI-related acceptance criteria using MCP browser tooling with evidence
(snapshots, logs, or screenshots).

## Inputs

For each criterion, use metadata from `Verify:`:
- route (e.g., `/login`)
- selector (e.g., `[data-testid="login-form"]`)
- expected state (visible, text, attribute, etc.)
- optional actions (click, type, hover)
- optional viewport

## Workflow Overview

```
1. Load config (dev server + auth + browser)
2. Select browser tool (with fallback chain)
3. Authenticate (if required)
4. Navigate and validate
5. Capture evidence
6. Handle errors and recover
7. Report results
```

## Step 1: Load Configuration

Read `.claude/verification-config.json` for:

**Dev Server:**
- `devServer.command`
- `devServer.url`
- `devServer.startupSeconds`

**Authentication:**
- `auth.strategy` — `none`, `env`, or `storage-state`
- `auth.loginRoute` — URL path for login form
- `auth.credentials.usernameVar` — Env var name for username
- `auth.credentials.passwordVar` — Env var name for password
- `auth.storageState` — Path to save/load session state

**Browser:**
- `browser.tool` — `auto`, `executeautomation`, `browsermcp`, `playwright`, `chromedevtools`
- `browser.headless` — Run headless (default: true)
- `browser.timeout` — Default timeout in ms (default: 30000)
- `browser.navigationTimeout` — Navigation timeout in ms (default: 60000)

If config is missing or incomplete, ask the human to run `/configure-verification`.

## Step 1.5: HTTP-First Evaluation

Before launching browser tools, evaluate if the criterion can be satisfied with HTTP.
This optimization skips browser overhead for criteria that don't require DOM inspection.

### Criteria Eligible for HTTP-First

| Criterion Pattern | HTTP Check | Skip Browser If... |
|-------------------|------------|-------------------|
| "Page loads at {url}" | `curl -sf {url}` | HTTP 200 returned |
| "API returns {status}" | `curl -o /dev/null -w "%{http_code}" {url}` | Status matches |
| "Endpoint responds with {data}" | `curl -s {url} \| jq/grep` | Data found |
| "Service health check" | `curl -sf {url}/health` | Health endpoint OK |
| "Redirect to {url}" | `curl -sI {url} \| grep Location` | Location header matches |

### HTTP-First Execution

```bash
# Generic page accessibility check
curl -sf "{devServer.url}{route}" -o /dev/null && echo "HTTP_PASS" || echo "HTTP_FAIL"

# Response content check
curl -s "{devServer.url}{route}" | grep -q "{expected_text}" && echo "HTTP_PASS" || echo "HTTP_FAIL"

# Status code check
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "{url}")
[ "$HTTP_CODE" = "{expected}" ] && echo "HTTP_PASS" || echo "HTTP_FAIL"
```

### Decision Logic

**If HTTP_PASS and criterion does NOT require:**
- Specific DOM element verification (`selector`, `data-testid`, `visible`)
- Visual appearance check (`screenshot`, `layout`, `style`)
- User interaction simulation (`click`, `type`, `hover`)
- Console log inspection (`console`, `errors`, `warnings`)
- Network timing analysis (`performance`, `timing`)

**Then:**
- Mark criterion as PASS
- Skip browser verification entirely
- Note method as "HTTP-first" in evidence
- Log: "Verified via HTTP (browser tools not required)"

**Otherwise:**
- Continue to Step 2 (browser tool selection)
- HTTP result can inform browser verification (e.g., server is reachable)

### HTTP-First Benefits

- **Speed:** curl is ~10x faster than browser launch
- **Reliability:** No browser MCP dependency issues
- **Simplicity:** Works even if no browser tools configured
- **Resources:** Lower memory and CPU usage

## Step 2: Tool Selection (Automatic with Fallback)

Automatically detect and use the best available browser tool. Try tools in
order until one responds:

```
1. ExecuteAutomation Playwright MCP (primary)
   - Package: @executeautomation/playwright-mcp-server
   - Test: Check for mcp__playwright__* or mcp__executeautomation__* tools
   - Why primary: Most stable, actively maintained (312+ commits), 143 device presets
   - Avoids @playwright/mcp@latest beta instability issues

2. Browser MCP (if extension installed)
   - Source: browsermcp.io browser extension
   - Test: Check for mcp__browsermcp__* tools
   - Advantage: Uses existing browser profile (stays logged in, avoids bot detection)
   - Requires: User has Browser MCP extension installed

3. Microsoft Playwright MCP (pinned version)
   - Package: @anthropic-ai/mcp-server-playwright (pinned, NOT @latest)
   - Test: Check for mcp__playwright__* tools (if not already found)
   - Why fallback: Official but @latest includes unstable betas
   - Use pinned version only

4. Chrome DevTools MCP (basic fallback)
   - Test: Call mcp__chrome-devtools__list_pages
   - Often pre-installed with Claude Code
   - Limited: Not designed for automation, less stable for complex workflows
   - Use for: Simple navigation, screenshots, basic interactions

5. Manual Verification (last resort) — SOFT BLOCK
   - If all tools fail, do NOT silently continue
   - Display warning and prompt user:
     ```
     ⚠️  NO BROWSER TOOLS AVAILABLE

     Attempted to detect browser MCP tools but none responded:
     - ExecuteAutomation Playwright: {status}
     - Browser MCP: {status}
     - Microsoft Playwright: {status}
     - Chrome DevTools: {status}

     Browser criteria cannot be verified automatically.

     Options:
     1. Continue anyway (criteria become manual verification)
     2. Stop and configure browser tools first

     To enable automated browser verification, add to ~/.mcp.json:
     {
       "mcpServers": {
         "executeautomation-playwright": {
           "command": "npx",
           "args": ["-y", "@executeautomation/playwright-mcp-server"]
         }
       }
     }
     ```
   - Use AskUserQuestion to let user choose:
     - "Continue with manual verification" → Mark criteria as BLOCKED, list for human
     - "Stop to configure tools" → Halt and provide detailed setup instructions
```

**Log tool selection:**
```
Browser Tool: ExecuteAutomation Playwright MCP (auto-detected)
Fallback chain: Browser MCP → Microsoft Playwright → Chrome DevTools → Manual (soft block)
```

## Step 3: Authentication

**Skip if `auth.strategy` is `none`.**

### Strategy: `storage-state`

1. Check if `auth.storageState` file exists and is recent (< 24h)
2. If exists, load session state into browser
3. Navigate to a protected route to verify session validity
4. If session invalid, proceed to login flow

### Strategy: `env` (or storage-state with invalid session)

1. Read credential env var names from config (NOT the values)
2. Navigate to `auth.loginRoute`
3. Identify login form fields (username/email, password)
4. Fill credentials using browser tool's form fill
   - Pass env var names to the tool, which reads values from environment
   - Agent NEVER sees plaintext credentials
5. Submit the form
6. Wait for successful login indicator (redirect, logged-in element)
7. Save session to `auth.storageState` for reuse

### Auth Failure Handling

If login fails after 2 attempts:
- Mark criteria as BLOCKED (not FAIL)
- Report: "Authentication failed. Check credentials in .env.verification"
- Do NOT expose credential values in error messages

## Step 4: Navigate and Validate

For each browser criterion:

1. Start from base URL (`devServer.url`)
2. Navigate to the criterion's route
3. Wait for content to load:
   - Use wait-for-text or wait-for-selector
   - Respect `browser.navigationTimeout`
4. Perform optional actions in order (click, type, hover)
5. Validate expected state:
   - visibility
   - text content
   - attribute values
   - layout position
6. Capture console errors and network failures when relevant

## Step 5: Evidence Capture

Capture evidence appropriate to the criterion type:

| Type | Evidence |
|------|----------|
| DOM | Accessibility snapshot, selector details |
| VISUAL | Screenshot |
| CONSOLE | Console log excerpt |
| NETWORK | Request/response summary |
| PERFORMANCE | Timing metrics (if supported) |
| ACCESSIBILITY | ARIA/semantic checks and notes |

Save evidence under `.claude/verification/` with stable names:
- `browser-{task-id}-{criterion-id}.png`
- `browser-{task-id}-{criterion-id}.json`

## Step 6: Error Recovery

**Detect failures:**
- Tool returns "undefined" or "Error calling tool"
- Connection timeout
- Server not responding

**Recovery procedure:**

```
1. Log the error with context:
   "Tool {name} returned: {error}"

2. If transient error (timeout, connection):
   - Wait 2 seconds
   - Retry current operation (max 2 retries)

3. If persistent error or tool unavailable:
   - Attempt tool restart (kill and re-init MCP)
   - If restart succeeds, retry current criterion

4. If restart fails:
   - Try next tool in fallback chain
   - Log: "Switching from {current} to {fallback}"

5. If all tools exhausted:
   - Mark remaining criteria as BLOCKED
   - Report: "Browser tools unavailable after trying:
     - ExecuteAutomation Playwright: {error}
     - Browser MCP: {error or 'not installed'}
     - Microsoft Playwright: {error}
     - Chrome DevTools: {error}
     Manual verification required."
```

**Session degradation detection:**

Some tools work initially then fail after extended use. Monitor for:
- Increasing response times
- Intermittent "undefined" errors
- Loss of page state

If detected, proactively switch to fallback before complete failure.

## Step 7: Output Format

Return a structured result for each criterion:

```
BROWSER VERIFICATION RESULT
---------------------------
Instruction ID: [ID]
Status: PASS | FAIL | BLOCKED
Type: DOM | VISUAL | CONSOLE | NETWORK | PERFORMANCE | ACCESSIBILITY
URL: [URL] | Viewport: [width]x[height]

Finding: [What was observed]
Expected: [What was expected]

Evidence:
- {path}

Suggested Fix: [If FAIL]
```

## Failure Handling Summary

| Condition | Action | Status |
|-----------|--------|--------|
| Dev server unreachable | Report failing command | BLOCKED |
| Selector missing | Capture screenshot | FAIL |
| Auth fails | Check credentials | BLOCKED |
| Tool unavailable | Try fallback chain | Continue or BLOCKED |
| Tool returns undefined | Retry then switch | Continue or BLOCKED |
| All tools fail | Require manual verification | BLOCKED |

## Tool-Specific Notes

### ExecuteAutomation Playwright MCP (Recommended Primary)
- Package: `@executeautomation/playwright-mcp-server`
- Most stable option, actively maintained (312+ commits)
- 143 device presets for responsive testing
- Cross-browser support (Chrome, Firefox, Safari)
- Install: Add to `.claude/settings.json` mcpServers:
  ```json
  {
    "mcpServers": {
      "playwright": {
        "command": "npx",
        "args": ["-y", "@executeautomation/playwright-mcp-server"]
      }
    }
  }
  ```

### Browser MCP (Best for Auth-Heavy Apps)
- Source: [browsermcp.io](https://browsermcp.io/)
- Uses your existing browser profile (stays logged in to services)
- Local execution (no network latency, better privacy)
- Bot-detection resistant (uses real browser fingerprint)
- Requires: Browser MCP Chrome extension installed
- Best for: Apps where maintaining login sessions matters

### Microsoft Playwright MCP (Use Pinned Version)
- Package: `@anthropic-ai/mcp-server-playwright` (recommended)
- Official implementation with accessibility tree support
- **AVOID** `@playwright/mcp@latest` — includes unstable betas causing "undefined" errors
- If you must use Microsoft's version, pin to a specific stable version

### Chrome DevTools MCP (Basic Fallback)
- Often pre-installed with Claude Code
- Good for debugging and simple automation
- Use `mcp__chrome-devtools__*` tools
- **Limitations:** Not designed for complex automation, less stable for multi-step workflows
- Best for: Quick screenshots, simple navigation, debugging

### Browserbase + Stagehand (Cloud Option)
- Package: `@browserbasehq/mcp-server-browserbase`
- Cloud-hosted browsers (no local browser needed)
- Stealth mode, proxy support, concurrent sessions
- Requires: Browserbase API key (external service)
- Best for: CI/CD pipelines, high-volume testing, anti-detection needs
