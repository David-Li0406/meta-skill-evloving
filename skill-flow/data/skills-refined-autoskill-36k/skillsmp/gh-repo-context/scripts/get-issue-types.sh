#!/bin/bash
# Get available issue types for current repo

OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')

gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    issueTypes(first: 20) {
      nodes { id name description }
    }
  }
}
' -f owner="$OWNER" -f repo="$REPO" --jq '.data.repository.issueTypes.nodes'
