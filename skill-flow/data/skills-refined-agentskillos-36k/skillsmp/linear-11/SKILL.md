---
name: linear
description: Interact with Linear issue tracker via the linctl CLI. Use when the user mentions Linear, issues, tickets, tasks, sprints, projects, or wants to manage work items. Supports creating, listing, updating, and assigning issues, plus team and project management.
allowed-tools:
  - Bash(linctl:*)
---

# Linear CLI (linctl)

Manage Linear issues, projects, teams, and comments via the `linctl` CLI.

## Critical Rules

1. **Always use `--json` flag** for all read operations
2. **Default filter is 6 months** - use `--newer-than all_time` to see older items
3. **Completed/canceled items are hidden by default** - use `--include-completed` to see them
4. Use team **keys** (e.g., `ENG`), not display names

## Quick Command Reference

```bash
# Issues
linctl issue list --json
linctl issue list --assignee me --json
linctl issue get LIN-123 --json
linctl issue create --title "Title" --team ENG
linctl issue update LIN-123 --state "In Progress"
linctl issue assign LIN-123

# Teams
linctl team list --json
linctl team get ENG --json
linctl team members ENG --json

# Projects
linctl project list --json
linctl project get <uuid> --json

# Comments
linctl comment list LIN-123 --json
linctl comment create LIN-123 --body "Text"

# Users
linctl user list --json
linctl user me --json
linctl whoami
```

## Detailed Documentation

- **[Issues](issues.md)** - Creating, updating, assigning, filtering, sub-issues, and workflows
- **[Projects](projects.md)** - Project tracking, progress, states, and team associations
- **[Teams](teams.md)** - Team management, members, roles, and organization
- **[Comments](comments.md)** - Adding comments, mentions, and discussion workflows
- **[Filtering & Sorting](filtering.md)** - Time-based filters, sorting options, and query patterns
- **[Scripting](scripting.md)** - JSON parsing, automation, and integration patterns
- **[Best Practices](best-practices.md)** - How to Linear: workflows, hygiene, triage, and anti-patterns
