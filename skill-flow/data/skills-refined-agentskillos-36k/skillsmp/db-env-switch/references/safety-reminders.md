# Safety Reminders

## Before Switching TO Production

1. Commit any uncommitted work
2. Understand all queries will hit live data
3. Be ready to switch back quickly if issues occur
4. Never run untested migrations on production
5. Never test email sending (will send to real users!)
6. Never experiment with destructive operations

## Before Switching TO Local

1. Ensure local Supabase is running (`npx supabase status`)
2. Ensure migrations are up to date (`npx supabase db reset` if needed)
3. Remember local data may be stale
4. Be aware of schema drift if migrations haven't been applied

## After ANY Switch

1. **ALWAYS restart dev server** (`npm run dev`)
2. **ALWAYS restart worker** (`npm run worker:dev`) if using automation
3. Verify in browser console that URL matches expectation
4. Test a simple query before proceeding
5. If worker was running, verify it reconnected

## Production Safety Rules

**When working on PRODUCTION database:**

**DO NOT**:
- Run destructive queries without WHERE clauses
- Test new features without thorough local testing first
- Experiment with schema migrations
- Send test emails
- Modify large amounts of data without backups
- Use worker automation without understanding what it does

**DO**:
- Query read-only operations only (SELECTs)
- Use production for debugging ONLY
- Switch back to local as soon as possible
- Keep session short and focused
- Have a backup plan / rollback strategy
