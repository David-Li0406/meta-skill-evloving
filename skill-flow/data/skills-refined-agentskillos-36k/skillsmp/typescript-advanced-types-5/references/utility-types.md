# Utility Types

Built-in TypeScript utility types for common type transformations.

## Object Transformation

### Partial<T>

Make all properties optional:

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

type PartialUser = Partial<User>;
// Type: { id?: string; name?: string; email?: string; }

function updateUser(id: string, updates: Partial<User>) {
  // Only pass fields that need updating
}
```

### Required<T>

Make all properties required:

```typescript
interface Config {
  host?: string;
  port?: number;
}

type RequiredConfig = Required<Config>;
// Type: { host: string; port: number; }
```

### Readonly<T>

Make all properties readonly:

```typescript
type ReadonlyUser = Readonly<User>;
// Type: { readonly id: string; readonly name: string; readonly email: string; }
```

### Pick<T, K>

Select specific properties:

```typescript
type UserPreview = Pick<User, "id" | "name">;
// Type: { id: string; name: string; }
```

### Omit<T, K>

Remove specific properties:

```typescript
type UserWithoutEmail = Omit<User, "email">;
// Type: { id: string; name: string; }
```

### Record<K, T>

Create object type with keys K and values T:

```typescript
type PageInfo = Record<"home" | "about" | "contact", { title: string; url: string }>;
// Type: { home: { title: string; url: string }; about: ...; contact: ...; }

type StringMap = Record<string, string>;
// Type: { [key: string]: string }
```

## Union Manipulation

### Exclude<T, U>

Exclude types from union:

```typescript
type T1 = Exclude<"a" | "b" | "c", "a">;
// Type: "b" | "c"

type T2 = Exclude<string | number | boolean, boolean>;
// Type: string | number
```

### Extract<T, U>

Extract types from union:

```typescript
type T1 = Extract<"a" | "b" | "c", "a" | "b">;
// Type: "a" | "b"

type T2 = Extract<string | number | (() => void), Function>;
// Type: () => void
```

### NonNullable<T>

Exclude null and undefined:

```typescript
type T = NonNullable<string | null | undefined>;
// Type: string
```

## Function Types

### Parameters<T>

Extract function parameter types as tuple:

```typescript
function greet(name: string, age: number): string {
  return `Hello ${name}, you are ${age}`;
}

type GreetParams = Parameters<typeof greet>;
// Type: [string, number]
```

### ReturnType<T>

Extract function return type:

```typescript
type GreetReturn = ReturnType<typeof greet>;
// Type: string
```

### ConstructorParameters<T>

Extract constructor parameter types:

```typescript
class User {
  constructor(public id: string, public name: string) {}
}

type UserConstructorParams = ConstructorParameters<typeof User>;
// Type: [string, string]
```

### InstanceType<T>

Extract instance type from constructor:

```typescript
type UserInstance = InstanceType<typeof User>;
// Type: User
```

## String Manipulation

```typescript
type Upper = Uppercase<"hello">; // "HELLO"
type Lower = Lowercase<"HELLO">; // "hello"
type Cap = Capitalize<"hello">; // "Hello"
type Uncap = Uncapitalize<"Hello">; // "hello"
```

## Promise Unwrapping

### Awaited<T>

Recursively unwrap Promise types:

```typescript
type A = Awaited<Promise<string>>; // string
type B = Awaited<Promise<Promise<number>>>; // number
type C = Awaited<boolean | Promise<string>>; // boolean | string
```

## This Parameter

### ThisParameterType<T>

Extract `this` parameter type:

```typescript
function greet(this: { name: string }) {
  console.log(`Hello, ${this.name}`);
}

type GreetThis = ThisParameterType<typeof greet>;
// Type: { name: string }
```

### OmitThisParameter<T>

Remove `this` parameter:

```typescript
type GreetWithoutThis = OmitThisParameter<typeof greet>;
// Type: () => void
```

## Combining Utility Types

```typescript
// Make all properties optional and readonly
type PartialReadonly<T> = Readonly<Partial<T>>;

// Pick properties and make them required
type RequiredPick<T, K extends keyof T> = Required<Pick<T, K>>;

// Omit properties and make rest partial
type PartialExcept<T, K extends keyof T> = Partial<Omit<T, K>> & Pick<T, K>;

interface User {
  id: string;
  name: string;
  email?: string;
  age?: number;
}

type CreateUser = PartialExcept<User, "id" | "name">;
// Type: { id: string; name: string; email?: string; age?: number; }
```
