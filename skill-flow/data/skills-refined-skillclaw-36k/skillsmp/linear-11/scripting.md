# Scripting & Automation

Use linctl's JSON output for scripting, automation, and integration.

## JSON Output

Always use `--json` flag for programmatic access:

```bash
linctl issue list --json
linctl project get UUID --json
linctl team members ENG --json
```

## Parsing with jq

### Basic Extraction

```bash
# Get specific fields
linctl issue list --json | jq '.[].identifier'

# Filter and format
linctl issue list --json | jq '.[] | {id: .identifier, title}'

# Raw output (no quotes)
linctl issue list --json | jq -r '.[].identifier'
```

### Common jq Patterns

```bash
# First item
linctl issue list --json | jq '.[0]'

# Count results
linctl issue list --json | jq 'length'

# Filter by condition
linctl issue list --json | jq '.[] | select(.priority == 1)'

# Map to new structure
linctl issue list --json | jq '[.[] | {issue: .identifier, owner: .assignee.email}]'

# Sort by field
linctl issue list --json | jq 'sort_by(.priority)'

# Group by field
linctl issue list --json | jq 'group_by(.state.name)'

# Unique values
linctl issue list --json | jq '[.[].state.name] | unique'
```

### Complex Queries

```bash
# Issues with assignee email domain
linctl issue list --json | jq '.[] | select(.assignee.email | test("@company.com$"))'

# Calculate percentage
linctl project get UUID --json | jq '.progress * 100 | floor | tostring + "%"'

# Nested field access
linctl issue get LIN-123 --json | jq '.team.key + "-" + (.identifier | split("-")[1])'

# Conditional output
linctl issue list --json | jq '.[] | if .priority == 1 then "URGENT: \(.title)" else .title end'
```

## Shell Integration

### Store in Variables

```bash
# Store single value
ISSUE_ID=$(linctl issue list --limit 1 --json | jq -r '.[0].identifier')
echo "Working on: $ISSUE_ID"

# Store as array
ISSUES=($(linctl issue list --assignee me --json | jq -r '.[].identifier'))
echo "My issues: ${ISSUES[@]}"
```

### Conditionals

```bash
# Check if any urgent issues
if linctl issue list --priority 1 --json | jq -e 'length > 0' > /dev/null; then
  echo "ALERT: You have urgent issues!"
fi

# Check if issue exists
if linctl issue get LIN-123 --json 2>/dev/null | jq -e '.identifier' > /dev/null; then
  echo "Issue exists"
else
  echo "Issue not found"
fi
```

### Loops

```bash
# Process each issue
linctl issue list --assignee me --json | jq -r '.[].identifier' | while read issue; do
  echo "Processing $issue..."
  linctl issue get "$issue" --json | jq '.title'
done

# For loop with array
for issue in $(linctl issue list --limit 5 --json | jq -r '.[].identifier'); do
  echo "Issue: $issue"
done
```

## Automation Scripts

### Daily Standup Report

```bash
#!/bin/bash
# daily-standup.sh

echo "# Daily Standup - $(date +%Y-%m-%d)"
echo ""

echo "## In Progress"
linctl issue list --assignee me --state "In Progress" --json | jq -r '.[] | "- [\(.identifier)] \(.title)"'

echo ""
echo "## Completed Yesterday"
linctl issue list --assignee me --include-completed --state "Done" --newer-than 1_day_ago --json | jq -r '.[] | "- [\(.identifier)] \(.title)"'

echo ""
echo "## Blocked"
linctl issue list --assignee me --json | jq -r '.[] | select(.state.name | test("(?i)block")) | "- [\(.identifier)] \(.title)"'
```

### Create Issue from Template

```bash
#!/bin/bash
# create-bug.sh <title>

TITLE="$1"
TEAM="ENG"

if [ -z "$TITLE" ]; then
  echo "Usage: create-bug.sh <title>"
  exit 1
fi

DESCRIPTION="## Steps to Reproduce
1.
2.
3.

## Expected Behavior


## Actual Behavior


## Environment
- OS:
- Browser:
- Version: "

RESULT=$(linctl issue create \
  --title "Bug: $TITLE" \
  --team "$TEAM" \
  --description "$DESCRIPTION" \
  --priority 2 \
  --assign-me \
  --json)

ISSUE_ID=$(echo "$RESULT" | jq -r '.identifier')
echo "Created: $ISSUE_ID"
echo "URL: $(echo "$RESULT" | jq -r '.url')"
```

### Weekly Team Report

