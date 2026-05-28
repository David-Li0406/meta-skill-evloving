# TypeScript-Specific Rules

These rules apply when reviewing **TypeScript** (`.ts`, `.tsx`) and **JavaScript** (`.js`, `.jsx`) files.

---

## 1. Type Safety

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| No `any` | Warning | Use `unknown` or specific types instead |
| Strict mode | Warning | Enable `strict: true` in tsconfig |
| Explicit return types | Info | On exported/public functions |
| No type assertions | Warning | Avoid `as Type` unless necessary |
| Discriminated unions | Info | Prefer over optional properties for variants |
| Generics over any | Info | Use generics for reusable typed functions |

### Check For

```typescript
// BAD: any
function process(data: any) { ... }
const result: any = fetch();

// BAD: Unsafe assertion
const user = data as User; // Could be wrong!

// BAD: Non-null assertion abuse
const name = user!.name!.first!;

// GOOD: Type guard
function isUser(data: unknown): data is User {
  return typeof data === 'object' && data !== null && 'id' in data;
}

// GOOD: Generic
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}
```

### Red Flags

- `any` appears more than once in a file
- Disabled type checks: `// @ts-ignore`, `// @ts-nocheck`
- Type assertions (`as`) without corresponding validation
- `Object` or `{}` as types (too broad)

---

## 2. Nullability

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| Optional chaining | Info | Use `?.` instead of `&&` chains |
| Nullish coalescing | Info | Use `??` over `\|\|` for defaults |
| Strict null checks | Warning | Enable in tsconfig |
| Explicit null handling | Warning | Don't assume values exist |
| Optional vs undefined | Info | Use `?:` for optional, not `\| undefined` |

### Check For

```typescript
// BAD: Verbose null checking
if (user && user.address && user.address.city) { ... }

// GOOD: Optional chaining
if (user?.address?.city) { ... }

// BAD: || with falsy values
const count = input || 0; // Bug if input is 0!

// GOOD: Nullish coalescing
const count = input ?? 0; // Only null/undefined

// BAD: Assuming existence
const name = user.name; // Could throw!

// GOOD: Handle undefined
const name = user?.name ?? 'Anonymous';
```

### Red Flags

- Long `&&` chains for null checks
- `||` used for defaults on numbers or booleans
- Missing `?` on properties that could be undefined
- `!` (non-null assertion) used more than once per function

---

## 3. Async/Promises

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| No floating promises | Critical | Always await or handle promises |
| Error handling | Warning | Try/catch or .catch() on async ops |
| Async consistency | Info | Don't mix async/await with .then() |
| Parallel execution | Info | Use `Promise.all` for independent ops |
| Async in loops | Warning | Avoid `forEach` with async callbacks |

### Check For

```typescript
// BAD: Floating promise (no await, no catch)
saveUser(user);
fetchData();

// GOOD: Awaited
await saveUser(user);

// GOOD: Fire-and-forget with error handling
saveUser(user).catch(console.error);

// BAD: Sequential when parallel is possible
const user = await getUser();
const orders = await getOrders();

// GOOD: Parallel
const [user, orders] = await Promise.all([getUser(), getOrders()]);

// BAD: forEach with async (doesn't wait)
items.forEach(async (item) => {
  await processItem(item);
});

// GOOD: for...of or Promise.all
for (const item of items) {
  await processItem(item);
}
// OR
await Promise.all(items.map(processItem));
```

### Red Flags

- Calls to async functions without `await`
- Missing `.catch()` on promises not awaited
- `async` in `.forEach()`, `.map()`, `.filter()` without proper handling
- Nested `.then()` chains (use async/await instead)

---

## 4. Imports/Exports

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| Named exports | Info | Prefer over default exports |
| Barrel files | Warning | Use cautiously (can cause circular deps) |
| Import order | Info | Group: external, internal, relative |
| No circular imports | Warning | Causes runtime issues |
| Type-only imports | Info | Use `import type` for types |

### Check For

```typescript
// GOOD: Named export
export function validateUser() { ... }
export const USER_ROLES = { ... };

// CAUTION: Default export (harder to refactor)
export default class UserService { ... }

// GOOD: Type-only import
import type { User } from './types';
import { validateUser } from './validation';

// BAD: Circular dependency
// file-a.ts
import { b } from './file-b';
export const a = b + 1;

// file-b.ts
import { a } from './file-a';
export const b = a + 1; // undefined!
```

### Red Flags

- `index.ts` files re-exporting everything (barrel files)
- Import loops between files
- Mixing default and named exports in same file
- Importing from deeply nested paths (`../../../utils`)

---

## 5. React (if applicable)

Only apply these if reviewing React code (detected by `.tsx` files or React imports).

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| Key props | Warning | Unique keys in lists, not array index |
| Hooks rules | Critical | Only at top level, only in components/hooks |
| Dependency arrays | Warning | Include all dependencies in useEffect/useMemo |
| Memo appropriately | Info | Don't memo everything, only expensive renders |
| Component size | Warning | Split large components (>200 lines) |

### Check For

```tsx
// BAD: Index as key
{items.map((item, i) => <Item key={i} />)}

// GOOD: Stable unique key
{items.map(item => <Item key={item.id} />)}

// BAD: Conditional hook
if (condition) {
  const [state, setState] = useState(); // Never do this!
}

// BAD: Missing dependency
useEffect(() => {
  fetchUser(userId);
}, []); // Missing userId!

// GOOD: Complete dependencies
useEffect(() => {
  fetchUser(userId);
}, [userId]);

// BAD: Over-memoization
const SimpleComponent = memo(({ name }) => <span>{name}</span>);

// GOOD: Memo for expensive components
const ExpensiveList = memo(({ items }) => (
  items.map(item => <ComplexItem key={item.id} {...item} />)
));
```

### Red Flags

- `key={index}` in map
- Hooks called conditionally or in loops
- Empty dependency arrays when dependencies exist
- `useMemo`/`useCallback` on simple values
- State updates in render (infinite loops)
- Missing cleanup in useEffect

---

## 6. Common Patterns

### Prefer

```typescript
// Object shorthand
const user = { name, email }; // not { name: name, email: email }

// Destructuring
const { id, name } = user; // not const id = user.id;

// Template literals
`Hello ${name}`; // not "Hello " + name

// Spread for immutability
const updated = { ...user, name: 'New' }; // not user.name = 'New'

// Array methods over loops
users.filter(u => u.active).map(u => u.name);
```

### Avoid

```typescript
// var (use const/let)
var x = 1;

// == (use ===)
if (x == null) // Unless intentionally checking null/undefined

// arguments object (use rest params)
function sum() { return [...arguments].reduce(...) }
// Use: function sum(...nums) { return nums.reduce(...) }

// Function constructor
new Function('a', 'return a');

// with statement
with (obj) { ... }
```

---

## Summary Checklist

Before completing TypeScript review:

- [ ] No `any` types (or justified exceptions)
- [ ] Strict null checks handled (optional chaining, nullish coalescing)
- [ ] All promises are awaited or have error handling
- [ ] No floating promises
- [ ] Imports are organized and no circular dependencies
- [ ] React hooks follow rules (if applicable)
- [ ] Keys are unique and stable (if applicable)
- [ ] Modern syntax used (const/let, template literals, destructuring)
