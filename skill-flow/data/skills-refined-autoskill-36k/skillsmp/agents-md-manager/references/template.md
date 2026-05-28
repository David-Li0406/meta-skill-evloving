# AGENTS.md Template

Complete template with examples. Adapt to your project; remove unused sections.

## Minimal Template (~30 lines)

```markdown
# Project Name

One-line description of what this project does.

## Stack

- Runtime: Node.js 20 / Python 3.12 / etc.
- Framework: Next.js / FastAPI / etc.
- Database: PostgreSQL / MongoDB / etc.
- Package manager: pnpm / uv / etc.

## Structure

src/           - Application source code
tests/         - Test suite
scripts/       - Build and utility scripts

## Commands

Install:    `pnpm install`
Dev:        `pnpm dev`
Test:       `pnpm test`
Lint:       `pnpm lint`
Build:      `pnpm build`

## Docs

See `agent_docs/` for detailed documentation.
```

## Standard Template (~60 lines)

```markdown
# Project Name

One-line description of what this project does.

## Stack

- Runtime: Node.js 20
- Framework: Next.js 14 (App Router)
- Database: PostgreSQL with Prisma ORM
- Auth: NextAuth.js
- Styling: Tailwind CSS
- Package manager: pnpm

## Structure

app/              - Next.js app router pages and layouts
components/       - React components
  ui/             - Base UI components
  features/       - Feature-specific components
lib/              - Shared utilities and helpers
prisma/           - Database schema and migrations
tests/            - Test suite (Vitest)

## Commands

Install:          `pnpm install`
Dev server:       `pnpm dev`
Run tests:        `pnpm test`
Run single test:  `pnpm test path/to/test`
Type check:       `pnpm typecheck`
Lint:             `pnpm lint`
Format:           `pnpm format`
DB migrate:       `pnpm prisma migrate dev`
DB generate:      `pnpm prisma generate`

## Verification

Before committing, run: `pnpm typecheck && pnpm lint && pnpm test`

## Documentation

Read relevant files from `agent_docs/` before starting work:

- `architecture.md` - System design and service boundaries
- `database.md` - Schema documentation and relationships
- `api.md` - API endpoints and contracts
- `testing.md` - Test patterns and fixtures
- `deployment.md` - CI/CD and environment setup
```

## Monorepo Template (~80 lines)

```markdown
# Monorepo Name

Brief description of the monorepo and its purpose.

## Stack

- Monorepo: Turborepo
- Runtime: Node.js 20
- Package manager: pnpm (workspaces)

## Structure

apps/
  web/            - Main web application (Next.js)
  api/            - Backend API service (Express)
  admin/          - Admin dashboard (Next.js)

packages/
  ui/             - Shared UI component library
  config/         - Shared ESLint/TypeScript configs
  db/             - Database client and schemas
  utils/          - Shared utilities

## Commands (Root)

Install all:      `pnpm install`
Build all:        `pnpm build`
Test all:         `pnpm test`
Lint all:         `pnpm lint`

## Commands (Per App)

Run from root with filter:

Dev web:          `pnpm --filter web dev`
Test api:         `pnpm --filter api test`
Build admin:      `pnpm --filter admin build`

Or cd into app directory and run directly.

## App Details

### web (apps/web/)
Main customer-facing application. Next.js 14 with App Router.
Port: 3000

### api (apps/api/)
REST API backend. Express with tRPC.
Port: 4000

### admin (apps/admin/)
Internal admin dashboard. Next.js with authentication.
Port: 3001

## Shared Packages

- `@repo/ui` - Import shared components
- `@repo/db` - Import Prisma client
- `@repo/utils` - Import shared utilities

## Documentation

See `agent_docs/` for detailed documentation:

- `architecture.md` - System design overview
- `apps/web.md` - Web app specifics
- `apps/api.md` - API specifics
- `packages.md` - Shared package documentation
```

## Python Template (~50 lines)

```markdown
# Project Name

One-line description.

## Stack

- Python: 3.12
- Framework: FastAPI
- Database: PostgreSQL with SQLAlchemy
- Package manager: uv
- Task runner: make

## Structure

src/
  project_name/   - Main application package
    api/          - API routes and endpoints
    models/       - SQLAlchemy models
    services/     - Business logic
    schemas/      - Pydantic schemas
tests/            - Pytest test suite
alembic/          - Database migrations

## Commands

Setup venv:       `uv venv && source .venv/bin/activate`
Install:          `uv pip install -e ".[dev]"`
Dev server:       `make dev` or `uvicorn src.project_name.main:app --reload`
Run tests:        `make test` or `pytest`
Run single test:  `pytest tests/path/to/test.py -v`
Type check:       `make typecheck` or `pyright`
Lint:             `make lint` or `ruff check .`
Format:           `make format` or `ruff format .`
DB migrate:       `alembic upgrade head`
New migration:    `alembic revision --autogenerate -m "description"`

## Verification

Before committing: `make check` (runs lint, typecheck, test)

## Documentation

See `agent_docs/` for detailed documentation.
```

## Key Principles Demonstrated

1. **Brevity** - Each template is under 100 lines
2. **Universal commands** - Only commands that apply to all work
3. **Clear structure** - Easy to scan and find information
4. **Pointers not content** - Reference agent_docs/ for details
5. **No code snippets** - Commands only, no implementation examples
