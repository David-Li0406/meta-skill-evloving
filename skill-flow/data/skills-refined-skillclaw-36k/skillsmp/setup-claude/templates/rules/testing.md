# Testing Rules

Test requirements and conventions for quality assurance.

## Always Do

- **Write tests for new features** - No feature is complete without tests
- **Test edge cases** - Empty inputs, null values, boundaries
- **Test error cases** - Verify errors are thrown and handled
- **Use descriptive test names** - Should read like documentation
- **Keep tests independent** - No test should depend on another
- **Use appropriate test types** - Unit, integration, e2e for different needs
- **Mock external services** - Don't call real APIs in unit tests
- **Run tests before committing** - Never commit broken tests
- **Maintain test fixtures** - Keep test data up to date
- **Test the public API** - Focus on behavior, not implementation

## Never Do

- ❌ **Skip tests for "simple" code** - Simple code can still break
- ❌ **Test implementation details** - Tests break on refactor
- ❌ **Use real services in unit tests** - Too slow, unreliable
- ❌ **Write flaky tests** - Fix or delete them
- ❌ **Ignore failing tests** - Fix immediately or revert
- ❌ **Test getters/setters** - No value in trivial tests
- ❌ **Use sleeps for timing** - Use proper async handling
- ❌ **Share state between tests** - Leads to flaky tests
- ❌ **Test third-party code** - Trust libraries, test integration

## Test Naming Convention

Format: `should [expected behavior] when [condition]`

```typescript
// Good names
it('should return empty array when no users match filter')
it('should throw ValidationError when email is invalid')
it('should retry 3 times when API returns 500')

// Bad names
it('test user filter')
it('works')
it('handles error')
```

## Test Structure

Use Arrange-Act-Assert (AAA) pattern:

```typescript
it('should calculate total with discount', () => {
  // Arrange - set up test data
  const cart = new Cart();
  cart.addItem({ price: 100, quantity: 2 });
  const discount = { type: 'percentage', value: 10 };

  // Act - perform the action
  const total = cart.calculateTotal(discount);

  // Assert - verify the result
  expect(total).toBe(180); // 200 - 10%
});
```

## Test Types

### Unit Tests

Test individual functions/classes in isolation.

```typescript
// user-service.test.ts
describe('UserService', () => {
  describe('validateEmail', () => {
    it('should return true for valid email', () => {
      expect(validateEmail('user@example.com')).toBe(true);
    });

    it('should return false for invalid email', () => {
      expect(validateEmail('not-an-email')).toBe(false);
    });
  });
});
```

### Integration Tests

Test multiple components working together.

```typescript
// user-api.integration.test.ts
describe('User API', () => {
  it('should create user and send welcome email', async () => {
    const user = await createUser({ email: 'test@example.com' });

    expect(user.id).toBeDefined();
    expect(emailService.sentEmails).toContainEqual(
      expect.objectContaining({
        to: 'test@example.com',
        subject: 'Welcome!'
      })
    );
  });
});
```

### End-to-End Tests

Test complete user flows.

```typescript
// checkout.e2e.test.ts
describe('Checkout Flow', () => {
  it('should complete purchase successfully', async () => {
    await page.goto('/products');
    await page.click('[data-testid="add-to-cart"]');
    await page.click('[data-testid="checkout"]');
    await page.fill('[name="card"]', '4242424242424242');
    await page.click('[data-testid="pay"]');

    await expect(page.locator('.success-message')).toBeVisible();
  });
});
```

## Mocking Guidelines

### When to Mock

- External APIs
- Database calls (in unit tests)
- Time-dependent code
- Random number generation
- File system operations

### When NOT to Mock

- The code under test
- Simple utility functions
- Data transformations

### Mock Example

```typescript
// Good mock usage
const mockApi = {
  getUser: vi.fn().mockResolvedValue({ id: '1', name: 'Alice' })
};

const service = new UserService(mockApi);
const user = await service.fetchUser('1');

expect(mockApi.getUser).toHaveBeenCalledWith('1');
expect(user.name).toBe('Alice');
```

## Test Coverage

### Coverage Goals

- **Statements**: 80%+ for new code
- **Branches**: 75%+ (test both if/else paths)
- **Functions**: 90%+ for public APIs

### What to Prioritize

1. Business logic
2. Error handling paths
3. Edge cases
4. Security-critical code

### What's OK to Skip

- Generated code
- Simple getters/setters
- Framework boilerplate
- Configuration files

## Examples

### Testing Async Code

**Good**:
```typescript
it('should fetch user successfully', async () => {
  const user = await userService.getUser('123');
  expect(user).toEqual({ id: '123', name: 'Alice' });
});

it('should throw when user not found', async () => {
  await expect(userService.getUser('999'))
    .rejects.toThrow(NotFoundError);
});
```

### Testing Error Handling

**Good**:
```typescript
describe('when API returns error', () => {
  beforeEach(() => {
    mockApi.getUser.mockRejectedValue(new Error('Network error'));
  });

  it('should throw ApiError', async () => {
    await expect(service.fetchUser('1'))
      .rejects.toThrow(ApiError);
  });

  it('should log the error', async () => {
    try {
      await service.fetchUser('1');
    } catch {}

    expect(logger.error).toHaveBeenCalled();
  });
});
```

## Exceptions

1. **Prototypes/spikes** - Quick experiments may skip tests
2. **Scripts** - One-off scripts may have minimal tests
3. **UI-only changes** - Pure styling may not need unit tests
4. **Emergency hotfixes** - Add tests immediately after
