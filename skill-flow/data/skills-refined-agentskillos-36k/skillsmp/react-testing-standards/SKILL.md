---
name: react-testing-standards
description: Comprehensive testing guidelines for React 19 applications with TypeScript
---

# React Testing Standards

## Testing Philosophy

### Guiding Principles

- Test user behavior, not implementation details
- Tests should resemble how users interact with your app
- Query by accessible roles and labels, not test IDs
- Integration tests over unit tests when practical
- Test the component contract, not internal state

### What to Test

**Priority High:**
- User interactions (clicks, typing, navigation)
- Conditional rendering based on props/state
- API integration and data fetching
- Form submissions and validation
- Error states and error recovery

**Priority Medium:**
- Accessibility features
- Loading states
- Edge cases and boundary conditions

**Avoid Testing:**
- Implementation details (state variable names)
- Third-party library internals
- CSS styling (use visual regression tests)
- Framework behavior (React itself)

## React Testing Library

### Query Priority

**1. Accessible Queries (Most Preferred):**
- `getByRole` - Most preferred
- `getByLabelText` - For form elements
- `getByPlaceholderText` - Alternative for inputs
- `getByText` - For non-interactive elements
- `getByDisplayValue` - For current input values

**2. Semantic Queries:**
- `getByAltText` - For images
- `getByTitle` - For title attributes

**3. Test IDs (Last Resort):**
- `getByTestId` - Only when element has no accessible role

### Query Variants

| Variant | Behavior |
|---------|----------|
| `getBy` | Throws error if not found - for elements that must exist |
| `queryBy` | Returns null if not found - for asserting non-existence |
| `findBy` | Returns promise - for async elements that appear later |

### User Interactions

**Library:** Use @testing-library/user-event, not fireEvent

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('user can type in input', async () => {
  const user = userEvent.setup();
  render(<SearchBox />);

  const input = screen.getByRole('textbox');
  await user.type(input, 'Hello');

  expect(input).toHaveValue('Hello');
});
```

**Common Interactions:**
- `user.click()` - Click elements
- `user.type()` - Type in inputs
- `user.clear()` - Clear input values
- `user.selectOptions()` - Select dropdown options
- `user.upload()` - Upload files

## Test Structure

### Anatomy

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  test('describes expected behavior', async () => {
    // Arrange - Set up test data and render
    const user = userEvent.setup();
    render(<ComponentName prop="value" />);

    // Act - Perform user interactions
    const button = screen.getByRole('button', { name: /click me/i });
    await user.click(button);

    // Assert - Verify expected outcomes
    expect(screen.getByText(/success/i)).toBeInTheDocument();
  });
});
```

### Best Practices

- One logical assertion per test
- Descriptive test names (what behavior is tested)
- Arrange-Act-Assert pattern
- Avoid beforeEach for test setup (makes tests less clear)
- Use async/await for user interactions

## Testing Patterns

### Component Rendering

**Basic:**
```tsx
test('renders with correct props', () => {
  render(<UserCard name="John" email="john@example.com" />);

  expect(screen.getByText('John')).toBeInTheDocument();
  expect(screen.getByText('john@example.com')).toBeInTheDocument();
});
```

**Conditional:**
```tsx
test('shows loading state', () => {
  render(<DataDisplay isLoading={true} />);

  expect(screen.getByRole('progressbar')).toBeInTheDocument();
});
```

### User Interactions

**Button Click:**
```tsx
test('increments counter on click', async () => {
  const user = userEvent.setup();
  render(<Counter />);

  const button = screen.getByRole('button', { name: /increment/i });
  await user.click(button);

  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});
```

**Form Submission:**
```tsx
test('submits form with user data', async () => {
  const handleSubmit = jest.fn();
  const user = userEvent.setup();
  render(<LoginForm onSubmit={handleSubmit} />);

  await user.type(screen.getByLabelText(/email/i), 'user@example.com');
  await user.type(screen.getByLabelText(/password/i), 'password123');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  expect(handleSubmit).toHaveBeenCalledWith({
    email: 'user@example.com',
    password: 'password123',
  });
});
```

