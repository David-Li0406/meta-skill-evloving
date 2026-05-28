# Advanced TypeScript Patterns

Patterns for writing type-safe, maintainable TypeScript code.

## Generics

### Basic Generic Functions

```typescript
// Generic function
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

// With constraints
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}

// Multiple type parameters
function zip<T, U>(arr1: T[], arr2: U[]): [T, U][] {
  return arr1.map((item, i) => [item, arr2[i]]);
}
```

### Generic Classes

```typescript
class Result<T, E = Error> {
  private constructor(
    private readonly value?: T,
    private readonly error?: E
  ) {}

  static ok<T>(value: T): Result<T, never> {
    return new Result(value);
  }

  static err<E>(error: E): Result<never, E> {
    return new Result(undefined, error);
  }

  isOk(): this is Result<T, never> {
    return this.error === undefined;
  }

  unwrap(): T {
    if (this.error) throw this.error;
    return this.value!;
  }

  map<U>(fn: (value: T) => U): Result<U, E> {
    if (this.error) return Result.err(this.error);
    return Result.ok(fn(this.value!));
  }
}
```

## Conditional Types

### Basic Conditional Types

```typescript
// Extract array element type
type ArrayElement<T> = T extends (infer U)[] ? U : never;

type A = ArrayElement<string[]>;  // string
type B = ArrayElement<number>;    // never

// Extract promise value
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;

type C = Awaited<Promise<Promise<string>>>;  // string

// Extract function return type
type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;
```

### Distributive Conditional Types

```typescript
// Distributes over unions
type NonNullable<T> = T extends null | undefined ? never : T;

type D = NonNullable<string | null | undefined>;  // string

// Exclude from union
type Exclude<T, U> = T extends U ? never : T;

type E = Exclude<'a' | 'b' | 'c', 'a'>;  // 'b' | 'c'

// Extract from union
type Extract<T, U> = T extends U ? T : never;

type F = Extract<'a' | 'b' | 1, string>;  // 'a' | 'b'
```

## Mapped Types

### Basic Mapped Types

```typescript
// Make all properties optional
type Partial<T> = {
  [K in keyof T]?: T[K];
};

// Make all properties required
type Required<T> = {
  [K in keyof T]-?: T[K];
};

// Make all properties readonly
type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};

// Pick specific properties
type Pick<T, K extends keyof T> = {
  [P in K]: T[P];
};
```

### Advanced Mapped Types

```typescript
// Remove readonly modifier
type Mutable<T> = {
  -readonly [K in keyof T]: T[K];
};

// Deep partial
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

// Nullable properties
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

// Transform property types
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface Person {
  name: string;
  age: number;
}

type PersonGetters = Getters<Person>;
// { getName: () => string; getAge: () => number; }
```

## Template Literal Types

```typescript
// Type-safe event handlers
type EventName = 'click' | 'focus' | 'blur';
type Handler = `on${Capitalize<EventName>}`;
// 'onClick' | 'onFocus' | 'onBlur'

// Route parameters
type Route = '/users/:userId/posts/:postId';
type Params = Route extends `${string}:${infer Param}/${infer Rest}`
  ? Param | Params<`/${Rest}`>
  : Route extends `${string}:${infer Param}`
  ? Param
  : never;
// 'userId' | 'postId'

// Dot notation paths
type PathOf<T, Prefix extends string = ''> = T extends object
  ? {
      [K in keyof T & string]: T[K] extends object
        ? PathOf<T[K], `${Prefix}${K}.`>
        : `${Prefix}${K}`;
    }[keyof T & string]
  : never;
```

## Type Guards

### User-Defined Type Guards

```typescript
interface Dog {
  bark(): void;
}

interface Cat {
  meow(): void;
}

// Type guard function
function isDog(animal: Dog | Cat): animal is Dog {
  return 'bark' in animal;
}

// Using the guard
function makeSound(animal: Dog | Cat) {
  if (isDog(animal)) {
    animal.bark();  // TypeScript knows it's Dog
  } else {
    animal.meow();  // TypeScript knows it's Cat
  }
}
```

### Assertion Functions

