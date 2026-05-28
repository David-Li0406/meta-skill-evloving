---
name: javascript-language-patterns
description: Use this skill for implementing modern JavaScript (ES2022+) patterns to ensure clean and maintainable code.
---

# JavaScript Language Patterns

## **Priority: P0 (CRITICAL)**

Modern JavaScript standards for clean, maintainable code.

## Implementation Guidelines

- **Variables**: Use `const` by default; use `let` if necessary. Avoid `var`.
- **Functions**: Prefer arrow functions for callbacks and function declarations for top-level functions.
- **Async**: Utilize `async/await` with `try/catch` for asynchronous operations.
- **Objects**: Implement destructuring, spread `...`, optional chaining `?.`, and nullish coalescing `??`.
- **Strings**: Use template literals `${}` for string interpolation.
- **Arrays**: Employ `map`, `filter`, and `reduce` methods; avoid traditional loops.
- **Modules**: Use ESM `import`/`export` syntax and export only what is necessary.
- **Classes**: Implement `#private` fields for true privacy.

## Anti-Patterns

- **No `var`**: Stick to block scope only.
- **No `==`**: Always use strict equality `===`.
- **No `new Object()`**: Use object literals `{}` instead.
- **No Callbacks**: Promisify all asynchronous operations.
- **No Mutation**: Prioritize immutability.

## Code Examples

```javascript
// Modern Syntax
const [x, ...rest] = items;
const name = user?.profile?.name ?? 'Guest';

// Async
async function getUser(id) {
  try {
    const res = await fetch(`/api/${id}`);
    return res.json();
  } catch (err) {
    console.error(err);
    throw err;
  }
}

// Class + Private
class Service {
  #key;
  constructor(k) {
    this.#key = k;
  }
}
```

## Reference & Examples

For advanced patterns and functional programming, refer to additional resources.

## Related Topics

best-practices | tooling