### Async Operations

**Data Fetching:**
```tsx
test('displays fetched data', async () => {
  render(<UserList />);

  // Wait for loading to finish
  expect(screen.getByText(/loading/i)).toBeInTheDocument();

  // Wait for data to appear
  const users = await screen.findAllByRole('listitem');
  expect(users).toHaveLength(3);
});
```

**With waitFor:**
```tsx
test('shows success message after submission', async () => {
  const user = userEvent.setup();
  render(<ContactForm />);

  await user.click(screen.getByRole('button', { name: /submit/i }));

  await waitFor(() => {
    expect(screen.getByText(/thank you/i)).toBeInTheDocument();
  });
});
```

### Error Handling

```tsx
test('displays error message on failure', async () => {
  // Mock API to return error
  jest.spyOn(api, 'fetchUser').mockRejectedValue(new Error('Failed'));

  render(<UserProfile userId="123" />);

  const errorMessage = await screen.findByText(/failed to load/i);
  expect(errorMessage).toBeInTheDocument();
});
```

## Mocking

### External Dependencies

**API Calls:**
```tsx
// Mock API module
jest.mock('@/lib/api', () => ({
  fetchUsers: jest.fn(),
}));

test('renders users from API', async () => {
  const mockUsers = [{ id: 1, name: 'Alice' }];
  fetchUsers.mockResolvedValue(mockUsers);

  render(<UserList />);

  expect(await screen.findByText('Alice')).toBeInTheDocument();
});
```

**React Query:**
```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function renderWithQueryClient(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>
  );
}
```

### What NOT to Mock

**Avoid:**
- React hooks (useState, useEffect, etc.)
- Component implementation details
- Child components (test integration instead)

**Acceptable:**
- External API calls
- Browser APIs (localStorage, fetch)
- Third-party libraries with side effects
- Date/time functions (Date.now())

## Accessibility Testing

### Practices

- Query by role (getByRole) enforces ARIA compliance
- Test keyboard navigation
- Verify focus management
- Check alt text on images

```tsx
test('button is keyboard accessible', async () => {
  const user = userEvent.setup();
  render(<Dialog />);

  // Tab to button
  await user.tab();
  expect(screen.getByRole('button')).toHaveFocus();

  // Activate with Enter
  await user.keyboard('{Enter}');
  expect(screen.getByRole('dialog')).toBeInTheDocument();
});
```

## Test Organization

### File Structure

- `ComponentName.test.tsx` - Component tests
- `utils.test.ts` - Utility function tests
- `__tests__/` directory - Alternative structure

### Describe Blocks

```tsx
describe('LoginForm', () => {
  describe('validation', () => {
    test('shows error for invalid email', () => {});
    test('shows error for short password', () => {});
  });

  describe('submission', () => {
    test('calls onSubmit with form data', () => {});
    test('shows success message after submit', () => {});
  });
});
```

## Coverage Guidelines

### Requirements

| Area | Coverage |
|------|----------|
| Critical paths | 100% |
| Components | 80%+ |
| Utilities | 90%+ |

### What to Prioritize

- User-facing features
- Business logic and calculations
- Error handling paths
- Form validation

### Acceptable Gaps

- Pure presentation components
- Third-party library wrappers
- Type definitions

## Common Pitfalls

### Avoid

- Testing implementation details (state names, effect calls)
- Snapshot tests for everything (brittle and uninformative)
- Using getByTestId as primary query method
- Not awaiting async operations
- Asserting on intermediate loading states

### Instead

- Test public API and user-visible behavior
- Snapshots only for static content that changes infrequently
- Query by role/label for accessibility
- Always await user events and async queries
- Assert on final rendered state

## CI Integration

### Requirements

- All tests must pass before merge
- Coverage reports generated and tracked
- Tests run on every pull request
- Fast test execution (< 5 minutes for unit/integration)
