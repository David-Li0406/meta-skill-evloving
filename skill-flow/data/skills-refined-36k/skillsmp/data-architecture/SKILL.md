---
name: data-architecture
description: Standards for Firestore schemas, migrations, and data integrity. Use when modifying database structures.
---

# Data Architecture

Detailed instructions for Firestore schema design, data migration, and seeding.

## When to use this skill

- Use this when modifying `server/src/seed.ts` or `src/types`.
- This is helpful for adding new collections, fields, or changing data relationships.
- Use this when debugging data sync issues or "missing field" errors.

## How to use it

### 1. Schema Integrity

- **Types First**: Define the interface in `src/types` before writing any DB code.
- **Seed Truth**: The `seed.ts` file is the ground truth. If a field exists in Types but not Seed, it's a bug.
- **No Deletions**: Prefer `deprecated: true` flags over deleting fields to prevent runtime crashes on old clients.

### 2. Migrations & Seeding

- **Dry Run Mandate**: Before updating `seed.ts` or running a migration, perform a comparison scan. Verify that incremental changes (e.g., adding a venue) do not accidentally wipe or regress existing records.
- **Idempotency**: All migration scripts must be safe to run multiple times (check if data exists before writing).
- **Batching**: Use `db.batch()` for multi-document updates to ensure atomicity.

### 3. Region

- Firestore must be in `us-west1`.
