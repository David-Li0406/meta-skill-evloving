# E2E Testing (Playwright)

Complete guide to end-to-end testing in ActionPhase with Playwright.

## Quick Links

- **[E2E Patterns Reference](e2e-patterns-reference.md)** ← **READ THIS for complete E2E patterns, helpers, and real examples**
- This file: Prerequisites and rules

## The Golden Rule

**E2E tests are the LAST step, NEVER the first!**

You MUST complete all four prerequisite steps before writing any E2E test.

---

## Mandatory E2E Checklist

**⚠️ ALL FOUR must pass before writing E2E test:**

### 1. Backend Unit Test ✅

```bash
# Test must pass WITHOUT database
SKIP_DB_TESTS=true go test ./pkg/db/services -run TestFeatureName -v

# Expected output: PASS
```

### 2. API Endpoint Verification ✅

```bash
# Login to get token
./backend/scripts/api-test.sh login-player

# Verify endpoint returns correct data
curl -s -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  http://localhost:3000/api/v1/endpoint | jq '.expected_field'

# Expected: Correct data structure returned
```

### 3. Frontend Component Test ✅

```bash
# Component test must pass
npm test -- ComponentName.test.tsx

# Expected output: PASS (all assertions green)
```

### 4. System Verification ✅

```bash
# Backend health check
curl -sf http://localhost:3000/health
# Expected: {"status": "ok"}

# Frontend running
curl -sf http://localhost:5173
# Expected: HTML response (no error)
```

**ONLY after all four pass → Write E2E test**

---

## Running E2E Tests

### Basic Commands

```bash
# Headless (CI mode) - auto-loads fixtures
just e2e

# With visible browser
just e2e-test headed

# Interactive UI mode
just e2e-test ui

# Debug specific test
just e2e-test debug
```

### Advanced Options

```bash
# Run specific test file
npx playwright test e2e/journeys/critical/user-onboarding.spec.ts

# Run tests matching pattern
npx playwright test -g "submit action"

# View HTML report
just e2e-test report

# Update snapshots
npx playwright test --update-snapshots
```

---

## E2E Test Structure

### File Organization

```
frontend/e2e/
├── global-setup.ts          # Automatic fixture loading (6 workers)
├── playwright.config.ts     # Playwright configuration
├── auth.setup.ts            # Shared auth state
├── helpers/
│   ├── auth.ts             # Login helpers
│   └── navigation.ts       # Common navigation
├── journeys/
│   ├── critical/           # Must-pass scenarios
│   │   ├── user-onboarding.spec.ts
│   │   └── multi-user-collaboration.spec.ts
│   └── standard/           # Feature-specific tests
│       ├── common-room-discussion.spec.ts
│       └── character-approval-workflow.spec.ts
```

### Test Template

```typescript
import { test, expect } from '@playwright/test';
import { loginAsGM, loginAsPlayer } from '../helpers/auth';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup: Login, navigate to starting point
    await loginAsPlayer(page, 'TestPlayer1');
    await page.goto('/games/164');
  });

  test('should perform specific action', async ({ page }) => {
    // 1. Arrange: Set up preconditions
    await page.waitForSelector('[data-testid="feature-container"]');

    // 2. Act: Perform the action
    await page.click('[data-testid="submit-button"]');

    // 3. Assert: Verify outcome
    await expect(page.getByText('Success!')).toBeVisible();
  });
});
```

---

## Playwright MCP Debugging (CRITICAL)

**⚠️ ALWAYS use Playwright MCP before modifying test code!**

### When a Test Fails

**DO NOT immediately modify the test.** Follow this protocol:

1. **Navigate to the page**
```typescript
mcp__playwright__browser_navigate({ url: "http://localhost:5173/games/164" })
```

2. **Check page state**
```typescript
mcp__playwright__browser_snapshot()
// Shows accessibility tree - is the element present?
```

3. **Check for JavaScript errors**
```typescript
mcp__playwright__browser_console_messages({ onlyErrors: true })
// Any console errors? Fix application code first!
```

4. **Manually test the feature**
```typescript
// Login
mcp__playwright__browser_type({
  element: "Email input",
  ref: "...",
  text: "test_player1@example.com"
})

// Perform action
mcp__playwright__browser_click({
  element: "Submit button",
  ref: "..."
})

// Verify result
mcp__playwright__browser_snapshot()
// Does the feature work manually?
```

### Fix Decision Tree

