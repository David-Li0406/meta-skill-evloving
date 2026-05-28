---
name: front-end-testing
description: Use this skill when you need to implement behavior-driven UI testing patterns with the DOM Testing Library across various front-end frameworks.
---

# Front-End Testing with DOM Testing Library

This skill focuses on framework-agnostic DOM Testing Library patterns that work across React, Vue, Svelte, and other frameworks. For React-specific patterns (renderHook, context, components), load the `react-testing` skill. For TDD workflow (RED-GREEN-REFACTOR), load the `tdd` skill. For general testing patterns (factories, public API testing), load the `testing` skill.

## Core Philosophy

**Test behavior users see, not implementation details.**

Testing Library exists to solve a fundamental problem: tests that break when you refactor (false negatives) and tests that pass when bugs exist (false positives).

### Two Types of Users

Your UI components have two users:
1. **End-users**: Interact through the DOM (clicks, typing, reading text)
2. **Developers**: You, refactoring implementation

**Kent C. Dodds principle**: "The more your tests resemble the way your software is used, the more confidence they can give you."

### Why This Matters

**False negatives** (tests break on refactor):
```typescript
// ❌ WRONG - Testing implementation (will break on refactor)
it('should update internal state', () => {
  const component = new CounterComponent();
  component.setState({ count: 5 }); // Coupled to state implementation
  expect(component.state.count).toBe(5);
});
```

**False positives** (bugs pass tests):
```typescript
// ❌ WRONG - Testing wrong thing
it('should render button', () => {
  render('<button data-testid="submit-btn">Submit</button>');
  expect(screen.getByTestId('submit-btn')).toBeInTheDocument();
  // Button exists but onClick is broken - test passes!
});
```

**Correct approach** (behavior-driven):
```typescript
// ✅ CORRECT - Testing user-visible behavior
it('should submit form when user clicks submit', async () => {
  const handleSubmit = vi.fn();
  const user = userEvent.setup();

  render(`
    <form id="login-form">
      <label>Email: <input name="email" /></label>
      <label>Password: <input name="password" type="password" /></label>
      <button type="submit">Submit</button>
    </form>
  `);

  document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    handleSubmit(new FormData(e.target));
  });

  await user.type(screen.getByLabelText(/email/i), 'user@example.com');
  await user.type(screen.getByLabelText(/password/i), 'password123');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  expect(handleSubmit).toHaveBeenCalledWith(expect.any(FormData));
});
```