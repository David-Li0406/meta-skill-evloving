---
name: monorepo-management
description: Design, operate, and evolve a Turborepo-based TypeScript monorepo using pnpm workspaces and Biome for linting and formatting. Optimized for real-time applications, shared contracts, and long-lived fullstack projects.
---

# Monorepo Management (Turborepo + pnpm + Biome)

Build a **clean, fast, and maintainable monorepo** that supports backend, frontend,
and shared packages with minimal friction and maximum clarity.

This skill assumes **Turborepo is the chosen tool** and does not re-evaluate
alternatives.

## When to Use This Skill

Use this skill when you need to:

- Set up a new **Turborepo-based monorepo**
- Manage backend + frontend + shared packages
- Optimize local development speed
- Define build, test, and dev pipelines
- Enforce consistent formatting and linting with **Biome**
- Manage shared TypeScript configuration
- Debug dependency or task orchestration issues

## Core Principles

- **Clarity over cleverness**
- **Explicit pipelines over magic**
- **Shared code must earn its place**
- **Local development speed > CI optimization**
- **One tool per concern**
  - Turborepo → task orchestration & caching
  - pnpm → dependency management
  - Biome → linting + formatting
  - TypeScript → type safety

## Tooling Stack (FIXED)

- **Monorepo**: Turborepo
- **Package manager**: pnpm workspaces
- **Language**: TypeScript
- **Lint + Format**: Biome
- **Build outputs**: per-package (`dist/`, `.next/`, etc.)

No ESLint.  
No Prettier.  
No Nx.

## Tooling Constraints

- Turborepo is mandatory
- Biome replaces ESLint + Prettier
- No duplicated tooling per package

## Reference Monorepo Structure

```txt
apps/
├── backend/
├── frontend/

packages/
├── domain/        # Pure domain logic (no frameworks)
├── contracts/     # API + realtime contracts
├── config/        # Shared tooling config (biome, tsconfig)
├── tsconfig/      # Base TS configs

docs/

turbo.json
package.json
pnpm-workspace.yaml
biome.json
```

## pnpm Workspace Setup

`pnpm-workspace.yaml`

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

Root `packages.json`

```json
{
  "name": "game-monorepo",
  "private": true,
  "packageManager": "pnpm@9",
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "format": "biome format .",
    "check": "biome check ."
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^5.4.0",
    "@biomejs/biome": "^1.7.0"
  }
}
```

## Turborepo Pipeline Design

`turbo.json`

```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": []
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### Pipeline Rules

- Shared packages build before apps
- `dev` is **never cached**
- `lint` and `check` are fast and uncached
- Avoid clever input overrides unless proven necessary

## Biome Configuration (Single Source of Truth)

Root `biome.json`

```json
{
  "$schema": "https://biomejs.dev/schemas/1.7.0/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "asNeeded"
    }
  }
}
```

### Package-Level Usage

Each package defines:

```json
{
  "scripts": {
    "lint": "biome check src",
    "format": "biome format src"
  }
}
```

No per-package ESLint configs.
No duplicated formatting rules.

## Shared TypeScripts Configuration

`packages/tsconfig/base.json`

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "skipLibCheck": true,
    "noEmit": true
  }
}
```

Apps and packages extend from this base.

## Code Sharing Rules

`packages/domain`

- Pure TypeScript
- No Node, no frameworks imports
- Used by backend only (initially)
- Rich domain models, not DTOs

`packages/contracts`

- API schemas
- Realtime event payloads
- Shared between backend and frontend
- Versioned carefully

### Golden Rule

> If a package is hard to explain, it does not belong in `packages/`

## Dependency Management (pnpm)

### Install dependencies

```bash
pnpm add zod --filter apps/backend
pnpm add @repo/contracts --filter apps/frontend
pnpm add -D ts-node -w
```

### Run tasks

```bash
pnpm turbo run build
pnpm turbo run dev
pnpm --filter apps/backend dev
```

## Build & Performance Guidelines

- Avoid unnecessary shared packages
- Avoid deep dependency chains
- Prefer duplication over premature abstraction
- Measure before optimizing cache inputs

## Best Practices

1. Keep pipelines minimal
2. Centralize tooling configs
3. Avoid circular dependencies
4. Use Biome everywhere
5. Prefer explicit scripts
6. Keep shared code intentional
7. Document package responsabilities

## Common Pitfalls

- Over-sharing utilities
- Treating Turborepo as a framework
- Per-package linting rules
- CI-first optimization
- Nx-style mental models

## Final Principle

> **A monorepo is a productivity tool, not a badge of complexity.**
> If it slows you down or confuses future readers, simplify it.
