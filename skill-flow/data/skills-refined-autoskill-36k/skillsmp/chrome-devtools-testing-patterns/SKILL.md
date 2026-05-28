---
name: chrome-devtools-testing-patterns
description: Standardize chrome-devtools usage for testing scenarios with best practices for browser automation, common interaction patterns, testing workflow integration, and robust error handling
license: MIT
compatibility: opencode
metadata:
  audience: developers, testers, qa-engineers
  domain: testing, browser-automation
  workflow: e2e-testing, functional-testing, accessibility-testing
  updated: "2025-01"
  keywords: chrome-devtools, testing, automation, e2e, browser-testing
---

## What I do

I help you standardize chrome-devtools usage patterns for testing scenarios in the GoPayShortcuts project. I provide:

- **Best practices for browser automation testing** - Establish reliable, maintainable testing patterns using chrome-devtools tools
- **Common interaction patterns** - Standardized approaches for page setup, navigation, element interaction, and verification
- **Testing workflow integration** - Seamless integration with functional, E2E, and accessibility testing processes
- **Practical examples and templates** - Ready-to-use patterns for scrolling, form filling, clicking, and waiting strategies
- **Error handling and troubleshooting** - Robust patterns for handling chrome-devtools failures and debugging test issues

## When to use me

Load this skill when:
- Writing or maintaining E2E tests that use chrome-devtools for browser automation
- Setting up new testing workflows that require browser interaction patterns
- Debugging failing browser tests or chrome-devtools operations
- Standardizing testing approaches across the team's automation suite
- Implementing accessibility testing using chrome-devtools capabilities

## Best practices for browser automation testing

### Page Setup and Configuration
- **Always select a page context** before operations using `chrome-devtools_select_page`
- **Set appropriate timeouts** for operations that may take time (navigation, waiting)
- **Configure network conditions** if testing under specific constraints (slow 3G, offline)
- **Resize page** to consistent dimensions for screenshot comparisons
- **Take snapshots** before interactions to get current element UIDs

### Reliable Element Interaction
- **Use snapshots for element identification** - Always take a fresh snapshot before selecting elements by UID
- **Prefer semantic selectors** over fragile XPath/CSS when possible
- **Wait for elements** before interaction using `chrome-devtools_wait_for` or evaluate scripts
- **Verify element state** before actions (enabled, visible, not obscured)

### Verification and Assertions
- **Use evaluate scripts** for complex DOM state checks rather than multiple tool calls
- **Capture screenshots** for visual regression testing
- **Check console messages** for JavaScript errors during test execution
- **Monitor network requests** to verify API calls and resource loading

## Common patterns

### Page Navigation Pattern
```javascript
// Pattern: Navigate to page and wait for load
chrome-devtools_navigate_page(type="url", url="https://example.com")
chrome-devtools_wait_for(text="Expected content")
chrome-devtools_take_snapshot()  // Get current element state
```

### Form Interaction Pattern
```javascript
// Pattern: Fill form and submit
chrome-devtools_take_snapshot()
chrome-devtools_fill_form(elements=[
  {"uid": "username-field", "value": "testuser"},
  {"uid": "password-field", "value": "testpass"}
])
chrome-devtools_click(uid="submit-button")
chrome-devtools_wait_for(text="Login successful")
```

### Element Verification Pattern
```javascript
// Pattern: Verify element exists and has expected state
chrome-devtools_evaluate_script(function=() => {
  const element = document.querySelector('#target-element');
  return element && element.textContent === 'Expected text';
})
```

## Integration with testing workflows

### Functional Testing Integration
- Use chrome-devtools for UI component testing within larger test suites
- Combine with assertion libraries for DOM state verification
- Integrate with existing test runners (Jest, Vitest) using tool calls

### E2E Testing Workflow
```javascript
// Example E2E flow
1. chrome-devtools_new_page(url="https://app.gopayshortcuts.com")
2. chrome-devtools_fill_form(elements=[...])  // Login
3. chrome-devtools_click(uid="dashboard-link")
4. chrome-devtools_wait_for(text="Welcome back")
5. chrome-devtools_take_screenshot(filePath="dashboard.png")  // Verification
6. chrome-devtools_close_page()
```

### Accessibility Testing Integration
- Use `chrome-devtools_performance_start_trace` for accessibility audits
- Check console messages for accessibility violations
- Evaluate scripts to test keyboard navigation and screen reader compatibility

## Examples

### Scrolling and Element Interaction
```javascript
// Scroll to element and click
chrome-devtools_evaluate_script(function=(element) => {
  element.scrollIntoView({ behavior: 'smooth' });
  return element.getBoundingClientRect();
}, args=[{"uid": "target-element"}])
chrome-devtools_click(uid="target-element")
```

### Form Filling with Validation
```javascript
// Fill form with validation checks
chrome-devtools_fill(uid="email-field", value="user@example.com")
chrome-devtools_evaluate_script(function=() => {
  const email = document.getElementById('email-field');
  return email.checkValidity();  // HTML5 validation
})
chrome-devtools_fill(uid="password-field", value="securePass123")
chrome-devtools_click(uid="register-button")
```

### Waiting for Dynamic Content
```javascript
// Wait for AJAX-loaded content
chrome-devtools_click(uid="load-more-button")
chrome-devtools_wait_for(text="New content loaded")
chrome-devtools_evaluate_script(function=() => {
  return document.querySelectorAll('.dynamic-item').length > 5;
})
```

## Error handling and troubleshooting

### Common Failure Patterns

**Element not found errors:**
- **Cause**: Page not fully loaded, dynamic content not rendered
- **Solution**: Add `chrome-devtools_wait_for` before taking snapshot, increase timeout
- **Prevention**: Use semantic selectors, avoid brittle XPath

**Timeout errors:**
- **Cause**: Network slow, page heavy, animations not complete
- **Solution**: Increase timeout parameter, wait for specific elements
- **Prevention**: Set realistic timeouts based on page complexity

**Stale element references:**
- **Cause**: Page updated after snapshot taken
- **Solution**: Take fresh snapshot before each interaction
- **Prevention**: Minimize time between snapshot and action

### Debugging Techniques

**Console logging:**
```javascript
chrome-devtools_list_console_messages()
chrome-devtools_get_console_message(msgid=0)
```

**Network inspection:**
```javascript
chrome-devtools_list_network_requests()
chrome-devtools_get_network_request(reqid=0)
```

**Visual debugging:**
```javascript
chrome-devtools_take_screenshot(filePath="debug-state.png")
chrome-devtools_take_snapshot(verbose=true)
```

**Performance analysis:**
```javascript
chrome-devtools_performance_start_trace(reload=true, autoStop=true)
# After test completes, analyze trace for bottlenecks
```

### Recovery Patterns

**Retry failed operations:**
```javascript
# Implement retry logic in your test framework
def retry_chrome_operation(operation, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            operation()
            break
        except Exception as e:
            if attempt == max_attempts - 1:
                raise e
            time.sleep(1)
```

**Clean up on failure:**
```javascript
# Always close pages in finally blocks
try:
    # test operations
finally:
    chrome-devtools_close_page()
```

## Reference

- **Chrome DevTools Protocol**: https://chromedevtools.github.io/devtools-protocol/
- **Related skills**: 
  - [sveltekit-fullstack-development](../sveltekit-fullstack-development/SKILL.md) - For SvelteKit testing integration
  - [testing-implementation-specialist](../testing-implementation-specialist/SKILL.md) - For comprehensive testing strategies
- **GoPayShortcuts testing docs**: See project README for testing setup