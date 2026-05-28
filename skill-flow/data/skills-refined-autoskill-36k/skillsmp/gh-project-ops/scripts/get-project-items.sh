#!/bin/bash
# Get all items in a project with their status
# Usage: get-project-items.sh [project-number]

PROJECT_NUM=$1

# Try to get from config if not provided
if [ -z "$PROJECT_NUM" ]; then
  if [ -f ".claude/gh-config.json" ]; then
    PROJECT_NUM=$(jq -r '.project.number' .claude/gh-config.json)
    PROJECT_ORG=$(jq -r '.project.org' .claude/gh-config.json)
  fi
fi

if [ -z "$PROJECT_NUM" ]; then
  echo "Usage: get-project-items.sh <project-number>" >&2
  echo "Or create .claude/gh-config.json with project settings" >&2
  exit 1
fi

# Get org from config or detect from repo
if [ -z "$PROJECT_ORG" ]; then
  PROJECT_ORG=$(gh repo view --json owner -q '.owner.login')
fi

gh api graphql -f query='
query($org: String!, $num: Int!) {
  organization(login: $org) {
    projectV2(number: $num) {
      title
      items(first: 100) {
        nodes {
          content {
            ... on Issue {
              title
              number
              url
              state
              repository { nameWithOwner }
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
' -f org="$PROJECT_ORG" -F num="$PROJECT_NUM" --jq '
.data.organization.projectV2.items.nodes | map({
  title: .content.title,
  number: .content.number,
  url: .content.url,
  state: .content.state,
  repo: .content.repository.nameWithOwner,
  status: (.fieldValues.nodes[] | select(.field.name == "Status") | .name) // "No Status"
})
'
