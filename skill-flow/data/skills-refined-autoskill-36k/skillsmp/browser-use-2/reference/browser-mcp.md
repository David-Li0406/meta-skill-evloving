# Browser MCP Reference

Complete reference for Browser MCP (Playwright-based browser automation).

## Overview

Browser MCP provides browser automation via Playwright. It operates independently of the user's browser, making it ideal for isolated testing with clean state.

## Prerequisites

1. Browser MCP server running (configured in MCP settings)
2. Dev server running (`pnpm dev` or `npm run dev`)

## Core Tools

### Navigation

```
mcp__browsermcp__browser_navigate
  url: <string>        # Full URL to navigate to
```

```
mcp__browsermcp__browser_go_back
# No parameters - goes back in history
```

```
mcp__browsermcp__browser_go_forward
# No parameters - goes forward in history
```

### Page Inspection

```
mcp__browsermcp__browser_snapshot
# No parameters
# Returns accessibility tree with element refs
```

This is the primary way to discover elements on the page. Returns refs like `ref="button 'Submit'"` that can be used for interaction.

### Screenshots

```
mcp__browsermcp__browser_screenshot
# No parameters - captures current page
```

### Element Interaction

```
mcp__browsermcp__browser_click
  element: <string>    # Human-readable description
  ref: <string>        # Exact ref from snapshot
```

```
mcp__browsermcp__browser_type
  element: <string>    # Human-readable description
  ref: <string>        # Exact ref from snapshot
  text: <string>       # Text to type
  submit: <boolean>    # Press Enter after typing
```

```
mcp__browsermcp__browser_hover
  element: <string>    # Human-readable description
  ref: <string>        # Exact ref from snapshot
```

```
mcp__browsermcp__browser_select_option
  element: <string>    # Human-readable description
  ref: <string>        # Exact ref from snapshot
  values: [<string>]   # Options to select
```

### Keyboard

```
mcp__browsermcp__browser_press_key
  key: <string>        # Key name: "Enter", "ArrowDown", "a"
```

### Waiting

```
mcp__browsermcp__browser_wait
  time: <number>       # Seconds to wait
```

### Console

```
mcp__browsermcp__browser_get_console_logs
# No parameters - returns all console messages
```

## Common Patterns

### Navigate and Verify

```
1. browser_navigate url="http://localhost:3001/dashboard"
2. browser_wait time=2
3. browser_screenshot
4. browser_get_console_logs
```

### Element Discovery

```
1. browser_navigate to page
2. browser_snapshot
3. Find element refs in accessibility tree
4. Use refs for click/type operations
```

### Form Submission

```
1. browser_navigate to form page
2. browser_snapshot to get refs
3. browser_type into each field (ref from snapshot)
4. browser_click submit button (ref from snapshot)
5. browser_wait for response
6. browser_screenshot result
7. browser_get_console_logs
```

### Workflow Testing

```
1. browser_navigate to starting point
2. For each step:
   a. browser_snapshot
   b. browser_click or browser_type
   c. browser_wait if needed
3. browser_screenshot at key points
4. browser_get_console_logs at end
```

### Dropdown Selection

```
1. browser_snapshot to find select element
2. browser_select_option with ref and values
3. browser_screenshot to verify
```

## Best Practices

1. **Snapshot before interacting** - Always get fresh refs
2. **Wait for page loads** - Use browser_wait after navigation
3. **Check console after actions** - Catch errors early
4. **Screenshot for evidence** - Capture state at key points
5. **Use exact refs** - Copy refs exactly from snapshot

## Accessibility Tree Format

The snapshot returns an accessibility tree like:

```
- document
  - navigation
    - link "Home" [ref="link 'Home'"]
    - link "Dashboard" [ref="link 'Dashboard'"]
  - main
    - heading "Welcome" [ref="heading 'Welcome'"]
    - form
      - textbox "Email" [ref="textbox 'Email'"]
      - textbox "Password" [ref="textbox 'Password'"]
      - button "Sign In" [ref="button 'Sign In'"]
```

Use the `ref` values exactly as shown for click/type operations.

## Troubleshooting

### Element not found
- Take a fresh snapshot - page state may have changed
- Check if element is visible (may be hidden or in different view)
- Wait for page to fully load

### Page not loading
- Verify dev server is running
- Check URL is correct (including port)
- Try browser_wait before snapshot

### Console errors not showing
- Console logs are cleared on navigation
- Call browser_get_console_logs immediately after the action you want to check

### Interaction not working
- Verify the ref is exactly as shown in snapshot
- Some elements may require hover before click
- Interactive elements may be dynamically loaded - wait and re-snapshot

## Limitations

- No access to user's logged-in sessions (isolated browser)
- No GIF recording capability
- No network request monitoring
- No JavaScript execution in page context
- Single browser instance (no multi-tab)

For these capabilities, use Claude in Chrome instead.
