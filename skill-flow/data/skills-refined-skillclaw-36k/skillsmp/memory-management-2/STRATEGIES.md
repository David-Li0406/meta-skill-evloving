# Memory Strategies

Advanced patterns for effective Claude Code memory management across sessions, teams, and projects.

## Project Onboarding Memory

When starting with a new project, build memory incrementally.

### Day 1: Minimal Setup

```markdown
# Project Name

## Commands
- `bun install` - Install dependencies
- `bun dev` - Start development
- `bun test` - Run tests

## Tech Stack
- Runtime: Bun
- Framework: [discovered from package.json]
```

### Week 1: Core Patterns

After working in the codebase:

```markdown
## Architecture
[Document the patterns you've discovered]

## Code Style
[Note conventions you've observed]

## Important Notes
[Gotchas you've encountered]
```

### Ongoing: Rules Files

As you discover file-specific patterns:

```
.claude/rules/
  components.md     # React patterns
  api.md            # API conventions
  database.md       # ORM patterns
```

### Onboarding Workflow

```bash
# 1. Start with the essentials
claude "Help me create a minimal CLAUDE.md for this project"

# 2. After exploring
claude "Update CLAUDE.md with patterns we've discovered"

# 3. Create specific rules
claude "Create a rules file for our React component patterns"
```

## Team Conventions

### Shared Memory Structure

```
project/
  CLAUDE.md               # Team conventions (committed)
  .claude/
    CLAUDE.md             # Alternative location
    rules/                # Modular team standards
      code-style.md
      testing.md
      security.md
    settings.json         # Shared tool settings
```

### What to Commit

**Always commit:**
- `CLAUDE.md` - Project context
- `.claude/rules/*.md` - Team conventions
- `.claude/settings.json` - Shared settings (careful with hooks)

**Never commit:**
- `.claude/settings.local.json` - Personal settings
- Personal preferences that override team standards

### Team CLAUDE.md Template

```markdown
# Project Name

## For Team Members

This CLAUDE.md contains our team conventions. Personal preferences
should go in your `~/.claude/CLAUDE.md`.

## Commands

### Development
- `bun dev` - Start development server
- `bun test` - Run test suite
- `bun lint` - Check code style

### Database
- `bun db:migrate` - Run migrations
- `bun db:studio` - Open database GUI

## Architecture

[Team-agreed architecture]

## Conventions

[Team-agreed coding standards]

## PR Requirements

1. All tests pass
2. Lint clean
3. Types check
4. Review approved
```

### Handling Convention Disagreements

When team members have different preferences:

1. **Document the decision** - In CLAUDE.md or a rules file
2. **Explain the why** - Future team members need context
3. **Be consistent** - Pick one and stick to it
4. **Review periodically** - Conventions can evolve

## Architecture Documentation

Use memory files to document architectural decisions.

### Architecture in CLAUDE.md

```markdown
## Architecture

### Layer Separation
```
API Layer (routes/)
    |
    v
Service Layer (services/)
    |
    v
Repository Layer (db/repositories/)
    |
    v
Database (PostgreSQL)
```

### Data Flow
1. Request hits route handler
2. Route validates input with Zod
3. Route calls service method
4. Service contains business logic
5. Service calls repository for data
6. Repository uses Drizzle ORM
7. Response flows back up

### Key Decisions
- **No direct DB calls from routes** - Always through services
- **Services are stateless** - No instance state, pure functions
- **Repositories abstract ORM** - Could swap Drizzle without touching services
```

### Architecture Rules File

```markdown
# .claude/rules/architecture.md
---
globs: ["src/**/*.ts"]
alwaysApply: true
description: Core architecture patterns
---

# Architecture Rules

## Layer Dependencies

Allowed imports:
- Routes -> Services, Types
- Services -> Repositories, Types
- Repositories -> DB Schema, Types

Forbidden:
- Routes -> Repositories (skip service layer)
- Services -> Routes (circular)
- Repositories -> Services (reverse dependency)

## File Organization

Each feature follows:
```
src/features/users/
  routes.ts         # API handlers
  service.ts        # Business logic
  repository.ts     # Data access
  types.ts          # Shared types
  schema.ts         # Zod schemas
