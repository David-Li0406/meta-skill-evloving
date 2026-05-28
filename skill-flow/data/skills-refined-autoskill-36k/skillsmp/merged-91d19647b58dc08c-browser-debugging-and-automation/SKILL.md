---
name: browser-debugging-and-automation
description: Use this skill for comprehensive browser debugging, UI testing, and performance analysis using Chrome DevTools MCP. Ideal for validating UI functionality, monitoring console output, analyzing network requests, and ensuring design fidelity.
---

# Browser Debugging and Automation

This skill provides a robust framework for browser-based UI testing, visual analysis, and debugging capabilities using Chrome DevTools MCP and optional external vision models via Claudish.

## When to Use This Skill

Invoke this skill when:

- **Validating Own Work**: After implementing UI features, verify functionality in a real browser.
- **Design Fidelity Checks**: Compare implementation screenshots against design references.
- **Visual Regression Testing**: Detect layout shifts, styling issues, or visual bugs.
- **Console Error Investigation**: Address user-reported console errors or warnings.
- **Form/Interaction Testing**: Ensure user interactions work correctly.
- **Pre-Commit Verification**: Validate changes before committing or deploying code.
- **Bug Reproduction**: Investigate UI bugs described by users.
- **Performance Analysis**: Analyze network requests and performance metrics.

## Prerequisites

### Required: Chrome DevTools MCP

Ensure Chrome DevTools MCP is installed and available:

```bash
# Check if available
mcp__chrome-devtools__list_pages 2>/dev/null && echo "Available" || echo "Not available"

# Install via claudeup (recommended)
npm install -g claudeup@latest
claudeup mcp add chrome-devtools
```

### Optional: External Vision Models (via OpenRouter)

For advanced visual analysis, use external vision-language models via Claudish:

```bash
# Check OpenRouter API key
[[ -n "${OPENROUTER_API_KEY}" ]] && echo "OpenRouter configured" || echo "Not configured"

# Install claudish
npm install -g claudish
```

## Core Tools

### Page Management

- **list_pages**: Get all open pages.
- **select_page**: Select a page for operations.
- **navigate_page**: Navigate to a specific URL or reload.
- **close_page**: Close a specific page.

### Snapshots and Screenshots

- **take_snapshot**: Get the current DOM structure with element UIDs.
- **take_screenshot**: Capture a visual representation of the page.

### Element Interaction

- **click**: Click on an element using its UID.
- **fill**: Type text into input fields.
- **hover**: Hover over an element.
- **handle_dialog**: Accept or dismiss browser alerts.

### Debugging Tools

- **list_console_messages**: Get console output.
- **list_network_requests**: Analyze network traffic.
- **evaluate_script**: Execute JavaScript in the page context.

### Performance Tools

- **performance_start_trace**: Start recording a performance profile.
- **performance_stop_trace**: Stop recording and save the trace.

## Workflow Patterns

### Pattern A: Identifying Elements

1. **Take a Snapshot**: Use `take_snapshot` to get the current page structure.
2. **Find the UID**: Identify the target element's UID.
3. **Interact**: Use `click(uid=...)` or `fill(uid=..., value=...)`.

### Pattern B: Troubleshooting Errors

1. **Check Console**: Use `list_console_messages` to identify JavaScript errors.
2. **Inspect Network**: Use `list_network_requests` to find failed resources.
3. **Evaluate Script**: Use `evaluate_script` to check specific DOM values.

### Pattern C: Performance Profiling

1. **Start Trace**: Use `performance_start_trace(reload=true, autoStop=true)`.
2. **Wait for Load**: Allow the page to load or the trace to finish.
3. **Analyze Insights**: Use `performance_analyze_insight` to identify performance issues.

## Best Practices

- **Always Snapshot First**: Use `take_snapshot` before interacting to get UIDs.
- **Select Page First**: Use `select_page` before page-specific operations.
- **Check Console for Errors**: Use `list_console_messages` for debugging.
- **Inspect Network**: Use `list_network_requests` to debug API issues.

## Example Usage

### 1. Validate UI After Implementation

```markdown
1. **Navigate to the page**:
   ```
   mcp__chrome-devtools__navigate_page(url: "http://localhost:5173/your-route")
   ```

2. **Take a screenshot**:
   ```
   mcp__chrome-devtools__take_screenshot(filePath: "/tmp/implementation.png")
   ```

3. **Check console for errors**:
   ```
   mcp__chrome-devtools__list_console_messages()
   ```

4. **Analyze network requests**:
   ```
   mcp__chrome-devtools__list_network_requests()
   ```

5. **Report results**: Compile findings and report to the team.
```

### 2. Perform Design Fidelity Check

```markdown
1. **Capture Design Reference**:
   ```
   mcp__chrome-devtools__navigate_page(url: "https://figma.com/proto/...")
   mcp__chrome-devtools__take_screenshot(filePath: "/tmp/design-reference.png")
   ```

2. **Capture Implementation**:
   ```
   mcp__chrome-devtools__navigate_page(url: "http://localhost:5173/component")
   mcp__chrome-devtools__take_screenshot(filePath: "/tmp/implementation.png")
   ```

3. **Analyze with Vision Model**:
   ```bash
   npx claudish --model qwen/qwen3-vl-32b-instruct --stdin --quiet <<EOF
   Compare these two UI screenshots and identify design fidelity issues:
   DESIGN REFERENCE: /tmp/design-reference.png
   IMPLEMENTATION: /tmp/implementation.png
   EOF
   ```

4. **Generate Fix Recommendations**: Parse output and create actionable fixes.
```

## Related Skills

- **react-typescript** - React component patterns.
- **tanstack-router** - Navigation and routing.
- **shadcn-ui** - Component library usage.
- **testing-frontend** - Automated testing strategies.