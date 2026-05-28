# Migration Safety Protocols (2026)

Database migrations are the most dangerous part of software engineering. This guide ensures zero-downtime deployments and data safety.

## 1. The Migration Lifecycle

1.  **Generate**: Use `bun prisma migrate dev --create-only` to review the SQL first.
2.  **Audit**: Check for destructive changes (e.g., `DROP COLUMN`, `RENAME COLUMN`).
3.  **Test**: Apply to a staging/preview database before production.
4.  **Execute**: Run `bun prisma migrate deploy` in the CI/CD pipeline.

## 2. Handling Destructive Changes

Never `DROP` or `RENAME` in a single deployment.

-   **Renaming a Column**:
    1.  Add the new column (keep the old one).
    2.  Write to both columns.
    3.  Backfill data from old to new.
    4.  Switch reads to the new column.
    5.  Wait 48 hours.
    6.  Drop the old column in a separate migration.

## 3. Lock Management

Avoid long-running migrations that lock tables.

-   **Index Creation**: Always use `CREATE INDEX CONCURRENTLY` in raw SQL migrations.
-   **NOT NULL**: Add columns as `NULL` first, backfill data, then add `NOT NULL` (ideally with `NOT VALID` as discussed in the Postgres 18 guide).

## 4. Numbered Migration Standard

We use 3-digit numbered sequences for clarity and ordering.

-   `db/migrations/001_initial_schema.sql`
-   `db/migrations/002_add_roles.sql`

## 5. Rollback Strategy

Every migration must have a corresponding "down" or "rollback" plan documented in the code comments, even if not automated.

---
*Updated: January 22, 2026 - 18:00*
