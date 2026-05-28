# CI Configuration Reference

## Contents
- GitHub Actions
- CI-Specific Config
- Handling Flaky Tests
- Sharding for Large Suites
- CI Anti-patterns

## GitHub Actions

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run Playwright tests
        run: npx playwright test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

## CI-Specific Config

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
    testDir: './tests',
    fullyParallel: true,
    forbidOnly: !!process.env.CI,  // Fail if test.only is committed
    retries: process.env.CI ? 2 : 0,  // Retry flaky tests in CI
    workers: process.env.CI ? 4 : undefined,
    reporter: process.env.CI
        ? [['html'], ['github']]  // GitHub annotations
        : [['html'], ['list']],

    use: {
        baseURL: process.env.BASE_URL || 'http://localhost:3000',
        trace: 'on-first-retry',
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
    },

    // Start dev server before tests
    webServer: {
        command: 'npm run dev',
        url: 'http://localhost:3000',
        reuseExistingServer: !process.env.CI,
        timeout: 120_000,
    },

    projects: [
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
        { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
        { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    ],
});
```

## Handling Flaky Tests

```typescript
// Retry configuration (prefer fixing root cause)
export default defineConfig({
    retries: process.env.CI ? 2 : 0,
});

// Mark known flaky test (temporary - fix the root cause!)
test('occasionally flaky test', {
    annotation: { type: 'issue', description: 'https://github.com/org/repo/issues/123' },
}, async ({ page }) => {
    // ...
});

// Skip in CI while investigating
test.skip(!!process.env.CI, 'Flaky in CI - investigating');

// Increase timeout for slow test
test('slow integration test', async ({ page }) => {
    test.setTimeout(60_000);
    // ...
});
```

## Sharding for Large Suites

```yaml
# Run tests in parallel across multiple jobs
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - name: Run tests
        run: npx playwright test --shard=${{ matrix.shard }}/4
```

## CI Anti-patterns

| Bad | Why | Good |
|-----|-----|------|
| No retries in CI | Single flake fails PR | `retries: 2` for CI |
| `test.only` committed | Other tests don't run | Use `forbidOnly: !!process.env.CI` |
| No artifact upload | Can't debug CI failures | Upload report on failure |
| Hardcoded URLs | Breaks in different envs | Use `baseURL` from env |
| No test sharding (huge suite) | Slow CI times | Shard across workers |
| Ignoring flaky tests | Tech debt accumulates | Fix root cause, track issues |
