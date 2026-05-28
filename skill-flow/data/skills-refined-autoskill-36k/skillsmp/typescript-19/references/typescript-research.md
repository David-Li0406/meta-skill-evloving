# typescript Research

Research document for the TypeScript language specialist skill. This skill helps developers write type-safe, maintainable TypeScript code.

## Phase 1: Upstream Survey

### VoltAgent typescript-pro Subagent

Source: [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-language-specialists/typescript-pro.md)

#### Identity
"Senior TypeScript developer with mastery of TypeScript 5.0+ and its ecosystem," specializing in advanced type systems, full-stack type safety, and modern build tooling.

#### Development Checklist
- [ ] Strict mode enabled with all compiler flags
- [ ] No unqualified `any` usage
- [ ] 100% type coverage for public APIs
- [ ] ESLint and Prettier configuration
- [ ] Test coverage exceeding 90%
- [ ] Proper source maps and declaration files
- [ ] Bundle size optimization

#### Specializations Covered

| Area | Topics |
|------|--------|
| Type Patterns | Conditional types, mapped types, template literals, discriminated unions, branded types, `satisfies` |
| Type System | Generics, `infer`, recursive types, type-level programming |
| Full-Stack | tRPC, GraphQL codegen, type-safe APIs, form validation |
| Build/Tooling | tsconfig, project references, path mapping, tree-shaking |
| Testing | Type-safe utilities, mocks, fixtures, property-based testing |
| Frameworks | React, Vue 3, Angular, Next.js, NestJS, Express |
| Performance | const enums, type-only imports, lazy evaluation |
| Error Handling | Result types, `never`, exhaustive checking |

#### Core Philosophy
"Type safety, developer experience, and build performance while maintaining code clarity and maintainability."

---

## Phase 2: Research Findings

### 1. Official TypeScript Style Guides

#### TypeScript Do's and Don'ts
Source: [typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)

**Don'ts:**
- Don't use `any` unless migrating from JavaScript
- Don't use `Object` — use `object` (non-primitive)
- Don't have generic types that don't use their type parameter
- Don't use `@ts-ignore` — fix the underlying issue

**Do's:**
- Use `unknown` when you don't know the type
- Use union types for nullable: `string | null`
- Use type guards for runtime checks

