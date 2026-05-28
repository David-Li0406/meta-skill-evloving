---
name: lib-utils
description: >-
  CI-safe utilities for TypeScript projects. Provides logger wrapper (falls back to stub when lib-log unavailable) and env injection (skips in CI). Use for projects that need to work in both dev and CI without special setup.
---

# lib-utils

Utilities that enhance development but gracefully degrade in CI environments.

| Import Path | Optional Dep | With Dep | Without Dep (CI) | Without Dep (not CI) |
|-------------|--------------|----------|------------------|----------------------|
| `@mdr/lib-utils/logger` | lib-log | Axiom logging | Console stub | **exit(1)** |
| `@mdr/lib-utils/env` | lib-1password | 1Password injection | No-op stub | **exit(1)** |
| `@mdr/lib-utils/browser` | lib-log | Axiom logging | Console stub | Console stub |

## Installation

```bash
bun add github:wsh-auto/lib-utils
```

**Consumer `package.json` (only include optionalDeps you use):**
```json
"dependencies": {
  "@mdr/lib-utils": "github:wsh-auto/lib-utils"
},
"optionalDependencies": {
  "@mdr/lib-log": "file:../lib-log"
}
```

- **Separate exports**: Import from `/logger` or `/env` - each loads only its optional dep
- **lib-utils**: always `github:` in dependencies
- **lib-log/lib-1password**: always `file:` in **optionalDependencies** - only include what you use
- **CI**: graceful degradation (console stub / no-op)
- **Not CI**: fatal exit if optional dep missing for the export you import

**For 1Password env injection**, create `.env.template` (committed) with `op://` refs:
```bash
export MY_API_KEY=op://wsh/skills_my-project/API_KEY
```
Add `.env` to `.gitignore` - it's generated with real values at runtime.

## Logging
### lib-log / logger.ts - createLogger(project-name)

```typescript
import { createLogger } from '@mdr/lib-utils/logger';

const log = createLogger('my-project');

log.info('Starting');
log.error('Failed', { code: 500 });
await log.flush();
```

- If `@mdr/lib-log` installed: full Axiom logging
- If not + CI: console-based stub (debug/info/warn/error all log)
- If not + not CI: exit(1) with instructions to add to optionalDependencies

**CLI commands must `await log.flush()`** before exit - otherwise logs may be lost (async shipping incomplete). Long-running daemons auto-flush in batches.

**Shared client:** All loggers share one Axiom client. One `flush()` call drains all loggers in the process.

**Test teardown:** Call `await shutdown()` (not `flush()`) to close the Axiom client and allow vitest to exit cleanly.

**Output destinations:** With lib-log, logs go to both stderr (keeps stdout clean for pipeable data) and Axiom (cloud persistence).

**Required logging (add these to your code):**
- `log.info()` - MUST log: state changes (create/update/delete), external interactions (send email, API calls), recovery actions
- `log.warn()` - MUST log: degraded state, potential issues
- `log.error()` - MUST log: failures, exceptions
- `log.debug()` - SHOULD log: internal function calls useful for debugging (off by default, enable via `LOG_LEVEL=debug`)

**Don't log** high-volume operations at info level (>45/min: polling loops, health pings).

### Browser - createLogger(project-name)

For frontend/browser environments (e.g., React apps bundled with Vite):

```typescript
import { createLogger } from '@mdr/lib-utils/browser';

const log = createLogger('wsh:frontend');
log.info('Page loaded');
```

**Key differences from `/logger`:**
- No Node.js APIs (works in browsers)
- Never exits fatally - always graceful degradation
- Uses lazy initialization (no top-level await for Vite compatibility)

### Querying Logs: `ax` CLI

**Naming convention:** Logger name = folder name. If you're in `cli-tt/`, logs are at `--project cli-tt` (auto-catches subsystems like `cli-tt:daemon`, `cli-tt:pool`).

```bash
ax                          # Logs for current folder (auto-detects)
ax projects                 # List all project names
ax --project '*cli-tt*'     # All cli-tt subsystems (glob pattern)
ax --level error            # Filter by level
ax --json                   # JSON output for agents
```

**Glob patterns:** Use `*foo*` (contains) - most useful since logger names have org prefix (e.g., `mdr:cli-tt`).

See `$mdr:lib-log` for full ax documentation including APL passthrough.

## lib-1password / env.ts - initEnv(projectRoot, skipIfEnvVars?, log?)

```typescript
import { resolve } from 'path';
import { initEnv } from '@mdr/lib-utils/env';

// When .env.template is in same directory as calling file:
initEnv(import.meta.dirname);

// When .env.template is in parent directory (e.g., src/index.ts → project root):
initEnv(resolve(import.meta.dirname, '..'));              // CORRECT: canonical path
// initEnv(import.meta.dirname + '/..');                  // WRONG: leaves '..' unresolved

// Optional parameters:
initEnv(projectRoot, ['MY_API_KEY']);                     // skip if env vars already set
initEnv(projectRoot, [], customLogger);                   // custom logger (must have info/error)
```

- Returns `DotenvConfigOutput` with `{ parsed: Record<string, string> }`
- If `@mdr/lib-1password` installed: delegates to lib1p.initEnv() (1Password injection)
- If not + CI: returns `{ parsed: {} }` (empty stub)
- If not + not CI: exit(1) with instructions to add to optionalDependencies

## Scripts
`scripts/_LIB-UTILS_update-dependents` - Updates all lib-utils dependents. Run with `--help` for usage.

