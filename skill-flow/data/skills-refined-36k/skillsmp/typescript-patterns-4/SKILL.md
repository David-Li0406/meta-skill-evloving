---
name: typescript-patterns
description: "TypeScript idioms, type guards, utility types, and type-safe patterns. Use when working with TypeScript types, generics, or type safety issues."
---

# TypeScript Patterns

## Overview

Decision guide for TypeScript patterns focusing on type safety, narrowing, and maintainable type definitions.

## Type Narrowing

### Discriminated Unions (Preferred)

```typescript
// DO: Use discriminated unions for state
type Result<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error }
  | { status: 'loading' };

function handle<T>(result: Result<T>) {
  if (result.status === 'success') {
    return result.data; // TypeScript knows data exists
  }
}
```

### Type Guards

```typescript
// Custom type guard
function isUser(value: unknown): value is User {
  return typeof value === 'object' && value !== null && 'id' in value;
}

// Use assertion functions for validation
function assertUser(value: unknown): asserts value is User {
  if (!isUser(value)) throw new Error('Invalid user');
}
```

## Utility Type Patterns

| Pattern | Use Case |
|---------|----------|
| `Partial<T>` | Optional updates, patch operations |
| `Required<T>` | Ensure all fields present |
| `Pick<T, K>` | Select specific fields |
| `Omit<T, K>` | Exclude fields (API responses) |
| `Record<K, V>` | Type-safe dictionaries |
| `Extract<T, U>` | Filter union types |

### Inference Patterns

```typescript
// Infer return type from function
type ApiResponse = Awaited<ReturnType<typeof fetchUser>>;

// Infer array element type
type Item = (typeof items)[number];

// Const assertion for literal types
const ROLES = ['admin', 'user', 'guest'] as const;
type Role = (typeof ROLES)[number]; // 'admin' | 'user' | 'guest'
```

## Generic Constraints

```typescript
// Constrain generics meaningfully
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Generic with default
type Response<T = unknown> = { data: T; status: number };
```

## Anti-Patterns

### Avoid These

```typescript
// BAD: any defeats type safety
function process(data: any) { ... }

// BAD: Type assertion without validation
const user = response as User;

// BAD: Non-null assertion without guards
user!.profile!.name;

// BAD: Overly complex conditional types
type Complex<T> = T extends A ? B extends C ? D : E : F;
```

### Prefer These

```typescript
// GOOD: unknown with narrowing
function process(data: unknown) {
  if (isValidData(data)) { ... }
}

// GOOD: Validate then use
const user = validateUser(response);

// GOOD: Optional chaining
user?.profile?.name;

// GOOD: Simple, readable types
type Simple<T> = T extends A ? B : C;
```

## Decision Guide

| Situation | Approach |
|-----------|----------|
| Union needs runtime check | Discriminated union with literal discriminant |
| Object might be null/undefined | Optional chaining `?.` |
| External data | `unknown` + type guard |
| Reusing object shape subset | `Pick<T, K>` or `Omit<T, K>` |
| String literals as types | `as const` assertion |
| Complex conditional logic | Break into named types |

## Red Flags

- Using `any` anywhere (use `unknown` instead)
- Multiple `!` non-null assertions in a row
- Type assertions without preceding validation
- `@ts-ignore` or `@ts-expect-error` without explanation
- Types that span 10+ lines (decompose them)

## Quick Reference

```typescript
// Branded types for type-safe IDs
type UserId = string & { readonly brand: unique symbol };
function createUserId(id: string): UserId { return id as UserId; }

// Exhaustive switch check
function assertNever(x: never): never {
  throw new Error(`Unexpected: ${x}`);
}

// Template literal types
type EventName = `on${Capitalize<'click' | 'focus'>}`; // 'onClick' | 'onFocus'
```
