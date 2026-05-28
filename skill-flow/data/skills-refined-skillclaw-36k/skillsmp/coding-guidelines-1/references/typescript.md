# TypeScript/JavaScript Patterns

Patterns and conventions for TypeScript and JavaScript projects.

## General Principles

- **Simplicity**: Straightforward solutions. No unnecessary intermediate variables—directly invoke/access if used once
- **Functional**: Pure functions, immutability, no classes/mutations
- **No duplication**: Extract to reusable helpers
- **Dependencies**: Check existing before adding new. Prefer well-maintained. Document rationale for major ones

## TypeScript Practices

### Strict Typing
Never use `any`—use `unknown` instead. Prefer `type` over `interface`. Infer when obvious.

```ts
// Prefer type
type User = { id: string; name: string };

// Derive from function returns
type Result = Awaited<ReturnType<typeof fetchUser>>;

// Type predicates for filters
items.filter((item): item is NonNullable<typeof item> => item !== null);
```

### Type Assertions
Prefer `satisfies` over `as`:

```ts
// Preferred
const config = { timeout: 5000 } satisfies Config;

// Avoid
const config = { timeout: 5000 } as Config;
```

### Variables
Prefer `const`. Use `let` only for: lazy init singletons, error cleanup, loop counters, complex state.

Prefer `undefined` over `null` for absent values.

### Inline Constants
Inline strings/numbers used 2-3 times in one module. Extract only when cross-module, complex, or likely to change.

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Types/Interfaces | PascalCase | `OrderEvent`, `UserConfig` |
| Functions/Variables | camelCase | `processOrder`, `maxRetries` |
| Files | Named as default export | `processOrder.ts` |
| Test files | Mirror source | `tests/processOrder.test.ts` |

**Descriptive names**: Full names, not abbreviations. Exceptions: `i` (index), `error` (catch), single-letter generics (`T`, `K`, `V`).

## Imports & Exports

### Import Paths
- `@/` for src/
- `@@/` for package root
- `./` for same directory only

### Export Patterns
Exports always at end of file. Use inline `type` keyword:

```ts
// At EOF
export { processOrder, type OrderResult };
export default processOrder;
```

**Default exports preferred**: Nearly every file has a default export named as the file. Named exports only for types or constants alongside default.

## Functions & Control Flow

### Arrow Functions with Implicit Returns

```ts
// Preferred
const double = (n: number) => n * 2;
const getUser = async (id: string) => fetchUser(id);

// Avoid
function double(n: number) { return n * 2; }
```

### Direct Callback References
Pass references directly if signatures match:

```ts
// Preferred
process.on("SIGINT", shutdown);
items.map(transform);

// Avoid
process.on("SIGINT", () => shutdown());
items.map((item) => transform(item));
```

### Functional Iteration
Prefer `map`, `filter`, `reduce` over `for`, `while`:

```ts
// Preferred
const names = users.map(u => u.name);
const active = users.filter(u => u.isActive);

// Avoid
const names = [];
for (const u of users) { names.push(u.name); }
```

### Wrapper Functions
Don't create functions called once at startup—execute at module scope. Don't wrap array functions—use single-item arrays.

### Conditionals
Combine related conditions, reduce nesting. Single-line for simple cases:

```ts
// Preferred
if (!user || !user.isActive) return;

// Avoid
if (!user) {
  return;
} else if (!user.isActive) {
  return;
}
```

## Object Patterns

### Property Ordering
Alphabetical by default. For mixed objects: primitives first, then nested (both alphabetically):

```ts
const config = {
  enabled: true,
  name: "app",
  timeout: 5000,
  nested: { ... },
  options: { ... },
};
```

### Dynamic Spread First
Spread dynamic properties first, explicit properties last (explicit overrides):

```ts
const user = { ...defaults, ...overrides, id: 123 };
```

### Method Chaining
Chain directly unless intermediate step needed for clarity:

```ts
// Preferred
const result = items.filter(isValid).map(transform).join(", ");

// Only break if complex
const filtered = items.filter(complexPredicate);
const result = filtered.map(transform);
```

### String Building
Use array join for conditional concatenation:

```ts
// Preferred
const path = [base, segment, file].filter(Boolean).join("/");

// Avoid
let path = base;
if (segment) path += "/" + segment;
path += "/" + file;
```

### Redundant Variables
Don't create multiple variables holding the same value.

## Comments

- **When**: Explain "why" not "what"—business logic, workarounds, non-obvious decisions
- **Avoid**: Never restate code. If self-explanatory, no comment needed
- **TODOs**: `// TODO:` with context (optional ticket ref)

## Error Handling

- Graceful failures with structured logging
- Include context: what failed, why, expected behavior
- Structured JSON via custom logger

```ts
logger.error("Order processing failed", {
  orderId,
  reason: error.message,
  expected: "valid order payload",
});
```

## Config & Environment

- Env vars only, no secrets in code
- Always update: `.env`, `.env.example`, `src/env.ts`
- Never access `process.env` directly—import from `src/env.ts`

```ts
// src/env.ts
import { z } from "zod";

const envSchema = z.object({
  DATABASE_URL: z.string(),
  API_KEY: z.string(),
});

export default envSchema.parse(process.env);
```
