# Playwright Patterns Reference

Detailed patterns and examples for Playwright E2E tests. For core workflow and rules, see the main SKILL.md.

---

## Locator Strategies

### Prefer data-testid attributes

```typescript
// Best - explicit test identifier
await page.getByTestId('create-shipment-btn').click();

// Good - accessible selectors
await page.getByRole('button', { name: 'Create' }).click();
await page.getByLabel('Reference number').fill('ABC123');

// Avoid - fragile selectors
await page.locator('.btn-primary').click();  // CSS class
await page.locator('div > span > button').click();  // DOM structure
```

### Adding test IDs to components

In Vue components, add `data-testid`:

```vue
<ButtonComponent data-testid="create-shipment-btn" label="Create" />
```

### Robust Patterns

| Pattern | Example | Why |
|---------|---------|-----|
| Use `data-testid` | `getByTestId('contract-save-btn')` | Explicit, stable, self-documenting |
| Scope to testid first | `getByTestId('zone-cell').locator('.multiselect')` | Limits blast radius of CSS changes |
| Use Radix attributes | `locator('[data-radix-popper-content-wrapper]')` | Framework-provided, stable |
| Add testid wrappers in Vue | `h('div', { 'data-testid': 'cell-name' }, [...])` | Makes table cells addressable |
| Use `getByRole` | `getByRole('button', { name: 'Save' })` | Semantic, accessibility-friendly |

### Fragile Anti-Patterns

| Anti-Pattern | Example | Problem |
|--------------|---------|---------|
| Index-based column | `td.nth(5)`, `input.nth(2)` | Breaks when columns reorder |
| Index-based multiselect | `.multiselect.nth(3)` | Breaks when fields added/removed |
| Generic CSS filtering | `.flex.flex-col` | Matches unrelated elements |
| Deeply nested CSS | `.card .header .btn` | Fragile to DOM restructuring |

### Refactoring fragile patterns

```typescript
// FRAGILE: Column index can change
const serviceLevelDropdown = lastRow.locator('.multiselect').nth(2);

// ROBUST: Add testid wrapper in Vue, then scope
// In Vue: h('div', { 'data-testid': 'surcharge-service-levels-cell' }, [...])
const serviceLevelDropdown = lastRow
  .getByTestId('surcharge-service-levels-cell')
  .locator('.multiselect');
```

---

## Page Object Wrappers

For complex components, create wrappers in `tests/helpers/wrappers/`:

```typescript
// MultiselectWrapper.ts
export default class MultiselectWrapper {
  constructor(private page: Page, private testId: string) {}

  async selectByText(text: string, clearFirst = false) {
    const select = this.page.getByTestId(this.testId);
    if (clearFirst) {
      await select.getByRole('button', { name: 'Clear' }).click();
    }
    await select.click();
    await this.page.getByText(text).click();
  }
}
```

Usage:

```typescript
const addressSelect = new MultiselectWrapper(page, 'sender-address-select');
await addressSelect.selectByText('ShipitSmarter Sender', true);
```

---

## Waiting Strategies

### Wait for navigation

```typescript
await page.waitForURL(`${BASE_URL}/shipment/${shipmentId}`);
```

### Wait for API responses

```typescript
await Promise.all([
  page.waitForResponse(async (resp) => {
    if (resp.url().includes('api/shipping/v4/shipments')) {
      const data = await resp.json();
      shipmentId = data?.id;
    }
    return resp.url().includes('api/shipping/v4/shipments') && resp.status() === 200;
  }),
  page.getByTestId('submit-btn').click(),
]);
```

### Wait for elements

```typescript
await page.getByTestId('loading-spinner').waitFor({ state: 'hidden' });
await page.getByText('Success').waitFor({ state: 'visible' });
```

---

## Timeout Strategy

| Operation | Timeout | Why |
|-----------|---------|-----|
| UI elements | 10-15s (default) | Appear instantly or fail |
| API responses | 60s | Firefox can be 2-3x slower |
| Test suite | 120s (global) | Never reduce |

