# Update Examples

Concrete before/after examples showing when and how to update CLAUDE.md.

---

## Example 1: New Module Added (Code Project)

**Change made:** Added `src/analytics/` module with event tracking.

### Before

```markdown
## Project Structure

- `src/auth/` — Authentication and session management
- `src/api/` — REST API endpoints
- `src/db/` — Database models and migrations
```

### After

```markdown
## Project Structure

- `src/analytics/` — Event tracking and usage metrics
- `src/auth/` — Authentication and session management
- `src/api/` — REST API endpoints
- `src/db/` — Database models and migrations
```

**Why:** New top-level module that future sessions need to know about.

---

## Example 2: Build Tool Changed (Code Project)

**Change made:** Migrated from webpack to vite.

### Before

```markdown
## Development

- Build: `npm run build` (webpack)
- Dev server: `npm run dev` (webpack-dev-server on port 3000)
- Bundle analysis: `npm run analyze`
```

### After

```markdown
## Development

- Build: `npm run build` (vite)
- Dev server: `npm run dev` (vite on port 5173)
- Preview production build: `npm run preview`
```

**Why:** Commands and ports changed. Removed stale `analyze` script that no
longer exists. Added `preview` which is vite-specific.

---

## Example 3: Chapter Reorganization (Text Project)

**Change made:** Split the "Security" chapter into "Authentication" and
"Authorization" chapters.

### Before

```markdown
## Document Structure

- `chapters/01-intro.tex` — Introduction and motivation
- `chapters/02-security.tex` — Security mechanisms
- `chapters/03-performance.tex` — Performance analysis
```

### After

```markdown
## Document Structure

- `chapters/01-intro.tex` — Introduction and motivation
- `chapters/02-authentication.tex` — Identity verification mechanisms
- `chapters/03-authorization.tex` — Access control and permissions
- `chapters/04-performance.tex` — Performance analysis
```

**Why:** File names changed, chapter numbering shifted, content split into two
files.

---

## Example 4: Removing Stale Info After Deletion

**Change made:** Removed the legacy `scripts/migrate_v1.py` migration tool that
was documented in CLAUDE.md.

### Before

```markdown
## Scripts

- `scripts/deploy.sh` — Deploy to production
- `scripts/migrate_v1.py` — Migrate from v1 database schema
- `scripts/seed.sh` — Seed development database
```

### After

```markdown
## Scripts

- `scripts/deploy.sh` — Deploy to production
- `scripts/seed.sh` — Seed development database
```

**Why:** The migration script was deleted. Leaving it documented would confuse
future sessions into referencing a nonexistent file.

---

## Example 5: New Convention Introduced

**Change made:** Introduced a shared error handling pattern across all API
endpoints.

### Before

```markdown
## Conventions

- Use TypeScript strict mode
- Prefer named exports over default exports
```

### After

```markdown
## Conventions

- Use TypeScript strict mode
- Prefer named exports over default exports
- Wrap API handlers with `withErrorHandler()` from `src/api/errors.ts`
```

**Why:** New pattern that all future API work should follow. Without this, future
sessions might write inconsistent error handling.

---

## Example 6: New Dependency Requiring Setup

**Change made:** Added Redis for caching, requiring a running Redis instance.

### Before

```markdown
## Setup

1. `npm install`
2. Copy `.env.example` to `.env` and fill in values
3. `npm run db:migrate`
```

### After

```markdown
## Setup

1. `npm install`
2. Copy `.env.example` to `.env` and fill in values
3. Start Redis: `docker run -d -p 6379:6379 redis:7`
4. `npm run db:migrate`
```

**Why:** Without the Redis step, the application won't start. Future sessions
need to know this prerequisite.
