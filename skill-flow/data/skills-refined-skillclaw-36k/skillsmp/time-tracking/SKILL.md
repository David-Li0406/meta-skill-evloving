---
name: time-tracking
description: |
  Time tracking with Toggl. Use this skill when:
  - Starting or stopping time entries
  - Checking current timer status
  - Generating time reports (daily, weekly, by project)
  - Reviewing productivity and time allocation
  - Managing projects and workspaces
allowed-tools:
  - mcp__toggl__toggl_start_timer
  - mcp__toggl__toggl_stop_timer
  - mcp__toggl__toggl_get_current_entry
  - mcp__toggl__toggl_get_time_entries
  - mcp__toggl__toggl_daily_report
  - mcp__toggl__toggl_weekly_report
  - mcp__toggl__toggl_project_summary
  - mcp__toggl__toggl_workspace_summary
  - mcp__toggl__toggl_list_workspaces
  - mcp__toggl__toggl_list_projects
  - mcp__toggl__toggl_list_clients
  - mcp__toggl__toggl_check_auth
  - mcp__toggl__toggl_warm_cache
---

# Time Tracking Skill

Manage time tracking with Toggl using the **Track-Report-Analyze** pattern.

## Phase 1: TRACK (Manage Timers)

### Check Current Status

```javascript
mcp__toggl__toggl_get_current_entry({})
```

Returns the running timer (if any) with:

- Description
- Project name
- Duration so far
- Start time

### Start a Timer

```javascript
mcp__toggl__toggl_start_timer({
  description: "Working on feature implementation",
  projectId: 12345,          // optional
  workspaceId: 67890,        // optional
  tags: ["development"]      // optional
})
```

If a timer is already running, it will be stopped automatically.

### Stop Current Timer

```javascript
mcp__toggl__toggl_stop_timer({})
```

### List Projects for Selection

```javascript
mcp__toggl__toggl_list_projects({
  workspaceId: 12345  // optional
})
```

### List Workspaces

```javascript
mcp__toggl__toggl_list_workspaces({})
```

## Phase 2: REPORT (View Time Data)

### Get Time Entries

```javascript
mcp__toggl__toggl_get_time_entries({
  startDate: "2025-01-01",
  endDate: "2025-01-31"
})
```

Returns hydrated entries with project and workspace names.

### Daily Report

```javascript
mcp__toggl__toggl_daily_report({
  date: "2025-01-15"  // optional, defaults to today
})
```

Returns:

- Total hours for the day
- Breakdown by project
- Breakdown by workspace
- List of entries

### Weekly Report

```javascript
mcp__toggl__toggl_weekly_report({
  startDate: "2025-01-13",
  endDate: "2025-01-19"
})
```

Returns:

- Total hours for the week
- Daily breakdown
- Project summaries
- Workspace summaries

### Project Summary

```javascript
mcp__toggl__toggl_project_summary({
  startDate: "2025-01-01",
  endDate: "2025-01-31"
})
```

### Workspace Summary

```javascript
mcp__toggl__toggl_workspace_summary({
  startDate: "2025-01-01",
  endDate: "2025-01-31"
})
```

## Phase 3: ANALYZE (Insights)

### Compare Periods

Compare current week to previous:

```javascript
// This week
const thisWeek = mcp__toggl__toggl_weekly_report({
  startDate: "2025-01-20",
  endDate: "2025-01-26"
})

// Last week
const lastWeek = mcp__toggl__toggl_weekly_report({
  startDate: "2025-01-13",
  endDate: "2025-01-19"
})
```

Then calculate:

- Week-over-week change
- Project allocation shifts
- Productivity trends

### Client Hours

```javascript
mcp__toggl__toggl_list_clients({
  workspaceId: 12345
})
```

Cross-reference with project data for client billing.

## Report Formatting

### Daily Summary Example

```text
## Daily Report - January 15, 2025

**Total: 7h 32m**

### By Project
| Project | Hours |
|---------|-------|
| Client A - Website | 3h 15m |
| Internal - Planning | 2h 00m |
| Client B - API | 2h 17m |

### Entries
1. 09:00-12:15 - Client A - Website - Homepage redesign
2. 13:00-15:00 - Internal - Planning - Q1 roadmap
3. 15:15-17:32 - Client B - API - Payment integration
```

### Weekly Summary Example

```text
## Weekly Report - Jan 13-19, 2025

**Total: 38h 45m** (vs 35h 20m last week, +9.7%)

### Daily Breakdown
| Day | Hours |
|-----|-------|
| Mon | 8h 15m |
| Tue | 7h 30m |
| Wed | 8h 00m |
| Thu | 7h 45m |
| Fri | 7h 15m |

### Top Projects
1. Client A - Website: 15h 30m (40%)
2. Internal - Development: 12h 00m (31%)
3. Client B - API: 8h 15m (21%)
4. Other: 3h 00m (8%)
```

## Performance Optimization

### Warm Cache

Pre-load workspace, project, and client data for faster queries:

```javascript
mcp__toggl__toggl_warm_cache({})
```

Run this at session start for better performance.

### Check Auth

Verify connection is valid:

```javascript
mcp__toggl__toggl_check_auth({})
```

## Best Practices

### Do

- Start timers with clear descriptions
- Assign projects for accurate reporting
- Use consistent tags across entries
- Review daily/weekly reports regularly
- Warm cache at session start

### Don't

- Leave timers running overnight unintentionally
- Create entries without descriptions
- Skip project assignment for billable work
- Forget to stop timer when switching tasks
