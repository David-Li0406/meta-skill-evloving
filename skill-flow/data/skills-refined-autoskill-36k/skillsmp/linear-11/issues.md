# Issues

Issues are the core work items in Linear. This document covers all issue operations.

## Listing Issues

### Basic List
```bash
linctl issue list --json
linctl issue ls --json          # Alias
```

### Filtering Options

| Flag | Description | Example |
|------|-------------|---------|
| `--assignee`, `-a` | Filter by assignee | `--assignee me` or `--assignee john@example.com` |
| `--state`, `-s` | Filter by state name | `--state "In Progress"` |
| `--team`, `-t` | Filter by team key | `--team ENG` |
| `--priority`, `-r` | Filter by priority (0-4) | `--priority 1` |
| `--include-completed`, `-c` | Include done/canceled | `--include-completed` |
| `--limit`, `-l` | Max results (default 50) | `--limit 100` |
| `--newer-than`, `-n` | Time filter | `--newer-than 2_weeks_ago` |
| `--sort`, `-o` | Sort order | `--sort updated` |

### Common List Queries

```bash
# My issues
linctl issue list --assignee me --json

# My in-progress work
linctl issue list --assignee me --state "In Progress" --json

# Urgent issues on my team
linctl issue list --team ENG --priority 1 --json

# Recently updated issues
linctl issue list --sort updated --newer-than 1_week_ago --json

# All issues including completed (override defaults)
linctl issue list --include-completed --newer-than all_time --json

# Unassigned issues
linctl issue list --assignee unassigned --json
```

## Getting Issue Details

```bash
linctl issue get LIN-123 --json
linctl issue show LIN-123 --json    # Alias
```

Returns comprehensive details including:
- Basic info (title, description, state, priority)
- Assignee and creator
- Team and project associations
- **Parent issue** (if this is a sub-issue)
- **Sub-issues** (child issues)
- **Git branches** linked to the issue
- **Cycle/sprint** information
- **Attachments** list
- **Recent comments** preview
- Due date and snooze status
- URL to Linear web interface

### JSON Response Structure

```json
{
  "id": "uuid",
  "identifier": "LIN-123",
  "title": "Issue title",
  "description": "Full description",
  "state": {
    "name": "In Progress",
    "type": "started"
  },
  "priority": 2,
  "priorityLabel": "High",
  "assignee": {
    "name": "John Doe",
    "email": "john@example.com"
  },
  "team": {
    "key": "ENG",
    "name": "Engineering"
  },
  "project": {
    "name": "Q1 Launch"
  },
  "cycle": {
    "name": "Sprint 23"
  },
  "parent": {
    "identifier": "LIN-100",
    "title": "Parent epic"
  },
  "subIssues": [...],
  "attachments": [...],
  "comments": [...],
  "branchName": "lin-123-issue-title",
  "dueDate": "2024-12-31",
  "createdAt": "2024-01-15T10:00:00Z",
  "updatedAt": "2024-01-20T14:30:00Z",
  "url": "https://linear.app/team/issue/LIN-123"
}
```

## Creating Issues

### Basic Create
```bash
linctl issue create --title "Issue title" --team ENG
linctl issue new --title "Issue title" --team ENG    # Alias
```

### Create Options

| Flag | Description | Example |
|------|-------------|---------|
| `--title` | Issue title (required) | `--title "Fix bug"` |
| `--team`, `-t` | Team key (required) | `--team ENG` |
| `--description`, `-d` | Issue description | `--description "Details..."` |
| `--priority` | Priority 0-4 (default 3) | `--priority 1` |
| `--assign-me`, `-m` | Assign to yourself | `--assign-me` |

### Create Examples

```bash
# Simple issue
linctl issue create --title "Add dark mode" --team ENG

# With description and self-assignment
linctl issue create \
  --title "Fix login timeout" \
  --team ENG \
  --description "Users report being logged out after 5 minutes" \
  --assign-me

# Urgent issue
linctl issue create \
  --title "Production database down" \
  --team ENG \
  --priority 1 \
  --assign-me

# Get created issue ID from JSON output
linctl issue create --title "New feature" --team ENG --json | jq -r '.identifier'
```

