# RLS Policy Patterns Reference

## User-Owned Data (Full CRUD)

```sql
ALTER TABLE public.user_notes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own notes"
ON public.user_notes FOR SELECT TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "Users can insert own notes"
ON public.user_notes FOR INSERT TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own notes"
ON public.user_notes FOR UPDATE TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can delete own notes"
ON public.user_notes FOR DELETE TO authenticated
USING (user_id = auth.uid());

-- Optional: Admin override
CREATE POLICY "Admins can view all notes"
ON public.user_notes FOR SELECT TO authenticated
USING (public.has_role(auth.uid(), 'admin'));
```

## Public Read, Admin Write

```sql
ALTER TABLE bible_schema.topical_topics ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public can read topics"
ON bible_schema.topical_topics FOR SELECT TO anon, authenticated
USING (true);

CREATE POLICY "Admins can insert topics"
ON bible_schema.topical_topics FOR INSERT TO authenticated
WITH CHECK (public.has_role(auth.uid(), 'admin'));

CREATE POLICY "Admins can update topics"
ON bible_schema.topical_topics FOR UPDATE TO authenticated
USING (public.has_role(auth.uid(), 'admin'))
WITH CHECK (public.has_role(auth.uid(), 'admin'));

CREATE POLICY "Admins can delete topics"
ON bible_schema.topical_topics FOR DELETE TO authenticated
USING (public.has_role(auth.uid(), 'admin'));
```

## Admin-Only Table (Audit Logs)

```sql
ALTER TABLE public.admin_audit_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Admins can view audit logs"
ON public.admin_audit_logs FOR SELECT TO authenticated
USING (public.has_role(auth.uid(), 'admin'));

CREATE POLICY "System can insert audit logs"
ON public.admin_audit_logs FOR INSERT TO authenticated
WITH CHECK (true); -- Controlled by SECURITY DEFINER function

-- No UPDATE or DELETE - audit logs are immutable
```

## Role-Based Access

```sql
CREATE POLICY "moderator_access"
ON table_name FOR SELECT, UPDATE TO authenticated
USING (
  public.has_role(auth.uid(), 'admin') OR
  public.has_role(auth.uid(), 'moderator')
);
```

## Admin Helper Functions

### Option 1: has_role() (existing in public schema)

```sql
CREATE FUNCTION public.has_role(_user_id uuid, _role app_role)
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
SET search_path TO 'public'
AS $$
  SELECT EXISTS (
    SELECT 1 FROM user_roles
    WHERE user_id = _user_id AND role = _role
  )
$$;
```

### Option 2: Schema-specific is_admin() (recommended for cleaner policies)

Create a helper in each schema for cleaner policy conditions:

```sql
CREATE OR REPLACE FUNCTION bible_schema.is_admin()
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public, extensions, pg_temp
AS $$
  SELECT public.has_role(auth.uid(), 'admin');
$$;

-- Restrict access
REVOKE ALL ON FUNCTION bible_schema.is_admin() FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION bible_schema.is_admin() TO authenticated;
```

**Benefits:**
- Cleaner policy conditions: `bible_schema.is_admin()` vs `public.has_role(auth.uid(), 'admin')`
- Centralized admin check logic
- Can add caching or additional checks later

## RLS Performance: Indexes

Always create indexes on columns used in RLS conditions:

```sql
-- User-owned tables
CREATE INDEX IF NOT EXISTS idx_tablename_user_id ON schema.tablename(user_id);

-- Owner-based tables
CREATE INDEX IF NOT EXISTS idx_tablename_created_by ON schema.tablename(created_by);

-- Status-filtered tables
CREATE INDEX IF NOT EXISTS idx_tablename_status ON schema.tablename(status);

-- Partial indexes for common filters
CREATE INDEX IF NOT EXISTS idx_tablename_approved
  ON schema.tablename(is_approved) WHERE is_approved = true;
```

## SECURITY DEFINER Functions

For privileged operations:

```sql
CREATE FUNCTION delete_user_by_admin(target_user_id uuid)
RETURNS boolean
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path TO 'public'
AS $$
BEGIN
  IF NOT public.has_role(auth.uid(), 'admin') THEN
    RAISE EXCEPTION 'Only admins can delete users';
  END IF;

  IF target_user_id = auth.uid() THEN
    RAISE EXCEPTION 'Cannot delete own account';
  END IF;

  DELETE FROM auth.users WHERE id = target_user_id;
  RETURN true;
END;
$$;
```

## Testing RLS Policies

### Test as User
```sql
SET ROLE authenticated;
SET request.jwt.claims.sub TO 'user-uuid-here';
SELECT * FROM user_notes; -- Should only see own notes
RESET ROLE;
```

### Test as Anon
```sql
SET ROLE anon;
SELECT * FROM verses; -- Should work for public data
SELECT * FROM user_notes; -- Should return empty/error
RESET ROLE;
```

### Test Admin Access
```sql
SELECT public.has_role('admin-user-uuid', 'admin'); -- true
SELECT public.has_role('regular-user-uuid', 'admin'); -- false
```

## Common Vulnerabilities

| Issue | Example | Fix |
|-------|---------|-----|
| No RLS enabled | `CREATE TABLE user_data (...)` | `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` |
| Missing auth.uid() check | `USING (true)` on user data | `USING (user_id = auth.uid())` |
| Service key in client | `createClient(url, SERVICE_ROLE_KEY)` | Use anon key only |
| No admin check on roles | Direct INSERT to user_roles | Use SECURITY DEFINER function |
| `FOR ALL` policy | `CREATE POLICY ... FOR ALL` | Use explicit INSERT/UPDATE/DELETE policies |
| `TO public` role | `CREATE POLICY ... TO public` | Use `TO anon` or `TO authenticated` explicitly |
| Missing WITH CHECK | `FOR UPDATE ... USING (...)` only | Add `WITH CHECK (same_condition)` |
| No RLS indexes | RLS on user_id without index | `CREATE INDEX ... ON table(user_id)` |
| anon read on sensitive data | `GRANT SELECT TO anon` on user logs | Revoke anon, use authenticated only |

## Validation Checklist

### User Data Tables
- [ ] RLS enabled
- [ ] SELECT checks `auth.uid()`
- [ ] INSERT enforces `user_id = auth.uid()`
- [ ] UPDATE/DELETE protect user data
- [ ] Admin override if needed

### Public Data Tables
- [ ] RLS enabled
- [ ] Public SELECT (`USING (true)`)
- [ ] Admin-only write policies

### Admin Tables
- [ ] RLS enabled
- [ ] All policies check `has_role()`
- [ ] Audit logging in place
