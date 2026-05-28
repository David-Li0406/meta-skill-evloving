---
name: browser-debug
description: Headless browser debugging for QA failures and visual testing. Use when investigating UI bugs, taking screenshots, or inspecting DOM and network requests.
license: MIT
compatibility: Requires Chrome DevTools MCP plugin for browser automation.
metadata:
  author: shipitsmarter
  version: "1.0"
---

# Browser Debug Skill

Guidelines for debugging QA failures using headless browser tools.

---

## Overview

When Playwright tests fail in CI, you need to investigate what went wrong. This skill covers:

1. **Accessing CI artifacts** - Traces, screenshots, videos
2. **Local reproduction** - Running failed tests locally
3. **Headless debugging** - Using Playwright's debug tools
4. **Visual comparison** - Understanding screenshot failures
5. **Chrome DevTools MCP** - AI-assisted browser debugging

---

## Chrome DevTools MCP Plugin

This project includes the Chrome DevTools MCP plugin for AI-assisted browser debugging. It's configured in `opencode.json` and allows the AI to interact with Chrome DevTools directly.

### Prerequisites

Start Chrome with remote debugging enabled:

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# Linux
google-chrome --remote-debugging-port=9222

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

### Available MCP Tools

Once Chrome is running with debugging enabled, the AI can use these tools:

| Tool | Description |
|------|-------------|
| `devtools_navigate` | Navigate to a URL |
| `devtools_screenshot` | Take a screenshot of the page |
| `devtools_console_eval` | Execute JavaScript in the console |
| `devtools_network_requests` | Get network request history |
| `devtools_console_logs` | Get console log messages |
| `devtools_dom_query` | Query DOM elements |
| `devtools_get_styles` | Get computed styles for an element |

### Development URLs

| Environment | URL | When to use |
|-------------|-----|-------------|
| **Dev server** | `http://localhost:8080` | Default - use with `npm run serve` |
| **Full stack** | `http://localhost` | When testing with docker compose (nginx + all services) |

### Example Usage

Ask the AI to help debug:
- "Navigate to localhost:8080/shipments and take a screenshot"
- "Check the network requests for any failed API calls"
- "Get the console logs to see any JavaScript errors"
- "Query all elements with data-testid containing 'shipment'"

---

## Accessing CI artifacts

### Download test artifacts from GitHub

```bash
# List recent workflow runs
gh run list --workflow=playwright

# Download artifacts from a specific run
gh run download <run-id>

# View artifacts in browser
gh run view <run-id> --web
```

### Artifacts included

| Artifact | Purpose |
|----------|---------|
| `playwright-report/` | HTML test report |
| `test-results/` | Screenshots, videos, traces per test |
| `trace.zip` | Playwright trace files |

---

## Viewing Playwright traces

Traces are the most powerful debugging tool - they capture everything:

```bash
# Open trace viewer
npx playwright show-trace path/to/trace.zip

# Or view the HTML report (includes traces)
npx playwright show-report playwright-report
```

### What traces show

- **Timeline** - Step-by-step action replay
- **DOM snapshots** - Page state at each step
- **Network** - All API requests/responses
- **Console** - Browser console logs
- **Source** - Test code with execution point

---

## Reproducing failures locally

### 1. Set up environment

```bash
cd playwright

# Copy example env file
cp .env.example .env.local

# Fill in credentials
# PLAYWRIGHT_BASE_URL=https://preview.viya.me
# PLAYWRIGHT_ORY_USERNAME=test-user@example.com
# PLAYWRIGHT_ORY_PASSWORD=secret
# ...
```

### 2. Run the specific failing test

```bash
# Run single test file
npx playwright test tests/app-tests/shipment/create.spec.ts

# Run specific test by name
npx playwright test -g "Create basic shipment"

# Run in headed mode to watch
npx playwright test --headed

# Run in debug mode with inspector
npx playwright test --debug
```

### 3. Run with same browser as CI

```bash
# Run on Chromium (matches CI)
npx playwright test --project=chromium

# Run on Firefox
npx playwright test --project=firefox
```

---

## Debug mode

### Using --debug flag

```bash
npx playwright test --debug tests/app-tests/shipment/create.spec.ts
```

This opens:
- **Browser window** - See the test run live
- **Playwright Inspector** - Step through test code

### Inspector controls

| Button | Action |
|--------|--------|
| Step over | Execute next action |
| Resume | Run to next breakpoint |
| Record | Generate new locators |
| Pick locator | Click element to get selector |