## Updating Issues

```bash
linctl issue update LIN-123 [flags]
linctl issue edit LIN-123 [flags]    # Alias
```

### Update Options

| Flag | Description | Example |
|------|-------------|---------|
| `--title` | New title | `--title "Updated title"` |
| `--description`, `-d` | New description | `--description "New details"` |
| `--assignee`, `-a` | Set assignee | `--assignee me` |
| `--state`, `-s` | Change state | `--state "Done"` |
| `--priority` | Set priority (0-4) | `--priority 2` |
| `--due-date` | Set due date | `--due-date "2024-12-31"` |

### Assignee Values

- `me` - Assign to yourself
- `email@example.com` - Assign by email
- `John Doe` - Assign by name
- `unassigned` - Remove assignee

### Update Examples

```bash
# Start working on an issue
linctl issue update LIN-123 --state "In Progress" --assignee me

# Complete an issue
linctl issue update LIN-123 --state "Done"

# Change priority to urgent
linctl issue update LIN-123 --priority 1

# Set due date
linctl issue update LIN-123 --due-date "2024-12-31"

# Remove due date
linctl issue update LIN-123 --due-date ""

# Reassign to someone else
linctl issue update LIN-123 --assignee jane@example.com

# Unassign
linctl issue update LIN-123 --assignee unassigned

# Multiple updates at once
linctl issue update LIN-123 \
  --title "Critical: Fix authentication" \
  --priority 1 \
  --assignee me \
  --state "In Progress"
```

## Assigning Issues

Quick command to assign an issue to yourself:

```bash
linctl issue assign LIN-123
```

This is equivalent to:
```bash
linctl issue update LIN-123 --assignee me
```

## Priority Reference

| Value | Label | When to Use |
|-------|-------|-------------|
| 0 | None | Backlog items, no urgency |
| 1 | Urgent | Production issues, blockers |
| 2 | High | Important, needs attention soon |
| 3 | Normal | Standard priority (default) |
| 4 | Low | Nice to have, when time permits |

## Common States

States vary by team configuration, but common ones include:

| State | Type | Description |
|-------|------|-------------|
| Backlog | backlog | Not yet planned |
| Todo | unstarted | Planned but not started |
| In Progress | started | Currently being worked on |
| In Review | started | Awaiting review |
| Done | completed | Finished |
| Canceled | canceled | Won't be done |

Get available states for a team:
```bash
linctl team get ENG --json | jq '.states'
```

## Sub-Issues (Parent/Child)

Linear supports hierarchical issues. When you get issue details:

- `parent` field shows the parent issue (if any)
- `subIssues` array lists child issues

```bash
# View issue with its hierarchy
linctl issue get LIN-123 --json | jq '{
  identifier,
  title,
  parent: .parent.identifier,
  subIssues: [.subIssues[].identifier]
}'
```

## Git Branch Integration

Linear creates suggested branch names. The `branchName` field contains the suggested branch:

```bash
# Get branch name for an issue
linctl issue get LIN-123 --json | jq -r '.branchName'
# Output: lin-123-fix-authentication-bug

# Create and checkout the branch
git checkout -b $(linctl issue get LIN-123 --json | jq -r '.branchName')
```

## Workflow Examples

### Start Working on an Issue
```bash
# 1. Find an issue to work on
linctl issue list --team ENG --state "Todo" --json | jq '.[0]'

# 2. Assign and start it
linctl issue update LIN-123 --assignee me --state "In Progress"

# 3. Create git branch
git checkout -b $(linctl issue get LIN-123 --json | jq -r '.branchName')
```

### Triage New Issues
```bash
# Find unassigned issues
linctl issue list --assignee unassigned --team ENG --json

# Set priority and assign
linctl issue update LIN-456 --priority 2 --assignee jane@example.com
```

### Daily Standup Check
```bash
# What am I working on?
linctl issue list --assignee me --state "In Progress" --json

# What's blocked/urgent?
linctl issue list --team ENG --priority 1 --json
```

### Complete and Close
```bash
# Mark as done
linctl issue update LIN-123 --state "Done"

# Add closing comment
linctl comment create LIN-123 --body "Fixed in PR #456"
```
