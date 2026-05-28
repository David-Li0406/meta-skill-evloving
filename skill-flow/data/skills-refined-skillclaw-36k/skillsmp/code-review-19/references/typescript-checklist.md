# TypeScript Code Review Checklist

Complete checklist for TypeScript/React code review.

## Quick Reference

| Priority | Category | Check |
|----------|----------|-------|
| Critical | React | No missing useEffect dependencies |
| Critical | Async | Proper error handling in promises |
| High | Types | No 'any' types without justification |
| High | Null Safety | Proper optional chaining/nullish coalescing |
| Medium | Performance | Memoization where needed |
| Medium | Components | Proper component decomposition |
| Low | Style | Consistent naming conventions |

## Detailed Checklist

### 1. Type Safety

- [ ] **No `any` types without justification**
  ```typescript
  // BAD
  const data: any = fetchData();

  // GOOD
  interface User {
    id: string;
    name: string;
  }
  const data: User = fetchData();
  ```

- [ ] **Proper typing for function parameters and returns**
  ```typescript
  // Explicit return types for public functions
  function calculateTotal(items: Item[]): number {
    return items.reduce((sum, item) => sum + item.price, 0);
  }
  ```

- [ ] **Generic types used appropriately**
  ```typescript
  function identity<T>(value: T): T {
    return value;
  }
  ```

- [ ] **Union types are narrowed properly**
  ```typescript
  function process(value: string | number) {
    if (typeof value === 'string') {
      return value.toUpperCase();
    }
    return value * 2;
  }
  ```

### 2. React Hooks

- [ ] **useEffect has correct dependencies**
  ```typescript
  // BAD - missing dependency
  useEffect(() => {
    fetchUser(userId);
  }, []);

  // GOOD - all dependencies listed
  useEffect(() => {
    fetchUser(userId);
  }, [userId]);
  ```

- [ ] **useEffect cleanup function when needed**
  ```typescript
  useEffect(() => {
    const subscription = subscribe(id);
    return () => subscription.unsubscribe();
  }, [id]);
  ```

- [ ] **useCallback/useMemo used appropriately**
  ```typescript
  // For functions passed to children
  const handleClick = useCallback(() => {
    doSomething(id);
  }, [id]);

  // For expensive computations
  const sortedItems = useMemo(
    () => items.sort((a, b) => a.name.localeCompare(b.name)),
    [items]
  );
  ```

- [ ] **No hooks called conditionally**
  ```typescript
  // BAD
  if (condition) {
    const [value, setValue] = useState(0);
  }

  // GOOD
  const [value, setValue] = useState(0);
  if (condition) {
    // use value
  }
  ```

### 3. Null/Undefined Handling

- [ ] **Optional chaining used for potentially null values**
  ```typescript
  const city = user?.address?.city;
  ```

- [ ] **Nullish coalescing for default values**
  ```typescript
  const name = user.name ?? 'Anonymous';
  ```

- [ ] **Type guards for narrowing**
  ```typescript
  function isUser(value: unknown): value is User {
    return typeof value === 'object' && value !== null && 'id' in value;
  }
  ```

### 4. Error Handling

- [ ] **Async errors are caught**
  ```typescript
  // BAD
  async function fetchData() {
    const response = await fetch(url);
    return response.json();
  }

  // GOOD
  async function fetchData() {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }
      return response.json();
    } catch (error) {
      console.error('Fetch failed:', error);
      throw error;
    }
  }
  ```

- [ ] **Error boundaries for React components**
  ```typescript
  <ErrorBoundary fallback={<ErrorDisplay />}>
    <UserProfile />
  </ErrorBoundary>
  ```

- [ ] **Errors are typed properly**
  ```typescript
  class ApiError extends Error {
    constructor(public status: number, message: string) {
      super(message);
    }
  }
  ```

### 5. Performance

- [ ] **Lists have stable keys**
  ```typescript
  // BAD
  {items.map((item, index) => <Item key={index} />)}

  // GOOD
  {items.map((item) => <Item key={item.id} />)}
  ```

- [ ] **Heavy components are memoized**
  ```typescript
  const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
    // expensive rendering
  });
  ```

- [ ] **Unnecessary re-renders avoided**
  ```typescript
  // BAD - new object every render
  <Child style={{ color: 'red' }} />

  // GOOD - stable reference
  const style = useMemo(() => ({ color: 'red' }), []);
  <Child style={style} />
  ```

### 6. Component Design

- [ ] **Props interfaces are defined**
  ```typescript
  interface ButtonProps {
    variant: 'primary' | 'secondary';
    onClick: () => void;
    children: React.ReactNode;
  }
  ```

- [ ] **Components are appropriately sized**
  - Extract reusable pieces
  - Split large components

- [ ] **State lives at the right level**
  - Local state for UI-only concerns
  - Lifted state for shared concerns

### 7. Next.js Specific (if applicable)

- [ ] **'use client' directive used correctly**
  ```typescript
  'use client';  // Only for client-side components
  ```

- [ ] **Server/Client component separation**
  - Server Components for data fetching
  - Client Components for interactivity

- [ ] **Proper data fetching patterns**
  ```typescript
  // Server Component
  async function UserList() {
    const users = await fetchUsers();
    return <UserListClient users={users} />;
  }
  ```

### 8. Code Style

- [ ] **Consistent naming conventions**
  - Components: PascalCase
  - Functions/variables: camelCase
  - Constants: SCREAMING_SNAKE_CASE or camelCase
  - Types/Interfaces: PascalCase

- [ ] **Imports are organized**
  - External dependencies first
  - Internal modules second
  - Types last

- [ ] **No unused imports/variables**

### 9. Security

- [ ] **No sensitive data in client code**
- [ ] **User input is validated**
- [ ] **XSS prevention in dynamic content**
  ```typescript
  // Use textContent instead of innerHTML
  // Use React's built-in escaping
  ```

## Review Output Format

When reporting issues, use this format:

```
## Issue: [Brief Title]

- **File**: path/to/file.ts:line_number
- **Severity**: Critical | High | Medium | Low
- **Category**: Types | Hooks | Performance | Style

### Problem
[Description of the issue]

### Current Code
```typescript
// problematic code
```

### Suggested Fix
```typescript
// corrected code
```
```
