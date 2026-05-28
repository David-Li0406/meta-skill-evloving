# Teams

Teams are the organizational unit in Linear. They have their own workflows, states, and issue prefixes.

## Listing Teams

```bash
linctl team list --json
linctl team ls --json          # Alias
```

### List Options

| Flag | Description | Example |
|------|-------------|---------|
| `--limit`, `-l` | Max results (default 50) | `--limit 100` |
| `--sort`, `-o` | Sort order | `--sort created` |

### JSON Response Structure

```json
[
  {
    "id": "uuid",
    "key": "ENG",
    "name": "Engineering",
    "description": "Backend and frontend development",
    "private": false,
    "issueCount": 156,
    "memberCount": 12
  }
]
```

### List Examples

```bash
# All teams with issue counts
linctl team list --json

# Find teams by name pattern
linctl team list --json | jq '.[] | select(.name | test("(?i)eng"))'

# Teams sorted by issue count
linctl team list --json | jq 'sort_by(.issueCount) | reverse'

# Private teams
linctl team list --json | jq '.[] | select(.private == true)'

# Large teams (>10 members)
linctl team list --json | jq '.[] | select(.memberCount > 10)'
```

## Getting Team Details

Use the team **key** (e.g., `ENG`), not the display name.

```bash
linctl team get ENG --json
linctl team show ENG --json    # Alias
```

### JSON Response Structure

```json
{
  "id": "uuid",
  "key": "ENG",
  "name": "Engineering",
  "description": "Backend and frontend development team",
  "private": false,
  "issueCount": 156,
  "memberCount": 12,
  "states": [
    {
      "name": "Backlog",
      "type": "backlog",
      "color": "#bbb"
    },
    {
      "name": "Todo",
      "type": "unstarted",
      "color": "#e2e2e2"
    },
    {
      "name": "In Progress",
      "type": "started",
      "color": "#f2c94c"
    },
    {
      "name": "In Review",
      "type": "started",
      "color": "#5e6ad2"
    },
    {
      "name": "Done",
      "type": "completed",
      "color": "#5e6ad2"
    },
    {
      "name": "Canceled",
      "type": "canceled",
      "color": "#95a2b3"
    }
  ],
  "labels": [
    {
      "name": "bug",
      "color": "#eb5757"
    },
    {
      "name": "feature",
      "color": "#bb87fc"
    }
  ],
  "cycles": {
    "enabled": true,
    "duration": 2,
    "startDay": 1
  },
  "timezone": "America/Los_Angeles",
  "createdAt": "2023-01-15T10:00:00Z"
}
```

### Key Fields Explained

| Field | Description |
|-------|-------------|
| `key` | Short identifier used in issue IDs (e.g., `ENG-123`) |
| `states` | Workflow states configured for this team |
| `labels` | Issue labels available for this team |
| `cycles` | Sprint/cycle configuration |
| `private` | Whether team is visible to all workspace members |

## Listing Team Members

```bash
linctl team members ENG --json
```

### JSON Response Structure

```json
[
  {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "displayName": "John",
    "active": true,
    "admin": false,
    "avatarUrl": "https://..."
  }
]
```

### Member Query Examples

```bash
# All members of a team
linctl team members ENG --json

# Active members only
linctl team members ENG --json | jq '.[] | select(.active == true)'

# Find admins in a team
linctl team members ENG --json | jq '.[] | select(.admin == true)'

# Count team members
linctl team members ENG --json | jq 'length'

# Get member emails
linctl team members ENG --json | jq -r '.[].email'
```

## Working with Team States

Each team can have custom workflow states. Get available states:

```bash
# List all states for a team
linctl team get ENG --json | jq '.states[] | {name, type}'

# States by type
linctl team get ENG --json | jq '.states | group_by(.type) | map({type: .[0].type, states: [.[].name]})'

# Find the "done" state name
linctl team get ENG --json | jq -r '.states[] | select(.type == "completed") | .name'
```

### State Types

| Type | Description |
|------|-------------|
| `backlog` | Not yet planned for work |
| `unstarted` | Planned but not started |
| `started` | Work in progress |
| `completed` | Successfully finished |
| `canceled` | Won't be completed |

## Working with Team Labels

```bash
# List all labels for a team
linctl team get ENG --json | jq '.labels[] | {name, color}'

# Find bug-related labels
linctl team get ENG --json | jq '.labels[] | select(.name | test("(?i)bug"))'
```

## Team Cycles (Sprints)

If cycles are enabled, the team has sprints:

```bash
# Check if team uses cycles
linctl team get ENG --json | jq '.cycles'

# Output:
# {
#   "enabled": true,
#   "duration": 2,      # weeks
#   "startDay": 1       # Monday
# }
```

## Finding Which Team a User Belongs To

```bash
# Check all teams for a specific user
for team in $(linctl team list --json | jq -r '.[].key'); do
  if linctl team members "$team" --json | jq -e '.[] | select(.email == "john@example.com")' > /dev/null 2>&1; then
    echo "Found in team: $team"
  fi
done
```

Or more efficiently:
```bash
# Get user's team memberships via user details
linctl user get john@example.com --json | jq '.teams'
```

## Workflow Examples

### Onboard to a New Team

```bash
# 1. Find the team
linctl team list --json | jq '.[] | {key, name, description}'

# 2. Get team details and workflow
linctl team get ENG --json | jq '{
  name,
  description,
  states: [.states[].name],
  labels: [.labels[].name]
}'

# 3. See who's on the team
linctl team members ENG --json | jq '.[] | {name, email}'

# 4. See current team workload
linctl issue list --team ENG --state "In Progress" --json | jq 'length'
```

### Team Health Dashboard

```bash
#!/bin/bash
TEAM="ENG"

echo "# Team $TEAM Status"
echo ""

# Member count
echo "## Team Size"
linctl team members $TEAM --json | jq 'length'

# Issue distribution
echo "## Issue Breakdown"
linctl team get $TEAM --json | jq -r '.states[] | "\(.name): checking..."'

# Issues by state
for state in "Backlog" "Todo" "In Progress" "Done"; do
  count=$(linctl issue list --team $TEAM --state "$state" --include-completed --json 2>/dev/null | jq 'length')
  echo "$state: $count"
done
```

### Compare Teams

```bash
# Team sizes and workloads
linctl team list --json | jq '.[] | {
  key,
  name,
  members: .memberCount,
  issues: .issueCount,
  issuesPerMember: (if .memberCount > 0 then (.issueCount / .memberCount | floor) else 0 end)
}'
```
