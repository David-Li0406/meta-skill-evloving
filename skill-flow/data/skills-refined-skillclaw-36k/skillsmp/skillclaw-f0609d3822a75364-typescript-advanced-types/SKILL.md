---
name: typescript-advanced-types
description: Use this skill when you need to master TypeScript's advanced type system, including generics, conditional types, mapped types, template literals, and utility types, to build robust and type-safe applications.
---

# TypeScript Advanced Types

Comprehensive guidance for mastering TypeScript's advanced type system.

## When to Use This Skill

- Building type-safe libraries or frameworks
- Creating reusable generic components
- Implementing complex type inference logic
- Designing type-safe API clients
- Building form validation systems
- Creating strongly-typed configuration objects
- Implementing type-safe state management
- Migrating JavaScript codebases to TypeScript

## Core Concepts

### 1. Generics

**Purpose:** Create reusable, type-flexible components while maintaining type safety.

**Basic Generic Function:**

```typescript
function identity<T>(value: T): T {
  return value;
}

const num = identity<number>(42); // Type: number
const str = identity<string>('hello'); // Type: string
const auto = identity(true); // Type inferred: boolean
```

**Generic Constraints:**

```typescript
interface HasLength {
  length: number;
}

function logLength<T extends HasLength>(item: T): T {
  console.log(item.length);
  return item;
}

logLength('hello'); // OK: string has length
logLength([1, 2, 3]); // OK: array has length
logLength({ length: 10 }); // OK: object has length
// logLength(42);             // Error: number has no length
```

**Multiple Type Parameters:**

```typescript
function merge<T, U>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 };
}

const merged = merge({ name: 'John' }, { age: 30 });
// Type: { name: string } & { age: number }
```

### 2. Conditional Types

**Purpose:** Create types that depend on conditions, enabling sophisticated type logic.

**Basic Conditional Type:**

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<string>; // true
type B = IsString<number>; // false
```

**Extracting Return Types:**

```typescript
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

function getUser() {
  return { id: 1, name: 'John' };
}

type User = ReturnType<typeof getUser>;
// Type: { id: number; name: string }
```

### 3. Mapped Types

**Purpose:** Transform existing types by iterating over their properties.

```typescript
type Readonly<T> = { readonly [P in keyof T]: T[P] };
type Partial<T> = { [P in keyof T]?: T[P] };
```

### 4. Template Literal Types

**Purpose:** Create string-based types with patterns.

```typescript
type EventName = "click" | "focus" | "blur";
type EventHandler = `on${Capitalize<EventName>}`; // "onClick" | "onFocus" | "onBlur"
```

### 5. Utility Types

**Purpose:** Use built-in helpers for common type transformations.

- `Partial<T>`: Makes all properties optional.
- `Required<T>`: Makes all properties required.
- `Readonly<T>`: Makes all properties readonly.
- `Pick<T, K>`: Selects a subset of properties.
- `Omit<T, K>`: Excludes a subset of properties.

## Best Practices

1. **Use `unknown` over `any`** - Enforce type checking.
2. **Prefer `interface` for object shapes** - Better error messages.
3. **Use `type` for unions and complex types** - More flexible.
4. **Leverage type inference** - Let TypeScript infer when possible.
5. **Create helper types** - Build reusable type utilities.
6. **Use const assertions** - Preserve literal types.
7. **Avoid type assertions** - Use them sparingly to maintain type safety.