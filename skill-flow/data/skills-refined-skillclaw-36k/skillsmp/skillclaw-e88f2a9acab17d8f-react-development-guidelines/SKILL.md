---
name: react-development-guidelines
description: Use this skill when you need comprehensive guidelines for developing, implementing, and testing React 19 applications with TypeScript.
---

# Skill body

## React Development Guidelines

### Code Review Guidelines

#### Component Architecture

**Red Flags:**
- 'use client' on components that don't use hooks or browser APIs
- Server Components trying to use hooks
- Client Components doing data fetching that should be on the server

**Good Practices:**
- Use Server Components for data fetching and static content.
- Use 'use client' only when necessary (hooks, events, browser APIs).
- Ensure Client Components receive data as props from Server Components.

#### TypeScript Usage

**Issues:**
- Use of 'any' without explanation.
- Type assertions without justification.
- Missing prop types and return types.

**Best Practices:**
- Define all props with interfaces.
- Use generic types for reusable components.
- Implement discriminated unions for complex state.

### Component Implementation

#### Default Approach

- Start with Server Components by default.
- Use TypeScript for all components.
- Define prop types with interfaces and export components as named exports.

#### Server Components Example

```tsx
interface UserProfileProps {
  userId: string;
}

export async function UserProfile({ userId }: UserProfileProps) {
  const user = await fetchUser(userId);
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

#### Client Components Example

```tsx
'use client';

import { useState } from 'react';

interface CounterProps {
  initialCount?: number;
}

export function Counter({ initialCount = 0 }: CounterProps) {
  const [count, setCount] = useState(initialCount);
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

### State Management

#### Local State

- Use `useState` for simple values and `useReducer` for complex state logic.

#### Shared State

- Lift state to a common ancestor or use Context for deep prop threading.
- Consider Zustand for global state management.

### Testing Guidelines

#### Testing Philosophy

- Test user behavior, not implementation details.
- Use accessible queries and prioritize integration tests.

#### What to Test

**Priority High:**
- User interactions, conditional rendering, API integration, form submissions.

**Avoid Testing:**
- Implementation details, third-party library internals, CSS styling.

#### React Testing Library

**Query Priority:**
1. Accessible Queries (e.g., `getByRole`)
2. Semantic Queries (e.g., `getByAltText`)
3. Test IDs (last resort)

**User Interactions Example:**

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