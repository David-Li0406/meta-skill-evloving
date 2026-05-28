# Filtering & Sorting

Control what data you retrieve and how it's ordered.

## Time-Based Filtering

### The 6-Month Default

**Critical**: List commands only show items from the last 6 months by default.

```bash
# These only show recent items:
linctl issue list --json              # Last 6 months
linctl project list --json            # Last 6 months

# To see everything:
linctl issue list --newer-than all_time --json
linctl project list --newer-than all_time --json
```

### The --newer-than Flag

Available on `issue list` and `project list`.

```bash
linctl issue list --newer-than <time-expression> --json
linctl issue list -n <time-expression> --json    # Short form
```

### Time Expression Formats

#### Relative Time (N_units_ago)

| Expression | Meaning |
|------------|---------|
| `30_minutes_ago` | Last 30 minutes |
| `2_hours_ago` | Last 2 hours |
| `1_day_ago` | Last 24 hours |
| `3_days_ago` | Last 3 days |
| `1_week_ago` | Last 7 days |
| `2_weeks_ago` | Last 14 days |
| `1_month_ago` | Last 30 days |
| `3_months_ago` | Last 90 days |
| `6_months_ago` | Last 6 months (default) |
| `1_year_ago` | Last 365 days |

Valid units: `minutes`, `hours`, `days`, `weeks`, `months`, `years`

#### Special Values

| Value | Meaning |
|-------|---------|
| `all_time` | No date filter (show everything) |

#### ISO Dates

```bash
# Specific date
linctl issue list --newer-than 2025-01-01 --json

# With time
linctl issue list --newer-than 2025-01-01T00:00:00Z --json
```

### Time Filter Examples

```bash
# Today's issues
linctl issue list --newer-than 1_day_ago --json

# This week's activity
linctl issue list --newer-than 1_week_ago --json

# Sprint planning (last 2 weeks)
linctl issue list --newer-than 2_weeks_ago --json

# Monthly review
linctl issue list --newer-than 1_month_ago --json

# Quarterly review
linctl project list --newer-than 3_months_ago --json

# Year in review
linctl issue list --newer-than 1_year_ago --include-completed --json

# Everything ever
linctl issue list --newer-than all_time --include-completed --json

# Since specific date
linctl issue list --newer-than 2024-07-01 --json
```

## Completion Filtering

### Hidden by Default

By default, `issue list` hides completed and canceled issues.

```bash
# Only active issues (default)
linctl issue list --json

# Include completed/canceled
linctl issue list --include-completed --json
linctl issue list -c --json    # Short form
```

### Project Completion

Same applies to projects:

```bash
# Active projects only (default)
linctl project list --json

# Include completed/canceled projects
linctl project list --include-completed --json
```

## Sorting

### The --sort Flag

Available on all list commands.

```bash
linctl issue list --sort <order> --json
linctl issue list -o <order> --json    # Short form
```

### Sort Orders

| Order | Description |
|-------|-------------|
| `linear` | Linear's default/UI order (respects manual ordering) |
| `created` | By creation date (newest first) |
| `updated` | By last update (most recently modified first) |

### Sort Examples

```bash
# Most recently updated issues
linctl issue list --sort updated --json

# Newest issues first
linctl issue list --sort created --json

# Recently updated projects
linctl project list --sort updated --json

# Newest comments
linctl comment list LIN-123 --sort created --json

# Recently active users
linctl user list --sort updated --json
```

## Combining Filters

Filters can be combined for precise queries.

### Issue Combinations

```bash
# My recent work
linctl issue list \
  --assignee me \
  --newer-than 2_weeks_ago \
  --sort updated \
  --json

# Team's urgent items
linctl issue list \
  --team ENG \
  --priority 1 \
  --state "In Progress" \
  --json

# All completed issues this quarter
linctl issue list \
  --include-completed \
  --state "Done" \
  --newer-than 3_months_ago \
  --sort created \
  --json

# Unassigned bugs this week
linctl issue list \
  --assignee unassigned \
  --newer-than 1_week_ago \
  --json

# Everything I touched recently
linctl issue list \
  --assignee me \
  --include-completed \
  --newer-than 1_month_ago \
  --sort updated \
  --json
```

### Project Combinations

```bash
# Active team projects
linctl project list \
  --team ENG \
  --state started \
  --json

# All projects this year
linctl project list \
  --newer-than 1_year_ago \
  --include-completed \
  --sort created \
  --json

# Recently updated paused projects
linctl project list \
  --state paused \
  --sort updated \
  --json
```

## Pagination

### The --limit Flag

Control how many results are returned.

```bash
linctl issue list --limit 100 --json
linctl issue list -l 100 --json    # Short form
```

Default is 50 for all list commands.

### Examples

```bash
# Get more results
linctl issue list --limit 200 --json

# Quick check (just a few)
linctl issue list --limit 5 --json

# Large export
linctl issue list --newer-than all_time --include-completed --limit 1000 --json
```

## Filter Quick Reference

### Issue Filters

| Flag | Short | Description |
|------|-------|-------------|
| `--assignee` | `-a` | Filter by assignee (`me`, email, `unassigned`) |
| `--state` | `-s` | Filter by state name |
| `--team` | `-t` | Filter by team key |
| `--priority` | `-r` | Filter by priority (0-4) |
| `--include-completed` | `-c` | Include done/canceled |
| `--newer-than` | `-n` | Time filter |
| `--sort` | `-o` | Sort order |
| `--limit` | `-l` | Max results |

### Project Filters

| Flag | Short | Description |
|------|-------|-------------|
| `--team` | `-t` | Filter by team key |
| `--state` | `-s` | Filter by project state |
| `--include-completed` | `-c` | Include completed/canceled |
| `--newer-than` | `-n` | Time filter |
| `--sort` | `-o` | Sort order |
| `--limit` | `-l` | Max results |

### User Filters

| Flag | Short | Description |
|------|-------|-------------|
| `--active` | `-a` | Show only active users |
| `--sort` | `-o` | Sort order |
| `--limit` | `-l` | Max results |

## Performance Tips

1. **Use time filters** - Avoid `all_time` on large workspaces
2. **Add specific filters** - Team, assignee, state narrow results fast
3. **Reasonable limits** - Don't request 10000 when you need 10
4. **Combine intelligently** - More filters = fewer results = faster

```bash
# Slow (gets everything)
linctl issue list --newer-than all_time --json

# Fast (specific query)
linctl issue list --team ENG --assignee me --state "In Progress" --json
```
