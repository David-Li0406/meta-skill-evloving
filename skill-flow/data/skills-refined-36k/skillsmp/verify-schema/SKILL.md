---
name: verify-schema
description: Checks database schema integrity and data consistency, specifically focusing on critical columns and legacy data migration.
---

# Verify Database Schema

This skill provides tools to verify that the database schema matches application expectations and that data is correctly migrated from legacy columns.

## Usage

Run the check script from the project root:

```bash
node skills/verify-schema/scripts/check-columns.js
```

## Checks Performed

- **Connection**: Verifies connection to Supabase.
- **Legacy Data**: Checks `photo_libraries` for rows where `google_drive_folder_id` is NULL but legacy `gdrive_folder_id` is set.
- **Column Existence**: Verifies critical columns exist (future expansion).

## Prevention Strategy
Use this skill before deployments or after database migrations to ensure application logic will access the correct data fields.
