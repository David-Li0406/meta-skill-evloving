# TypeScript Utility Types Reference

TypeScript provides built-in utility types that help transform and manipulate types. This guide covers the most useful ones and when to use them.

## Object Manipulation

### `Partial<T>`

Makes all properties of `T` optional.

**When to use**: Partial updates, optional configuration objects, patch operations.

```ts
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
}

// Only require fields you're updating
function updateUser(id: string, updates: Partial<User>) {
  // updates can have any subset of User properties
}

updateUser("123", { name: "Alice" }); // Valid
updateUser("123", { email: "alice@example.com", age: 30 }); // Valid
```

### `Required<T>`

Makes all properties of `T` required (opposite of Partial).

**When to use**: Ensuring all optional properties are provided, validation layers.

```ts
interface Config {
  host?: string;
  port?: number;
  timeout?: number;
}

// Ensure full config before connecting
function connect(config: Required<Config>) {
  // All properties are guaranteed to exist
  console.log(`Connecting to ${config.host}:${config.port}`);
}
```

### `Readonly<T>`

Makes all properties of `T` readonly.

**When to use**: Immutable data structures, preventing mutations, API responses.

```ts
interface User {
  id: string;
  name: string;
}

const user: Readonly<User> = { id: "1", name: "Alice" };
user.name = "Bob"; // Error: Cannot assign to 'name' because it is read-only

// Use with arrays for immutable lists
const numbers: Readonly<number[]> = [1, 2, 3];
numbers.push(4); // Error: Property 'push' does not exist on type 'readonly number[]'
```

### `Record<K, V>`

Creates an object type with keys of type `K` and values of type `V`.

**When to use**: Dictionaries, maps, lookup tables, configuration objects.

```ts
// Define a map of string keys to number values
type Scores = Record<string, number>;
const gameScores: Scores = {
  alice: 100,
  bob: 85,
  charlie: 92
};

// Define specific keys
type UserRole = "admin" | "user" | "guest";
type Permissions = Record<UserRole, string[]>;

const permissions: Permissions = {
  admin: ["read", "write", "delete"],
  user: ["read", "write"],
  guest: ["read"]
};
```

### `Pick<T, K>`

Creates a type by picking specific properties `K` from `T`.

**When to use**: Extracting subsets of properties, DTOs, API request/response types.

```ts
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  createdAt: Date;
}

// Only expose safe fields in API response
type UserPublic = Pick<User, "id" | "name" | "email">;

const publicUser: UserPublic = {
  id: "1",
  name: "Alice",
  email: "alice@example.com"
  // password and createdAt not included
};
```

### `Omit<T, K>`

Creates a type by omitting specific properties `K` from `T` (opposite of Pick).

**When to use**: Excluding sensitive/internal fields, creating variations of types.

```ts
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
}

// Remove sensitive field
type SafeUser = Omit<User, "password">;

// Create input type (without server-generated fields)
type UserInput = Omit<User, "id">;

function createUser(input: UserInput): User {
  return {
    id: generateId(),
    ...input
  };
}
```

## Function Types

### `Parameters<T>`

Extracts parameter types from a function type as a tuple.

**When to use**: Creating wrapper functions, middleware, decorators.

```ts
function greet(name: string, age: number) {
  return `Hello ${name}, you are ${age} years old`;
}

type GreetParams = Parameters<typeof greet>; // [string, number]

function loggedGreet(...args: GreetParams) {
  console.log("Calling greet with:", args);
  return greet(...args);
}
```

### `ReturnType<T>`

Extracts the return type from a function type.

**When to use**: Type inference from existing functions, ensuring consistent return types.

```ts
function createUser() {
  return {
    id: "123",
    name: "Alice",
    email: "alice@example.com"
  };
}

type User = ReturnType<typeof createUser>;
// User is { id: string; name: string; email: string }

// Use in other functions
function saveUser(user: User) {
  // ...
}
```

### `Awaited<T>`

Unwraps the type from a Promise.

**When to use**: Working with async functions, extracting resolved types.

```ts
async function fetchUser() {
  return {
    id: "123",
    name: "Alice"
  };
}

type User = Awaited<ReturnType<typeof fetchUser>>;
// User is { id: string; name: string }

// Nested promises
type DeepPromise = Promise<Promise<string>>;
type Resolved = Awaited<DeepPromise>; // string
```

## String Manipulation

### `Uppercase<S>`, `Lowercase<S>`, `Capitalize<S>`, `Uncapitalize<S>`

Transform string literal types.

**When to use**: Working with literal types, API key formatting, constant names.

