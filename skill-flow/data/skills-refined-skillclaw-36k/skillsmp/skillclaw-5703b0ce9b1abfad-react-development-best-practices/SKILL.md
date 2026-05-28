---
name: react-development-best-practices
description: Use this skill when you want to build maintainable and performant React applications using modern patterns, hooks, and TypeScript.
---

# React Development Best Practices

Guidelines for building scalable, maintainable, and performant React applications.

## Core Principles

- **Single Responsibility**: Each component should do one thing well.
- **Composition Over Inheritance**: Use composition with props and children instead of inheritance.
- **Props Over State**: Prefer controlled components; lift state when needed.
- **Type Everything**: Use TypeScript interfaces for all props and state.
- **Avoid Inline Functions in Render**: Use `useCallback` for event handlers passed to children.
- **Memoize Expensive Calculations**: Use `useMemo` for costly computations.
- **Key Prop Stability**: Never use array index as key for dynamic lists.
- **Error Boundaries**: Wrap major sections with error boundaries.
- **Accessibility First**: Include ARIA attributes and keyboard navigation.

## Implementation Guidelines

### Component Structure

```typescript
import { type FC, useState, useCallback, useMemo } from "react";

// Props interface with clear documentation
interface UserCardProps {
  /** User data to display */
  user: User;
  /** Called when edit button is clicked */
  onEdit?: (userId: string) => void;
  /** Additional CSS classes */
  className?: string;
}

/**
 * Displays user information in a card format.
 * Supports optional edit functionality.
 */
export const UserCard: FC<UserCardProps> = ({
  user,
  onEdit,
  className,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleEdit = useCallback(() => {
    onEdit?.(user.id);
  }, [onEdit, user.id]);

  const displayName = useMemo(
    () => `${user.firstName} ${user.lastName}`.trim(),
    [user.firstName, user.lastName]
  );

  return (
    <article className={`user-card ${className ?? ""}`}>
      <h3>{displayName}</h3>
      {onEdit && (
        <button onClick={handleEdit} aria-label={`Edit ${displayName}`}>
          Edit
        </button>
      )}
    </article>
  );
};
```

### Custom Hooks

```typescript
import { useState, useEffect } from 'react';

function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchData() {
      try {
        setLoading(true);
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');
        const result = await response.json();
        if (!cancelled) {
          setData(result);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err : new Error('Failed to fetch'));
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchData();

    return () => {
      cancelled = true; // Cleanup
    };
  }, [url]);

  return { data, loading, error };
}
```

## Anti-Patterns to Avoid

- **No Classes**: Use functional components with hooks.
- **No Prop Drilling**: Use Context or state management libraries.
- **No Nested Definitions**: Define components at the top level.
- **No Index Keys**: Use stable IDs for lists.
- **No Inline Handlers**: Define event handlers outside of the return statement.

## Related Topics

- Hooks
- State Management
- Performance Optimization