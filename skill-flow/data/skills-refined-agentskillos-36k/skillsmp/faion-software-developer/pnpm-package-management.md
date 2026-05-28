---
id: pnpm-package-management
name: "Package Management (pnpm)"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Package Management (pnpm)

## Overview

pnpm is a fast, disk-efficient package manager that uses a content-addressable store and symlinks. This methodology covers pnpm configuration, workspace management, and best practices for modern JavaScript/TypeScript projects.

## When to Use

- All new JavaScript/TypeScript projects
- Monorepo management
- Projects requiring strict dependency isolation
- CI/CD pipelines needing fast installs
- Teams wanting consistent dependency resolution

## Key Principles

1. **Strict by default** - No phantom dependencies
2. **Disk efficiency** - Shared content-addressable store
3. **Workspaces** - First-class monorepo support
4. **Speed** - Faster than npm and yarn
5. **Security** - Prevents dependency confusion attacks

## Best Practices

### Installation and Setup

```bash
# Install pnpm globally
npm install -g pnpm

# Or use corepack (Node.js 16.9+)
corepack enable
corepack prepare pnpm@latest --activate

# Check version
pnpm --version

# Initialize new project
pnpm init

# Install all dependencies
pnpm install

# Shorthand
pnpm i
```

### Configuration

```ini
# .npmrc
# Strict peer dependencies
strict-peer-dependencies=true

# Auto-install peer dependencies
auto-install-peers=true

# Don't hoist to root (strict)
shamefully-hoist=false

# Node.js version enforcement
engine-strict=true

# Lockfile settings
lockfile=true
prefer-frozen-lockfile=true

# Registry
registry=https://registry.npmjs.org/

# Private registry
@mycompany:registry=https://npm.mycompany.com/
```

```yaml
# .pnpmfile.cjs (for dependency hooks)
module.exports = {
  hooks: {
    readPackage(pkg) {
      // Override package.json of dependencies
      if (pkg.name === 'some-package') {
        pkg.dependencies = {
          ...pkg.dependencies,
          'fixed-dep': '^2.0.0',
        };
      }
      return pkg;
    },
  },
};
```

### Dependency Management

```bash
# Add production dependency
pnpm add express zod

# Add dev dependency
pnpm add -D typescript @types/node vitest

# Add peer dependency
pnpm add --save-peer react

# Add optional dependency
pnpm add -O sharp

# Add exact version
pnpm add express@4.18.2 --save-exact

# Add from git
pnpm add github:user/repo
pnpm add git+https://github.com/user/repo.git

# Remove dependency
pnpm remove express

# Update dependencies
pnpm update              # All
pnpm update express      # Single
pnpm update --latest     # To latest (ignore semver)
pnpm update -i           # Interactive mode

# Show outdated
pnpm outdated

# Audit for vulnerabilities
pnpm audit
pnpm audit --fix         # Auto-fix where possible

# Why is package installed?
pnpm why lodash
```

### Workspaces (Monorepo)

```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'
  - 'tools/*'
```

```
project/
├── pnpm-workspace.yaml
├── package.json
├── pnpm-lock.yaml
├── apps/
│   ├── web/
│   │   └── package.json
│   └── api/
│       └── package.json
├── packages/
│   ├── ui/
│   │   └── package.json
│   ├── config/
│   │   └── package.json
│   └── types/
│       └── package.json
└── tools/
    └── scripts/
        └── package.json
```

```json
// Root package.json
{
  "name": "monorepo",
  "private": true,
  "scripts": {
    "build": "pnpm -r build",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint",
    "dev": "pnpm --filter web dev"
  },
  "devDependencies": {
    "typescript": "^5.3.0"
  }
}
```

### Workspace Commands

```bash
# Run command in all packages
pnpm -r build
pnpm --recursive build

# Run in specific package
pnpm --filter web build
pnpm --filter @mycompany/ui build

# Run in packages matching pattern
pnpm --filter "./packages/*" build

# Run in package and its dependencies
pnpm --filter web... build

# Run in dependents of package
pnpm --filter ...@mycompany/ui build

# Add dependency to specific workspace
pnpm --filter web add react

# Add workspace package as dependency
pnpm --filter web add @mycompany/ui --workspace

# Install only for specific workspace
pnpm --filter web install
```

### Workspace Package References

```json
// apps/web/package.json
{
  "name": "@mycompany/web",
  "dependencies": {
    "@mycompany/ui": "workspace:*",
    "@mycompany/types": "workspace:^1.0.0",
    "react": "^18.0.0"
  }
}
```

```
workspace:* - Any version from workspace
workspace:^ - Compatible versions (^)
workspace:~ - Patch versions (~)
workspace:1.0.0 - Exact version
```

### Scripts and Lifecycle

```json
// package.json
{
  "scripts": {
    "preinstall": "npx only-allow pnpm",
    "prepare": "husky install",
    "build": "tsc -b",
    "test": "vitest run",
    "lint": "eslint . --fix",
    "typecheck": "tsc --noEmit"
  }
}
```

```bash
# Run script
pnpm build
pnpm run build

# Run with arguments
pnpm test -- --coverage

# Run multiple scripts sequentially
pnpm build && pnpm test

# Run scripts in parallel
pnpm -r --parallel build

# Run in topological order (respecting deps)
pnpm -r build  # Default behavior
```

### CI/CD Configuration

```yaml
# GitHub Actions
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm build

      - name: Test
        run: pnpm test

      - name: Lint
        run: pnpm lint
```

```dockerfile
# Dockerfile
FROM node:20-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

FROM base AS deps
WORKDIR /app
COPY pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm fetch

FROM deps AS build
COPY . .
RUN pnpm install --frozen-lockfile --offline
RUN pnpm build

FROM base AS runtime
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules

CMD ["node", "dist/index.js"]
```

### Publishing Packages

```bash
# Prepare for publish
pnpm pack

# Publish to npm
pnpm publish

# Publish with access level
pnpm publish --access public

# Workspace publishing
pnpm -r publish

# Changesets for versioning
pnpm add -Dw @changesets/cli
pnpm changeset init
pnpm changeset       # Create changeset
pnpm changeset version  # Update versions
pnpm -r publish      # Publish all
```

### Store Management

```bash
# Show store path
pnpm store path

# Prune unreferenced packages
pnpm store prune

# Verify store integrity
pnpm store status

# Add to store without installing
pnpm fetch
```

## Anti-patterns

### Avoid: Using npm/yarn Commands

```bash
# BAD - mixing package managers
npm install lodash
yarn add express

# GOOD - use pnpm consistently
pnpm add lodash express
```

### Avoid: Not Committing Lockfile

```gitignore
# BAD
pnpm-lock.yaml

# GOOD - always commit lockfile
# pnpm-lock.yaml should be in git
```

### Avoid: Shamefully Hoisting

```ini
# BAD - defeats pnpm's benefits
shamefully-hoist=true

# GOOD - keep strict (default)
shamefully-hoist=false
```

## References

- [pnpm Documentation](https://pnpm.io/)
- [pnpm Workspaces](https://pnpm.io/workspaces)
- [pnpm CLI](https://pnpm.io/cli/add)
- [Changesets](https://github.com/changesets/changesets)