```typescript
// API wait with explicit timeout
const response = page.waitForResponse(
  (r) => r.url().includes('/api/') && r.request().method() === 'POST',
  { timeout: 60000 }
);
```

---

## Cross-browser Cleanup

Only run cleanup in the last browser project to avoid race conditions:

```typescript
test.afterAll(async ({ browser }, testInfo) => {
  if (testInfo.project.name !== 'firefox') return;
  // ... cleanup code
});
```

---

## Common Patterns

### Verify input values after fill

```typescript
const input = page.locator('input[placeholder*="contract name"]');
await input.fill('value');
await expect(input).toHaveValue('value'); // Always verify
```

### Button state verification

```typescript
const btn = page.getByRole('button', { name: 'Save' });
await expect(btn).toBeEnabled();
await btn.click();
```

### Vue-Multiselect handling

```typescript
const dropdown = row.locator('.multiselect');
await dropdown.click();
const option = dropdown.locator('.multiselect__content-wrapper').getByText('Option');
await option.click();
```

### Descriptive assertions

```typescript
await expect(
  page.getByText(reference),
  `Contract ${reference} should be in list`
).toBeVisible();
```

---

## Assertions Reference

```typescript
import { expect } from '~/helpers/fixtures';

// Visibility
await expect(page.getByText('Shipment created')).toBeVisible();
await expect(page.getByTestId('error-message')).not.toBeVisible();

// Text content
await expect(page.getByTestId('reference')).toHaveText('ABC123');
await expect(page.getByTestId('status')).toContainText('Active');

// Input values
await expect(page.getByLabel('Weight')).toHaveValue('10');

// URL
await expect(page).toHaveURL(/\/shipment\/\d+/);

// Count
await expect(page.getByTestId('list-item')).toHaveCount(3);
```

---

## Best Practices Summary

> Based on [Playwright's official best practices](https://playwright.dev/docs/best-practices)

### Testing philosophy

**Test user-visible behavior**
- Test what end users see and interact with
- Avoid relying on implementation details (CSS classes, DOM structure, function names)
- Your test should interact with the rendered output, not internal code

**Make tests isolated**
- Each test should be independent - own storage, cookies, data
- Use `beforeEach` hooks for common setup (like navigation or login)
- Avoid tests that depend on state from previous tests (unless using `test.describe.serial`)

**Avoid testing third-party dependencies**
- Don't test external sites or APIs you don't control
- Mock external dependencies using Playwright's Network API:

```typescript
await page.route('**/api/external-service', route => route.fulfill({
  status: 200,
  body: JSON.stringify({ data: 'mocked response' }),
}));
```

### Use web-first assertions

Always use async assertions that auto-wait and retry:

```typescript
// Good - waits for condition
await expect(page.getByText('welcome')).toBeVisible();

// Bad - doesn't wait, can cause flaky tests
expect(await page.getByText('welcome').isVisible()).toBe(true);
```

### Use locators effectively

**Chain and filter locators** for precision:

```typescript
// Find button within a specific list item
await page
  .getByRole('listitem')
  .filter({ hasText: 'Product 2' })
  .getByRole('button', { name: 'Add to cart' })
  .click();
```

### Use soft assertions for multiple checks

When you want to check multiple things without stopping at the first failure:

```typescript
// Soft assertions collect all failures
await expect.soft(page.getByTestId('status')).toHaveText('Success');
await expect.soft(page.getByTestId('count')).toHaveText('5');

// Test continues even if above assertions fail
await page.getByRole('link', { name: 'next page' }).click();
```

---

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| `Timeout exceeded` | Element not found | Check selector, add explicit wait |
| `strict mode violation` | Multiple matches | Make selector more specific |
| `Target closed` | Navigation during action | Add `waitForNavigation` |
| Button disabled | Form invalid | Fill required fields, verify values |
| Click intercepted | Overlapping element | Scope selector to container |
| Firefox slower | Browser difference | Use 60s timeout for API waits |
