---
name: typescript-advanced-types
description: "Master TypeScript's advanced type system including generics, conditional types, mapped types, template literals, and utility types. Use when implementing complex type logic, creating reusable type utilities, or ensuring compile-time type safety."
allowed-tools: Read Glob Grep
context: fork
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

## Quick Reference

| Topic | Reference | Use When |
|-------|-----------|----------|
| Generics | `references/generics.md` | Type parameters, constraints, inference |
| Conditional Types | `references/conditional-types.md` | Type-level conditions, `infer` keyword |
| Mapped Types | `references/mapped-types.md` | Transform existing types, key remapping |
| Template Literals | `references/template-literals.md` | String manipulation types |
| Utility Types | `references/utility-types.md` | Built-in type helpers |
| Patterns | `references/patterns.md` | Real-world examples, type guards |

## How to Use

1. Load this skill when working with TypeScript types
2. Read the relevant reference file for your specific topic
3. Apply patterns to your implementation

## Core Concepts Overview

### Generics
Create reusable, type-flexible components: `function identity<T>(value: T): T`

### Conditional Types
Types that depend on conditions: `type IsString<T> = T extends string ? true : false`

### Mapped Types
Transform types by iterating properties: `type Readonly<T> = { readonly [P in keyof T]: T[P] }`

### Template Literal Types
String-based types with patterns: `type EventHandler = \`on${Capitalize<EventName>}\``

### Utility Types
Built-in helpers: `Partial`, `Required`, `Pick`, `Omit`, `Record`, `Exclude`, `Extract`

## Best Practices

1. **Use `unknown` over `any`** - Enforce type checking
2. **Prefer `interface` for object shapes** - Better error messages
3. **Use `type` for unions and complex types** - More flexible
4. **Leverage type inference** - Let TypeScript infer when possible
5. **Create helper types** - Build reusable type utilities
6. **Use const assertions** - Preserve literal types
7. **Avoid type assertions** - Use type guards instead
8. **Use strict mode** - Enable all strict compiler options

## Common Pitfalls

1. Over-using `any` - Defeats TypeScript's purpose
2. Ignoring strict null checks - Leads to runtime errors
3. Too complex types - Slows down compilation
4. Not using discriminated unions - Misses type narrowing
5. Forgetting readonly modifiers - Allows unintended mutations
6. Circular type references - Causes compiler errors

## Resources

- **TypeScript Handbook**: https://www.typescriptlang.org/docs/handbook/
- **Type Challenges**: https://github.com/type-challenges/type-challenges
- **TypeScript Deep Dive**: https://basarat.gitbook.io/typescript/
