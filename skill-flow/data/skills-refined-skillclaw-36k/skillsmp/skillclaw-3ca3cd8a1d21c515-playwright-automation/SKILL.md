---
name: playwright-automation
description: Use this skill for browser automation tasks such as navigating web pages, taking screenshots, filling forms, and running tests with Playwright.
---

# Skill body

## When to Use This Skill

- For browser automation tasks including web scraping, testing, and visual verification.
- When you need to interact with web elements, capture screenshots, or validate UI flows.

## Available Tools

| Tool | Purpose |
|------|---------|
| `playwright_navigate` | Navigate to a URL |
| `playwright_screenshot` | Capture the current page or specific elements |
| `playwright_click` | Click an element |
| `playwright_fill` | Fill a form field |
| `playwright_select` | Select an option from a dropdown |
| `playwright_hover` | Hover over an element |
| `playwright_evaluate` | Execute JavaScript in the page context |
| `playwright_get_content` | Retrieve page content or accessibility tree |

## Common Workflows

### Navigate and Screenshot

```javascript
// Navigate to a URL
playwright_navigate({ url: "https://example.com" })

// Take a screenshot
playwright_screenshot({ name: "homepage" })
```

### Form Interaction

```javascript
// Fill a form
playwright_fill({ selector: "#email", value: "test@example.com" })
playwright_fill({ selector: "#password", value: "secret123" })

// Click submit
playwright_click({ selector: "button[type='submit']" })
```

### Validate Page Load

```javascript
// Navigate to a page and check if it loads correctly
playwright_navigate({ url: "https://app.example.com" })
const title = playwright_evaluate({ 
  script: "document.title" 
})
// Verify title matches expected
```

### Check for Console Errors

```javascript
const errors = [];
page.on('console', (msg) => {
  if (msg.type() === 'error') errors.push(msg.text());
});
await playwright_navigate({ url: "http://localhost:3000" });
```

### Extract Data

```javascript
playwright_evaluate({
  script: `
    Array.from(document.querySelectorAll('.item'))
      .map(el => ({
        title: el.querySelector('.title')?.textContent,
        price: el.querySelector('.price')?.textContent
      }))
  `
})
```

## Selector Strategies

| Priority | Selector Type | Example |
|----------|---------------|---------|
| 1 | data-testid | `[data-testid="submit-btn"]` |
| 2 | role | `button[name="Submit"]` |
| 3 | text | `text="Submit"` |
| 4 | CSS | `.btn-primary` |
| 5 | XPath | `//button[@type="submit"]` |

**Prefer** `data-testid` for stability in tests.

## Output

This skill provides a comprehensive approach to browser automation, allowing for effective testing, validation, and interaction with web applications.