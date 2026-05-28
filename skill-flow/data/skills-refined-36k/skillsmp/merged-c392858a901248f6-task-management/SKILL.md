---
name: task-management
description: Use this skill for tracking and automating task progress, assigning issues, and managing workflows based on Supabase DB.
---

# Task Management Skill

This skill allows for tracking developer task progress, assigning issues, and automating workflow steps using a Supabase database.

## 🔴 Data Source Change (v2.0.0)

| Version | Data Source | Method |
|---------|-------------|--------|
| v1.x    | GitHub Projects | GraphQL API |
| **v2.0** | **Supabase** | Querying `issues` and `issue_status_history` |

## Triggers

- `/SEMO:task-progress` command
- Keywords: "어디까지 했어", "현황", "체크리스트", "진행도"
- Automatic invocation when an issue number is provided

## Developer Process Overview

```text
1. Assign task (backlog → todo)
2. Change status (todo → in_progress)
3. Write specifications (spec.md, plan.md, tasks.md)
4. Commit & push specifications
5. Create feature branch
6. Create draft PR
7. Implement code
8. Write and run tests
9. Pass lint and build
10. Push and request review (in_progress → review)
11. Merge PR and approve (review → testing)
12. QA test in STG environment (testing → done)
```

### Status Flow

```text
backlog → todo → in_progress → review → testing → done
                      ↓           ↑
                  Confirmation Request  Revision Request
```

## Workflow Steps

### Step 1: Retrieve Current Issue Status

```sql
-- Retrieve issue details
SELECT
  i.number,
  i.title,
  i.type,
  i.status,
  i.state,
  i.labels,
  i.estimation_point,
  ap.name AS assignee_name,
  TO_CHAR(i.created_at, 'YYYY-MM-DD') AS created_at,
  TO_CHAR(i.updated_at, 'YYYY-MM-DD') AS updated_at
FROM issues i
LEFT JOIN agent_personas ap ON i.assignee_id = ap.id
WHERE i.number = <issue_number>
  AND i.office_id = '{office_uuid}';
```

### Step 2: Retrieve Status Change History

```sql
-- Retrieve status change history
SELECT
  ish.from_status,
  ish.to_status,
  TO_CHAR(ish.changed_at, 'YYYY-MM-DD HH24:MI') AS changed_at,
  ap.name AS changed_by
FROM issue_status_history ish
LEFT JOIN agent_personas ap ON ish.changed_by = ap.id
WHERE ish.issue_id = (
  SELECT id FROM issues WHERE number = <issue_number>
)
ORDER BY ish.changed_at DESC;
```

### Step 3: Create Progress Checklist

```typescript
// Query from Supabase
const { data: issue, error } = await supabase
  .from('issues')
  .select(`
    number, title, status, body,
    assignee:agent_personas(name)
  `)
  .eq('number', <issue_number>)
  .eq('office_id', officeId)
  .single();

// Generate checklist based on status
const checklist = generateChecklist(issue.status);
```

## Quick Checks

| Step | Command |
|------|---------|
| Branch | `git branch --show-current` |
| PR Check | `gh pr list --head {branch} --json number,isDraft` |
| Lint | `npm run lint` |
| Type Check | `npx tsc --noEmit` |
| Unpushed Check | `git log origin/{branch}..HEAD --oneline` |

## Output Format

```markdown
[SEMO] Skill: task-progress 호출 - #<issue_number>

## 📋 Task Progress Status: #<issue_number>

### Issue Information

| Item | Content |
|------|---------|
| **Title** | <issue_title> |
| **Type** | <issue_type> |
| **Status** | <issue_status> |
| **Assignee** | @<assignee_name> |
| **Workload** | <estimation_point> points |

### Progress Checklist

- [x] 1. Task Assigned
- [x] 2. Status Changed (todo → in_progress)
- [x] 3. Spec Written
- [x] 4. Feature Branch Created
- [ ] 5. Code Implemented
- [ ] 6. Tests Written
- [ ] 7. Lint/Build Passed
- [ ] 8. Review Requested
- [ ] 9. PR Merged

### Status Change History

| Time | Change | Changed By |
|------|--------|------------|
| <timestamp> | <from_status> → <to_status> | @<changed_by> |

### Next Steps

🎯 **Current Step**: Code Implementation
📌 **Recommended Action**: `skill:write-code` 호출

[SEMO] Skill: task-progress 완료
```

## Automatic Status Change

### On Review Request (Step 9)

When the PR is ready, automatically change the status to "review":

```sql
-- Change status to review
SELECT * FROM update_issue_status(
  <issue_number>,
  '{office_uuid}'::uuid,
  'review',
  '{actor_uuid}'::uuid
);
```

```markdown
[SEMO] Skill: task-progress → Status Automatically Changed

📋 **Issue**: #<issue_number>
🔀 **PR**: #<pr_number> Ready for Review
🔄 **Status Change**: in_progress → **review**

✅ Status Change Completed
```

## Error Handling

### Issue Not Found

```markdown
❌ Issue #<issue_number> not found.

Check:
- Is the issue number correct?
- Is the Office ID correct?
```

### No Status History

```markdown
⚠️ No status change history for issue #<issue_number>.

This is a new issue that has not been changed yet.
Current status: backlog
```

## Fallback to GitHub Projects

If Supabase connection fails:

```bash
# Fallback: Query status via GitHub Projects GraphQL
gh api graphql -f query='
  query {
    repository(owner: "semicolon-devteam", name: "semo") {
      issue(number: <issue_number>) {
        projectItems(first: 1) {
          nodes {
            fieldValueByName(name: "Status") {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
              }
            }
          }
        }
      }
    }
  }
'
```

## Related Skills

- [project-status](../project-status/SKILL.md) - Status Change
- [start-task](../start-task/SKILL.md) - Start Task
- [assign-task](../assign-task/SKILL.md) - Assign Task

## References

- [issues table migration](../../../semo-repository/supabase/migrations/20260113003_issues_discussions.sql)
- [Verification Steps](references/verification-steps.md) - Detailed verification logic
- [Automation](references/automation.md) - Automation commands, output format