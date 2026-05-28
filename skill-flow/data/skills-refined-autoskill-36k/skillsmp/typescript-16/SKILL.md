---
name: typescript
description: TypeScript/JavaScript coding standards. Use when working on TS/JS code to ensure type safety, proper async handling, and clean code style.
---

# TypeScript / JavaScript

Critical rules for TypeScript and JavaScript development.

---

## Types & Safety

- Use strict TypeScript (`strict: true`); avoid `any`, `unknown` only when truly unknown
- Prefer `interface` for object shapes; `type` for unions/intersections/utilities
- No implicit `any`; explicit return types on exported functions
- Use `as const` for literals; avoid type assertions (`as`) unless unavoidable
- Nullish: prefer `??` over `||`; use optional chaining `?.` over manual checks

## Code Style

- `const` by default; `let` only when mutation needed; never `var`
- Destructure props/objects at function entry
- Arrow functions for callbacks; named functions for top-level/exported
- No dead code, unused imports, or commented-out blocks

## Async & Error Handling

- Always `await` promises or explicitly handle them; no floating promises
- Use try/catch for async; propagate errors with context
- Avoid `.then()/.catch()` chains; prefer async/await

## Modules & Imports

- Imports at file top, grouped: external → internal → types
- Prefer named exports; default exports only for pages/components where framework requires
- No circular imports
