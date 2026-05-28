---
name: linear
description: Interacts with Linear for issue management. Use when the user asks about their issues, wants to create issues, or needs team/project IDs.
---

# Linear CLI

Manage Linear issues via `linear/linear.py`. Requires `LINEAR_API_KEY` env var.

## Quick Start

```bash
linear/linear.py list-issues              # My assigned issues
linear/linear.py get-issue ENG-123        # Issue details + branch name
```

## When to Use

- User asks about their Linear issues or assignments
- User wants to create a new issue
- User needs team or project IDs for issue creation

## Workflow: Create Issue

1. `linear/linear.py list-teams` → get team ID
2. `linear/linear.py list-projects --team <TEAM_ID>` → get project ID
3. `linear/linear.py create-issue --team <TEAM_ID> --project <PROJECT_ID> --title "Title" -d "Description"`

## Commands

| Command | Usage |
|---------|-------|
| `list-issues` | List assigned issues. `--recent N` for issues created in last N minutes |
| `get-issue <ID>` | Returns description, identifier, title, branch name |
| `create-issue` | `--team` required, `--project` and `-d` optional. Creates in backlog |
| `list-teams` | Output: `<name> (<key>): <id>` |
| `list-projects` | Output: `<name>: <id>`. Optional `--team` filter |