```
Did Playwright MCP show the feature works manually?
├─ YES → Fix the test (timing, selectors, expectations)
│   └─ Check: Race condition? Wrong selector? Missing wait?
│
└─ NO → Fix the application code
    └─ Check: JavaScript error? Element not rendered? API failure?
```

### Common Debugging Scenarios

**Timeout waiting for element:**
```typescript
// 1. Use Playwright MCP to navigate
mcp__playwright__browser_navigate({ url: "..." })

// 2. Check if element exists
mcp__playwright__browser_snapshot()

// 3. If element exists but test fails → timing issue
// Solution: Add explicit wait
await page.waitForSelector('[data-testid="element"]');

// 4. If element missing → feature not implemented or broken
// Solution: Fix application code first
```

**Form submission fails:**
```typescript
// 1. Check console for errors
mcp__playwright__browser_console_messages({ onlyErrors: true })

// 2. Check network requests
mcp__playwright__browser_network_requests()

// 3. Manually submit form
mcp__playwright__browser_click({ element: "Submit", ref: "..." })
mcp__playwright__browser_snapshot()

// 4. Is error message shown? Fix application
// 5. Form submits manually but test fails? Fix test
```

---

## Best Practices

### Selectors

**Prefer data-testid** (most reliable):
```typescript
await page.click('[data-testid="submit-action"]');
```

**Use role-based selectors** (accessible):
```typescript
await page.getByRole('button', { name: 'Submit' }).click();
```

**Avoid class names** (brittle):
```typescript
await page.click('.btn-primary'); // ❌ Class may change
```

### Waits

**Explicit waits** (reliable):
```typescript
await page.waitForSelector('[data-testid="success-message"]');
await page.waitForLoadState('networkidle');
```

**Avoid arbitrary timeouts** (flaky):
```typescript
await page.waitForTimeout(3000); // ❌ Arbitrary
```

### Test Independence

Each test should be **fully independent**:

```typescript
test.beforeEach(async ({ page }) => {
  // Fresh state for every test
  await loginAsPlayer(page, 'TestPlayer1');
  await page.goto('/games/164');
});

test.afterEach(async ({ page }) => {
  // Cleanup if needed (fixtures auto-reset)
});
```

### One Concern Per Test

**Good** (single concern):
```typescript
test('should show autocomplete when typing @', async ({ page }) => {
  await page.fill('[data-testid="message-input"]', '@');
  await expect(page.getByText('TestPlayer1')).toBeVisible();
});

test('should mention user when selected from autocomplete', async ({ page }) => {
  await page.fill('[data-testid="message-input"]', '@');
  await page.click('[data-testid="mention-TestPlayer1"]');
  await expect(page.locator('[data-testid="message-input"]'))
    .toHaveValue('@TestPlayer1 ');
});
```

**Bad** (multiple concerns):
```typescript
test('mentions feature works', async ({ page }) => {
  // Tests autocomplete + selection + submission + rendering ❌
  // Too many concerns in one test!
});
```

---

## Common Patterns

### Authentication

```typescript
import { loginAsGM, loginAsPlayer } from '../helpers/auth';

// Login as GM
await loginAsGM(page);

// Login as specific player
await loginAsPlayer(page, 'TestPlayer1');

// Login with custom credentials
await page.goto('/login');
await page.fill('[data-testid="email-input"]', 'test_gm@example.com');
await page.fill('[data-testid="password-input"]', 'testpassword123');
await page.click('[data-testid="login-button"]');
await page.waitForURL('/dashboard');
```

### Navigation

```typescript
// Navigate to game
await page.goto('/games/164');

// Wait for page load
await page.waitForLoadState('networkidle');

// Navigate via UI
await page.click('[data-testid="game-link-164"]');
await expect(page).toHaveURL(/\/games\/164/);
```

### Form Submission

```typescript
// Fill form
await page.fill('[data-testid="title-input"]', 'My Game Title');
await page.fill('[data-testid="description-input"]', 'Game description');

// Submit
await page.click('[data-testid="submit-button"]');

// Wait for success
await expect(page.getByText('Game created successfully')).toBeVisible();
```

### Multi-User Scenarios

```typescript
test('GM and player can collaborate', async ({ browser }) => {
  // Create two contexts (separate sessions)
  const gmContext = await browser.newContext();
  const playerContext = await browser.newContext();

  const gmPage = await gmContext.newPage();
  const playerPage = await playerContext.newPage();

  // GM actions
  await loginAsGM(gmPage);
  await gmPage.goto('/games/164');
  await gmPage.click('[data-testid="advance-phase"]');

  // Player sees phase change
  await loginAsPlayer(playerPage, 'TestPlayer1');
  await playerPage.goto('/games/164');
  await expect(playerPage.getByText('Action Phase')).toBeVisible();

  // Cleanup
  await gmContext.close();
  await playerContext.close();
});
```

