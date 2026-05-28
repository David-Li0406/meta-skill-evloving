# General Clean Code Principles (TypeScript 5.5+)

## Core Principles

### 1. Single Responsibility

- Each function/component does ONE thing
- If you need "and" to describe it, split it
- Functions < 20 lines, components < 150 lines

### 2. DRY (Don't Repeat Yourself)

- Extract repeated code into functions/hooks
- BUT don't over-abstract prematurely
- Rule of 3: abstract on the third repetition

### 3. KISS (Keep It Simple)

- Prefer simple solutions over clever ones
- Readable > Concise
- Future you will thank present you

### 4. Remove Dead Code

- Delete unused code and commented-out blocks
- No backward compatibility unless explicitly instructed

---

## Naming Conventions

### Variables & Functions

```typescript
// BAD
const d = new Date();
const fn = (x) => x * 2;

// GOOD
const currentDate = new Date();
const doubleValue = (value: number) => value * 2;
```

| Type             | Convention    | Example                       |
| ---------------- | ------------- | ----------------------------- |
| Variables        | camelCase     | `userName`, `isLoading`       |
| Collections      | Plural names  | `users`, `items`              |
| Components/Types | PascalCase    | `UserCard`, `UserCardProps`   |
| Functions        | Verbs         | `fetchData`, `getUserById`    |
| Booleans         | is/has/should | `isLoading`, `hasAccess`      |
| Constants        | UPPER_SNAKE   | `API_BASE_URL`, `MAX_RETRIES` |
| Config Objects   | camelCase     | `appConfig`, `queryConfig`    |

### File & Folder Organization

- **Folders**: kebab-case (`user-profile/`, `auth-utils/`)
- **Components**: By use case (`components/actions/`, `components/cards/`)
- **Features**: By domain (`features/auth/`, `features/dashboard/`)
- **Shared Code**: In lib/ folders (`lib/services/`, `lib/types/`, `lib/utils/`)
- **Tests**: In `__tests__` folders adjacent to code

---

## Code Organization

- **Cognitive Complexity**: Keep functions focused and under reasonable limits
- **Boolean Extraction**: Extract complex conditions into well-named variables
- **Early Returns**: Use early returns to reduce nesting
- **Simple Conditionals**: Prefer simple conditionals over nested ternaries
- **Separation of Concerns**: Group related code together

---

## TypeScript 5.5+ Patterns

### Inferred Type Predicates (5.5+)

TypeScript 5.5 automatically infers type predicates - no more manual type guards!

```typescript
// OLD (before 5.5) - Manual type guard
function isDefined<T>(value: T | undefined | null): value is T {
  return value !== undefined && value !== null;
}

// NEW (5.5+) - Automatic inference
const isDefined = <T>(value: T | null | undefined) =>
  value !== null && value !== undefined;

// Both work in filter chains
const results = [1, null, 2, undefined, 3].filter(isDefined);
// Type: number[]
```

### Const Type Parameters

Preserve literal types with `const` type parameters:

```typescript
function createConfig<const T>(config: T): T {
  return config;
}

const config = createConfig({
  mode: "development", // Type: 'development' (not string)
  port: 3000, // Type: 3000 (not number)
});
```

### Satisfies Operator

Validate types without widening:

```typescript
type Config = {
  endpoint: string;
  timeout: number;
};

// Validates against Config but keeps precise types
const config = {
  endpoint: "https://api.example.com",
  timeout: 5000,
} satisfies Config;

config.endpoint; // Type: 'https://api.example.com' (not string)
```

### Satisfies + As Const (Maximum Safety)

```typescript
const routes = {
  home: "/",
  about: "/about",
} as const satisfies Record<string, `/${string}`>;

// All routes must start with '/'
// Types are readonly and literal
```

---

## Branded Types for Safety

Prevent accidental mixing of primitives:

```typescript
declare const __brand: unique symbol;
type Brand<T, TBrand> = T & { [__brand]: TBrand };

type UserId = Brand<string, "UserId">;
type ProductId = Brand<string, "ProductId">;

function createUserId(id: string): UserId {
  if (!/^user_[a-z0-9]+$/.test(id)) {
    throw new Error("Invalid user ID");
  }
  return id as UserId;
}

function getUser(id: UserId) {
  /* ... */
}

const userId = createUserId("user_123");
const productId = "prod_456" as ProductId;

getUser(userId); // ✅
getUser(productId); // ❌ Type error!
```

