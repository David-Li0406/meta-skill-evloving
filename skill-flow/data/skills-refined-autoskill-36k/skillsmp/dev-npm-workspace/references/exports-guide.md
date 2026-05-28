# Subpath Exports Configuration Guide

## Overview

Node.js subpath exports enable packages to define multiple entry points, providing fine-grained control over what consumers can import. This is essential for tree-shaking and API encapsulation in workspace packages.

## Basic Structure

### Root Package Exports

The root `package.json` exports both the main entry and workspace packages:

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./core": {
      "types": "./src/packages/core/dist/index.d.ts",
      "import": "./src/packages/core/dist/index.js"
    },
    "./utils": {
      "types": "./src/packages/utils/dist/index.d.ts",
      "import": "./src/packages/utils/dist/index.js"
    },
    "./server": {
      "types": "./src/packages/server/dist/index.d.ts",
      "import": "./src/packages/server/dist/index.js"
    }
  }
}
```

### Package-Level Exports

Each workspace package has its own exports:

```json
{
  "exports": {
    ".": {
      "source": "./src/index.ts",
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./result": {
      "source": "./src/result/index.ts",
      "types": "./dist/result/index.d.ts",
      "import": "./dist/result/index.js"
    },
    "./task": {
      "source": "./src/task/index.ts",
      "types": "./dist/task/index.d.ts",
      "import": "./dist/task/index.js"
    }
  }
}
```

## Export Conditions

### Condition Order Matters

Conditions are evaluated in order; first match wins:

```json
{
  "exports": {
    ".": {
      "source": "./src/index.ts", // Bundler development
      "types": "./dist/index.d.ts", // TypeScript
      "import": "./dist/index.js" // Node.js ESM
    }
  }
}
```

### Common Conditions

| Condition     | Environment | Use Case                  |
| ------------- | ----------- | ------------------------- |
| `types`       | TypeScript  | Type definitions (.d.ts)  |
| `import`      | Node.js ESM | `import` statements       |
| `require`     | Node.js CJS | `require()` calls         |
| `default`     | Fallback    | Universal fallback        |
| `source`      | Bundlers    | Development source files  |
| `browser`     | Browsers    | Browser-specific builds   |
| `node`        | Node.js     | Node.js-specific builds   |
| `production`  | Production  | Minified/optimized builds |
| `development` | Development | Debug builds              |

### Dual Package Support

For packages supporting both ESM and CommonJS:

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/esm/index.js",
      "require": "./dist/cjs/index.js"
    }
  }
}
```

## Pattern Examples

### Pattern 1: Main Entry Only

Simplest case - single entry point:

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    }
  }
}
```

**Import:**

```typescript
import { Result, Option } from "@scope/core";
```

### Pattern 2: Subpath Modules

Multiple entry points for different features:

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./result": {
      "types": "./dist/result/index.d.ts",
      "import": "./dist/result/index.js"
    },
    "./task": {
      "types": "./dist/task/index.d.ts",
      "import": "./dist/task/index.js"
    },
    "./schema": {
      "types": "./dist/schema/index.d.ts",
      "import": "./dist/schema/index.js"
    }
  }
}
```

**Imports:**

```typescript
// Full package
import { Result, Task, Schema } from "@scope/core";

// Specific module (tree-shakeable)
import { Result, Option } from "@scope/core/result";
import { Task, TaskEither } from "@scope/core/task";
```

### Pattern 3: Wildcard Exports

Dynamic subpath matching:

```json
{
  "exports": {
    ".": "./dist/index.js",
    "./*": "./dist/*/index.js",
    "./internal/*": null // Block access to internal modules
  }
}
```

**Note:** Wildcards are powerful but can be hard to maintain. Prefer explicit exports.

### Pattern 4: Nested Subpaths

Deep module access:

```json
{
  "exports": {
    ".": "./dist/index.js",
    "./result/ok": "./dist/result/ok/index.js",
    "./result/option": "./dist/result/option/index.js",
    "./result/either": "./dist/result/either/index.js"
  }
}
```

