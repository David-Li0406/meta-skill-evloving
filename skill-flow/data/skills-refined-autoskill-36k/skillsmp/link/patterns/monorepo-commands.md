# Monorepo Commands Reference

Common commands for working with the mediapp monorepo using Bun workspaces.

## Workspace Structure

```
mediapp/
├── package.json          # Root workspace
├── bunfig.toml          # Bun workspace config
└── packages/
    ├── web/             # @mediapp/web
    └── api/             # @mediapp/api
```

## Installation

```bash
# Install all dependencies (root + all packages)
bun install

# Install dependency in specific package
bun --filter @mediapp/web add react-query
bun --filter @mediapp/api add elysia

# Install dev dependency
bun --filter @mediapp-web add -d @types/node
```

## Development

```bash
# Run both packages in parallel
bun run dev

# Run specific package
bun --filter @mediapp/web dev
bun --filter @mediapp/api dev

# Build specific package
bun --filter @mediapp/web build
bun --filter @mediapp/api build

# Build all packages
bun run build
```

## Package Scripts

### Web (packages/web)

```bash
cd packages/web

bun run dev          # Start dev server (port 5176)
bun run build        # Production build
bun run preview      # Preview production build
bun run lint         # ESLint check
bun run typecheck    # TypeScript check
```

### API (packages/api)

```bash
cd packages/api

bun run dev          # Start dev server (port 5300)
bun run build        # Production build
bun run start        # Run production build
bun run lint         # ESLint check
bun run typecheck    # TypeScript check

# Database
bun run db:generate  # Generate migration from schema changes
bun run db:migrate   # Apply migrations
bun run db:seed      # Seed database with test data
bun run db:reset     # Drop all tables and re-migrate
bun run db:studio    # Open Drizzle Studio
```

## Database Workflow

```bash
# 1. Make schema changes in packages/api/src/db/schema/

# 2. Generate migration
cd packages/api
bun run db:generate

# 3. Review migration in drizzle/migrations/

# 4. Apply migration
bun run db:migrate

# 5. Optional: Seed data
bun run db:seed
```

## Type Checking

```bash
# Check all packages
bun run typecheck

# Check specific package
cd packages/web && bun run typecheck
cd packages/api && bun run typecheck
```

## Linting

```bash
# Lint all packages
bun run lint

# Lint specific package
cd packages/web && bun run lint
cd packages/api && bun run lint

# Auto-fix
cd packages/web && bun run lint --fix
cd packages/api && bun run lint --fix
```

## Git Workflow

```bash
# Commit changes
git add .
git commit -m "feat: add feature name"

# Common commit prefixes
# feat:     New feature
# fix:      Bug fix
# refactor: Code refactoring
# docs:     Documentation
# style:    Formatting, missing semicolons, etc.
# test:     Adding tests
# chore:    Maintenance
```

## Environment Variables

### API (.env)

```bash
# packages/api/.env
DATABASE_URL=postgresql://user:pass@localhost:5432/mediapp
BETTER_AUTH_SECRET=your-secret-here
BETTER_AUTH_URL=http://localhost:5300
CORS_ORIGIN=http://localhost:5176
```

### Web (.env)

```bash
# packages/web/.env
VITE_API_URL=http://localhost:5300
```

## Debugging

### API Debug

```bash
cd packages/api

# Run with inspector
bun --inspect run dev

# View logs
bun run dev | bunyan  # If using bunyan logger
```

### Web Debug

```bash
cd packages/web

# Run with source maps
bun run dev

# Open React DevTools in browser
# Open Network tab to inspect API calls
```

## Production Build

```bash
# Build all packages
bun run build

# Test production builds locally
cd packages/api && bun run start    # Port 5300
cd packages/web && bun run preview  # Port 5176
```

## Troubleshooting

### Clear Cache

```bash
# Remove node_modules and reinstall
rm -rf node_modules packages/*/node_modules
bun install

# Clear Bun cache
bun pm cache rm
```

### Reset Database

```bash
cd packages/api
bun run db:reset
bun run db:seed
```

### Fix TypeScript Errors

```bash
# Rebuild TypeScript declarations
bun run typecheck

# Check for circular dependencies
cd packages/web && bun run build
cd packages/api && bun run build
```

### Port Conflicts

```bash
# Check what's using port 5176 or 5300
lsof -i :5176
lsof -i :5300

# Kill process
kill -9 <PID>
```

## Performance

### Bundle Analysis (Web)

```bash
cd packages/web
bun run build

# Analyze bundle size
bunx vite-bundle-visualizer
```

### Database Performance (API)

```bash
cd packages/api

# Open Drizzle Studio to inspect queries
bun run db:studio

# Check migration performance
time bun run db:migrate
```

## Useful Aliases

Add to your shell profile:

```bash
# Navigate
alias ma="cd ~/code/mediapp"
alias maw="cd ~/code/mediapp/packages/web"
alias maa="cd ~/code/mediapp/packages/api"

# Development
alias madev="cd ~/code/mediapp && bun run dev"
alias maweb="cd ~/code/mediapp && bun --filter @mediapp/web dev"
alias maapi="cd ~/code/mediapp && bun --filter @mediapp/api dev"

# Database
alias madb="cd ~/code/mediapp/packages/api && bun run db:studio"
alias maseed="cd ~/code/mediapp/packages/api && bun run db:seed"
```
