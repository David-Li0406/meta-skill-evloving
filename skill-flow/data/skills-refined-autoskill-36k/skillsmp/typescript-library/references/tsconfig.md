# TypeScript Configuration for Libraries

## Recommended tsconfig.json

```json
{
  "compilerOptions": {
    // Output
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",

    // Declarations
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,

    // Strictness
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,

    // Interop
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "verbatimModuleSyntax": true,

    // Performance
    "skipLibCheck": true,
    "incremental": true
  },
  "include": ["src"],
  "exclude": ["**/*.test.ts", "**/*.spec.ts"]
}
```

## Key Options Explained

### Module System

| Option | Description |
|--------|-------------|
| `module: "NodeNext"` | Modern Node.js ESM + CJS support |
| `moduleResolution: "NodeNext"` | Package.json exports resolution |
| `verbatimModuleSyntax: true` | Explicit import/export type syntax |

### Output

| Option | Description |
|--------|-------------|
| `declaration: true` | Generate .d.ts files |
| `declarationMap: true` | Enable go-to-definition in source |
| `sourceMap: true` | Enable debugging |
| `outDir: "dist"` | Output directory |

### Strictness (Recommended)

```json
{
  "strict": true,
  "noUncheckedIndexedAccess": true,
  "noImplicitOverride": true,
  "noPropertyAccessFromIndexSignature": true,
  "exactOptionalPropertyTypes": true
}
```

## ESM-Only Library

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "declaration": true,
    "declarationMap": true,
    "outDir": "dist"
  }
}
```

## Dual CJS/ESM Library

Use tsup or unbuild instead of tsc directly:

```typescript
// tsup.config.ts
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['cjs', 'esm'],
  dts: true,
  splitting: false,
  sourcemap: true,
  clean: true
});
```

## Path Aliases

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

Note: Path aliases need bundler support (tsup, esbuild) for runtime.

## Composite Projects (Monorepo)

```json
// packages/core/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "references": [
    { "path": "../utils" }
  ]
}
```

## Build-Only Config

```json
// tsconfig.build.json
{
  "extends": "./tsconfig.json",
  "exclude": [
    "**/*.test.ts",
    "**/*.spec.ts",
    "test/**",
    "**/__tests__/**"
  ]
}
```

Use: `tsc -p tsconfig.build.json`

## Common Issues

### "Cannot find module" for .js imports

With NodeNext, use `.js` extensions in imports even for `.ts` files:

```typescript
import { foo } from './utils.js';  // Correct
import { foo } from './utils';     // Error
```

### Type-only imports

With `verbatimModuleSyntax`:

```typescript
import type { User } from './types.js';  // Correct
import { type User } from './types.js';  // Also correct
import { User } from './types.js';       // Error if User is type-only
```
