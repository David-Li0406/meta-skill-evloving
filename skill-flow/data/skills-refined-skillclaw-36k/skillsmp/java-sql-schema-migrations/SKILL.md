---
name: java-sql-schema-migrations
description: Flyway/Liquibase-agnostic database migration strategy for backward-compatible, zero-downtime schema changes using expand/contract. Includes rollout plan, safety checks, and verification steps.
license: CC-BY-4.0
compatibility:
  jdk: "17+"
  build: ["Maven", "Gradle"]
  databases: ["PostgreSQL", "MySQL", "MariaDB", "SQL Server", "Oracle"]
  migration_tools: ["Flyway", "Liquibase", "Manual SQL (controlled)"]
metadata:
  owner: "backend-platform"
  version: "1.0"
  tags: ["java", "database", "migrations", "zero-downtime", "expand-contract", "flyway", "liquibase"]
---

# java-sql-schema-migrations

## Intent

Provide a repeatable, tool-agnostic playbook to evolve SQL schemas safely in production with minimal downtime and minimal blast radius. The default strategy is **expand/contract** with **backward compatibility** at every intermediate step.

## Scope

### In scope

- Schema evolution (tables/columns/indexes/constraints) with **zero-downtime** or **near-zero downtime**
- Rollout sequencing: application deploy(s) + migration(s) + backfill(s) + cleanup
- Guardrails: locking risk, long-running DDL, verification, rollback strategy
- Flyway/Liquibase conventions (but the approach works with any migration runner)

### Out of scope

- One-off emergency hotfix DDL executed manually without review/audit
- Major cross-database re-platforming (treat as a dedicated project)
- Data warehouse / analytics-only pipelines

## When to use

- Adding/removing columns, changing types, introducing new constraints
- Splitting/merging tables, renaming columns, changing indexes under load
- Any release that touches DB schema and must avoid downtime or breaking older app versions

## Core principles (non-negotiable)

1. **Every intermediate state must be compatible with both:**
   - the currently deployed application, and
   - the next application version (during progressive rollout).
2. **Avoid long exclusive locks**: prefer online/low-lock DDL where supported.
3. **Prefer additive changes first** (expand), destructive changes last (contract).
4. **Data backfills are application changes** (they need throttling, observability, and retry).
5. **Migrations are audited artifacts**: versioned, reviewed, reproducible, and verified.

## Inputs (required context)

- DB engine/version (e.g., PostgreSQL 14, MySQL 8)
- Migration tool (Flyway vs Liquibase) and where migrations live
- Deployment model (blue/green, canary, rolling, multi-region)
- Traffic pattern and peak windows
- SLO constraints (max allowed latency increase / error rate during rollout)
- Safety knobs: statement timeout, lock timeout, max runtime per migration

## Standard workflow: Expand / Migrate / Backfill / Switch / Contract

### Step 0 — Preflight checklist

- Identify the change category:
  - Additive (safe default)
  - Requires backfill
  - Requires dual-write / dual-read
  - Potentially locking DDL
- Estimate risk:
  - table size, index build time, lock level, write amplification
- Define success criteria:
  - “no increased 5xx”
  - “p99 latency <= baseline + X ms”
  - “replication lag within threshold”
- Define rollback route:
  - app rollback must still work with expanded schema
  - do not rely on “down” migrations for large data changes

### Step 1 — EXPAND (add new schema without breaking old code)

Common patterns:

- Add new nullable column with default handled in application (not DB if it locks)
- Add new table alongside old
- Add new index in an online-compatible manner (engine-specific)
- Add new constraint as NOT VALID / NOCHECK first (engine-specific), validate later

Example: add a column safely

- Add column as NULLable
- Application writes it optionally
- Backfill existing rows
- Later enforce NOT NULL (after verification)

### Step 2 — DEPLOY app that can operate with BOTH schemas

- Implement “read old + new” or “prefer new fallback to old”
- Implement “dual-write” only when necessary and with idempotency
- Keep feature flag(s) to switch reads/writes independently
- Include metrics to verify new-path adoption (counts, ratios, error rates)

### Step 3 — BACKFILL with throttling and observability

- Backfill is a controlled batch job, not a single massive UPDATE
- Use chunking (by PK range, time window), bounded concurrency, retry
- Track:
  - processed rows
  - lag/backlog
  - error rate
  - execution time
