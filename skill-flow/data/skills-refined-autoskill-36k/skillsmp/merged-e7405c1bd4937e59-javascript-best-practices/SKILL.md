---
name: javascript-best-practices
description: Use this skill for idiomatic JavaScript patterns and conventions to ensure maintainable code.
---

# JavaScript Best Practices

## **Priority: P1 (OPERATIONAL)**

Conventions and patterns for writing maintainable JavaScript.

## Implementation Guidelines

- **Naming**: `camelCase` for variables/functions, `PascalCase` for classes, and `UPPER_SNAKE` for constants.
- **Errors**: Always throw `Error` objects and handle all asynchronous errors.
- **Comments**: Use JSDoc for APIs, focusing on explaining "why" rather than "what".
- **Files**: Each file should contain one entity, with `index.js` used for exports.
- **Modules**: Prefer named exports only, following the order: External -> Internal -> Related.

## Anti-Patterns

- **No Globals**: Encapsulate state to avoid global variables.
- **No Magic Numbers**: Use `const` for constants instead of hardcoded values.
- **No Nesting**: Utilize guard clauses and early returns to reduce nesting.
- **No Defaults**: Favor named exports over default exports.
- **No Side Effects**: Strive to keep functions pure without side effects.

## Code Example

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

// Async function with JSDoc
/** @throws {APIError} */
export async function getData(id) {
  if (!id) throw new APIError('Missing ID', 400);
  const res = await fetch(`/api/${id}`);
  if (!res.ok) throw new APIError('Failed', res.status);
  return res.json();
}
```

## Reference & Examples

For module patterns and project structure, refer to the relevant documentation.

## Related Topics

language | tooling