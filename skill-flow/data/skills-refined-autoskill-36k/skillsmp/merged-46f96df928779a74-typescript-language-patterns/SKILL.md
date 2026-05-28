---
name: typescript-language-patterns
description: Use this skill when you need to apply modern TypeScript standards for type safety, performance, and maintainability in your code.
---

# TypeScript Language Patterns

## **Priority: P0 (CRITICAL)**

Modern TypeScript standards for type-safe, maintainable code.

## Implementation Guidelines

- **Type Annotations**: Explicit params/returns. Infer locals.
- **Interfaces vs Types**: Use `interface` for APIs and `type` for unions.
- **Strict Mode**: Enable `strict: true`.
- **Null Safety**: Utilize `?.` and `??`.
- **Enums**: Prefer literal unions or `as const`.
- **Generics**: Write reusable, type-safe code.
- **Type Guards**: Implement `typeof`, `instanceof`, and predicates.
- **Utility Types**: Use `Partial`, `Pick`, `Omit`, `Record`.
- **Immutability**: Favor `readonly` arrays/objects.
- **Const Assertions**: Apply `as const` and `satisfies`.
- **Template Literals**: Format with `on${Capitalize<string>}`.
- **Discriminated Unions**: Include a literal `kind` property.
- **Advanced Types**: Explore Mapped, Conditional, and Indexed types.
- **Access Modifiers**: Default to `public`, use `private`/`protected` or `#private` for internals.
- **Branded Types**: Define as `string & { __brand: 'Id' }`.

## Anti-Patterns

- **Avoid `any`**: Use `unknown` instead.
- **Avoid `Function`**: Specify function signatures like `() => void`.
- **Avoid `enum`**: Be aware of runtime costs.
- **Avoid `!`**: Use type narrowing.

## Code Examples

```typescript
// Branded Type
type UserId = string & { __brand: 'Id' };

// Satisfies (Validate + Infer)
const cfg = { port: 3000 } satisfies Record<string, number>;

// Discriminated Union
type Result<T> = { kind: 'ok'; data: T } | { kind: 'err'; error: Error };
```

## Reference & Examples

For advanced type patterns and utility types, refer to additional resources.

## Related Topics

best-practices | security | tooling