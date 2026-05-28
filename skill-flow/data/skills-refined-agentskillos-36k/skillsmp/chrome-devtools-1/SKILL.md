---
name: chrome-devtools
description: Chrome DevTools MCP for interactive debugging and development. Use for CSS inspection, network debugging, console access, performance profiling, and real-time development iteration.
---

# Chrome DevTools Skill

**Activation:** debugging, CSS inspection, network debugging, console, performance, real-time development, layout issues, computed styles

## Overview

Chrome DevTools MCP connects to your running Chrome browser for interactive debugging. Use it during development for faster iteration cycles.

**Key Difference from Playwright:**
- **Chrome DevTools** = Interactive development, debugging, exploration
- **Playwright** = Automated testing, screenshot verification, CI/CD

## When to Use Each

| Task | Chrome DevTools | Playwright |
|------|-----------------|------------|
| CSS debugging | **Yes** - Live inspect, edit styles | No |
| Console errors during dev | **Yes** - Real-time monitoring | Yes - Snapshot |
| Network inspection | **Yes** - Full request/response details | Yes - Summary |
| Performance profiling | **Yes** - CPU, memory, rendering | No |
| Screenshot proof for PR | No | **Yes** - Required |
| Automated E2E tests | No | **Yes** - Primary tool |
| Element state inspection | **Yes** - Computed styles, box model | Yes - Accessibility tree |
| Storage inspection | **Yes** - localStorage, cookies, IndexedDB | No |

## MCP Tools

### Page Interaction

```
mcp__chrome-devtools__navigate - Navigate to URL
mcp__chrome-devtools__screenshot - Capture screenshot
mcp__chrome-devtools__click - Click element
mcp__chrome-devtools__type - Type text
mcp__chrome-devtools__evaluate - Run JavaScript in page context
```

### Debugging

```
mcp__chrome-devtools__get_console_logs - Get console output
mcp__chrome-devtools__get_network_logs - Get network requests with full details
mcp__chrome-devtools__get_computed_style - Get computed CSS for element
mcp__chrome-devtools__get_element_info - Get element properties, box model
```

### Performance

```
mcp__chrome-devtools__get_performance_metrics - CPU, memory, paint timing
mcp__chrome-devtools__start_profiling - Begin CPU profile
mcp__chrome-devtools__stop_profiling - End and get profile data
```

## Development Workflow

### 1. CSS Debugging

When something doesn't look right:

```markdown
1. Get element info
   → mcp__chrome-devtools__get_element_info selector=".my-element"
   → Shows: box model, dimensions, position

2. Get computed styles
   → mcp__chrome-devtools__get_computed_style selector=".my-element"
   → Shows: All applied CSS, computed values

3. Identify the issue (wrong padding, unexpected margin, etc.)

4. Fix in code, hot reload, verify
```

### 2. Network Debugging

When API calls aren't working:

```markdown
1. Get network logs
   → mcp__chrome-devtools__get_network_logs
   → Shows: All requests with status, timing, headers

2. Find failing request

3. Get request details
   → Full request/response headers
   → Request body
   → Response body (if error)

4. Fix issue (wrong endpoint, missing auth, etc.)
```

### 3. Console Monitoring

During development iteration:

```markdown
1. Make code change

2. Check console immediately
   → mcp__chrome-devtools__get_console_logs
   → Catch errors as they happen

3. Fix and iterate quickly
```

### 4. Layout Investigation

When layout breaks:

```markdown
1. Get element info for parent
   → Check dimensions, display mode

2. Get computed styles
   → Check flex/grid properties
   → Check overflow behavior

3. Get child element info
   → Compare expected vs actual sizes

4. Identify constraint causing issue
```

## Complementary Use with Playwright

### Development Phase (Chrome DevTools)

```markdown
You: "The button styling looks wrong"

1. Navigate to page (DevTools)
   → mcp__chrome-devtools__navigate url="http://localhost:3000/page"

2. Inspect button styles
   → mcp__chrome-devtools__get_computed_style selector="button.primary"

3. Find issue: wrong color value applied

4. Fix CSS in code

5. Verify fix visually (DevTools)
   → mcp__chrome-devtools__get_computed_style (confirm new value)
```

### PR Phase (Playwright)

```markdown
Once feature is working:

1. Run through screenshot-eval checklist
   → mcp__playwright__browser_navigate
   → mcp__playwright__browser_console_messages
   → mcp__playwright__browser_network_requests
   → mcp__playwright__browser_take_screenshot

2. Include screenshot proof in PR
```

## Common Use Cases

### "Why isn't my CSS applying?"

```markdown
1. Get computed style
   → mcp__chrome-devtools__get_computed_style selector=".my-class"

2. Look for:
   - Value different from expected → specificity issue
   - Value shows "inherit" or "initial" → rule not matching
   - Value correct but element wrong → targeting issue
```

### "My API call returns wrong data"

```markdown
1. Get network logs
   → mcp__chrome-devtools__get_network_logs

2. Find the API call, check:
   - Request URL correct?
   - Request headers (auth token)?
   - Request body (if POST)?
   - Response status code?
   - Response body contents?
```

### "Something is slow"

```markdown
1. Get performance metrics
   → mcp__chrome-devtools__get_performance_metrics

2. Look for:
   - High CPU usage → expensive computation
   - Memory growing → leak
   - Long paint times → complex rendering
```

### "Element not where expected"

```markdown
1. Get element info
   → mcp__chrome-devtools__get_element_info selector=".element"

2. Check box model:
   - Content size
   - Padding
   - Border
   - Margin

3. Compare with parent container
   → mcp__chrome-devtools__get_element_info selector=".parent"
```

## Setup

Chrome DevTools MCP requires:
1. Chrome browser running with remote debugging enabled
2. MCP server configured in Claude Code settings

The agent will connect to your existing Chrome session, so you can see changes in real-time.

## Related Skills

- `playwright` - For automated testing and PR verification
- `screenshot-eval` - For systematic error checking
- `frontend-dev` - For Astro + React patterns
- `frontend-design` - For design principles
