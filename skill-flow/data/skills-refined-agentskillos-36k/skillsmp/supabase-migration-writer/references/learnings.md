# Supabase Migration Writer Learnings

## Critical: Type Synchronization

### The Problem
When creating migrations that add:
- New tables
- New RPC functions
- New columns

The TypeScript types file (`apps/raamattu-nyt/src/integrations/supabase/types.ts`) does NOT automatically update. This causes:
1. TypeScript errors in IDE
2. Lovable Cloud build failures
3. Type assertion workarounds (`as any`) scattered through code

### Required Actions After Migration

**After creating ANY migration that adds tables, columns, or RPC functions:**

1. **Regenerate types** (if Supabase CLI available):
   ```bash
   npx supabase gen types typescript --project-id iryqgmjauybluwnqhxbg > apps/raamattu-nyt/src/integrations/supabase/types.ts
   ```

2. **Or manually add types** to `types.ts`:
   - For new tables: Add Row, Insert, Update types
   - For new RPC functions: Add to `Functions` section
   - For new columns: Add to existing table types

3. **For RPC functions not in generated types**, add manual type definitions:
   ```typescript
   // In a separate types file or at usage site
   // apps/raamattu-nyt/src/integrations/supabase/types.ts or types/rpc.ts

   export interface DeleteErrorReportParams {
     p_id: string;
   }
   ```

### Common Patterns Causing Type Drift

| Migration Action | Type Impact | Fix |
|-----------------|-------------|-----|
| `CREATE TABLE` | Missing Row/Insert/Update | Regenerate or add manually |
| `CREATE FUNCTION` | Missing from Functions | Add function signature |
| `ALTER TABLE ADD COLUMN` | Missing from Row/Insert/Update | Add to all three types |
| `DROP TABLE/FUNCTION` | Orphaned types | Remove from types.ts |

### Workaround Pattern (When Types Can't Be Updated)

When immediate type regeneration isn't possible, use this pattern:

```typescript
// Use type assertion with explicit any cast and biome-ignore
// biome-ignore lint/suspicious/noExplicitAny: RPC not in generated types
const { data, error } = await supabase.rpc("new_function" as any, {
  p_param: value,
});
```

**Important:** Add a comment explaining WHY the assertion is needed.

## Anti-Patterns

| Don't | Do Instead | Reason |
|-------|------------|--------|
| Create migration without updating types | Always update types.ts after migration | Prevents build failures |
| Use `as any` without comment | Add biome-ignore with explanation | Maintains code clarity |
| Assume Lovable will auto-sync types | Manually verify types are current | Lovable uses the committed types.ts |

## Sticky Fixes

- **Lovable build fails with type errors**: Types.ts is out of sync. Regenerate from Supabase or manually add missing types.
- **RPC function "does not exist"**: Either migration not applied OR function not in types. Check both.
- **Column not in Update type**: Supabase generates separate Row/Insert/Update types. All three need the column.
