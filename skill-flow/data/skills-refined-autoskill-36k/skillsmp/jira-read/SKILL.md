---
name: jira-read
description: Read data from Jira including issues, comments, sprints, and execute JQL queries. Use when you need to fetch or search Jira data without making changes.
license: MIT
compatibility: Requires Jira Cloud API access with read permissions
metadata:
  author: ximplicity
  version: "1.0"
  category: jira
---

# Jira Read Skill

Read-only operations for Jira data retrieval and analysis.

## Allowed Operations

- Read issue by key (e.g., `PROJECT-123`)
- Execute JQL queries
- Read issue metadata (fields, transitions, comments)
- Read issue changelog/history
- List projects and boards
- Read sprint information
- Get velocity metrics

## Forbidden Operations

- Writing or updating issues
- Adding comments
- Transitioning issues
- Creating issues
- Deleting anything

## Constraints

- Maximum 50 issues per query (use pagination for more)
- Rate limiting must be respected
- All requests require proper authentication

## Input Requirements

- Issue keys: `[A-Z]+-\d+` pattern (e.g., PROJ-123)
- Project keys: uppercase alphanumeric
- JQL queries: validate before execution

## Quick JQL Reference

```jql
# Common patterns
assignee = currentUser() AND status != Done
project = PROJ AND sprint IN openSprints()
created >= -7d AND priority = High
```

For detailed JQL syntax, operators, and examples, see [JQL-CHEATSHEET.md](references/JQL-CHEATSHEET.md).

## Error Handling

| Status | Action |
|--------|--------|
| 404 | Issue not found - verify key |
| 401/403 | Auth error - check credentials |
| 429 | Rate limited - backoff and retry |

For complete error codes and retry strategies, see [ERROR-HANDLING.md](references/ERROR-HANDLING.md).

## Example Usage

```
Get issue PROJ-123 with full details
Search for open bugs in project WEBAPP
Show sprint velocity for the last 5 sprints
Find issues assigned to me in current sprint
```
