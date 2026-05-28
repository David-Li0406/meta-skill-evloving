# JQL Cheatsheet

Quick reference for Jira Query Language (JQL) syntax and common patterns.

## Basic Syntax

```
field operator value [AND|OR field operator value...]
```

## Common Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `status = "In Progress"` |
| `!=` | Not equals | `status != Done` |
| `>` `<` `>=` `<=` | Comparison | `created >= -7d` |
| `~` | Contains (text) | `summary ~ "login"` |
| `!~` | Does not contain | `summary !~ "test"` |
| `IN` | In list | `status IN ("Open", "In Progress")` |
| `NOT IN` | Not in list | `priority NOT IN (Low, Lowest)` |
| `IS EMPTY` | Field is empty | `assignee IS EMPTY` |
| `IS NOT EMPTY` | Field has value | `fixVersion IS NOT EMPTY` |

## Date Functions

| Function | Description | Example |
|----------|-------------|---------|
| `now()` | Current time | `due < now()` |
| `-Nd` | N days ago | `created >= -7d` |
| `-Nw` | N weeks ago | `updated >= -2w` |
| `startOfDay()` | Start of today | `created >= startOfDay()` |
| `startOfWeek()` | Start of week | `created >= startOfWeek()` |
| `startOfMonth()` | Start of month | `created >= startOfMonth()` |
| `endOfDay()` | End of today | `due <= endOfDay()` |

## Common Query Patterns

### By Status
```jql
# Open issues
status = Open

# In progress
status = "In Progress"

# Not done
status != Done

# Multiple statuses
status IN ("To Do", "In Progress", "In Review")
```

### By Assignee
```jql
# Assigned to me
assignee = currentUser()

# Unassigned
assignee IS EMPTY

# Assigned to specific user
assignee = "john.doe@company.com"
```

### By Date
```jql
# Created in last 7 days
created >= -7d

# Updated this week
updated >= startOfWeek()

# Overdue issues
due < now() AND status != Done

# Due this week
due >= startOfWeek() AND due <= endOfWeek()
```

### By Project and Type
```jql
# Specific project
project = PROJ

# Multiple projects
project IN (PROJ, API, WEB)

# Bugs only
issuetype = Bug

# Stories and tasks
issuetype IN (Story, Task)
```

### Sprint Queries
```jql
# Current sprint
sprint IN openSprints()

# Future sprints
sprint IN futureSprints()

# Closed sprints
sprint IN closedSprints()

# Specific sprint
sprint = "Sprint 10"

# No sprint assigned
sprint IS EMPTY
```

### Combined Patterns

```jql
# My open bugs in current sprint
project = PROJ AND assignee = currentUser() AND issuetype = Bug AND sprint IN openSprints()

# Unassigned high priority items
priority IN (High, Highest) AND assignee IS EMPTY AND status != Done

# Recently updated epics
issuetype = Epic AND updated >= -7d

# Blocked issues
status = Blocked OR labels = blocked

# Issues without story points
"Story Points" IS EMPTY AND issuetype IN (Story, Task)
```

## Ordering Results

```jql
# By priority (high first)
ORDER BY priority DESC

# By creation date (newest first)
ORDER BY created DESC

# Multiple sort fields
ORDER BY priority DESC, created ASC
```

## Text Search

```jql
# Search in summary
summary ~ "authentication"

# Search in description
description ~ "API endpoint"

# Search in comments
comment ~ "needs review"

# Full text search (all text fields)
text ~ "login error"
```

## Parent/Child Relationships

```jql
# Children of an epic
parent = PROJ-100

# Issues linked to specific issue
issueLink = PROJ-100

# Subtasks of a story
parent = PROJ-200 AND issuetype = Sub-task
```
