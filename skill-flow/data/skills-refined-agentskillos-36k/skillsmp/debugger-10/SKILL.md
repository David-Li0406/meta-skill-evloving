---
name: debugger
description: Diagnose and fix bugs, errors, and unexpected behavior in the codebase
allowed-tools:
  - Bash
  - Grep
  - Read
  - Edit
---

# Debugger

## Purpose

Diagnose and fix bugs, errors, and unexpected behavior in the codebase.

## When to Invoke

- Application crashes or errors
- Tests failing unexpectedly
- Unexpected behavior in features
- Performance issues
- Build failures
- Runtime errors

## Capabilities

- Analyze error messages and stack traces
- Identify root causes
- Check logs and console output
- Examine relevant code
- Isolate issues through minimal reproduction

## Common Issues

| Issue Type        | Common Causes                                              |
| ----------------- | ---------------------------------------------------------- |
| TypeScript errors | Type mismatches, missing imports, incorrect generics       |
| Database issues   | Connection problems, migration failures, incorrect queries |
| Build failures    | Dependency conflicts, environment variables, configuration |
| Runtime errors    | Null/undefined, race conditions, memory leaks              |
| Performance       | N+1 queries, memory leaks, slow endpoints                  |

## Debugging Process

1. **Gather Information** - Error messages, stack traces, console output, recent changes
2. **Analyze** - Identify symptoms, trace code path, check dependencies, review configuration
3. **Isolate** - Create minimal reproduction, eliminate variables, test assumptions
4. **Fix** - Apply solution, verify fix works, add tests to prevent regression

## Common Commands

```bash
# Dependencies
pnpm ls [package-name]
pnpm outdated

# Type checking
pnpm typecheck
pnpm nx typecheck [app]

# Database
pnpm db:push
pnpm db:studio

# Docker/Testcontainers
docker ps
docker logs [container-id]

# Build issues
pnpm nx reset
pnpm nx build [app] --skip-nx-cache
```

## Solutions Reference

| Error                          | Solution                                                                 |
| ------------------------------ | ------------------------------------------------------------------------ |
| Module not found               | Check import paths, verify package installed, check tsconfig paths       |
| Cannot connect to database     | Check DATABASE_URL, verify PostgreSQL running, check port conflicts      |
| Type X not assignable to Y     | Check type definitions, verify Zod schemas match, review generics        |
| Testcontainers failed to start | Verify Docker running, check port conflicts, ensure sufficient resources |
| Unexpected token               | Check TypeScript version, verify babel/swc config, review tsconfig       |

## Output Format

1. **Issue Identified** - Clear description of the problem
2. **Root Cause** - Why it's happening
3. **Solution** - How to fix it
4. **Code Changes** - Specific changes needed
5. **Prevention** - How to avoid this in the future
6. **Verification** - How to verify the fix works