### Adding breakpoints in code

```typescript
test('my test', async ({ page }) => {
  await page.goto('/shipments');
  
  // Pause here for debugging
  await page.pause();
  
  await page.click('button');
});
```

---

## UI mode (recommended for development)

```bash
npx playwright test --ui
```

Features:
- **Test explorer** - Run individual tests
- **Watch mode** - Re-run on file changes
- **Time travel** - Step through test execution
- **DOM viewer** - Inspect page at any point

---

## Console logging

### Add console listener to tests

```typescript
test('debugging test', async ({ page }) => {
  // Log all console messages
  page.on('console', (msg) => {
    console.log(`[Browser ${msg.type()}]: ${msg.text()}`);
  });

  // Log errors specifically
  page.on('pageerror', (error) => {
    console.error(`[Page Error]: ${error.message}`);
  });

  await page.goto('/shipments');
});
```

### View network requests

```typescript
page.on('request', (request) => {
  console.log(`>> ${request.method()} ${request.url()}`);
});

page.on('response', (response) => {
  console.log(`<< ${response.status()} ${response.url()}`);
});
```

---

## Screenshot debugging

### Take screenshots at specific points

```typescript
await page.screenshot({ path: 'debug-before-click.png' });
await page.getByTestId('submit').click();
await page.screenshot({ path: 'debug-after-click.png' });
```

### Full page screenshot

```typescript
await page.screenshot({ path: 'full-page.png', fullPage: true });
```

### Screenshot specific element

```typescript
await page.getByTestId('my-component').screenshot({ path: 'component.png' });
```

---

## Common failure patterns

### Element not found

**Symptom:**
```
Error: locator.click: Target element is not attached to the DOM
```

**Debug steps:**
1. Open trace, find the step that failed
2. Check DOM snapshot - is element present?
3. Look for timing issues - element may load later
4. Check if element is in iframe or shadow DOM

**Common fixes:**
```typescript
// Wait for element to be visible
await page.getByTestId('button').waitFor({ state: 'visible' });

// Wait for network idle
await page.waitForLoadState('networkidle');

// Increase timeout for slow elements
await page.getByTestId('button').click({ timeout: 30000 });
```

### Timeout waiting for selector

**Symptom:**
```
Error: Timeout 10000ms exceeded while waiting for getByTestId('element')
```

**Debug steps:**
1. Is the element rendered at all?
2. Does it have the correct data-testid?
3. Is it hidden by v-if/v-show?
4. Is there a loading state blocking it?

### Test passes locally, fails in CI

**Symptom:** Test works on your machine but fails in CI.

**Common causes:**
1. **Timing** - CI is slower, needs longer waits
2. **Data** - Different test data between environments
3. **Authentication** - Session/cookie issues
4. **Screen size** - CI uses different viewport

**Debug steps:**
```bash
# Run with same settings as CI
npx playwright test --retries 2 --workers 3

# Use CI environment
PLAYWRIGHT_BASE_URL=https://preview.viya.me npx playwright test
```

### Flaky tests

**Symptom:** Test sometimes passes, sometimes fails.

**Debug steps:**
1. Run test multiple times: `npx playwright test --repeat-each=10`
2. Look for race conditions in traces
3. Check for animations that affect timing
4. Look for dynamic data that changes between runs

**Common fixes:**
```typescript
// Wait for animations to complete
await page.getByTestId('modal').waitFor({ state: 'visible' });
await page.waitForTimeout(300); // Wait for animation

// Use stable selectors
await page.getByRole('button', { name: 'Submit' }); // Better
await page.locator('.btn-primary'); // Avoid - fragile
```

---

## Debugging checklist

When investigating a failure:

- [ ] Download and open the trace file
- [ ] Identify the exact step that failed
- [ ] Check DOM snapshot at failure point
- [ ] Review network requests - any failures?
- [ ] Check console logs for errors
- [ ] Try reproducing locally with --debug
- [ ] Compare screenshots before/after failure
- [ ] Check if test is flaky (run multiple times)

---

## Quick reference

```bash
# View trace from CI
npx playwright show-trace test-results/*/trace.zip

# View HTML report
npx playwright show-report

# Debug specific test
npx playwright test --debug -g "test name"

# UI mode
npx playwright test --ui

# Run with video
npx playwright test --video on

# Run headed (visible browser)
npx playwright test --headed
```

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **playwright-test** | Writing new tests and test conventions |
| **pr-review** | Overall PR review workflow |
