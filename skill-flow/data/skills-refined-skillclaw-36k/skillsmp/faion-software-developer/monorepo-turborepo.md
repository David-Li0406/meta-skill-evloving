---
id: monorepo-turborepo
name: "Monorepo Setup (Turborepo)"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Monorepo Setup (Turborepo)

## Overview

Turborepo is a high-performance build system for JavaScript/TypeScript monorepos. It provides intelligent caching, parallel execution, and incremental builds. This methodology covers setup, configuration, and best practices for scalable monorepo architecture.

## When to Use

- Multiple related packages/applications
- Shared code between projects
- Teams needing consistent tooling
- Projects requiring fast CI builds
- Microservices with shared libraries

## Key Principles

1. **Remote caching** - Never rebuild the same code twice
2. **Parallel execution** - Run independent tasks concurrently
3. **Incremental builds** - Only rebuild what changed
4. **Task pipelines** - Define task dependencies
5. **Workspace conventions** - Consistent structure across packages

## Best Practices

### Project Structure

```
monorepo/
├── turbo.json              # Turborepo configuration
├── package.json            # Root package.json
├── pnpm-workspace.yaml     # pnpm workspace config
├── pnpm-lock.yaml
├── .gitignore
│
├── apps/                   # Applications
│   ├── web/               # Next.js frontend
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── src/
│   │
│   ├── api/               # Backend API
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── src/
│   │
│   └── docs/              # Documentation site
│       ├── package.json
│       └── src/
│
├── packages/              # Shared packages
│   ├── ui/               # Shared UI components
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── src/
│   │
│   ├── config/           # Shared configs (eslint, tsconfig)
│   │   ├── package.json
│   │   ├── eslint-preset.js
│   │   └── tsconfig/
│   │
│   ├── types/            # Shared TypeScript types
│   │   ├── package.json
│   │   └── src/
│   │
│   └── utils/            # Shared utilities
│       ├── package.json
│       └── src/
│
└── tools/                # Build tools & scripts
    └── scripts/
```

### Turborepo Configuration

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "typecheck": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "clean": {
      "cache": false
    }
  }
}
```

### Root Package.json

```json
// package.json
{
  "name": "monorepo",
  "private": true,
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint",
    "test": "turbo test",
    "typecheck": "turbo typecheck",
    "clean": "turbo clean",
    "format": "prettier --write \"**/*.{ts,tsx,md}\""
  },
  "devDependencies": {
    "turbo": "^1.12.0",
    "prettier": "^3.2.0"
  },
  "packageManager": "pnpm@8.14.0",
  "engines": {
    "node": ">=18.0.0"
  }
}
```

### Workspace Configuration

```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'
  - 'tools/*'
```

### Shared TypeScript Config

```json
// packages/config/tsconfig/base.json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  }
}

// packages/config/tsconfig/nextjs.json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "extends": "./base.json",
  "compilerOptions": {
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "preserve",
    "noEmit": true,
    "incremental": true,
    "plugins": [{ "name": "next" }]
  }
}

// packages/config/tsconfig/library.json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "extends": "./base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

### App Package Configuration

```json
// apps/web/package.json
{
  "name": "@monorepo/web",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@monorepo/ui": "workspace:*",
    "@monorepo/utils": "workspace:*",
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "devDependencies": {
    "@monorepo/config": "workspace:*",
    "@types/react": "^18.0.0",
    "typescript": "^5.3.0"
  }
}

// apps/web/tsconfig.json
{
  "extends": "@monorepo/config/tsconfig/nextjs.json",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### Library Package Configuration

```json
// packages/ui/package.json
{
  "name": "@monorepo/ui",
  "version": "0.0.0",
  "private": true,
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./button": {
      "import": "./dist/button.mjs",
      "require": "./dist/button.js",
      "types": "./dist/button.d.ts"
    }
  },
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts",
    "dev": "tsup src/index.ts --format cjs,esm --dts --watch",
    "lint": "eslint src/",
    "typecheck": "tsc --noEmit",
    "clean": "rm -rf dist"
  },
  "dependencies": {
    "class-variance-authority": "^0.7.0"
  },
  "peerDependencies": {
    "react": "^18.0.0"
  },
  "devDependencies": {
    "@monorepo/config": "workspace:*",
    "@types/react": "^18.0.0",
    "react": "^18.0.0",
    "tsup": "^8.0.0",
    "typescript": "^5.3.0"
  }
}

// packages/ui/tsconfig.json
{
  "extends": "@monorepo/config/tsconfig/library.json",
  "compilerOptions": {
    "jsx": "react-jsx",
    "lib": ["ES2022", "DOM"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Shared ESLint Config

```javascript
// packages/config/eslint-preset.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-type-checked',
    'prettier',
  ],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  rules: {
    '@typescript-eslint/no-unused-vars': [
      'error',
      { argsIgnorePattern: '^_' },
    ],
    '@typescript-eslint/consistent-type-imports': [
      'warn',
      { prefer: 'type-imports' },
    ],
  },
  ignorePatterns: ['dist', 'node_modules', '.turbo'],
};
```

### Running Commands

```bash
# Build all packages
pnpm build
# or
turbo build

# Build specific package
turbo build --filter=@monorepo/web

# Build package and dependencies
turbo build --filter=@monorepo/web...

# Run dev for multiple apps
turbo dev --filter=@monorepo/web --filter=@monorepo/api

# Dry run to see what would run
turbo build --dry-run

# Run with cache disabled
turbo build --force

# Run with verbose output
turbo build --verbosity=2
```

### Remote Caching

```bash
# Login to Vercel (for remote cache)
turbo login

# Link to Vercel project
turbo link

# Or use self-hosted cache
# turbo.json
{
  "remoteCache": {
    "signature": true
  }
}

# Set environment variables for custom cache
export TURBO_API=https://cache.example.com
export TURBO_TOKEN=your_token
export TURBO_TEAM=your_team
```

### CI/CD Configuration

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

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm build

      - name: Lint
        run: pnpm lint

      - name: Test
        run: pnpm test

      - name: Type Check
        run: pnpm typecheck
```

## Anti-patterns

### Avoid: Circular Dependencies

```json
// BAD - packages depend on each other
// packages/a depends on packages/b
// packages/b depends on packages/a

// GOOD - extract shared code
// packages/shared (no deps)
// packages/a depends on shared
// packages/b depends on shared
```

### Avoid: Missing Task Dependencies

```json
// BAD - typecheck might run before build
{
  "pipeline": {
    "typecheck": {}
  }
}

// GOOD - explicit dependencies
{
  "pipeline": {
    "typecheck": {
      "dependsOn": ["^build"]
    }
  }
}
```

### Avoid: Caching Non-Deterministic Tasks

```json
// BAD - dev server cached
{
  "pipeline": {
    "dev": {
      "outputs": []
    }
  }
}

// GOOD - disable cache for dev
{
  "pipeline": {
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

## References

- [Turborepo Documentation](https://turbo.build/repo/docs)
- [Turborepo Examples](https://github.com/vercel/turbo/tree/main/examples)
- [Monorepo Tools](https://monorepo.tools/)
- [pnpm Workspaces](https://pnpm.io/workspaces)