---

## Fixture Management

E2E tests use **automatic fixture reset** via `global-setup.ts`.

### How It Works

1. **Before all tests**, `global-setup.ts` runs once
2. Applies common fixtures: `apply_common.sh`
3. Applies worker-specific fixtures for 6 parallel workers
4. Each worker gets isolated test data (users, games with offset IDs)

### Test Data Available

- **Test Users**: `TestGM`, `TestPlayer1-5` (password: `testpassword123`)
- **Worker-specific users**: `TestGM_1`, `TestPlayer1_1`, etc. (for workers 1-5)
- **Test Games**: 164-168, 200-210, 300-310, 335-345, 400-410, 600-610
- **Worker-specific games**: Game IDs offset by worker index × 10,000
  - Worker 0: Game 164
  - Worker 1: Game 10164
  - Worker 2: Game 20164
  - etc.

### Using Fixtures in Tests

```typescript
test('should load game data', async ({ page }) => {
  await loginAsPlayer(page, 'TestPlayer1');

  // Use predictable game ID (Worker 0)
  await page.goto('/games/164');

  // Fixture data is consistent
  await expect(page.getByText('Shadows Over Innsmouth')).toBeVisible();
});
```

### Manual Fixture Reload (Rarely Needed)

```bash
# Reload all fixtures
just load-e2e

# Apply specific worker fixtures
DB_NAME=actionphase ./backend/pkg/db/test_fixtures/apply_e2e_worker.sh 0
```

**Note**: Fixtures automatically reset before each test run. Manual reload only needed for local debugging.

---

## Playwright Configuration

Key settings in `playwright.config.ts`:

```typescript
export default defineConfig({
  workers: 6,                    // Parallel workers
  retries: process.env.CI ? 2 : 0, // Retry flaky tests in CI
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'retain-on-failure',  // Save trace on failure
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  globalSetup: './e2e/global-setup.ts', // Auto fixture loading
});
```

---

## Debugging Failed Tests

### 1. Check Test Output

```bash
# Run with reporter that shows details
npx playwright test --reporter=list

# Output shows:
# - Which test failed
# - Assertion that failed
# - Timeout details
# - Screenshots/traces saved
```

### 2. View HTML Report

```bash
just e2e-test report
# Opens interactive HTML report
# Shows screenshots, traces, network activity
```

### 3. Run in Headed Mode

```bash
# Watch test execute in real browser
just e2e-test headed
```

### 4. Use Debug Mode

```bash
# Pause execution, step through test
just e2e-test debug

# Or debug specific test
npx playwright test --debug -g "test name"
```

### 5. Use Playwright MCP (Primary Method)

See "Playwright MCP Debugging" section above.

**Always start with Playwright MCP before modifying test code!**

---

## CI/CD Integration

E2E tests run in CI via GitHub Actions:

```yaml
- name: Run E2E tests
  run: |
    npm run build
    npx playwright test --reporter=github
```

**CI-specific behavior**:
- Retries: 2 (flaky test protection)
- Headless: Always
- Fixtures: Auto-loaded via global-setup
- Artifacts: Screenshots/traces uploaded on failure

---

## Anti-Patterns

### ❌ Writing E2E Before Lower Tests

```typescript
// NO unit test, NO component test → straight to E2E ❌
test('feature works', async ({ page }) => { ... });
```

**Solution**: Follow the pyramid (unit → API → component → E2E)

### ❌ Multiple Concerns in One Test

```typescript
test('mentions work', async ({ page }) => {
  // Tests autocomplete + submission + rendering + validation ❌
});
```

**Solution**: Split into focused tests

### ❌ Arbitrary Timeouts

```typescript
await page.waitForTimeout(5000); // ❌ Flaky
```

**Solution**: Explicit waits for specific conditions

### ❌ Brittle Selectors

```typescript
await page.click('.btn-primary'); // ❌ Class may change
```

**Solution**: Use data-testid or role-based selectors

### ❌ Skipping Playwright MCP Debugging

```typescript
// Test fails → immediately change test expectations ❌
```

**Solution**: Use Playwright MCP to verify feature works first

---

**Back to**: [SKILL.md](../SKILL.md)
