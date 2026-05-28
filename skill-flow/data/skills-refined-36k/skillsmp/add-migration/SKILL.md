---
name: add-migration
description: Create a new database migration with timestamp-based naming. Use when adding schema changes.
---

# Add Database Migration

Create a new database migration file with proper timestamp-based naming to avoid conflicts when working in parallel.

## Instructions

### 1. Generate timestamp for the migration

Get the current local timestamp in YYYYMMDDHHmmss format:

```bash
date +%Y%m%d%H%M%S
```

This will output something like: `20260120154111`

### 2. Create the migration file

Migrations live in `apps/backend/src/db/migrations/` and follow the naming convention:

```
YYYYMMDDHHmmss_descriptive_name.sql
```

Example: `20260120154111_add_user_preferences.sql`

**File naming guidelines:**

- Use the timestamp from step 1
- Use lowercase with underscores for the description
- Be descriptive but concise (e.g., `add_table`, `drop_column`, `add_index`)
- Never reuse an existing timestamp

### 3. Write the migration

Migrations should be idempotent where possible and include comments explaining the change:

```sql
-- Add user preferences table
-- This allows users to customize their workspace experience

CREATE TABLE IF NOT EXISTS user_preferences (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    preferences JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_preferences_user_workspace
    ON user_preferences(user_id, workspace_id);
```

### 4. Test the migration

```bash
# Apply the migration
cd apps/backend
bun run db:migrate

# Verify it worked
bun run db:status
```

## Migration Guidelines

**DO:**

- Use `CREATE TABLE IF NOT EXISTS` for new tables
- Use `CREATE INDEX IF NOT EXISTS` for new indexes
- Add comments explaining the purpose
- Keep migrations focused on one logical change
- Test migrations before committing

**DON'T:**

- Modify existing migration files (see INV-17)
- Combine unrelated schema changes
- Add data migrations without transactions
- Forget to handle down migrations if needed

## Common Patterns

**Add a column:**

```sql
-- Add display_name to streams
ALTER TABLE streams
ADD COLUMN IF NOT EXISTS display_name TEXT;
```

**Drop a column:**

```sql
-- Remove unused legacy_id column
ALTER TABLE users
DROP COLUMN IF EXISTS legacy_id;
```

**Add an index:**

```sql
-- Speed up stream lookups by workspace
CREATE INDEX IF NOT EXISTS idx_streams_workspace
    ON streams(workspace_id);
```

**Create a table:**

```sql
-- Create memos table for GAM system
CREATE TABLE IF NOT EXISTS memos (
    id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

## Troubleshooting

**Timestamp collision:**
If you somehow generate the same timestamp as an existing migration:

```bash
# Wait one second and generate a new timestamp
sleep 1 && date +%Y%m%d%H%M%S
```

**Migration fails:**

1. Check the error message in the migration output
2. Fix the SQL in your migration file
3. If the migration partially applied, you may need to manually rollback:
   ```bash
   psql postgresql://threa:threa@localhost:5454/threa
   # Manually undo the changes
   ```
4. Try running the migration again

**Need to undo a migration:**
Since migrations are immutable once committed (INV-17), create a new migration that reverts the changes:

```bash
date +%Y%m%d%H%M%S  # Get new timestamp
# Create: 20260120160000_revert_user_preferences.sql
```

## Examples

**Adding a new feature table:**

```bash
# Generate timestamp
TIMESTAMP=$(date +%Y%m%d%H%M%S)

# Create migration file
touch apps/backend/src/db/migrations/${TIMESTAMP}_add_reactions.sql

# Edit the file with your schema changes
# Then test it
cd apps/backend && bun run db:migrate
```

**Adding an index for performance:**

```bash
TIMESTAMP=$(date +%Y%m%d%H%M%S)
cat > apps/backend/src/db/migrations/${TIMESTAMP}_index_messages_stream.sql << 'EOF'
-- Add index for message queries by stream
-- Improves performance when loading stream history

CREATE INDEX IF NOT EXISTS idx_messages_stream_created
    ON messages(stream_id, created_at DESC);
EOF

cd apps/backend && bun run db:migrate
```
