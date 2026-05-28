---
name: pnpm
description: pnpm package manager patterns and gotchas. Use when running pnpm commands, configuring workspaces, or parallel script execution.
---

# pnpm

## Environment

Use `pnpm env` for Node version management (not nvm).

## Parallel Scripts

**CRITICAL:** To run multiple scripts in parallel, use pattern matching:

```bash
pnpm run '/pattern/'
```

Example: `pnpm run '/docs:dev:.*/'` runs all matching scripts concurrently.

**NEVER use `--parallel` flag** - it's only for workspace packages, not for running multiple scripts in a single package.
