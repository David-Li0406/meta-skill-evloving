---
name: web-application-testing
description: Use this skill to interact with and test local web applications using Playwright, ensuring frontend functionality and debugging UI behavior.
---

# Web Application Testing Skill

This skill enables comprehensive testing and debugging of local web applications using Playwright automation.

## When to Use This Skill

Use this skill when you need to:
- Test frontend functionality in a real browser
- Verify UI behavior and interactions
- Debug web application issues
- Capture screenshots for documentation or debugging
- Inspect browser console logs
- Validate form submissions and user flows
- Check responsive design across viewports

## Prerequisites

- Node.js installed on the system
- A locally running web application (or accessible URL)
- Playwright will be installed automatically if not present

## Core Capabilities

### 1. Browser Automation
- Navigate to URLs
- Click buttons and links
- Fill form fields
- Select dropdowns
- Handle dialogs and alerts

### 2. Verification
- Assert element presence
- Verify text content
- Check element visibility
- Validate URLs
- Test responsive behavior

### 3. Debugging
- Capture screenshots
- View console logs
- Inspect network requests
- Debug failed tests

## Project Configuration

### Installation

```bash
# Install Playwright (if not already installed)
pnpm add -D -w @playwright/test

# Install browsers
pnpm exec playwright install
```

### Helper Scripts

- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is absolutely necessary.

## Decision Tree: Choosing Your Approach

```text
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Usage Examples

### Example 1: Basic Navigation Test
```javascript
// Navigate to a page and verify title
await page.goto('http://localhost:4200');
const title = await page.title();
console.log('Page title:', title);
```

### Example 2: Form Interaction
```javascript
// Fill out and submit a form
await page.fill('#username', 'demo@test.com');
await page.fill('#password', '123123');
await page.click('button[type="submit"]');
await page.waitForURL('**/dashboard');
```

### Example 3: Screenshot Capture
```javascript
// Capture a screenshot for debugging
await page.screenshot({ path: 'debug.png', fullPage: true });
```

## Guidelines

1. **Always verify the app is running** - Check that the local server is accessible before running tests.
2. **Use explicit waits** - Wait for elements or navigation to complete before interacting.
3. **Capture screenshots on failure** - Take screenshots to help debug issues.
4. **Clean up resources** - Always close the browser when done.
5. **Handle timeouts gracefully** - Set reasonable timeouts for slow operations.
6. **Test incrementally** - Start with simple interactions before complex flows.
7. **Use selectors wisely** - Prefer data-testid or other stable selectors for reliability.