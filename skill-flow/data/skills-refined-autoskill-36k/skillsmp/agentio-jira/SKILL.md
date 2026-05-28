---
name: agentio-jira
description: Use when interacting with JIRA - list projects, search issues, get issue details, add comments, or transition issues. Requires agentio CLI with a configured JIRA profile.
---

# JIRA Operations with agentio

Use `agentio jira` commands to interact with JIRA. Multiple profiles can be configured - the default profile is used unless you specify `--profile <name>`.

## List Projects

```bash
agentio jira projects [--limit N]
```

Options:
- `--limit <n>`: Maximum number of projects (default: 50)

## Search Issues

```bash
agentio jira search [options]
```

Options:
- `--jql <query>`: JQL query for advanced search
- `--project <key>`: Filter by project key
- `--status <status>`: Filter by status
- `--assignee <name>`: Filter by assignee
- `--limit <n>`: Maximum number of issues (default: 50)

JQL examples:
- `project = PROJ` - Issues in project
- `assignee = currentUser()` - Assigned to you
- `status = "In Progress"` - By status
- `created >= -7d` - Created in last 7 days
- `updated >= -1d` - Updated in last day
- `priority = High` - By priority
- `labels = bug` - By label

Combine: `project = PROJ AND status = "To Do" AND assignee = currentUser()`

## Get Issue Details

```bash
agentio jira get <issue-key>
```

Example:
```bash
agentio jira get PROJ-123
```

## Add a Comment

```bash
agentio jira comment <issue-key> [body]
```

Or pipe via stdin:
```bash
echo "Comment text" | agentio jira comment PROJ-123
```

## List Transitions

```bash
agentio jira transitions <issue-key>
```

Shows available status transitions for an issue with their IDs.

## Transition Issue

```bash
agentio jira transition <issue-key> <transition-id>
```

First list transitions to get the ID, then transition:
```bash
agentio jira transitions PROJ-123
agentio jira transition PROJ-123 31
```
