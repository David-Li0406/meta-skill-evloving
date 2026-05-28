---
name: react-best-practices
description: React + TypeScript development best practices
status: ✅ Working
last-validated: 2025-12-15
---

# React Best Practices

## Purpose
Invoked when writing or reviewing React components. Provides React + TypeScript best practices for hooks, state management, and performance optimization.

## Component Design
- Keep components small and focused (single responsibility)
- Prefer functional components over class components
- Extract reusable logic into custom hooks
- Use composition over inheritance
- Props should be immutable

## Hooks Best Practices
- Follow Rules of Hooks (only at top level, only in React functions)
- Use useState for component-specific state
- Use useReducer for complex state logic
- Use useCallback for stable function references
- Use useMemo for expensive computations
- Clean up effects with return functions

## State Management
- Keep state as local as possible
- Lift state only when needed
- Use Context for global state sparingly
- Consider state management libraries for complex apps
- Derive data instead of storing redundant state

## Performance
- Use React.memo for expensive components
- Avoid inline function definitions in render
- Use key prop correctly in lists
- Split large components into smaller ones
- Use lazy loading for route components

## Code Organization
- One component per file
- Group by feature/module, not by type
- Use index files for clean imports
- Separate business logic from UI logic
- TypeScript required for all components

## Common Pitfalls
- Don't mutate state directly
- Don't use array index as key
- Don't forget cleanup in useEffect
- Don't nest components inside render
- Don't fetch data without handling loading/error states
