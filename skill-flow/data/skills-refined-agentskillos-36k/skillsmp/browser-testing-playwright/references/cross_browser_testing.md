# Cross-Browser Testing

Cross-browser testing ensures your application works consistently across different web browsers. Playwright makes this easy by allowing you to define "projects" for each browser you want to test against.

## Configuring Projects

Projects are configured in the `playwright.config.ts` file. By default, Playwright sets up projects for Chromium (Chrome, Edge), Firefox, and WebKit (Safari).

You can also use device descriptors to simulate different viewports and user agents.

### Example `playwright.config.ts` for Cross-Browser Testing

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // ... other settings
  testDir: './tests',

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },

    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    /* Test against mobile viewports. */
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },

    /* Test against branded browsers. */
    // {
    //   name: 'Microsoft Edge',
    //   use: { channel: 'msedge' },
    // },
    // {
    //   name: 'Google Chrome',
    //   use: { channel: 'chrome' },
    // },
  ],
  // ... other settings
});
```

## Running Tests

When you run `npx playwright test`, Playwright will run your entire test suite against **all** configured projects in parallel.

### Running a Specific Project

If you want to run tests against only one browser, you can use the `--project` flag.

```bash
# Run tests only on Chromium
npx playwright test --project=chromium

# Run tests only on mobile Safari
npx playwright test --project="Mobile Safari"
```

## Browser-Specific Logic

Sometimes, you might need to write a test that is specific to a certain browser. You can use `test.skip` or `test.fixme` to conditionally run or skip tests based on the browser name.

The browser name is available from the `browserName` property in your test.

```typescript
import { test, expect } from '@playwright/test';

test('should only run on firefox', async ({ page, browserName }) => {
  // Skip this test if it's not running on Firefox
  test.skip(browserName !== 'firefox', 'This feature is Firefox-only');

  await page.goto('/some-firefox-feature');
  // ... test logic
});

test('should have a different title on WebKit', async ({ page, browserName }) => {
  await page.goto('/');

  if (browserName === 'webkit') {
    await expect(page).toHaveTitle('My App for Safari');
  } else {
    await expect(page).toHaveTitle('My App');
  }
});
```
This allows you to handle minor inconsistencies between browsers without having to create entirely separate test files.