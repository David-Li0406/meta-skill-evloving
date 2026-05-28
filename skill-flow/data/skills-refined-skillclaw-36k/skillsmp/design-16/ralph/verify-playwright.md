# Playwright Verification Procedure

## Extracting PLAYWRIGHT_VERIFY

Test scripts output the spec using a heredoc:

```bash
cat << 'PLAYWRIGHT_VERIFY'
{ "route": "/", "checks": [...] }
PLAYWRIGHT_VERIFY
```

Parse test output for content between `PLAYWRIGHT_VERIFY` markers.

## Execution

1. **Ensure dev server running**
   - Check ralph-state.json for dev_server.port
   - Health check: `curl http://localhost:{port} --max-time 2`
   - If not healthy: start with `Bash(command, run_in_background=true)`
   - Wait up to 30s for server to be ready

2. **Navigate**: `mcp__playwright__browser_navigate({ url: "http://localhost:{port}{route}" })`

3. **Snapshot**: `mcp__playwright__browser_snapshot({})`

4. **Verify each check**:

   | Type | How to Find in Snapshot | MCP Tool |
   |------|-------------------------|----------|
   | heading | `heading` node at specified level, name contains text | snapshot |
   | button | `button` node, name contains text | snapshot |
   | link | `link` node, name contains text | snapshot |
   | text | any node name contains text | snapshot |
   | section | region/section with label | snapshot |
   | navigation | navigation landmark | snapshot |
   | **click** | Click element, verify URL changes | browser_click |
   | **url** | Verify current URL matches expected | snapshot (Page URL) |
   | **flow** | Multi-step click → verify sequence | see below |

5. **Build result**:
   - Success: `{ "passed": true, "checks": [...] }`
   - Failure: `{ "passed": false, "failures": [...], "suggestion": "..." }`

---

## Integration Testing (Click Flows)

### Click Check

Verifies clicking an element navigates to expected URL:

```json
{
  "type": "click",
  "element": "Stakeholder Network",
  "element_type": "link",
  "expected_url": "/network"
}
```

**Execution:**
1. Find element ref in snapshot matching `element` text and `element_type`
2. `mcp__playwright__browser_click({ element: "...", ref: "..." })`
3. Wait for navigation: `mcp__playwright__browser_wait_for({ time: 2 })`
4. Verify Page URL contains `expected_url`

### Flow Check

Multi-step user flow verification:

```json
{
  "type": "flow",
  "name": "Dashboard to Meeting Prep",
  "steps": [
    { "action": "navigate", "url": "/" },
    { "action": "verify", "heading": "SA DASHBOARD" },
    { "action": "click", "link": "Providence" },
    { "action": "verify", "url_contains": "/meeting-prep" },
    { "action": "verify", "heading": "MEETING PREP:" }
  ]
}
```

**Execution:**
1. Execute each step sequentially
2. Fail on first step that doesn't pass
3. Report which step failed with context

### Example: Integration Test in PLAYWRIGHT_VERIFY

```json
{
  "route": "/",
  "prp_phase": "4",
  "checks": [
    { "type": "heading", "level": 1, "text": "SA DASHBOARD" },
    { "type": "section", "label": "ACCOUNTS" },

    { "type": "click", "element": "Stakeholder Network", "element_type": "link", "expected_url": "/network" },
    { "type": "click", "element": "Dashboard", "element_type": "link", "expected_url": "/" },

    { "type": "flow", "name": "Account drill-down", "steps": [
      { "action": "navigate", "url": "/" },
      { "action": "click", "link": "Providence" },
      { "action": "verify", "url_contains": "/meeting-prep?account=Providence" },
      { "action": "verify", "heading": "MEETING PREP: Providence" }
    ]}
  ]
}
```

---

## Retry Context

On failure, inject into next attempt:

```
Previous Playwright verification failed:
- Route: {route}
- Expected: {check type} "{text}"
- Actual: {what was found in snapshot}
- Snapshot excerpt: {relevant portion}
- Suggestion: {helpful hint based on what was found}
```

## Common Failure Patterns

| Expected | Actual | Likely Cause |
|----------|--------|--------------|
| Button "Submit" | Not found | Button rendered with different text, or not rendered at all |
| Heading "Dashboard" | Found "Login" | Auth redirect - page requires login |
| Section "Metrics" | Not found | Component not rendering, check imports |
| **Click → URL /network** | **URL still /**  | **Nav link has href="#" not actual URL** |
| **Click element** | **Element not found** | **Element ref changed after re-render** |

## Snapshot Reading Tips

The snapshot is a YAML-like accessibility tree:

```
- heading "Page Title" [level=1]
- navigation "Main"
  - link "Home" [ref=e39]
    - /url: /
  - link "Settings" [ref=e41]
    - /url: /settings
- main
  - heading "Section" [level=2]
  - button "Submit" [ref=e50]
```

Match checks against this structure. Level matters for headings.

**For click checks:** Look for `/url:` under link nodes to verify href before clicking.
