<common_errors>
| Error | Cause | Fix |
|-------|-------|-----|
| "Index not found" | Using `.withIndex()` for undefined index | Add index to schema.ts, run `npx convex dev` |
| "Schema validation failed" | Document doesn't match validator | Check field types, ensure required fields present |
| "Type mismatch in validator" | Return type doesn't match `returns` | Update function return or `returns` validator |
| "Function not found" | Using wrong api/internal reference | Check import path, ensure function exported |
| "Cannot read ctx.db in action" | Actions can't access database directly | Use `ctx.runQuery` or `ctx.runMutation` |
| "Authentication provider not configured" | Missing auth provider setup | Check convex/auth.config.ts and env variables |
</common_errors>

<debug_approach>
1. Check Convex dashboard logs for stack traces
2. Run `npx convex dev` to see TypeScript errors
3. Verify schema matches function validators
</debug_approach>

<verification_checklist>
After every change:

1. **Schema validates:** Check schema.ts compiles
2. **Functions have validators:** Every query/mutation/action has `args` and `returns`
3. **Indexes exist:** Every `.withIndex()` has corresponding index in schema
4. **Types are strict:** Using `Id<"table">` not `string` for IDs
5. **Internal functions are private:** Sensitive logic uses `internal*` functions
6. **preloadQuery works:** Server components preload, client components consume

```bash
# Check Convex builds
npx convex dev
# or
npx convex deploy --dry-run
```
</verification_checklist>

<application_quality_checklist>
A well-built Convex + Next.js app:
- Uses new function syntax with explicit validators
- Has proper indexes for all query patterns (no `.filter()`)
- Separates public vs internal functions appropriately
- Uses preloadQuery for server-rendered pages
- Uses proxy.ts for auth routing (not AuthGuard components)
- Has strict TypeScript types with `Id<>` and `Doc<>`
- Handles real-time updates via Convex subscriptions
- Actions properly isolated for external API calls
</application_quality_checklist>
