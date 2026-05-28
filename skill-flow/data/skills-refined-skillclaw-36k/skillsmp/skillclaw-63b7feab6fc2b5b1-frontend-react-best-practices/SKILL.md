---
name: frontend-react-best-practices
description: Use this skill when you need to implement robust, maintainable, and performant frontend code in React, following best practices for component design, state management, and data flow.
---

# Skill body

## Overview

This skill outlines best practices for developing frontend applications using React, focusing on component design, state management, and data flow. It emphasizes the use of TypeScript for type safety and accessibility considerations.

## Component Design

### General Rules
- Use **Function Components** exclusively; avoid class components.
- Follow the **Single Responsibility Principle**: each component should have one responsibility.
- Use **Props** to pass data; define prop types clearly.

### Composition Patterns
- Utilize composition for building UI components. For example:
  ```typescript
  function Card({ children }: { children: React.ReactNode }) {
    return <div className="card">{children}</div>;
  }
  ```

### Naming Conventions
- Component names should be in **PascalCase**.
- Props and variable names should be in **camelCase**.

### Accessibility
- Ensure all components are accessible by using ARIA attributes and semantic HTML.
- Consider keyboard navigation in your designs.

## State Management

### Local State
- Use `useState` for local component state.
- For shared state, consider using the **Context API** or **custom hooks**.

### Custom Hooks
- Create custom hooks for reusable logic. Always prefix with `use`.
- Example of a custom hook for data fetching:
  ```typescript
  function useQuery<T>(fetcher: () => Promise<T>) {
    const [data, setData] = useState<T | null>(null);
    const [error, setError] = useState<Error | null>(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
      let cancelled = false;
      fetcher()
        .then(result => { if (!cancelled) setData(result); })
        .catch(err => { if (!cancelled) setError(err); })
        .finally(() => { if (!cancelled) setLoading(false); });
      return () => { cancelled = true; };
    }, []);
    
    return { data, error, loading };
  }
  ```

## Data Flow

### Unidirectional Data Flow
- Maintain a single source of truth for state.
- Data should flow down from parent to child components via props.

### Immutable State Updates
- Always use immutable patterns for state updates:
  ```typescript
  setUsers(prev => [...prev, newUser]); // Correct
  ```

## Error Handling
- Implement error boundaries for components that may fail.
- Handle loading, error, and empty states explicitly in your UI.

## Type Safety
- Use TypeScript with strict mode to ensure type safety across your application.
- Avoid using `any`; prefer `unknown` and narrow down types as needed.

## Testing
- Write tests for your components and hooks to ensure they behave as expected.
- Use libraries like `@testing-library/react` for testing React components.

## Conclusion
By following these best practices, you can create React applications that are not only functional but also maintainable and accessible, ensuring a better experience for both developers and users.