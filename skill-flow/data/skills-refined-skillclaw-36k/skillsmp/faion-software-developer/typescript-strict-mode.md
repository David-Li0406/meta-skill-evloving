---
id: typescript-strict-mode
name: "TypeScript Strict Mode"
domain: DEV
skill: faion-software-developer
category: "development"
---

# TypeScript Strict Mode

## Overview

TypeScript strict mode enables comprehensive type checking that catches errors at compile time, improves code quality, and provides better IDE support. This methodology covers strict configuration, type patterns, and best practices for type-safe TypeScript development.

## When to Use

- All new TypeScript projects
- Migrating JavaScript to TypeScript
- Improving type safety in existing projects
- Building libraries and shared packages
- Production applications requiring reliability

## Key Principles

1. **Enable strict mode** - All strict checks by default
2. **No implicit any** - Every value must have a type
3. **Null safety** - Handle null/undefined explicitly
4. **Explicit returns** - Functions declare their return types
5. **Prefer unknown over any** - Type-safe handling of unknown values

## Best Practices

### Strict Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    // Strict Mode (enables all below)
    "strict": true,

    // Individual strict flags (already included in strict)
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,

    // Additional strict checks (not in strict)
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noPropertyAccessFromIndexSignature": true,

    // Module resolution
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,

    // Emit
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",

    // Interop
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### noImplicitAny

```typescript
// BAD - implicit any
function process(data) {
  return data.value;
}

// GOOD - explicit types
function process(data: ProcessInput): ProcessOutput {
  return data.value;
}

// When type is truly unknown, use unknown
function handleInput(input: unknown): void {
  if (typeof input === 'string') {
    console.log(input.toUpperCase());
  }
}
```

### strictNullChecks

```typescript
// BAD - null not handled
function getUser(id: string): User {
  return users.find(u => u.id === id); // Error: could be undefined
}

// GOOD - explicit null handling
function getUser(id: string): User | undefined {
  return users.find(u => u.id === id);
}

// Or with assertion when you know it exists
function getRequiredUser(id: string): User {
  const user = users.find(u => u.id === id);
  if (!user) {
    throw new Error(`User ${id} not found`);
  }
  return user;
}

// Optional chaining and nullish coalescing
const userName = user?.name ?? 'Anonymous';
const email = user?.contact?.email;
```

### noUncheckedIndexedAccess

```typescript
// Without noUncheckedIndexedAccess
const arr: string[] = ['a', 'b', 'c'];
const item = arr[5]; // Type: string (but actually undefined!)

// With noUncheckedIndexedAccess
const arr: string[] = ['a', 'b', 'c'];
const item = arr[5]; // Type: string | undefined

// Safe access patterns
function getFirst<T>(items: T[]): T | undefined {
  return items[0]; // Correctly typed as T | undefined
}

// When you know index is valid
function getFirstRequired<T>(items: T[]): T {
  const first = items[0];
  if (first === undefined) {
    throw new Error('Array is empty');
  }
  return first;
}

// Object index signatures
interface Cache {
  [key: string]: string;
}
const cache: Cache = {};
const value = cache['key']; // Type: string | undefined
```

### exactOptionalPropertyTypes

```typescript
// Without exactOptionalPropertyTypes
interface Config {
  timeout?: number;
}
const config: Config = { timeout: undefined }; // OK

// With exactOptionalPropertyTypes
interface Config {
  timeout?: number;
}
const config: Config = { timeout: undefined }; // Error!
const config2: Config = {}; // OK - property omitted

// Use explicit undefined when needed
interface ConfigWithExplicitUndefined {
  timeout?: number | undefined;
}
const config3: ConfigWithExplicitUndefined = { timeout: undefined }; // OK
```

### Type Narrowing

