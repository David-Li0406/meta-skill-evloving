---
name: typescript-language-patterns
description: Use this skill when you want to apply modern TypeScript standards for type safety, performance, and maintainability in your code.
---

# TypeScript Language Patterns

## **Priority: P0 (CRITICAL)**

Modern TypeScript standards for type-safe, maintainable code.

## Implementation Guidelines

- **Type Annotations**: Use explicit parameters and return types. Infer local variables where appropriate.
- **Interfaces vs Types**: Use `interface` for defining APIs and `type` for unions.
- **Strict Mode**: Enable strict mode with `strict: true` in your `tsconfig.json`.
- **Null Safety**: Utilize optional chaining (`?.`) and nullish coalescing (`??`).
- **Enums**: Prefer literal unions or use `as const` for constant values.
- **Generics**: Write reusable, type-safe code using generics.
- **Type Guards**: Implement type guards using `typeof`, `instanceof`, and custom predicates.
- **Utility Types**: Leverage built-in utility types like `Partial`, `Pick`, `Omit`, and `Record`.
- **Immutability**: Use `readonly` for arrays and objects to enforce immutability.
- **Const Assertions**: Use `as const` and `satisfies` for literal values and type validation.
- **Template Literals**: Use template literals for dynamic string creation, e.g., `on${Capitalize<string>}`.
- **Discriminated Unions**: Implement discriminated unions with a literal `kind` property.
- **Advanced Types**: Explore mapped, conditional, and indexed types for complex scenarios.
- **Access Modifiers**: Default to `public` access. Use `private` or `protected` for internal members.

## Anti-Patterns

- **Avoid `any`**: Use `unknown` instead of `any` for better type safety.
- **Avoid `Function`**: Specify function signatures instead of using the generic `Function` type.
- **Avoid Enums**: Minimize the use of enums due to runtime costs.
- **Avoid Non-null Assertion (`!`)**: Use type narrowing instead of non-null assertions.

## Code Examples

```typescript
// Branded Type
type UserId = string & { __brand: 'Id' };

// Satisfies (Validate + Infer)
const cfg = { port: 3000 } satisfies Record<string, number>;

// Discriminated Union
type Result<T> = { kind: 'ok'; data: T } | { kind: 'err'; error: Error };
```

## Related Topics

best-practices | security | tooling