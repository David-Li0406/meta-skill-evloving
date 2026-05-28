# TRR Backend 2025: Repo Context

## Database + migrations
- Supabase-managed Postgres. SQL migrations live in `supabase/migrations/`.
- Seed data: `supabase/seed.sql`.
- Local Supabase config: `supabase/config.toml` (core schema exposed in API).
- Deterministic schema docs generator: `scripts/supabase/generate_schema_docs.py`.
- No ORM migration framework detected (no Prisma/Drizzle/TypeORM); use SQL migrations.

## Current core schema (from `supabase/schema_docs/`)
Primary tables used in TRR ingestion and API:
- `core.shows` (imdb/tmdb ids, show metadata, `imdb_meta` JSON)
- `core.people`
- `core.show_cast`
- `core.episode_appearances`
- `core.episodes`
- `core.seasons`
- `core.show_images` (one row per image, source + metadata)
- `core.season_images`
- `core.episode_cast`
- `core.cast_memberships`
- `core.sync_state`

## Access patterns
- Supabase Python client is used in:
  - `api/deps.py` (client + error helpers)
  - `api/routers/*.py` (discussions, dms, shows, surveys)
  - `trr_backend/repositories/*.py` (CRUD helpers for core tables)
- Ingestion + enrichment:
  - `scripts/import_shows_from_lists.py`, `scripts/run_show_import_job.py`
  - `scripts/sync_shows.py`, `scripts/sync_seasons.py`, `scripts/sync_episodes.py`
  - `trr_backend/ingestion/show_metadata_enricher.py`

## Object storage
- Canonical storage is AWS S3 (store files in S3, metadata + access control in Postgres).

## RLS + auth
- Supabase Auth is in use; RLS is expected on `core` tables.
- `supabase/config.toml` exposes `core` schema through PostgREST.
- Service-role clients are used for ingestion and admin tasks.

## Migration compatibility
- Use SQL files in `supabase/migrations/` with safe, additive changes.
- Prefer expand/contract migrations and idempotent backfills.
