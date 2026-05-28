---
name: nextjs-react-redux-typescript-best-practices
description: Use this skill for comprehensive guidelines on developing maintainable applications with Next.js, React, Redux Toolkit, and TypeScript.
---

# Next.js React Redux TypeScript Best Practices

This document provides a unified set of guidelines for building maintainable, scalable applications using Next.js, React, Redux Toolkit, and TypeScript.

## Development Philosophy

- Produce clean, maintainable, and scalable code following SOLID principles.
- Favor functional and declarative programming patterns.
- Prioritize type safety and static analysis.
- Embrace component-driven architecture.

## Code Style Standards

- **Indentation**: Use tabs.
- **Strings**: Use single quotes (unless escaping is needed).
- **Semicolons**: Omit unless disambiguation is required.
- **Operators**: Space around infix operators.
- **Functions**: Space before declaration parentheses.
- **Equality**: Always use `===` over `==`.
- **Line length**: Maximum 80 characters.
- **Conditionals**: Use braces for multi-line if statements.
- **Collections**: Trailing commas in multiline arrays/objects.

## Naming Conventions

| Convention | Usage |
|------------|-------|
| PascalCase | Components, type definitions, interfaces |
| kebab-case | Directory and file names (e.g., `user-profile.tsx`) |
| camelCase | Variables, functions, methods, hooks, properties, props |
| UPPERCASE | Environment variables, constants, global configurations |

### Prefixes

- **Event handlers**: `handle` (e.g., `handleClick`).
- **Booleans**: verbs (e.g., `isLoading`, `hasError`).
- **Custom hooks**: `use` (e.g., `useAuth`, `useForm`).

## React Best Practices

### Components

- Use functional components with TypeScript interfaces.
- Define components using the `function` keyword.
- Extract reusable logic into custom hooks.
- Apply composition patterns properly.
- Leverage `React.memo()` strategically.
- Implement cleanup in `useEffect` hooks.

### Performance

- Use `useCallback` for memoizing functions.
- Apply `useMemo` for expensive computations.
- Avoid inline function definitions in JSX.
- Implement code splitting via dynamic imports.
- Use proper `key` props in lists (never use index).

## Redux Toolkit Best Practices

### Core Principles

- Implement Redux Toolkit for global state management.
- Use `createSlice` to define state, reducers, and actions together.
- Normalize state structure to prevent deeply nested data.
- Employ selectors to encapsulate state access.
- Separate concerns by feature; avoid monolithic slices.

### Async Operations

- Use RTK Query for data fetching and caching.
- Define API slices with endpoints.
- Implement optimistic updates when appropriate.

## TypeScript Implementation

- Enable strict mode.
- Define clear interfaces for props, state, and Redux structure.
- Use type guards for undefined/null safety.
- Apply generics for flexibility.
- Prefer `interface` over `type` for objects.

## Error Handling and Validation

### Forms

- Use Zod for schema validation.
- Integrate with React Hook Form for form management.
- Provide clear error messaging.

### Error Boundaries

- Catch and handle React tree errors gracefully.
- Log errors to external services (e.g., Sentry).
- Display user-friendly fallback UIs.

## Testing

### Unit Testing

- Use Jest and React Testing Library.
- Follow the Arrange-Act-Assert pattern.
- Mock external dependencies and API calls.

### Integration Testing

- Focus on user workflows.
- Proper test environment setup/teardown.
- Selective snapshot testing.

## Accessibility (a11y)

- Use semantic HTML and accurate ARIA attributes.
- Ensure full keyboard navigation and proper focus management.
- Maintain accessible color contrast and logical heading hierarchy.

## Security

- Implement input sanitization to prevent XSS.
- Use DOMPurify for HTML sanitization.
- Apply proper authentication methods.

## Internationalization (i18n)

- Use `next-i18next` for translations.
- Implement locale detection and formatting.

## Documentation

- Use JSDoc for all public functions, classes, methods, and interfaces.
- Write clear, concise descriptions with proper markdown formatting.