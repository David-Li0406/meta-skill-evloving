# Monorepo Tooling

Integration patterns for Turborepo, Nx, Lerna, and pnpm workspaces with Claude Code.

## Tool Comparison

| Feature | Turborepo | Nx | Lerna | pnpm |
|---------|-----------|-----|-------|------|
| Caching | Remote + Local | Remote + Local | Via Nx | Local |
| Task graph | Yes | Yes | Via Nx | Basic |
| Affected detection | Yes | Yes | Via Nx | No |
| Plugins | No | Yes | No | No |
| Learning curve | Low | Medium | Low | Low |

## Turborepo

### Configuration

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": []
    },
    "lint": {
      "outputs": []
    },
    "typecheck": {
      "dependsOn": ["^typecheck"],
      "outputs": []
    }
  }
}
```

### Essential Commands

```bash
# Build everything
turbo run build

# Build single package
turbo run build --filter=@org/package

# Build package + dependencies
turbo run build --filter=@org/package...

# Build package + dependents
turbo run build --filter=...@org/package

# Build only changed (since last commit)
turbo run build --filter=...[HEAD^]

# Build only changed (since main)
turbo run build --filter=...[main]

# Multiple tasks
turbo run build test lint

# Parallel tasks
turbo run lint typecheck --parallel

# See what would run
turbo run build --dry-run

