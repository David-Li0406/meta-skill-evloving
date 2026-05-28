# Browser Testing with Playwright MCP

## Available Commands

```javascript
// Navigate to URL
browser.navigate("http://localhost:3000/path")

// Check for element
browser.querySelector(".class-name")

// Get console logs
browser.getConsoleLogs()

// Take screenshot
browser.screenshot()

// Click element
browser.click("selector")

// Type into input
browser.type("selector", "text")

// Wait for element
browser.waitFor("selector", timeout)
```

## Common Test Patterns

### Visual Verification

```markdown
1. Navigate: `browser.navigate("http://localhost:3000/dashboard")`
2. Wait for load: `browser.waitFor(".dashboard-content")`
3. Screenshot: `browser.screenshot()`
4. Check console: `browser.getConsoleLogs()` — verify no errors
```

### Form Interaction

```markdown
1. Navigate to form page
2. Fill fields:
   - `browser.type("#email", "test@example.com")`
   - `browser.type("#password", "secure123")`
3. Submit: `browser.click("button[type=submit]")`
4. Verify: Check success message or redirect
```

### Data Display

```markdown
1. Navigate to data page
2. Wait for data: `browser.waitFor("[data-testid='data-table']")`
3. Verify content: Check expected text/elements present
4. Test interactions: sorting, filtering, pagination
```

## Integration with Test Phases

### Phase 4 Browser Tests

Use Playwright MCP for:
- Visual verification after UI changes
- Form interaction testing
- Console error detection
- Screenshot evidence collection

### When to Use

- After ANY UI change
- When testing user workflows
- For visual regression checks
- To collect evidence of test completion

## Troubleshooting

**Element not found**: Wait longer or check selector
**Console errors**: Investigate before marking pass
**Screenshots**: Always capture for evidence
**Network issues**: Check browser network tab
