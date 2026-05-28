---
name: turborepo-monorepo-management
description: Use this skill when managing monorepos with Turborepo, including workspace configuration, build pipelines, caching strategies, and CI/CD optimization.
---

# Turborepo Monorepo Management

Expert guidance for building and managing monorepos with Turborepo. Covers workspace setup, pipeline configuration, caching strategies, and CI/CD optimization.

## Project Structure

```
projectx/
├── apps/                   # Applications
│   ├── auth/              # NestJS auth service
│   ├── order/             # NestJS order service
│   ├── product/           # NestJS product service
│   ├── storybook/         # Component documentation
│   └── web/               # React Router frontend
├── packages/              # Shared packages
│   ├── core/              # @projectx/core - NestJS shared modules
│   ├── db/                # @projectx/db - Prisma client
│   ├── email/             # @projectx/email - Email templates
│   ├── models/            # @projectx/models - TypeScript types
│   ├── payment/           # @projectx/payment - Stripe
│   ├── ui/                # @projectx/ui - React components
│   └── workflows/         # @projectx/workflows - Temporal
├── turbo.json             # Turborepo config
├── pnpm-workspace.yaml    # Workspace definition
└── package.json           # Root package
```

## Quick Start

```bash
# Create new Turborepo monorepo
npx create-turbo@latest my-monorepo

# Add Turborepo to existing monorepo
npm install turbo --save-dev

# Run all build tasks
turbo run build

# Run with cache bypass
turbo run build --force
```

## Workspace Configuration

### pnpm Workspaces (Recommended)

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
  - "tools/*"
```

### npm Workspaces

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev"
  }
}
```

### Yarn Workspaces

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": {
    "packages": ["apps/*", "packages/*"],
    "nohoist": ["**/react-native", "**/react-native/**"]
  }
}
```

## Turbo Configuration

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "build/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**", "test/**"]
    },
    "lint": {
      "dependsOn": ["^build"]
    }
  }
}
```

## Common Commands

### Development

```bash
# Run all apps in development
pnpm dev

# Run specific app
pnpm dev:web
pnpm dev:auth
pnpm dev:order
pnpm dev:product

# Run Storybook
pnpm storybook
```

### Building

```bash
# Build all packages and apps
pnpm build

# Build specific targets
pnpm build:web
pnpm build:ui
pnpm build:auth

# Build with turbo filter
turbo run build --filter=web
turbo run build --filter=@projectx/ui
```

### Testing

```bash
# Run all tests
pnpm test

# Test specific package
pnpm --filter web test
pnpm --filter @projectx/ui test
```

### Filtering

```bash
# Build a package and its dependencies
turbo run build --filter=web...

# Build dependents of a package
turbo run build --filter=...@projectx/ui

# Build everything except one package
turbo run build --filter=!storybook

# Build changed packages since main
turbo run build --filter=[main]
```

## Caching Strategies

### Local Caching

Turbo caches build outputs locally in `node_modules/.cache/turbo`.

```bash
# Clear local cache
turbo run build --force

# View cache status
turbo run build --dry-run
```

### Remote Caching (Optional)

```bash
# Login to Vercel for remote caching
turbo login

# Link to project
turbo link
```

## CI/CD Optimization

### GitHub Actions with Turborepo

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - uses: pnpm/action-setup@v3
        with:
          
      - uses: actions/setup-node@v4
        with:
          node-          cache: "pnpm"

      - run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm turbo run build --filter="...[HEAD^1]"

      - name: Test
        run: pnpm turbo run test --filter="...[HEAD^1]"

      - name: Lint
        run: pnpm turbo run lint --filter="...[HEAD^1]"
```

## Best Practices

1. **Use workspace protocol** - Always use `workspace:*` for internal dependencies.
2. **Keep packages focused** - Each package should have a single responsibility.
3. **Minimize dependencies** - Avoid unnecessary inter-package dependencies.
4. **Use turbo filters** - Run commands only where needed.
5. **Cache outputs** - Configure outputs correctly in turbo.json.
6. **Share configurations** - Use shared TypeScript and ESLint configurations.
7. **Consistent naming** - Use `@projectx/` scope for all packages.

## Troubleshooting

### Common Issues

```bash
# Clear all caches
turbo run clean
rm -rf node_modules .turbo

# Debug cache misses
turbo run build --summarize

# Check why task ran
turbo run build --dry-run=json | jq '.tasks[] | {name, cache}'

# Verbose logging
turbo run build --verbosity=2
```

### Dependency Issues

```bash
# Clean and reinstall (cross-platform)
npx rimraf node_modules pnpm-lock.yaml
pnpm install
```

### Build Order Issues

```bash
# See what turbo will build
turbo run build --dry-run

# Force rebuild without cache
turbo run build --force
```

### Type Issues

```bash
# Regenerate TypeScript build info
pnpm build:core
pnpm build:ui
pnpm build
```

## Quick Reference

| Command                              | Description                   |
| ------------------------------------ | ----------------------------- |
| `turbo run build`                    | Run build in all packages     |
| `turbo run build --filter=web`       | Run in specific package       |
| `turbo run build --filter=...[main]` | Run in changed packages       |
| `turbo run build --force`            | Skip cache                    |
| `turbo run build --dry-run`          | Show what would run           |
| `turbo run build --graph`            | Visualize task graph          |
| `turbo prune --docker`               | Prune for Docker              |
| `turbo login`                        | Authenticate for remote cache |
| `turbo link`                         | Link to Vercel project        |