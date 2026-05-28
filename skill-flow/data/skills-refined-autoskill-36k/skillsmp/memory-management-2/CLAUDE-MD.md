# CLAUDE.md Deep Dive

Complete guide to creating effective CLAUDE.md files for Claude Code projects.

## File Locations

CLAUDE.md can exist in multiple locations with different scopes:

| Location | Scope | Best For |
|----------|-------|----------|
| `~/.claude/CLAUDE.md` | All projects | Personal preferences |
| `~/CLAUDE.md` | Home directory projects | Less common |
| `./CLAUDE.md` | Project root | Primary project memory |
| `./.claude/CLAUDE.md` | Config directory | Same as root, organized |
| `./subdir/CLAUDE.md` | Subdirectory | Monorepo packages |

### Location Priority

Files load in order, with later files taking precedence:

1. `~/.claude/CLAUDE.md` (global)
2. Project root `CLAUDE.md`
3. `.claude/CLAUDE.md`
4. Current working directory CLAUDE.md

## Essential Sections

Every effective CLAUDE.md should include these sections.

### 1. Project Overview

Start with a brief description:

```markdown
# Project Name

A TypeScript CLI tool for managing Claude Code extensions.
Uses Bun runtime with React for terminal UI.
```

**Tips:**
- Keep it to 1-3 sentences
- Mention the primary language/runtime
- State the project's purpose

### 2. Commands

The most critical section. Include exact commands for common operations:

```markdown
## Commands

- `bun install` - Install dependencies
- `bun dev` - Start development server (port 3000)
- `bun test` - Run all tests
- `bun test:watch` - Run tests in watch mode
- `bun build` - Build for production
- `bun lint` - Check code style
- `bun lint:fix` - Auto-fix lint issues
- `bun typecheck` - Check TypeScript types
```

**Tips:**
- Use exact commands (copy-pasteable)
- Include port numbers and important flags
- Add comments for non-obvious options
- Cover build, test, lint, and run scenarios

### 3. Tech Stack

Document the technology choices:

```markdown
## Tech Stack

- **Runtime**: Bun 1.1+
- **Framework**: React 19 + React Router 7
- **Database**: PostgreSQL 15 with Drizzle ORM
- **Auth**: Better Auth with session tokens
- **Styling**: Tailwind CSS + shadcn/ui
- **Testing**: Bun test (unit), Playwright (E2E)
```

**Tips:**
- Include version constraints when important
- Explain non-standard choices briefly
- List primary libraries by category

### 4. Architecture

Provide project structure context:

```markdown
## Architecture

```
src/
  routes/        # API route handlers (Hono)
  services/      # Business logic layer
  db/
    schema/      # Drizzle schema definitions
    migrations/  # Database migrations
  lib/           # Shared utilities
  components/    # React components (for CLI UI)
tests/
  unit/          # Unit tests
  e2e/           # End-to-end tests
```

### Key Patterns

- Routes call services, never DB directly
- Services handle business logic and call repositories
- Use Drizzle's query builder, not raw SQL
```

**Tips:**
- Show directory structure visually
- Explain the layering/separation of concerns
- Note important patterns or conventions

### 5. Code Style

Document project-specific conventions:

```markdown
## Code Style

- Use single quotes for strings
- Prefer for-loops over forEach
- Use `type` over `interface` except for extensible contracts
- Errors: throw `AppError` with error codes, not generic Error
- Naming: camelCase for files, PascalCase for components
```

**Tips:**
- Focus on non-obvious or project-specific rules
- Don't repeat language defaults
- Explain the "why" for unusual conventions

### 6. Important Notes

Critical information Claude should always know:

```markdown
## Important Notes

- **Never mock database** - Use test database with `bun test:db:setup`
- **Auth required** - All API routes need `requireAuth` middleware
- **Env vars** - Check `.env.example` for required variables
- **Drizzle migrations** - Always run `bun db:migrate` after schema changes
```

**Tips:**
- Use for error-prone areas
- Include "gotchas" you've encountered
- Highlight security-critical patterns

## Optional Sections

Include these when relevant:

### Environment Variables

```markdown
## Environment Variables

See `.env.example` for all required variables.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SESSION_SECRET` - 32+ char secret for sessions
- `API_KEY` - External API authentication
```

### API Conventions

```markdown
## API Conventions

- Base path: `/api/v1`
- Auth: Bearer token in `Authorization` header
- Errors: `{ error: string, code: string, details?: object }`
- Pagination: `?page=1&limit=20` (default 20, max 100)
```

### Testing

```markdown
## Testing

### Unit Tests
```bash
bun test                    # All tests
bun test src/services       # Service tests only
bun test --watch            # Watch mode
```

### E2E Tests
```bash
bun test:e2e               # Run Playwright tests
bun test:e2e --ui          # Interactive mode
```

### Test Database
```bash
bun test:db:setup          # Create test database
bun test:db:reset          # Reset to clean state
```
```

### Deployment

```markdown
## Deployment

- **Staging**: Auto-deploys on push to `develop`
- **Production**: Manual deploy via GitHub Actions
- **Rollback**: `bun run deploy:rollback`

See `docs/deployment.md` for full process.
```

## Complete Example

Here's a well-structured CLAUDE.md for a real project:

```markdown
# Acme Dashboard

