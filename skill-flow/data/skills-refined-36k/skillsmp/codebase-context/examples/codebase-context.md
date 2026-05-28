# Codebase Context

> **INSTRUCTION FOR AGENTS:** Read this file FIRST before exploring the codebase. This provides pre-built context to minimize exploration tokens.

---

## Project Overview

**Name:** ExampleApp
**Description:** A full-stack web application for managing tasks
**Type:** Monorepo with web app and API
**Package Manager:** pnpm

---

## Directory Structure

```
example-app/
├── src/                      # Next.js web app source
│   ├── app/                  # Next.js App Router (pages + API routes)
│   │   ├── api/v1/           # Versioned public API endpoints
│   │   ├── dashboard/        # Dashboard pages
│   │   └── settings/         # Settings pages
│   ├── components/           # React components by feature
│   │   ├── ui/               # Shared UI primitives
│   │   ├── tasks/            # Task-related components
│   │   └── layout/           # Layout components
│   ├── lib/                  # Shared utilities
│   │   ├── db/               # Database queries/mutations
│   │   └── utils/            # General utilities
│   ├── types/                # TypeScript type definitions
│   └── hooks/                # Custom React hooks
├── prisma/                   # Prisma schema and migrations
├── scripts/                  # Utility scripts
└── docs/                     # Project documentation
```

---

## Key Files by Feature

### API Routes (`src/app/api/v1/`)

- `tasks/route.ts` - CRUD for tasks
- `tasks/[id]/route.ts` - Individual task operations
- `users/route.ts` - User management

### Database (`src/lib/db/`)

- `queries.ts` - Read queries
- `mutations.ts` - Write operations
- `client.ts` - Prisma client singleton

### Components (`src/components/`)

- `tasks/task_card.tsx` - Task display card
- `tasks/task_list.tsx` - Task list with filters
- `layout/header.tsx` - Main navigation header

---

## Patterns & Conventions

### Naming

- Files: `snake_case.ts` (e.g., `task_card.tsx`)
- Functions: `camelCase` (e.g., `createTask`)
- Types: `PascalCase` (e.g., `Task`, `User`)
- Components: `PascalCase` (e.g., `TaskCard`)

### Code Style

- Use `type` over `interface` unless interface merging needed
- Use named exports over default exports
- Use async/await over .then() chains
- Use early returns to reduce nesting
- Use `@/` path alias for imports (maps to `src/`)

### Testing

- Colocate tests: `*.spec.ts` next to source files
- Use Vitest with jsdom for React components
- Group tests under `describe(functionName, ...)`

---

## Tech Stack

| Layer     | Technology              |
| --------- | ----------------------- |
| Framework | Next.js 14 (App Router) |
| Language  | TypeScript (strict)     |
| Styling   | Tailwind CSS            |
| Database  | PostgreSQL + Prisma     |
| Auth      | NextAuth.js             |
| Testing   | Vitest                  |
| Hosting   | Vercel                  |

---

## Database Schema (Key Tables)

| Table   | Purpose                    |
| ------- | -------------------------- |
| `users` | User accounts              |
| `tasks` | Task items with status     |
| `tags`  | Tags for categorizing tasks |

---

## Important Rules

1. **NEVER push code with type errors** - Pre-commit hook enforces this
2. **Colocate tests** - Put `*.spec.ts` next to source files
3. **Use Conventional Commits** - `feat:`, `fix:`, `docs:`, etc.
4. **API routes are public** - Design for third-party use

---

## Quick Commands

```bash
# Development
pnpm dev                    # Start dev server

# Quality gates
pnpm typecheck              # TypeScript check
pnpm lint                   # ESLint
pnpm test                   # Run tests

# Database
pnpm db:push                # Push schema changes
pnpm db:generate            # Generate Prisma client
```

---

## Environment Variables

Required in `.env.local`:

- `DATABASE_URL` - PostgreSQL connection string
- `NEXTAUTH_SECRET` - Auth encryption key
- `NEXTAUTH_URL` - App URL for auth callbacks

---

## Common Gotchas

- **Port 3000**: Dev server runs on default port 3000
- **Prisma client**: Must regenerate after schema changes
- **Pre-commit hooks**: All quality gates must pass before commit

---

## Domain Concepts

- **Task**: A work item with title, description, status, and due date
- **Status**: `pending`, `in_progress`, `completed`, `archived`
- **Tag**: A label for categorizing tasks

---

## Key Workflows

### Task Creation Flow

1. User submits task form
2. API validates input
3. Task saved to database
4. UI updates optimistically
