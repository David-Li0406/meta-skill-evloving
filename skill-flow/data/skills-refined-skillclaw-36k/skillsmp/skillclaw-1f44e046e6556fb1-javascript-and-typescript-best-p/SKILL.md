---
name: javascript-and-typescript-best-practices
description: Use this skill when you want to apply idiomatic patterns and conventions for clean, maintainable code in both JavaScript and TypeScript.
---

# Implementation Guidelines

## General Guidelines
- **Naming Conventions**:
  - Classes/Types: `PascalCase`
  - Variables/Functions: `camelCase`
  - Constants: `UPPER_SNAKE`
  - Prefix `I` for interfaces only if necessary.

- **Functions**:
  - Use arrow functions for callbacks; regular functions for exports.
  - Always specify return types for public API functions.

- **Modules**:
  - Use named exports only. 
  - Import order: external → internal → relative.

- **Async Handling**:
  - Use `async/await` for asynchronous code, not raw Promises.
  - Use `Promise.all()` for parallel execution.

- **Error Handling**:
  - Throw `Error` objects only. Handle all async errors appropriately.

- **Comments**:
  - Use JSDoc for APIs. Explain "why" not "what".

- **Files**:
  - One entity per file. Use `index.js` or `index.ts` for exports.

## Anti-Patterns
- **Avoid**:
  - Default exports; prefer named exports.
  - Implicit returns; always specify return types.
  - Unused variables; enable `noUnusedLocals`.
  - Using `require`; prefer ES6 `import`.
  - Empty interfaces; use `type` or non-empty interfaces.
  - Using `any`; use `unknown` only when necessary.
  - Globals; encapsulate state.
  - Magic numbers; use constants.
  - Deep nesting; prefer guard clauses and early returns.
  - Side effects; keep functions pure.

## Code Examples

### JavaScript Example
```javascript
// Constants
const STATUS = { OK: 200, ERROR: 500 };

// Errors
class APIError extends Error {
  constructor(msg, code) {
    super(msg);
    this.code = code;
  }
}

// Async + JSDoc
/** @throws {APIError} */
export async function getData(id) {
  if (!id) throw new APIError('Missing ID', 400);
  const res = await fetch(`/api/${id}`);
  if (!res.ok) throw new APIError('Failed', res.status);
  return res.json();
}
```

### TypeScript Example
```typescript
// TypeScript Example
interface User {
  id: number;
  name: string;
}

async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) throw new Error('Failed to fetch user');
  return response.json();
}
```

## Related Topics
- language | tooling | security