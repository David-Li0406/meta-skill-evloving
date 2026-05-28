# Local Mode - Detailed Steps

Local testing workflow for database migrations. 6 steps, no commits, no production changes.

## Step 1: Verify Migration Date

Check the migration filename and confirm the timestamp:

```bash
ls -la supabase/migrations/*.sql | tail -5
```

Parse the timestamp from filename format: `YYYYMMDDHHMMSS_description.sql`

Use AskUserQuestion to confirm:
```typescript
{
  questions: [{
    question: "Found migration '20251224000000_salesforce_connections.sql' dated 2025-12-24. Is this date correct?",
    header: "Date Check",
    options: [
      { label: "Yes, date is correct", description: "Proceed with this timestamp" },
      { label: "No, wrong date", description: "Stop - rename migration file first" }
    ],
    multiSelect: false
  }]
}
```

## Step 2: Reset Local Database

Run the database reset to apply all migrations:

```bash
npx supabase db reset
```

Expected output:
```
Resetting local database...
Applying migrations...
  20251003165051_bootstrap_admin.sql
  20251025030217_change_duration_days.sql
  20251224000000_salesforce_connections.sql  ← NEW
Seeding data...
Local database ready.
```

If this fails, see [error-recovery.md](error-recovery.md#local-test-fails).

## Step 3: Run pgTAP Tests

Verify database health with pgTAP tests:

```bash
npm run test:sql
```

This runs all tests in `supabase/tests/pgtap/`:
- `00-schema/` - Schema validation
- `20-rls/` - RLS policy tests

If tests fail, stop and show the failure. Fix before proceeding.

## Step 4: Check for Missing Tests

Analyze the migration for new tables/policies that need tests:

1. Read migration file, identify:
   - `CREATE TABLE` statements
   - `CREATE POLICY` statements
   - New functions/triggers

2. Check existing tests in `supabase/tests/pgtap/`

3. If new tables found, ask user:
```typescript
{
  questions: [{
    question: "Migration creates new table 'salesforce_connections'. Create pgTAP tests?",
    header: "Tests",
    options: [
      { label: "Yes, create tests first", description: "Create schema and RLS tests" },
      { label: "No, skip tests", description: "Proceed without tests" }
    ],
    multiSelect: false
  }]
}
```

Test file naming:
- Schema: `supabase/tests/pgtap/00-schema/XX-table-name.test.sql`
- RLS: `supabase/tests/pgtap/20-rls/XX-table-name-rls.test.sql`

## Step 5: Restart Worker

**Critical**: When database resets, the worker's PostgreSQL connection becomes invalid but doesn't auto-reconnect. Worker appears running but stops processing events.

Find and kill the worker:

```bash
# Windows: Find worker PID
wmic process where "commandline like '%worker%' and name='node.exe'" get processid

# Kill stuck worker
taskkill //F //PID [PID]

# Restart worker
npm run worker:dev
```

Verify worker is processing:
```
[AutomationWorker] Starting automation worker...
[AutomationWorker] Listening for automation_outbox notifications
[AutomationWorker] Started polling every 2000ms
```

## Step 6: Generate Types Locally

Generate TypeScript types from the LOCAL database (not production):

```bash
npx supabase gen types typescript --local > src/integrations/supabase/types.ts
```

**Note**: These types are NOT committed in local mode - they're for local development only.

## Final Output

After successful completion:

```
Local Migration Test COMPLETE!

Migration: 20251224000000_salesforce_connections.sql
Date: 2025-12-24

Results:
  Database reset successful (seed.sql creates test users + analytics data)
  pgTAP tests passed
  Worker restarted
  Types generated (local)

Test Accounts:
  Admin: zcramer@gmail.com / 123123
  User: b@b.com / 123123

Next Steps:
  1. Test in browser at http://localhost:8080
  2. Log in with a test account
  3. Verify new features work
  4. When ready to deploy, say "push migration to production"

Migration NOT committed to Git yet
Production database NOT changed
```
