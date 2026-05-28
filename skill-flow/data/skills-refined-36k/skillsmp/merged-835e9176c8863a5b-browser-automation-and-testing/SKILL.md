---
name: browser-automation-and-testing
description: Use this skill for end-to-end testing, browser automation, visual regression, and validating user workflows with Playwright or similar tools.
---

# Browser Automation and Testing

## When to Use This Skill

Use when:
- Writing end-to-end tests
- Testing user workflows
- Validating cross-browser compatibility
- Implementing visual regression tests
- Debugging browser interactions

## Playwright Setup

### Installation

```bash
pnpm add -D @playwright/test
npx playwright install
```

### Configuration

Create a `playwright.config.ts` file:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 30000,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'] } },
  ],

  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Test Patterns

### Basic Page Test

```typescript
import { test, expect } from '@playwright/test';

test('homepage loads correctly', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveTitle(/My App/);
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
});
```

### User Flow Test

```typescript
test('user can upload and process files', async ({ page }) => {
  await page.goto('/');

  // Upload file
  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles('./test-files/sample.txt');

  // Wait for processing
  await expect(page.getByText('Processing...')).toBeVisible();
  await expect(page.getByText('Processing...')).not.toBeVisible();

  // Verify result
  await expect(page.getByTestId('file-tree')).toContainText('sample.txt');
});
```

### Form Interaction

```typescript
test('form submission works', async ({ page }) => {
  await page.goto('/settings');

  // Fill form
  await page.getByLabel('Max file size').fill('64');
  await page.getByLabel('Remove empty lines').check();

  // Submit
  await page.getByRole('button', { name: 'Save' }).click();

  // Verify
  await expect(page.getByText('Settings saved')).toBeVisible();
});
```

## Locator Strategies

```typescript
// Preferred: Role-based (accessible)
page.getByRole('button', { name: 'Submit' });
page.getByRole('textbox', { name: 'Email' });
page.getByRole('checkbox', { name: 'Remember me' });

// Label-based
page.getByLabel('Password');

// Text-based
page.getByText('Welcome');
page.getByText(/welcome/i);  // Case insensitive

// Test ID (when others don't work)
page.getByTestId('submit-button');

// CSS selector (last resort)
page.locator('.submit-btn');
```

## Assertions

```typescript
// Visibility
await expect(element).toBeVisible();
await expect(element).toBeHidden();

// Content
await expect(element).toHaveText('Hello');
await expect(element).toContainText('Hello');

// Attributes
await expect(element).toHaveAttribute('disabled');
await expect(element).toHaveClass(/active/);

// Count
await expect(page.getByRole('listitem')).toHaveCount(5);

// URL
await expect(page).toHaveURL('/dashboard');
```

## Visual Regression

```typescript
test('component looks correct', async ({ page }) => {
  await page.goto('/component-demo');

  // Full page screenshot
  await expect(page).toHaveScreenshot('full-page.png');

  // Element screenshot
  const card = page.getByTestId('card');
  await expect(card).toHaveScreenshot('card.png');
});
```

## Debugging Workflow

### Visual Debugging

```bash
# Take snapshot first (shows element refs)
Use mcp__playwright__browser_snapshot

# Identify element by ref from snapshot
Use mcp__playwright__browser_click with ref="element-ref"

# Check console for errors
Use mcp__playwright__browser_console_messages
```

### Network Debugging

```bash
# Get all network requests
Use mcp__playwright__browser_network_requests

# Filter for API calls
Use mcp__playwright__browser_network_requests with includeStatic=false
```

### JavaScript Debugging

```bash
# Run arbitrary JS
Use mcp__playwright__browser_evaluate with function="() => document.title"

# Check element state
Use mcp__playwright__browser_evaluate with function="(el) => el.value" and element ref
```

## Running Tests

```bash
# All tests
npx playwright test

# Specific file
npx playwright test upload.spec.ts

# Headed mode
npx playwright test --headed

# Debug mode
npx playwright test --debug

# Update snapshots
npx playwright test --update-snapshots
```

## E2E Testing Guidelines

### Critical Notes

- **No Mocking in E2E Tests**: Always test against real backend services to avoid false confidence.
- **Three-Layer Validation**: Ensure every E2E test step validates UI action, DOM update, and database state.

### Example E2E Test

```typescript
test('should add gear to My Gear collection', async ({ page }) => {
  // LAYER 1: UI Action - Real browser interaction
  await page.goto('/gear/browse');
  await page.getByRole('tab', { name: 'Amps' }).click();
  await page.getByRole('checkbox', { name: /TS808/i }).check();

  // LAYER 2: DOM Update - Verify UI responds
  await expect(page.getByText('Added to My Gear')).toBeVisible();

  // LAYER 3: Database State - Verify backend saved it
  const response = await page.request.get('/api/v1/gear/mine');
  const data = await response.json();
  expect(data.items.some(item => item.name.includes('TS808'))).toBe(true);
});
```

## Environment Variables

E2E tests require environment variables for your worktree's ports:

```bash
export E2E_BASE_URL=http://localhost:9000       # Frontend (nginx)
export E2E_API_URL=http://localhost:8000        # Backend API
export E2E_DATABASE_URL=postgresql+asyncpg://shootout:devpassword@localhost:5432/shootout
```