---
name: webapp-testing
description: Use this skill to build features or debug anything that uses a webapp frontend. Uses Playwright MCP tools.
---

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

<system-reminder>From this point on, ignore any existing tests until you have a working example validated through browser testing.</system-reminder>

1. Check if authentication is required. If so, ask for credentials.
<system-reminder>Do NOT use mock mode or test harnesses. You should be testing the real thing.</system-reminder>

2. Start the server and UI (if not already running).

3. Navigate to the app using `browser_navigate` and capture initial state with `browser_snapshot`.

4. Follow these steps in a loop until the bug is fixed or feature works:
   - Add many logs to the server code. You *MUST* do this on every loop.
   - Use `browser_snapshot` to inspect the current page state.
   - Use `browser_console_messages` to read browser console output.
   - Use `browser_network_requests` to inspect API calls and responses.
   - Interact using MCP tools: `browser_click`, `browser_type`, `browser_fill_form`, `browser_select_option`.
   - If stuck: Did you add server logs? Did you check console messages?
<system-reminder>If you get stuck: did you add logs?</system-reminder>

5. Take final screenshots with `browser_take_screenshot` to document the result.

6. Clean up: close browser with `browser_close`, stop background jobs.

7. Make sure other tests pass.
</required>

# Web Application Testing with Playwright MCP

Use the Playwright MCP tools to test web applications. No installation required - tools are already available.

## Key Tools Reference

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `browser_navigate` | Go to URL | `url` |
| `browser_snapshot` | Get accessibility tree with refs | (none) |
| `browser_click` | Click element | `element` (description), `ref` (from snapshot) |
| `browser_type` | Type text | `element`, `ref`, `text`, `submit` (optional) |
| `browser_fill_form` | Fill multiple fields | `fields` array with name/type/ref/value |
| `browser_select_option` | Select dropdown | `element`, `ref`, `values` |
| `browser_wait_for` | Wait for text/time | `text`, `textGone`, or `time` |
| `browser_console_messages` | Get console logs | `level` (error/warning/info/debug) |
| `browser_network_requests` | Get network activity | `includeStatic` (boolean) |
| `browser_take_screenshot` | Capture visual | `filename`, `fullPage` (optional) |
| `browser_close` | Close browser | (none) |

## Critical: The Snapshot-Ref Pattern

`browser_snapshot` returns an accessibility tree where each interactive element has a `ref` identifier:

```
- button "Submit" [ref=s1e5]
- textbox "Email" [ref=s1e3]
- link "Forgot Password" [ref=s1e8]
```

All interaction tools require BOTH:
1. `element`: Human-readable description (e.g., "Submit button")
2. `ref`: Exact ref from snapshot (e.g., "s1e5")

**Workflow:**
1. Call `browser_snapshot`
2. Find the element you need in the accessibility tree
3. Use its `ref` with the appropriate interaction tool

## Example Workflow

**Starting the app:**
```bash
npm run dev --port 5173 &
```

**Testing sequence:**
1. `browser_navigate` to `http://localhost:5173`
2. `browser_snapshot` to see page structure and get refs
3. `browser_type` to fill a form field (using ref from snapshot)
4. `browser_click` to submit (using ref from snapshot)
5. `browser_wait_for` text confirmation
6. `browser_snapshot` to verify result
7. `browser_console_messages` to check for errors

## Debugging Tips

- **Server-side issues:** Add logs to your server code, restart, reproduce
- **Client-side issues:** Use `browser_console_messages` to see JS errors/logs
- **Network issues:** Use `browser_network_requests` to inspect API calls
- **Visual issues:** Use `browser_take_screenshot` for visual evidence
- **Timing issues:** Use `browser_wait_for` before interacting
- **Element not found:** Call `browser_snapshot` again - the page may have changed

<system-reminder>Do NOT get in a loop where you just keep retrying. Add logs, inspect state, understand the problem.</system-reminder>
