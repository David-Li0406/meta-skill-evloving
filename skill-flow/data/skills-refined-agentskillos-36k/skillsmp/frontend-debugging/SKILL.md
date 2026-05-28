---
name: frontend-debugging
description: Expert guidance for debugging Next.js, React, and Playwright applications with modern tools and best practices.
---

# Frontend Debugging

Use this skill when you need to troubleshoot UI issues, state management bugs, or test failures in a Next.js/React environment.

## VSCode Simple Browser (Recommended)

The Simple Browser is a lightweight embedded browser in VSCode, ideal for quick visual debugging without leaving the editor.

### How to Use
1. **Start Dev Server**: Run `bun dev` to start your app (typically on `http://localhost:5001`).
2. **Open Simple Browser**: Use the `open_simple_browser` tool with the URL to preview directly in VSCode.
3. **Side-by-Side View**: Drag the Simple Browser tab to view code and preview simultaneously.

### Agent Workflow
When debugging UI issues:
```
1. Start the dev server: bun dev (background process)
2. Open Simple Browser: open_simple_browser with http://localhost:5001
3. Navigate to the problematic route: open_simple_browser with http://localhost:5001/route
4. Read the relevant component code
5. Make changes and observe the preview (auto-refreshes with Fast Refresh)
```

### Benefits
- **No Context Switching**: Stay in VSCode while visually inspecting the app.
- **Fast Iteration**: Changes trigger Fast Refresh; see results instantly.
- **Route Testing**: Quickly navigate to any route by changing the URL.
- **Screenshot Capability**: Use Playwright MCP tools to capture screenshots if deeper inspection is needed.

### Limitations
- No DevTools access (use external browser for DOM/Network inspection).
- Basic rendering only (no browser extensions like React DevTools).
- Use external browser for complex debugging scenarios.

## Next.js Debugging

### Server-Side Debugging
- **Inspect Flag**: Run `bun dev --inspect` to enable the Node.js inspector.
- **VS Code**: Use the "Next.js: debug server-side" configuration in `launch.json`.
- **Chrome**: Navigate to `chrome://inspect` to attach to the server process.

### Client-Side Debugging
- **Browser DevTools**: Use the Sources tab (Chrome) or Debugger tab (Firefox).
- **React DevTools**: Use the Components and Profiler tabs to inspect state and props.
- **Breakpoints**: Use `debugger;` statements in code or set breakpoints in DevTools.

## Playwright Debugging

### Interactive Debugging
- **Inspector**: Run `npx playwright test --debug` to open the Playwright Inspector.
- **Manual Pause**: Insert `await page.pause()` in your test to stop execution and inspect the page.
- **Headed Mode**: Use `--headed` to see the browser during execution.

### Post-Mortem Analysis
- **Trace Viewer**: Record traces with `trace: 'on'` in config and view them with `npx playwright show-trace {path-to-trace}`.
- **Actionability Logs**: Check the logs in the Inspector to see why an action (like a click) failed.

### Playwright MCP for Visual Debugging
When Simple Browser isn't enough, use Playwright MCP tools for deeper inspection:
- **Snapshot**: `mcp_playwright_mc_browser_snapshot` captures the accessibility tree.
- **Screenshot**: `mcp_playwright_mc_browser_take_screenshot` captures a visual screenshot.
- **Navigate**: `mcp_playwright_mc_browser_navigate` opens a URL in a full Playwright browser.
- **Click/Type**: Interact with elements programmatically for automated debugging.

## Best Practices
1. **Start with Simple Browser**: For quick visual checks, use Simple Browser first.
2. **Escalate to External Browser**: When you need DevTools, open in Chrome/Firefox.
3. **Use Playwright MCP for Automation**: For repetitive debugging or screenshots.
4. **Source Maps**: Ensure `productionBrowserSourceMaps: true` is set in `next.config.ts` if debugging production builds.
5. **Console Logging**: Use `console.log` sparingly; prefer breakpoints for complex state inspection.
6. **Network Tab**: Monitor API calls and responses in external browser DevTools.
7. **Fast Refresh**: Be aware that Fast Refresh might clear local state; use persistent storage or URL state for critical data.