- Prefer resumable backfill with a progress table or checkpointing

### Step 4 — SWITCH reads/writes to the new representation

- Turn on feature flag: read-from-new
- Observe metrics + logs
- Turn on: write-to-new only (if dual-write was temporary)
- Ensure consistency checks pass

### Step 5 — CONTRACT (remove old schema only after safe window)

- Drop old columns/tables/indexes only after:
  - all app versions in fleet no longer use old schema
  - backfill complete and verified
  - stable window (e.g., multiple deploys)
- Contract steps should be small and reversible where possible

## Handling common schema change types

### 1) Renaming a column (no downtime)

Never rename in-place if older app versions may still reference old name.
Instead:

1. Expand: add new column (new_name)
2. Deploy: dual-write (old_name + new_name) or write-to-new + read fallback
3. Backfill: populate new_name from old_name
4. Switch: read new_name only
5. Contract: drop old_name

### 2) Changing a column type

Avoid direct ALTER TYPE on large hot tables.
Prefer:

- add new column with target type
- dual-write / backfill
- switch reads
- drop old column

### 3) Adding a NOT NULL constraint

Do NOT set NOT NULL before backfill.

- Add column nullable
- Backfill
- Validate no NULL remains
- Enforce NOT NULL

### 4) Adding uniqueness

- Add unique index/constraint only after ensuring no duplicates
- For existing duplicates: design conflict resolution strategy first

### 5) Building indexes safely

- Engine-specific:
  - PostgreSQL: build concurrently
  - MySQL: online DDL depends on engine/version
- Watch:
  - write amplification
  - replication lag
  - lock waits

## Tooling notes (Flyway / Liquibase agnostic)

### Flyway operational expectations

- Migrations are immutable once applied (checksum validation)
- Separate “schema history” table exists and is authoritative
- Use “validate” in CI and before production deploys
- Prefer small, ordered, reviewed versioned migrations

### Liquibase operational expectations

- Changesets have IDs/authors; checksums detect edits
- Contexts/labels allow environment-specific behavior (use sparingly and document)
- Rollbacks exist but should not be your primary “safety strategy” for large data

## Definition of Done (DoD)

- [ ] Migration scripts reviewed and idempotency assessed (where applicable)
- [ ] Backward compatibility verified (old app works with new schema)
- [ ] A backfill plan exists with throttling + retries + metrics
- [ ] Observability added: dashboard/alerts for lock waits, replication lag, error rate
- [ ] Production rollout plan documented (order of operations + abort conditions)
- [ ] Post-change verification queries defined and executed
- [ ] Contract step scheduled only after safe window

## Guardrails (What NOT to do)

- Never run irreversible destructive DDL during peak traffic without an explicit go/no-go
- Never “edit applied migrations” in-place (create a new migration instead)
- Never rely on down migrations as the primary rollback for large backfills
- Avoid big-bang backfills (single transaction updating millions of rows)
- Avoid schema changes that require full table rewrite unless you have a maintenance window

## Common failure modes & fixes

- Symptom: migration blocks writers
  - Likely cause: DDL took an exclusive lock
  - Fix: redesign with expand/contract, use online index build, add lock timeout
- Symptom: app rollback fails after schema change
  - Likely cause: migration was not backward compatible
  - Fix: ensure additive-first; app rollback must tolerate expanded schema
- Symptom: checksum mismatch
  - Likely cause: applied migration was edited
  - Fix: restore original, add a new migration; use validation early in CI

## Cursor usage (recommended)

### Minimal context to attach

- Migration folder (e.g., db/migration or liquibase/changelog)
- Entities/Repositories impacted
- The PR diff of the change (if exists)
- The production DB engine/version notes

### Agent workflow prompt snippet

“Use java-sql-schema-migrations. Propose an expand/contract plan with file paths. Identify any locking risks and required backfill jobs. Provide verification queries and a rollout runbook.”

## Suggested resources layout

- references/
  - migration-safety-checklist.md
  - db-engine-online-ddl-notes.md
- scripts/
  - backfill_template.sql (or Java batch job skeleton)
  - verify_queries.sql
  - migration_preflight.sh (optional, read-only checks)
