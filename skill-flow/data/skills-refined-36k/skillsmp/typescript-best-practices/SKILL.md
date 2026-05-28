---
name: typescript-best-practices
description: This skill should be used when the user asks to "review TypeScript code", "check my TS code", "review this TypeScript", "write TypeScript", or when writing, reviewing, or refactoring TypeScript code in projects with tsconfig.json or .ts/.tsx files. Provides dos and don'ts for type design, naming conventions, generics, and patterns.
---

# TypeScript Best Practices

Guidelines for writing clean, type-safe, and maintainable TypeScript code.

> **Note:** If the repository has established code style conventions, follow those first. These guidelines serve as defaults.

## Core Principles

1. **Type-First Design** - Define types before implementation; minimize reliance on inference
2. **Interface for Structure** - Use `interface` for objects, `type` for unions/mapped/conditional
3. **Namespace for Type Organization** - Group related types with namespaces (types only, not runtime)
4. **Generic Const for Strictness** - Use `<const TConfig>` for strict literal inference
5. **Extract, Don't Redefine** - Get types from existing definitions instead of duplicating
6. **Strictest Config** - Use strictest tsconfig base; install `ts-reset` for saner built-in types

## Quick Reference

### interface vs type

| Use | When |
|-----|------|
| `interface` | Object structures, class contracts, extensible APIs |
| `type` | Union types, mapped types, conditional types, tuples |

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Interface/Type | PascalCase | `UserProfile`, `ResponseData` |
| Generic parameters | `T` prefix | `TUser`, `TConfig` (never bare `T`, `K`, `V`) |
| Acronyms | First cap only | `userId`, `ApiResponse` (NOT `userID`, `APIResponse`) |
| Constants | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Variables/Functions | camelCase | `getUserById`, `isActive` |

### Array Syntax

| DO | DON'T |
|----|-------|
| `Array<TItem>` | `TItem[]` |
| `ReadonlyArray<TItem>` | `readonly TItem[]` |

### Object Types

| Use Case | DO | DON'T |
|----------|-----|-------|
| Empty object | `Record<string, never>` | `{}` |
| Any object (extends) | `Record<string, any>` | `Record<string, unknown>` |
| Any object (annotation) | `Record<string, unknown>` | `Record<string, any>` |
| Non-primitive | `object` | `{}` |

### Assertions

| DO | DON'T |
|----|-------|
| Zod/arktype for runtime validation | `response as User` |
| `satisfies` for compile-time checks | `value as unknown as Type` |
| Type guards (`if ('prop' in obj)`) | `as any` to silence errors |
| Explicit null checks | `x!` non-null assertion |

### Function Declarations

```typescript
// DO: Type on the const
const myFunction: myFunction.Type = (options) => {
  // implementation
};

// DO: satisfies when namespace doesn't exist
const onClick = ((event) => {
  // implementation
}) satisfies React.ComponentProps<'button'>['onClick'];
```

### Type Extraction

```typescript
// DO: Extract from existing definitions
type OnClick = React.ComponentProps<'button'>['onClick'];
type ItemIds = Array<Item['id']>;
type TimeoutType = NonNullable<typeof config['timeout']>;

// DON'T: Manually redefine types
type BadItemIds = Array<number>; // Won't update if Item.id changes
```

## Summary Checklist

Before committing TypeScript code, verify:

- [ ] Used `interface` for object types, `type` for unions/mapped/conditional
- [ ] No `as` or `!` assertions — use Zod, `satisfies`, type guards, or explicit null checks
- [ ] Branded types use Zod `.brand()` or type-fest `Tagged` (not manual casting)
- [ ] Naming follows conventions (PascalCase types, `T` prefix for generics, `Id` not `ID`)
- [ ] Types extracted from existing definitions where possible
- [ ] Functions use namespace pattern for complex type organization
- [ ] Arrow functions for const declarations
- [ ] Complex generics have type tests

## Reference Files

For detailed patterns and examples, see:

- **[type-patterns.md](references/type-patterns.md)** - Type syntax, assertions, namespace pattern, generics
- **[code-style.md](references/code-style.md)** - Safe array access, early return, avoid destructuring, avoid enum
- **[union-exhaustive.md](references/union-exhaustive.md)** - Discriminated unions + exhaustive handling (e.g., for state, events, API responses)
- **[branded-types.md](references/branded-types.md)** - Nominal types for ID/unit safety (e.g., UserId vs OrderId)
- **[template-literals.md](references/template-literals.md)** - String pattern types (e.g., event names, CSS values, route parameters)
- **[type-testing.md](references/type-testing.md)** - Type-level testing with `*.test-d.ts` files
- **[setup.md](references/setup.md)** - tsconfig, strict options, ts-reset configuration

## Notes

- These guidelines complement, not replace, project-specific conventions
- When in doubt, prioritize readability and maintainability
- Runtime type validation (zod, arktype) is recommended for external data
- Avoid over-engineering types; simple is better than clever
