---
name: e2e
description: >
  Testing E2E strategies based on Clean Architecture layers with cypress.
  Trigger: Invoke when writing tests E2E or testing user flows, verifying full integration in realistic scenarios.
license: Apache-2.0
metadata:
  author: jmgomezdev
  version: '1.0'
---

## E2E Testing Fundamentals

### What to Test with E2E:

- Critical user journeys (login, checkout, signup)
- Complex interactions (drag-and-drop, multi-step forms)
- Cross-browser compatibility
- Real API integration
- Authentication flows

### What NOT to Test with E2E:

- Unit-level logic (use unit tests)
- API contracts (use integration tests)
- Edge cases (too slow)
- Internal implementation details

## Best Practices:

### Fundamentals:

- Test user behavior, not implementation
- Keep tests independent
- Make tests deterministic
- Optimize for speed
- Use data-testid, not CSS selectors

### Test Coverage:

- Critical user paths tested (signup, login, purchase)
- Happy paths covered
- Error scenarios tested
- Edge cases included
- Mobile viewport tested

### Test Quality:

- Stable selectors (data-testid, roles)
- No arbitrary timeouts
- No test interdependencies
- Proper waits for async operations
- Clear test descriptions

### Use Stable Selectors

```typescript
// ❌ Brittle - breaks when styling changes
await page.locator('.btn-primary.large').click();
await page.locator('div > div > button:nth-child(2)').click();

// ✅ Semantic - uses accessible roles
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('test@example.com');

// ✅ Test IDs - explicit test hooks
await page.getByTestId('submit-button').click();
await page.getByTestId('email-input').fill('test@example.com');

// In your component:
<button data-testid="submit-button">Submit</button>
<input data-testid="email-input" type="email" />
```

### Mocking External Services

```typescript
// ✅ Mock API responses
test('handles API error', async ({ page }) => {
  // Intercept and mock API call
  await page.route('**/api/users', (route) => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Server error' }),
    });
  });

  await page.goto('/users');

  await expect(page.getByText('Failed to load users')).toBeVisible();
});

// ✅ Mock successful response
test('displays user list', async ({ page }) => {
  await page.route('**/api/users', (route) => {
    route.fulfill({
      status: 200,
      body: JSON.stringify({
        users: [
          { id: 1, name: 'Alice' },
          { id: 2, name: 'Bob' },
        ],
      }),
    });
  });

  await page.goto('/users');

  await expect(page.getByText('Alice')).toBeVisible();
  await expect(page.getByText('Bob')).toBeVisible();
});
```

## Resources

- [Cypress Documentation](https://www.cypress.io/)

## Keywords

`e2e`, `end-to-end`, ``.