#### Google TypeScript Style Guide
Source: [google.github.io/styleguide/tsguide.html](https://google.github.io/styleguide/tsguide.html)

Key points:
- Return type annotations: optional, but reviewers may request for clarity
- `undefined` vs `null`: no preference, be consistent
- Don't decorate names with type info (no `strName`, `IInterface`)
- Avoid trailing/leading underscores for private members

#### TS.dev Style Guide
Source: [ts.dev/style](https://ts.dev/style/)

Key points:
- Don't use `@ts-ignore` — it masks real problems
- Type assertions (`as`) and non-null assertions (`!`) are unsafe
- Both only silence the compiler, no runtime checks

---

### 2. tsconfig.json Best Practices

Source: [typescriptlang.org/tsconfig](https://www.typescriptlang.org/tsconfig/)

#### Recommended Strict Configuration

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "isolatedModules": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true
  }
}
```

#### What `strict: true` Enables

| Flag | Effect |
|------|--------|
| `noImplicitAny` | Error on implicit `any` |
| `noImplicitThis` | Error on implicit `this` as `any` |
| `strictNullChecks` | `null`/`undefined` not assignable to other types |
| `strictFunctionTypes` | Correct variance checking for function params |
| `strictBindCallApply` | Strict checking of `bind`/`call`/`apply` |
| `strictPropertyInitialization` | Class properties must be initialized |
| `useUnknownInCatchVariables` | Catch variables typed as `unknown` |
| `alwaysStrict` | Emit `"use strict"` |

#### Additional Recommended Flags

```json
{
  "compilerOptions": {
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "exactOptionalPropertyTypes": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

---

### 3. ESLint with TypeScript

Source: [typescript-eslint.io](https://typescript-eslint.io/getting-started/)

#### Flat Config Setup (ESLint 9+)

```javascript
// eslint.config.mjs
// @ts-check
import eslint from '@eslint/js';
import { defineConfig } from 'eslint/config';
import tseslint from 'typescript-eslint';

export default defineConfig(
  eslint.configs.recommended,
  tseslint.configs.strictTypeChecked,
  tseslint.configs.stylisticTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
      },
    },
  },
  {
    files: ['**/*.js'],
    extends: [tseslint.configs.disableTypeChecked],
  },
);
```

#### Recommended Config Tiers

| Config | Description |
|--------|-------------|
| `recommended` | Baseline rules |
| `strict` | Stricter rules, more opinionated |
| `strictTypeChecked` | Type-aware strict rules |
| `stylistic` | Code style rules |
| `stylisticTypeChecked` | Type-aware style rules |

#### Key Rules to Enable

```javascript
{
  rules: {
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/no-non-null-assertion': 'warn',
    '@typescript-eslint/consistent-type-assertions': 'error',
    '@typescript-eslint/consistent-type-imports': 'error',
    '@typescript-eslint/no-floating-promises': 'error',
    '@typescript-eslint/no-misused-promises': 'error',
    '@typescript-eslint/await-thenable': 'error',
    '@typescript-eslint/require-await': 'error',
  }
}
```

---

### 4. Utility Types

Source: [typescriptlang.org/docs/handbook/utility-types](https://www.typescriptlang.org/docs/handbook/utility-types.html)

#### Built-in Utility Types

| Type | Purpose | Example |
|------|---------|---------|
| `Partial<T>` | All properties optional | `Partial<User>` for updates |
| `Required<T>` | All properties required | `Required<Config>` |
| `Readonly<T>` | All properties readonly | `Readonly<State>` |
| `Pick<T, K>` | Select specific keys | `Pick<User, 'id' \| 'name'>` |
| `Omit<T, K>` | Exclude specific keys | `Omit<User, 'password'>` |
| `Record<K, V>` | Dictionary type | `Record<string, User>` |
| `Exclude<T, U>` | Exclude types from union | `Exclude<Status, 'deleted'>` |
| `Extract<T, U>` | Extract types from union | `Extract<Event, MouseEvent>` |
| `NonNullable<T>` | Remove null/undefined | `NonNullable<string \| null>` |
| `ReturnType<F>` | Function return type | `ReturnType<typeof fn>` |
| `Parameters<F>` | Function parameter types | `Parameters<typeof fn>` |
| `Awaited<T>` | Unwrap Promise | `Awaited<Promise<User>>` |

#### Best Practices

```typescript
// Good: Named intermediate types
type UserUpdate = Partial<User>;
type PublicUser = Omit<User, 'password' | 'email'>;

// Avoid: Over-nested utilities
type Bad = Pick<Partial<Omit<User, 'id'>>, 'name'>;

// Good: Split into named types
type EditableUser = Omit<User, 'id'>;
type OptionalUser = Partial<EditableUser>;
type NameOnly = Pick<OptionalUser, 'name'>;
```

#### Cautions

- `Partial<T>` allows `{}` — don't use for object creation
- `Omit` on required fields is dangerous without replacement
- Don't overuse — sometimes explicit types are clearer

---

### 5. Common Mistakes

Sources: [dev.to/leapcell](https://dev.to/leapcell/top-16-typescript-mistakes-developers-make-and-how-to-fix-them-4p9a), [allthingstypescript.dev](https://www.allthingstypescript.dev/p/avoid-using-type-assertions-in-typescript)

#### The `any` Problem

```typescript
// Bad: any disables type checking
function process(data: any) {
  return data.foo.bar;  // No errors, crashes at runtime
}

// Good: use unknown + type guards
function process(data: unknown) {
  if (isValidData(data)) {
    return data.foo.bar;  // Type-safe
  }
  throw new Error('Invalid data');
}
```

#### Type Assertions Are Unsafe

```typescript
// Bad: assertion without validation
const user = response.data as User;

// Good: runtime validation
const user = validateUser(response.data);

// Bad: double assertion (very dangerous)
const num = value as unknown as number;

// Bad: non-null assertion without certainty
const element = document.getElementById('app')!;

// Good: explicit null check
const element = document.getElementById('app');
if (!element) throw new Error('Element not found');
```

#### Object Type Pitfalls

```typescript
// Bad: Object (capital O)
function process(obj: Object) {}

// Good: object (lowercase) or specific type
function process(obj: object) {}
function process(obj: Record<string, unknown>) {}

// Bad: {} allows primitives
function process(obj: {}) {}  // allows string, number, etc.

// Good: Record for object constraint
function process(obj: Record<string, unknown>) {}
```

#### Promise/Async Mistakes

```typescript
// Bad: floating promise (no await/catch)
async function save() {
  fetchData();  // Promise ignored!
}

// Good: handle the promise
async function save() {
  await fetchData();
}

// Bad: unnecessary async
async function getName(): Promise<string> {
  return 'John';  // No await needed
}

// Good: remove async if not needed
function getName(): string {
  return 'John';
}
```

#### Index Signature Access

```typescript
// Unsafe without noUncheckedIndexedAccess
const obj: Record<string, string> = {};
const value = obj['key'];  // string (but actually undefined!)

// Safe with noUncheckedIndexedAccess
const value = obj['key'];  // string | undefined
if (value !== undefined) {
  // now value is string
}
```

---

### 6. Type Patterns

#### Discriminated Unions

```typescript
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: Error };

function handle<T>(result: Result<T>) {
  if (result.success) {
    console.log(result.data);  // T
  } else {
    console.error(result.error);  // Error
  }
}
```

#### Type Guards

```typescript
// Type predicate
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

// In-operator narrowing
function process(value: Dog | Cat) {
  if ('bark' in value) {
    value.bark();  // Dog
  } else {
    value.meow();  // Cat
  }
}
```

#### Branded Types

```typescript
type UserId = string & { __brand: 'UserId' };
type OrderId = string & { __brand: 'OrderId' };

function createUserId(id: string): UserId {
  return id as UserId;
}

function getUser(id: UserId) {}

const userId = createUserId('123');
const orderId = '456' as OrderId;

getUser(userId);   // OK
getUser(orderId);  // Error: OrderId not assignable to UserId
```

#### Template Literal Types

```typescript
type EventName = `on${Capitalize<string>}`;

type CSSValue = `${number}${'px' | 'rem' | 'em' | '%'}`;

type Route = `/users/${string}` | `/posts/${string}`;
```

#### The `satisfies` Operator (TS 4.9+)

```typescript
// Without satisfies: loses literal types
const config: Record<string, string | number> = {
  port: 3000,
  host: 'localhost',
};
config.port;  // string | number

// With satisfies: keeps literal types
const config = {
  port: 3000,
  host: 'localhost',
} satisfies Record<string, string | number>;
config.port;  // number
```

---

## Audit Checklist Summary

### Critical (Must Have)
- [ ] `strict: true` in tsconfig.json
- [ ] No explicit `any` usage
- [ ] No `@ts-ignore` comments
- [ ] ESLint with typescript-eslint configured
- [ ] Type assertions minimized and justified

### Important (Should Have)
- [ ] `noUncheckedIndexedAccess` enabled
- [ ] Type-aware lint rules (`strictTypeChecked`)
- [ ] Consistent type imports (`import type`)
- [ ] Public API has explicit types
- [ ] Discriminated unions for state management
- [ ] Type guards instead of assertions

### Recommended (Nice to Have)
- [ ] Branded types for IDs
- [ ] `satisfies` for config objects
- [ ] Template literal types for string patterns
- [ ] Custom utility types documented
- [ ] Type tests for complex types
- [ ] 100% type coverage for public APIs

---

## Sources

### Official Documentation
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TypeScript Do's and Don'ts](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
- [TSConfig Reference](https://www.typescriptlang.org/tsconfig/)
- [Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)

### Style Guides
- [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
- [TS.dev Style Guide](https://ts.dev/style/)

### Tools
- [typescript-eslint](https://typescript-eslint.io/)
- [ESLint Flat Config](https://eslint.org/docs/latest/use/configure/configuration-files)

### Best Practices
- [Better Stack - TypeScript Strict Option](https://betterstack.com/community/guides/scaling-nodejs/typescript-strict-option/)
- [Better Stack - Utility Types](https://betterstack.com/community/guides/scaling-nodejs/ts-utility-types/)
- [All Things TypeScript - Avoid Type Assertions](https://www.allthingstypescript.dev/p/avoid-using-type-assertions-in-typescript)

### Upstream
- [VoltAgent typescript-pro](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-language-specialists/typescript-pro.md)
