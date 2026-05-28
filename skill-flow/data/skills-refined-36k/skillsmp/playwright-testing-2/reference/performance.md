# Performance Reference

## Contents
- Parallel Execution
- Efficient Authentication
- API Shortcuts for Data Setup
- Performance Anti-patterns
- Test Isolation with Contexts

## Parallel Execution

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
    // Run tests in parallel (default: true)
    fullyParallel: true,

    // Number of parallel workers
    workers: process.env.CI ? 4 : undefined, // undefined = use all CPUs

    // Fail fast in CI
    maxFailures: process.env.CI ? 10 : undefined,
});
```

**Tests must be independent for parallel execution.** Each test should:
- Create its own data
- Not depend on other tests' side effects
- Clean up if necessary (or use isolated contexts)

## Efficient Authentication

```typescript
// SLOW: Login through UI for every test
test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password');
    await page.getByRole('button', { name: 'Sign in' }).click();
    await page.waitForURL('/dashboard');
});

// FAST: Reuse authentication state
// global-setup.ts
import { chromium } from '@playwright/test';

async function globalSetup() {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    await page.goto('/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password');
    await page.getByRole('button', { name: 'Sign in' }).click();
    await page.waitForURL('/dashboard');

    // Save auth state
    await page.context().storageState({ path: '.auth/user.json' });
    await browser.close();
}

export default globalSetup;

// playwright.config.ts
export default defineConfig({
    globalSetup: require.resolve('./global-setup'),
    projects: [
        { name: 'setup', testMatch: /global-setup\.ts/ },
        {
            name: 'tests',
            use: { storageState: '.auth/user.json' },
            dependencies: ['setup'],
        },
    ],
});
```

## API Shortcuts for Data Setup

```typescript
// SLOW: Create test data through UI
test('deletes a project', async ({ page }) => {
    // Create project through UI - slow!
    await page.goto('/projects/new');
    await page.getByLabel('Name').fill('Test Project');
    await page.getByRole('button', { name: 'Create' }).click();
    await page.waitForURL(/\/projects\/\d+/);

    // Now test deletion...
});

// FAST: Create test data via API
test('deletes a project', async ({ page, request }) => {
    // Create via API - fast!
    const response = await request.post('/api/projects', {
        data: { name: 'Test Project' }
    });
    const { id } = await response.json();

    // Test the actual UI behavior
    await page.goto(`/projects/${id}`);
    await page.getByRole('button', { name: 'Delete' }).click();
    await page.getByRole('button', { name: 'Confirm' }).click();

    await expect(page.getByText('Project deleted')).toBeVisible();
});
```

## Performance Anti-patterns

| Slow | Fast |
|------|------|
| `waitForLoadState('networkidle')` | `waitForResponse` for specific API |
| UI-based auth every test | Reuse `storageState` |
| Create all data through UI | API calls for setup |
| `waitForTimeout(ms)` | Condition-based waits |
| Running all browsers locally | Run browsers in parallel |
| Full E2E for every edge case | Unit tests + selective E2E |

## Test Isolation with Contexts

```typescript
// Each test gets isolated browser context (cookies, storage)
test('test one', async ({ context, page }) => {
    // Fresh context - no shared state with other tests
});

// Share context within a describe block if needed
test.describe(() => {
    let sharedPage: Page;

    test.beforeAll(async ({ browser }) => {
        sharedPage = await browser.newPage();
        // Expensive setup once
    });

    test.afterAll(async () => {
        await sharedPage.close();
    });
});
```
