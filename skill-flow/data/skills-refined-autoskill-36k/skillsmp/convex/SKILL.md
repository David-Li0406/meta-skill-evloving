---
name: convex
description: Convex backend development patterns, validators, indexes, actions, queries, mutations, file storage, scheduling, React hooks, components, and testing. Use when writing Convex code, debugging Convex issues, planning Convex architecture, or writing Convex tests.
---

# Convex Development Guide

Provide comprehensive Convex development guidance to avoid common mistakes and ensure code compiles on first try.

## Priorities

1. **Compile + typecheck** on first try
2. **Respect Convex's constraints** (indexes, limits, auth, schedulers, file storage)
3. **Avoid expensive / subtle bugs** (wrong indexes, misuse of actions, broken hooks)

## Mental Model

Convex is a **hosted backend** with:
- **Database**: documents + indexes + full-text search
- **Functions**: `query`, `mutation`, `action`, plus internal variants
- **Realtime queries**: `useQuery` on the client auto-subscribes
- **File storage**, **Auth** (via `@convex-dev/auth`), **Scheduler** (cron + `runAfter`)

Code layout:
- **Backend**: `convex/*.ts` files
- **Client**: React using `convex/react` (`useQuery`, `useMutation`)
- **Generated API**: `convex/_generated/api` exports `api` + `internal`

## Quick Reference

### Functions
- Import from `./_generated/server`
- Use `query({ args, handler })` syntax
- Always define `args` validators

### Indexes (CRITICAL)
- **Never** use `.filter()` - use `.withIndex()` instead
- **Never** define `by_creation_time` index (it's built-in)
- **Never** include `_creationTime` in custom index fields

### Actions
- Add `"use node";` at top for Node modules
- **Never** use `ctx.db` - use `ctx.runQuery`/`ctx.runMutation`
- Only actions support dynamic imports

### Scheduler
- Auth does NOT propagate - use internal functions
- Use function references (`internal.file.fn`), not the function itself

### React Hooks
- **Never** call hooks conditionally
- Use `"skip"` pattern: `useQuery(api.foo, condition ? args : "skip")`
- `usePaginatedQuery` returns `{ results, status, loadMore }` for infinite scroll

### Testing
- Use `convex-test` with Vitest
- Pass `schema` to `convexTest()` for validation
- Use `t.withIdentity()` for auth testing

## Reference Files

Load these as needed based on the task:

| Topic | File | When to use |
|-------|------|-------------|
| Schema & Validators | [schema-validators.md](references/schema-validators.md) | Defining tables, validators, system fields |
| Functions | [functions.md](references/functions.md) | Query/mutation/action patterns, calling functions |
| Indexes & Queries | [indexes-queries.md](references/indexes-queries.md) | Database queries, indexes, search |
| Pagination | [pagination.md](references/pagination.md) | usePaginatedQuery, cursor-based pagination, infinite scroll |
| Actions & HTTP | [actions-http.md](references/actions-http.md) | Actions, HTTP endpoints, external APIs |
| Scheduling | [scheduling.md](references/scheduling.md) | Cron jobs, scheduled functions |
| File Storage | [file-storage.md](references/file-storage.md) | Uploads, downloads, file metadata |
| Limits | [limits.md](references/limits.md) | Size limits, time limits, design constraints |
| Environment Variables | [env-secrets.md](references/env-secrets.md) | Secrets, API keys, environment setup |
| React Patterns | [react-patterns.md](references/react-patterns.md) | useQuery, useMutation, skip pattern |
| Auth | [auth.md](references/auth.md) | Authentication, user identity |
| Components | [components.md](references/components.md) | Presence, ProseMirror, Resend components |
| TypeScript Fixes | [typescript-fixes.md](references/typescript-fixes.md) | TS2589 errors, static API generation |
| Checklist | [checklist.md](references/checklist.md) | Pre-commit verification checklist |
| Testing | [testing.md](references/testing.md) | convex-test, Vitest patterns |

## Process

1. Check the quick reference above for common patterns
2. Load specific reference files based on the task
3. Verify against the [checklist](references/checklist.md) before finalizing code
