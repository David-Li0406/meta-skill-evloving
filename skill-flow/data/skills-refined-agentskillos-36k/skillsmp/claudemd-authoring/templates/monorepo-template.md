# Monorepo CLAUDE.md Template

Use this template for Nx, Turborepo, Lerna, and other monorepo projects.

---

```markdown
# [Project Name]

## Quick Reference

\`\`\`bash
# Workspace commands
[tool] run build          # Build all packages
[tool] run test           # Test all packages
[tool] run lint           # Lint all packages

# Single package
[tool] run build --filter=[package]
[tool] run test --filter=[package]

# Dependencies
[package-manager] install  # Install all deps
\`\`\`

---

## 1. Monorepo Overview

**Tool**: [Nx/Turborepo/Lerna/pnpm workspaces]
**Package Manager**: [npm/yarn/pnpm]
**Total Packages**: [N]

### Package Categories

| Category | Count | Location |
|----------|-------|----------|
| Apps | [N] | `apps/` |
| Libraries | [N] | `packages/` or `libs/` |
| Tools | [N] | `tools/` |

---

## 2. Package Inventory

### Applications

| Package | Path | Description | Port |
|---------|------|-------------|------|
| [app-1] | `apps/[name]` | [Purpose] | [Port] |
| [app-2] | `apps/[name]` | [Purpose] | [Port] |

### Libraries

| Package | Path | Description | Consumers |
|---------|------|-------------|-----------|
| [lib-1] | `packages/[name]` | [Purpose] | [apps that use it] |
| [lib-2] | `packages/[name]` | [Purpose] | [apps that use it] |

---

## 3. Dependency Graph

\`\`\`
[app-1] ──> [lib-shared] ──> [lib-utils]
[app-2] ──> [lib-shared]
            [lib-ui]
\`\`\`

### Build Order

1. `[lib-utils]` (no dependencies)
2. `[lib-shared]` (depends on utils)
3. `[app-1]`, `[app-2]` (depend on shared)

---

## 4. Development

### Setup

\`\`\`bash
git clone [repo-url]
cd [project-name]
[package-manager] install
\`\`\`

### Running Apps

\`\`\`bash
# Start specific app
[tool] run dev --filter=[app-name]

# Start multiple apps
[tool] run dev --filter=[app-1] --filter=[app-2]
\`\`\`

### Adding Packages

\`\`\`bash
# Generate new app
[tool] generate app [name]

# Generate new library
[tool] generate lib [name]
\`\`\`

---

## 5. Shared Configuration

### TypeScript

| Config | Location | Purpose |
|--------|----------|---------|
| Base | `tsconfig.base.json` | Shared compiler options |
| App | `apps/*/tsconfig.json` | App-specific settings |
| Lib | `packages/*/tsconfig.json` | Library settings |

### ESLint

| Config | Location | Purpose |
|--------|----------|---------|
| Root | `.eslintrc.js` | Base rules |
| Overrides | Per-package | Package-specific rules |

### Build

| Config | Location | Purpose |
|--------|----------|---------|
| [Tool config] | `[turbo.json/nx.json]` | Task orchestration |
| Package scripts | `package.json` | Per-package commands |

---

## 6. CI/CD

### Pipeline Stages

| Stage | Command | Scope |
|-------|---------|-------|
| Install | `[pm] install` | All |
| Lint | `[tool] run lint` | Changed |
| Test | `[tool] run test` | Changed |
| Build | `[tool] run build` | Changed + deps |

### Affected Commands

\`\`\`bash
# Only affected packages
[tool] affected --target=build
[tool] affected --target=test
\`\`\`

---

## 7. Conventions

### Package Naming

- Apps: `[prefix]-[name]`
- Libraries: `@[scope]/[name]`

### Import Paths

\`\`\`typescript
// Use workspace aliases
import { util } from '@[scope]/[lib-name]';

// Never use relative paths across packages
// ❌ import { util } from '../../packages/lib/src';
\`\`\`
```

---

## Customization Notes

- Replace `[tool]` with actual tool (nx, turbo, lerna)
- Replace `[package-manager]` with npm/yarn/pnpm
- Add tool-specific commands and configurations
- Include caching configuration if relevant