# View task graph
turbo run build --graph
```

### Filtering Syntax

| Filter | Meaning |
|--------|---------|
| `--filter=pkg` | Single package |
| `--filter=pkg...` | Package + its dependencies |
| `--filter=...pkg` | Package + its dependents |
| `--filter=...pkg...` | Package + deps + dependents |
| `--filter=...[ref]` | Changed since git ref |
| `--filter=./apps/*` | Glob pattern |
| `--filter=!pkg` | Exclude package |

### Caching

```bash
# Check cache status
turbo run build --dry-run

# Force rebuild (skip cache)
turbo run build --force

# Show cache location
turbo config
```

### Claude Code Integration

```bash
# Before making changes - identify affected packages
turbo run build --dry-run --filter=...[HEAD^]

# After changes - build affected
turbo run build test --filter=...@org/changed-package

# Full validation
turbo run build test lint typecheck
```

## Nx

### Configuration

```json
// nx.json
{
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["{projectRoot}/dist"]
    },
    "test": {
      "dependsOn": ["build"]
    }
  },
  "defaultBase": "main"
}
```

### Essential Commands

```bash
# Build everything
nx run-many --target=build

# Build single package
nx run @org/package:build

# Build affected only
nx affected --target=build

# Build affected since specific ref
nx affected --target=build --base=main

# Show affected projects
nx affected --print-affected

# Multiple targets
nx run-many --target=build,test

# View dependency graph
nx graph

# View affected graph
nx affected:graph
```

### Project Configuration

```json
// packages/mylib/project.json
{
  "name": "@org/mylib",
  "targets": {
    "build": {
      "executor": "@nx/js:tsc",
      "outputs": ["{projectRoot}/dist"],
      "options": {
        "outputPath": "packages/mylib/dist",
        "main": "packages/mylib/src/index.ts",
        "tsConfig": "packages/mylib/tsconfig.lib.json"
      }
    },
    "test": {
      "executor": "@nx/jest:jest",
      "options": {
        "jestConfig": "packages/mylib/jest.config.ts"
      }
    }
  }
}
```

### Generators

```bash
# Generate new library
nx g @nx/js:library mylib --directory=packages/mylib

# Generate new app
nx g @nx/next:application myapp --directory=apps/myapp

# Generate component
nx g @nx/react:component Button --project=@org/ui

# List available generators
nx list
```

### Claude Code Integration

```bash
# Identify affected before work
nx affected --print-affected

# After changes
nx affected --target=build
nx affected --target=test

# Check for circular deps
nx graph --affected
```

## Lerna

### Configuration

```json
// lerna.json
{
  "version": "independent",
  "npmClient": "pnpm",
  "useWorkspaces": true,
  "command": {
    "version": {
      "conventionalCommits": true
    },
    "publish": {
      "conventionalCommits": true
    }
  }
}
```

### Essential Commands

```bash
# Run script in all packages
lerna run build

# Run in specific package
lerna run build --scope=@org/package

# Run in package + dependencies
lerna run build --scope=@org/package --include-dependencies

# Run in changed packages
lerna run build --since=main

# List packages
lerna list

# List changed packages
lerna changed

# Version packages
lerna version

# Publish packages
lerna publish
```

### Filtering

```bash
# Single scope
lerna run build --scope=@org/package

# Multiple scopes
lerna run build --scope=@org/core --scope=@org/utils

# Glob pattern
lerna run build --scope='@org/app-*'

# Exclude
lerna run build --ignore=@org/docs

# Since ref
lerna run build --since=main
```

### Claude Code Integration

```bash
# Check what's changed
lerna changed

# Build changed
lerna run build --since=HEAD^

# Test changed
lerna run test --since=HEAD^
```

## pnpm Workspaces

### Configuration

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
  - 'apps/*'
```

```json
// package.json
{
  "name": "monorepo",
  "private": true,
  "packageManager": "pnpm@8.0.0"
}
```

### Essential Commands

```bash
# Install all dependencies
pnpm install

# Run script in all packages
pnpm -r run build

# Run in specific package
pnpm --filter @org/package run build

# Run in package + dependencies
pnpm --filter @org/package... run build

# Run in package + dependents
pnpm --filter ...@org/package run build

# Run in changed packages
pnpm --filter "...[HEAD^]" run build

# Add dependency to package
pnpm --filter @org/package add lodash

# Add internal dependency
pnpm --filter @org/consumer add @org/provider

# List packages
pnpm -r list
```

### Filter Syntax

| Filter | Meaning |
|--------|---------|
| `--filter pkg` | Single package |
| `--filter pkg...` | Package + dependencies |
| `--filter ...pkg` | Package + dependents |
| `--filter "./apps/*"` | Glob pattern |
| `--filter "...[ref]"` | Changed since ref |

### Claude Code Integration

```bash
# Build affected
pnpm --filter "...[HEAD^]" run build

# Test affected
pnpm --filter "...[HEAD^]" run test

# Typecheck affected
pnpm --filter "...[HEAD^]" run typecheck
```

## Workspace-Aware Operations

### Adding Dependencies

```bash
# Turborepo (uses underlying package manager)
pnpm --filter @org/package add lodash

# Nx
nx g @nx/workspace:npm-package lodash --project=@org/package

# Lerna
lerna add lodash --scope=@org/package

# pnpm
pnpm --filter @org/package add lodash
```

### Internal Dependencies

```json
// package.json in consuming package
{
  "dependencies": {
    // Turborepo with pnpm
    "@org/shared": "workspace:*",

    // Nx
    "@org/shared": "*",

    // Lerna
    "@org/shared": "^1.0.0",

    // pnpm
    "@org/shared": "workspace:*"
  }
}
```

### Running Scripts

```bash
# All packages
turbo run build        # Turborepo
nx run-many -t build   # Nx
lerna run build        # Lerna
pnpm -r run build      # pnpm

# Single package
turbo run build --filter=@org/pkg    # Turborepo
nx run @org/pkg:build                # Nx
lerna run build --scope=@org/pkg     # Lerna
pnpm --filter @org/pkg run build     # pnpm

# Affected packages
turbo run build --filter=...[HEAD^]  # Turborepo
nx affected -t build                 # Nx
lerna run build --since=HEAD^        # Lerna
pnpm --filter "...[HEAD^]" run build # pnpm
```

## Build Optimization

### Caching Strategies

```bash
# Turborepo - Check cache hits
turbo run build --dry-run --summarize

# Nx - Cache statistics
nx reset  # Clear cache if needed
nx run-many -t build --verbose

# Force rebuild
turbo run build --force
nx run-many -t build --skip-nx-cache
```

### Parallelization

```bash
# Turborepo - Parallel by default
turbo run lint test --parallel

# Nx - Control concurrency
nx run-many -t build --parallel=5

# pnpm - Parallel execution
pnpm -r --parallel run lint
```

### CI/CD Optimization

```yaml
# GitHub Actions with Turborepo
- name: Cache turbo
  uses: actions/cache@v3
  with:
    path: .turbo
    key: turbo-${{ github.sha }}
    restore-keys: turbo-

- name: Build
  run: turbo run build --filter=...[origin/main]
```

## Tool Detection

```bash
# Detect which tool is configured
detect_monorepo_tool() {
  if [ -f "turbo.json" ]; then
    echo "turborepo"
  elif [ -f "nx.json" ]; then
    echo "nx"
  elif [ -f "lerna.json" ]; then
    echo "lerna"
  elif [ -f "pnpm-workspace.yaml" ]; then
    echo "pnpm"
  else
    echo "unknown"
  fi
}

detect_monorepo_tool
```

## Common Patterns

### Pattern: Affected Testing

```bash
# Turborepo
turbo run test --filter=...[HEAD^]

# Nx
nx affected -t test

# Lerna
lerna run test --since=HEAD^

# pnpm
pnpm --filter "...[HEAD^]" run test
```

### Pattern: Clean Build

```bash
# Turborepo
turbo run build --force

# Nx
nx reset && nx run-many -t build

# Lerna
lerna clean && lerna run build

# pnpm
pnpm -r exec rm -rf dist && pnpm -r run build
```

### Pattern: Release Workflow

```bash
# Turborepo + Changesets
pnpm changeset
pnpm changeset version
turbo run build
pnpm changeset publish

# Nx
nx release

# Lerna
lerna version
lerna publish
```

## Troubleshooting

### Issue: Cache Not Working

```bash
# Turborepo
turbo run build --summarize  # Check cache status
turbo run build --force       # Bypass cache

# Nx
nx reset                      # Clear cache
nx run @org/pkg:build --skip-nx-cache
```

### Issue: Wrong Dependency Order

```bash
# Visualize graph
turbo run build --graph
nx graph

# Check task configuration
cat turbo.json | grep -A5 "dependsOn"
cat nx.json | grep -A5 "dependsOn"
```

### Issue: Affected Detection Wrong

```bash
# Check base ref
turbo run build --filter=...[main] --dry-run
nx affected --base=main --print-affected

# Check if files are ignored
cat .gitignore | grep -v "^#"
```

## Quick Reference Card

| Action | Turborepo | Nx | pnpm |
|--------|-----------|-----|------|
| Build all | `turbo run build` | `nx run-many -t build` | `pnpm -r run build` |
| Build one | `turbo run build --filter=pkg` | `nx run pkg:build` | `pnpm --filter pkg build` |
| Build affected | `turbo run build --filter=...[HEAD^]` | `nx affected -t build` | `pnpm --filter "...[HEAD^]" build` |
| View graph | `turbo run build --graph` | `nx graph` | N/A |
| Clear cache | `rm -rf .turbo` | `nx reset` | N/A |
| Force build | `turbo run build --force` | `nx run-many -t build --skip-nx-cache` | N/A |
