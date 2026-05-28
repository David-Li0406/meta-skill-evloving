---
name: elegant-defense-philosophy
description: Use this skill to apply the 5 Laws of Elegant Defense in your code, ensuring that data flows naturally and errors are minimized.
---

# The 5 Laws of Elegant Defense

**Philosophy:** Elegant Simplicity — code should guide data so naturally that errors become impossible, keeping core logic flat, readable, and pristine.

## Law 1: Early Exit (Guard Clauses)

**Concept:** Indentation is the enemy of simplicity. Deep nesting hides bugs.

**Rule:** Handle edge cases, nulls, and errors at the very top of functions.

**Practice:**
```typescript
// ✅ GOOD: Guard clause
if (!valid) return;
doWork();

// ❌ BAD: Nested
if (valid) {
  doWork();
}
```

## Law 2: Make Illegal States Unrepresentable (Parse, Don't Validate)

**Concept:** Don't check data repeatedly; structure it so it can't be wrong.

**Rule:** Parse inputs at the boundary. Once data enters internal logic, it must be in a trusted, typed state.

**Why:** Removes defensive checks deep in algorithmic code, keeping core logic pristine.

```typescript
// ✅ GOOD: Parse at boundary, trusted internally
const user = parseUser(rawInput); // throws if invalid
processUser(user); // user is guaranteed valid

// ❌ BAD: Validate everywhere
function processUser(data: unknown) {
  if (!data.name) throw new Error("Name is required.");
  if (!data.email) throw new Error("Email is required.");
  // repeated everywhere
}
```

## Law 3: Atomic Predictability

**Concept:** A function must never surprise the caller.

**Rule:** Functions should be "Pure" where possible. Same Input = Same Output. No hidden mutations.

**Defense:** Avoid `void` functions that mutate global state. Return new data structures instead.

```typescript
// ✅ GOOD: Pure, predictable
function addItem(list: Item[], item: Item): Item[] {
  return [...list, item];
}

// ❌ BAD: Mutates, surprises caller
function addItem(list: Item[], item: Item): void {
  list.push(item); // mutates input!
}
```

## Law 4: Fail Fast, Fail Loud

**Concept:** Silent failures cause complexity later.

**Rule:** If a state is invalid, halt immediately with a descriptive error. Do not try to "patch" bad data.

**Result:** Keeps logic simple by never accounting for "half-broken" states.

```typescript
// ✅ GOOD: Fail immediately
if (!config.apiKey) {
  throw new Error("API key is required. Set OPENCODE_API_KEY environment variable.");
}

// ❌ BAD: Silent failure, undefined behavior
const apiKey = config.apiKey || ""; // empty string will cause issues
```

## Law 5: Intentional Naming

**Concept:** Comments are often a crutch for bad code.

**Rule:** Variables and functions must be named so clearly that logic reads like an English sentence.

**Defense:** `isUserEligible` is better than `check()`. The name itself guarantees the boolean logic.

## Adherence Checklist
Before completing your task, verify:
- [ ] **Guard Clauses:** Are all edge cases handled at the top with early returns?
- [ ] **Parsed State:** Is data parsed into trusted types at the boundary?
- [ ] **Purity:** Are functions predictable and free of hidden mutations?
- [ ] **Fail Loud:** Do invalid states throw clear, descriptive errors?
- [ ] **Intentional Naming:** Are variable and function names clear and descriptive?