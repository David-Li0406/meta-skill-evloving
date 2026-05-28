# Monorepo Setup with Nx + pnpm Workspaces

## Overview

**Key Principle:** Nx doesn't replace package managers—it builds on top of them.

**Recommended Stack:**
- **pnpm workspaces** - Package manager's workspace model for dependency management
- **Nx** - Task orchestration, caching, and build optimization
- Both work together for optimal monorepo management

**Why this combination:**
- pnpm handles package installation and linking
- Nx handles task running, caching, and affected commands
- Best of both worlds: dependency management + task optimization

---

## Initial Setup

### Prerequisites

**Install tools:**
```bash
# Via Homebrew
brew install pnpm node

# Or via npm
npm install -g pnpm
```

**Verify:**
```bash
pnpm --version
node --version
```

### Create Monorepo

**Option 1: Start from scratch**
```bash
# Create directory
mkdir my-monorepo && cd my-monorepo

# Initialize pnpm workspace
pnpm init

# Add Nx
pnpm add -D nx @nx/workspace
```

**Option 2: Use Nx preset**
```bash
npx create-nx-workspace@latest my-monorepo
# Choose: pnpm as package manager
# Choose: Integrated monorepo or Standalone
```

---

## pnpm Workspaces Configuration

### pnpm-workspace.yaml

**Root file defining workspace packages:**
```yaml
packages:
  - 'packages/*'
  - 'apps/*'
  - 'tools/*'
```

This tells pnpm where to find workspace packages.

### Root package.json

```json
{
  "name": "my-monorepo",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "dev": "nx run-many --target=dev --all",
    "build": "nx run-many --target=build --all",
    "test": "nx run-many --target=test --all",
    "lint": "nx run-many --target=lint --all",
    "format": "nx format:write",
    "affected:test": "nx affected --target=test",
    "affected:build": "nx affected --target=build"
  },
  "devDependencies": {
    "nx": "^18.0.0",
    "@nx/workspace": "^18.0.0",
    "@nx/js": "^18.0.0",
    "typescript": "^5.3.0"
  },
  "packageManager": "pnpm@8.15.0"
}
```

### .npmrc

**pnpm configuration:**
```ini
# Hoist dependencies to root node_modules
shamefully-hoist=false
hoist-pattern[]=*eslint*
hoist-pattern[]=*prettier*

# Strict peer dependencies
strict-peer-dependencies=true

# Store directory
store-dir=~/.pnpm-store

# Auto install peers
auto-install-peers=true

# Link workspace packages
link-workspace-packages=true
```

---

## Nx Configuration

### nx.json

**Core Nx configuration:**
```json
{
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "extends": "nx/presets/npm.json",
  "tasksRunnerOptions": {
    "default": {
      "runner": "nx/tasks-runners/default",
      "options": {
        "cacheableOperations": ["build", "lint", "test", "type-check"],
        "parallel": 3
      }
    }
  },
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "cache": true
    },
    "test": {
      "cache": true
    },
    "lint": {
      "cache": true
    },
    "type-check": {
      "cache": true
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*", "sharedGlobals"],
    "production": [
      "default",
      "!{projectRoot}/**/?(*.)+(spec|test).[jt]s?(x)?(.snap)",
      "!{projectRoot}/tsconfig.spec.json",
      "!{projectRoot}/.eslintrc.json"
    ],
    "sharedGlobals": []
  },
  "generators": {
    "@nx/react": {
      "application": {
        "babel": false,
        "style": "css",
        "linter": "eslint",
        "bundler": "vite"
      }
    }
  }
}
```

---

## Project Structure

**Typical monorepo layout:**
```
my-monorepo/
├── apps/
│   ├── web/                    # Next.js frontend
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── src/
│   └── api/                    # Express backend
│       ├── package.json
│       ├── tsconfig.json
│       └── src/
├── packages/
│   ├── shared-ui/              # Shared React components
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── src/
│   ├── shared-types/           # Shared TypeScript types
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── src/
│   └── utils/                  # Shared utilities
│       ├── package.json
│       ├── tsconfig.json
│       └── src/
├── tools/
│   └── scripts/                # Build scripts, generators
├── pnpm-workspace.yaml
├── nx.json
├── package.json
├── tsconfig.base.json          # Base TypeScript config
└── .gitignore
```

