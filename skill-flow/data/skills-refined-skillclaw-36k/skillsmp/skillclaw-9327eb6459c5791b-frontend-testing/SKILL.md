---
name: frontend-testing
description: Use this skill when writing and reviewing frontend tests with Vitest and React Testing Library, focusing on component tests and user interactions.
---

# Skill body

## Overview

This skill provides patterns and best practices for testing frontend applications using Vitest and React Testing Library.

## Testing Philosophy

### User-Centric Testing

Test behavior, not implementation. Query elements the way users would find them.

```tsx
// BAD: Testing implementation
expect(wrapper.state('isOpen')).toBe(true);
expect(wrapper.find('.modal-class').exists()).toBe(true);

// GOOD: Testing behavior
expect(screen.getByRole('dialog')).toBeInTheDocument();
expect(screen.getByText('Modal Title')).toBeVisible();
```

### Query Priority

Use queries in this order (most to least preferred):

1. `getByRole` - Accessible to everyone
2. `getByLabelText` - Form elements
3. `getByPlaceholderText` - Inputs
4. `getByText` - Non-interactive elements
5. `getByDisplayValue` - Form current values
6. `getByAltText` - Images
7. `getByTestId` - Last resort

## Component Testing (React)

### Basic Component Test

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserCard } from './UserCard';

describe('UserCard', () => {
  const user = { id: '1', name: 'John Doe', email: 'john@example.com' };

  it('renders user information', () => {
    render(<UserCard user={user} />);

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('calls onSelect when clicked', async () => {
    const onSelect = vi.fn();
    const userEvt = userEvent.setup();

    render(<UserCard user={user} onSelect={onSelect} />);

    await userEvt.click(screen.getByRole('button'));

    expect(onSelect).toHaveBeenCalledWith(user);
  });
});

### Testing Async Components

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { UserList } from './UserList';

// Mock API
vi.mock('@/api', () => ({
  getUsers: vi.fn(),
}));

describe('UserList', () => {
  const queryClient = new QueryClient();
  // Add tests for UserList component here
});
```