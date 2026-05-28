---
name: react-code-reviewer
description: Comprehensive code review guidelines for React 19 TypeScript projects
---

# React Code Review Guidelines

## Review Categories

### Component Architecture

#### Server vs Client

**Red Flags:**
- 'use client' on component that doesn't use hooks or browser APIs
- Server Component trying to use hooks
- Client Component doing data fetching that should be on server

**Good Practices:**
- Server Components for data fetching and static content
- 'use client' only when necessary (hooks, events, browser APIs)
- Client Components receive data as props from Server Components

#### Component Structure

**Issues:**
- Component exceeds 300 lines (consider splitting)
- Multiple responsibilities in one component
- Deeply nested component tree (> 5 levels)
- Repeated code that could be extracted to hook

**Look For:**
- Single responsibility principle
- Proper component composition
- Extracted custom hooks for reusable logic

### TypeScript Usage

#### Type Safety

**Issues:**
- Use of 'any' without explanation comment
- Type assertions (as Type) without justification
- Non-null assertions (!) without null checks
- Missing prop types (implicit any)
- Missing return type on exported functions

**Best Practices:**
- All props have interface definitions
- Generic types for reusable components
- Discriminated unions for complex state
- Proper utility type usage (Partial, Pick, Omit)

#### Naming

**Check:**
- PascalCase for components and types
- camelCase for variables and functions
- Descriptive names (avoid single letters except in maps)
- Hooks prefixed with 'use'

### State Management

#### React State

**Issues:**
- Using state for derived values (should use useMemo)
- Prop drilling more than 2 levels (consider Context)
- State that could be computed from props
- Missing useCallback for functions passed to children

**Patterns:**
- useState for local UI state
- useReducer for complex state logic
- Context for deeply nested props
- Zustand for global client state
- React Query for server state

#### Side Effects

**Common Issues:**
- useEffect with missing dependencies
- useEffect without cleanup function (subscriptions)
- Infinite loops from state updates in useEffect
- Side effects in render (should be in useEffect)

**Verify:**
- All useEffect dependencies listed correctly
- Cleanup functions for subscriptions/timers
- No state updates during render

### Performance

#### Optimization

**Unnecessary Optimization:**
- React.memo on simple components
- useMemo for cheap calculations
- useCallback everywhere (premature optimization)

**Missing Optimization:**
- Expensive calculations without useMemo
- Functions recreated on every render passed to children
- Large lists without virtualization
- No code splitting for large components

#### Re-renders

**Check:**
- Inline object creation in props ({} in JSX)
- Inline array creation in props ([] in JSX)
- Inline function definitions in JSX
- Context value not memoized

### Error Handling

#### Coverage

**Missing:**
- No error handling for async operations
- No loading states for data fetching
- Missing error boundaries
- Silent error catching (empty catch blocks)

**Good Practices:**
- Loading, error, and success states all handled
- Error boundaries around route segments
- User-friendly error messages
- Retry mechanisms for failed requests

### Accessibility

#### Requirements

**Critical Issues:**
- Interactive elements without keyboard support
- Missing alt text on images
- Poor color contrast ratios
- Missing ARIA labels on custom controls
- Improper heading hierarchy

**Verify:**
- All buttons/links keyboard accessible
- Form inputs have labels
- Semantic HTML used appropriately
- Focus management in modals/dialogs

### Styling

#### Tailwind

**Issues:**
- Extremely long className strings (extract to component)
- Repeated utility combinations (create component)
- Hard-coded colors not from theme
- Magic numbers in spacing (use spacing scale)

**Best Practices:**
- Use theme colors and spacing
- Responsive classes for mobile-first design
- Conditional classes with clsx/classnames

#### CSS Modules

**Check:**
- Scoped styles don't leak globally
- No !important flags (indicates specificity issue)
- Consistent naming convention

### Data Fetching

#### React Query

**Issues:**
- Fetching in useEffect instead of React Query
- Query keys not unique or not arrays
- Missing error handling in queries
- Not using mutation for state-changing operations

**Verify:**
- Proper query key structure
- Mutations for POST/PUT/DELETE
- Query invalidation after mutations
- Loading and error states handled

#### Server Components

**Check:**
- Direct data fetching (no useEffect)
- Async function declaration
- Proper error handling with try-catch
- Loading states via Suspense boundaries

### Testing

#### Coverage

**Missing:**
- No tests for components with logic
- Only happy path tested
- Implementation details tested instead of behavior
- Missing edge case tests

**Verify:**
- User interactions tested
- Loading and error states tested
- Accessibility in tests (query by role/label)
- Integration over unit tests

### Security

**Common Issues:**
- Dangerously setting innerHTML without sanitization
- Unvalidated user input in URLs
- Sensitive data in client components (should be server)
- API keys/secrets exposed in client code

**Verify:**
- User input sanitized before rendering
- Authentication checks in appropriate places
- Secrets kept on server side

### Code Quality

#### Readability

**Issues:**
- Unclear variable names
- Complex nested ternaries
- Large boolean expressions without extraction
- No comments for complex logic

**Improvements:**
- Extract complex conditions to variables
- Use early returns to reduce nesting
- Add JSDoc for public APIs

#### Consistency

**Verify:**
- Consistent component declaration style (function vs const)
- Consistent import order
- Consistent naming conventions
- Follows project conventions in CLAUDE.md

## Review Process

### Checklist

- [ ] Component uses correct Server/Client designation
- [ ] TypeScript types complete and accurate
- [ ] State management appropriate for use case
- [ ] Performance optimizations justified
- [ ] Error handling comprehensive
- [ ] Accessibility requirements met
- [ ] Tests cover main user flows
- [ ] Code follows project conventions

### Severity Levels

**Critical:**
- Security vulnerabilities
- Accessibility blocking issues
- Data loss possibilities

**Major:**
- Type safety violations
- Performance problems
- Missing error handling

**Minor:**
- Code style inconsistencies
- Missing comments
- Minor optimization opportunities
