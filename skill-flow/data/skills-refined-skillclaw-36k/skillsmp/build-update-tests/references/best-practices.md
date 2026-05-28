# Best Practices

Testing best practices, common patterns, and guidelines.

## Pattern Compliance Priority

When evaluating and creating tests, check patterns in this order:

### P0 - MUST FIX (Safety & Correctness)

- No direct database INSERTs in E2E (playwright-best-practices.md Pattern #2)
- Proper async handling (testing-patterns.md Pattern #1, #2)
- Worker validation in E2E (playwright-best-practices.md Pattern #4)
- ONE test per user journey (playwright-best-practices.md Pattern #1)

### P1 - SHOULD FIX (Maintainability)

- test.step() organization (playwright-best-practices.md Pattern #1)
- Proper cleanup (playwright-best-practices.md Pattern #5)
- Comprehensive assertions (not just existence checks)
- Testing behavior over implementation

### P2 - NICE TO HAVE (Best Practices)

- Test naming conventions
- Describe block organization
- Helper function usage
- Code comments in tests

**CRITICAL**: Fix P0 pattern violations BEFORE creating new tests. A test that violates patterns is worse than no test.

---

## When Integration Tests Are Needed

**REQUIRED for**:
- Services interacting with real database
- Multiple services coordinating
- Background jobs/workers involved
- Complex data transformations
- Transaction management
- Caching behavior

**NOT NEEDED for**:
- Simple CRUD operations (covered by E2E)
- Pure functions (covered by unit tests)
- Thin wrappers around libraries

---

## When E2E Tests Are Needed

**REQUIRED for**:
- Complete user workflows (form -> submit -> persistence)
- Automation triggers (user action -> worker processes -> result)
- Multi-step processes (add -> edit -> delete)
- Critical business flows (checkout, payment, etc.)
- User-facing forms and components

**NOT NEEDED for**:
- Display-only components (covered by unit tests)
- Utility functions
- Internal helpers
- Non-user-facing code

---

## React Component Testing

### Setup

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
```

### Provider Wrapper

```typescript
const renderComponent = (props = {}) => {
  return render(
    <QueryClientProvider client={queryClient}>
      <AuthContext.Provider value={mockAuth}>
        <MyComponent {...defaultProps} {...props} />
      </AuthContext.Provider>
    </QueryClientProvider>
  );
};
```

### User Interactions

```typescript
const user = userEvent.setup();
await user.click(screen.getByRole('button', { name: 'Submit' }));
await user.type(screen.getByLabelText('Email'), 'test@example.com');
```

### Async Updates

```typescript
await waitFor(() => {
  expect(screen.getByText('Success!')).toBeInTheDocument();
});
```

---

## Service Testing

### Mock External Dependencies

```typescript
vi.mock('@/integrations/supabase/client');

const mockSupabase = {
  from: vi.fn(() => ({
    select: vi.fn().mockResolvedValue({ data: [], error: null })
  }))
};
```

### Test Return Values

```typescript
it('returns data and null error on success', async () => {
  const result = await myService.fetchData();
  expect(result).toEqual({ data: [...], error: null });
});
```

### Test Error Handling

```typescript
it('returns null data and error message on failure', async () => {
  mockSupabase.from.mockRejectedValue(new Error('Network error'));
  const result = await myService.fetchData();
  expect(result).toEqual({ data: null, error: 'Network error' });
});
```

---

## Utility Testing

### Test Thoroughly

```typescript
describe('formatCurrency', () => {
  it('formats USD correctly', () => {
    expect(formatCurrency(1234.56, 'USD')).toBe('$1,234.56');
  });

  it('handles zero', () => {
    expect(formatCurrency(0, 'USD')).toBe('$0.00');
  });

  it('handles negative numbers', () => {
    expect(formatCurrency(-100, 'USD')).toBe('-$100.00');
  });
});
```

### Test Edge Cases

- Null/undefined inputs
- Empty arrays/objects
- Boundary values
- Invalid inputs

---

## Common Patterns

### Mocking TanStack Query Hooks

```typescript
vi.mock('@/hooks/useMyQuery');

beforeEach(() => {
  vi.mocked(useMyQuery).mockReturnValue({
    data: mockData,
    isLoading: false,
    error: null
  });
});
```

### Mocking Form Submission

```typescript
it('submits form with correct data', async () => {
  const mockSubmit = vi.fn();
  const user = userEvent.setup();

  render(<MyForm onSubmit={mockSubmit} />);

  await user.type(screen.getByLabelText('Name'), 'John Doe');
  await user.click(screen.getByRole('button', { name: 'Submit' }));

  expect(mockSubmit).toHaveBeenCalledWith({
    name: 'John Doe'
  });
});
```

### Testing Conditional Rendering

```typescript
it('shows error message when validation fails', async () => {
  const user = userEvent.setup();
  render(<MyForm />);

  await user.click(screen.getByRole('button', { name: 'Submit' }));

  expect(screen.getByText('Name is required')).toBeInTheDocument();
});

it('hides error message when field is filled', async () => {
  const user = userEvent.setup();
  render(<MyForm />);

  await user.click(screen.getByRole('button', { name: 'Submit' }));
  expect(screen.getByText('Name is required')).toBeInTheDocument();

  await user.type(screen.getByLabelText('Name'), 'John');

  expect(screen.queryByText('Name is required')).not.toBeInTheDocument();
});
```

---

## Error Handling

### File Not Found

- Verify the file path with the user
- Check if file was moved or renamed

### Can't Determine What to Test

- Ask user for clarification on expected behavior
- Request requirements documentation
- Focus on obvious user-facing functionality

### Tests Fail After Creation

Analyze failures carefully. Determine if failure indicates:
- Test bug -> Fix the test
- Source code bug -> Report to user
- Missing context -> Ask user

### Circular Dependencies or Complex Mocking

- Report difficulty to user
- Suggest code refactoring for better testability
- Create tests for what's testable now

---

## Success Criteria

A successful test suite should:

1. Cover all P0 critical paths (100%)
2. Cover most P1 important functionality (80%+)
3. Have clear, descriptive test names
4. Use proper mocking for external dependencies
5. Pass consistently (no flaky tests)
6. Follow project conventions
7. Be maintainable (easy to update when code changes)

---

## Key Principles

- **Fix before Create**: Always fix pattern violations in existing tests BEFORE creating new tests
- **P0 First**: Critical functionality must be tested before nice-to-haves
- **Quality over Quantity**: 10 comprehensive tests better than 50 shallow ones
- **Tests as Documentation**: Anyone reading tests should understand what the code does
- **Behavior over Implementation**: Test user-visible behavior, not internal details
- **Pattern Compliance is Non-Negotiable**: A test that violates patterns is worse than no test
