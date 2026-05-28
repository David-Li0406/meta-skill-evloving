---
name: issue-management
description: Use this skill when you need to manage issue statuses and retrieve bug reports from a Supabase database.
---

# Body of the merged SKILL.md

## Purpose

This skill allows you to update the status of issues and retrieve bug reports from the Supabase `issues` table. It supports status changes and bug filtering based on various criteria.

## Status Management

### Status Options

| Status | Description |
|--------|-------------|
| backlog | Initial state |
| todo | To-do list |
| in_progress | In development |
| review | Awaiting code review |
| testing | QA testing phase |
| done | Task completed |

### Workflow for Updating Status

1. **Update Status in Supabase**

```typescript
// Update issue status using Supabase client
const { data, error } = await supabase
  .from('issues')
  .update({ status: '<new_status>' })
  .eq('number', <issue_number>)
  .eq('office_id', <office_id>)
  .select('number, title, status')
  .single();
```

2. **Direct SQL Update (MCP Server)**

```sql
-- Update status of a single issue
UPDATE issues
SET status = '<new_status>',
    updated_at = NOW()
WHERE number = <issue_number>
  AND office_id = '<office_uuid>'
RETURNING number, title, status;
```

3. **Using the update_issue_status Function (Recommended)**

```sql
-- Call the status change function (automatically records history)
SELECT * FROM update_issue_status(
  <issue_number>,                    -- issue_number
  '<office_uuid>'::uuid,            -- office_id
  '<new_status>',                    -- new_status
  '<actor_uuid>'::uuid              -- changed_by (optional)
);
```

4. **Check Current Status**

```sql
-- Check current status
SELECT number, title, status
FROM issues
WHERE number = <issue_number>
  AND office_id = '<office_uuid>';
```

### Bulk Status Change

```sql
-- Bulk update status for issues with a specific label
UPDATE issues
SET status = '<new_status>',
    updated_at = NOW()
WHERE '<label>' = ANY(labels)
  AND state = 'open'
  AND office_id = '<office_uuid>'
RETURNING number, title, status;
```

## Bug Retrieval

### Workflow for Retrieving Bugs

1. **Retrieve Bugs from Supabase**

```typescript
// Retrieve bug issues using Supabase client
const { data: bugs, error } = await supabase
  .from('bug_list')
  .select('*')
  .order('created_at', { ascending: false });
```

2. **Direct SQL Query (MCP Server)**

```sql
-- Query bug_list view
SELECT * FROM bug_list;

-- Or directly from issues table
SELECT
  i.number,
  i.title,
  i.status,
  ap.name as assignee_name,
  i.created_at
FROM issues i
LEFT JOIN agent_personas ap ON i.assignee_id = ap.id
WHERE i.type = 'bug'
  AND i.state = 'open'
ORDER BY i.created_at DESC;
```

### Output Format for Bugs

```markdown
## 🐛 Bug Issue Status (Based on Supabase DB)

| # | Title | Status | Assignee | Created At |
|---|-------|--------|----------|------------|
| #123 | API response delay | in_progress | Developer | 2025-12-01 |
| #456 | Button not clickable | todo | Frontend | 2025-12-05 |

---
**Total 2 Open Bug Issues**
```

## Error Handling

### Status Update Errors

- **Issue Not Found**

```markdown
⚠️ **Issue Not Found**

Cannot find Issue #<issue_number>.
- Please check the issue number.
- Ensure the Office ID is correct.
```

- **Invalid Status Value**

```markdown
⚠️ **Invalid Status Value**

'<status>' is not a valid status value.

Available statuses:
- backlog, todo, in_progress, review, testing, done
```

- **Supabase Connection Error**

```markdown
⚠️ **Supabase Connection Error**

Cannot change status.
- Please check MCP server settings.
```

### Bug Retrieval Errors

- **Supabase Connection Error**

```markdown
⚠️ **Supabase Connection Error**

Cannot connect to the Supabase project.
- Please check MCP server settings.
- Verify Supabase URL and API key.
```

- **Permission Error**

```markdown
⚠️ **Table Access Error**

Cannot access the issues table.
- Check RLS policies.
- Verify service key usage.
```

## Fallback Mechanism

If Supabase connection fails, fallback to GitHub CLI for status updates and bug retrieval.

```bash
# Fallback: GitHub Issue Type based retrieval
gh issue list --repo <repo_name> --state open \
  --json number,title,issueType,createdAt,assignees \
  --jq '.[] | select(.issueType.name == "Bug")'
```

## Related Skills

- [project-status Skill](../project-status/SKILL.md) - Change issue status
- [check-feedback Skill](../check-feedback/SKILL.md) - Collect feedback issues