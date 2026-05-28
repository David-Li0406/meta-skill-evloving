---
name: typescript-javascript-development
description: Use this skill when writing or reviewing TypeScript and JavaScript code to ensure adherence to best practices and coding standards.
---

# TypeScript/JavaScript Development Skill

## Type Checking

When iterating solutions (not reviewing), run type check:

```bash
pnpm tsc --noEmit
# monorepo: cd apps/demo-app && pnpm tsc --noEmit
```

## Code Block Types

- Pure TypeScript: `ts`
- TypeScript with JSX: `tsx`

## Style Rules

- Prefer early returns over nested conditionals.
- Use named functions over arrow functions (except for callbacks/one-liners).
- Use strict equality: `===`, `!==` only.
- Use `const` for non-mutated variables.
- Prefer `async/await` over `.then()`.
- Avoid using `any` — find specific types.
- Use `import type` for type-only imports.
- Always use curly braces for `if` statements.
- Avoid barrel exports in `index.ts` to maintain tree-shaking.
- Do not write code in `index.ts(x)` — use specific names.
- Use `satisfies never` in switch default for exhaustiveness.
- Prefer `satisfies <Type>` over type casting for traceability.

## Examples

```ts
// ✓ Early return
function process(data: Data | null) {
  if (!data) {
    return;
  }
  // process
}

// ✗ Nested
function process(data: Data | null) {
  if (data) {
    // process
  }
}
```

```ts
// ✓ Named function
function add(a: number, b: number): number {
  return a + b;
}

// ✓ One-liner arrow acceptable
const add = (a: number, b: number): number => a + b;

// ✗ Multi-line arrow
const add = (a: number, b: number): number => {
  return a + b;
};
```

```ts
// ✓ Type imports
import type { MyType } from './types';
import { type ReactNode } from 'react';
```

```ts
// ✓ Exhaustiveness + satisfies
function factory(target: 'a' | 'b'): A | B | null {
  switch (target) {
    case 'a':
      return new A();
    case 'b':
      return new B();
    default:
      target satisfies never;
      return null;
  }
}

// ✓ satisfies for traceability
const obj = { key: 'value' } satisfies Record<string, string>;

// ✗ Type casting loses inference
const obj: Record<string, string> = { key: 'value' };
```

```ts
// ✓ Always curly braces
if (!condition) {
  return;
}

// ✗ No braces
if (!condition) return;
```