---

## Creating Packages

### TypeScript Library

**packages/utils/package.json:**
```json
{
  "name": "@repo/utils",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    }
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "lint": "eslint src",
    "type-check": "tsc --noEmit",
    "test": "vitest"
  },
  "devDependencies": {
    "@repo/typescript-config": "workspace:*",
    "typescript": "^5.3.0",
    "vitest": "^1.0.0"
  }
}
```

**packages/utils/tsconfig.json:**
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts"]
}
```

**packages/utils/project.json (Nx):**
```json
{
  "name": "utils",
  "$schema": "../../node_modules/nx/schemas/project-schema.json",
  "sourceRoot": "packages/utils/src",
  "projectType": "library",
  "targets": {
    "build": {
      "executor": "nx:run-commands",
      "outputs": ["{projectRoot}/dist"],
      "options": {
        "command": "tsc",
        "cwd": "packages/utils"
      }
    },
    "lint": {
      "executor": "@nx/eslint:lint"
    },
    "test": {
      "executor": "@nx/vite:test"
    }
  },
  "tags": ["type:util"]
}
```

### Next.js Application

**apps/web/package.json:**
```json
{
  "name": "@repo/web",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "@repo/shared-ui": "workspace:*",
    "@repo/utils": "workspace:*",
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@repo/typescript-config": "workspace:*",
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "typescript": "^5.3.0"
  }
}
```

---

## Shared Configurations

### Shared TypeScript Config

**packages/typescript-config/package.json:**
```json
{
  "name": "@repo/typescript-config",
  "version": "0.0.0",
  "private": true,
  "files": ["base.json", "nextjs.json", "react-library.json"]
}
```

**packages/typescript-config/base.json:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    "strict": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

**Usage in package:**
```json
{
  "extends": "@repo/typescript-config/base.json",
  "compilerOptions": {
    "outDir": "./dist"
  }
}
```

### Shared ESLint Config

**packages/eslint-config/package.json:**
```json
{
  "name": "@repo/eslint-config",
  "version": "0.0.0",
  "private": true,
  "main": "index.js",
  "dependencies": {
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint-config-prettier": "^9.0.0"
  }
}
```

---

## Dependency Management

### Installing Dependencies

**Workspace root:**
```bash
pnpm add -D -w typescript
```

**Specific package:**
```bash
pnpm add axios --filter @repo/web
pnpm add -D vitest --filter @repo/utils
```

**All packages:**
```bash
pnpm add -r lodash
```

### Workspace Dependencies

**Use `workspace:*` protocol:**
```json
{
  "dependencies": {
    "@repo/utils": "workspace:*",
    "@repo/shared-ui": "workspace:^"
  }
}
```

**Install all:**
```bash
pnpm install
```

This creates symlinks between workspace packages.

---

## Nx Task Running

### Run Single Task

```bash
# Run specific project
nx build @repo/utils
nx test @repo/web

# With Nx console
nx run @repo/utils:build
```

### Run Many Tasks

```bash
# Run target for all projects
nx run-many --target=build --all

# Run specific projects
nx run-many --target=test --projects=utils,web

# Parallel execution
nx run-many --target=build --all --parallel=3
```

### Affected Commands

**Only run tasks for affected projects:**
```bash
# Test affected
nx affected --target=test

# Build affected
nx affected --target=build

