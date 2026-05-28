---
name: playwright
description: Browser automation via Playwright MCP. Use for verification, browsing, web scraping, testing, screenshots, and all browser interactions.
---

# Playwright Skill

## When to Load This Skill

- Browser automation tasks
- Visual verification of web applications
- Web scraping and data extraction
- Screenshot capture
- End-to-end testing workflows
- Form filling and interaction testing

---

## Available MCP Tools

The `playwright` MCP provides these tools:

| Tool | Purpose |
|------|---------|
| `playwright_navigate` | Go to a URL |
| `playwright_screenshot` | Capture the current page |
| `playwright_click` | Click an element |
| `playwright_fill` | Fill a form field |
| `playwright_select` | Select dropdown option |
| `playwright_hover` | Hover over element |
| `playwright_evaluate` | Run JavaScript in page |

---

## Common Workflows

### Navigate and Screenshot

```javascript
// Navigate to URL
playwright_navigate({ url: "https://example.com" })

// Take screenshot
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

### Wait for Elements

```javascript
// Navigate and wait for content
playwright_navigate({ url: "https://example.com" })
playwright_evaluate({ 
  script: "document.querySelector('.loaded')?.textContent" 
})
```

---

## Selector Strategies

| Priority | Selector Type | Example |
|----------|---------------|---------|
| 1 | data-testid | `[data-testid="submit-btn"]` |
| 2 | role | `button[name="Submit"]` |
| 3 | text | `text="Submit"` |
| 4 | CSS | `.btn-primary` |
| 5 | XPath | `//button[@type="submit"]` |

**Prefer** `data-testid` for stability.

---

## Verification Patterns

### Check Page Loaded

```javascript
playwright_navigate({ url: "https://app.example.com" })
const title = playwright_evaluate({ 
  script: "document.title" 
})
// Verify title matches expected
```

### Check Element Visible

```javascript
playwright_evaluate({
  script: `
    const el = document.querySelector('.success-message');
    el && el.offsetParent !== null
  `
})
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

---

## Best Practices

1. **Always screenshot** after important actions for evidence
2. **Use explicit waits** rather than arbitrary delays
3. **Prefer stable selectors** (data-testid > CSS class)
4. **Handle navigation** - wait for page load before interacting
5. **Clean up** - close browsers when done

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Element not found | Selector wrong or element not rendered | Wait for element, check selector |
| Timeout | Page too slow | Increase timeout, check network |
| Navigation failed | Invalid URL or network error | Verify URL, check connectivity |
