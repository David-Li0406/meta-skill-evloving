---
name: playwright
description: Playwright browser automation and E2E testing. Use for browser testing, screenshots, debugging, MCP tools, page objects, and visual verification.
context: fork
---

# Playwright Skill

**Activation:** E2E testing, browser automation, debugging, screenshots
**Version:** 1.57.0

## ⚠️ CRITICAL: No Mocking in E2E Tests

```
┌─────────────────────────────────────────────────────────────┐
│  E2E TESTS MUST HIT REAL BACKEND                            │
├─────────────────────────────────────────────────────────────┤
│  ❌ NEVER use page.route() to mock API responses            │
│  ❌ NEVER use route.fulfill() with fake data                │
│  ✅ ALWAYS test against real Docker services                │
│  ✅ ALWAYS verify real database changes                     │
└─────────────────────────────────────────────────────────────┘
```

**Why?** Mocked tests create false confidence. A mocked test can pass while the real feature is broken (e.g., login pointing to wrong port slipped through because tests mocked the auth endpoint).

> **Runs on HOST (Exception to Container-First Rule)**
>
> E2E tests run on the host because they need browser control:
> ```bash
> just test-e2e-quick          # Quick E2E (< 1 min, for commits)
> just test-e2e-full           # Full E2E (for pre-PR)
> pytest -m e2e tests/e2e/python/  # All E2E tests
> ```
> This is an intentional exception. See `.claude/rules/container-execution.md`.

## Timeout Configuration (M3 Max Optimized)

**CRITICAL:** This configuration uses aggressive timeouts to prevent tests from hanging.

| Timeout Type | Local (M3 Max) | CI |
|--------------|----------------|-----|
| Test timeout | 5s | 30s |
| Action timeout | 2s | 10s |
| Navigation timeout | 3s | 15s |
| Expect timeout | 2s | 10s |
| Global timeout | 2 min | 10 min |

Tests will **fail fast** if services are down. Global setup verifies services before tests run.

## Pre-Flight Health Check

Before running any test, the global setup verifies:
1. Backend HTTP endpoint (`/health`) responds
2. Frontend HTTP endpoint responds
3. Browser can launch and navigate

If any check fails, tests abort with clear troubleshooting instructions.

## Overview

Playwright is used for:
1. **E2E Testing** - Frontend integration tests
2. **Pipeline Rendering** - HTML to PNG for comparison images
3. **Debugging** - Visual browser automation

## MCP Integration

This project has Playwright MCP available for **automated testing and PR verification**.

**For interactive debugging during development, use Chrome DevTools MCP instead** - see `chrome-devtools` skill.

| Task | Tool |
|------|------|
| Development iteration, CSS debugging | Chrome DevTools |
| PR verification, screenshots | Playwright |
| E2E test automation | Playwright |

Use `mcp__playwright__*` tools for browser automation:

### Navigation
```
mcp__playwright__browser_navigate - Go to URL
mcp__playwright__browser_navigate_back - Go back
mcp__playwright__browser_snapshot - Get page accessibility tree (preferred over screenshot)
mcp__playwright__browser_take_screenshot - Capture screenshot
```

### Interaction
```
mcp__playwright__browser_click - Click element
mcp__playwright__browser_type - Type text
mcp__playwright__browser_fill_form - Fill multiple fields
mcp__playwright__browser_select_option - Select dropdown option
mcp__playwright__browser_hover - Hover over element
mcp__playwright__browser_press_key - Press keyboard key
```

### Debugging
```
mcp__playwright__browser_console_messages - Get console logs
mcp__playwright__browser_network_requests - Get network requests
mcp__playwright__browser_evaluate - Run JavaScript
```

## Three-Layer Validation Pattern

