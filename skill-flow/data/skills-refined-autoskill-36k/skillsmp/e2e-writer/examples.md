# E2E Writer - Examples

## Complete Test Pattern

```typescript
import { test, expect } from '@playwright/test';

test.describe('Create Ticket Workflow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('should create a new ticket successfully', async ({ page }) => {
    // Navigate
    await page.getByRole('link', { name: 'Create ticket' }).click();

    // Verify page
    await expect(page.getByRole('heading', { level: 1 })).toContainText('Create new ticket');

    // Fill form using semantic selectors
    await page.getByLabel('Title').fill('Repair elevator');
    await page.getByLabel('Description').fill('Elevator is not working');
    await page.getByLabel('Status').selectOption('NEW');

    // Submit
    await page.getByRole('button', { name: 'Create' }).click();

    // Verify success
    await expect(page.getByText(/ticket created successfully/i)).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Repair elevator' })).toBeVisible();
  });

  test('should show error when required fields are missing', async ({ page }) => {
    // Navigate
    await page.getByRole('link', { name: 'Create ticket' }).click();

    // Submit without filling
    await page.getByRole('button', { name: 'Create' }).click();

    // Verify error
    await expect(page.getByText(/title is required/i)).toBeVisible();
  });
});
```

## Best Practices

### Wait for Dynamic Elements

```typescript
// ✅ GOOD - Wait explicitly
await page.getByText('Loading...').toBeVisible();
await page.getByText('Loading...').toBeHidden();

// Then continue
await expect(page.getByRole('heading')).toContainText('Tickets');
```

### Avoid Arbitrary Timeouts

```typescript
// ❌ BAD
await page.waitForTimeout(2000);

// ✅ GOOD - Wait for specific element
await page.getByRole('button', { name: 'Create' }).waitFor();
```

### Clean Up After Tests

```typescript
test.afterEach(async ({ page }) => {
  // Clean up test data if necessary
  await page.evaluate(() => localStorage.clear());
});
```

## Naming Convention

```
tests/e2e/[scenario-name].spec.ts

Examples :
- tests/e2e/create-ticket.spec.ts
- tests/e2e/edit-ticket.spec.ts
- tests/e2e/add-comment.spec.ts
```

## Run E2E Tests

```bash
npm run test:e2e        # Headless mode (CI)
npm run test:e2e:ui     # UI mode
npm run test:e2e:debug  # Step by step mode
```
