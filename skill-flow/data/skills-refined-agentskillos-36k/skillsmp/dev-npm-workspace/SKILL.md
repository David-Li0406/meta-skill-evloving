---
name: dev-npm-workspace
description: Set up npm workspaces for monorepo architecture. Use when creating a new monorepo, migrating to workspaces, or replicating the standard workspace pattern defined in this skill. Provides complete setup with TypeScript project references, exports configuration, and cross-package dependencies.
license: Apache-2.0
compatibility: Designed for Claude Code, OpenAI Codex, and any Agent Skills compatible product
metadata:
  author: staytuned
  version: "1.0"
  category: development
---

# NPM Workspace Setup

## What is it?

A comprehensive skill for setting up npm workspaces following the standardized monorepo architecture defined here. This skill provides an interactive workflow to analyze the target repository and generate a complete workspace configuration including TypeScript project references, subpath exports, and cross-package dependency management.

## Why use it?

- **Production-ready structure**: Based on a mature monorepo layout with multiple packages
- **TypeScript-first**: Full project references with incremental builds via tsgo
- **Modern ESM**: Proper `"type": "module"` and subpath exports for tree-shaking
- **Cross-package deps**: Workspace protocol (`*`) for local package references
- **Scalable**: Supports nested package structures (e.g., `examples/ecom/backend`)
- **Private registry ready**: GitHub npm Package Registry or custom npm registry support

---

## How to use it?

> [!IMPORTANT]
> Before creating any files, you MUST complete the Requirements Gathering phase and wait for user responses.

### Phase 1: Repository Analysis (REQUIRED)

First, analyze the target repository to understand its current state:

#### Step 1.0: Auto-detect Repository State

Before asking questions, quickly scan the repo to detect what already exists. Capture:

- Root `package.json` (name, scripts, workspaces, engines, publishConfig)
- Root `tsconfig.json` (compilerOptions and paths)
- Existing `.npmrc` and registry config
- Existing packages under `src/packages/` and any `examples/` apps
- Any existing workspace config (npm/yarn/pnpm)

If the repo already has workspaces, treat this as a **migration** or **alignment** task, not a greenfield setup.

#### Step 1.1: Identify Repository Context

Ask the user:

```
Setting up npm workspaces for the current repository.

Default: Current VS Code workspace / git repo
(Auto-detected from your active workspace)

Please confirm or provide:
1. Use current repo? (Y/n, or provide different path/URL)
2. Primary language: TypeScript (default) or specify other
3. Current structure: fresh repo / existing code to migrate / adding to existing workspace

Your answers (press Enter for defaults):
```

#### Step 1.2: Determine Package Structure

Ask the user:

```
How should packages be organized?

Default: **Nested** - Packages in `src/packages/` with examples in `examples/`
(Standard pattern: src/packages/{package-name})

Options:
1. **Use default nested structure** (recommended)
2. **Custom**: Describe your preferred structure

Your choice (1 or 2, describe if custom):
```

If the auto-detect step finds an existing structure, propose a migration plan instead of forcing a rewrite.

#### Step 1.3: Define Packages

Ask the user:

```
What packages should be created?

Naming conventions:
- Library packages: Use descriptive names (e.g., core, utils, server)
- Web app packages: Use `app-*` prefix (e.g., app-dashboard, app-admin, app-landing)
- Example packages: Place in examples/ directory (e.g., examples/ecom/backend)

If packages already exist, list them and confirm whether they should stay as-is or be migrated.

For each package, provide:
- Package name (following conventions above)
- Description
- Dependencies on other workspace packages

Example:
- core: Base utilities, no dependencies
- utils: Shared utilities, depends on core
- server: HTTP server, depends on core, utils
- app-dashboard: Admin dashboard web app, depends on core, server

Your packages:
```

#### Step 1.4: Organization Scope

Ask the user:

```
What npm organization scope should be used?

Default: @your-scope (press Enter to use default)

Override with custom scope? (leave blank for default, or provide scope like @myorg):
```

#### Step 1.5: Registry Configuration

Ask the user:

```
Which npm registry will packages be published to?

Default: **GitHub Package Registry** (https://npm.pkg.github.com)

Options:
1. **Use GitHub Package Registry** (default, press Enter)
2. **Custom private registry** (provide URL)
3. **No publishing** (private packages only, no registry config)

Your choice (1, 2 with URL, or 3):
```

---

### Phase 2: Create a Detailed Plan (REQUIRED)

Before changing files, produce a plan that mirrors the standard pattern in this skill and is tailored to the target repo. Include:

- What will be created vs. updated (root `package.json`, `tsconfig.json`, `.npmrc`, package configs)
- Package list, paths, and dependency graph
- Root exports and `files` entries derived from packages
- TypeScript project reference layout
- Registry and publish configuration
- Any migrations required to align existing packages with the standard pattern

Only after the user approves the plan should file changes proceed.

### Phase 3: Generate Configuration Files