---

## No `any` - Use Alternatives

### Use `unknown` Instead

```typescript
// ❌ BAD
function process(data: any) {
  return data.value;
}

// ✅ GOOD
function process(data: unknown) {
  if (typeof data === "object" && data !== null && "value" in data) {
    return (data as { value: unknown }).value;
  }
  throw new Error("Invalid data");
}
```

### Use Generics

```typescript
// ❌ BAD
function identity(value: any): any {
  return value;
}

// ✅ GOOD
function identity<T>(value: T): T {
  return value;
}
```

### Use Discriminated Unions

```typescript
type AsyncState<T> =
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function handleState<T>(state: AsyncState<T>) {
  switch (state.status) {
    case "loading":
      return "Loading...";
    case "success":
      return state.data; // ✅ Type-safe
    case "error":
      return state.error.message;
    default:
      const _exhaustive: never = state;
      return _exhaustive;
  }
}
```

---

## Utility Types Best Practices

| Type            | Use Case                     |
| --------------- | ---------------------------- |
| `Partial<T>`    | Update/patch operations      |
| `Required<T>`   | Enforce all properties       |
| `Pick<T, K>`    | Create subset types (DTOs)   |
| `Omit<T, K>`    | Remove sensitive fields      |
| `Record<K, T>`  | Type-safe dictionaries       |
| `Readonly<T>`   | Immutable types              |
| `ReturnType<T>` | Extract function return type |

```typescript
// Update payload - only changed fields
type UserUpdate = Partial<Pick<User, "name" | "email">>;

// Public API response - no password
type PublicUser = Omit<User, "password" | "createdAt">;

// Permission map - all roles required
type Permissions = Record<"admin" | "user" | "guest", string[]>;
```

---

## Template Literal Types

Type-safe string patterns:

```typescript
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type Endpoint = `/${string}`;
type ApiRoute = `${HttpMethod} ${Endpoint}`;

const route: ApiRoute = "GET /users"; // ✅
const invalid: ApiRoute = "PATCH /users"; // ❌

// CSS values
type CSSUnit = "px" | "rem" | "em" | "%";
type CSSValue = `${number}${CSSUnit}`;

const margin: CSSValue = "10px"; // ✅
```

---

## Error Handling

### Typed Errors

```typescript
class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
  ) {
    super(message);
    this.name = "AppError";
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, "NOT_FOUND", 404);
  }
}
```

### Result Type Pattern

```typescript
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };

function parseJSON<T>(json: string): Result<T> {
  try {
    return { ok: true, value: JSON.parse(json) };
  } catch (e) {
    return { ok: false, error: e as Error };
  }
}

const result = parseJSON<User>(data);
if (result.ok) {
  console.log(result.value); // ✅ Type: User
} else {
  console.error(result.error); // ✅ Type: Error
}
```

---

## File Organization

### One Component Per File

```
components/
  Button/
    Button.tsx
    Button.test.tsx
    index.ts
```

### Feature-Based Structure

```
features/
  auth/
    components/
    hooks/
    utils/
    types.ts
```

### Import Order

```typescript
// 1. External libraries
import { useState } from "react";

// 2. Internal absolute imports
import { Button } from "@/components/Button";

// 3. Relative imports
import { formatDate } from "./utils";

// 4. Types (last)
import type { User } from "@/types";
```

---

## tsconfig.json Recommendations

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

---

## Anti-Patterns to Avoid

| Pattern        | Why It's Bad        | Fix                     |
| -------------- | ------------------- | ----------------------- |
| `any` type     | No type safety      | Use `unknown`, generics |
| Magic numbers  | Hard to understand  | Named constants         |
| Deep nesting   | Hard to read        | Early returns           |
| Long functions | Hard to test        | Split into smaller      |
| Commented code | Clutters codebase   | Delete it               |
| `console.log`  | Noise in production | Proper logging          |

---

## Code Commenting

