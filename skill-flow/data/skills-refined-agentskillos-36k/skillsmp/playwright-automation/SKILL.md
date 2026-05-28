---
name: playwright-automation
description: Browser automation via Playwright MCP - screenshots, interactions, DOM inspection
requires_mcp: playwright
impact: HIGH
impactMetrics:
  - "E2E testing without test framework setup"
  - "Visual debugging via screenshots"
  - "DOM inspection via accessibility tree"
categories:
  - name: "Navigation"
    impact: HIGH
  - name: "Screenshots"
    impact: HIGH
  - name: "Form Interaction"
    impact: MEDIUM
  - name: "DOM Inspection"
    impact: MEDIUM
  - name: "JavaScript Evaluation"
    impact: LOW
allowed-tools:
  - mcp__playwright__*
---

# Playwright Browser Automation

Control Chrome/Firefox/WebKit browsers for UI/UX work, testing, and debugging.

## MCP Server

This skill uses the `@playwright/mcp` server configured in `.mcp.json`.

## Available Tools

| Tool | Purpose |
|------|---------|
| `playwright_navigate` | Go to a URL |
| `playwright_screenshot` | Capture page or element screenshot |
| `playwright_click` | Click an element |
| `playwright_fill` | Fill form inputs |
| `playwright_select` | Select from dropdowns |
| `playwright_hover` | Hover over elements |
| `playwright_evaluate` | Execute JavaScript |
| `playwright_get_content` | Get page content/accessibility tree |

## Usage Patterns

### Take Screenshot
```
Navigate to https://example.com and take a full-page screenshot
```

### Form Interaction
```
Fill the email field with "test@example.com" and click Submit
```

### DOM Inspection
```
Get the accessibility tree of the page and find all buttons
```

### Visual Testing
```
Navigate to /dashboard, take screenshot, compare with baseline
```

## Integration with Other Skills

- **web-design-guidelines** - Validate UI against guidelines after screenshot
- **react-best-practices** - Check React app patterns via DOM inspection
- **test** workflow - E2E test generation and execution

## MCP Tool Details

### playwright_navigate
Navigate to a URL. Waits for page load.
```
playwright_navigate(url="https://example.com")
```

### playwright_screenshot
Capture full page or element screenshot.
```
playwright_screenshot()                    # Full page
playwright_screenshot(selector=".header")  # Element only
playwright_screenshot(fullPage=true)       # Include scrolled content
```

### playwright_click
Click an element by selector or accessibility label.
```
playwright_click(selector="button[type=submit]")
playwright_click(text="Sign In")
```

### playwright_fill
Fill form inputs.
```
playwright_fill(selector="input[name=email]", value="test@example.com")
playwright_fill(selector="#password", value="secret123")
```

### playwright_select
Select from dropdown menus.
```
playwright_select(selector="select#country", value="US")
```

### playwright_hover
Hover over elements (for tooltips, menus).
```
playwright_hover(selector=".dropdown-trigger")
```

### playwright_evaluate
Execute JavaScript in page context.
```
playwright_evaluate(script="document.querySelectorAll('button').length")
playwright_evaluate(script="localStorage.getItem('token')")
```

### playwright_get_content
Get page content or accessibility tree.
```
playwright_get_content()                   # HTML content
playwright_get_content(format="a11y")      # Accessibility tree
```

## Best Practices

1. **Use accessibility tree for element selection** - more stable than CSS selectors
2. **Take screenshots before/after interactions** - for debugging
3. **Use `playwright_evaluate` for complex DOM queries** - when selectors aren't enough
4. **Chain with web-design-guidelines** - for UI audits after screenshots
5. **Wait between actions** - some interactions need time to settle

## Example Workflows

### Login Flow Test
```
1. playwright_navigate(url="https://app.example.com/login")
2. playwright_screenshot()  # Before state
3. playwright_fill(selector="#email", value="test@example.com")
4. playwright_fill(selector="#password", value="password123")
5. playwright_click(text="Sign In")
6. playwright_screenshot()  # After state - verify dashboard
```

### UI Audit
```
1. playwright_navigate(url="https://example.com")
2. playwright_screenshot(fullPage=true)
3. playwright_get_content(format="a11y")
4. [Apply web-design-guidelines to the accessibility tree]
```

### Form Validation Testing
```
1. playwright_navigate(url="/signup")
2. playwright_click(text="Submit")  # Submit empty form
3. playwright_screenshot()  # Capture validation errors
4. playwright_get_content()  # Check error messages in DOM
```

## When to Use MCP vs CLI

| Use Case | Recommendation |
|----------|----------------|
| Quick visual check | MCP - faster setup |
| Full E2E suite | CLI (npx playwright test) |
| Interactive debugging | MCP - step through actions |
| CI/CD pipeline | CLI - better reporting |
| Ad-hoc testing | MCP - no test file needed |
| Screenshot comparison | MCP + manual review |