**Every E2E test step must validate all three layers:**

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: UI Action (Browser Interaction)                   │
│  User performs action in real browser                        │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: DOM Update (UI Response)                          │
│  UI shows feedback that action succeeded                     │
├─────────────────────────────────────────────────────────────┤
│  LAYER 3: Database State (Backend Persistence)              │
│  Data actually saved in real database                        │
└─────────────────────────────────────────────────────────────┘
```

**Why all three?** Tests that skip any layer create false confidence:
- **No UI action**: Testing API, not user experience
- **No DOM check**: UI could be broken/stub but test passes
- **No DB check**: UI "theater" - buttons work but nothing saves

### Complete Example

```typescript
test('should add gear to My Gear collection', async ({ page }) => {
  // LAYER 1: UI Action - Real browser interaction
  await page.goto('/gear/browse');
  await page.getByRole('tab', { name: 'Amps' }).click();
  await page.getByRole('checkbox', { name: /TS808/i }).check();

  // LAYER 2: DOM Update - Verify UI responds
  await expect(page.getByText('Added to My Gear')).toBeVisible();

  // Optionally verify it appears in My Gear tab
  await page.getByRole('tab', { name: 'My Gear' }).click();
  await expect(page.getByText('TS808')).toBeVisible();

  // LAYER 3: Database State - Verify backend saved it
  const response = await page.request.get('/api/v1/gear/mine');
  const data = await response.json();
  expect(data.items.some(item => item.name.includes('TS808'))).toBe(true);
});
```

### Anti-Patterns to Avoid

```typescript
// ❌ BAD: Only checks UI, doesn't verify database
test('adds gear (incomplete)', async ({ page }) => {
  await page.goto('/gear/browse');
  await page.getByRole('checkbox', { name: 'TS808' }).check();
  await expect(page.getByText('Added')).toBeVisible();
  // Missing: Database verification!
});

// ❌ BAD: API-only test, doesn't use browser
test('adds gear (not E2E)', async ({ page }) => {
  const response = await page.request.post('/api/v1/gear', {
    data: { name: 'TS808' }
  });
  expect(response.status()).toBe(201);
  // Missing: Actual UI interaction!
});

// ❌ BAD: Uses test.skip() when prerequisites missing
test('adds gear if data exists', async ({ page }) => {
  const hasData = await checkIfDataExists();
  if (!hasData) {
    test.skip(); // WRONG - test should FAIL to force fixing prerequisites
  }
  // ...
});
```

### When Prerequisites Are Missing

**Tests must FAIL, not skip:**

```typescript
test('should load gear models in Browse tab', async ({ page }) => {
  await page.goto('/gear/browse');
  await page.getByRole('tab', { name: 'Amps' }).click();

  // If models don't load, this FAILS (correct behavior)
  await expect(page.getByRole('checkbox').first()).toBeVisible({ timeout: 5000 });

  // Don't do: if (no models) { test.skip(); }
  // The test failing reveals the bug that needs fixing
});
```

### Python E2E with Database Validation

```python
# tests/e2e/python/test_full_flow.py
import pytest
from sqlalchemy import text

@pytest.mark.e2e
async def test_add_gear_to_collection(page, db_session, test_user):
    """Three-layer validation in Python E2E test."""

    # LAYER 1: UI Action
    await page.goto("/gear/browse")
    await page.click("role=tab[name='Amps']")
    await page.check("role=checkbox[name=/TS808/i]")

    # LAYER 2: DOM Update
    await page.wait_for_selector("text=Added to My Gear", state="visible")

    # LAYER 3: Database State
    result = await db_session.execute(
        text("SELECT id FROM user_gear WHERE user_id = :uid AND name LIKE :name"),
        {"uid": str(test_user.id), "name": "%TS808%"}
    )
    assert result.fetchone() is not None, "Gear not saved to database after UI action"
```

## Debugging Workflow

### 1. Visual Debugging

```
# Take snapshot first (shows element refs)
Use mcp__playwright__browser_snapshot

# Identify element by ref from snapshot
Use mcp__playwright__browser_click with ref="element-ref"

