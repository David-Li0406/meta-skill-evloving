---
name: jira-write
description: Create and update Jira issues, add comments, transition statuses, and manage sprints. Use when you need to make changes to Jira data. Supports dry-run mode for validation.
license: MIT
compatibility: Requires Jira Cloud API access with write permissions
metadata:
  author: ximplicity
  version: "1.0"
  category: jira
---

# Jira Write Skill

Write operations for creating and modifying Jira data.

## Allowed Operations

- Create issues
- Update issue fields
- Add comments
- Transition issues between statuses
- Move issues to sprints
- Update sprint details
- Link issues

## Forbidden Operations

- Delete issues (requires separate approval)
- Bulk operations without explicit approval
- Modifying project settings
- User management
- Permission changes

## Constraints

- All write operations support dry-run mode
- Each operation must be atomic
- Maximum 10 operations per batch

## Dry-Run Mode

**Always recommend dry-run first for important changes:**

```json
{
  "issueKey": "PROJ-123",
  "summary": "New title",
  "dryRun": true
}
```

When `dryRun: true`:
1. Validates all inputs
2. Checks permissions
3. Returns what WOULD happen
4. Makes NO changes

## Quick Reference

### Create Issue
```json
{
  "projectKey": "PROJ",
  "summary": "Issue title",
  "issueTypeName": "Bug",
  "priority": "High"
}
```

### Update Issue
```json
{
  "issueKey": "PROJ-123",
  "summary": "Updated title",
  "labels": ["urgent"]
}
```

### Transition Issue
```json
{
  "issueKey": "PROJ-123",
  "transitionName": "Done"
}
```

For detailed transition workflows, see [TRANSITIONS-GUIDE.md](references/TRANSITIONS-GUIDE.md).

For complete field formats and custom fields, see [FIELD-REFERENCE.md](references/FIELD-REFERENCE.md).

## Error Handling

| Scenario | Action |
|----------|--------|
| Validation failure | Return all errors at once |
| Permission denied | Clear message, no retry |
| Conflict | Return current state |

## Example Usage

```
Create a bug in project API with high priority
Update PROJ-123 to add acceptance criteria
Transition PROJ-456 to In Review
Move issues PROJ-1, PROJ-2 to Sprint 5
```
