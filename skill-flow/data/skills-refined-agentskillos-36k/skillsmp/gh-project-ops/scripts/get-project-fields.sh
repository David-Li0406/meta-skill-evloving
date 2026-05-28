#!/bin/bash
# Get available fields and options for a project
# Usage: get-project-fields.sh [project-number]

PROJECT_NUM=$1

# Try to get from config if not provided
if [ -z "$PROJECT_NUM" ]; then
  if [ -f ".claude/gh-config.json" ]; then
    PROJECT_NUM=$(jq -r '.project.number' .claude/gh-config.json)
    PROJECT_ORG=$(jq -r '.project.org' .claude/gh-config.json)
  fi
fi

if [ -z "$PROJECT_NUM" ]; then
  echo "Usage: get-project-fields.sh <project-number>" >&2
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
      fields(first: 20) {
        nodes {
          ... on ProjectV2SingleSelectField {
            name
            options { name id }
          }
          ... on ProjectV2Field {
            name
          }
        }
      }
    }
  }
}
' -f org="$PROJECT_ORG" -F num="$PROJECT_NUM" --jq '.data.organization.projectV2'