```typescript
function assertDefined<T>(
  value: T | undefined | null,
  message?: string
): asserts value is T {
  if (value === undefined || value === null) {
    throw new Error(message ?? 'Value is not defined');
  }
}

function process(value: string | undefined) {
  assertDefined(value, 'Value required');
  // value is now string, not string | undefined
  console.log(value.toUpperCase());
}
```

## Discriminated Unions

```typescript
// Use a literal type discriminator
type Result<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error }
  | { status: 'loading' };

function handleResult<T>(result: Result<T>) {
  switch (result.status) {
    case 'success':
      console.log(result.data);  // data is available
      break;
    case 'error':
      console.error(result.error);  // error is available
      break;
    case 'loading':
      console.log('Loading...');
      break;
  }
}

// Exhaustiveness checking
function assertNever(x: never): never {
  throw new Error(`Unexpected value: ${x}`);
}

function handleStatus(status: 'a' | 'b' | 'c') {
  switch (status) {
    case 'a': return 1;
    case 'b': return 2;
    case 'c': return 3;
    default: return assertNever(status);  // Compile error if case missing
  }
}
```

## Branded Types

```typescript
// Prevent mixing similar types
type Brand<T, B> = T & { __brand: B };

type UserId = Brand<string, 'UserId'>;
type OrderId = Brand<string, 'OrderId'>;

function getUser(id: UserId): User { /* ... */ }
function getOrder(id: OrderId): Order { /* ... */ }

// Type-safe!
const userId = 'user-123' as UserId;
const orderId = 'order-456' as OrderId;

getUser(userId);   // OK
getUser(orderId);  // Error! OrderId is not UserId
```

## Common Mistakes

### Mistake: Using `any` Instead of `unknown`

```typescript
// ❌ BAD: any bypasses type checking
function parse(json: string): any {
  return JSON.parse(json);
}

// ✅ GOOD: unknown requires type narrowing
function parse(json: string): unknown {
  return JSON.parse(json);
}

const data = parse('{"name": "test"}');
// Must narrow before use
if (isUser(data)) {
  console.log(data.name);
}
```

### Mistake: Object vs Record

```typescript
// ❌ BAD: object type is too broad
function keys(obj: object): string[] {
  return Object.keys(obj);  // Returns string[], not keyof typeof obj
}

// ✅ GOOD: Use generics for type safety
function keys<T extends object>(obj: T): (keyof T)[] {
  return Object.keys(obj) as (keyof T)[];
}
```

### Mistake: Type Assertions Over Guards

```typescript
// ❌ BAD: Assertion bypasses safety
const user = response.data as User;

// ✅ GOOD: Validate at runtime
function isUser(data: unknown): data is User {
  return (
    typeof data === 'object' &&
    data !== null &&
    'id' in data &&
    'name' in data
  );
}

if (isUser(response.data)) {
  const user = response.data;  // Safely typed
}
```

### Mistake: Forgetting `as const`

```typescript
// ❌ BAD: Types are widened
const config = {
  endpoint: '/api/users',
  method: 'GET',  // type: string
};

// ✅ GOOD: Preserve literal types
const config = {
  endpoint: '/api/users',
  method: 'GET',  // type: 'GET'
} as const;

// Now this works
type Method = typeof config.method;  // 'GET', not string
```

### Mistake: Inconsistent Null Handling

```typescript
// ❌ BAD: Multiple patterns
function getUser(id: string): User | null { }
function getOrder(id: string): Order | undefined { }

// ✅ GOOD: Consistent pattern
function getUser(id: string): User | undefined { }
function getOrder(id: string): Order | undefined { }

// Or use Result type for explicit error handling
function getUser(id: string): Result<User, NotFoundError> { }
```

## Best Practices

1. **Enable strict mode** - All `strict` flags in tsconfig
2. **Prefer `unknown` over `any`** - Forces type narrowing
3. **Use discriminated unions** - For type-safe state handling
4. **Avoid type assertions** - Use type guards instead
5. **Use `as const`** - For literal type inference
6. **Leverage utility types** - Don't reinvent `Partial`, `Pick`, etc.
7. **Brand primitive types** - Prevent ID mix-ups
8. **Make invalid states unrepresentable** - Design types that can't be wrong
