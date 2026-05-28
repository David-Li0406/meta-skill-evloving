---
name: typescript-and-javascript
description:
  Writes TypeScript and JavaScript code following best practices and style
  rules. Use when writing TS/JS code or reviewing code style.
---

# TypeScript/JavaScript Protocol

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

- Early returns over nested conditionals
- Named functions over arrows (except callbacks/one-liners)
- Strict equality: `===`, `!==` only
- `const` for non-mutated variables
- `async/await` over `.then()`
- Never use `any` — find specific types
- `import type` for type-only imports
- Always use curly braces for `if`
- Never barrel exports in index.ts (harms tree-shaking)
- Never write code in index.ts(x) — use specific names
- `satisfies never` in switch default for exhaustiveness
- `satisfies <Type>` over type casting for traceability

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