# Check console for errors
Use mcp__playwright__browser_console_messages
```

### 2. Network Debugging

```
# Get all network requests
Use mcp__playwright__browser_network_requests

# Filter for API calls
Use mcp__playwright__browser_network_requests with includeStatic=false
```

### 3. JavaScript Debugging

```
# Run arbitrary JS
Use mcp__playwright__browser_evaluate with function="() => document.title"

# Check element state
Use mcp__playwright__browser_evaluate with function="(el) => el.value" and element ref
```

## E2E Test Patterns (Python - No Mocking)

### ✅ CORRECT: Test Against Real Backend

```python
# tests/e2e/python/tests/test_signal_chain.py
import pytest
from playwright.async_api import Page, expect
from sqlalchemy import text

@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.e2e_quick
async def test_create_signal_chain(page: Page, db_session, frontend_url: str):
    """Three-layer validation: UI action → DOM update → database state."""

    # LAYER 1: UI Action - Navigate and interact
    await page.goto(f"{frontend_url}/builder")
    await page.fill('[name="chain-name"]', 'E2E Test Chain')
    await page.select_option('[name="platform"]', 'nam')
    await page.click('button:has-text("Save")')

    # LAYER 2: DOM Update - Verify UI response
    await expect(page).to_have_url(re.compile(r'/library/chains'))
    await expect(page.get_by_text('E2E Test Chain')).to_be_visible()

    # LAYER 3: Database State - Verify persistence
    result = await db_session.execute(
        text("SELECT id FROM signal_chains WHERE name = :name"),
        {"name": "E2E Test Chain"}
    )
    assert result.fetchone() is not None, "Chain not saved to database"
```

### ❌ WRONG: Never Mock API Responses

```python
# ❌ DO NOT DO THIS - defeats the purpose of E2E testing
@pytest.fixture
async def mock_api(page: Page):
    await page.route('**/api/v1/signal-chains', lambda route: route.fulfill(
        status=200,
        body='{"signal_chains": []}'
    ))
```

### Auth Pattern for E2E

```python
# tests/e2e/python/conftest.py
@pytest.fixture
async def context(browser: Browser) -> AsyncGenerator[BrowserContext, None]:
    """Create browser context with authentication via dev-login."""
    context = await browser.new_context()

    # Authenticate via dev-login endpoint (DEBUG mode only)
    dev_login_url = f"{API_URL}/api/v1/auth/dev-login?username={TEST_USERNAME}"

    async with httpx.AsyncClient(follow_redirects=False) as client:
        response = await client.post(dev_login_url)
        session_cookie = response.cookies.get("session")

        await context.add_cookies([{
            "name": "session",
            "value": session_cookie,
            "domain": "localhost",
            "path": "/",
        }])

    yield context
    await context.close()
```

### Verifying Real Database Changes

```python
@pytest.mark.asyncio
@pytest.mark.e2e
async def test_persist_to_database(page: Page, db_session, frontend_url: str):
    """Verify data persists to database after UI action."""

    # Create something via UI
    await page.goto(f"{frontend_url}/builder")
    await page.fill('[name="name"]', 'Persistent Test')
    await page.click('button:has-text("Save")')

    # Verify via direct database query
    result = await db_session.execute(
        text("SELECT id FROM signal_chains WHERE name = :name"),
        {"name": "Persistent Test"}
    )
    assert result.fetchone() is not None, "Data not persisted to database"

    # Double-check by refreshing page
    await page.reload()
    await expect(page.get_by_text('Persistent Test')).to_be_visible()
```

## Assertions

```python
from playwright.async_api import expect

# Visibility
await expect(page.locator(".error")).to_be_visible()
await expect(page.locator(".loading")).to_be_hidden()

# Text content
await expect(page.locator("h1")).to_have_text("Dashboard")
await expect(page.locator(".message")).to_contain_text("Success")

# Attributes
await expect(page.locator("input")).to_have_value("test@example.com")
await expect(page.locator("button")).to_be_disabled()

