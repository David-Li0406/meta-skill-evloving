---
name: typescript-dev
description: Use this skill when writing TypeScript code that requires strict type safety, eliminating `any` types, and implementing runtime validation patterns with Zod.
---

# TypeScript Development

Type-safe code = compile-time errors = runtime confidence.

<when_to_use>

- Writing new TypeScript code
- Eliminating `any` types
- Using modern TypeScript 5.5+ features
- Validating API inputs/outputs with Zod
- Implementing Result types and discriminated unions
- Creating branded types for domain concepts

NOT for: runtime-only logic unrelated to types, non-TypeScript projects

</when_to_use>

<config>

**tsconfig.json** strict settings:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitReturns": true,
    "forceConsistentCasingInFileNames": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "skipLibCheck": false
  }
}
```

**Version requirements**: TS 5.2+ (`using`), TS 5.4+ (`NoInfer`), TS 5.5+ (inferred predicates)

</config>

## Core Patterns

<eliminating_any>

`any` defeats the type system. Use `unknown` + guards.

```typescript
// ❌ NEVER
function process(data: any) { return data.value; }

// ✅ ALWAYS
function process(data: unknown): string {
  if (!hasValue(data)) throw new TypeError('Invalid');
  return data.value.toString();
}

function hasValue(v: unknown): v is { value: unknown } {
  return typeof v === 'object' && v !== null && 'value' in v;
}
```

Validate at boundaries:

```typescript
async function fetchUser(id: string): Promise<User> {
  const data: unknown = await fetch(`/api/users/${id}`).then(r => r.json());
  return UserSchema.parse(data);
}
```

</eliminating_any>

<result_types>

Exceptions hide errors from types. Result makes them explicit.

```typescript
type Result<T, E = Error> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly error: E };

type UserError =
  | { readonly type: 'not-found'; readonly id: string }
  | { readonly type: 'network'; readonly message: string };

async function getUser(id: string): Promise<Result<User, UserError>> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (response.status === 404)
      return { ok: false, error: { type: 'not-found', id } };
    const data: unknown = await response.json();
    return { ok: true, value: UserSchema.parse(data) };
  } catch (error) {
    return { ok: false, error: { type: 'network', message: error.message } };
  }
}
```

</result_types>