# JavaScript/TypeScript Standards

Language-specific conventions extending the core code standards.

## TypeScript Preferences

### Use TypeScript Over JavaScript

For any file that will be maintained long-term, prefer TypeScript. The type safety catches bugs early and serves as documentation.

### Type Annotations

- **Always type:** function parameters and return types
- **Let inference work:** for local variables when obvious
- **Avoid `any`:** use `unknown` if type is truly unknown

```typescript
// Yes
function calculateTotal(items: OrderItem[]): number {
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  return subtotal;  // Type inferred
}

// No
function calculateTotal(items: any): any {
  // ...
}
```

### Interfaces vs Types

- **Interface:** for object shapes, especially if they'll be extended
- **Type:** for unions, primitives, or computed types

```typescript
// Interface for shapes
interface User {
  id: string;
  name: string;
}

interface AdminUser extends User {
  permissions: string[];
}

// Type for unions
type Status = 'pending' | 'active' | 'completed';
type Result<T> = { success: true; data: T } | { success: false; error: string };
```

---

## Functions

### Arrow Functions vs Function Declarations

- **Arrow:** for callbacks, short inline functions
- **Declaration:** for top-level named functions (better stack traces)

```typescript
// Top-level: declaration
function processOrder(order: Order): Result {
  // ...
}

// Callback: arrow
const activeOrders = orders.filter(order => order.isActive);
```

### Async/Await Over Promises

```typescript
// Yes
async function fetchUserData(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();
  return data;
}

// Avoid
function fetchUserData(id: string): Promise<User> {
  return fetch(`/api/users/${id}`)
    .then(response => response.json())
    .then(data => data);
}
```

### Destructuring

Use for clarity, not to show off:

```typescript
// Yes - improves readability
function displayUser({ name, email, role }: User) {
  console.log(`${name} (${email}) - ${role}`);
}

// No - excessive
const { data: { users: { 0: { profile: { name } } } } } = response;
```

---

## Objects & Arrays

### Object Shorthand

```typescript
const name = 'Alice';
const age = 30;

// Yes
const user = { name, age };

// No
const user = { name: name, age: age };
```

### Spread Over Mutation

```typescript
// Yes
const updated = { ...user, lastLogin: new Date() };

// No
user.lastLogin = new Date();
```

### Array Methods Over Loops

Prefer `.map()`, `.filter()`, `.reduce()` for transformation:

```typescript
// Yes
const activeUserNames = users
  .filter(user => user.isActive)
  .map(user => user.name);

// Acceptable for complex logic or performance-critical code
const activeUserNames = [];
for (const user of users) {
  if (user.isActive) {
    activeUserNames.push(user.name);
  }
}
```

---

## Modules

### Named Exports Over Default

Named exports improve refactoring and autocomplete:

```typescript
// Yes
export function createUser() { ... }
export function deleteUser() { ... }
import { createUser, deleteUser } from './users';

// Avoid
export default function createUser() { ... }
import createUser from './users';
```

### Import Organization

```typescript
// 1. Node built-ins
import fs from 'fs';
import path from 'path';

// 2. External packages
import express from 'express';
import { z } from 'zod';

// 3. Internal absolute imports
import { config } from '@/config';
import { logger } from '@/utils/logger';

// 4. Relative imports
import { validateInput } from './validation';
import type { UserInput } from './types';
```

---

## Error Handling

### Custom Error Classes

```typescript
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`, 'NOT_FOUND', 404);
    this.name = 'NotFoundError';
  }
}
```

### Type-Safe Error Handling

```typescript
// Result type pattern
type Result<T, E = Error> = 
  | { success: true; data: T }
  | { success: false; error: E };

function parseJson<T>(text: string): Result<T> {
  try {
    return { success: true, data: JSON.parse(text) };
  } catch (e) {
    return { success: false, error: e as Error };
  }
}

// Usage
const result = parseJson<User>(text);
if (result.success) {
  console.log(result.data.name);  // Type-safe
} else {
  console.error(result.error.message);
}
```

---

## Null & Undefined

### Prefer `undefined` Over `null`

TypeScript defaults to `undefined`. Use `null` only when interacting with APIs that require it.

### Nullish Coalescing

```typescript
// Yes - only catches null/undefined
const value = input ?? 'default';

// Be careful - catches all falsy
const value = input || 'default';  // '' and 0 become 'default'
```

### Optional Chaining

```typescript
// Yes
const street = user?.address?.street;

// No
const street = user && user.address && user.address.street;
```

---

## React-Specific (When Applicable)

### Functional Components

```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

function Button({ label, onClick, disabled = false }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
}
```

### Hooks

- Call at top level only
- Custom hooks start with `use`
- Extract complex logic to custom hooks

```typescript
function useUserData(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);
  
  return { user, loading };
}
```