After gathering requirements, generate the following files:

#### Step 3.1: Root package.json

Create the root `package.json` with workspace configuration:

```json
{
  "name": "@{scope}/{repo-name}",
  "version": "1.0.0",
  "description": "{description}",
  "type": "module",
  "sideEffects": false,
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./{package-1}": {
      "types": "./src/packages/{package-1}/dist/index.d.ts",
      "import": "./src/packages/{package-1}/dist/index.js"
    }
  },
  "files": [
    "dist",
    "src/packages/{package-1}/dist",
    "src/packages/{package-2}/dist"
  ],
  "workspaces": [
    "src/packages/{package-1}",
    "src/packages/{package-2}",
    "examples/{example-1}"
  ],
  "scripts": {
    "build": "npm run type-check && tsgo -b .",
    "type-check": "tsgo -b . --noEmit",
    "build:all:workspaces": "npm run build --workspaces",
    "clean": "rimraf dist tsconfig.tsbuildinfo src/packages/*/.rslib src/packages/*/dist src/packages/*/tsconfig.tsbuildinfo src/packages/*/tsconfig.build.tsbuildinfo",
    "format": "prettier --write 'src/packages/**/*.{ts,js,md}'",
    "format:check": "prettier --check 'src/packages/**/*.{ts,js,md}'",
    "lint": "eslint . --ext .ts --flag unstable_native_nodejs_ts_config --cache --cache-strategy content --cache-location .eslintcache --report-unused-disable-directives --no-warn-ignored",
    "prepublishOnly": "npm run build",
    "prepare": "husky"
  },
  "lint-staged": {
    "*.ts": ["eslint --fix", "prettier --write"]
  },
  "engines": {
    "node": ">=24.11.1"
  },
  "publishConfig": {
    "registry": "https://npm.pkg.github.com"
  }
}
```

Keep `exports`, `files`, and `workspaces` in sync. This pattern uses explicit entries per package rather than wildcards to control what is published.
For a pixel-perfect match, mirror additional root scripts and devDependencies as needed for the target repo (for example, any repo-specific test commands).

#### Step 3.2: Root tsconfig.json

Create strict TypeScript configuration:

```json
{
  "compilerOptions": {
    "allowSyntheticDefaultImports": true,
    "composite": true,
    "declaration": true,
    "declarationMap": true,
    "esModuleInterop": true,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true,
    "incremental": true,
    "inlineSources": false,
    "isolatedModules": true,
    "lib": ["esnext", "DOM", "DOM.Iterable"],
    "module": "NodeNext",
    "moduleDetection": "force",
    "moduleResolution": "NodeNext",
    "newLine": "lf",
    "noEmitOnError": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitAny": true,
    "noImplicitOverride": true,
    "noImplicitThis": true,
    "noImplicitReturns": true,
    "noPropertyAccessFromIndexSignature": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "outDir": "./dist",
    "paths": {
      "*": ["./*"],
      "@{scope}/*": ["./src/packages/*/src"]
    },
    "preserveConstEnums": true,
    "removeComments": false,
    "resolveJsonModule": true,
    "rootDir": "src",
    "sourceMap": true,
    "strict": true,
    "stripInternal": false,
    "target": "esnext",
    "typeRoots": ["./node_modules/@types"],
    "types": ["node"],
    "useDefineForClassFields": true,
    "useUnknownInCatchVariables": true,
    "verbatimModuleSyntax": true,
    "noUncheckedSideEffectImports": true,
    "strictBuiltinIteratorReturn": true,
    "assumeChangesOnlyAffectDirectDependencies": true,
    "noErrorTruncation": true,
    "resolvePackageJsonExports": true,
    "resolvePackageJsonImports": true
  },
  "include": ["src/index.ts"]
}
```

#### Step 3.3: Package-level tsconfig.json

For each workspace package, create two configs:

**tsconfig.json** (development):

```json
{
  "extends": "../../../tsconfig.json",
  "compilerOptions": {
    "module": "esnext",
    "moduleResolution": "bundler",
    "outDir": "./dist",
    "rootDir": ".",
    "composite": true,
    "verbatimModuleSyntax": true,
    "paths": {}
  },
  "include": ["src/**/*", "test/**/*"]
}
```