- **Self-Documenting**: Clear structure and naming
- **Minimal Comments**: Concise, explain large sections only
- **Explain "Why"**: Capture intent, rationale, trade-offs; avoid restating obvious
- **No Temporary Comments**: Avoid comments about recent changes; keep evergreen
- **TSDoc for Public APIs**: Document all public API functions with TSDoc (include simple example)

---

## Error Handling

### Principles

- **Fail Fast**: Validate input early; fail with clear messages
- **Early Returns**: Prefer early returns over nested conditionals for error cases
- **Specific Types**: Use specific exception/error types for targeted handling
- **Centralized**: Handle at boundaries (controllers, API layers), not scattered try-catch
- **Clean Up**: Always clean resources in finally blocks
- **Type-Safe**: Throw `Error` objects with descriptive messages, not strings
- **Meaningful Try-Catch**: Don't catch errors just to rethrow them

### Typed Errors Pattern

```typescript
class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
  ) {
    super(message);
    this.name = "AppError";
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, "NOT_FOUND", 404);
  }
}
```

### User Experience

- **User-Friendly**: Clear, actionable messages without technical details
- **Preserve State**: Keep form data and page state on error
- **Recovery**: Provide next steps (retry, back, help) and suggest corrections
- **i18n**: Localize messages; keep concise
- **Graceful Degradation**: Show fallback UI when dependencies fail

### Resilience

- **Retry**: Exponential backoff for transient failures
- **Offline**: Queue or no-op non-critical actions (mobile)
- **Domain Errors**: Wrap low-level errors; never leak internals to clients
- **Monitoring**: Capture exceptions with safe context; redact sensitive data

### Debugging

- **No Debug Statements**: Remove `console.log`, `debugger`, and `alert` from production

---

## Validation

- **Server-Side**: Always validate on server; never trust client-side alone
- **Client-Side for UX**: Immediate feedback, but duplicate server-side
- **Fail Early**: Validate and reject invalid data before processing
- **Specific Messages**: Clear, field-specific error messages
- **Allowlists**: Define what is allowed over blocking what's not
- **Type & Format**: Check data types, formats, ranges, required fields
- **Sanitize**: Prevent injection attacks (SQL, XSS, command injection)
- **Business Rules**: Validate at appropriate application layer
- **Consistency**: Apply across all entry points (forms, APIs, jobs)

---

## Modern JavaScript

- **Arrow Functions**: Use for callbacks and short functions
- **For...of Loops**: Prefer over `.forEach()` and indexed `for` loops
- **Safe Access**: Use optional chaining (`?.`) and nullish coalescing (`??`)
- **Template Literals**: Prefer over string concatenation
- **Destructuring**: Use for object and array assignments
- **Variable Declarations**: Use `const` by default, `let` only when reassignment is needed, never `var`

---

## Async & Promises

- **Await Promises**: Always `await` promises in async functions
- **Async/Await**: Use instead of promise chains for better readability
- **Error Handling**: Handle errors appropriately with try-catch blocks
- **Promise Executors**: Don't use async functions as Promise executors

---

## Null & Undefined

- **Avoid in Returns**: Don't return `null` or `undefined`
- **Optional Properties**: Use `?:` instead of union with `undefined`
- **Optional Chaining**: Prefer `?.` and `??`

---

## Exports & Imports

- **Named Exports**: Use only (except Expo screens and Next.js App Router)
- **Import Separation**: Keep `import type` separated
- **String Literal Unions**: Prefer over enums

### Import Order

```typescript
// 1. External libraries
import { useState } from "react";

// 2. Internal absolute imports
import { Button } from "@/components/Button";

// 3. Relative imports
import { formatDate } from "./utils";

// 4. Types (last)
import type { User } from "@/types";
```

---

## Development Conventions

- **Project Structure**: Predictable, logical organization
- **Documentation**: Up-to-date README with setup, architecture, contribution guidelines
- **Dependencies**: Keep up-to-date and minimal; document major ones
- **Version Control**: Clear commit messages, feature branches, meaningful PR descriptions
- **Feature Flags**: Use for incomplete features over long-lived branches
- **Changelog**: Track significant changes and improvements
- **Environment**: Use env variables; never commit secrets or API keys
- **Code Review**: Consistent process with clear expectations
- **Testing**: Define required level before merging (unit, integration, e2e)
