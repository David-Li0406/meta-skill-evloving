# AGENTS.md Examples

Complete examples for different project types.

## Example 1: Laravel + React + Inertia.js (Full-Stack)

```markdown
# Project Name - Laravel + React + Inertia.js

Brief one-sentence description of what this application does.

## Quick Commands

- **Dev**: `npm run dev` (Vite HMR - auto-starts in Herd)
- **Build**: `npm run build` (production assets)
- **Test**: `composer test` (Pest with coverage)
- **Quality**: `composer run checks` (Rector, Pint, PHPStan, coverage)
- **Frontend Quality**: `npm run checks` (ESLint, Prettier, TypeScript)
- **Fresh DB**: `php artisan migrate:fresh --seed`

## Tech Stack

- **Backend**: PHP 8.5, Laravel 12, PostgreSQL
- **Frontend**: React 19, TypeScript, Inertia.js, Tailwind CSS v4
- **Testing**: Pest v4 with browser testing (Playwright)
- **Quality**: Rector, Pint, PHPStan/Larastan (level 8)
- **Environment**: Laravel Herd (auto HTTPS, Redis, MinIO)

## Key Directories

- `app/Actions/{Domain}/` - Business logic operations (domain-driven)
- `app/DTOs/{Domain}/` - Data transfer objects for type-safe data passing
- `app/Http/Controllers/` - Thin route handlers (delegate to Actions)
- `app/Http/Requests/` - Form validation with toDTO() methods
- `app/Http/Resources/` - API response formatting
- `app/Models/` - Eloquent models with PHPDoc properties
- `resources/js/components/` - React components (one per file)
- `resources/js/pages/` - Inertia page components
- `resources/js/layouts/` - Layout wrappers for pages
- `tests/Feature/` - HTTP endpoint tests (most common)
- `tests/Unit/` - Isolated business logic tests
- `tests/Browser/` - End-to-end browser tests (Playwright)

## Architecture Decisions

- **Business Logic**: Action classes in `app/Actions/{Domain}/` following domain-driven design
- **Validation**: Form Requests with `toDTO()` methods convert to type-safe DTOs
- **Controllers**: Thin controllers that delegate to Actions (single responsibility)
- **React Components**: Function components with TypeScript, no `FC` type, use `import type`
- **State Management**: React Context for global state, TanStack Query for server state
- **Testing Strategy**: Feature tests for all HTTP endpoints, browser tests for complex UI flows
- **Type Safety**: 100% type coverage required (PHPStan level 8, TypeScript strict)

## Before Committing

All code must pass:

- Rector (automated refactoring)
- Pint (code formatting)
- PHPStan level 8 (static analysis)
- 90% code coverage minimum
- 100% type coverage
- ESLint + Prettier (frontend)
- TypeScript compilation (no errors)

Run `composer run checks` to verify all backend checks.
Run `npm run checks` to verify all frontend checks.

Formatters run automatically on save (Pint for PHP, Prettier for JS/TS/JSON).

## Environment Notes

- Laravel Herd provides automatic HTTPS at URL in `APP_URL` (.env)
- No need to run `php artisan serve` - always available via Herd
- Redis and MinIO automatically configured and running
- Vite HMR works with Herd's HTTPS automatically

## Available Skills

Load skills on-demand for specific tasks:

**Backend**: creating-actions, creating-dtos, creating-form-requests, creating-controllers, creating-migrations, managing-models, writing-feature-tests, writing-unit-tests

**Frontend**: creating-react-components, creating-inertia-pages, creating-hooks, creating-layouts, defining-typescript-types

**Quality**: ensuring-laravel-quality, ensuring-frontend-quality, writing-browser-tests

## Custom Commands

Quick access patterns:

- `/test` - Run all tests with coverage
- `/quality` - Run all quality checks and fix issues
- `/component Name` - Create React component
- `/action ActionName` - Create Action class

## For More Context

- Skill files in `.opencode/skill/` provide detailed patterns for specific tasks
- Load skills automatically by mentioning task types (e.g., "create an Action")
```

## Example 2: React SPA (Frontend Only)