```ts
type EventName = "click" | "focus" | "blur";

type EventHandler = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"

type UppercaseEvent = Uppercase<EventName>;
// "CLICK" | "FOCUS" | "BLUR"

// Practical example: HTTP methods
type HTTPMethod = "get" | "post" | "put" | "delete";
type MethodHandler = `handle${Capitalize<HTTPMethod>}`;
// "handleGet" | "handlePost" | "handlePut" | "handleDelete"
```

## Advanced Utilities

### `Exclude<T, U>`

Excludes types from `T` that are assignable to `U`.

**When to use**: Filtering union types, removing specific cases.

```ts
type AllRoles = "admin" | "user" | "guest" | "system";
type UserRoles = Exclude<AllRoles, "system">;
// "admin" | "user" | "guest"

type Primitive = string | number | boolean | null | undefined;
type NonNullPrimitive = Exclude<Primitive, null | undefined>;
// string | number | boolean
```

### `Extract<T, U>`

Extracts types from `T` that are assignable to `U` (opposite of Exclude).

**When to use**: Filtering to specific types in unions.

```ts
type AllTypes = string | number | boolean | (() => void);
type Functions = Extract<AllTypes, Function>;
// () => void

type Value = string | number | User;
type Primitives = Extract<Value, string | number>;
// string | number
```

### `NonNullable<T>`

Excludes `null` and `undefined` from `T`.

**When to use**: After null checks, ensuring values are defined.

```ts
type NullableUser = User | null | undefined;
type DefiniteUser = NonNullable<NullableUser>;
// User

function processUser(user: User | null) {
  if (user === null) return;

  // user is now NonNullable<typeof user>
  const definite: NonNullable<typeof user> = user;
}
```

### `InstanceType<T>`

Extracts the instance type from a constructor function type.

**When to use**: Working with classes, dependency injection, factories.

```ts
class User {
  constructor(public name: string) {}
}

type UserInstance = InstanceType<typeof User>;
// UserInstance is User

function createInstance<T extends new (...args: any[]) => any>(
  Constructor: T
): InstanceType<T> {
  return new Constructor();
}
```

## Combining Utilities

Utility types can be composed for powerful type transformations:

```ts
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  role: "admin" | "user";
}

// Partial update, excluding id (can't change) and password (use separate endpoint)
type UserUpdate = Partial<Omit<User, "id" | "password">>;

// Read-only public user
type PublicUser = Readonly<Pick<User, "id" | "name" | "email">>;

// Required config with defaults removed
interface ConfigWithDefaults {
  host?: string;
  port?: number;
  timeout: number;
}

type FinalConfig = Required<ConfigWithDefaults>;
```

## Custom Utility Examples

Build your own utilities by combining built-ins:

```ts
// Make specific fields optional
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

interface User {
  id: string;
  name: string;
  email: string;
}

type UserWithOptionalEmail = PartialBy<User, "email">;
// { id: string; name: string; email?: string }

// Make specific fields required
type RequiredBy<T, K extends keyof T> = Omit<T, K> & Required<Pick<T, K>>;

// Deep partial (for nested objects)
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Mutable (opposite of Readonly)
type Mutable<T> = {
  -readonly [P in keyof T]: T[P];
};
```

## Best Practices

1. **Prefer utility types over type assertions** - They're type-safe and caught at compile time
2. **Use `Pick`/`Omit` instead of duplicating types** - Single source of truth
3. **Combine utilities for complex transformations** - Build sophisticated types from simple ones
4. **Name derived types clearly** - `UserUpdate`, `PublicUser`, etc. show intent
5. **Use `ReturnType`/`Parameters` for library functions** - Stay in sync with actual implementation
6. **Create custom utilities for repeated patterns** - DRY applies to types too

## Common Patterns

### API Response Types

```ts
interface ApiResponse<T> {
  data: T;
  error: string | null;
  loading: boolean;
}

type UserResponse = ApiResponse<User>;
type UsersResponse = ApiResponse<User[]>;
```

### Form State Types

```ts
interface FormState<T> {
  values: Partial<T>;
  errors: Partial<Record<keyof T, string>>;
  touched: Partial<Record<keyof T, boolean>>;
}

type UserFormState = FormState<User>;
```

### Event Handlers

```ts
type EventHandler<T = Event> = (event: T) => void;
type ChangeHandler = EventHandler<ChangeEvent<HTMLInputElement>>;
type ClickHandler = EventHandler<MouseEvent>;
```

These utility types help maintain type safety while reducing code duplication and improving maintainability.
