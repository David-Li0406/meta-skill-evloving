# Projects

Projects in Linear group related issues toward a larger goal. They have progress tracking, timelines, and team associations.

## Listing Projects

### Basic List
```bash
linctl project list --json
linctl project ls --json          # Alias
```

**Important**: By default, only shows projects created in the last 6 months.

### Filtering Options

| Flag | Description | Example |
|------|-------------|---------|
| `--team`, `-t` | Filter by team key | `--team ENG` |
| `--state`, `-s` | Filter by project state | `--state started` |
| `--include-completed`, `-c` | Include completed/canceled | `--include-completed` |
| `--limit`, `-l` | Max results (default 50) | `--limit 100` |
| `--newer-than`, `-n` | Time filter | `--newer-than 1_year_ago` |
| `--sort`, `-o` | Sort order | `--sort updated` |

### Project States

| State | Description |
|-------|-------------|
| `planned` | Not yet started |
| `started` | Currently in progress |
| `paused` | Temporarily on hold |
| `completed` | Successfully finished |
| `canceled` | Will not be completed |

### List Examples

```bash
# All active projects
linctl project list --json

# Projects for a specific team
linctl project list --team ENG --json

# Only in-progress projects
linctl project list --state started --json

# All projects including completed
linctl project list --include-completed --newer-than all_time --json

# Recently updated projects
linctl project list --sort updated --json

# Paused projects that need attention
linctl project list --state paused --json
```

## Getting Project Details

Projects are identified by UUID (not readable IDs like issues).

```bash
# First, get the project ID from list
linctl project list --json | jq '.[] | {name, id}'

# Then get details
linctl project get 65a77a62-ec5e-491e-b1d9-84aebee01b33 --json
linctl project show 65a77a62-ec5e-491e-b1d9-84aebee01b33 --json    # Alias
```

### JSON Response Structure

```json
{
  "id": "65a77a62-ec5e-491e-b1d9-84aebee01b33",
  "name": "Q1 Product Launch",
  "description": "Launch new features for Q1",
  "state": "started",
  "progress": 0.65,
  "scope": 20,
  "issueCountHistory": {
    "completed": 13,
    "started": 4,
    "unstarted": 2,
    "backlog": 1
  },
  "teams": [
    {
      "key": "ENG",
      "name": "Engineering"
    },
    {
      "key": "DESIGN",
      "name": "Design"
    }
  ],
  "members": [
    {
      "name": "John Doe",
      "email": "john@example.com"
    }
  ],
  "lead": {
    "name": "Jane Smith",
    "email": "jane@example.com"
  },
  "initiative": {
    "name": "2024 Growth"
  },
  "startDate": "2024-01-01",
  "targetDate": "2024-03-31",
  "createdAt": "2023-12-15T10:00:00Z",
  "updatedAt": "2024-01-20T14:30:00Z",
  "completedAt": null,
  "url": "https://linear.app/team/project/q1-product-launch"
}
```

### Key Fields Explained

| Field | Description |
|-------|-------------|
| `progress` | Completion percentage (0.0 - 1.0) |
| `scope` | Total number of issues in project |
| `issueCountHistory` | Breakdown by issue state |
| `teams` | All teams contributing to project |
| `members` | Individuals assigned to project |
| `lead` | Project lead/owner |
| `initiative` | Parent initiative (if any) |
| `startDate` | Planned start date |
| `targetDate` | Target completion date |
| `completedAt` | Actual completion date (if done) |

## Working with Project Data

### Find Projects by Progress

```bash
# Projects nearly complete (>80%)
linctl project list --json | jq '.[] | select(.progress > 0.8) | {name, progress}'

# Projects with low progress that might be at risk
linctl project list --json | jq '.[] | select(.progress < 0.2 and .state == "started") | {name, progress}'

# Stalled projects (started but 0% progress)
linctl project list --json | jq '.[] | select(.progress == 0 and .state == "started")'
```

### Project Health Check

```bash
# Get project stats
linctl project get <uuid> --json | jq '{
  name,
  progress: (.progress * 100 | floor | tostring + "%"),
  completed: .issueCountHistory.completed,
  inProgress: .issueCountHistory.started,
  todo: .issueCountHistory.unstarted,
  backlog: .issueCountHistory.backlog,
  total: .scope
}'
```

### Find Projects by Team

```bash
# All projects a team is involved in
linctl project list --team ENG --json | jq '.[] | {name, state, progress}'

# Cross-team projects
linctl project list --json | jq '.[] | select(.teams | length > 1) | {name, teams: [.teams[].key]}'
```

### Timeline Analysis

```bash
# Projects past their target date
linctl project list --json | jq --arg today "$(date +%Y-%m-%d)" '
  .[] | select(.targetDate != null and .targetDate < $today and .state == "started") |
  {name, targetDate, progress}
'

# Projects starting soon
linctl project list --json | jq '.[] | select(.state == "planned") | {name, startDate}'
```

## Project Hierarchy

Projects can belong to **Initiatives** (higher-level groupings):

```bash
# See which initiative a project belongs to
linctl project get <uuid> --json | jq '.initiative'

# Find all projects in an initiative
linctl project list --json | jq '.[] | select(.initiative.name == "2024 Growth") | .name'
```

## Finding Issues in a Project

Issues reference their project. To find issues in a specific project:

```bash
# Get project ID
PROJECT_ID=$(linctl project list --json | jq -r '.[] | select(.name == "Q1 Launch") | .id')

# Issues are associated via the project field
# Note: linctl doesn't have direct project filter for issues
# Use team filter and cross-reference
linctl issue list --team ENG --json | jq --arg pid "$PROJECT_ID" '
  .[] | select(.project.id == $pid)
'
```

## Workflow Examples

### Project Status Report

```bash
#!/bin/bash
# Generate status for all active projects

echo "# Active Projects Status"
echo ""

linctl project list --state started --json | jq -r '.[] | "## \(.name)\n- Progress: \(.progress * 100 | floor)%\n- Completed: \(.issueCountHistory.completed)/\(.scope)\n- Target: \(.targetDate // "Not set")\n"'
```

### Find At-Risk Projects

```bash
# Projects that are behind schedule
linctl project list --state started --json | jq '
  .[] |
  select(.progress < 0.5 and .targetDate != null) |
  {
    name,
    progress: "\(.progress * 100 | floor)%",
    targetDate,
    remaining: (.scope - .issueCountHistory.completed)
  }
'
```

### Team Workload Analysis

```bash
# How many active projects per team
linctl project list --state started --json | jq '
  [.[].teams[].key] | group_by(.) | map({team: .[0], count: length})
'
```
