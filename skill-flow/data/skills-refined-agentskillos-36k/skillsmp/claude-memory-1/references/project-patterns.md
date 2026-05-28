<project_patterns>
CLAUDE.md patterns optimized for specific project types.

<nextjs_app_router>

```markdown
# [Project Name] - Next.js App Router

## Tech Stack

- Next.js 15 with App Router
- TypeScript (strict mode)
- TailwindCSS + shadcn/ui
- [Database solution]

## Commands

- `pnpm dev` - Start dev server
- `pnpm build` - Production build
- `pnpm lint` - Check code
- `pnpm test:ci` - Run tests

## Directory Structure
```

app/
├── (auth)/ # Auth routes
├── (dashboard)/ # Dashboard routes
├── api/ # API routes
└── layout.tsx # Root layout
src/
├── components/ # UI components
├── lib/ # Utilities
└── hooks/ # React hooks

```

## Conventions

### Components
- Prefer Server Components
- Use `"use client"` only for interactivity
- Keep components under 300 lines

### Data Fetching
- Server Components: Direct database access
- Client Components: TanStack Query
- Mutations: Server Actions

### File Naming
- `page.tsx` - Route pages
- `layout.tsx` - Layouts
- `loading.tsx` - Loading states
- `error.tsx` - Error boundaries

## Important
- **NEVER** use `use client` for data fetching
- Always add `loading.tsx` for async pages
- Use `generateMetadata` for SEO
```

</nextjs_app_router>

<nextjs_pages_router>

```markdown
# [Project Name] - Next.js Pages Router

## Tech Stack

- Next.js 14 with Pages Router
- TypeScript
- TailwindCSS

## Commands

- `pnpm dev` - Development
- `pnpm build` - Production build
- `pnpm test` - Run tests

## Directory Structure
```

pages/
├── api/ # API routes
├── \_app.tsx # App wrapper
├── \_document.tsx # Document
└── index.tsx # Home page
src/
├── components/ # Components
├── lib/ # Utilities
└── hooks/ # Hooks

```

## Data Fetching
- `getServerSideProps` - SSR data
- `getStaticProps` - SSG data
- `useSWR` or TanStack Query - Client data

## API Routes
- Located in `pages/api/`
- Use `NextApiRequest` and `NextApiResponse` types
```

</nextjs_pages_router>

<react_vite>

```markdown
# [Project Name] - React + Vite

## Tech Stack

- React 18 + TypeScript
- Vite for bundling
- TailwindCSS
- TanStack Query

## Commands

- `pnpm dev` - Start dev server
- `pnpm build` - Production build
- `pnpm preview` - Preview build
- `pnpm test` - Run tests

## Directory Structure
```

src/
├── components/ # UI components
├── features/ # Feature modules
├── hooks/ # Custom hooks
├── lib/ # Utilities
├── routes/ # Route components
└── main.tsx # Entry point

```

## Conventions
- Functional components only
- Custom hooks for logic reuse
- TanStack Query for server state
- Zustand for client state
```

</react_vite>

<node_express>

```markdown
# [Project Name] - Node.js API

## Tech Stack

- Node.js + Express
- TypeScript
- PostgreSQL + Prisma
- Jest for testing

## Commands

- `pnpm dev` - Start with hot reload
- `pnpm build` - Compile TypeScript
- `pnpm start` - Start production
- `pnpm test` - Run tests

## Directory Structure
```

src/
├── controllers/ # Route handlers
├── middleware/ # Express middleware
├── models/ # Data models
├── routes/ # Route definitions
├── services/ # Business logic
├── utils/ # Helpers
└── index.ts # Entry point

```

## Conventions
- Controllers handle HTTP only
- Services contain business logic
- Middleware for cross-cutting concerns
- Always validate input with Zod

## Error Handling
- Use custom error classes
- Central error middleware
- Always return consistent error format
```

</node_express>

<python_fastapi>

```markdown
# [Project Name] - Python FastAPI

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy + PostgreSQL
- Pytest

## Commands

- `uvicorn main:app --reload` - Development
- `pytest` - Run tests
- `ruff check .` - Lint
- `ruff format .` - Format

## Directory Structure
```

app/
├── api/ # Route handlers
├── core/ # Config, security
├── db/ # Database models
├── schemas/ # Pydantic models
├── services/ # Business logic
└── main.py # Entry point

```

## Conventions
- Pydantic for validation
- Dependency injection for services
- Async where beneficial
- Type hints everywhere
```

</python_fastapi>

<monorepo_turborepo>

```markdown
# [Project Name] - Turborepo Monorepo

## Tech Stack

- Turborepo for build orchestration
- pnpm workspaces
- TypeScript

## Commands

- `pnpm install` - Install all deps
- `pnpm dev` - Start all apps
- `pnpm build` - Build all packages
- `pnpm test` - Test all packages
- `pnpm --filter web dev` - Start specific app

## Directory Structure
```

apps/
├── web/ # Main frontend
├── api/ # Backend API
└── admin/ # Admin panel
packages/
├── ui/ # Shared components
├── config/ # Shared config
├── types/ # Shared types
└── utils/ # Shared utilities

```

## Package Development
- Changes to `packages/*` require rebuild
- Use `pnpm --filter` for targeted commands
- Shared types in `packages/types`

## Conventions
- Each app has its own CLAUDE.md
- Root CLAUDE.md for universal rules
- Keep packages focused and minimal
```

</monorepo_turborepo>

<cli_tool>

```markdown
# [Tool Name] - CLI Tool

## Tech Stack

- TypeScript
- Commander.js for CLI
- Chalk for colors

## Commands

- `pnpm dev` - Watch mode
- `pnpm build` - Compile
- `pnpm link` - Link globally
- `[tool-name] --help` - Show help

## Directory Structure
```

src/
├── commands/ # CLI commands
├── lib/ # Core logic
├── utils/ # Helpers
└── index.ts # Entry point

```

## Adding Commands
1. Create command in `src/commands/`
2. Register in `src/index.ts`
3. Add tests in `__tests__/`

## Output Conventions
- Use chalk for colors
- Errors to stderr
- Progress with ora spinners
```

</cli_tool>

<library_package>

```markdown
# [Library Name] - npm Package

## Tech Stack

- TypeScript
- tsup for bundling
- Vitest for testing

## Commands

- `pnpm build` - Build package
- `pnpm test` - Run tests
- `pnpm dev` - Watch mode
- `pnpm publish` - Publish to npm

## Directory Structure
```

src/
├── index.ts # Main exports
├── utils/ # Internal helpers
└── types.ts # Type definitions

```

## Publishing Checklist
1. Update version in package.json
2. Run tests: `pnpm test`
3. Build: `pnpm build`
4. Publish: `pnpm publish`

## Conventions
- Export types alongside functions
- Document with JSDoc
- Maintain backwards compatibility
```

</library_package>
</project_patterns>

<customization_notes>
<adapt_sections>
Each pattern is a starting point. Adapt by:

1. Removing irrelevant sections
2. Adding project-specific conventions
3. Adjusting commands for your setup
4. Including critical architectural decisions
   </adapt_sections>

<keep_minimal>
Even for complex projects, aim for under 150 lines. Move detailed documentation to separate files and link from CLAUDE.md.
</keep_minimal>
</customization_notes>
