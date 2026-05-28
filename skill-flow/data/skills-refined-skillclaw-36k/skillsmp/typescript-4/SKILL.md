---
name: typescript
description: Write type-safe TypeScript. Use when writing or reviewing TypeScript code. Covers type safety best practices, avoiding dangerous features (any/as), and proper narrowing techniques.
---

# TypeScript

## Checklist

1. **No `any`** - Use `unknown` and validate with valibot
2. **No `as`** - Fix types at source
3. **No `!`** - Explicit checks instead
4. **NO `value is T`** - Use a validator library like valibot instead
5. **Discriminated unions** - Add `type` field to narrow

## Good Practices

1. `as const` - For literal types only
2. `value satisfies T` - Type-checks value without changing its type (safe, unlike `is T`)
3. Builtin narrowing - `typeof`, `Array.isArray`, `in`, `instanceof` are always safe
4. `T extends SomeType` if T is required to have some trait
5. `foo?.bar` - Use `?.` for safe property access
6. Tagged unions - `type User = { role: "admin"; permissions: string[] } | { role: "guest"; expiresAt: Date }` then narrow with `if (user.role === "admin")`
7. When refactoring - Fix ONE type error at a time (type inference changes)
8. Const string unions - `type Status = "pending" | "active" | "done"` instead of enums

## When Stuck - NEVER Give Up

**IMPORTANT: Every time you encounter a type error, repeat this checklist in your response before attempting a fix.**

When you're stuck and considering `any` or `as`, STOP:

1. **Read the library's documentation** - Most type issues come from misunderstanding the library API
2. **Search GitHub issues** (library repo) - Someone likely faced the same problem
3. Read error message more carefully
4. Use valibot to validate (if the type is unknown at runtime)
5. Ask the user

**`any` and `as` are admitting defeat.** Always use choose another method.
