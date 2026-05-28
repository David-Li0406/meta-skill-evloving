---
name: turborepo
description: Use this skill when configuring tasks, workflows, and pipelines in a Turborepo monorepo setup, including managing dependencies, caching, and CI optimization.
---

# Turborepo Skill

Build system for JavaScript/TypeScript monorepos. Turborepo caches task outputs and runs tasks in parallel based on the dependency graph.

## IMPORTANT: Package Tasks, Not Root Tasks

**DO NOT create Root Tasks. ALWAYS create package tasks.**

When creating tasks/scripts/pipelines, you MUST:

1. Add the script to each relevant package's `package.json`.
2. Register the task in the root `turbo.json`.
3. The root `package.json` only delegates via `turbo run <task>`.

**DO NOT** put task logic in the root `package.json`. This defeats Turborepo's parallelization.

```json
// DO THIS: Scripts in each package
// apps/web/package.json
{ "scripts": { "build": "next build", "lint": "eslint .", "test": "vitest" } }

// apps/api/package.json
{ "scripts": { "build": "tsc", "lint": "eslint .", "test": "vitest" } }

// packages/ui/package.json
{ "scripts": { "build": "tsc", "lint": "eslint .", "test": "vitest" } }
```

```json
// turbo.json - register tasks
{
  "tasks": {
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**"] },
    "lint": {},
    "test": { "dependsOn": ["build"] }
  }
}
```

```json
// Root package.json - ONLY delegates, no task logic
{
  "scripts": {
    "build": "turbo run build",
    "lint": "turbo run lint",
    "test": "turbo run test"
  }
}
```

```json
// DO NOT DO THIS - defeats parallelization
// Root package.json
{
  "scripts": {
    "build": "cd apps/web && next build && cd ../api && tsc",
    "lint": "eslint apps/ packages/",
    "test": "vitest"
  }
}
```

Root Tasks (`//#taskname`) are ONLY for tasks that truly cannot exist in packages (rare).

## Secondary Rule: `turbo run` vs `turbo`

**Always use `turbo run` when the command is written into code:**

```json
// package.json - ALWAYS "turbo run"
{
  "scripts": {
    "build": "turbo run build"
  }
}
```

```yaml
# CI workflows - ALWAYS "turbo run"
- run: turbo run build --affected
```

**The shorthand `turbo <tasks>` is ONLY for one-off terminal commands** typed directly by humans or agents. Never write `turbo build` into package.json, CI, or scripts.

## Quick Decision Trees

### "I need to configure a task"

```
Configure a task?
├─ Define task dependencies → references/configuration/tasks.md
├─ Lint/check-types (parallel + caching) → Use Transit Nodes pattern (see below)
├─ Specify build outputs → references/configuration/tasks.md#outputs
├─ Handle environment variables → references/environment/README.md
├─ Set up dev/watch tasks → references/configuration/tasks.md#persistent
├─ Package-specific config → references/configuration/README.md#package-configurations
└─ Global settings (cacheDir, daemon) → references/configuration/global-options.md
```

### "My cache isn't working"

```
Cache problems?
├─ Tasks run but outputs not restored → Missing `outputs` key
├─ Cache misses unexpectedly → references/caching/gotchas.md
├─ Need to debug hash inputs → Use --summarize or --dry
├─ Want to skip cache entirely → Use --force or cache: false
├─ Remote cache not working → references/caching/remote-cache.md
└─ Environment causing misses → references/environment/gotchas.md
```

### "I want to run only changed packages"

```
Run only what changed?
├─ Changed packages + dependents (RECOMMENDED) → turbo run build --affected
├─ Custom base branch → --affected --affected-base=origin/develop
├─ Manual git comparison → --filter=...[origin/main]
└─ See all filter options → references/filtering/README.md
```

**`--affected` is the primary way to run only changed packages.** It automatically compares against the default branch and includes dependents.

### "I want to filter packages"

```
Filter packages?
├─ Only changed packages → --affected (see above)
├─ By package name → --filter=web
├─ By directory → --filter=./apps/*
├─ Package + dependencies → --filter=web...
├─ Package + dependents → --filter=...web
└─ Complex combinations → references/filtering/patterns.md
```

### "Environment variables aren't working"

```
Environment issues?
├─ Vars not available at runtime → Strict mode filtering (default)
├─ Cache hits with wrong env → Var not in `env` key
├─ .env changes not causing rebuilds → .env not in `inputs`
├─ CI variables missing → references/environment/gotchas.md
└─ Framework vars (NEXT_PUBLIC_*) → Auto-included via inference
```

