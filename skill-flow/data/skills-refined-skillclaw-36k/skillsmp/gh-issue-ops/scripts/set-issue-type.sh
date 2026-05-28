#!/bin/bash
# Set issue type by name (resolves ID dynamically)
# Usage: set-issue-type.sh <number> <type-name>

NUMBER=$1
TYPE_NAME=$2

if [ -z "$NUMBER" ] || [ -z "$TYPE_NAME" ]; then
  echo "Usage: set-issue-type.sh <number> <type-name>" >&2
  exit 1
fi

OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')

# Get type ID by name (case-insensitive)
TYPE_ID=$(gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    issueTypes(first: 20) {
      nodes { id name }
    }
  }
}
' -f owner="$OWNER" -f repo="$REPO" --jq ".data.repository.issueTypes.nodes[] | select(.name | ascii_downcase == \"$(echo "$TYPE_NAME" | tr '[:upper:]' '[:lower:]')\") | .id")

if [ -z "$TYPE_ID" ]; then
  echo "Error: Type '$TYPE_NAME' not found in repo" >&2
  echo "Available types:" >&2
  gh api graphql -f query='
  query($owner: String!, $repo: String!) {
    repository(owner: $owner, name: $repo) {
      issueTypes(first: 20) { nodes { name } }
    }
  }
  ' -f owner="$OWNER" -f repo="$REPO" --jq '.data.repository.issueTypes.nodes[].name' >&2
  exit 1
fi

# Get issue node ID
NODE_ID=$(gh api "repos/$OWNER/$REPO/issues/$NUMBER" --jq '.node_id')

if [ -z "$NODE_ID" ]; then
  echo "Error: Issue #$NUMBER not found" >&2
  exit 1
fi

# Set type
gh api graphql -f query="
mutation {
  updateIssue(input: {id: \"$NODE_ID\", issueTypeId: \"$TYPE_ID\"}) {
    issue { id title }
  }
}
" --jq '.data.updateIssue.issue'

echo "Set issue #$NUMBER type to $TYPE_NAME"
