---
name: webapp-testing
description: Web application testing skill using Antigravity browser and Playwright CLI. Use for E2E testing, visual debugging, interaction testing, accessibility checks, and deep audit strategies. Supports both live browser interaction via browser_subagent and headless automated testing via Playwright scripts.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, browser_subagent
---

# Web App Testing

> Discover and test everything. Leave no route untested.

---

## 🔧 Testing Tools Available

This skill provides **two testing approaches** based on the scenario:

### 1. Antigravity Browser (browser_subagent)
**Use for:** Live interaction, visual debugging, complex user flows, authentication testing

```yaml
when_to_use:
  - Need to see what's happening in real-time
  - Testing login/authentication flows
  - Debugging visual issues
  - Recording user interactions
  - Testing with existing session/cookies
  - Complex multi-step flows

capabilities:
  - Click, type, navigate interactively
  - Capture screenshots and recordings
  - Interact with authenticated sessions
  - Visual inspection of page state
  - Real-time debugging
```

**Usage Pattern:**
```
browser_subagent:
  TaskName: "Testing Login Flow"
  Task: |
    1. Navigate to https://example.com/login
    2. Enter email "test@example.com" in the email field
    3. Enter password "testpass" in the password field
    4. Click the "Sign In" button
    5. Wait for redirect to dashboard
    6. Capture screenshot of final state
    7. Report: page title, URL, any error messages visible
  RecordingName: "login_flow_test"
```

### 2. Playwright CLI Scripts
**Use for:** Automated headless testing, CI/CD, batch testing, accessibility audits

```yaml
when_to_use:
  - Automated regression testing
  - CI/CD pipeline integration
  - Performance metrics collection
  - Accessibility checks
  - Batch URL testing
  - Headless server environments

capabilities:
  - Headless browser automation
  - JSON output for parsing
  - Screenshot capture
  - Element counting
  - Performance timing
  - Accessibility checks
```

**Scripts Available:**

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/playwright_runner.py` | Basic browser test | `python scripts/playwright_runner.py <url>` |
| | With screenshot | `python scripts/playwright_runner.py <url> --screenshot` |
| | Accessibility check | `python scripts/playwright_runner.py <url> --a11y` |
| `scripts/with_server.py` | Test with local dev server | `python scripts/with_server.py <start_cmd> <url>` |

**Requires:** `pip install playwright && playwright install chromium`

---

## 🎯 Decision Matrix: Which Tool to Use?

| Scenario | Tool | Why |
|----------|------|-----|
| Debug visual bug | **browser_subagent** | See issue in real-time |
| Test login flow | **browser_subagent** | Handle auth complexity |
| Record user flow | **browser_subagent** | Creates WebP recording |
| CI/CD testing | **Playwright CLI** | Headless, scriptable |
| Batch URL audit | **Playwright CLI** | JSON output, fast |
| Accessibility audit | **Playwright CLI** | Structured a11y report |
| Performance metrics | **Playwright CLI** | Timing data extraction |
| Investigate console errors | **browser_subagent** | Real-time console access |
| Test authenticated pages | **browser_subagent** | Browser has session |
| Screenshot comparison | **Playwright CLI** | Consistent headless capture |

---

## 📋 Testing Workflows

### Workflow 1: Visual Bug Investigation

```yaml
steps:
  1. Use browser_subagent to navigate to the affected page
  2. Observe the visual issue
  3. Inspect element states
  4. Capture screenshot with recording
  5. Test fix by interacting with the page
  6. Document findings
```

**Example:**
```
browser_subagent:
  TaskName: "Investigating Button Bug"
  Task: |
    1. Navigate to https://app.example.com/dashboard
    2. Find the "Submit" button
    3. Check if it has correct styling (should be blue, rounded)
    4. Click the button and observe behavior
    5. Report: button visibility, click response, any errors
  RecordingName: "button_bug_investigation"
```

### Workflow 2: E2E Flow Testing

```yaml
steps:
  1. Use browser_subagent for complex flows with auth
  2. Navigate through the entire user journey
  3. Verify each step completes correctly
  4. Capture recording for documentation
```

**Example:**
```
browser_subagent:
  TaskName: "Testing Checkout Flow"
  Task: |
    1. Navigate to https://store.example.com
    2. Add product to cart (click "Add to Cart" button)
    3. Go to cart page
    4. Click "Checkout"
    5. Fill shipping form with test data
    6. Click "Place Order"
    7. Verify order confirmation page appears
    8. Report: order number if visible, final page URL
  RecordingName: "checkout_flow_test"
