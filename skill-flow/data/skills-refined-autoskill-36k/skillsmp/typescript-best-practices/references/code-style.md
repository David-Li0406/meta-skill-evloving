# Code Style Patterns

## Safe Array Access

With `noUncheckedIndexedAccess` enabled, array index access returns `T | undefined`. Handle this properly:

```typescript
const items: Array<string> = ['a', 'b', 'c'];

// DON'T: Index access without null check
for (let i = 0; i < items.length; i++) {
  console.log(items[i].toUpperCase()); // Error: items[i] is string | undefined
}

// DON'T: Non-null assertion to bypass check
for (let i = 0; i < items.length; i++) {
  console.log(items[i]!.toUpperCase()); // Dangerous: suppresses real errors
}

// DO: Explicit undefined check
for (let i = 0; i < items.length; i++) {
  const item = items[i];
  if (item === undefined) continue;
  console.log(item.toUpperCase()); // item is narrowed to string
}

// DO: Use for-of when index is not needed
for (const item of items) {
  console.log(item.toUpperCase()); // item is string, no undefined
}

// DO: Use forEach or map
items.forEach((item) => {
  console.log(item.toUpperCase());
});
```

**Prefer iteration methods over index access** — `for-of`, `forEach`, `map`, `filter` all provide properly typed values without the `undefined` concern.

## Early Return Pattern

Use guard clauses to handle edge cases first, keeping the main logic un-nested:

```typescript
// DO: Guard clauses with early return
function processUser(user: User | null) {
  if (user === null) return;
  if (!user.isActive) return;
  if (user.role !== 'admin') return;

  // Main logic here, un-nested
  performAdminAction(user);
}

// DON'T: Deeply nested conditions
function processUserBad(user: User | null) {
  if (user !== null) {
    if (user.isActive) {
      if (user.role === 'admin') {
        performAdminAction(user);
      }
    }
  }
}
```

**Ternary for simple branching** — useful but avoid deep nesting:

```typescript
// DO: Ternary with simple conditions first
function getMessage(status: Status) {
  return status === 'loading' ? 'Please wait...' :
         status === 'error' ? 'Something went wrong' :
         status === 'success' ? 'Done!' :
         'Unknown status';
}

// DO: Early return ternary — simple cases first, complex last
function processRequest(request: Request) {
  return !request.isValid ? { error: 'Invalid request' } :
         request.isCached ? getCachedResponse(request) :
         executeFullRequest(request);
}

// DON'T: Overly complex nested ternary
const result = a ? (b ? (c ? x : y) : z) : (d ? w : v);
```

**Guidelines:**
- Simple/quick-exit conditions first
- Complex logic last (or extract to separate function)
- If ternary becomes hard to read, use `if` statements instead

## Avoid Destructuring

Prefer direct property access over destructuring. Benefits:
- **Readability** — Clear which object a property belongs to
- **No name conflicts** — No need for renaming (`{ data: userData }`)
- **Type narrowing works** — Discriminated unions narrow correctly

```typescript
// DO: Direct property access
const query = useQuery();

if (query.isLoading) {
  return <Spinner />;
}
if (query.isSuccess) {
  // Type narrowing works!
  return <div>{query.data.name}</div>; // data is TData
}
if (query.isError) {
  return <Error message={query.error.message} />;
}

// DON'T: Destructuring breaks type narrowing
const { isLoading, isSuccess, isError, data, error } = useQuery();

if (isLoading) {
  return <Spinner />;
}
if (isSuccess) {
  // Type narrowing doesn't work!
  return <div>{data?.name}</div>; // data is still TData | undefined
}
```

**Why destructuring breaks narrowing:**

When you destructure, each variable becomes independent. Checking `isSuccess` doesn't narrow `data` because TypeScript doesn't track the relationship between separate variables.

## Avoid enum

TypeScript `enum` generates runtime code that can't be stripped by type-only transpilers (esbuild, swc in strip-only mode). Use const arrays instead:

```typescript
// DON'T: enum generates runtime code
enum State {
  Loading = 'loading',
  Success = 'success',
  Error = 'error',
}

// DO: const array + derived type
const states = ['loading', 'success', 'error'] as const;
type State = (typeof states)[number];  // 'loading' | 'success' | 'error'

// Runtime access still works
states.forEach((s) => console.log(s));
```

### With Zod

```typescript
import { z } from 'zod';

const states = ['loading', 'success', 'error'] as const;
const StateSchema = z.enum(states);
type State = z.infer<typeof StateSchema>;

// Runtime validation
const state = StateSchema.parse('loading');  // OK
StateSchema.parse('invalid');                // Throws ZodError

// DO: Use safeParse to replace includes
function isValidState(value: string): value is State {
  return StateSchema.safeParse(value).success;
}

// DON'T: Array.includes has type issues
// states.includes(unknownString);  // Error
```

**Why avoid enum:**
- `enum` is TypeScript-only syntax that emits runtime JavaScript
- Type-stripping tools (esbuild, swc) can't handle it without full TypeScript compilation
- Const arrays are pure JavaScript + types, fully strippable
- Union types provide the same type safety with better tree-shaking
