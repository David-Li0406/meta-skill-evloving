# Prior Work Summary Template

Create this file at the start of a context-aware SDD session. Update after each task completion.

## File Location

```
docs/plans/prior_work_summary.md
# OR alongside your plan file:
docs/plans/feature-plan.md
docs/plans/feature-plan-prior-work.md
```

## Template

```markdown
# Prior Work Summary

Plan: [plan-file-path]
Started: [date]
Last updated: [date]

## Completed Tasks

### Task 1: [Task Name]
**Summary:** [2-3 line description of what was implemented]
**Files:** [comma-separated list of main files changed]
**Key decisions:** [any architectural decisions that affect later tasks]

### Task 2: [Task Name]
**Summary:** [2-3 line description]
**Files:** [files changed]
**Key decisions:** [if any]

...

## Patterns Established

[Patterns that subsequent tasks should follow]

- API endpoints follow: `src/api/[resource]/[action].ts`
- Services use dependency injection via constructor
- All database operations use transactions

## Dependencies Created

[Things that later tasks can/should use]

- `AuthService` available at `src/services/auth.ts`
- `UserModel` with CRUD at `src/models/user.ts`
- Shared validation schemas at `src/schemas/`

## Anti-patterns Noted

[Things that caused issues, for future reference]

- Don't use `any` type - caused type errors in Task 3
- Remember to add RLS policies for new tables
```

## Compression Rules

### After 5 tasks: Compress older entries

Before (detailed):
```markdown
### Task 1: Auth Middleware
**Summary:** Implemented JWT validation middleware that checks...
**Files:** src/middleware/auth.ts, src/config/jwt.ts, tests/middleware/auth.test.ts
**Key decisions:** Used jose library for JWT, 1h token expiry
```

After (compressed):
```markdown
### Task 1: Auth Middleware
JWT validation. Files: middleware/auth.ts. Uses jose library.
```

### After 10 tasks: Ultra-compress oldest

```markdown
## Completed (summarized)
- Tasks 1-5: Auth system (middleware, login, logout, refresh, session)
- Tasks 6-7: User management (CRUD, roles)

## Recent (detailed)
### Task 8: ...
### Task 9: ...
### Task 10: ...
```

## What to Include

| Include | Why |
|---------|-----|
| Feature-level summary | Context for later tasks |
| Main files changed | Know where code lives |
| Key decisions | Consistency across tasks |
| Patterns established | Follow conventions |
| Dependencies created | Reuse in later tasks |

## What to Exclude

| Exclude | Why |
|---------|-----|
| Implementation details | Code is the source of truth |
| Review feedback | Already addressed |
| Test specifics | Tests document themselves |
| Full file paths | Main file name sufficient |
| Reasoning/rationale | Over-explains |

## Example: Well-Compressed Summary

```markdown
# Prior Work Summary

Plan: docs/plans/auth-feature.md

## Completed

### Task 1: JWT Middleware
Auth middleware with token validation. Files: middleware/auth.ts

### Task 2: Login Endpoint
Email/password login with session. Files: api/auth/login.ts, services/auth.ts

### Task 3: User Model
Prisma schema + TypeScript types. Files: prisma/schema.prisma, types/user.ts

## Patterns
- Auth endpoints at `api/auth/[action].ts`
- Services injected via context

## Dependencies
- `AuthService.validateToken()`
- `UserModel.findByEmail()`
```

## Providing to Implementer

When dispatching implementer, include compressed version:

```markdown
## Prior Work Summary

- Task 1: JWT middleware. Files: middleware/auth.ts
- Task 2: Login endpoint with sessions. Files: api/auth/login.ts
- Task 3: User model with Prisma. Files: schema.prisma, types/user.ts

Patterns: Auth at api/auth/, services via context injection.
Dependencies: AuthService.validateToken(), UserModel.findByEmail()
```

Target: **<200 tokens** for prior work section in implementer prompt.