```
```

## Tech Stack Documentation

### Comprehensive Stack Doc

```markdown
## Tech Stack

### Runtime & Build
| Tool | Version | Purpose |
|------|---------|---------|
| Bun | 1.1+ | Runtime, package manager, bundler |
| TypeScript | 5.3+ | Type safety |
| Biome | 1.5+ | Linting and formatting |

### Backend
| Library | Purpose | Docs |
|---------|---------|------|
| Hono | Web framework | docs/hono.md |
| Drizzle | ORM | docs/drizzle.md |
| Better Auth | Authentication | docs/auth.md |
| Zod | Validation | - |

### Frontend
| Library | Purpose |
|---------|---------|
| React 19 | UI framework |
| React Router 7 | Routing |
| TanStack Query | Data fetching |
| Tailwind CSS | Styling |
| shadcn/ui | Components |

### Testing
| Tool | Use For |
|------|---------|
| Bun test | Unit tests |
| Playwright | E2E tests |
| MSW | API mocking |
```

### Stack-Specific Rules

```markdown
# .claude/rules/drizzle.md
---
globs: ["src/db/**/*.ts", "drizzle/**/*"]
---

# Drizzle ORM Patterns

## Schema Definition
```typescript
import { pgTable, text, timestamp, uuid } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});
```

## Query Patterns
```typescript
// Select with relations
const user = await db.query.users.findFirst({
  where: eq(users.id, userId),
  with: { posts: true },
});

// Insert returning
const [newUser] = await db.insert(users)
  .values({ email, name })
  .returning();

// Transaction
await db.transaction(async (tx) => {
  await tx.insert(users).values(userData);
  await tx.insert(profiles).values(profileData);
});
```
```

## Cross-Session Continuity

Strategies for maintaining context between Claude Code sessions.

### Session Start Hooks

Inject recent context when sessions begin:

```json
// .claude/settings.json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "cat .claude/session-context.md 2>/dev/null || echo ''"
          }
        ]
      }
    ]
  }
}
```

### Session Context File

Maintain a file with recent context:

```markdown
# .claude/session-context.md

## Recent Work (Updated: 2025-01-08)

### Current Focus
Implementing user authentication with Better Auth.

### In Progress
- [ ] Add password reset flow
- [ ] Email verification

### Recent Decisions
- Using session tokens (not JWT) for auth
- Redis for session storage in production

### Blockers
- Waiting on SMTP credentials for email

## Quick Context
Last commit: "feat: add login and signup routes"
Current branch: feature/auth
```

### Automatic Context Updates

Hook to update context after sessions:

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/scripts/update-context.sh"
          }
        ]
      }
    ]
  }
}
```

```bash
#!/bin/bash
# .claude/scripts/update-context.sh

cat > .claude/session-context.md << EOF
# Session Context

## Recent Work (Updated: $(date +%Y-%m-%d))

### Git Status
$(git status --short 2>/dev/null || echo "Not a git repo")

### Recent Commits
$(git log --oneline -5 2>/dev/null || echo "No commits")

### Current Branch
$(git branch --show-current 2>/dev/null || echo "Unknown")
EOF
```

## Memory for Different Project Types

### Monorepo Pattern

```
monorepo/
  CLAUDE.md                    # Shared conventions
  .claude/
    rules/
      workspace.md             # Monorepo-specific rules

  apps/
    web/
      CLAUDE.md                # Web app context
    api/
      CLAUDE.md                # API context
    mobile/
      CLAUDE.md                # Mobile app context

  packages/
    shared/
      CLAUDE.md                # Shared package context
    ui/
      CLAUDE.md                # UI library context
```

Root CLAUDE.md:

```markdown
# Monorepo

## Structure
- `apps/` - Deployable applications
- `packages/` - Shared libraries

## Commands (from root)
- `bun install` - Install all dependencies
- `bun dev` - Start all apps in dev mode
- `bun test` - Run all tests
- `bun build` - Build all packages

