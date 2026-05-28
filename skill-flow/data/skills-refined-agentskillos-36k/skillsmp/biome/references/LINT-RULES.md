# Biome Lint Rules

Guide for Biome linting rules and configuration in projects.

## Overview

Biome is used as a replacement for ESLint in projects. It provides:
- Fast linting
- Code formatting
- Integrated tooling
- TypeScript support

## Configuration File

Biome uses `biome.json` configuration file in each project.

Example from `GGA Team.this project.WebApi/biome.json`:

```json
{
  "$schema": "https://biomejs.dev/schemas/2.3.2/schema.json",
  "linter": {
    "enabled": true,
    "rules": {
      "correctness": {
        "noUnusedVariables": "error",
        "noUnusedImports": "error",
        "useParseIntRadix": "error"
      },
      "suspicious": {
        "noExplicitAny": "off",
        "noImplicitAnyLet": "off",
        "noDoubleEquals": "warn",
        "noGlobalIsNan": "error"
      },
      "style": {
        "useConst": "error",
        "useImportType": "off",
        "useTemplate": "warn",
        "noNonNullAssertion": "warn"
      },
      "complexity": {
        "noForEach": "off",
        "noBannedTypes": "off",
        "useLiteralKeys": "warn",
        "useOptionalChain": "warn",
        "noStaticOnlyClass": "warn"
      }
    }
  }
}
```

## Rule Categories

### Correctness Rules

**Enforce code correctness and prevent bugs.**

| Rule | Level | Description | Example |
|------|-------|-------------|---------|
| `noUnusedVariables` | error | Disallow unused variables | `const x = 1;` (x not used) |
| `noUnusedImports` | error | Disallow unused imports | `import { foo } from 'bar';` (foo not used) |
| `useParseIntRadix` | error | Require radix in parseInt | `parseInt('10')` → `parseInt('10', 10)` |
| `noUnusedPrivateMembers` | error | Disallow unused private class members | Private method/property never used |

### Suspicious Rules

**Detect potentially problematic code.**

| Rule | Level | Description | Example |
|------|-------|-------------|---------|
| `noExplicitAny` | off | Disallow explicit any type | `const x: any = ...;` |
| `noImplicitAnyLet` | off | Disallow implicit any in let | `let x;` (no type annotation) |
| `noDoubleEquals` | warn | Disallow ==, use === | `x == y` → `x === y` |
| `noGlobalIsNan` | error | Disallow global isNaN | `isNaN(x)` → `Number.isNaN(x)` |
| `noConsoleLog` | off | Disallow console.log | `console.log('debug');` |

### Style Rules

**Enforce consistent code style.**

| Rule | Level | Description | Example |
|------|-------|-------------|---------|
| `useConst` | error | Use const when possible | `let x = 1;` (never reassigned) |
| `useImportType` | off | Use import type for type-only imports | `import { type Foo } from 'bar';` |
| `useTemplate` | warn | Use template literals instead of concatenation | `a + b` → `${a}${b}` |
| `noNonNullAssertion` | warn | Disallow non-null assertion | `x!` → remove or use optional chaining |

### Complexity Rules

**Control code complexity.**

| Rule | Level | Description | Example |
|------|-------|-------------|---------|
| `noForEach` | off | Disallow forEach | Use for...of or map instead |
| `noBannedTypes` | off | Disallow certain types | Restrict {} or object types |
| `useLiteralKeys` | warn | Use literal keys | `obj['key']` → `obj.key` |
| `useOptionalChain` | warn | Use optional chaining | `obj && obj.prop` → `obj?.prop` |
| `noStaticOnlyClass` | warn | Disallow classes with only static members | Use object or namespace |

## Rule Levels

| Level | Behavior | When to Fix |
|-------|----------|-------------|
| `error` | Fails lint/build | Must fix immediately |
| `warn` | Shows warning | Should fix when convenient |
| `off` | Disabled | Ignore the rule |

## Common Issues and Fixes

### Unused Variables/Imports

**Issue**: Biome reports unused imports/variables

**Fix**:
```typescript
// ❌ Error: Unused import
import { foo, bar } from './module';

function test() {
  return foo();
}

// ✅ Fix: Remove unused import
import { foo } from './module';

function test() {
  return foo();
}
```

### Use Const

**Issue**: Biome suggests using const instead of let

**Fix**:
```typescript
// ❌ Warning: Use const
let x = 10;
console.log(x);

// ✅ Fix: Use const
const x = 10;
console.log(x);
```

### Double Equals

**Issue**: Biome warns about == instead of ===

**Fix**:
```typescript
// ❌ Warning: Use ===
if (x == 5) { ... }

// ✅ Fix: Use ===
if (x === 5) { ... }
```

### Optional Chain

**Issue**: Biome suggests optional chaining

**Fix**:
```typescript
// ❌ Warning: Use optional chain
if (user && user.profile && user.profile.name) {
  console.log(user.profile.name);
}

// ✅ Fix: Use optional chain
if (user?.profile?.name) {
  console.log(user.profile.name);
}
```

## Customizing Rules

To customize rules for a project, edit `biome.json`:

```json
{
  "linter": {
    "rules": {
      "suspicious": {
        "noExplicitAny": "warn" // Change from "off" to "warn"
      },
      "style": {
        "useImportType": "error" // Change from "off" to "error"
      }
    }
  }
}
```

## Finding Biome Configurations

```bash
# View WebApi biome config
cat GGA Team.this project.WebApi/biome.json

# View WebExecutor biome config
cat GGA Team.this project.WebExecutor/biome.json

# View all biome configs
find . -name "biome.json" -type f

# Compare configs across projects
diff GGA Team.this project.WebApi/biome.json GGA Team.this project.WebExecutor/biome.json
```

## Related Skills

- **`biome`** - Biome commands and format configuration
- **`webapi`** - NestJS backend linting
- **`testing`** - Test file linting
