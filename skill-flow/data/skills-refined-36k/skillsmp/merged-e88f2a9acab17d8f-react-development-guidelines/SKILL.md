---
name: react-development-guidelines
description: Use this skill for comprehensive guidelines on implementing, reviewing, and testing React 19 applications with TypeScript.
---

# React Development Guidelines

## Code Review Guidelines

### Component Architecture

#### Server vs Client

**Red Flags:**
- 'use client' on components that don't use hooks or browser APIs
- Server Components trying to use hooks
- Client Components performing data fetching that should be on the server

**Good Practices:**
- Use Server Components for data fetching and static content
- Apply 'use client' only when necessary (hooks, events, browser APIs)
- Ensure Client Components receive data as props from Server Components

#### Component Structure

**Issues:**
- Components exceeding 300 lines (consider splitting)
- Multiple responsibilities within a single component
- Deeply nested component trees (> 5 levels)
- Repeated code that could be extracted to hooks

**Look For:**
- Adherence to the single responsibility principle
- Proper component composition
- Use of custom hooks for reusable logic

### TypeScript Usage

#### Type Safety

**Issues:**
- Use of 'any' without explanation
- Type assertions without justification
- Non-null assertions without null checks
- Missing prop types

**Best Practices:**
- Define all props with interfaces
- Use generic types for reusable components
- Implement discriminated unions for complex state

#### Naming

**Check:**
- PascalCase for components and types
- camelCase for variables and functions
- Descriptive names (avoid single letters except in maps)
- Prefix hooks with 'use'

### State Management

#### React State

**Issues:**
- Using state for derived values (use useMemo instead)
- Prop drilling more than 2 levels (consider Context)
- State that could be computed from props

**Patterns:**
- Use `useState` for local UI state
- Use `useReducer` for complex state logic
- Use Context for deeply nested props
- Use Zustand for global client state
- Use React Query for server state

### Performance

#### Optimization

**Unnecessary Optimization:**
- Using React.memo on simple components
- Using useMemo for cheap calculations

**Missing Optimization:**
- Expensive calculations without useMemo
- Functions recreated on every render passed to children

### Error Handling

**Common Issues:**
- Missing error handling for async operations
- No loading states for data fetching
- Silent error catching (empty catch blocks)

**Good Practices:**
- Handle loading, error, and success states
- Use error boundaries around route segments

### Accessibility

**Critical Issues:**
- Interactive elements without keyboard support
- Missing alt text on images
- Poor color contrast ratios

**Verify:**
- All buttons/links are keyboard accessible
- Form inputs have labels

### Styling

#### Tailwind CSS

**Issues:**
- Extremely long className strings (extract to component)
- Hard-coded colors not from theme

**Best Practices:**
- Use theme colors and spacing
- Responsive classes for mobile-first design

## Component Implementation

### Default Approach

- Start with Server Components by default
- Use TypeScript for all components
- Define prop types with interfaces
- Export components as named exports

### Client Components

**Guidelines:**
- Add 'use client' at the top
- Use hooks for state and effects
- Optimize re-renders with memo/useMemo/useCallback

## Testing Guidelines

### Testing Philosophy

**Guiding Principles:**
- Test user behavior, not implementation details
- Use accessible queries (e.g., `getByRole`, `getByLabelText`)

### What to Test

**Priority High:**
- User interactions (clicks, typing)
- Conditional rendering based on props/state
- API integration and data fetching

### React Testing Library

**Query Priority:**
1. Accessible Queries (Most Preferred)
2. Semantic Queries
3. Test IDs (Last Resort)

### User Interactions

**Library:** Use @testing-library/user-event

### Test Structure

**Anatomy:**
```tsx
describe('ComponentName', () => {
  test('describes expected behavior', async () => {
    // Arrange
    // Act
    // Assert
  });
});
```

### Mocking

**External Dependencies:**
- Mock API calls and third-party libraries with side effects

## Code Quality Checklist

- [ ] All props have TypeScript types
- [ ] Components are focused (single responsibility)
- [ ] Proper error handling
- [ ] Accessibility attributes are present

## Coverage Guidelines

### Requirements

| Area | Coverage |
|------|----------|
| Critical paths | 100% |
| Components | 80%+ |
| Utilities | 90%+ |

### What to Prioritize

- User-facing features
- Business logic and calculations

## Common Pitfalls

### Avoid

- Testing implementation details
- Snapshot tests for everything

### Instead

- Test public API and user-visible behavior
- Query by role/label for accessibility