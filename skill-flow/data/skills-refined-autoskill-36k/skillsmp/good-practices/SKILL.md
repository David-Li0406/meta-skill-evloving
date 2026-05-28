---
name: good-practices
description: TypeScript coding standards and design principles. Use when writing new code, reviewing code, refactoring, or when guidance is needed on naming conventions, documentation (JSDoc), immutability, strict typing, testing patterns, or design principles like avoiding over-abstraction.
---

# Naming Conventions

- **camelCase** for variables, functions, methods, and parameters
- **PascalCase** for classes, interfaces, types, and enums
- **All code and comments must be in English**
- Names must reveal intent: `getUserById` instead of `get`, `calculateTotalPrice` instead of `calc`
- Boolean variables/methods use prefixes: `isActive`, `hasPermission`, `canEdit`, `shouldRetry`
- Avoid cryptic abbreviations: `transaction` instead of `tx`, `configuration` instead of `cfg`
- Collections should be plural: `users`, `orderItems`, `activeConnections`

# Documentation

- **Every method must have JSDoc comments** including:
  - Description of what the method does
  - `@param` tags with types and descriptions for all parameters
  - `@returns` tag with type and description of the return value
  - `@throws` tag documenting any exceptions the method may throw

Example:

```typescript
/**
 * Calculates the total price including tax.
 * @param {number} basePrice - The base price before tax
 * @param {number} taxRate - The tax rate as a decimal (e.g., 0.21 for 21%)
 * @returns {number} The total price including tax
 * @throws {Error} If basePrice or taxRate is negative
 */
function calculateTotalPrice(basePrice: number, taxRate: number): number {
  if (basePrice < 0 || taxRate < 0) {
    throw new Error('Price and tax rate must be non-negative');
  }
  return basePrice * (1 + taxRate);
}
```

# Design Principles

## Avoid Over-Abstraction

- Only abstract when there is a clear, demonstrated need
- Prefer concrete implementations over premature generalization
- Wait until you have at least two or three concrete use cases before creating an abstraction

## Minimize Long-Term Complexity

- **Concentrate internal complexity behind simple, consistent interfaces** - The implementation can be complex, but the API should be intuitive
- **Create deep abstractions that do much with little** - Prefer modules that provide significant functionality through a minimal interface
- **Avoid premature generalizations** - Solve the problem at hand; don't design for hypothetical future requirements
- **Use comments only to explain decisions and reasoning that the code cannot express** - Comments should answer "why", not "what"

## Interface Design

- Keep public interfaces small and focused
- Hide implementation details aggressively
- Make common operations simple and rare operations possible
- Prefer composition over inheritance when the relationship is not strictly "is-a"

# Immutability by Default

- Prefer `const` over `let` whenever possible
- Use `readonly` for properties that should not be mutated after initialization
- Prefer immutable array methods (`.map()`, `.filter()`, `.reduce()`) over mutations (`.push()`, `.splice()`)
- When state must change, create new objects/arrays instead of mutating existing ones

# Strict Typing

- **Never use `any`** — use `unknown` when the type is truly unknown, then narrow it
- Enable `strict: true` in tsconfig.json
- Prefer specific types over broad generic types
- Use union types and type guards for runtime type safety
- Define explicit return types for public methods

# Testing

- **Every public method must have corresponding unit tests**
- Tests should cover:
  - Happy path (expected behavior with valid inputs)
  - Edge cases (empty arrays, null values, boundary conditions)
  - Error cases (invalid inputs, expected exceptions)
- Test names should describe the expected behavior: `should return null when user is not found`
- Keep tests independent — each test should set up its own data and not depend on other tests
- Aim for tests that are fast, isolated, and deterministic

# Dependencies

- **Always verify the latest version before installing any package**
- Check npm or the official documentation to ensure you are installing the most recent stable version
- Use `npm info <package> version` or check npmjs.com to confirm the latest version
- Avoid installing outdated packages that may have known vulnerabilities or missing features
