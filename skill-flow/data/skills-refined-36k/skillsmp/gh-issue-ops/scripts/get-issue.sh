#!/bin/bash
# Get full issue details including type
# Usage: get-issue.sh <number>

NUMBER=$1

if [ -z "$NUMBER" ]; then
  echo "Usage: get-issue.sh <number>" >&2
  exit 1
fi

OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')

# Get basic issue info
BASIC=$(gh issue view "$NUMBER" --json title,body,state,url,labels,assignees)

# Get type via GraphQL
TYPE=$(gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $number) {
      issueType { name }
    }
  }
}
' -f owner="$OWNER" -f repo="$REPO" -F number="$NUMBER" --jq '.data.repository.issue.issueType.name // "none"')

# Combine results
echo "$BASIC" | jq --arg type "$TYPE" '. + {type: $type}'
