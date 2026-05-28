# RLS and Security: The Zero-Trust Database (2026)

Row-Level Security (RLS) is the final line of defense against unauthorized data access.

## 1. Enabling RLS

Every table in a Supabase or Neon project MUST have RLS enabled.

```sql
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
```

## 2. Standard Policy Patterns

### Own-Data Access
```sql
CREATE POLICY "Users can manage their own projects"
ON projects
FOR ALL
USING (auth.uid() = user_id);
```

### Team-Based Access
```sql
CREATE POLICY "Team members can view shared data"
ON team_data
FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM team_members
    WHERE team_members.team_id = team_data.team_id
    AND team_members.user_id = auth.uid()
  )
);
```

## 3. Security Definers vs Security Invokers

-   **Definer**: Function runs with the owner's privileges (Dangerous, use sparingly).
-   **Invoker**: Function runs with the caller's privileges (Recommended for API integration).

## 4. Column-Level Security (CLS)

In 2026, we use Views to enforce CLS for sensitive fields like hashes or internal IDs.

```sql
CREATE VIEW public_user_profiles AS
SELECT id, name, avatar_url
FROM users
WHERE is_public = true;
```

## 5. Audit Logging (Temporal History)

Use the native PostgreSQL `system_versioning` pattern to keep a history of all changes.

```sql
ALTER TABLE sensitive_data ADD COLUMN valid_from TIMESTAMPTZ GENERATED ALWAYS AS ROW START;
ALTER TABLE sensitive_data ADD COLUMN valid_to TIMESTAMPTZ GENERATED ALWAYS AS ROW END;
ALTER TABLE sensitive_data ADD PERIOD FOR SYSTEM_TIME (valid_from, valid_to);
ALTER TABLE sensitive_data SET (system_versioning = ON);
```

---
*Updated: January 22, 2026 - 18:00*
