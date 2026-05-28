---
name: linear
description: Read when creating or updating Linear issues
---
# Rules
- **All issues must be part of a project** - Always specify `project` parameter when creating issues
- **All issues must be assigned to ME** - Always set `assignee: "me"` when creating or updating issues

# Project IDs
- Find UUID via `list_projects` then use the `id` field
- When creating/updating issues, use project UUID in `project` parameter

# Status Values
- Use exact state names: `"Done"`, `"In Progress"`, `"Todo"`, `"Backlog"`, `"Canceled"`

# Team Parameter
- Can use team name directly or team ID
