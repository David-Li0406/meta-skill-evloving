# Logging Time to Jira Tickets

Complete guide to logging work time (worklogs) to Jira tickets using the `log_worklog.py` script.

## Overview

Worklogs track time spent on Jira tickets. This script allows you to log time with flexible date formats, custom comments, and dry-run preview capabilities.

## Quick Start

```bash
# Log 2 hours 30 minutes to a ticket for a specific date
python3 scripts/log_worklog.py PROJ-123 "2h 30m" --date 2026-01-20

# Log time for yesterday
python3 scripts/log_worklog.py PROJ-123 "1h" --date yesterday

# Log time for today
python3 scripts/log_worklog.py PROJ-123 "45m" --date today

# Preview without logging (dry run)
python3 scripts/log_worklog.py PROJ-123 "2h" --date today --dry-run
```

## Time Format

The script accepts time in hours and/or minutes:

| Format | Example | Result |
|--------|---------|--------|
| Hours only | `"2h"` | 2 hours |
| Minutes only | `"30m"` | 30 minutes |
| Combined | `"2h 30m"` | 2 hours 30 minutes |
| Combined | `"1h 45m"` | 1 hour 45 minutes |

**Notes:**
- Time is case-insensitive (`2H` = `2h`)
- Spaces between hours and minutes are optional
- At least hours OR minutes must be specified

## Date Formats

Multiple date formats are supported:

| Format | Example | Description |
|--------|---------|-------------|
| `today` | `--date today` | Current date |
| `now` | `--date now` | Current date (alias) |
| `yesterday` | `--date yesterday` | Previous day |
| `YYYY-MM-DD` | `--date 2026-01-20` | ISO date format |
| `M/D` | `--date 1/20` | Month/Day (current year) |
| `M-D` | `--date 1-20` | Month-Day (current year) |

## Commands

### Basic Worklog

Log time with auto-generated comment (ticket key + summary):

```bash
python3 scripts/log_worklog.py PROJ-123 "2h" --date 2026-01-20
```

**Output:**
```
Logging time to Jira:
  Ticket:  PROJ-123
  Summary: Implement user authentication
  Date:    2026-01-20
  Time:    2h
  Comment: PROJ-123: Implement user authentication

✅ Worklog created successfully!
  Worklog ID: 12345
  View: https://orases.atlassian.net/browse/PROJ-123?focusedWorklogId=12345
```

### Custom Comment

Add a descriptive comment to the worklog:

```bash
python3 scripts/log_worklog.py PROJ-123 "3h" --date yesterday --comment "Code review and bug fixes"
```

### Preview with Dry Run

See what would be logged without making changes:

```bash
python3 scripts/log_worklog.py PROJ-123 "2h 30m" --date today --dry-run
```

**Output:**
```
[DRY RUN] Logging time to Jira:
  Ticket:  PROJ-123
  Summary: Implement user authentication
  Date:    2026-01-21
  Time:    2h 30m
  Comment: PROJ-123: Implement user authentication

[DRY RUN] No changes made.
```

## Natural Language Patterns

When using the Jira skill, these phrases trigger worklog actions:

| User Says | Action |
|-----------|--------|
| "log 2 hours to PROJ-123 for yesterday" | Log worklog |
| "add 30 minutes to PROJ-123 for today" | Log worklog |
| "track 1h 30m on PROJ-123 for 2026-01-20" | Log worklog |
| "log time to PROJ-123" | Prompt for details |

## Common Workflows

### End of Day Time Logging

Log time at the end of each workday:

```bash
# Log today's work
python3 scripts/log_worklog.py PROJ-123 "4h" --date today --comment "Feature implementation"
python3 scripts/log_worklog.py PROJ-456 "2h" --date today --comment "Code review"
```

### Catch-up Logging

Log time from previous days:

```bash
# Log from yesterday
python3 scripts/log_worklog.py PROJ-123 "6h" --date yesterday

# Log from a specific date
python3 scripts/log_worklog.py PROJ-123 "8h" --date 2026-01-15
```

### Quick Meeting Time

Log short time entries:

```bash
python3 scripts/log_worklog.py PROJ-123 "30m" --date today --comment "Sprint planning meeting"
```

## Error Handling

### Invalid Time Format

```
Error: Invalid time format '2hours'. Use formats like '2h', '30m', '2h 30m'
```

**Solution:** Use correct format with `h` for hours and `m` for minutes.

### Invalid Date Format

```
Error: Cannot parse date 'jan-20'. Use YYYY-MM-DD, M/D, 'today', or 'yesterday'
```

**Solution:** Use supported date formats (see Date Formats section).

### Ticket Not Found (404)

```
Error: HTTP 404: Issue does not exist or you do not have permission to see it
```

**Solution:** Verify ticket key and your access permissions.

### Authentication Error (401)

```
Error: HTTP 401: Basic authentication with passwords is deprecated.
```

**Solution:** Regenerate your API token at:
https://id.atlassian.com/manage-profile/security/api-tokens

### Missing Credentials

```
❌ Error: Missing credentials

Required environment variables:
  - ATLASSIAN_EMAIL
  - ATLASSIAN_API_TOKEN
```

**Solution:** Set environment variables (see `scripts/SETUP.md`).

## Script Reference

**Location:** `scripts/log_worklog.py`

**Arguments:**

| Argument | Description |
|----------|-------------|
| `ISSUE_KEY` | Jira ticket key (e.g., PROJ-123) |
| `TIME_SPENT` | Time to log (e.g., "2h", "30m", "2h 30m") |

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--date` | `-d` | Date of work (required) |
| `--comment` | `-c` | Custom comment (default: "TICKET: Summary") |
| `--dry-run` | `-n` | Preview without making changes |
| `--site` | | Override Atlassian site hostname |

## Environment Variables

```bash
ATLASSIAN_EMAIL="your.email@company.com"
ATLASSIAN_API_TOKEN="ATATT..."
ATLASSIAN_SITE="yoursite.atlassian.net"
```

## Script Features

- No external dependencies (Python 3.6+ standard library only)
- API token authentication
- Flexible date parsing (today, yesterday, ISO format, M/D)
- Auto-generated comments from ticket summary
- Dry-run mode for previewing changes
- ADF (Atlassian Document Format) comment support
- Clear error messages with actionable solutions
