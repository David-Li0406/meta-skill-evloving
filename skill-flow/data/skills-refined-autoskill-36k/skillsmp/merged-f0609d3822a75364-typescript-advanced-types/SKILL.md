---
name: typescript-advanced-types
description: Master TypeScript's advanced type system including generics, conditional types, mapped types, template literals, and utility types. Use when implementing complex type logic, creating reusable type utilities, or ensuring compile-time type safety.
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

## Core Concepts Overview

### 1. Generics
Create reusable, type-flexible components while maintaining type safety.

**Basic Generic Function:**
```typescript
function identity<T>(value: T): T {
  return value;
}
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
```

### 2. Conditional Types
Types that depend on conditions, enabling sophisticated type logic.

**Basic Conditional Type:**
```typescript
type IsString<T> = T extends string ? true : false;
```

### 3. Mapped Types
Transform existing types by iterating over their properties.

**Basic Mapped Type:**
```typescript
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};
```

### 4. Template Literal Types
Create string-based types with pattern matching and transformation.

**Basic Template Literal:**
```typescript
type EventName = 'click' | 'focus' | 'blur';
type EventHandler = `on${Capitalize<EventName>}`; // "onClick" | "onFocus" | "onBlur"
```

### 5. Utility Types
Built-in helpers for common type transformations.

```typescript
type PartialUser = Partial<User>; // Make all properties optional
type RequiredUser = Required<PartialUser>; // Make all properties required
type ReadonlyUser = Readonly<User>; // Make all properties readonly
type UserName = Pick<User, 'name' | 'email'>; // Select specific properties
type UserWithoutPassword = Omit<User, 'password'>; // Remove specific properties
```

## Best Practices

1. **Use `unknown` over `any`** - Enforce type checking.
2. **Prefer `interface` for object shapes** - Better error messages.
3. **Use `type` for unions and complex types** - More flexible.
4. **Leverage type inference** - Let TypeScript infer when possible.
5. **Create helper types** - Build reusable type utilities.
6. **Use const assertions** - Preserve literal types.
7. **Avoid type assertions** - Use type guards instead.
8. **Use strict mode** - Enable all strict compiler options.

## Common Pitfalls

1. Over-using `any` - Defeats TypeScript's purpose.
2. Ignoring strict null checks - Can lead to runtime errors.
3. Too complex types - Can slow down compilation.
4. Not using discriminated unions - Misses type narrowing opportunities.
5. Forgetting readonly modifiers - Allows unintended mutations.
6. Circular type references - Can cause compiler errors.

## Resources

- **TypeScript Handbook**: https://www.typescriptlang.org/docs/handbook/
- **Type Challenges**: https://github.com/type-challenges/type-challenges
- **TypeScript Deep Dive**: https://basarat.gitbook.io/typescript/
- **Effective TypeScript**: Book by Dan Vanderkam