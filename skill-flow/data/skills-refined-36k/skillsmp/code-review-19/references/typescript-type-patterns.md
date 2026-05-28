# TypeScript Type Design Patterns

Best practices for type design in TypeScript.

## Discriminated Unions

Use for state management and result types.

```typescript
// Request State
type RequestState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

// Usage
function renderState<T>(state: RequestState<T>) {
  switch (state.status) {
    case 'idle':
      return <Idle />;
    case 'loading':
      return <Loading />;
    case 'success':
      return <Data data={state.data} />;
    case 'error':
      return <Error error={state.error} />;
  }
}
```

```typescript
// API Result
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const user = await api.getUser(id);
    return { success: true, data: user };
  } catch (e) {
    return { success: false, error: e as Error };
  }
}
```

## Type Guards

Create custom type guards for runtime validation.

```typescript
// Basic type guard
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

// Object type guard
interface User {
  id: string;
  name: string;
  email: string;
}

function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value && typeof (value as User).id === 'string' &&
    'name' in value && typeof (value as User).name === 'string' &&
    'email' in value && typeof (value as User).email === 'string'
  );
}

// Array type guard
function isUserArray(value: unknown): value is User[] {
  return Array.isArray(value) && value.every(isUser);
}
```

## Branded Types

Prevent mixing similar types.

```typescript
// Create branded type
type Brand<T, B> = T & { readonly __brand: B };

type UserId = Brand<string, 'UserId'>;
type PostId = Brand<string, 'PostId'>;

// Factory functions
function createUserId(id: string): UserId {
  return id as UserId;
}

function createPostId(id: string): PostId {
  return id as PostId;
}

// Type-safe function
function fetchUser(userId: UserId): Promise<User> {
  return api.get(`/users/${userId}`);
}

// Usage
const userId = createUserId('user-123');
const postId = createPostId('post-456');

fetchUser(userId);  // OK
fetchUser(postId);  // Type error!
```

## Utility Types

Leverage built-in utility types.

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: Date;
}

// Partial - all optional
type UserUpdate = Partial<User>;

// Required - all required
type CompleteUser = Required<User>;

// Pick - select properties
type UserCredentials = Pick<User, 'email' | 'name'>;

// Omit - exclude properties
type UserInput = Omit<User, 'id' | 'createdAt'>;

// Record - key-value mapping
type UserById = Record<string, User>;

// Readonly - immutable
type ImmutableUser = Readonly<User>;

// Parameters/ReturnType - function types
type FetchParams = Parameters<typeof fetch>;
type FetchReturn = ReturnType<typeof fetch>;
```

## Mapped Types

Transform types systematically.

```typescript
// Make all properties nullable
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

// Make specific properties required
type RequireKeys<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Add prefix to keys
type Prefixed<T, P extends string> = {
  [K in keyof T as `${P}${string & K}`]: T[K];
};

// Form field types
type FormField<T> = {
  value: T;
  error: string | null;
  touched: boolean;
};

type FormState<T> = {
  [K in keyof T]: FormField<T[K]>;
};
```

## Conditional Types

Create types based on conditions.

```typescript
// Unwrap array element type
type ArrayElement<T> = T extends readonly (infer E)[] ? E : never;

// Unwrap promise type
type Awaited<T> = T extends Promise<infer U> ? U : T;

// Extract function return type
type AsyncReturnType<T extends (...args: any[]) => Promise<any>> =
  T extends (...args: any[]) => Promise<infer R> ? R : never;

// Conditional based on property
type IsRequired<T, K extends keyof T> =
  {} extends Pick<T, K> ? false : true;
```

## Template Literal Types

Create string-based types.

```typescript
// HTTP methods
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

// API routes
type ApiRoute = `/${string}`;

// Combined
type ApiEndpoint = `${HttpMethod} ${ApiRoute}`;

// Event handlers
type EventName = 'click' | 'focus' | 'blur';
type EventHandler = `on${Capitalize<EventName>}`;
// Result: "onClick" | "onFocus" | "onBlur"

// CSS units
type CSSUnit = 'px' | 'em' | 'rem' | '%';
type CSSValue = `${number}${CSSUnit}`;
```

## Generic Constraints

Constrain generic types effectively.

```typescript
// Constrain to specific shape
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Constrain to callable
function memoize<T extends (...args: any[]) => any>(fn: T): T {
  const cache = new Map();
  return ((...args: Parameters<T>) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  }) as T;
}

// Multiple constraints
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}
```

## Best Practices

### Prefer Union Types Over Enums

```typescript
// Prefer this
type Status = 'pending' | 'active' | 'inactive';

// Over this (unless you need reverse mapping)
enum StatusEnum {
  Pending = 'pending',
  Active = 'active',
  Inactive = 'inactive',
}
```

### Use `unknown` Over `any`

```typescript
// Prefer this - forces type checking
function parse(input: unknown): Data {
  if (isData(input)) {
    return input;
  }
  throw new Error('Invalid data');
}

// Avoid this - bypasses type checking
function parse(input: any): Data {
  return input;  // No safety
}
```

### Const Assertions for Literals

```typescript
// Without const assertion
const config = {
  endpoint: '/api',
  timeout: 5000,
};
// Type: { endpoint: string; timeout: number }

// With const assertion
const config = {
  endpoint: '/api',
  timeout: 5000,
} as const;
// Type: { readonly endpoint: "/api"; readonly timeout: 5000 }
```

### Infer When Possible

```typescript
// Let TypeScript infer when obvious
const name = 'John';  // string
const count = 42;     // number
const items = [1, 2, 3];  // number[]

// Annotate when not obvious or for documentation
const config: AppConfig = loadConfig();
function calculateTotal(items: Item[]): number { }
```
