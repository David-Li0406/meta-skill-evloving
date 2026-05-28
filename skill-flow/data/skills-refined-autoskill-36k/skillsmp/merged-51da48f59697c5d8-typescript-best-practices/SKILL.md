---
name: typescript-best-practices
description: Use this skill to implement idiomatic TypeScript patterns for clean, maintainable code.
---

# TypeScript Best Practices

## **Priority: P1 (OPERATIONAL)**

Idiomatic patterns for writing clean, maintainable TypeScript code.

## Implementation Guidelines

- **Naming Conventions**:
  - Use `PascalCase` for classes, interfaces, types, and enums.
  - Use `camelCase` for variables, functions, methods, and parameters.
  - Use `UPPER_SNAKE_CASE` for constants.
  - Prefix interfaces with `I` only when necessary for disambiguation.
  
- **Functions**:
  - Prefer arrow functions for callbacks and short functions; use regular functions for methods and exported functions.
  - Always specify return types for public APIs.

- **Modules**:
  - Use named exports only; one export per file for major components/classes.
  - Organize imports in the order: external → internal → relative.

- **Async/Await**:
  - Prefer `async/await` over raw Promises and always handle errors with try/catch in async functions.
  - Use `Promise.all()` for parallel operations.

- **Classes**:
  - Explicitly use `private`, `protected`, and `public` modifiers.
  - Favor composition over inheritance and use `readonly` for properties that don't change after construction.

- **Types**:
  - Use `never` for exhaustiveness checking in `switch` cases.
  - Use `asserts` for runtime type validation.
  - Use `?:` for optional properties instead of `| undefined`.
  - Use `import type` for tree-shaking.

## Anti-Patterns

- Avoid default exports; use named exports instead.
- Always specify return types to avoid implicit returns.
- Enable `noUnusedLocals` to prevent unused variables.
- Use ES6 `import` instead of `require`.
- Avoid empty interfaces; prefer `type` or non-empty interfaces.
- Never use `any`; use `unknown` only when necessary.

## Code Examples

```typescript
// Named Export + Immutable Interface
export interface User {
  readonly id: string;
  name: string;
}

// Exhaustive Check
function getStatus(s: 'ok' | 'fail') {
  switch (s) {
    case 'ok': return 'OK';
    case 'fail': return 'Fail';
    default: const _chk: never = s; return _chk;
  }
}

// Assertion
function assertDefined<T>(val: T): asserts val is NonNullable<T> {
  if (val == null) throw new Error("Defined expected");
}

// Organize imports
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

import { UserRepository } from '@/repositories/user.repository';
import { Logger } from '@/utils/logger';

// Type-only imports
import type { Request, Response } from 'express';
```

## Reference & Examples

For project structure and module organization, see [references/REFERENCE.md](references/REFERENCE.md).

## Related Topics

language | tooling | security