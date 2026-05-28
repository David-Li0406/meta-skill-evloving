# Workspace Configuration Reference

Detailed information about workspace configurations, monorepo tools, and dependency protocols.

## Table of Contents

1. [Workspace Configuration Formats](#workspace-configuration-formats)
2. [Workspace Protocols](#workspace-protocols)
3. [Monorepo Tools](#monorepo-tools)
4. [Workspace Discovery](#workspace-discovery)
5. [Cross-Workspace Dependencies](#cross-workspace-dependencies)

---

## Workspace Configuration Formats

### npm Workspaces (npm 7+)

**Configuration in package.json:**
```json
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}
```

**With exclusions:**
```json
{
  "workspaces": [
    "packages/*",
    "!packages/excluded"
  ]
}
```

**Features:**
- Glob pattern support
- Shared node_modules at root
- Hoisting of common dependencies
- Cross-workspace linking

**Limitations:**
- Basic filtering capabilities
- No built-in parallelization
- Limited monorepo-specific features

---

### Yarn Workspaces

**Yarn v1 configuration in package.json:**
```json
{
  "private": true,
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}
```

**Yarn Berry (v2+) configuration in package.json:**
```json
{
  "private": true,
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}
```

**Additional Berry features in .yarnrc.yml:**
```yaml
nodeLinker: pnp

# Enable workspace tools
plugins:
  - path: .yarn/plugins/@yarnpkg/plugin-workspace-tools.cjs

# Constraints
enableConstraintsChecks: true
```

**Constraints file (constraints.pro):**
```prolog
% Enforce consistent dependency versions
gen_enforced_dependency(WorkspaceCwd, DependencyIdent, DependencyRange, DependencyType) :-
  workspace_has_dependency(WorkspaceCwd, DependencyIdent, DependencyRange, DependencyType).
```

**Features:**
- Workspace protocol
- Plug'n'Play mode (Berry)
- Constraints system (Berry)
- Advanced filtering (Berry)

---

### pnpm Workspaces

**Configuration in pnpm-workspace.yaml:**
```yaml
packages:
  - 'packages/*'
  - 'apps/*'
  - 'tools/*'
  # Exclude patterns
  - '!**/test/**'
  - '!**/__tests__/**'
```

**Additional configuration in package.json:**
```json
{
  "pnpm": {
    "overrides": {
      "lodash": "^4.17.21"
    },
    "packageExtensions": {
      "react": {
        "peerDependencies": {
          "react-dom": "*"
        }
      }
    }
  }
}
```

**Catalogs (pnpm 8+) in package.json:**
```json
{
  "pnpm": {
    "catalogs": {
      "default": {
        "react": "^18.2.0",
        "typescript": "^5.0.0"
      },
      "backend": {
        "express": "^4.18.0",
        "fastify": "^4.0.0"
      }
    }
  }
}
```

**Features:**
- Efficient disk usage
- Strict dependency isolation
- Advanced filtering
- Catalog support for version management
- Workspace protocol with ranges

---

### Bun Workspaces

**Configuration in package.json:**
```json
{
  "name": "my-monorepo",
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}
```

**Features:**
- Compatible with npm/yarn workspace format
- Fast installation
- Limited advanced features (still evolving)

---

## Workspace Protocols

Workspace protocols allow packages to reference other packages in the same workspace.

### pnpm Workspace Protocol

**Syntax:**
```json
{
  "dependencies": {
    "@myorg/utils": "workspace:*",      // Any version in workspace
    "@myorg/core": "workspace:^",       // Semver caret (^x.y.z)
    "@myorg/shared": "workspace:~",     // Semver tilde (~x.y.z)
    "@myorg/types": "workspace:^1.0.0"  // Specific semver range
  }
}
```

**Resolution:**
- `workspace:*` → Links to workspace package, any version
- `workspace:^` → Converts to `^x.y.z` in published package
- `workspace:~` → Converts to `~x.y.z` in published package
- `workspace:^1.0.0` → Validates version matches range

**Publishing behavior:**
- `workspace:*` → Replaced with actual version on publish
- `workspace:^` → Replaced with `^x.y.z` on publish

---

### Yarn Workspace Protocol

**Syntax (Yarn Berry):**
```json
{
  "dependencies": {
    "@myorg/utils": "workspace:*",
    "@myorg/core": "workspace:^",
    "@myorg/shared": "workspace:~"
  }
}
```

**Features:**
- Similar to pnpm workspace protocol
- Supported in Yarn v2+
- Not available in Yarn v1

---

### npm/Yarn v1 Workspace References

**npm and Yarn v1 use implicit workspace resolution:**
```json
{
  "dependencies": {
    "@myorg/utils": "1.0.0"  // Resolved from workspace if available
  }
}
```

**Explicit file protocol:**
```json
{
  "dependencies": {
    "@myorg/utils": "file:../utils"  // Explicit local reference
  }
}
```

---

## Monorepo Tools

### Turborepo

**Detection:**
- `turbo.json` file present

**Configuration (turbo.json):**
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
    "dev": {
      "cache": false
    }
  }
}
```

**Running commands:**
```bash
turbo run build                      # Run build with caching
turbo run test --filter=web          # Run test in 'web' package
turbo run build --filter=...web      # Build web and its dependencies
turbo run lint --no-cache            # Skip cache
```

**Key features:**
- Incremental builds with caching
- Parallel execution
- Dependency graph awareness
- Remote caching support
- Works with any package manager

**Filter syntax:**
```bash
--filter=web                         # Specific package
--filter=@myorg/*                    # All packages in scope
--filter=...web                      # Package and dependencies
--filter=web...                      # Package and dependents
--filter=[origin/main]               # Changed since git ref
```

---

### Nx

**Detection:**
- `nx.json` file present
- `workspace.json` or project.json files

**Configuration (nx.json):**
```json
{
  "tasksRunnerOptions": {
    "default": {
      "runner": "nx/tasks-runners/default",
      "options": {
        "cacheableOperations": ["build", "test", "lint"]
      }
    }
  },
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
```

**Project configuration (project.json):**
```json
{
  "name": "web",
  "targets": {
    "build": {
      "executor": "@nx/vite:build",
      "outputs": ["{projectRoot}/dist"]
    },
    "test": {
      "executor": "@nx/jest:jest"
    }
  }
}
```

**Running commands:**
```bash
nx run web:build                     # Run build target for web project
nx run-many --target=build           # Run build for all projects
nx run-many --target=test --all      # Run test for all projects
nx affected --target=build           # Build only affected projects
nx affected --target=test --base=main # Test changed since main
```

**Key features:**
- Task orchestration and caching
- Code generation
- Dependency graph visualization
- Affected command for incremental builds
- Plugin ecosystem
- Distributed task execution

---

### Lerna

**Detection:**
- `lerna.json` file present

**Configuration (lerna.json):**
```json
{
  "version": "independent",
  "npmClient": "pnpm",
  "command": {
    "publish": {
      "conventionalCommits": true
    }
  },
  "packages": [
    "packages/*"
  ]
}
```

**Running commands:**
```bash
lerna run build                      # Run build in all packages
lerna run test --scope=web           # Run test in 'web' package
lerna run lint --since origin/main   # Run lint in changed packages
lerna run build --stream             # Stream output
```

**Key features:**
- Version management
- Publishing coordination
- Conventional commits
- Workspace command execution
- Often used with npm/yarn/pnpm

**Note:** Lerna development slowed; many features now in package managers. Nx has taken over Lerna maintenance.

---

## Workspace Discovery

### Finding Workspace Packages

**1. Parse workspace configuration:**

For pnpm:
```bash
# Read pnpm-workspace.yaml
packages:
  - 'packages/*'
  - 'apps/*'
```

For npm/yarn/bun:
```bash
# Read package.json workspaces field
{
  "workspaces": ["packages/*", "apps/*"]
}
```

**2. Use Glob tool to find package.json files:**
```bash
# Based on patterns found
packages/*/package.json
apps/*/package.json
```

**3. Read each package.json for metadata:**
```json
{
  "name": "@myorg/utils",
  "version": "1.0.0",
  "scripts": { ... },
  "dependencies": { ... }
}
```

---

### Workspace Structure Example

```
monorepo/
├── package.json              # Root package.json with workspaces
├── pnpm-workspace.yaml       # pnpm workspace config
├── turbo.json                # Turborepo config
├── packages/
│   ├── utils/
│   │   ├── package.json      # @myorg/utils
│   │   └── src/
│   ├── core/
│   │   ├── package.json      # @myorg/core
│   │   └── src/
│   └── types/
│       ├── package.json      # @myorg/types
│       └── src/
└── apps/
    ├── web/
    │   ├── package.json      # @myorg/web
    │   └── src/
    └── api/
        ├── package.json      # @myorg/api
        └── src/
```

---

## Cross-Workspace Dependencies

### Dependency Graph Analysis

**Example workspace dependencies:**

```
@myorg/web
  ├─ @myorg/utils (workspace)
  ├─ @myorg/core (workspace)
  │  └─ @myorg/utils (workspace)
  └─ react (external)

@myorg/api
  ├─ @myorg/utils (workspace)
  ├─ @myorg/types (workspace)
  └─ express (external)
```

### Topological Ordering

When running commands across workspaces, some tools respect dependency order:

**Yarn Berry:**
```bash
yarn workspaces foreach -pt build   # Parallel with topological order
```

**pnpm:**
```bash
pnpm -r build                       # Respects dependency order by default
```

**Turborepo:**
```bash
turbo run build                     # Uses dependency graph automatically
```

**Nx:**
```bash
nx run-many --target=build          # Respects task dependencies
```

### Build Order Example

For the dependency graph above:

1. `@myorg/utils` (no dependencies)
2. `@myorg/types` (no dependencies)
3. `@myorg/core` (depends on utils)
4. `@myorg/web` and `@myorg/api` (parallel, both depend on built packages)

---

## Common Workspace Patterns

### Shared Configuration Packages

```
packages/
├── eslint-config/
│   ├── package.json
│   └── index.js
├── tsconfig/
│   ├── package.json
│   ├── base.json
│   └── nextjs.json
```

Usage:
```json
{
  "extends": "@myorg/tsconfig/base.json"
}
```

### Internal Tools

```
tools/
├── scripts/
│   ├── package.json
│   └── build-utils.ts
```

### Workspace Naming Conventions

**Scoped packages:**
```
@myorg/utils
@myorg/core
@myorg/web
```

**Benefits:**
- Clear ownership
- Namespace separation
- npm organization support

---

## Best Practices

### Workspace Organization

1. **Group by type:**
   - `packages/` - Shared libraries
   - `apps/` - Applications
   - `tools/` - Internal tooling

2. **Consistent naming:**
   - Use scoped packages (`@myorg/name`)
   - Descriptive names

3. **Dependency management:**
   - Use workspace protocol
   - Pin external dependencies at root
   - Share common dependencies

### Version Management

**Independent versioning:**
```json
// lerna.json
{
  "version": "independent"
}
```

**Fixed versioning:**
```json
{
  "version": "1.0.0"
}
```

### Publishing

**Private workspaces:**
```json
{
  "private": true  // Won't be published
}
```

**Public packages:**
```json
{
  "name": "@myorg/utils",
  "version": "1.0.0",
  "publishConfig": {
    "access": "public"
  }
}
```
