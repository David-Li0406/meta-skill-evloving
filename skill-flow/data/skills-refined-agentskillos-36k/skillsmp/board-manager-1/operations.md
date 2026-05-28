# Board Manager Operations

## Overview

Operations for managing issues on the GitHub Project Board.

## Quick Reference

| Operation | Command |
|-----------|---------|
| Add to project | `gh project item-add 8 --owner joeczar --url <issue-url>` |
| List items | `gh project item-list 8 --owner joeczar` |
| Move to In Progress | See GraphQL below |
| Move to Done | See GraphQL below |

## Add Issue to Project

When starting work on an issue, ensure it's on the board:

```bash
gh project item-add 8 --owner joeczar --url "https://github.com/joeczar/code-graph-mcp/issues/<number>"
```

This is idempotent - safe to run even if already added.

## Get Project Item ID

To update an item's status, you need its project item ID:

```bash
gh project item-list 8 --owner joeczar --format json | jq '.items[] | select(.content.number == <issue_number>) | .id'
```

Or via GraphQL:

```bash
gh api graphql -f query='
query {
  user(login: "joeczar") {
    projectV2(number: 8) {
      items(first: 100) {
        nodes {
          id
          content {
            ... on Issue {
              number
            }
          }
        }
      }
    }
  }
}' | jq '.data.user.projectV2.items.nodes[] | select(.content.number == <issue_number>) | .id'
```

## Move to In Progress

```bash
ITEM_ID="<from-above>"
gh api graphql -f query='
mutation {
  updateProjectV2ItemFieldValue(input: {
    projectId: "PVT_kwHOAbYJAM4BM5GY"
    itemId: "'"$ITEM_ID"'"
    fieldId: "PVTSSF_lAHOAbYJAM4BM5GYzg8C2zk"
    value: { singleSelectOptionId: "47fc9ee4" }
  }) {
    projectV2Item { id }
  }
}'
```

## Move to Done

```bash
ITEM_ID="<from-above>"
gh api graphql -f query='
mutation {
  updateProjectV2ItemFieldValue(input: {
    projectId: "PVT_kwHOAbYJAM4BM5GY"
    itemId: "'"$ITEM_ID"'"
    fieldId: "PVTSSF_lAHOAbYJAM4BM5GYzg8C2zk"
    value: { singleSelectOptionId: "98236657" }
  }) {
    projectV2Item { id }
  }
}'
```

## Helper Function

For repeated use, here's a bash function pattern:

```bash
move_issue_status() {
  local issue_number=$1
  local status_id=$2  # f75ad846=Todo, 47fc9ee4=InProgress, 98236657=Done

  # Get item ID
  local item_id=$(gh project item-list 8 --owner joeczar --format json | \
    jq -r '.items[] | select(.content.number == '$issue_number') | .id')

  if [ -z "$item_id" ]; then
    echo "Issue #$issue_number not found on project board"
    return 1
  fi

  # Update status
  gh api graphql -f query='
  mutation {
    updateProjectV2ItemFieldValue(input: {
      projectId: "PVT_kwHOAbYJAM4BM5GY"
      itemId: "'"$item_id"'"
      fieldId: "PVTSSF_lAHOAbYJAM4BM5GYzg8C2zk"
      value: { singleSelectOptionId: "'"$status_id"'" }
    }) {
      projectV2Item { id }
    }
  }'
}

# Usage:
# move_issue_status 12 "47fc9ee4"  # Move #12 to In Progress
# move_issue_status 12 "98236657"  # Move #12 to Done
```

## Workflow Integration

### In setup-agent

After assigning self to issue:
1. Add issue to project board
2. Move to "In Progress"

### In finalize-agent

After PR creation:
1. Move to "Done" (or leave for PR merge to handle)

## Error Handling

### Issue Not on Board

If item ID query returns empty:
```bash
# Add issue first
gh project item-add 8 --owner joeczar --url "https://github.com/joeczar/code-graph-mcp/issues/<number>"
# Then retry the status update
```

### GraphQL Errors

Common issues:
- Invalid item ID: Issue not on board
- Invalid option ID: Check config.md for correct IDs
- Permission denied: Check gh auth status
