# Playwright MCP Validation (Required)

## Ensure MCP server is running
- Attempt a lightweight MCP call (snapshot or navigate).
- If MCP is unavailable, start it from this repo root:
  - WSL/Linux: `npx @playwright/mcp@latest`
  - Windows host: `cmd /c npx @playwright/mcp@latest`
- Keep the server running for the full validation session.

## Preflight
- Load Excel data and print keys (mask secrets).
- Confirm the target URL and test that the page loads.

## Validate each step
Use the same pattern for every action (fill/click):
1. Take a snapshot before the action.
2. Perform the action.
3. For `.fill()`, evaluate the field value and compare to the Excel value.
4. Take a screenshot after the action.
5. After checkpoints, collect console errors and network requests.

```text
mcp__playwright__browser_snapshot
mcp__playwright__browser_type
mcp__playwright__browser_evaluate
mcp__playwright__browser_take_screenshot
mcp__playwright__browser_console_messages(level="error")
mcp__playwright__browser_network_requests(includeStatic=false)
```

## Error handling
On any exception:
- Capture a screenshot and snapshot.
- Collect console errors and failed network requests.
- Report the mismatch and re-raise the error.

## Report
Write a markdown report that includes:
- Script path, Excel path, target subject, timestamp
- Excel keys loaded (mask secrets)
- Step-by-step status + screenshots
- Console error summary
- Network request summary (failures highlighted)
