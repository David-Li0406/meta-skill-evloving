# TypeScript Standards

TypeScript best practices for type safety and maintainability in React frontend code.

---

## Strict Mode

### Configuration

TypeScript strict mode is **enabled**:

```json
// tsconfig.json
{
    "compilerOptions": {
        "strict": true,
        "noImplicitAny": true,
        "strictNullChecks": true
    }
}
```

**This means:**
- No implicit `any` types
- Null/undefined must be handled explicitly
- Type safety enforced

---

## No `any` Type

### The Rule

```typescript
// ❌ NEVER use any
function handleData(data: any) {
    return data.something;
}

// ✅ Use specific types
interface MyData {
    something: string;
}

function handleData(data: MyData) {
    return data.something;
}

// ✅ Or use unknown for truly unknown data
function handleUnknown(data: unknown) {
    if (typeof data === 'object' && data !== null && 'something' in data) {
        return (data as MyData).something;
    }
}
```

**If you truly don't know the type:**
- Use `unknown` (forces type checking)
- Use type guards to narrow
- Document why type is unknown

---

## Type Imports

### Use `import type`

```typescript
// ✅ CORRECT - import type for types
import type { User, Post } from '~types';
import type { SxProps, Theme } from '@mui/material';

// ✅ CORRECT - regular import for values
import { Box, Paper } from '@mui/material';

// ❌ AVOID - mixing type and value imports
import { Box, Paper, SxProps, Theme } from '@mui/material';
```

**Why?**
- Clearer intent
- Smaller bundle (types are removed)
- Better IDE support

---

## Function Return Types

### Explicit Returns

```typescript
// ✅ CORRECT - explicit return type
function calculateTotal(items: Item[]): number {
    return items.reduce((sum, item) => sum + item.price, 0);
}

// ✅ CORRECT - async function
async function fetchUser(id: string): Promise<User> {
    const response = await api.get(`/users/${id}`);
    return response.data;
}

// React components (return type inferred is ok)
export const MyComponent: React.FC<Props> = ({ id }) => {
    return <div>{id}</div>;
};
```

---

## Utility Types

### Common Utility Types

```typescript
// Partial - all properties optional
type PartialUser = Partial<User>;

// Pick - select specific properties
type UserName = Pick<User, 'firstName' | 'lastName'>;

// Omit - exclude specific properties
type UserWithoutPassword = Omit<User, 'password'>;

// Required - all properties required
type RequiredSettings = Required<Settings>;

// Record - typed object
type UserRoles = Record<string, Role>;
```

### Real-World Examples

```typescript
// Update DTO (partial of creation)
type UpdateUserDTO = Partial<CreateUserDTO>;

// API Response
type ApiResponse<T> = {
    data: T;
    success: boolean;
    error?: string;
};

// Query result type
type QueryResult<T> = {
    data: T;
    isLoading: boolean;
    error: Error | null;
};
```

---

## Type Guards

### Custom Type Guards

```typescript
// Type guard function
function isUser(value: unknown): value is User {
    return (
        typeof value === 'object' &&
        value !== null &&
        'id' in value &&
        'email' in value
    );
}

// Usage
function handleData(data: unknown) {
    if (isUser(data)) {
        // data is typed as User here
        console.log(data.email);
    }
}
```

### Discriminated Unions

```typescript
type SuccessResult = {
    type: 'success';
    data: User;
};

type ErrorResult = {
    type: 'error';
    message: string;
};

type Result = SuccessResult | ErrorResult;

function handleResult(result: Result) {
    if (result.type === 'success') {
        // result.data is typed
        console.log(result.data);
    } else {
        // result.message is typed
        console.log(result.message);
    }
}
```

---

## Type Assertions

### Use Carefully

```typescript
// ✅ OK - When you know more than TypeScript
const element = document.getElementById('root') as HTMLDivElement;

// ✅ OK - After validation
if (isUser(data)) {
    const user = data as User;
}

// ❌ AVOID - Escape hatch
const data = getData() as any;  // WRONG

// ❌ AVOID - Unsafe assertion
const value = unknownValue as string;  // Might not be string
```

---

## Null/Undefined Handling

### Optional Chaining

```typescript
// ✅ CORRECT
const name = user?.profile?.name;

// Equivalent to:
const name = user && user.profile && user.profile.name;
```

### Nullish Coalescing

```typescript
// ✅ CORRECT
const displayName = user?.name ?? 'Anonymous';

// Only uses default if null or undefined
// (Different from || which triggers on '', 0, false)
```

### Non-Null Assertion (Use Carefully)

```typescript
// ✅ OK - When you're certain value exists
const data = queryClient.getQueryData<Data>(['data'])!;

// ⚠️ CAREFUL - Only use when you KNOW it's not null
// Better to check explicitly:
const data = queryClient.getQueryData<Data>(['data']);
if (data) {
    // Use data
}
```

---

## Summary

**TypeScript Checklist:**
- ✅ Strict mode enabled
- ✅ No `any` type (use `unknown` if needed)
- ✅ Explicit return types on functions
- ✅ Use `import type` for type imports
- ✅ JSDoc comments on prop interfaces
- ✅ Utility types (Partial, Pick, Omit, Required, Record)
- ✅ Type guards for narrowing
- ✅ Optional chaining and nullish coalescing
- ❌ Avoid type assertions unless necessary

**See Also:**
- [component-patterns.md](component-patterns.md) - Component typing
- [data-fetching.md](data-fetching.md) - API typing
