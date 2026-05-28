#!/bin/bash
# Get issues that had status changes today
# Usage: get-status-changes-today.sh [project-number]

PROJECT_NUM=$1
TODAY=$(date +%Y-%m-%d)

# Try to get from config if not provided
if [ -z "$PROJECT_NUM" ]; then
  if [ -f ".claude/gh-config.json" ]; then
    PROJECT_NUM=$(jq -r '.project.number' .claude/gh-config.json)
    PROJECT_ORG=$(jq -r '.project.org' .claude/gh-config.json)
  fi
fi

if [ -z "$PROJECT_NUM" ]; then
  echo "Usage: get-status-changes-today.sh <project-number>" >&2
  echo "Or create .claude/gh-config.json with project settings" >&2
  exit 1
fi

# Get org from config or detect from repo
if [ -z "$PROJECT_ORG" ]; then
  PROJECT_ORG=$(gh repo view --json owner -q '.owner.login')
fi

# Get all project items first
ITEMS=$(gh api graphql -f query='
query($org: String!, $num: Int!) {
  organization(login: $org) {
    projectV2(number: $num) {
      items(first: 100) {
        nodes {
          content {
            ... on Issue {
              number
              title
              repository { owner { login } name }
            }
          }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2SingleSelectField { name } }
              }
            }
          }
        }
      }
    }
  }
}
' -f org="$PROJECT_ORG" -F num="$PROJECT_NUM")

# Parse items and check timeline for each
echo "$ITEMS" | jq -r '
.data.organization.projectV2.items.nodes[] |
select(.content.number != null) |
"\(.content.repository.owner.login)/\(.content.repository.name) \(.content.number) \(.content.title) \(.fieldValues.nodes[] | select(.field.name == "Status") | .name // "No Status")"
' | while read -r owner_repo number title status; do
  OWNER=$(echo "$owner_repo" | cut -d'/' -f1)
  REPO=$(echo "$owner_repo" | cut -d'/' -f2)

  # Check if this issue had status changes today
  CHANGED_TODAY=$(gh api "repos/$OWNER/$REPO/issues/$number/timeline" --jq "
    [.[] | select(.event == \"project_v2_item_status_changed\" and (.created_at | startswith(\"$TODAY\")))] | length
  " 2>/dev/null)

  if [ "$CHANGED_TODAY" -gt 0 ]; then
    echo "{\"number\": $number, \"title\": \"$title\", \"status\": \"$status\", \"repo\": \"$owner_repo\", \"changed_today\": true}"
  fi
done | jq -s '.'
