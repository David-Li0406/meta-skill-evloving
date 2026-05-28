---
name: react-testing
description: Use this skill when testing React applications with the React Testing Library, focusing on components, hooks, and context.
---

# Skill body

## React Testing Library

This skill focuses on React-specific testing patterns. For general DOM testing patterns (queries, userEvent, async, accessibility), load the `front-end-testing` skill. For TDD workflow, load the `tdd` skill.

---

## Testing React Components

**React components are just functions that return JSX.** Test them like functions: inputs (props) → output (rendered DOM).

### Basic Component Testing

```tsx
// ✅ CORRECT - Test component behavior
it('should display user name when provided', () => {
  render(<UserProfile name="Alice" email="alice@example.com" />);

  expect(screen.getByText(/alice/i)).toBeInTheDocument();
  expect(screen.getByText(/alice@example.com/i)).toBeInTheDocument();
});
```

```tsx
// ❌ WRONG - Testing implementation
it('should set name state', () => {
  const wrapper = mount(<UserProfile name="Alice" />);
  expect(wrapper.state('name')).toBe('Alice'); // Internal state!
});
```

### Testing Props

```tsx
// ✅ CORRECT - Test how props affect rendered output
it('should call onSubmit when form submitted', async () => {
  const handleSubmit = vi.fn();
  const user = userEvent.setup();

  render(<LoginForm onSubmit={handleSubmit} />);

  await user.type(screen.getByLabelText(/email/i), 'test@example.com');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  expect(handleSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
  });
});
```

### Testing Conditional Rendering

```tsx
// ✅ CORRECT - Test what user sees in different states
it('should show error message when login fails', async () => {
  server.use(
    http.post('/api/login', () => {
      return HttpResponse.json({ error: 'Invalid credentials' }, { status: 401 });
    })
  );

  const user = userEvent.setup();
  render(<LoginForm />);

  await user.type(screen.getByLabelText(/email/i), 'wrong@example.com');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  await screen.findByText(/invalid credentials/i);
});
```

---

## Testing React Hooks

### Custom Hooks with renderHook

**Built into React Testing Library** (since v13):

```tsx
import { renderHook } from '@testing-library/react';

it('should toggle value', () => {
  const { result } = renderHook(() => useToggle(false));

  expect(result.current.value).toBe(false);

  act(() => {
    result.current.toggle();
  });

  expect(result.current.value).toBe(true);
});
```