**Import:**

```typescript
import { ok, err, isOk } from "@scope/core/result/ok";
```

### Pattern 5: Source Condition for Bundlers

Enable direct source imports for bundlers (Vite, Webpack, esbuild):

```json
{
  "exports": {
    ".": {
      "source": "./src/index.ts",
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    }
  }
}
```

**Benefits:**

- HMR with original source
- Better source maps
- Avoid double-compilation

## Example Export Map

### core

```json
{
  "exports": {
    ".": { "types": "./dist/index.d.ts", "import": "./dist/index.js" },
    "./algebra": { ... },
    "./result": { ... },
    "./task": { ... },
    "./schema": { ... },
    "./stream": { ... },
    "./optics": { ... },
    "./security": { ... },
    "./fp": { ... },
    "./collections": { ... },
    "./validation": { ... },
    "./infra": { ... },
    "./async": { ... },
    "./temporal": { ... },
    "./observability": { ... },
    "./encoding": { ... },
    "./resource": { ... }
  }
}
```

### server

```json
{
  "exports": {
    ".": { ... },
    "./utils": { ... },
    "./intent": { ... },
    "./sdui": { ... },
    "./ssr": { ... },
    "./policy": { ... },
    "./security": { ... },
    "./realtime": { ... },
    "./adapters": { ... }
  }
}
```

## TypeScript Integration

### Type-First Resolution

Always list `types` condition first:

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts", // FIRST
      "import": "./dist/index.js"
    }
  }
}
```

### tsconfig.json Requirements

Enable package.json exports resolution:

```json
{
  "compilerOptions": {
    "moduleResolution": "NodeNext",
    "resolvePackageJsonExports": true,
    "resolvePackageJsonImports": true
  }
}
```

### Declaration Maps

Enable declaration maps for "Go to Definition":

```json
{
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true
  }
}
```

## Preventing Internal Imports

### Explicit Deny

Block specific paths:

```json
{
  "exports": {
    ".": "./dist/index.js",
    "./internal/*": null,
    "./_private/*": null
  }
}
```

### Missing = Blocked

Unlisted paths are automatically blocked:

```json
{
  "exports": {
    ".": "./dist/index.js",
    "./result": "./dist/result/index.js"
    // "./internals" is NOT listed = blocked
  }
}
```

Attempting to import unlisted paths:

```typescript
import { internal } from "@scope/core/internals";
// Error: Package subpath './internals' is not defined by "exports"
```

## Migration Guide

### From `main` to `exports`

**Before (legacy):**

```json
{
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "module": "./dist/esm/index.js"
}
```

**After (modern):**

```json
{
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    }
  }
}
```

**Note:** Keep `main` and `types` for backwards compatibility with older tools.

### Adding Subpath Exports

1. Identify public modules
2. Create index.ts for each subpath
3. Add to exports map
4. Update imports in consuming code

## Debugging Exports

### Check Resolution

```bash
# Node.js module resolution
node --input-type=module -e "import('@scope/core/result')"

# Check with npm
npm explain @scope/core
```

### Common Errors

| Error                           | Cause                     | Fix                     |
| ------------------------------- | ------------------------- | ----------------------- |
| `ERR_PACKAGE_PATH_NOT_EXPORTED` | Subpath not in exports    | Add to exports map      |
| `ERR_MODULE_NOT_FOUND`          | File doesn't exist        | Check path, build first |
| TypeScript can't find types     | Missing `types` condition | Add `types` field       |

## Best Practices

1. **List `types` first** - TypeScript resolves conditions in order
2. **Include `source` for bundlers** - Better development experience
3. **Be explicit** - List all public subpaths explicitly
4. **Block internals** - Don't export implementation details
5. **Match directory structure** - Subpath should reflect file structure
6. **Use consistent pattern** - Same structure across all exports
7. **Test all paths** - Verify each export resolves correctly
