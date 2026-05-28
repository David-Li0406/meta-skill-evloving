---
name: functional-programming
description: Use this skill when writing logic or data transformations with a focus on functional programming principles and immutable data.
---

# Functional Patterns

## Core Principles

- **No data mutation** - immutable structures only
- **Pure functions** wherever possible
- **Composition** over inheritance
- **No comments** - code should be self-documenting
- **Array methods** over loops
- **Options objects** over positional parameters

---

## Why Immutability Matters

Immutable data is the foundation of functional programming. Understanding WHY helps you embrace it:

- **Predictable**: Same input always produces same output (no hidden state changes)
- **Debuggable**: State doesn't change unexpectedly - easier to trace bugs
- **Testable**: No hidden mutable state makes tests straightforward
- **React-friendly**: React's reconciliation and memoization optimizations work correctly
- **Concurrency-safe**: No race conditions when data can't change

**Example of the problem:**
```typescript
// ❌ WRONG - Mutation creates unpredictable behavior
const user = { name: 'Alice', permissions: ['read'] };
grantPermission(user, 'write'); // Mutates user.permissions internally
console.log(user.permissions); // ['read', 'write'] - SURPRISE! user changed
```

```typescript
// ✅ CORRECT - Immutable approach is predictable
const user = { name: 'Alice', permissions: ['read'] };
const updatedUser = grantPermission(user, 'write'); // Returns new object
console.log(user.permissions); // ['read'] - original unchanged
console.log(updatedUser.permissions); // ['read', 'write'] - new version
```

---

## Functional Light

We follow "Functional Light" principles - practical functional patterns without heavy abstractions:

**What we DO:**
- Pure functions and immutable data
- Composition and declarative code
- Array methods over loops
- Type safety and readonly

**What we DON'T do:**
- Category theory or monads
- Heavy FP libraries (fp-ts, Ramda)
- Over-engineering with abstractions
- Functional for the sake of functional

**Why:** The goal is **maintainable, testable code** - not academic purity. If a functional pattern makes code harder to understand, don't use it.

**Example - Keep it simple:**
```typescript
// ✅ GOOD - Simple, clear, functional
const activeUsers = users.filter(u => u.active);
const userNames = activeUsers.map(u => u.name);

// ❌ OVER-ENGINEERED - Unnecessary abstraction
const compose = <T>(...fns: Array<(arg: T) => T>) => (x: T) =>
  fns.reduceRight((v, f) => f(v);
```