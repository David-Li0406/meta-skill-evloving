---
name: supabase-patterns
description: Supabase client patterns for StepLeague, including MCP server usage, auth deadlock prevention, admin client usage, and session handling. Use when working with database queries, authentication, MCP tools, or Supabase client code. Keywords: database, MCP, auth, session, RLS, deadlock, timeout, query, migration.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.1"
  project: "stepleague"
---

# Supabase Patterns Skill

## Overview

StepLeague uses Supabase for:
- PostgreSQL database with Row Level Security (RLS)
- Authentication (email, Google OAuth)
- Storage (images, attachments)

---

## Supabase MCP Server (CRITICAL)

> **This project has MCP access to Supabase.** Use it for queries, migrations, and verification.

### Available MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp_supabase-mcp-server_list_projects` | List all Supabase projects |
| `mcp_supabase-mcp-server_list_tables` | List tables in a schema |
| `mcp_supabase-mcp-server_execute_sql` | Run SQL queries |
| `mcp_supabase-mcp-server_apply_migration` | Apply DDL migrations |
| `mcp_supabase-mcp-server_list_migrations` | List existing migrations |
| `mcp_supabase-mcp-server_get_logs` | Get service logs |
| `mcp_supabase-mcp-server_search_docs` | Search Supabase documentation |
| `mcp_supabase-mcp-server_get_project` | Get project details |

### ⚠️ Common MCP Failures & Solutions (EXPANDED)

| Problem | Cause | Solution |
|---------|-------|----------|
| **"Connection refused"** | MCP server not running | Restart Antigravity IDE, check `mcp_config.json` |
| **"Timeout" / No response** | Query too complex, large result | Add `LIMIT 10`, simplify query, break into parts |
| **"Project not found"** | Wrong project_id | Run `list_projects` first to get correct ID |
| **"Permission denied"** | RLS blocking | Use `execute_sql` (bypasses RLS) |
| **SQL syntax error** | Wrong SQL dialect | Use PostgreSQL syntax (e.g., `ILIKE` not `LIKE`, `::text` casts) |
| **Migration conflicts** | Duplicate migration name | Check `list_migrations` first, use unique timestamps |
| **No output returned** | Query executed but empty | Query succeeded - data may not exist, verify table |
| **"Invalid API key"** | Token expired/wrong | Check Supabase dashboard for new API key |
| **Intermittent failures** | Network/rate limits | Retry after 30s, reduce query frequency |

### MCP Troubleshooting Flowchart

```
MCP Tool Not Working?
├─ No response at all
│  ├─ Check: Is Antigravity MCP enabled? (Settings → MCP)
│  ├─ Check: Is `mcp_config.json` correct?
│  └─ Try: Restart Antigravity IDE
├─ Returns error message
│  ├─ "project not found" → Run list_projects first
│  ├─ "permission denied" → Use execute_sql, not user queries
│  └─ "timeout" → Add LIMIT, break query into parts
└─ Returns empty
   ├─ Query succeeded, no matching data
   └─ Verify table exists with list_tables
```

### Best Practices for MCP

1. **Always list projects first** to get the correct project_id
2. **Use LIMIT 10** on SELECT queries to avoid timeouts
3. **For DDL changes, use apply_migration** not execute_sql
4. **Check existing migrations** before creating new ones
5. **If MCP fails, document what you tried** and fallback to manual options
6. **Verify changes after making them** - query the data to confirm

### Example: Safe MCP Query

```
// Step 1: List projects to get ID
mcp_supabase-mcp-server_list_projects

// Step 2: Query with LIMIT (avoid timeouts)
mcp_supabase-mcp-server_execute_sql({
  project_id: "your-project-id",
  query: "SELECT * FROM users LIMIT 10"
})

// Step 3: Verify data after insert/update
mcp_supabase-mcp-server_execute_sql({
  project_id: "your-project-id",
  query: "SELECT id, subject, board_status FROM feedback WHERE id = 'uuid-here'"
})
```

### When MCP Fails Completely

If MCP is unavailable:

1. **Document the issue** - Note error message and what you tried
2. **Use API endpoints** - Many operations can be done via app APIs:
   - `/api/admin/kanban` for feedback/roadmap
   - `/api/admin/settings` for app settings
3. **Provide SQL for user** - Write the SQL and ask user to run in Supabase dashboard

---

## Critical Rules

### 1. NEVER Use `<Database>` Generics

```typescript
// ❌ WRONG - causes cascading 'never' type errors
const supabase = createServerClient<Database>(...);

// ✅ CORRECT - untyped
const supabase = await createServerSupabaseClient();
const { data } = await supabase.from("leagues").select("*");
const leagues = (data || []).map((l: any) => ({ ... }));
```

### 2. Use adminClient in API Routes

