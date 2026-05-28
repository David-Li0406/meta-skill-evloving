---
name: typescript-javascript-coding-standards
description: Use this skill when writing, reviewing, or refactoring JavaScript and TypeScript code to ensure adherence to best practices and coding standards.
---

# Coding Standards for JavaScript and TypeScript

## General Principles

- Use existing APIs that return promises instead of constructing promises with `new`.
- Use TypeScript for all code, defining strict types for all message passing between components.
- Prefer interfaces over types for object definitions and avoid enums; use const objects with 'as const' assertion.

## Naming Conventions

- **camelCase** for variables, functions, methods, and parameters.
- **PascalCase** for classes, interfaces, types, and enums.
- All code and comments must be in English.
- Names must reveal intent: `getUserById` instead of `get`, `calculateTotalPrice` instead of `calc`.
- Boolean variables/methods use prefixes: `isActive`, `hasPermission`, `canEdit`, `shouldRetry`.
- Avoid cryptic abbreviations: `transaction` instead of `tx`, `configuration` instead of `cfg`.
- Collections should be plural: `users`, `orderItems`, `activeConnections`.

## Documentation

- Every method must have JSDoc comments including:
  - Description of what the method does.
  - `@param` tags with types and descriptions for all parameters.
  - `@returns` tag with type and description of the return value.
  - `@throws` tag documenting any exceptions the method may throw.

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

## Type Safety

- Never use `any` - define explicit types.
- Avoid type assertions (`as`) when possible.
- Resolve type errors immediately.
- Prefer union types and discriminated unions.

## Error Handling

- Never use exceptions for control flow.
- Use the Result<T, E> pattern for internal logic and domain functions.
- Use try-catch for error translation when necessary.

## Component Architecture Patterns

### Pattern 1: Direct Import

- Use for simple, single-purpose components with no reuse needs.
- Trade-offs: Simple, less boilerplate but harder to test.

### Pattern 2: Feature Layer + Presentational Components

- Use for reusable components across contexts with complex business logic.
- Trade-offs: Testable and reusable but can lead to over-engineering.

## Design Principles

- Avoid over-abstraction; only abstract when there is a clear need.
- Concentrate internal complexity behind simple, consistent interfaces.
- Create deep abstractions that do much with little.
- Use comments to explain decisions and reasoning.