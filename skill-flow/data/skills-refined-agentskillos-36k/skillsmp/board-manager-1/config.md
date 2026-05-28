# Board Manager Configuration

## Project Details

| Property | Value |
|----------|-------|
| Project Number | 8 |
| Project Node ID | `PVT_kwHOAbYJAM4BM5GY` |
| Owner | joeczar |
| Repository | joeczar/code-graph-mcp |

## Status Field

| Property | Value |
|----------|-------|
| Field ID | `PVTSSF_lAHOAbYJAM4BM5GYzg8C2zk` |
| Field Name | Status |

### Status Options

| Status | Option ID | Use For |
|--------|-----------|---------|
| Todo | `f75ad846` | Backlog, not started |
| In Progress | `47fc9ee4` | Currently working |
| Done | `98236657` | Completed |

## GraphQL Mutations

### Add Issue to Project

```graphql
mutation AddIssueToProject($projectId: ID!, $contentId: ID!) {
  addProjectV2ItemById(input: {
    projectId: $projectId
    contentId: $contentId
  }) {
    item {
      id
    }
  }
}
```

Variables:
```json
{
  "projectId": "PVT_kwHOAbYJAM4BM5GY",
  "contentId": "<issue-node-id>"
}
```

### Update Item Status

```graphql
mutation UpdateItemStatus($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $projectId
    itemId: $itemId
    fieldId: $fieldId
    value: {
      singleSelectOptionId: $optionId
    }
  }) {
    projectV2Item {
      id
    }
  }
}
```

Variables for "In Progress":
```json
{
  "projectId": "PVT_kwHOAbYJAM4BM5GY",
  "itemId": "<project-item-id>",
  "fieldId": "PVTSSF_lAHOAbYJAM4BM5GYzg8C2zk",
  "optionId": "47fc9ee4"
}
```

## CLI Commands

### Add Issue to Project

```bash
gh project item-add 8 --owner joeczar --url "https://github.com/joeczar/code-graph-mcp/issues/<number>"
```

### View Project Items

```bash
gh project item-list 8 --owner joeczar --format json
```

### Update Item Status (via GraphQL)

```bash
gh api graphql -f query='
mutation {
  updateProjectV2ItemFieldValue(input: {
    projectId: "PVT_kwHOAbYJAM4BM5GY"
    itemId: "<item-id>"
    fieldId: "PVTSSF_lAHOAbYJAM4BM5GYzg8C2zk"
    value: {
      singleSelectOptionId: "<option-id>"
    }
  }) {
    projectV2Item { id }
  }
}'
```

## Usage in Workflows

### Start Working on Issue

1. Add issue to project (if not already)
2. Set status to "In Progress"

```bash
# Add to project
gh project item-add 8 --owner joeczar --url "https://github.com/joeczar/code-graph-mcp/issues/{number}"

# Get item ID (from add output or query)
# Then update status to In Progress
```

### Complete Issue

1. Set status to "Done"
2. (PR merge will auto-close issue)