### "I need to set up CI"

```
CI setup?
├─ GitHub Actions → references/ci/github-actions.md
├─ Vercel deployment → references/ci/vercel.md
├─ Remote cache in CI → references/caching/remote-cache.md
├─ Only build changed packages → --affected flag
├─ Skip unnecessary builds → turbo-ignore (references/cli/commands.md)
└─ Skip container setup when no changes → turbo-ignore
```

### "I want to watch for changes during development"

```
Watch mode?
├─ Re-run tasks on change → turbo watch (references/watch/README.md)
├─ Dev servers with dependencies → Use `with` key (references/configuration/tasks.md#with)
├─ Restart dev server on dep change → Use `interruptible: true`
└─ Persistent dev tasks → Use `persistent: true`
```

### "I need to create/structure a package"

```
Package creation/structure?
├─ Create an internal package → references/best-practices/packages.md
├─ Repository structure → references/best-practices/structure.md
├─ Dependency management → references/best-practices/dependencies.md
├─ Best practices overview → references/best-practices/README.md
├─ JIT vs Compiled packages → references/best-practices/packages.md#compilation-strategies
└─ Sharing code between apps → references/best-practices/README.md#package-types
```

### "How should I structure my monorepo?"

```
Monorepo structure?
├─ Standard layout (apps/, packages/) → references/best-practices/README.md
├─ Package types (apps vs libraries) → references/best-practices/README.md#package-types
├─ Creating internal packages → references/best-practices/packages.md
├─ TypeScript configuration → references/best-practices/structure.md#typescript-configuration
├─ ESLint configuration → references/best-practices/structure.md#eslint-configuration
├─ Dependency management → references/best-practices/dependencies.md
└─ Enforce package boundaries → references/boundaries/README.md
```

### "I want to enforce architectural boundaries"

```
Enforce boundaries?
├─ Check for violations → turbo boundaries
├─ Tag packages → references/boundaries/README.md#tags
├─ Restrict which packages can import others → references/boundaries/README.md#rule-types
└─ Prevent cross-package file imports → references/boundaries/README.md
```

## Critical Anti-Patterns

### Using `turbo` Shorthand in Code

**`turbo run` is recommended in package.json scripts and CI pipelines.** The shorthand `turbo <task>` is intended for interactive terminal use.

```json
// WRONG - using shorthand in package.json
{
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev"
  }
}

// CORRECT
{
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev"
  }
}
```

```yaml
# WRONG - using shorthand in CI
- run: turbo build --affected

# CORRECT
- run: turbo run build --affected
```

### Root Scripts Bypassing Turbo

Root `package.json` scripts MUST delegate to `turbo run`, not run tasks directly.

```json
// WRONG - bypasses turbo entirely
{
  "scripts": {
    "build": "bun build",
    "dev": "bun dev"
  }
}

// CORRECT - delegates to turbo
{
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev"
  }
}
```

### Using `&&` to Chain Turbo Tasks

Don't chain turbo tasks with `&&`. Let turbo orchestrate.

```json
// WRONG - turbo task not using turbo run
{
  "scripts": {
    "changeset:publish": "bun build && changeset publish"
  }
}

// CORRECT
{
  "scripts": {
    "changeset:publish": "turbo run build && changeset publish"
  }
}
```

### `prebuild` Scripts That Manually Build Dependencies

Scripts like `prebuild` that manually build other packages bypass Turborepo's dependency graph.

```json
// WRONG - manually building dependencies
{
  "scripts": {
    "prebuild": "cd ../../packages/types && bun run build && cd ../utils && bun run build",
    "build": "next build"
  }
}
```

**However, the fix depends on whether workspace dependencies are declared:**

1. **If dependencies ARE declared** (e.g., `"@repo/types": "workspace:*"` in package.json), remove the `prebuild` script. Turbo's `dependsOn: ["^build"]` handles this automatically.

2. **If dependencies are NOT declared**, the `prebuild` exists because `^build` won't trigger without a dependency relationship. The fix is to:
   - Add the dependency to package.json: `"@repo/types": "workspace:*"`
   - Then remove the `prebuild` script

```json
// CORRECT - declare dependency, let turbo handle build order
// package.json
{
  "dependencies": {
    "@repo/types": "workspace:*",
    "@repo/utils": "workspace:*"
  },
  "scripts": {
    "build": "next build"
  }
}

// turbo.json
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
```

**Key insight:** `^build` only runs build in packages listed as dependencies. No dependency declaration = no automatic build ordering.

### Overly Broad `globalDependencies`

