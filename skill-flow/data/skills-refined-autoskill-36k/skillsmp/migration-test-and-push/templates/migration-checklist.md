# Database Migration Pre-Flight Checklist

Use this checklist before testing and deploying migrations to ensure safety and prevent production incidents.

## Pre-Deployment Checklist

### Migration Quality

- [ ] **Idempotent**: Migration can run multiple times safely
  ```sql
  -- Use IF NOT EXISTS / IF EXISTS patterns
  DO $$
  BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns ...) THEN
      ALTER TABLE ... ADD COLUMN ...;
    END IF;
  END $$;
  ```

- [ ] **Validation**: Migration includes checks and raises exceptions on failure
  ```sql
  -- Validate changes worked
  IF NOT EXISTS (...expected state...) THEN
    RAISE EXCEPTION 'Migration failed validation';
  END IF;
  ```

- [ ] **Reversible**: You know how to rollback if needed
  - Document rollback SQL in comments
  - Or plan for new "undo" migration

### Security

- [ ] **RLS Policies**: New tables have row-level security policies
  ```sql
  ALTER TABLE new_table ENABLE ROW LEVEL SECURITY;

  CREATE POLICY "Users can view own org data"
    ON new_table FOR SELECT
    USING (organization_id = auth.uid_organization_id());
  ```

- [ ] **Multi-Tenant Isolation**: All queries filter by `organization_id`
  - Critical for EOS Implementer Hub (300+ orgs)
  - Prevents data leaks between organizations

- [ ] **Permissions**: Functions have proper security definer/invoker settings

### Data Integrity

- [ ] **Constraints**: Appropriate NOT NULL, CHECK, UNIQUE, FOREIGN KEY constraints
  ```sql
  ALTER TABLE users ADD CONSTRAINT email_format
    CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');
  ```

- [ ] **Defaults**: Sensible default values for new columns
  - Especially important when adding columns to existing tables with data

- [ ] **Indexes**: Performance indexes for new query patterns
  ```sql
  CREATE INDEX CONCURRENTLY idx_sessions_org_date
    ON sessions(organization_id, created_at DESC);
  ```

### Testing

- [ ] **Local Test**: Migration passes `npx supabase db reset`
  - Tests migration in isolation
  - Catches syntax errors, constraint violations

- [ ] **Realistic Data**: Tested with production-like data volume
  - Not just empty tables
  - Consider edge cases (NULL values, duplicates, etc.)

- [ ] **Related Queries**: Tested queries that depend on migrated tables
  - Application still works after migration
  - No broken queries or missing columns

### Production Readiness

- [ ] **Timing**: Migration during low-traffic window (if possible)
  - Reduces impact of potential downtime
  - Easier to rollback if needed

- [ ] **Monitoring**: Ready to watch logs and metrics after deployment
  - Error rates
  - Query performance
  - User reports

- [ ] **Rollback Plan**: Know what to do if migration breaks production
  - New migration to undo changes
  - Or restore from backup (last resort)

- [ ] **Communication**: Team knows migration is happening
  - Especially for potentially disruptive changes
  - Coordinate with team members who might be deploying code

## Common Migration Patterns

### Adding Column to Existing Table

```sql
DO $$
BEGIN
    -- Check if column exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'users' AND column_name = 'timezone'
    ) THEN
        -- Add column with default (safe for existing rows)
        ALTER TABLE users ADD COLUMN timezone VARCHAR(50) DEFAULT 'America/New_York';

        -- Validate
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_name = 'users' AND column_name = 'timezone'
        ) THEN
            RAISE EXCEPTION 'Failed to add timezone column';
        END IF;

        RAISE NOTICE 'Added timezone column to users table';
    ELSE
        RAISE NOTICE 'timezone column already exists (skipping)';
    END IF;
END $$;
```

### Creating New Table with RLS

```sql
-- Create table (idempotent)
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    preferences JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, organization_id)
);

-- Enable RLS
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- Create policies
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE tablename = 'user_preferences' AND policyname = 'Users can view own prefs'
    ) THEN
        CREATE POLICY "Users can view own prefs"
            ON user_preferences FOR SELECT
            USING (user_id = auth.uid() AND organization_id = auth.uid_organization_id());
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE tablename = 'user_preferences' AND policyname = 'Users can update own prefs'
    ) THEN
        CREATE POLICY "Users can update own prefs"
            ON user_preferences FOR UPDATE
            USING (user_id = auth.uid() AND organization_id = auth.uid_organization_id());
    END IF;
END $$;

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_user_prefs_user_id
    ON user_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_user_prefs_org_id
    ON user_preferences(organization_id);

-- Validate table was created
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_name = 'user_preferences'
    ) THEN
        RAISE EXCEPTION 'Failed to create user_preferences table';
    END IF;
    RAISE NOTICE 'user_preferences table created successfully';
END $$;
```

### Modifying Existing Column

```sql
DO $$
BEGIN
    -- Change column type (with validation)
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'sessions'
        AND column_name = 'duration_days'
        AND data_type = 'integer'
    ) THEN
        -- Change integer to numeric for fractional days
        ALTER TABLE sessions ALTER COLUMN duration_days TYPE NUMERIC(10,2);

        -- Validate change
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_name = 'sessions'
            AND column_name = 'duration_days'
            AND data_type = 'numeric'
        ) THEN
            RAISE EXCEPTION 'Failed to change duration_days to numeric';
        END IF;

        RAISE NOTICE 'Changed duration_days from integer to numeric(10,2)';
    ELSE
        RAISE NOTICE 'duration_days already numeric or does not exist (skipping)';
    END IF;
END $$;
```

## Post-Deployment Verification

After migration completes:

- [ ] **UI Test**: Test affected features in production interface
- [ ] **Error Logs**: Check for new errors or warnings
- [ ] **Performance**: Monitor query performance metrics
- [ ] **User Reports**: Watch for user complaints about broken features

## If Something Goes Wrong

### Immediate Actions:

1. **Assess Impact**: How many users/features affected?
2. **Check Logs**: What errors are occurring?
3. **Notify Team**: Alert developers and stakeholders
4. **Rollback Decision**: Can we fix forward or need to rollback?

### Rollback Options:

**Option 1: Fix-Forward Migration** (preferred)
- Create new migration that fixes the issue
- Test locally, then deploy quickly
- Preserves data, no downtime

**Option 2: Manual SQL Fix** (emergency)
- Connect to production database
- Run corrective SQL manually
- Document exactly what was done
- Create migration to match manual changes

**Option 3: Restore from Backup** (last resort)
- Only if data corrupted beyond repair
- Results in data loss (changes since backup)
- Requires downtime

## Remember

- **Git before database**: Always commit to Git BEFORE pushing to production
- **Test locally first**: Catch errors before they reach users
- **Get approval**: Never push to production without confirmation
- **Monitor after**: Watch for issues after deployment
- **Learn from mistakes**: Document what went wrong and how to prevent it

This checklist is your safety net. Use it every time! 🛡️
