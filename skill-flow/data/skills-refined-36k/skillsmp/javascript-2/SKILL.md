---
name: javascript
description: "JavaScript development process and code review. Use when writing JavaScript code, reviewing JavaScript PRs, debugging unexpected behavior, configuring ESLint and Prettier, or setting up testing. Also use when code uses `==` instead of `===`, variables are reassigned frequently, async code isn't awaited, error handling is missing, or module systems are mixed. Essential for ES6+ features, async/await patterns, nullish coalescing, and common JavaScript gotchas."
---

# JavaScript Skill

## Overview

JavaScript's flexibility is both its strength and weakness. This skill guides writing predictable, maintainable JavaScript that avoids common pitfalls.

**Core principle:** Explicit is better than implicit. JavaScript's type coercion and dynamic nature require discipline to write reliably.

## The JavaScript Development Process

### Phase 1: Choose Patterns

**Before writing implementation:**

1. **Module System**
   - Use ES modules (`import`/`export`) for new code
   - CommonJS only for Node.js legacy compatibility
   - Don't mix in the same file

2. **Async Strategy**
   - Use async/await over .then() chains
   - Handle all promise rejections
   - Consider Promise.all for parallel operations

3. **Error Handling**
   - Define custom error types
   - Always catch specific errors
   - Re-throw unexpected errors

### Phase 2: Write Defensively

**Avoid JavaScript's pitfalls:**

1. **Use Strict Comparisons**
   ```javascript
   // ✅ Always use ===
   if (value === null) { }

   // ❌ Type coercion surprises
   if (value == null) { }  // Only OK for null/undefined check
   ```

2. **Prefer const/let**
   ```javascript
   // ✅ Immutable by default
   const config = { api: 'https://...' };

   // ✅ let for reassignment
   let count = 0;

   // ❌ Never use var
   var x = 1;  // Hoisting bugs
   ```

3. **Handle Nullish Values**
   ```javascript
   // ✅ Nullish coalescing for defaults
   const name = user.name ?? 'Anonymous';

   // ❌ || has falsy trap (0, '', false)
   const count = data.count || 10;  // 0 becomes 10!
   ```

### Phase 3: Review for Quality

**Before approving:**

1. **Check Async Handling**
   - All promises awaited or caught?
   - No floating promises?
   - Error boundaries in place?

2. **Check Immutability**
   - Arguments not mutated?
   - Objects cloned before modification?
   - const used where possible?

3. **Check Iteration**
   - for...of for arrays (not for...in)?
   - Appropriate array method used?
   - No mutation in map/filter?

## Red Flags - STOP and Fix

### Type Coercion Red Flags

```javascript
// Loose equality (surprises)
if (x == y) { }

// Falsy trap with ||
const value = input || default;  // 0, '', false become default

// typeof null bug
typeof null === 'object'  // true! Check explicitly

// Array type check
typeof [] === 'object'  // true! Use Array.isArray()
```

### Async Red Flags

```javascript
// Floating promise (unhandled rejection)
doAsyncThing();

// forEach with async (doesn't wait)
items.forEach(async (item) => {
  await process(item);  // Doesn't wait!
});

// Missing error handling
const data = await fetch(url);  // What if it fails?
```

### Mutation Red Flags

```javascript
// Mutating function arguments
function process(options) {
  options.processed = true;  // Mutates caller's object!
}

// Mutating in map
items.map(item => {
  item.processed = true;  // Mutates original!
  return item;
});

// Shallow copy trap
const copy = { ...original };
copy.nested.value = 1;  // Also mutates original.nested!
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "== is fine if you know the types" | You don't always. Use ===. |
| "var is the same as let" | Hoisting causes bugs. Use let/const. |
| "I'll add error handling later" | Later never comes. Handle now. |
| "It's just a quick script" | Scripts become production. Write properly. |
| "The framework handles it" | Frameworks don't catch everything. Be explicit. |

## JavaScript Checklist

Before approving JavaScript code:

- [ ] **Strict equality**: Using === not ==
- [ ] **const/let**: No var usage
- [ ] **Async handled**: All promises awaited or caught
- [ ] **No mutation**: Arguments and arrays not mutated
- [ ] **Nullish**: Using ?? not || for defaults
- [ ] **Error handling**: Errors caught and handled
- [ ] **Linting**: ESLint configured and passing

## Quick Patterns

### Safe Defaults

```javascript
// ✅ Nullish coalescing
const count = data.count ?? 0;
const name = user?.name ?? 'Anonymous';

// ✅ Default parameters
function greet(name = 'World') {
  return `Hello, ${name}!`;
}

// ✅ Destructuring with defaults
const { timeout = 5000, retries = 3 } = options;
```

### Async/Await

```javascript
// ✅ Proper error handling
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}

// ✅ Parallel execution
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
]);
```

### Immutable Updates

```javascript
// ✅ Shallow clone
const updated = { ...original, status: 'active' };

// ✅ Array without mutation
const added = [...items, newItem];
const removed = items.filter(i => i.id !== id);
const modified = items.map(i =>
  i.id === id ? { ...i, status: 'done' } : i
);
```

## Quick Commands

```bash
# Linting
npx eslint . --fix

# Formatting
npx prettier --write .

# Testing
npm test

# Security
npm audit
```

## References

Detailed patterns and examples in `references/`:
- `es6-patterns.md` - Modern JavaScript features
- `async-patterns.md` - Promise and async/await patterns
- `common-mistakes.md` - JavaScript gotchas and fixes
