---
name: vault-status
description: >
  Use when user wants to check progress or get an overview.
  Triggered when intention involves understanding current state of projects or work.
  Summarizes project status, recent activity, and pending items.
---

# Vault Status

## Behavior

1. Determine scope:
   - Specific project → scan that project folder
   - General → scan all of `01_Projects/`
2. Gather information:
   - Project status from frontmatter
   - Recent notes (last 7 days)
   - Note count and last modified dates
   - Incomplete tasks (checkbox items)
3. Present organized summary

## Status Levels

| Status | Meaning |
|--------|---------|
| active | Currently being worked on |
| paused | Temporarily on hold |
| completed | Finished, ready for archive |

## Output Format - Single Project

```markdown
## Project: {name}

- **Status**: {active/paused/completed}
- **Created**: {date}
- **Due**: {date or "Not set"}
- **Last updated**: {date of most recent note}
- **Notes**: {count} files

### Recent Activity
- {date}: {note title}
- {date}: {note title}

### Open Tasks
- [ ] Task from notes...

### Next Actions
{Suggested next steps based on content}
```

## Output Format - General Status

```markdown
## Vault Status

### Active Projects ({count})
| Project | Last Activity | Notes |
|---------|---------------|-------|
| {name} | {date} | {count} |

### Stalled Projects (no updates in 2+ weeks)
- {project name} - last updated {date}

### Inbox Status
- {count} items awaiting processing

### This Week
- {count} daily notes
- {count} new captures
```

## Stalled Detection

Flag projects as "stalled" if:
- Status is `active`
- No new notes in 14+ days
- Has incomplete tasks
