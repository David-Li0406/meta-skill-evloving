---
name: typescript-standard
description: "TypeScript coding standards. Use when: writing or reviewing TypeScript code (*.ts, *.tsx)."
---

# TypeScript Standard

## 1. Programming Paradigm

- **Class-less by Default**: Write logic as pure functions (Stateless & Idempotent)
- **Stateless Modules**: Avoid module-scope `let` or singletons; push side effects outside functions

## 2. Type Definition Strategy

### Use `type` when:

- Union/Intersection types are needed (e.g., `A | B`)
- Creating aliases for primitives or tuples
- Defining React Props or internal data models (prevents unintended Declaration Merging)

### Use `interface` when:

- Defining public library APIs that allow extension
- Using `implements` to constrain class shapes (when classes are exceptionally needed)

## 3. Schema & Validation

- **Zod First**: Define Zod schemas for API responses and external inputs; extract types with `z.infer`
- **No Type Assertion**: Avoid `as` casts; use Zod's `.parse()` or type guards for safe type narrowing

## 4. Error Handling

- **Result Pattern**: Prefer `Result<T, E>` (neverthrow) or Zod's `safeParse` over `throw`
- **Discriminated Unions for State**: Use tagged unions for state representation (e.g., `{ status: "success"; data: T } | { status: "error"; error: E }`)

## 5. Immutability

- **Readonly by Default**: Use `readonly` for object properties and `ReadonlyArray<T>` for arrays
- **Const Assertions**: Use `as const` for literal types
- **No Mutations**: Avoid `.push()`, `.splice()`, direct property assignment; use spread or `.map()` / `.filter()`

## 6. Review Checklist

When reviewing code:

1. If classes are used, suggest rewriting as functions
2. If module-level state exists, suggest injecting as arguments
3. If `any` or inappropriate `interface` is used, recommend `type` or Zod schema
4. If `throw` is used for expected errors, suggest Result pattern or `safeParse`
5. If complex state uses boolean flags, suggest discriminated unions
6. If mutable operations (`.push()`, direct assignment) are used, suggest immutable alternatives