**tsconfig.build.json** (production):

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "rootDir": "src",
    "outDir": "dist",
    "emitDeclarationOnly": false,
    "noEmit": false
  },
  "include": ["src/**/*"],
  "exclude": ["test/**/*", "**/*.test.ts"]
}
```

#### Step 3.4: Package-level package.json

For each workspace package:

```json
{
  "name": "@{scope}/{package-name}",
  "version": "1.0.0",
  "type": "module",
  "sideEffects": false,
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "exports": {
    ".": {
      "source": "./src/index.ts",
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./{submodule}": {
      "source": "./src/{submodule}/index.ts",
      "types": "./dist/{submodule}/index.d.ts",
      "import": "./dist/{submodule}/index.js"
    }
  },
  "files": ["dist"],
  "private": true,
  "scripts": {
    "build": "tsgo -p tsconfig.build.json",
    "lint": "eslint .",
    "format": "prettier --write ."
  },
  "dependencies": {
    "@{scope}/{dep-package}": "*"
  }
}
```

#### Step 3.5: .npmrc Configuration

Create `.npmrc` for registry authentication:

```ini
@{scope}:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GH_TOKEN}
```

---

### Phase 4: Create Directory Structure

Generate the complete directory structure:

```plaintext
{repo-root}/
├── package.json              # Root workspace config
├── package-lock.json         # Lock file (npm install generates)
├── tsconfig.json             # Root TypeScript config
├── .npmrc                    # Registry configuration
├── .gitignore                # Git ignores
├── .editorconfig             # Editor settings
├── .prettierrc.json          # Prettier config
├── eslint.config.ts          # ESLint config
├── src/
│   ├── index.ts              # Root re-exports (recommended, keep in sync with exports)
│   └── packages/
│       ├── {package-1}/
│       │   ├── package.json
│       │   ├── tsconfig.json
│       │   ├── tsconfig.build.json
│       │   ├── README.md
│       │   └── src/
│       │       └── index.ts
│       └── {package-2}/
│           ├── package.json
│           ├── tsconfig.json
│           ├── tsconfig.build.json
│           ├── README.md
│           └── src/
│               └── index.ts
└── examples/                  # (Optional) Example apps
    └── {example-1}/
        ├── package.json
        ├── tsconfig.json
        └── src/
            └── index.ts
```

---

### Phase 5: Initialize Workspace

Execute setup commands:

```bash
# 1. Install all dependencies (creates symlinks for workspace packages)
npm install

# 2. Build all packages in topological order
npm run build --workspaces

# 3. Verify workspace setup
npm ls --all

# 4. Run type check
npm run type-check
```

---

### Phase 6: Validation Checklist

Verify the workspace setup:

- [ ] Root `package.json` has `"workspaces"` array listing all packages
- [ ] Each package has its own `package.json` with correct `"name"`
- [ ] Package names use consistent scope: `@{scope}/{package}`
- [ ] Cross-package deps use `"*"` (workspace protocol): `"@scope/other": "*"`
- [ ] All packages have `"type": "module"` for ESM
- [ ] Each package has proper `"exports"` with types and import conditions
- [ ] Root and package `tsconfig.json` files are properly linked via `extends`
- [ ] Build scripts work: `npm run build --workspaces`
- [ ] `.npmrc` is configured for the target registry
- [ ] `npm ls` shows no missing or invalid dependencies

---

## Examples

### Example 1: Minimal 3-Package Setup

```bash
# Create a new repo with core, utils, and server packages

# 1. Initialize root
npm init -y
npm pkg set type="module"
npm pkg set workspaces='["src/packages/core", "src/packages/utils", "src/packages/server"]'

# 2. Create package directories
mkdir -p src/packages/{core,utils,server}/src

# 3. Initialize each package
cd src/packages/core && npm init -y && npm pkg set name="@scope/core" type="module"
cd ../utils && npm init -y && npm pkg set name="@scope/utils" type="module"
cd ../server && npm init -y && npm pkg set name="@scope/server" type="module"

# 4. Add cross-package dependency
npm pkg set dependencies.@scope/core="*" dependencies.@scope/utils="*"

# 5. Install from root
cd ../../../
npm install
```

### Example 2: Reference Workspace Setup

Use the templates in `templates/` as the canonical reference for configuration structure and placeholders.

---

## Supporting References

- [workspace-architecture.md](references/workspace-architecture.md) - Deep dive into monorepo patterns
- [exports-guide.md](references/exports-guide.md) - Subpath exports configuration
- [typescript-project-refs.md](references/typescript-project-refs.md) - TypeScript project references
- [templates/](templates/) - Ready-to-use configuration templates

---

## Troubleshooting

### Common Issues

| Issue                          | Solution                                                    |
| ------------------------------ | ----------------------------------------------------------- |
| `ERESOLVE unable to resolve`   | Run `npm install --force` or check workspace configurations |
| Package not found in workspace | Ensure package is listed in root `workspaces` array         |
| TypeScript can't find module   | Check `paths` in tsconfig and package `exports`             |
| Circular dependency            | Restructure packages or use interface-based injection       |
| Build order wrong              | npm workspaces builds in topological order automatically    |

### Debugging Commands

```bash
# Show workspace structure
npm ls --all

# Explain a package resolution
npm explain @scope/package-name

# Check for issues
npm doctor

# Clean rebuild
npm run clean && npm install && npm run build --workspaces
```

---

## Limitations

- npm workspaces require npm 7+ (Node.js 15+)
- Circular dependencies between packages are not supported
- Private packages need registry authentication for CI/CD
- Some edge cases may require explicit peer dependencies