```bash
#!/bin/bash
# team-report.sh <team-key>

TEAM="${1:-ENG}"

echo "# $TEAM Weekly Report"
echo "Generated: $(date)"
echo ""

echo "## Summary"
TOTAL=$(linctl issue list --team "$TEAM" --newer-than 1_week_ago --include-completed --json | jq 'length')
COMPLETED=$(linctl issue list --team "$TEAM" --newer-than 1_week_ago --include-completed --state "Done" --json | jq 'length')
IN_PROGRESS=$(linctl issue list --team "$TEAM" --state "In Progress" --json | jq 'length')

echo "- Total issues this week: $TOTAL"
echo "- Completed: $COMPLETED"
echo "- Currently in progress: $IN_PROGRESS"
echo ""

echo "## Issues by Assignee"
linctl issue list --team "$TEAM" --newer-than 1_week_ago --json | jq -r '
  group_by(.assignee.email // "unassigned") |
  map({assignee: .[0].assignee.email // "unassigned", count: length}) |
  .[] | "- \(.assignee): \(.count)"'

echo ""
echo "## Completed Issues"
linctl issue list --team "$TEAM" --include-completed --state "Done" --newer-than 1_week_ago --json | jq -r '.[] | "- [\(.identifier)] \(.title)"'
```

### Batch Update Issues

```bash
#!/bin/bash
# bulk-update.sh - Move all backlog issues to a new state

STATE="Todo"
TEAM="ENG"

echo "Moving backlog issues to $STATE..."

linctl issue list --team "$TEAM" --state "Backlog" --json | jq -r '.[].identifier' | while read issue; do
  echo "Updating $issue..."
  linctl issue update "$issue" --state "$STATE"
done

echo "Done!"
```

### Issue Export to CSV

```bash
#!/bin/bash
# export-issues.sh

echo "identifier,title,state,assignee,priority,created"

linctl issue list --newer-than all_time --include-completed --json | jq -r '.[] | [
  .identifier,
  (.title | gsub(","; ";")),
  .state.name,
  (.assignee.email // "unassigned"),
  .priorityLabel,
  .createdAt
] | @csv'
```

## Integration Patterns

### Git Hooks

```bash
#!/bin/bash
# .git/hooks/prepare-commit-msg
# Prepend issue ID from branch name

BRANCH=$(git branch --show-current)
ISSUE=$(echo "$BRANCH" | grep -oE '[A-Z]+-[0-9]+')

if [ -n "$ISSUE" ]; then
  # Verify issue exists
  if linctl issue get "$ISSUE" --json 2>/dev/null | jq -e '.identifier' > /dev/null; then
    sed -i.bak "1s/^/[$ISSUE] /" "$1"
  fi
fi
```

### Create Branch from Issue

```bash
#!/bin/bash
# start-issue.sh <issue-id>

ISSUE="$1"

if [ -z "$ISSUE" ]; then
  echo "Usage: start-issue.sh <issue-id>"
  exit 1
fi

# Get branch name from Linear
BRANCH=$(linctl issue get "$ISSUE" --json | jq -r '.branchName')

if [ -z "$BRANCH" ] || [ "$BRANCH" = "null" ]; then
  echo "Could not get branch name for $ISSUE"
  exit 1
fi

# Create and checkout branch
git checkout -b "$BRANCH"

# Update issue status
linctl issue update "$ISSUE" --state "In Progress" --assignee me

# Add starting comment
linctl comment create "$ISSUE" --body "Started work on branch \`$BRANCH\`"

echo "Ready to work on $ISSUE"
```

### Sync with External Systems

```bash
#!/bin/bash
# sync-to-slack.sh - Post urgent issues to Slack

WEBHOOK_URL="https://hooks.slack.com/services/xxx"

URGENT=$(linctl issue list --priority 1 --json | jq '[.[] | {id: .identifier, title, assignee: .assignee.name}]')

if [ "$(echo "$URGENT" | jq 'length')" -gt 0 ]; then
  PAYLOAD=$(jq -n --argjson issues "$URGENT" '{
    text: "🚨 Urgent Issues",
    blocks: [
      {type: "header", text: {type: "plain_text", text: "🚨 Urgent Issues"}},
      {type: "section", text: {type: "mrkdwn", text: ($issues | map("• *\(.id)*: \(.title) (\(.assignee // "unassigned"))") | join("\n"))}}
    ]
  }')

  curl -X POST -H 'Content-type: application/json' --data "$PAYLOAD" "$WEBHOOK_URL"
fi
```

## Error Handling

```bash
#!/bin/bash
# Robust error handling

set -e  # Exit on error

get_issue() {
  local issue_id="$1"
  local result

  if ! result=$(linctl issue get "$issue_id" --json 2>&1); then
    echo "Error fetching $issue_id: $result" >&2
    return 1
  fi

  if echo "$result" | jq -e '.identifier' > /dev/null 2>&1; then
    echo "$result"
    return 0
  else
    echo "Invalid response for $issue_id" >&2
    return 1
  fi
}

# Usage
if issue=$(get_issue "LIN-123"); then
  echo "Title: $(echo "$issue" | jq -r '.title')"
else
  echo "Failed to get issue"
fi
```

## Environment Variables

linctl respects these environment variables:

| Variable | Purpose |
|----------|---------|
| `LINEAR_API_KEY` | API key (alternative to `linctl auth`) |
| `NO_COLOR` | Disable colored output |

```bash
# Use API key from environment
export LINEAR_API_KEY="lin_api_xxxxx"
linctl issue list --json

# Disable colors for logging
NO_COLOR=1 linctl issue list
```
