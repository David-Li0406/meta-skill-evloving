---
name: playwright
description: End-to-end testing automation with Playwright for web applications
---

# Playwright Testing Skill

This skill enables automated browser testing using Playwright for comprehensive E2E test coverage.

## Overview

Playwright is a powerful framework for web testing and automation that supports:
- Cross-browser testing (Chromium, Firefox, WebKit)
- Headless and headed modes
- Auto-waiting for elements
- Network interception
- Screenshot and video capture
- Mobile emulation

## Core Capabilities

### 1. Test Planning
- Analyze application flows and identify critical paths
- Design test scenarios covering happy paths and edge cases
- Prioritize tests based on risk and user impact

### 2. Test Generation
- Create maintainable Playwright tests using best practices
- Implement Page Object Model for code reusability
- Use proper selectors (data-testid preferred)
- Handle asynchronous operations correctly

### 3. Test Healing
- Identify flaky tests and root causes
- Suggest fixes for failing tests
- Update selectors when UI changes
- Implement retry strategies

## Best Practices

### Selector Strategy
```javascript
// ✅ GOOD: Use data-testid
await page.locator('[data-testid="submit-button"]').click();

// ✅ GOOD: Use role-based selectors
await page.getByRole('button', { name: 'Submit' }).click();

// ❌ AVOID: Fragile CSS selectors
await page.locator('div.container > button.btn-primary').click();
```

### Waiting and Assertions
```javascript
// ✅ Auto-waiting with expect
await expect(page.locator('[data-testid="result"]')).toBeVisible();

// ✅ Wait for network
await page.waitForResponse(resp => resp.url().includes('/api/data'));

// ❌ Arbitrary timeouts
await page.waitForTimeout(5000); // Avoid
```

### Page Object Model
```javascript
// pages/LoginPage.js
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email"]');
    this.passwordInput = page.locator('[data-testid="password"]');
    this.submitButton = page.locator('[data-testid="login-submit"]');
  }

  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}
```

## Test Structure

### Basic Test Template
```javascript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup: Navigate to page, login, etc.
    await page.goto('http://localhost:8000');
  });

  test('should perform expected action', async ({ page }) => {
    // Arrange
    // Act
    // Assert
    await expect(page.locator('[data-testid="result"]')).toHaveText('Expected');
  });

  test.afterEach(async ({ page }) => {
    // Cleanup if needed
  });
});
```

### API Testing
```javascript
test('should fetch employee data', async ({ request }) => {
  const response = await request.get('/api/employees?year=2024');
  expect(response.ok()).toBeTruthy();

  const data = await response.json();
  expect(data).toHaveProperty('employees');
  expect(data.employees).toBeInstanceOf(Array);
});
```

## Configuration

### playwright.config.js
```javascript
module.exports = {
  testDir: './tests',
  timeout: 30000,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  use: {
    baseURL: 'http://localhost:8000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'on-first-retry',
  },

  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
    { name: 'webkit', use: { browserName: 'webkit' } },
  ],
};
```

## Common Test Scenarios

### 1. Authentication Flow
```javascript
test('should login successfully', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Login' }).click();

  await page.locator('[data-testid="username"]').fill('admin');
  await page.locator('[data-testid="password"]').fill('password');
  await page.locator('[data-testid="login-submit"]').click();

  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
});
```

### 2. Form Submission
```javascript
test('should submit leave request', async ({ page }) => {
  await page.goto('/leave-requests');

  await page.locator('[data-testid="start-date"]').fill('2024-12-25');
  await page.locator('[data-testid="end-date"]').fill('2024-12-26');
  await page.locator('[data-testid="reason"]').fill('Vacation');

  await page.locator('[data-testid="submit"]').click();

  await expect(page.locator('[data-testid="success-message"]'))
    .toContainText('Request submitted successfully');
});
```

### 3. Data Table Interaction
```javascript
test('should filter employee table', async ({ page }) => {
  await page.goto('/employees');

  await page.locator('[data-testid="year-filter"]').selectOption('2024');

  await expect(page.locator('[data-testid="employee-row"]'))
    .toHaveCount(await page.locator('[data-testid="employee-row"]').count());

  const firstRow = page.locator('[data-testid="employee-row"]').first();
  await expect(firstRow).toContainText('2024');
});
```

### 4. Chart/Graph Validation
```javascript
test('should display usage rate chart', async ({ page }) => {
  await page.goto('/dashboard');

  // Wait for chart to render
  await page.waitForFunction(() => {
    const canvas = document.querySelector('[data-testid="usage-chart"]');
    return canvas && canvas.getContext('2d');
  });

  const chartCanvas = page.locator('[data-testid="usage-chart"]');
  await expect(chartCanvas).toBeVisible();

  // Screenshot for visual regression
  await expect(chartCanvas).toHaveScreenshot('usage-chart.png');
});
```

## Running Tests

### Command Line
```bash
# Run all tests
npx playwright test

# Run specific file
npx playwright test tests/employees.spec.js

# Run in headed mode (see browser)
npx playwright test --headed

# Run in debug mode
npx playwright test --debug

# Generate test report
npx playwright show-report
```

### CI/CD Integration
```yaml
# .github/workflows/playwright.yml
name: Playwright Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright Browsers
        run: npx playwright install --with-deps
      - name: Run Playwright tests
        run: npx playwright test
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

## Debugging Tips

1. **Use Playwright Inspector**: `npx playwright test --debug`
2. **Pause execution**: `await page.pause();`
3. **Verbose logging**: `DEBUG=pw:api npx playwright test`
4. **Screenshots**: `await page.screenshot({ path: 'screenshot.png' });`
5. **Console logs**: Monitor with `page.on('console', msg => console.log(msg.text()));`

## For YuKyuDATA Application

Key test scenarios to implement:
1. User authentication flow
2. Employee vacation data sync from Excel
3. Leave request submission and approval workflow
4. Dashboard KPI calculations
5. Chart rendering and data accuracy
6. Year filter functionality
7. Employee detail modal
8. Dark/light theme toggle
9. Data export functionality
10. Compliance alerts

Remember: **Reliable > Fast, Maintainable > Clever, Clear > Concise**
