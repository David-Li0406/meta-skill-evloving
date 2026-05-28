---
name: ensuring-mobile-standards
description: Ensure consistent code quality, style, and best practices for mobile apps. Use when writing code, reviewing PRs, or setting up linting.
---

# Mobile App Coding Standards

## When to use this skill
- When writing new code or refactoring existing code.
- During code reviews to check for adherence to standards.
- When configuring linting or formatting rules.
- When creating new components to ensure they meet quality guidelines.

## Code Style
- **Type Checking**: Use TypeScript (React Native) or Dart (Flutter) with strict type checking enabled. Avoid `any`.
- **Linting**: Follow established rules (ESLint/Prettier for JS/TS, Dart Analyzer for Dart).
- **Naming Conventions**:
    - Use `PascalCase` for Components, Classes, and Types.
    - Use `camelCase` for variables, functions, and hooks.
    - Use `UPPER_CASE` for constants.
    - Use meaningful, descriptive names (e.g., `fetchUserData` instead of `getData`).
- **Documentation**: Add JSDoc/DartDoc comments for complex functions, interfaces, and public APIs.

## Component Guidelines
- **Functional Components**: Prefer functional components with hooks over class components in React Native.
- **Typed Props**: Define props interfaces for all components.
- **Size Limit**: Keep components small and focused. Aim for <300 lines. Split larger components into smaller sub-components.
- **Logic Extraction**: Move complex business logic, data fetching, and side effects into custom hooks or services. Keep the UI layer dumb.

## State Management
- **Tooling**: Use the agreed-upon state manager (e.g., Redux Toolkit, Context API, Riverpod).
- **Structure**: Keep state normalized (avoid deep nesting).
- **Actions**: Use descriptive action names that describe *what happened* (e.g., `userLoggedIn`), not *what to do*.
- **Async Handling**: Handle loading, error, and success states explicitly for all async operations.

## API Integration
- **Async/Await**: Use `async`/`await` syntax for cleaner asynchronous code.
- **Error Handling**: Implement `try/catch` blocks and handle errors gracefully. Display user-friendly error messages.
- **Interceptors**: Use request/response interceptors for common tasks like adding auth tokens or logging errors.
- **Resilience**: Handle network failures and offline states.

## Performance
- **Lazy Loading**: Lazy load heavy components or screens to improve initial startup time.
- **Assets**: Optimize images and use proper formats (WebP, SVG).
- **Rendering**: Avoid unnecessary re-renders. Use `React.memo`, `useMemo`, and `useCallback` appropriately (but don't premature optimize).
- **Lists**: Use `FlatList` or `SectionList` for long lists with `removeClippedSubviews`.
