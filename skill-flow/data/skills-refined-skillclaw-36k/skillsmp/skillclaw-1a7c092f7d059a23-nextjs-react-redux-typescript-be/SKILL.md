---
name: nextjs-react-redux-typescript-best-practices
description: Use this skill when developing maintainable and scalable applications with Next.js, React, Redux Toolkit, and TypeScript, following best practices and guidelines.
---

# Next.js, React, Redux Toolkit, and TypeScript Best Practices

This skill provides comprehensive guidelines for building maintainable and scalable applications using Next.js, React, Redux Toolkit, and TypeScript.

## Development Philosophy

- Produce maintainable, scalable code following SOLID principles.
- Favor functional and declarative approaches over imperative styles.
- Prioritize type safety and static analysis.
- Embrace component-driven architecture.

## Code Style Standards

- **Indentation**: Use tabs.
- **Strings**: Use single quotes (unless escaping needed).
- **Semicolons**: Omit unless disambiguation required.
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
- **Booleans**: verbs (e.g., `isLoading`, `hasError`, `canSubmit`).
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
- Leverage automatic cache invalidation.
- Implement optimistic updates when appropriate.

### TypeScript Integration

- Enable strict mode.
- Define clear interfaces for props and Redux state structure.
- Apply generics where type flexibility is needed.
- Prefer interfaces over types for object structures.
- Use typed hooks (`useAppDispatch`, `useAppSelector`).

## Next.js Best Practices

### Core

- Use App Router for routing.
- Implement metadata management.
- Apply proper caching strategies.
- Implement error boundaries.

### Components

- Use built-in components: `Image`, `Link`, `Script`, `Head`.
- Implement loading states.
- Use appropriate data fetching methods.