`globalDependencies` affects ALL tasks in ALL packages. Be specific.

```json
// WRONG - heavy hammer, affects all hashes
{
  "globalDependencies": ["**/.env.*local"]
}

// BETTER - move to task-level inputs
{
  "globalDependencies": [".env"],
  "tasks": {
    "build": {
      "inputs": ["$TURBO_DEFAULT$", ".env*"],
      "outputs": ["dist/**"]
    }
  }
}
```

### Repetitive Task Configuration

Look for repeated configuration across tasks that can be collapsed. Turborepo supports shared configuration patterns.

```json
// WRONG - repetitive env and inputs across tasks
{
  "tasks": {
    "build": {
      "env": ["API_URL", "DATABASE_URL"],
      "inputs": ["$TURBO_DEFAULT$", ".env*"]
    },
    "test": {
      "env": ["API_URL", "DATABASE_URL"],
      "inputs": ["$TURBO_DEFAULT$", ".env*"]
    },
    "dev": {
      "env": ["API_URL", "DATABASE_URL"],
      "inputs": ["$TURBO_DEFAULT$", ".env*"],
      "cache": false,
      "persistent": true
    }
  }
}

// BETTER - use globalEnv and globalDependencies for shared config
{
  "globalEnv": ["API_URL", "DATABASE_URL"],
  "globalDependencies": [".env*"],
  "tasks": {
    "build": {},
    "test": {},
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

**When to use global vs task-level:**

- `globalEnv` / `globalDependencies` - affects ALL tasks, use for truly shared config.
- Task-level `env` / `inputs` - use when only specific tasks need it.

### NOT an Anti-Pattern: Large `env` Arrays

A large `env` array (even 50+ variables) is **not** a problem. It usually means the user was thorough about declaring their build's environment dependencies. Do not flag this as an issue.

### Using `--parallel` Flag

The `--parallel` flag bypasses Turborepo's dependency graph. If tasks need parallel execution, configure `dependsOn` correctly instead.

```bash
# WRONG - bypasses dependency graph
turbo run lint --parallel

# CORRECT - configure tasks to allow parallel execution
# In turbo.json, set dependsOn appropriately (or use transit nodes)
turbo run lint
```

### Package-Specific Task Overrides in Root turbo.json

When multiple packages need different task configurations, use **Package Configurations** (`turbo.json` in each package) instead of cluttering root `turbo.json` with `package#task` overrides.

```json
// WRONG - root turbo.json with many package-specific overrides
{
  "tasks": {
    "test": { "dependsOn": ["build"] },
    "@repo/web#test": { "outputs": ["coverage/**"] },
    "@repo/api#test": { "outputs": ["coverage/**"] },
    "@repo/utils#test": { "outputs": [] },
    "@repo/cli#test": { "outputs": [] },
    "@repo/core#test": { "outputs": [] }
  }
}

// CORRECT - use Package Configurations
// Root turbo.json - base config only
{
  "tasks": {
    "test": { "dependsOn": ["build"] }
  }
}

// packages/web/turbo.json - package-specific override
{
  "extends": ["//"],
  "tasks": {
    "test": { "outputs": ["coverage/**"] }
  }
}

// packages/api/turbo.json
{
  "extends": ["//"],
  "tasks": {
    "test": { "outputs": ["coverage/**"] }
  }
}
```

**Benefits of Package Configurations:**

- Keeps configuration close to the code it affects.
- Root turbo.json stays clean and focused on base patterns.
- Easier to understand what's special about each package.
- Works with `$TURBO_EXTENDS$` to inherit + extend arrays.

**When to use `package#task` in root:**

- Single package needs a unique dependency (e.g., `"deploy": { "dependsOn": ["web#build"] }`).
- Temporary override while migrating.

See `references/configuration/README.md#package-configurations` for full details.

### Using `../` to Traverse Out of Package in `inputs`

Don't use relative paths like `../` to reference files outside the package. Use `$TURBO_ROOT$` instead.

```json
// WRONG - traversing out of package
{
  "tasks": {
    "build": {
      "inputs": ["$TURBO_DEFAULT$", "../shared-config.json"]
    }
  }
}

// CORRECT - use $TURBO_ROOT$ for repo root
{
  "tasks": {
    "build": {
      "inputs": ["$TURBO_DEFAULT$", "$TURBO_ROOT$/shared-config.json"]
    }
  }
}
```

### Missing `outputs` for File-Producing Tasks

**Before flagging missing `outputs`, check what the task actually produces:**

1. Read the package's script (e.g., `"build": "tsc"`, `"test": "vitest"`).
2. Determine if it