```markdown
# Project Name - React TypeScript SPA

Brief description of the application.

## Quick Commands

- **Dev**: `npm run dev` (Vite dev server)
- **Build**: `npm run build` (production bundle)
- **Test**: `npm test` (Vitest with coverage)
- **Lint**: `npm run lint` (ESLint + Prettier)
- **Type Check**: `npm run type-check` (TypeScript compiler)
- **Preview**: `npm run preview` (test production build)

## Tech Stack

- **Framework**: React 19, TypeScript 5
- **Build**: Vite 6
- **Routing**: React Router v7
- **State**: TanStack Query + Zustand
- **Styling**: Tailwind CSS v4
- **Testing**: Vitest + React Testing Library + Playwright

## Key Directories

- `src/components/` - Reusable React components
- `src/pages/` - Route page components
- `src/features/` - Feature-based modules (components + hooks + utils)
- `src/lib/` - Shared utilities and helpers
- `src/api/` - API client and endpoint definitions
- `tests/` - Test files mirror src/ structure

## Architecture Decisions

- **Component Organization**: Feature-based in `src/features/`, shared in `src/components/`
- **State Management**: TanStack Query for server state, Zustand for client state
- **API Layer**: All API calls through `src/api/client.ts` with typed endpoints
- **Component Pattern**: Function components with hooks, no class components
- **Type Safety**: Strict TypeScript, no `any` types, use `unknown` for unsafe data
- **Testing**: Unit tests for logic, integration tests for features, e2e for critical flows

## Before Committing

All code must pass:

- TypeScript compilation (`npm run type-check`)
- ESLint with no warnings (`npm run lint`)
- Prettier formatting (auto-formatted on save)
- Test suite with 90% coverage (`npm test -- --coverage`)
- Production build succeeds (`npm run build`)

## For More Context

- @docs/component-patterns.md for component conventions
- @docs/state-management.md for state patterns
- @docs/testing-strategy.md for test organization
```

## Example 3: Python CLI Tool

```markdown
# Project Name - Python CLI Tool

Brief description of what the CLI does.

## Quick Commands

- **Setup**: `uv venv && uv pip install -e ".[dev]"` (create venv and install)
- **Run**: `project-name [command]` (main CLI entry point)
- **Test**: `pytest --cov` (tests with coverage)
- **Lint**: `ruff check .` (linting)
- **Format**: `ruff format .` (auto-formatting)
- **Type Check**: `mypy src/` (static type checking)

## Tech Stack

- **Python**: 3.12+
- **CLI Framework**: Click 8
- **Testing**: pytest with pytest-cov
- **Linting**: Ruff (replaces flake8, isort, black)
- **Type Checking**: mypy with strict mode
- **Package Manager**: uv (fast pip alternative)

## Key Directories

- `src/project_name/` - Main package code
- `src/project_name/commands/` - CLI command implementations
- `src/project_name/utils/` - Shared utilities
- `tests/` - Test files mirror src/ structure
- `tests/fixtures/` - Test data and fixtures

## Architecture Decisions

- **CLI Pattern**: Click-based command groups with decorators
- **Configuration**: Load from `~/.config/project-name/config.toml`
- **Error Handling**: Custom exception hierarchy, user-friendly error messages
- **Testing**: Unit tests for pure functions, integration tests for commands
- **Type Safety**: Full type hints with mypy strict mode

## Before Committing

All code must pass:

- Ruff linting (`ruff check .`)
- Ruff formatting (`ruff format .`)
- mypy type checking (`mypy src/`)
- pytest with 90% coverage (`pytest --cov --cov-report=term-missing`)

## For More Context

- @docs/commands.md for adding new CLI commands
- @docs/testing.md for testing patterns
```

## Example 4: Monorepo

```markdown
# Monorepo Name

Turborepo monorepo with multiple packages.

## Quick Commands

- **Dev**: `turbo run dev` (all packages)
- **Test**: `turbo run test` (all packages)
- **Build**: `turbo run build` (all packages)
- **Workspace**: `turbo run dev --filter=@scope/package` (single package)

## Key Directories

- `apps/web/` - Next.js web application (see apps/web/AGENTS.md)
- `apps/api/` - Express API server (see apps/api/AGENTS.md)
- `packages/ui/` - Shared UI components (see packages/ui/AGENTS.md)
- `packages/types/` - Shared TypeScript types

## Architecture Decisions

- Shared packages in `packages/` with proper exports
- Apps in `apps/` consume packages via workspace names
- Turborepo for caching and parallel execution

## Before Committing

Run from root:

- `turbo run lint` - All linting
- `turbo run test` - All tests
- `turbo run build` - Verify builds

## For More Context

- See package-level AGENTS.md for package-specific conventions
```
