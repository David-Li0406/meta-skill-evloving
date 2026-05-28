# Testing Pyramid Reference

## Overview

The Testing Pyramid is a framework for organizing tests by scope and speed. More tests at the bottom (fast, focused), fewer at the top (slow, broad).

```
         /\
        /  \     E2E (Few)
       /----\
      /      \   Integration (Some)
     /--------\
    /          \ Unit (Many)
   /____________\
```

---

## Unit Tests

**Purpose:** Test individual functions/components in isolation

**Characteristics:**
- Fast (milliseconds)
- Deterministic
- No external dependencies (mocks/stubs for boundaries)
- Heavy domain logic coverage

**What to Test:**
- Pure functions with various inputs
- Edge cases and boundary conditions
- Error handling paths
- State transitions

**Example:**
```typescript
// Testing a pure function
describe('calculateDiscount', () => {
  it('returns 0 for orders under $50', () => {
    expect(calculateDiscount(49.99)).toBe(0);
  });

  it('returns 10% for orders $50-$100', () => {
    expect(calculateDiscount(75)).toBe(7.5);
  });

  it('returns 20% for orders over $100', () => {
    expect(calculateDiscount(150)).toBe(30);
  });
});
```

**Best Practices:**
- One assertion per test (when possible)
- Descriptive test names that read like documentation
- Arrange-Act-Assert pattern
- Test behavior, not implementation

---

## Integration Tests

**Purpose:** Verify components work together correctly

**Characteristics:**
- Medium speed (seconds)
- May use real databases/services (test instances)
- Tests module boundaries and contracts

**What to Test:**
- Database ↔ API contracts
- Service boundaries
- External API integrations
- Data flow between layers

**Example:**
```typescript
describe('UserService + UserRepository', () => {
  beforeEach(async () => {
    await testDb.reset();
  });

  it('creates user and persists to database', async () => {
    const user = await userService.createUser({
      email: 'test@example.com',
      name: 'Test User'
    });

    const persisted = await userRepository.findById(user.id);
    expect(persisted.email).toBe('test@example.com');
  });
});
```

**Best Practices:**
- Use test databases or containers (not mocks)
- Reset state between tests
- Test realistic scenarios
- Focus on contracts, not internals

---

## E2E Tests

**Purpose:** Simulate real user journeys through the entire system

**Characteristics:**
- Slow (minutes)
- Tests full stack
- Prone to flakiness
- Most expensive to maintain

**What to Test:**
- Critical user paths (sign up, login, checkout, payment)
- Happy paths first
- Cross-system flows (user action triggers email, updates dashboard)

**Example:**
```typescript
describe('Checkout Flow', () => {
  it('completes purchase successfully', async () => {
    await page.goto('/products');
    await page.click('[data-testid="add-to-cart"]');
    await page.click('[data-testid="checkout"]');
    await page.fill('#email', 'test@example.com');
    await page.fill('#card', '4242424242424242');
    await page.click('[data-testid="pay"]');

    await expect(page.locator('.success')).toBeVisible();
  });
});
```

**Best Practices:**
- Keep the suite small and focused
- Run on staging environments that mirror production
- Build in retries for flakiness
- Don't duplicate what unit/integration tests cover

---

## Human Review

**Purpose:** Catch what automation cannot

**What to Evaluate:**
1. **Functionality** — Does it work correctly?
2. **Visual** — Does it look right?
3. **Feel** — Does it feel good? (responsiveness, transitions)
4. **Accessibility** — Keyboard navigation, screen reader compatibility

**When to Do It:**
- After all automated tests pass
- Before merging to main
- On real devices when possible

---

## Test Distribution Guidelines

| Project Size | Unit | Integration | E2E |
|--------------|------|-------------|-----|
| Small | 80% | 15% | 5% |
| Medium | 70% | 20% | 10% |
| Large | 60% | 25% | 15% |

**Rule of Thumb:** If E2E tests are slow or flaky, push coverage down the pyramid.

---

## Contract Tests

For API boundaries, consider contract tests:

```typescript
// Provider side
describe('User API Contract', () => {
  it('GET /users/:id returns user schema', async () => {
    const response = await request(app).get('/users/1');
    expect(response.body).toMatchSchema(userSchema);
  });
});

// Consumer side
describe('UserClient Contract', () => {
  it('expects user schema from API', async () => {
    const user = await userClient.getUser(1);
    expect(user).toMatchSchema(userSchema);
  });
});
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Ice cream cone | More E2E than unit tests | Push coverage down |
| Testing implementation | Brittle tests | Test behavior |
| Shared state | Flaky tests | Reset between tests |
| Over-mocking | Tests don't catch real bugs | Use real dependencies when possible |
| Slow unit tests | Feedback loop broken | Remove I/O, mock boundaries |