# URL
await expect(page).to_have_url("**/dashboard")
```

## Locator Strategies (Priority Order)

1. **Role-based** (most resilient)
   ```python
   page.get_by_role("button", name="Submit")
   page.get_by_role("heading", name="Dashboard")
   page.get_by_role("textbox", name="Email")
   ```

2. **Test ID** (explicit, stable)
   ```python
   page.get_by_test_id("shootout-list")
   page.locator('[data-testid="create-button"]')
   ```

3. **Label/Placeholder** (user-facing)
   ```python
   page.get_by_label("Email")
   page.get_by_placeholder("Enter your email")
   ```

4. **CSS Selectors** (last resort)
   ```python
   page.locator(".submit-btn")
   page.locator("#main-form input[type='email']")
   ```

## DOM Validation Patterns

Our frontend components expose `data-testid` and `data-*` attributes for reliable testing.
See [Frontend Development Standards](https://github.com/krazyuniks/guitar-tone-shootout/wiki/Frontend-Development-Standards).

### Finding Elements by Test ID

```typescript
// Primary method - use data-testid
const list = page.getByTestId('shootout-list');
const card = page.getByTestId('shootout-card');
const deleteBtn = page.getByTestId('shootout-card-delete-btn');
```

### State Assertions

```typescript
// Check loading state
await expect(page.getByTestId('shootout-list')).not.toHaveAttribute('data-loading', 'true');

// Check error state
await expect(page.getByTestId('shootout-list')).not.toHaveAttribute('data-error', 'true');

// Check empty state
await expect(page.getByTestId('shootout-list')).not.toHaveAttribute('data-empty', 'true');
```

### Finding Specific Entities

```typescript
// Find specific item by entity ID
const specificCard = page.locator('[data-shootout-id="abc123"]');
await expect(specificCard).toBeVisible();

// Find by status
const readyCards = page.locator('[data-status="ready"]');
const count = await readyCards.count();
```

### Expected Component Test IDs

| Component | Test ID Pattern |
|-----------|-----------------|
| Lists | `{entity}-list` |
| Cards | `{entity}-card` |
| Actions | `{entity}-{action}-btn` |
| Forms | `{entity}-form` |
| Inputs | `{entity}-{field}-input` |

---

## Debugging Tips

### Console Errors
```
# Via MCP
Use mcp__playwright__browser_console_messages with level="error"

# In Python
page.on("console", lambda msg: print(f"Console: {msg.text}"))
```

### Network Failures
```
# Via MCP
Use mcp__playwright__browser_network_requests

# In Python
page.on("requestfailed", lambda req: print(f"Failed: {req.url}"))
```

### Screenshots on Failure
```python
@pytest.fixture
async def page(browser: Browser, request):
    page = await browser.new_page()
    yield page
    if request.node.rep_call.failed:
        await page.screenshot(path=f"screenshots/{request.node.name}.png")
```

### Trace Recording
```python
context = await browser.new_context()
await context.tracing.start(screenshots=True, snapshots=True)

# ... run tests ...

await context.tracing.stop(path="trace.zip")
# Open with: npx playwright show-trace trace.zip
```

## Running E2E Tests

E2E tests are in `tests/e2e/python/` and run on the HOST (not in Docker):

```bash
# Quick E2E tests (< 1 min, for commits)
just test-e2e-quick

# Full E2E tests (for pre-PR)
just test-e2e-full

# All E2E tests
pytest -m e2e tests/e2e/python/

# Specific test file
pytest tests/e2e/python/tests/test_shootouts.py -v

# With visible browser (headful mode)
pytest -m e2e tests/e2e/python/ --headed
```

### Environment Variables

E2E tests require environment variables for your worktree's ports:

```bash
export E2E_BASE_URL=http://localhost:9000       # Frontend (nginx)
export E2E_API_URL=http://localhost:8000        # Backend API
export E2E_DATABASE_URL=postgresql+asyncpg://shootout:devpassword@localhost:5432/shootout
```