```typescript
// Type guards
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function processValue(value: unknown): string {
  if (isString(value)) {
    return value.toUpperCase(); // Type narrowed to string
  }
  return String(value);
}

// Discriminated unions
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: Error };

function handleResult<T>(result: Result<T>): T {
  if (result.success) {
    return result.data; // Type narrowed, data exists
  }
  throw result.error; // Type narrowed, error exists
}

// in operator narrowing
interface Dog {
  bark(): void;
}
interface Cat {
  meow(): void;
}

function speak(animal: Dog | Cat): void {
  if ('bark' in animal) {
    animal.bark(); // Dog
  } else {
    animal.meow(); // Cat
  }
}

// instanceof narrowing
function formatDate(input: Date | string): string {
  if (input instanceof Date) {
    return input.toISOString();
  }
  return new Date(input).toISOString();
}
```

### Assertion Functions

```typescript
// Type assertion function
function assertDefined<T>(
  value: T | null | undefined,
  message?: string
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message ?? 'Value is null or undefined');
  }
}

// Usage
const user: User | null = getUser();
assertDefined(user, 'User must exist');
// After assertion, user is typed as User
console.log(user.name);

// Assert condition
function assert(
  condition: unknown,
  message?: string
): asserts condition {
  if (!condition) {
    throw new Error(message ?? 'Assertion failed');
  }
}

// Usage
function processOrder(order: Order | null): void {
  assert(order !== null, 'Order required');
  assert(order.items.length > 0, 'Order must have items');
  // order is typed as Order with items
}
```

### Branded Types

```typescript
// Prevent mixing similar primitive types
type UserId = string & { readonly __brand: 'UserId' };
type OrderId = string & { readonly __brand: 'OrderId' };

function createUserId(id: string): UserId {
  return id as UserId;
}

function createOrderId(id: string): OrderId {
  return id as OrderId;
}

function getUser(id: UserId): User {
  // ...
}

function getOrder(id: OrderId): Order {
  // ...
}

// Usage - type safety!
const userId = createUserId('user-123');
const orderId = createOrderId('order-456');

getUser(userId);  // OK
getUser(orderId); // Error! OrderId not assignable to UserId
```

### Const Assertions

```typescript
// Without as const
const config = {
  endpoint: '/api',
  methods: ['GET', 'POST'],
};
// Type: { endpoint: string; methods: string[] }

// With as const
const config = {
  endpoint: '/api',
  methods: ['GET', 'POST'],
} as const;
// Type: { readonly endpoint: '/api'; readonly methods: readonly ['GET', 'POST'] }

// Useful for discriminated unions
const ACTIONS = {
  INCREMENT: 'INCREMENT',
  DECREMENT: 'DECREMENT',
} as const;

type ActionType = typeof ACTIONS[keyof typeof ACTIONS];
// Type: 'INCREMENT' | 'DECREMENT'
```

### Template Literal Types

```typescript
// Type-safe string patterns
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type Endpoint = `/api/${string}`;

function request(method: HttpMethod, url: Endpoint): Promise<Response> {
  return fetch(url, { method });
}

request('GET', '/api/users');      // OK
request('GET', '/users');          // Error: doesn't match /api/*
request('PATCH', '/api/users');    // Error: PATCH not in HttpMethod

// Event handlers
type EventName = `on${Capitalize<string>}`;
// Matches: 'onClick', 'onSubmit', 'onChange', etc.

interface Props {
  onClick?: () => void;
  onSubmit?: () => void;
}
```

## Anti-patterns

### Avoid: Using any

```typescript
// BAD
function process(data: any): any {
  return data.value;
}

// GOOD - use unknown and narrow
function process(data: unknown): unknown {
  if (isValidData(data)) {
    return data.value;
  }
  throw new Error('Invalid data');
}
```

### Avoid: Non-null Assertion Overuse

```typescript
// BAD - hiding potential bugs
const name = user!.name!.first!;

// GOOD - handle nulls properly
const name = user?.name?.first ?? 'Unknown';
```

### Avoid: Type Assertions

```typescript
// BAD - bypassing type system
const user = data as User;

// GOOD - validate at runtime
function isUser(data: unknown): data is User {
  return (
    typeof data === 'object' &&
    data !== null &&
    'id' in data &&
    'email' in data
  );
}

if (isUser(data)) {
  // data is typed as User
}
```

## References

- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [TypeScript Strict Mode](https://www.typescriptlang.org/tsconfig#strict)
- [Type Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
