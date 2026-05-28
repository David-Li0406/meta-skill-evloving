---
name: git-workflow
description: Standards for committing and pushing code to the Cycle Navigator Dashboard repository. Use this when the user wants to save, commit, or deploy changes.
---

# Git Workflow Instructions

When performing a commit or preparing a push, follow these project-specific rules:

1. **Pre-Commit Verification**:
   - Backend: Run `ruff check backend/` for linting and `pytest backend/` for tests.
   - If frontend changes were made: Run `npm run lint` and `npm test` in the `web` directory.
   - This prevents merging broken code to main.

2. **Commit Message Format**:
   - Use descriptive headers with format: `<type>(<scope>): <description>`
   - Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
   - Scope: affected component (e.g., `backend/tasks`, `web/components`)
   - Examples:
     - ✅ `feat(backend/tasks): add retry logic for failed macro jobs`
     - ❌ `fix stuff` (too vague)
   - For breaking changes or multi-line details, add a body with issue references (e.g., `Closes #123`)

3. **Breaking Changes**:
   - Mark breaking changes in the commit body with: `BREAKING CHANGE: <description>`
   - Include in breaking changes: Celery paths, database schema, API endpoints, environment variables, or config structure.
   - Examples:
     - `BREAKING CHANGE: Celery tasks moved from services.macro_worker to celery_app. Update docker-compose.yml.`
     - `BREAKING CHANGE: API endpoint /api/v1/tasks renamed to /api/v2/tasks.`
   - For database changes, ensure migrations are included in `scripts/timescale_migrations.sql`.

4. **Safety Checks**:
   - Never commit `.env` files or sensitive API keys (FRED_API_KEY, COINGECKO_API_KEY).
   - Verify that any new database migrations are included in `scripts/timescale_migrations.sql`.