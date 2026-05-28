---
name: typescript-next-tailwind
description: Next.js TypeScript Tailwind stack template
argument-hint: N/A
---

# Architecture

## Clean architecture

Layer Structure:

- Separate code by layer: Domain, Application, Infrastructure, Presentation
- Direct dependencies inward only
- Keep domain layer framework-agnostic
- Define interfaces at layer boundaries

Domain Layer:

- Place business logic and entities here
- Use pure, framework-free models
- Define domain services for complex logic
- Declare repository interfaces only

Application Layer:

- Implement use cases as orchestrators
- Keep services single-responsibility
- Use DTOs for all data transfer
- Validate input at boundaries

Infrastructure Layer:

- Implement domain repository interfaces
- Isolate external systems (DB, APIs, files)
- Keep infrastructure out of business logic

Presentation Layer:

- Handle API requests and responses
- Use controllers for HTTP logic
- Centralize error handling and validation
- Format all responses consistently

## Feature based architecture

- Organize code by business feature
- Place all feature code in its own folder
- Co-locate components, hooks, and state per feature
- Use shared folders for common code
- Store features in `features/` directory
- Use global state only for app-wide concerns

# Standards

## Naming convention

General Principles:

- Use descriptive names
- Reveal intent in all names
- No single-letter names (except loops)
- No abbreviations except common ones
- Use consistent terminology

Functions and Methods:

- Use verbs for actions
- Use nouns for value-returning
- Prefix booleans with is, has, should
- No anemic models

Variables and Properties:

- Use plural for arrays/collections

Constants:

- Use UPPER_SNAKE_CASE
- Scope constants appropriately
- Group related constants in enum or object

## Clean code

Code Quality:

- Write no comments
- Use strict types only
- Disallow untyped values
- Use explicit constants, never magic numbers
- Avoid double negatives
- Use long, readable variable names
- Write the simplest code possible
- Eliminate duplication (DRY)

Length Limits:

- Max 30 lines per function
- Max 5 params per function
- Max 300 lines per file
- Max 10 sub-files per folder

Responsibilities:

- One responsibility per file

Functions:

- No flag parameters

Errors:

- Fail fast
- Throw errors early
- Use custom domain errors
- Translate errors to user language
- Log errors in EN with error codes

## Clean code for frontend

- Use smart/dumb component pattern
- Smart components handle data and logic
- Dumb components display only, use interfaces

# Typescript

Classes and Interfaces:

- Use PascalCase for names
- Use nouns or noun phrases

Functions and Methods:

- Use camelCase for names
- Use verbs for actions
- Use nouns for value-returning
- Prefix booleans with is, has, should
- No anemic models

Strict Types:

- Type everything explicitly
- Never use `any` or `unknown`
- Avoid `as` for type conversion
- Use type guards for assertions
- Use generics for reusable functions

Interfaces and Types:

- Use `interface` for extensible objects
- Use `type` for unions and primitives

Nullability:

- Avoid `null` and `undefined` in returns

Enumerations:

- Prefer string literal unions to enums
- Use const enums if needed
- Define enum values explicitly

Lint & Error:

- Catch errors as `unknown | Error`

Generics:

- Use descriptive type parameter names

# NextJS

Architecture:

- Use modular structure

Modules:

- Import new files in parent module

Classes:

- Use DI for external interactions
- Use plain class for utilities

Controllers:

- Only handle HTTP layer
- Use DTOs for input/output
- Call use-cases, not repositories

Domain Objects:

- Validate with class-validator

Domain Services:

- Encapsulate domain logic
- No DB access

Use Cases:

- Use commands/queries for DB
- Never call DB directly

Repositories:

- Implement domain interface
- Export const KEY
- Type with model property
- Return domain objects only
- Keep Prisma types internal

Mappers:

- Use DI for mappers
- Map all properties
- Return validated instances

Testing:

- Use Jest
- Import all modules
- No DB mock for integration

Seed:

- Use Prisma types
- Assume empty DB
- Inject as service

# Tailwind CSS Standards

Configuration:

- Use CSS-based configuration in `tailwind.css`.

CSS Variables:

- Use CSS variables for theme values.
  - ✅ `var(--color-red-500)`
  - ❌ `theme(colors.red.500)`
- Use CSS variable names for media queries.
  - ✅ `theme(--breakpoint-xl)`
  - ❌ `theme(screens.xl)`

Custom Utilities:

- Register custom utilities with `@utility`.

```css
@utility btn {
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: ButtonFace;
}
```

Variants:

- Apply variants left-to-right.
  - ✅ `*:first:pt-0`
  - ❌ `first:*:pt-0`
- Use parentheses for arbitrary CSS variables.
  - ✅ `bg-(--brand-color)`
  - ❌ `bg-[--brand-color]`

Responsive Design:

- Scope hover styles with `@media (hover: hover)`.
- Avoid hover for critical functionality.

Component Frameworks (Vue/Svelte/CSS Modules):

- Import theme with `@reference`.

```css
@reference "../../app.css";
```

- Prefer direct CSS variables over `@apply`.

```css
/* ✅ Preferred */
h1 { color: var(--text-red-500); }

/* ❌ Avoid when possible */
h1 { @apply text-red-500; }
```

Removed Features:

- Avoid deprecated opacity utilities (`bg-black/50`).
  - ✅ `bg-black/50`
  - ❌ `bg-opacity-50`
- Avoid `@tailwind` directives (`@import "tailwindcss"`).
  - ✅ `@import "tailwindcss"`
  - ❌ `@tailwind base`
- Avoid JS config features (`corePlugins`, etc.).

Best Practices:

- Use modern CSS features (`@property`, `color-mix()`).
- Include outline colors for transitions.

```html
<button class="transition outline-cyan-500 hover:outline-2">
```

- Sort utilities by property count.
- Use CSS cascade layers for organization.
