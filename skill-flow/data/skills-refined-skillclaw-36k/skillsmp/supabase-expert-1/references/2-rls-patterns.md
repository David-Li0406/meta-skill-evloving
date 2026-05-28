# 2. RLS Patterns & Security Advisor

**Impact: CRITICAL**

Row Level Security (RLS) is the wall between your data and the world. In 2026, RLS is enabled by default for all new tables.

## 2.1 Essential Policy Patterns

### Ownership (Private Data)
The most common pattern: only the user who created the row can see it.
```sql
create policy "Users can view their own data"
on "profiles"
for select
to authenticated
using ( (select auth.uid()) = id );
```

### Public Access (Read-Only)
Allow everyone (including unauthenticated users) to read, but not write.
```sql
create policy "Everyone can view posts"
on "posts"
for select
to anon
using ( status = 'published' );
```

### Role-Based Access Control (RBAC) with Custom Claims
Instead of joining a `user_roles` table in every query, use JWT custom claims.
```sql
-- Assuming a custom claim 'role' exists in the JWT
create policy "Admins can delete everything"
on "content"
for delete
to authenticated
using ( (auth.jwt() ->> 'role') = 'admin' );
```

## 2.2 AI-Assisted Security (Splinter)

Supabase 2026 includes **Splinter**, an AI security advisor that analyzes your RLS policies for common holes like:
- Policies that use `getSession()` logic internally.
- Overly broad `UPDATE` policies that don't check `old` values.
- Missing `CHECK` constraints on `INSERT` policies.

**Check command (CLI):**
```bash
supabase inspect rls --ai
```

## 2.3 Column-Level Security (CLS)

In 2026, you can hide specific columns from certain roles even if they have access to the row.

```sql
-- Prevent 'anon' from seeing the 'email' column
revoke select (email) on table profiles from anon;
```

## 2.4 Common Pitfalls

1.  **Circular Dependencies**: Creating a policy on `users` that queries `users` to check permissions. Use `auth.jwt()` metadata to avoid this.
2.  **Performance**: Avoid complex subqueries in `USING` clauses. Prefer `exists` checks or materialized views for complex logic.
3.  **Service Role Abuse**: Using the `service_role` key in edge functions for user-facing logic. Always prefer `Revocable Secret Keys` with scoped permissions.
