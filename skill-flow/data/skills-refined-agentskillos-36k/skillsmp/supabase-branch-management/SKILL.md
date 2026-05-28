---
name: supabase-branch-management
description: Create, list, and clean up Supabase preview branches for isolated testing. Use when the user mentions preview branches, branch cleanup, or Supabase branching.
---
# Supabase Branch Management

## Quick Start

1. List existing branches if needed.
2. Create a new preview branch.
3. Fetch branch URL for testing.
4. Clean up branch after use.

## Steps

- Use repo scripts:
  - `scripts/create-supabase-branch.js`
  - `scripts/get-branch-id.js`
  - `scripts/get-branch-url.js`
  - `scripts/cleanup-supabase-branch.js`
- Follow `docs/supabase_branching.md`.

## Notes

- Use hosted Supabase only.
- Avoid Docker‑dependent commands.