# Based on specific base
nx affected --target=test --base=main
```

**How it works:**
- Git diff to find changed files
- Nx project graph to find dependent projects
- Only runs tasks for affected projects

### Task Dependencies

**Ensure dependencies build first:**
```json
{
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
```

The `^` means "run for dependencies first".

---

## Nx Caching

### How Caching Works

1. **Task inputs** - Source files, dependencies, environment
2. **Hash computation** - Nx computes hash of inputs
3. **Cache check** - If hash exists, restore outputs
4. **Cache store** - After task runs, store outputs

### Cache Configuration

**nx.json:**
```json
{
  "tasksRunnerOptions": {
    "default": {
      "options": {
        "cacheableOperations": ["build", "lint", "test"],
        "cacheDirectory": ".nx/cache"
      }
    }
  }
}
```

### Cache Commands

```bash
# Clear cache
nx reset

# Run without cache
nx build @repo/utils --skip-nx-cache

# View cache info
nx show projects --with-target=build
```

---

## Project Graph

**Visualize dependencies:**
```bash
nx graph
```

Opens interactive graph showing:
- All projects
- Dependencies between projects
- Task dependencies

**Export graph:**
```bash
nx graph --file=graph.html
```

---

## Generators

### Create Generator

**tools/generators/package/index.ts:**
```ts
import { Tree, formatFiles, generateFiles, joinPathFragments } from '@nx/devkit'

export default async function (tree: Tree, schema: { name: string }) {
  generateFiles(
    tree,
    joinPathFragments(__dirname, './files'),
    `packages/${schema.name}`,
    {
      name: schema.name,
      packageName: `@repo/${schema.name}`,
    }
  )
  await formatFiles(tree)
}
```

**Usage:**
```bash
nx g @repo/tools:package my-new-package
```

---

## Multi-Language Monorepos

**Combine TypeScript, Rust, Python:**

**Directory structure:**
```
monorepo/
├── apps/
│   └── web/                    # TypeScript/Next.js
├── packages/
│   ├── ui/                     # TypeScript/React
│   └── core/                   # Rust library
├── services/
│   └── api/                    # Python/FastAPI
├── pnpm-workspace.yaml         # For TypeScript packages
├── Cargo.toml                  # For Rust workspace
└── nx.json                     # Nx orchestrates all
```

**Cargo.toml (Rust workspace):**
```toml
[workspace]
members = ["packages/core"]
resolver = "2"
```

**Nx orchestrates tasks across all languages:**
```bash
# Build everything
nx run-many --target=build --all

# This runs:
# - tsc for TypeScript packages
# - cargo build for Rust packages
# - Python package builds
```

---

## Common Scripts

**Root package.json:**
```json
{
  "scripts": {
    "dev": "nx run-many --target=dev --all --parallel=10",
    "build": "nx run-many --target=build --all",
    "build:affected": "nx affected --target=build",
    "test": "nx run-many --target=test --all",
    "test:affected": "nx affected --target=test",
    "lint": "nx run-many --target=lint --all",
    "lint:fix": "nx run-many --target=lint --all --fix",
    "format": "nx format:write",
    "format:check": "nx format:check",
    "type-check": "nx run-many --target=type-check --all",
    "clean": "nx reset && rm -rf node_modules **/node_modules",
    "graph": "nx graph"
  }
}
```

---

## Best Practices

1. **Use workspace protocol** - `workspace:*` for internal dependencies
2. **Shared configs** - Extract common configs to shared packages
3. **Project tags** - Use Nx tags for organization and linting rules
4. **Cache everything** - Mark builds, tests, lints as cacheable
5. **Affected commands** - Use in CI to only test/build changed code
6. **Project boundaries** - Define clear boundaries with Nx enforce-module-boundaries
7. **Type-safe imports** - Use TypeScript project references

---

## Quick Reference

**Setup:**
```bash
pnpm init
pnpm add -D nx @nx/workspace
```

**Package management:**
```bash
pnpm add package --filter @repo/app
pnpm add -D -w devtool
pnpm install
```

**Nx commands:**
```bash
nx build @repo/package
nx run-many --target=build --all
nx affected --target=test
nx graph
nx reset
```

**Files:**
- `pnpm-workspace.yaml` - Workspace definition
- `nx.json` - Nx configuration
- `package.json` - Root package
- `project.json` - Per-project Nx config
