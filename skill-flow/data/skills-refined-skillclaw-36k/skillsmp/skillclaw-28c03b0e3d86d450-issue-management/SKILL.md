---
name: issue-management
description: Use this skill when you need to manage issue statuses or retrieve bug issue lists in a Supabase database.
---

# Skill body

## Purpose

This skill allows you to update the status of issues and retrieve lists of bug issues from the Supabase database.

## Workflow

### 1. Update Issue Status

To change the status of an issue in the Supabase `issues` table, use the following methods:

#### Using Supabase Client

```typescript
// Supabase client to update issue status
const { data, error } = await supabase
  .from('issues')
  .update({ status: 'in_progress' }) // Change to desired status
  .eq('number', 123) // Issue number
  .eq('office_id', officeId) // Office ID
  .select('number, title, status')
  .single();
```

#### Using SQL Directly

```sql
-- Update issue status directly
UPDATE issues
SET status = 'in_progress', updated_at = NOW()
WHERE number = 123 AND office_id = '{office_uuid}'
RETURNING number, title, status;
```

#### Using Helper Function (Recommended)

```sql
-- Call the helper function to update status and log history
SELECT * FROM update_issue_status(
  123,                    -- issue_number
  '{office_uuid}'::uuid,  -- office_id
  'in_progress',          -- new_status
  '{actor_uuid}'::uuid    -- changed_by (optional)
);
```

### 2. Retrieve Bug Issues

To list bug issues from the Supabase database, use the following methods:

#### Using Supabase Client

```typescript
// Supabase client to retrieve bug issues
const { data: bugs, error } = await supabase
  .from('bug_list')
  .select('*')
  .order('created_at', { ascending: false });
```

#### Using SQL Directly

```sql
-- Retrieve bug issues from the bug_list view
SELECT * FROM bug_list;

-- Or directly from the issues table
SELECT
  i.number,
  i.title,
  i.status,
  ap.name as assignee_name,
  i.created_at
FROM issues i
LEFT JOIN agent_personas ap ON i.assignee_id = ap.id
WHERE i.type = 'bug' AND i.state = 'open'
ORDER BY i.created_at DESC;
```

### 3. Check Current Status

To check the current status of an issue:

```sql
-- Check current status of an issue
SELECT number, title, status
FROM issues
WHERE number = 123 AND office_id = '{office_uuid}';
```

### 4. Bulk Update Issue Status

To change the status of multiple issues at once:

```sql
-- Bulk update status for issues with a specific label
UPDATE issues
SET status = 'in_progress', updated_at = NOW()
WHERE 'project:차곡' = ANY(labels) AND state = 'open' AND office_id = '{office_uuid}'
RETURNING number, title, status;
```

## Status Options

| Status         | Description          |
|----------------|----------------------|
| backlog        | Initial state        |
| todo           | To-do list           |
| in_progress    | In development        |
| review         | Awaiting code review  |
| testing        | In QA testing         |
| done           | Task completed        |

## Output Format for Bug Issues

```markdown
## 🐛 Bug Issue Status (Based on Supabase DB)

| #   | Title                | Status       | Assignee   | Created At          |
|-----|----------------------|--------------|------------|---------------------|
| #123| API response delay    | in_progress  | Developer  | 2025-12-01          |
| #456| Button click failure   | todo         | Frontend   | 2025-12-05          |

---
**Total 2 Open Bug Issues**
```