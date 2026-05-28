---
name: playwright
description: Automate browser interactions with Playwright MCP. Use for web scraping, form filling, testing, or any browser-based automation tasks.
compatibility: opencode
metadata:
  workflow: browser-automation
---

## What I do

- Automate browser interactions for web scraping and testing
- Fill forms, click buttons, and navigate pages
- Capture screenshots and page state
- Handle authentication and session persistence

## When to use me

Use this when you need to interact with web pages, automate browser-based tasks, fill forms, scrape content, or test web applications.

## Tool Preference

**Prefer `playwright_browser_run_code` for batch operations** - it executes multiple Playwright operations in a single call, reducing round-trips.

```javascript
// Good: Single call for multiple operations
await page.goto('https://example.com');
await page.fill('#email', 'user@test.com');
await page.fill('#password', 'secret');
await page.click('button[type="submit"]');

// Avoid: Multiple individual tool calls
// playwright_browser_navigate -> playwright_browser_type -> playwright_browser_click
```

## When to Use Individual Tools

- **Snapshot needed**: Use `playwright_browser_snapshot` to read page state for decision-making
- **Dynamic interaction**: When next action depends on page response
- **Debugging**: Step-by-step execution for troubleshooting

## Screenshot Rule

After any screen-modifying action, call `playwright_browser_take_screenshot`:

```
filename: "latest.png"  # ALWAYS use this unless user specifies another name
```

## Screen-Changing Tools

These tools modify the visible page and require screenshots:

- `playwright_browser_navigate`, `playwright_browser_click`, `playwright_browser_type`
- `playwright_browser_fill_form`, `playwright_browser_select_option`, `playwright_browser_press_key`
- `playwright_browser_handle_dialog`, `playwright_browser_file_upload`
- `playwright_browser_tabs` (select/new), `playwright_browser_run_code`

## Common Patterns

```
# Batch operation with screenshot
playwright_browser_run_code(code) -> playwright_browser_take_screenshot(filename: "latest.png")

# Individual operation with screenshot
playwright_browser_click(element, ref) -> playwright_browser_take_screenshot(filename: "latest.png")
```

## Best Practices

1. **Use snapshots for state**: Call `playwright_browser_snapshot` to understand current page state
2. **Batch when possible**: Combine multiple actions in `playwright_browser_run_code`
3. **Screenshot after changes**: Always capture visual state after modifications
4. **Handle errors gracefully**: Check for element existence before interacting
