# NPM Workspace Architecture

## Overview

npm workspaces is a native monorepo solution built into npm (v7+) that enables managing multiple packages within a single repository. This document explains the architecture patterns used in this skill.

## Core Concepts

### 1. Workspace Declaration

The root `package.json` declares workspace locations using glob patterns:

```json
{
  "workspaces": [
    "src/packages/core",
    "src/packages/utils",
    "src/packages/server",
    "examples/ecom/backend",
    "examples/ecom/frontend"
  ]
}
```

**Pattern Options:**

| Pattern            | Description                      |
| ------------------ | -------------------------------- |
| `"packages/*"`     | All direct children of packages/ |
| `"src/packages/*"` | Nested package directory         |
| `"apps/*"`         | Application packages             |
| `"packages/**"`    | Recursive (all nested packages)  |

### 2. Hoisting

npm workspaces hoists shared dependencies to the root `node_modules`:

```plaintext
repo/
├── node_modules/           # Hoisted dependencies
│   ├── typescript/
│   ├── eslint/
│   └── @scope/
│       ├── package1/ -> ../../src/packages/package1  # Symlink!
│       └── package2/ -> ../../src/packages/package2  # Symlink!
├── src/packages/
│   ├── package1/
│   │   ├── node_modules/   # Package-specific deps (if needed)
│   │   └── package.json
│   └── package2/
│       └── package.json
└── package.json
```

**Benefits:**

- Single `node_modules` for shared dependencies
- Disk space savings
- Consistent versions across packages
- Symlinked workspace packages for instant updates

### 3. Topological Ordering

npm automatically orders workspace operations based on dependency graph:

```plaintext
core (no deps)
    ↓
utils (depends on core)
    ↓
server (depends on core, utils)
```

When running `npm run build --workspaces`, packages build in correct order.

## Architecture Patterns

### Pattern 1: Layered Dependencies

Packages form dependency layers where higher layers depend on lower:

```plaintext
Layer 0: core (core primitives)
Layer 1: utils (depends on Layer 0)
Layer 2: server (depends on Layer 0-1)
```

**Rules:**

- Lower layers NEVER depend on higher layers
- Same-layer packages MAY depend on each other if no cycles
- Circular dependencies are forbidden

### Pattern 2: Feature Packages

Each package owns a complete feature domain:

| Package  | Domain | Responsibility                               |
| -------- | ------ | -------------------------------------------- |
| `core`   | Core   | Functional primitives (Result, Option, Task) |
| `utils`  | Utils  | Shared utilities and helpers                 |
| `server` | Server | HTTP, APIs, SSR                              |

### Pattern 3: Shared Development Dependencies

DevDependencies are declared at root only:

```json
// Root package.json
{
  "devDependencies": {
    "typescript": "^5.9.3",
    "eslint": "latest",
    "prettier": "latest",
    "@typescript/native-preview": "7.0.0-dev.20251203.1"
  }
}
```

```json
// Package package.json - NO devDependencies
{
  "devDependencies": {}
}
```

**Why?**

- Single version of TypeScript, ESLint, etc.
- Faster installs
- Consistent tooling across all packages

### Pattern 4: Workspace Protocol

Reference sibling packages using `"*"`:

```json
// server/package.json
{
  "dependencies": {
    "@scope/core": "*",
    "@scope/utils": "*"
  }
}
```

**How it works:**

- `"*"` resolves to the local workspace version
- npm creates symlinks in `node_modules`
- No version conflicts between workspace packages
- Changes are immediately visible (no reinstall needed)

## Directory Structure Deep Dive

```plaintext
repo/
├── package.json              # Workspace root
├── package-lock.json         # Single lock file for all
├── tsconfig.json             # Root TypeScript config
├── eslint.config.ts          # Shared ESLint config
├── .prettierrc.json          # Shared Prettier config
├── .npmrc                    # Registry configuration
│
├── src/
│   ├── index.ts              # Root entry (re-exports)
│   └── packages/
│       ├── core/
│       │   ├── package.json
│       │   ├── tsconfig.json       # Extends root
│       │   ├── tsconfig.build.json # Production build
│       │   ├── README.md
│       │   ├── src/
│       │   │   ├── index.ts
│       │   │   ├── core/
│       │   │   ├── task/
│       │   │   └── ...
│       │   └── dist/               # Built output
│       │
│       ├── utils/
│       │   ├── package.json
│       │   ├── tsconfig.json
│       │   ├── tsconfig.build.json
│       │   ├── src/
│       │   └── dist/
│       │
│       └── server/
│           ├── package.json        # Has dependencies on siblings
│           ├── tsconfig.json
│           ├── tsconfig.build.json
│           ├── src/
│           └── dist/
│
└── examples/                       # Example applications
    └── ecom/
        ├── backend/                # Also a workspace package
        │   └── package.json
        └── frontend/
            └── package.json
```

## Scripts Architecture

### Root Scripts

```json
{
  "scripts": {
    "build": "npm run type-check && tsgo -b .",
    "type-check": "tsgo -b . --noEmit",
    "build:all:workspaces": "npm run build --workspaces",
    "clean": "rimraf dist tsconfig.tsbuildinfo src/packages/*/dist",
    "lint": "eslint . --ext .ts",
    "format": "prettier --write 'src/packages/**/*.{ts,js,md}'"
  }
}
```

### Package Scripts

```json
{
  "scripts": {
    "build": "tsgo -p tsconfig.build.json",
    "lint": "eslint .",
    "format": "prettier --write ."
  }
}
```

### Running Scripts

```bash
# Run in all workspaces
npm run build --workspaces

# Run in specific package
npm run build --workspace=@scope/core

# Run in multiple packages
npm run build --workspace=@scope/core --workspace=@scope/utils
```

## Versioning Strategy

### Independent Versioning

Each package has its own version:

```json
// core/package.json
{ "version": "1.1.0" }

// server/package.json
{ "version": "1.0.0" }
```

### Release-Please Integration

Use release-please for automated versioning:

```json
// .release-please-manifest.json
{
  "src/packages/core": "1.1.0",
  "src/packages/utils": "1.0.0",
  "src/packages/server": "1.0.0"
}
```

## Publishing

### Private Packages

Packages with `"private": true` are not published:

```json
{
  "private": true
}
```

### GitHub Package Registry

```json
// Root package.json
{
  "publishConfig": {
    "registry": "https://npm.pkg.github.com"
  }
}
```

```ini
# .npmrc
@scope:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GH_TOKEN}
```

### Publishing Commands

```bash
# Publish all non-private packages
npm publish --workspaces

# Publish specific package
npm publish --workspace=@scope/core
```

## Performance Optimization

### 1. Incremental Builds

TypeScript project references enable incremental builds:

```json
{
  "compilerOptions": {
    "composite": true,
    "incremental": true
  }
}
```

### 2. Build Caching

`.tsbuildinfo` files cache compilation results:

```bash
# Clean caches when needed
rimraf src/packages/*/tsconfig.tsbuildinfo
```

### 3. Parallel Execution

npm 9+ supports parallel workspace operations:

```bash
# Build in parallel (where possible)
npm run build --workspaces --if-present
```

## Best Practices Checklist

- [ ] All workspace packages listed in root `workspaces` array
- [ ] Consistent naming with scope: `@scope/package-name`
- [ ] Cross-package deps use `"*"` (workspace protocol)
- [ ] DevDependencies at root only
- [ ] Each package has `"type": "module"`
- [ ] TypeScript configs extend root config
- [ ] Separate `tsconfig.build.json` for production
- [ ] Single `package-lock.json` at root
- [ ] No circular dependencies between packages
