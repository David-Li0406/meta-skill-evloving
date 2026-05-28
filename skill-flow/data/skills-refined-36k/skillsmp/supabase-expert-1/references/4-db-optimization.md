# 4. Database Optimization & Revocable Keys

**Impact: MEDIUM**

Managing database performance and secret keys in 2026.

## 4.1 Revocable Secret Keys

Supabase 2026 introduces **Revocable Secret Keys** to replace the high-privilege `service_role` key.

**Workflow:**
1.  Generate a key in the Dashboard for a specific task (e.g., "Daily Cleanup Script").
2.  Assign specific scopes (e.g., `SELECT`, `DELETE` on `logs` table only).
3.  The key automatically expires or can be manually revoked if leaked.

**Why?** Static `service_role` keys are the #1 cause of catastrophic data breaches in Supabase projects.

## 4.2 Query Optimization with Index Advisor

Use the built-in Index Advisor to find slow queries and missing indexes.

```sql
-- Run this in the SQL Editor to get suggestions
explain (analyze, buffers) select * from messages where user_id = '...';
```

### Essential Indexes for Auth/RLS:
- **Foreign Keys**: Every column used in an RLS `JOIN` or `WHERE` clause MUST have an index.
- **JSONB**: Use `gin` indexes for complex filtering on metadata columns.

## 4.3 Edge Functions (Deno 2.0)

In 2026, Edge Functions are powered by Deno 2.0.

**Best Practices:**
- **Connection Pooling**: Use Supabase's built-in connection pooler (Port 6543) to avoid exhausting database connections.
- **Streaming Responses**: Use standard `ReadableStream` to stream LLM responses or large datasets back to the client.
- **Regional Execution**: Pin your functions to the same region as your database to minimize internal latency.

## 4.4 Data Migrations (Supabase CLI)

Always use versioned migrations.

```bash
# Create a new migration
supabase migration new add_orders_table

# Apply changes to local DB
supabase db reset

# Push to production
supabase db push
```
Native GitHub Actions will now verify your migrations against your RLS policies before allowing a push to production.
