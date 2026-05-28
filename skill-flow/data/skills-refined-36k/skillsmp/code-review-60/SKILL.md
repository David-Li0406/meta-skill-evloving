---
name: code-review
description: Perform code reviews for this No Name Running Club application (Next.js 16 App Router + React 19 + TypeScript + Tailwind CSS 4 + Prisma + NextAuth v5). Use when reviewing PRs/diffs, proposing architectural changes, or giving code quality feedback. Covers server actions/route handlers, service-layer patterns, Prisma queries & migrations, auth/role checks, caching/revalidation, security, and performance.
---

# Code Review

Follow these guidelines when reviewing code for this Next.js + Prisma application.

## Review Checklist

### Correctness & DX

Look for these issues in code changes:

- **Runtime errors**: `undefined` access, unhandled promise rejections, missing null checks on optional Prisma fields
- **Validation gaps**: `FormData` parsing without guarding missing/invalid fields
- **Error handling**: throwing generic errors where UI needs actionable messages; leaking internal errors to the client
- **Time & timezone**: using `new Date()` inconsistently for “today” semantics

### Next.js App Router Patterns

- **Server vs client boundaries**:
  - Prefer **Server Components by default**
  - Add `"use client"` only when required (state, effects, browser-only APIs, event handlers)
  - Keep client components small; push data access and heavy work to server components/actions
- **Server Actions** (`"use server"` in `src/app/actions/*`):
  - Authenticate early via `auth()` from `src/lib/auth.ts`
  - For admin-only actions, wrap with `withAdminAuth()` from `src/lib/admin.ts`
  - After mutations that affect server-rendered pages, call `revalidatePath(...)` (see `src/app/actions/admin.ts`)
- **Route handlers** (`src/app/api/*`):
  - Validate input and return appropriate status codes
  - Avoid doing business logic directly in the route; delegate to services

### Service Layer (`src/services/`)

- Keep business rules in services (not in components, actions, or route handlers)
- Prefer **stateless** service methods (many services in this repo use static methods)
- Keep Prisma access centralized and testable; avoid duplicating query logic across actions/pages

### Prisma & Database

- **Prisma client**: always import `prisma` from `src/lib/prisma.ts` (singleton pattern)
- **N+1 queries**: watch for loops that call Prisma repeatedly; prefer `include`/`select`/`where in (...)`
- **Transactions**: for multi-write operations, consider `prisma.$transaction(...)` to maintain invariants
- **Migrations**: follow `.claude/rules/database.md`
  - Never edit committed migrations; create a new migration instead

### Authentication, Authorization, Security

- **Auth checks**: ensure all mutations and sensitive reads require `auth()` (or admin wrapper)
- **Role checks**: admin screens/actions should use the existing role plumbing (token role set in `src/lib/auth.ts`)
- **Secrets**: never log credentials, tokens, or full environment configs
- **User input**: validate and normalize user-controlled strings (zip code, units, ids)

### Performance & UX

- **Over-fetching**: avoid fetching unused fields; use `select` for large models
- **Client bundle**: avoid turning large subtrees into client components; avoid adding heavy deps casually
- **UI feedback**: for server actions triggered from client, ensure pending states (`useTransition`) and error states exist

### Long-Term Impact

Flag for extra care / senior review when changes involve:

- **Prisma migrations** (schema changes) or dangerous backfills
- **Auth/role logic** (`src/lib/auth.ts`, `src/lib/admin.ts`, middleware)
- **Caching/revalidation** changes that affect correctness
- **New dependency adoption** (bundle size, licensing, maintenance)
- **External API calls** (weather, analytics exports, etc.)

## Feedback Guidelines

### Tone

- Be polite and constructive
- Provide actionable suggestions with code examples
- Phrase as questions when uncertain: "Have you considered...?"

### Approval

- Approve when only minor issues remain
- Don't block PRs for stylistic preferences already covered by linters
- Goal is risk reduction, not perfect code