A React dashboard for managing Acme Corp's customer data.
Built with React 19, React Router 7, and PostgreSQL.

## Commands

- `bun install` - Install dependencies
- `bun dev` - Start dev server (http://localhost:3000)
- `bun build` - Production build
- `bun test` - Run unit tests
- `bun test:e2e` - Run Playwright E2E tests
- `bun db:migrate` - Run database migrations
- `bun db:studio` - Open Drizzle Studio
- `bun lint` - Check code with Biome
- `bun typecheck` - TypeScript type checking

## Tech Stack

- **Runtime**: Bun 1.1+
- **Frontend**: React 19, React Router 7, TanStack Query
- **Backend**: Hono API routes
- **Database**: PostgreSQL 16, Drizzle ORM
- **Auth**: Better Auth (session-based)
- **Styling**: Tailwind CSS, shadcn/ui components
- **Testing**: Bun test, Playwright

## Architecture

```
app/
  routes/           # React Router routes
  components/       # UI components
    ui/             # shadcn/ui primitives
    features/       # Feature-specific components
  lib/
    db/             # Drizzle schema and queries
    api/            # API client utilities
    auth/           # Auth helpers
server/
  routes/           # Hono API handlers
  services/         # Business logic
  middleware/       # Auth, logging, etc.
```

## Code Style

- Biome for linting and formatting (see biome.json)
- Use for-loops, not forEach
- Prefer named exports over default exports
- Components: PascalCase files and names
- Utilities: camelCase files and names

## Important Notes

- **Database**: Never mock - use test database
- **Auth**: All API routes require `authMiddleware`
- **Errors**: Use `AppError` class with error codes
- **Env**: Copy `.env.example` to `.env` before starting
- **Migrations**: Run after pulling new changes

## Testing

Unit tests: `bun test`
E2E tests: `bun test:e2e`

Test database setup:
```bash
bun db:test:create   # One-time setup
bun db:test:reset    # Before test runs
```

## Deployment

See `docs/deployment.md` for full process.
```

## What NOT to Include

### Avoid These

```markdown
## Bad Examples

### Too Verbose
The project uses React, which is a JavaScript library for building
user interfaces. React was created by Facebook and is now maintained
by Meta. We chose React because...

### Obvious Information
- Write clean code
- Follow best practices
- Test your changes

### Duplicated Documentation
[Entire API reference pasted here - 500 lines]

### Stale Information
- Uses Node 14 (we're on Node 20)
- Run `npm install` (we use Bun now)

### Personal Preferences in Project Memory
- I prefer vim keybindings
- Always use dark mode
```

### Instead

```markdown
## Good Alternatives

### Concise
React 19 frontend with TanStack Query for data fetching.

### Actionable
Run `bun test` before committing. All tests must pass.

### Reference
API documentation: `docs/api.md`

### Current
Runtime: Bun 1.1+, Commands: `bun install`, `bun dev`

### Appropriate Scope
(Keep personal preferences in ~/.claude/CLAUDE.md)
```

## Updating CLAUDE.md

### When to Update

- New technology added to stack
- Command syntax changes
- Architecture patterns established
- Common mistakes discovered
- Team conventions agreed upon

### How to Update

1. **Keep it current** - Stale information is worse than none
2. **Be incremental** - Add context as you learn the project
3. **Review periodically** - Monthly check for accuracy
4. **Version control** - Track changes with meaningful commits

### Update Workflow

```bash
# After making significant project changes
# 1. Review current CLAUDE.md
# 2. Update outdated sections
# 3. Add new patterns discovered
# 4. Remove obsolete information
# 5. Commit with descriptive message

git add CLAUDE.md
git commit -m "docs: update CLAUDE.md with new auth patterns"
```

## Global vs Project Memory

### Global (`~/.claude/CLAUDE.md`)

Personal preferences that apply everywhere:

```markdown
# Global Preferences

## Code Style
- Use single quotes
- Prefer for-loops over forEach
- Use `const` by default

## Tools
- Use Bun over npm
- Use ripgrep (rg) for search
- Use Biome over ESLint + Prettier

## Workflow
- Run tests before committing
- Prefer small, focused changes
```

### Project (`./CLAUDE.md`)

Project-specific context:

```markdown
# My Project

This is specific to this project...
```

### Resolving Conflicts

When global and project conflict:

1. Project settings take precedence
2. Be explicit when overriding: "For this project, use npm (not Bun)"
3. Don't fight your global settings unnecessarily

## Multi-CLAUDE.md Projects

For monorepos or large projects:

```
project/
  CLAUDE.md                    # Shared across all packages
  packages/
    frontend/
      CLAUDE.md                # Frontend-specific
    backend/
      CLAUDE.md                # Backend-specific
    shared/
      CLAUDE.md                # Shared library context
```

### Inheritance

Claude reads CLAUDE.md files from:
1. Global (`~/.claude/CLAUDE.md`)
2. Project root
3. Current working directory

So `packages/frontend/CLAUDE.md` inherits from root `CLAUDE.md`.

## CLAUDE.md vs Rules

Use CLAUDE.md for:
- Project-wide context
- Commands and tech stack
- Architecture overview
- Always-needed information

Use rules for:
- File-type-specific guidance
- Conditional instructions
- Modular, focused memory
- Large instruction sets

See [RULES.md](./RULES.md) for rules documentation.