## App-Specific Commands
Run from app directory or use workspace command:
- `bun --filter web dev`
- `bun --filter api test`

## Shared Packages
- `@repo/ui` - Component library
- `@repo/shared` - Utilities and types
```

### Library/SDK Pattern

```markdown
# My SDK

## Package Info
- Name: @myorg/sdk
- Version: See package.json
- Entry: src/index.ts

## Commands
- `bun dev` - Watch mode
- `bun build` - Build for distribution
- `bun test` - Run tests
- `bun docs` - Generate documentation

## Public API
Only export from `src/index.ts`. Internal modules should not be
exposed to consumers.

## Testing
- Unit tests for all public methods
- Integration tests in `tests/integration/`
- Consumer tests in `tests/consumer/`

## Publishing
1. Update version in package.json
2. Update CHANGELOG.md
3. Run `bun publish`
```

### CLI Tool Pattern

```markdown
# My CLI Tool

## Development
- `bun dev` - Run CLI in dev mode
- `bun build` - Build executable
- `bun test` - Run tests

## Usage
```bash
my-cli <command> [options]
```

## Commands Structure
Commands in `src/commands/`, one file per command.

## Adding Commands
1. Create `src/commands/new-command.ts`
2. Export command definition
3. Register in `src/cli.ts`

## Testing Commands
Use `runCommand()` helper in tests to simulate CLI execution.
```

## Memory Maintenance

### Regular Review Checklist

Weekly or bi-weekly:

- [ ] Commands still accurate?
- [ ] Tech stack up to date?
- [ ] Architecture reflects current state?
- [ ] Rules files still relevant?
- [ ] Remove obsolete information

### Deprecation Pattern

When patterns change:

```markdown
## Migrations (UPDATED 2025-01-08)

> **DEPRECATED**: Old migration pattern using `db:migrate:run`
> **NEW**: Use `bun db:migrate` with Drizzle Kit

Old workflow (deprecated):
- ~~`bun db:migrate:generate`~~
- ~~`bun db:migrate:run`~~

New workflow:
- `bun db:generate` - Generate migration
- `bun db:migrate` - Apply migrations
```

### Memory Cleanup

Periodically remove:

1. **Obsolete commands** - Old scripts, renamed commands
2. **Outdated patterns** - Superseded conventions
3. **Stale references** - Dead links, removed files
4. **Duplicate information** - Consolidate redundancy

## Integration with Weave

For projects using the Weave knowledge framework:

### Weave + Memory

```
.agent/weave/           # Institutional knowledge
  dimensions/
    E/                  # Patterns (epistemology)
    Π/                  # Practices (praxeology)
    ...

.claude/
  CLAUDE.md             # Operational memory
  rules/                # Conditional rules
```

### Relationship

- **CLAUDE.md** - Day-to-day operational context
- **Rules** - File-specific guidance
- **Weave** - Institutional knowledge, decisions, patterns

### Syncing Knowledge

When discoveries from a session should persist:

1. **Immediate** - Update CLAUDE.md or rules
2. **Institutional** - Add to Weave dimensions
3. **Both** - Reference Weave from memory

```markdown
# CLAUDE.md

## Patterns

For established patterns, see `.agent/weave/dimensions/E/`.

Quick reference:
- API error handling: `E/api-error-pattern`
- React Query setup: `E/react-query-pattern`
```

## Quick Reference

### File Locations

| Type | Path | Scope |
|------|------|-------|
| Global | `~/.claude/CLAUDE.md` | All projects |
| Project | `./CLAUDE.md` | This project |
| Config | `./.claude/CLAUDE.md` | This project |
| Rules | `./.claude/rules/*.md` | Conditional |

### Update Frequency

| Content | Update When |
|---------|-------------|
| Commands | When they change |
| Tech Stack | When dependencies change |
| Architecture | After major refactors |
| Rules | When patterns evolve |
| Context | Each session |

### Memory Size Guidelines

| File | Target | Max |
|------|--------|-----|
| CLAUDE.md | ~100 lines | 500 lines |
| Rule file | ~50 lines | 200 lines |
| Total rules | 5-10 files | 20 files |
