---
name: database-seeding
description: Seed and manage test data for dev/preview environments. Use when the user mentions seeding, creating test users, or resetting seed data.
---
# Database Seeding

## Quick Start

1. Identify target environment (dev/preview).
2. Apply seed data and create test users.
3. Validate seeded records.

## Steps

- Follow `docs/SEEDING.md`.
- Use repo assets/scripts:
  - `supabase/seed.sql`
  - `scripts/create-test-users.mjs`
  - `scripts/seed-admin-users.ts`

## Output

- Summary of seeded entities and any failures.
