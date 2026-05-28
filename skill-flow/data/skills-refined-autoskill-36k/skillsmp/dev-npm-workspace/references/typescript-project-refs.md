# TypeScript Project References for Workspaces

## Overview

TypeScript project references enable treating each workspace package as a separate TypeScript project while maintaining type awareness across the monorepo. This enables incremental builds and proper dependency tracking.

## Core Concepts

### Composite Projects

Each workspace package is a "composite" TypeScript project:

```json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

**Requirements for composite:**

- Must have `composite: true`
- Must have `declaration: true`
- Must include all source files via `include` or `files`

### Build Mode (`-b` or `--build`)

TypeScript's build mode understands project references:

```bash
# Build all referenced projects in correct order
tsc -b .

# Using tsgo (faster native TypeScript)
tsgo -b .

# Watch mode
tsc -b . --watch
```

## Configuration Structure

### Root tsconfig.json

```json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true,
    "incremental": true,
    "target": "esnext",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "paths": {
      "@scope/*": ["./src/packages/*/src"]
    }
  },
  "include": ["src/index.ts"]
}
```

### Package tsconfig.json

```json
{
  "extends": "../../../tsconfig.json",
  "compilerOptions": {
    "module": "esnext",
    "moduleResolution": "bundler",
    "outDir": "./dist",
    "rootDir": ".",
    "composite": true,
    "verbatimModuleSyntax": true,
    "paths": {}
  },
  "include": ["src/**/*", "test/**/*"]
}
```

### Package tsconfig.build.json

Separate config for production builds:

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "rootDir": "src",
    "outDir": "dist",
    "emitDeclarationOnly": false,
    "noEmit": false
  },
  "include": ["src/**/*"],
  "exclude": ["test/**/*", "**/*.test.ts"]
}
```

## Why Two tsconfig Files?

### tsconfig.json (Development)

- Includes tests (`test/**/*`)
- Includes test files (`**/*.test.ts`)
- Used by IDE for type checking
- `rootDir: "."` includes all source

### tsconfig.build.json (Production)

- Excludes tests
- Only builds `src/**/*`
- `rootDir: "src"` for clean output structure
- Used by build scripts

```bash
# Production build
tsgo -p tsconfig.build.json

# Development type check
tsc --noEmit
```

## Reference Configuration

### Strict TypeScript Settings

```json
{
  "compilerOptions": {
    // Strictness
    "strict": true,
    "noImplicitAny": true,
    "noImplicitThis": true,
    "noImplicitReturns": true,
    "noImplicitOverride": true,
    "strictBuiltinIteratorReturn": true,
    "useUnknownInCatchVariables": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    "noUncheckedIndexedAccess": true,
    "noUncheckedSideEffectImports": true,

    // Quality
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,

    // ESM
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "verbatimModuleSyntax": true,
    "resolveJsonModule": true,
    "resolvePackageJsonExports": true,
    "resolvePackageJsonImports": true,

    // Output
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "composite": true,
    "incremental": true,

    // Performance
    "assumeChangesOnlyAffectDirectDependencies": true
  }
}
```

### Path Mapping

Root config defines path aliases:

```json
{
  "compilerOptions": {
    "paths": {
      "*": ["./*"],
      "@scope/*": ["./src/packages/*/src"]
    }
  }
}
```

Package configs clear path mappings (use package.json exports instead):

```json
{
  "compilerOptions": {
    "paths": {}
  }
}
```

## Incremental Builds

### How It Works

1. TypeScript creates `.tsbuildinfo` files
2. On rebuild, compares source timestamps
3. Only recompiles changed files and dependents

### Build Info Files

```plaintext
repo/
├── tsconfig.tsbuildinfo              # Root build info
└── src/packages/
    ├── core/
    │   └── tsconfig.tsbuildinfo      # Package build info
    └── server/
        └── tsconfig.tsbuildinfo
```

### Clean Builds

When incremental builds have issues:

```bash
# Clean all build artifacts
npm run clean

# Script definition
"clean": "rimraf dist tsconfig.tsbuildinfo src/packages/*/.rslib src/packages/*/dist src/packages/*/tsconfig.tsbuildinfo src/packages/*/tsconfig.build.tsbuildinfo"
```

## Using tsgo (Native TypeScript)

Use `tsgo` for faster builds:

```json
{
  "devDependencies": {
    "@typescript/native-preview": "7.0.0-dev.20251203.1"
  },
  "scripts": {
    "build": "npm run type-check && tsgo -b .",
    "type-check": "tsgo -b . --noEmit"
  }
}
```

### Performance Comparison

| Operation   | tsc  | tsgo |
| ----------- | ---- | ---- |
| Full build  | ~15s | ~3s  |
| Incremental | ~5s  | ~1s  |
| Type check  | ~10s | ~2s  |

## Cross-Package Imports

### Import Syntax

```typescript
// Using package name (recommended)
import { Result, Option } from "@scope/core";
import { Result } from "@scope/core/result";

// Works because of:
// 1. npm workspace symlinks
// 2. package.json exports
// 3. tsconfig moduleResolution: "NodeNext"
```

### Type Resolution Flow

1. TypeScript sees `@scope/core`
2. Looks in `node_modules/@scope/core`
3. Finds symlink → `src/packages/core`
4. Reads `package.json` exports
5. Resolves `types` condition to `.d.ts` files

## Workspace Build Scripts

### Root package.json

```json
{
  "scripts": {
    "build": "npm run type-check && tsgo -b .",
    "type-check": "tsgo -b . --noEmit",
    "build:all:workspaces": "npm run build --workspaces"
  }
}
```

### Package package.json

```json
{
  "scripts": {
    "build": "tsgo -p tsconfig.build.json"
  }
}
```

### Build Order

```bash
# Build all workspaces in topological order
npm run build --workspaces

# Build specific package and its dependencies
npm run build --workspace=@scope/server
```

## Troubleshooting

### Error: Cannot find module

**Cause:** Missing build output or incorrect paths

**Fix:**

```bash
# Rebuild all packages
npm run clean && npm run build --workspaces
```

### Error: Output differs from source

**Cause:** Stale `.tsbuildinfo`

**Fix:**

```bash
# Delete build info
rm -rf tsconfig.tsbuildinfo src/packages/*/tsconfig.tsbuildinfo
```

### Error: Circular dependencies

**Cause:** Package A depends on B, B depends on A

**Fix:**

1. Extract shared code to new package
2. Both depend on shared package
3. No cycles allowed

### Declaration not found

**Cause:** `declaration: true` missing

**Fix:**

```json
{
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true
  }
}
```

## Best Practices

1. **Always use `composite: true`** in all tsconfig files
2. **Separate dev and build configs** for clean outputs
3. **Clear paths in packages** - rely on package.json exports
4. **Use `verbatimModuleSyntax`** for ESM correctness
5. **Enable `declarationMap`** for IDE navigation
6. **Use incremental builds** for performance
7. **Extend from root config** for consistency
8. **Include `.tsbuildinfo` in `.gitignore`**