```

### Workflow 3: Automated Health Check

```bash
# Use Playwright for headless automated checks
python .agent/skills/webapp-testing/scripts/playwright_runner.py https://example.com --screenshot

# Output: JSON with page health, element counts, performance metrics
```

### Workflow 4: Accessibility Audit

```bash
# Use Playwright for structured a11y report
python .agent/skills/webapp-testing/scripts/playwright_runner.py https://example.com --a11y

# Output: JSON with alt text coverage, heading structure, form labels
```

---

## 🔍 Deep Audit Approach

### Discovery First

| Target | How to Find |
|--------|-------------|
| Routes | Scan app/, pages/, router files |
| API endpoints | Grep for HTTP methods |
| Components | Find component directories |
| Features | Read documentation |

### Systematic Testing

1. **Map** - List all routes/APIs
2. **Scan** - Verify they respond (Playwright CLI batch)
3. **Test** - Cover critical paths (browser_subagent for complex flows)

---

## 🏗️ Testing Pyramid

```
        /\          E2E (Few)
       /  \         Critical user flows → browser_subagent
      /----\
     /      \       Integration (Some)
    /--------\      API, data → Playwright CLI
   /          \
  /------------\    Component (Many)
                    Individual UI → Unit tests
```

---

## ✅ E2E Best Practices

| Practice | Implementation |
|----------|----------------|
| Use data-testid | Stable selectors for both tools |
| Wait for elements | browser_subagent waits automatically |
| Clean state | Start fresh for each test |
| Test user behavior | Not implementation details |
| Record evidence | Use RecordingName for documentation |

---

## 📸 browser_subagent Output Guidelines

When using browser_subagent, always specify in Task:
1. **What to navigate to** (URL)
2. **What to interact with** (specific elements)
3. **What to capture** (screenshots, final state)
4. **What to report** (specific data points to return)
5. **When to stop** (clear completion criteria)

**Good Task Description:**
```
1. Navigate to https://app.example.com/settings
2. Click the "Profile" tab
3. Verify the profile form is visible
4. Report: page title, form field count, any error banners visible
Return: SUCCESS if form loaded, FAILURE with error message if not
```

**Bad Task Description:**
```
Test the settings page
```

---

## 🔧 Playwright CLI Output

The `playwright_runner.py` script returns JSON:

```json
{
  "url": "https://example.com",
  "timestamp": "2024-01-21T10:30:00",
  "status": "success",
  "page": {
    "title": "Example Domain",
    "url": "https://example.com/",
    "status_code": 200
  },
  "health": {
    "loaded": true,
    "has_title": true,
    "has_h1": true,
    "has_links": true
  },
  "performance": {
    "dom_content_loaded": 450,
    "load_complete": 890
  },
  "elements": {
    "links": 5,
    "buttons": 2,
    "inputs": 1,
    "forms": 0
  },
  "screenshot": "/tmp/maestro_screenshots/screenshot_20240121_103000.png"
}
```

---

## 🚫 Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Use browser_subagent for batch tests | Use Playwright CLI for batch |
| Use Playwright for auth flows | Use browser_subagent for auth |
| Vague task descriptions | Specific step-by-step instructions |
| Skip recording name | Always name recordings descriptively |
| Ignore console errors | Check and report errors |
| Test implementation | Test user behavior |

---

## 📊 Integration with Debug Workflow

When `/debug` invokes this skill:

1. **For visual bugs**: Use browser_subagent to see the issue
2. **For automated checks**: Use Playwright CLI for health checks
3. **For recording evidence**: Set RecordingName to capture proof
4. **For accessibility**: Use Playwright --a11y flag

---

## 🚀 Quick Reference

| Task | Method |
|------|--------|
| See bug live | `browser_subagent` |
| Test login | `browser_subagent` |
| Record flow | `browser_subagent` with RecordingName |
| Batch health check | `playwright_runner.py <url>` |
| Get screenshot | `playwright_runner.py <url> --screenshot` |
| A11y audit | `playwright_runner.py <url> --a11y` |
| Test with dev server | `with_server.py <cmd> <url>` |

---

> **Remember:** browser_subagent for interaction & debugging, Playwright CLI for automation & CI.