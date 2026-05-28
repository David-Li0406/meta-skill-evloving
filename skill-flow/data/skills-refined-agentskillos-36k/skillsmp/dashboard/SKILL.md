---
name: dashboard
description: Generate and open the interactive backlog dashboard in the browser.
---

# Dashboard Skill

Generate and open the backlog dashboard.

## Usage

Type `/dashboard` to generate and open the dashboard.

## Action

When invoked, run:

```bash
cd /Users/daniel/Documents/Mad-dashboard-recovery && \
python .claude/plans/backlog/scripts/generate_dashboard.py && \
cp backlog-dashboard.html /Users/daniel/Documents/Mad/backlog-dashboard.html && \
open /Users/daniel/Documents/Mad/backlog-dashboard.html
```

## Features

The dashboard includes:
- Metrics cards (Total Items, Completed, Unassigned, Blocked, Reopened)
- Interactive charts (click to filter table)
- Multi-select filters for Status, Priority, Category
- Clickable table rows with detail popup
- Refresh button
