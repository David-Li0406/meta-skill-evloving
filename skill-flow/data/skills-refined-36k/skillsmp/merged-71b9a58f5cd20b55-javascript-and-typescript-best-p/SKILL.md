---
name: javascript-and-typescript-best-practices
description: Use this skill when writing, reviewing, or refactoring JavaScript and TypeScript code, focusing on coding standards, design principles, and testing practices.
---

# JavaScript and TypeScript Best Practices

## General Coding Standards

- Use existing APIs that return promises instead of constructing promises with `new`.
- **Functional Domain Modeling** design: Use functions instead of classes.
- **Imports**: Use `./` for same directory imports and `@/` for cross-directory or global imports.

## Naming Conventions

- Use **camelCase** for variables, functions, methods, and parameters.
- Use **PascalCase** for classes, interfaces, types, and enums.
- All code and comments must be in English.
- Names must reveal intent: e.g., `getUserById` instead of `get`.
- Boolean variables/methods should use prefixes: `isActive`, `hasPermission`.
- Avoid cryptic abbreviations: e.g., `transaction` instead of `tx`.
- Collections should be plural: e.g., `users`, `orderItems`.

## Documentation

- Every method must have JSDoc comments, including:
  - Description of what the method does.
  - `@param` tags with types and descriptions for all parameters.
  - `@returns` tag with type and description of the return value.
  - `@throws` tag documenting any exceptions the method may throw.

## Design Principles

### Avoid Over-Abstraction

- Only abstract when there is a clear, demonstrated need.
- Prefer concrete implementations over premature generalization.

### Minimize Long-Term Complexity

- Concentrate internal complexity behind simple, consistent interfaces.
- Create deep abstractions that do much with little.
- Use comments only to explain decisions and reasoning that the code cannot express.

### Immutability by Default

- Prefer `const` over `let` whenever possible.
- Use `readonly` for properties that should not be mutated after initialization.
- Prefer immutable array methods (`.map()`, `.filter()`, `.reduce()`) over mutations.

### Strict Typing

- Never use `any` — use `unknown` when the type is truly unknown.
- Enable `strict: true` in `tsconfig.json`.
- Prefer specific types over broad generic types.

## Testing Practices

- Every public method must have corresponding unit tests.
- Tests should cover:
  - Happy path (expected behavior with valid inputs).
  - Edge cases (empty arrays, null values).
  - Error cases (invalid inputs).
- Test names should describe the expected behavior.

### Testing Policy

- Minimal unit tests only; avoid E2E tests.
- Test business logic and critical functions only.
- Place `*.test.ts(x)` adjacent to source files.

## Error Handling

- Never use exceptions for control flow.
- Use the `Result<T, E>` pattern for internal logic and domain functions.
- Use try-catch for external operations (I/O, DB, fetch).

### Result Pattern Example

```typescript
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

// Example function using Result pattern
function parseId(input: unknown): Result<string, "Invalid ID"> {
  return typeof input === "string" && input !== ""
    ? { ok: true, value: input }
    : { ok: false, error: "Invalid ID" };
}
```

## Dependencies

- Always verify the latest version before installing any package.
- Check npm or the official documentation to ensure you are installing the most recent stable version.