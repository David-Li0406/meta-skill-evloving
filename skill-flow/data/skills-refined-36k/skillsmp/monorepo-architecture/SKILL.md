---
name: Monorepo Architecture
description: Turborepo configuration, pnpm workspaces, and internal packages management for Lumira V2.
---

# Monorepo Architecture

## Context

Lumira V2 is a **Turborepo** monorepo managed by **pnpm 8.15.4**.

```
lumira-monorepo/
├── apps/
│   ├── api/          # NestJS 10 backend
│   └── web/          # Next.js 14 frontend
├── packages/
│   ├── config/       # Shared ESLint, TypeScript configs
│   ├── database/     # Prisma schema & generated client
│   ├── shared/       # Shared types, utils, constants
│   └── ui/           # Shared React components
├── turbo.json        # Pipeline configuration
├── pnpm-workspace.yaml
└── package.json      # Root scripts
```

---

## Core Principles

1. **Single Version Policy**: All apps use the same dependency versions.
2. **Internal Packages**: Use `@packages/*` aliases for cross-app sharing.
3. **Task Caching**: Turbo caches builds for unchanged packages.

---

## Configuration Files

### `turbo.json` Pipeline

```json
{
  "tasks": {
    "build": { "dependsOn": ["^build"], "outputs": [".next/**", "dist/**"] },
    "dev": { "cache": false, "persistent": true },
    "db:generate": { "cache": false },
    "test": { "dependsOn": ["build"] }
  }
}
```

### `pnpm-workspace.yaml`

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

---

## Common Commands

```bash
# Development (all apps)
pnpm dev

# Build all
pnpm build

# Run specific app
pnpm --filter web dev
pnpm --filter api dev

# Add dependency to specific package
pnpm --filter @packages/ui add framer-motion

# Run task for specific app
turbo run build --filter=web
```

---

## Internal Package Usage

### Importing from `@packages/database`

```typescript
import { prisma, User, Mission } from '@packages/database';
```

### Importing from `@packages/ui`

```typescript
import { Button, Card, Input } from '@packages/ui';
```

### Importing from `@packages/shared`

```typescript
import { BRAND_CONFIG, formatDate } from '@packages/shared';
```

---

## Best Practices

- **Never** use relative paths to import from other workspaces.
- **Always** declare internal dependencies in each package's `package.json`.
- **Avoid** circular dependencies between packages.
- **Use** `turbo prune` in Dockerfiles to isolate app dependencies.
