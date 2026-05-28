---
name: beads
description: Beads issue tracker CLI reference. Use when creating issues, managing tasks, querying work items, or tracking dependencies with bd commands.
user-invocable: true
---

# Beads Issue Tracker Skill

Use this skill when working with the Beads (`bd`) issue tracker to create, manage, and query issues.

## Quick Reference

### List Issues

```bash
# Open issues (default)
bd list --status open

# All issues including closed
bd list --all

# Filter by priority (P0=highest, P4=lowest)
bd list --priority 1
bd list --priority-max 2  # P0-P2

# Filter by type
bd list --type feature
bd list --type bug
bd list --type task
bd list --type chore

# Filter by label
bd list --label security
bd list --label authorization,blocking  # AND (must have all)
bd list --label-any security,cleanup    # OR (any of these)

# Combined filters
bd list --status open --priority-max 2 --type feature

# Tree view (hierarchical)
bd list --pretty
bd list --tree

# Detailed output
bd list --long
```

### Show Issue Details

```bash
bd show <issue-id>
bd show substruct-9pi

# Compact output
bd show --short <issue-id>

# JSON for scripting
bd show --json <issue-id>
```

### Create Issues

```bash
# Basic creation
bd new "Issue title" --type task --priority 2

# Full creation with description
bd new "Title" \
  --type feature \
  --priority 1 \
  --labels "security,authorization" \
  --description "$(cat <<'EOF'
## Problem
Description of the problem.

## Proposed Solution
How to fix it.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## References
- File: path/to/file.rs:42
EOF
)"

# Quick capture (returns only ID)
bd q "Quick issue title"
```

### Issue Types

| Type | Use For |
|------|---------|
| `feature` | New functionality |
| `bug` | Defects to fix |
| `task` | Work items |
| `chore` | Maintenance, cleanup |
| `epic` | Large multi-issue work |

### Priorities

| Priority | Meaning |
|----------|---------|
| P0 | Critical/Blocking |
| P1 | High priority |
| P2 | Normal (default) |
| P3 | Low priority |
| P4 | Backlog |

### Update Issues

```bash
# Update status
bd update <issue-id> --status in_progress
bd update <issue-id> --status blocked
bd update <issue-id> --status open

# Update priority
bd update <issue-id> --priority 1

# Add/remove labels
bd update <issue-id> --add-label blocking
bd update <issue-id> --remove-label cleanup

# Update title
bd update <issue-id> --title "New title"

# Claim issue (set assignee + in_progress atomically)
bd update <issue-id> --claim
```

### Close Issues

```bash
# Close with reason
bd close <issue-id> --reason "Completed in commit abc123"

# Close last touched issue
bd close --reason "Done"

# Show what's unblocked after closing
bd close <issue-id> --suggest-next
```

### Comments

```bash
# List comments
bd comments <issue-id>

# Add comment
bd comments add <issue-id> "Progress update: completed X, working on Y"

# Add comment from file
bd comments add <issue-id> -f notes.txt
```

### Dependencies

```bash
# Create blocking dependency (A blocks B)
bd dep <blocker-id> --blocks <blocked-id>
bd dep substruct-9pi --blocks substruct-uto

# Add dependency (B depends on A)
bd dep add <dependent-id> <dependency-id>

# Create related link (bidirectional)
bd dep relate <issue-1> <issue-2>

# List dependencies
bd dep list <issue-id>

# Show dependency tree
bd dep tree <issue-id>

# Check for cycles
bd dep cycles
```

### Search

```bash
# Text search
bd search "password hashing"

# Filter by title
bd list --title-contains "projection"

# Filter by description
bd list --desc-contains "SQLite"
```

## Substruct Project Conventions

### Label Taxonomy

| Label | Meaning |
|-------|---------|
| `authorization` | Authorization bounded context |
| `persistence` | EventStore/ProjectionStore |
| `infrastructure` | Core patterns |
| `projections` | Read model projections |
| `security` | Security-sensitive |
| `blocking` | Blocks other work |
| `cleanup` | Technical debt cleanup |
| `documentation` | Docs improvements |
| `testing` | Test coverage |

### Issue Description Template

For Substruct issues, use this structure:

```markdown
## Problem
What's wrong or missing? Include code references.

## Context
Why does this matter? What's the impact?

## Proposed Solution
How should we fix it? Options if multiple approaches.

## Acceptance Criteria
- [ ] Specific, testable criteria
- [ ] Tests pass
- [ ] Clippy clean

## References
- File: path/to/file.rs:line
- ADR: docs/adr/0001-*.md
- Memory: Forgetful #42 (title)
```

### Workflow

1. **Starting work**: `bd update <id> --claim`
2. **Progress updates**: `bd comments add <id> "Update..."`
3. **Blocked**: `bd update <id> --status blocked`
4. **Completing**: `bd close <id> --reason "Commit abc123"`

### Common Queries

```bash
# What should I work on next?
bd list --status open --priority-max 2

# What's blocking progress?
bd list --status blocked

# Security-related issues
bd list --label security

# Issues I'm working on
bd list --status in_progress --assignee $(git config user.name)

# Overdue issues
bd list --overdue
```

## Tips

- Use `bd list --pretty` for visual hierarchy
- Use `--json` flag for scripting
- Issue IDs follow pattern: `substruct-xxx` (3 random chars)
- Last touched issue remembered - many commands work without explicit ID
- Daemon runs in background for sync - check with `bd daemon status`