```typescript
import { createServerSupabaseClient, createAdminClient } from "@/lib/supabase/server";

export async function POST(request: Request) {
  // Regular client for auth only
  const supabase = await createServerSupabaseClient();
  const { data: { user } } = await supabase.auth.getUser();
  
  // Admin client for database operations (bypasses RLS)
  const adminClient = createAdminClient();
  const { data } = await adminClient.from("table").select("*");
}
```

### 3. Use withApiHandler (Preferred)

Reference the `api-handler` skill - it handles all client creation for you.

---

## Auth Deadlocks (CRITICAL)

> **For detailed auth patterns, see the [`auth-patterns`](../auth-patterns/SKILL.md) skill.**

### Quick Reminder

| Method | Safety |
|--------|--------|
| `getSession()` on client | ❌ **NEVER** - Can deadlock |
| `getUser()` on server | ✅ Safe |
| `onAuthStateChange` | ✅ Safe for client |
| Cookie parsing | ✅ Safe fallback |

The `auth-patterns` skill covers:
- getUser vs getSession decision flowchart
- Client-side auth patterns (onAuthStateChange)
- Background task fallbacks (cookie parsing)
- Token expiry validation
- Session timeout handling
- Debugging auth issues

---

## Client Types

| Client | Location | Use Case |
|--------|----------|----------|
| `createServerSupabaseClient` | `@/lib/supabase/server` | Server-side, respects RLS |
| `createAdminClient` | `@/lib/supabase/server` | Server-side, bypasses RLS |
| `createBrowserClient` | `@/lib/supabase/client` | Client-side components |

### When to Use Each

| Scenario | Client |
|----------|--------|
| API route - auth check | `createServerSupabaseClient` |
| API route - database ops | `createAdminClient` |
| Server component data fetching | `createServerSupabaseClient` |
| Client component | `createBrowserClient` |
| Background job / admin task | `createAdminClient` |

---

## RLS (Row Level Security)

### The Rule

**All application queries in API routes should use `adminClient`** to bypass RLS.

**Why?** RLS adds complexity and potential for access issues. Server-side code should handle authorization explicitly.

### When RLS Still Applies

- Direct Supabase client calls from browser (realtime, etc.)
- Supabase Edge Functions

### Pattern

```typescript
export const POST = withApiHandler({
  auth: 'required',  // Handler verifies auth
}, async ({ user, adminClient }) => {
  // Admin client bypasses RLS - we already verified auth above
  const { data } = await adminClient
    .from("submissions")
    .insert({ user_id: user.id, ... })
    .select()
    .single();
  
  return { data };
});
```

---

## Migrations

### File Naming

```
supabase/migrations/YYYYMMDDHHMMSS_description.sql
```

Example: `20260116114200_add_skills_reference.sql`

### Migration via MCP

```typescript
mcp_supabase-mcp-server_apply_migration({
  project_id: "your-project-id",
  name: "add_skills_reference",
  query: "ALTER TABLE users ADD COLUMN skills_enabled BOOLEAN DEFAULT true;"
})
```

### Best Practices

1. **Always check existing migrations first** with `list_migrations`
2. **Use descriptive names** - what the migration does
3. **Include both UP and DOWN** logic in comments
4. **Test locally first** if possible

---

## Session Handling

### The Problem

Long-running operations (batch uploads, image processing) can cause session timeouts.

### Solution: Session Caching

```typescript
// Don't call getUser() repeatedly in loops
const user = context.user; // Already resolved by withApiHandler

for (const item of items) {
  // Use cached user, not new auth call
  await processItem(item, user.id);
}
```

### Timeout Prevention

```typescript
// Add timeout wrapper
const withTimeout = <T>(promise: Promise<T>, ms: number): Promise<T> => {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) => 
      setTimeout(() => reject(new Error('Timeout')), ms)
    )
  ]);
};

const result = await withTimeout(
  supabase.from("table").select("*"),
  5000 // 5 second timeout
);
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `src/lib/supabase/server.ts` | Server client creation |
| `src/lib/supabase/client.ts` | Browser client creation |
| `src/lib/auth/sessionCache.ts` | Session caching utilities |
| `src/components/providers/AuthProvider.tsx` | Auth state management |
| `supabase/migrations/` | All database migrations |

---

## Common Queries

### Get User Profile

```typescript
const { data: profile } = await adminClient
  .from("users")
  .select("*")
  .eq("id", userId)
  .single();
```

### Check Membership

```typescript
const { data: membership } = await adminClient
  .from("memberships")
  .select("role")
  .eq("user_id", userId)
  .eq("league_id", leagueId)
  .single();
```

### Insert with Return

```typescript
const { data, error } = await adminClient
  .from("submissions")
  .insert({ user_id, for_date, steps })
  .select()
  .single();

if (error) throw new AppError({
  code: ErrorCode.DB_INSERT_FAILED,
  message: error.message,
  context: { table: 'submissions' }
});
```

---

## Related Skills

- `api-handler` - Uses adminClient automatically
- `error-handling` - Database error codes
- `architecture-philosophy` - Why we bypass RLS in API routes
