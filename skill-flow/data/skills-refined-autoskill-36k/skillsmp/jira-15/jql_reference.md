# JQL (Jira Query Language) Reference

## Basic Syntax

JQL queries use field-operator-value patterns:
```
field operator value
```

## Fields

### Standard Fields
| Field | Description | Example |
|-------|-------------|---------|
| `project` | Project key or name | `project = PROJ` |
| `issuetype` / `type` | Issue type | `type = Bug` |
| `status` | Issue status | `status = "In Progress"` |
| `priority` | Issue priority | `priority = High` |
| `assignee` | Assigned user | `assignee = john` |
| `reporter` | Issue reporter | `reporter = jane` |
| `created` | Creation date | `created >= 2024-01-01` |
| `updated` | Last update date | `updated >= -7d` |
| `resolved` | Resolution date | `resolved >= startOfMonth()` |
| `due` | Due date | `due <= endOfWeek()` |
| `summary` | Issue summary | `summary ~ "login"` |
| `description` | Issue description | `description ~ "error"` |
| `labels` | Issue labels | `labels = backend` |
| `component` | Components | `component = "API"` |
| `fixVersion` | Fix version | `fixVersion = "1.0"` |
| `affectedVersion` | Affected version | `affectedVersion = "0.9"` |
| `sprint` | Sprint name or ID | `sprint in openSprints()` |
| `parent` | Parent issue (subtasks) | `parent = PROJ-123` |
| `resolution` | Resolution type | `resolution = Fixed` |

### Custom Fields
Access custom fields by name or ID:
```jql
"Custom Field Name" = value
cf[10001] = value
```

## Operators

### Comparison Operators
| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `status = Done` |
| `!=` | Not equals | `status != Done` |
| `>` | Greater than | `priority > Medium` |
| `>=` | Greater than or equal | `created >= 2024-01-01` |
| `<` | Less than | `priority < High` |
| `<=` | Less than or equal | `due <= endOfWeek()` |
| `~` | Contains (text search) | `summary ~ "error"` |
| `!~` | Does not contain | `summary !~ "test"` |
| `in` | In list | `status in (Open, "In Progress")` |
| `not in` | Not in list | `status not in (Done, Closed)` |
| `is` | Is empty/null | `assignee is EMPTY` |
| `is not` | Is not empty/null | `assignee is not EMPTY` |
| `was` | Historical value | `status was "In Progress"` |
| `was in` | Historical in list | `status was in (Open, "In Progress")` |
| `was not` | Historical not value | `status was not Done` |
| `changed` | Field changed | `status changed` |

## Logical Operators

```jql
# AND - both conditions must be true
project = PROJ AND status = Open

# OR - either condition can be true
priority = High OR priority = Critical

# NOT - negates condition
NOT status = Done

# Parentheses for grouping
project = PROJ AND (priority = High OR priority = Critical)
```

## Functions

### Date Functions
| Function | Description |
|----------|-------------|
| `now()` | Current date/time |
| `currentLogin()` | Time of current login |
| `startOfDay()` | Start of current day |
| `startOfWeek()` | Start of current week |
| `startOfMonth()` | Start of current month |
| `startOfYear()` | Start of current year |
| `endOfDay()` | End of current day |
| `endOfWeek()` | End of current week |
| `endOfMonth()` | End of current month |
| `endOfYear()` | End of current year |

### User Functions
| Function | Description |
|----------|-------------|
| `currentUser()` | Currently logged-in user |
| `membersOf("group")` | Members of a group |

### Sprint Functions
| Function | Description |
|----------|-------------|
| `openSprints()` | All open sprints |
| `closedSprints()` | All closed sprints |
| `futureSprints()` | All future sprints |

### Other Functions
| Function | Description |
|----------|-------------|
| `issueHistory()` | Issues in history |
| `linkedIssues(key)` | Issues linked to key |
| `votedIssues()` | Issues voted by user |
| `watchedIssues()` | Issues watched by user |

## Relative Dates

Use negative numbers for past dates:
```jql
created >= -7d    # Last 7 days
updated >= -2w    # Last 2 weeks
created >= -1M    # Last 1 month
created >= -1y    # Last 1 year
```

## Sorting

Use ORDER BY to sort results:
```jql
project = PROJ ORDER BY created DESC
project = PROJ ORDER BY priority DESC, created ASC
```

Sort options:
- `ASC` - Ascending (default)
- `DESC` - Descending

## Common Query Examples

### By Time Period
```jql
# Created today
created >= startOfDay()

# Created this week
created >= startOfWeek()

# Updated in last 24 hours
updated >= -24h

# Resolved this month
resolved >= startOfMonth() AND resolved <= endOfMonth()
```

### By Assignment
```jql
# My open issues
assignee = currentUser() AND status != Done

# Unassigned issues
assignee is EMPTY

# Issues assigned to team
assignee in membersOf("developers")
```

### By Status
```jql
# Open issues
status = Open

# In progress
status = "In Progress"

# Not done
status not in (Done, Closed, Resolved)

# Recently moved to Done
status = Done AND status changed after -7d
```

### Sprint Queries
```jql
# Current sprint issues
sprint in openSprints()

# Specific sprint
sprint = "Sprint 42"

# Issues not in any sprint
sprint is EMPTY

# Backlog items
sprint is EMPTY AND status = Open
```

### Complex Queries
```jql
# High priority bugs in current sprint
project = PROJ AND type = Bug AND priority in (High, Critical) AND sprint in openSprints()

# Overdue issues
due < now() AND status != Done

# Issues blocked and not updated recently
status = Blocked AND updated < -3d

# Subtasks of an epic
parent = PROJ-100 OR "Epic Link" = PROJ-100
```

## Text Search

Use `~` for text search with wildcards:
```jql
# Contains word
summary ~ "error"

# Starts with
summary ~ "API*"

# Exact phrase
summary ~ "\"login failed\""

# Multiple terms (OR)
summary ~ "error OR failure"
```

## Best Practices

1. **Use project filter first** - Narrows down results quickly
2. **Limit results** - Use `maxResults` parameter in API calls
3. **Be specific** - More filters = faster queries
4. **Use indexes** - Standard fields are indexed, custom fields may not be
5. **Avoid wildcards at start** - `summary ~ "*error"` is slow
6. **Quote values with spaces** - `status = "In Progress"`
