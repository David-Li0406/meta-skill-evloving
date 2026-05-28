# GitHub API Queries Reference

## Project ID
`PVT_kwHOCOopjs4BLVik` (ACT Ecosystem Development)

## Fields Available
- Status, Sprint, Priority, Type, Effort
- ACT Project, Milestone, Due Date

## Fetch Backlog Issues

```graphql
query {
  node(id: "PVT_kwHOCOopjs4BLVik") {
    ... on ProjectV2 {
      items(first: 100, filter: {fieldValues: [{fieldId: "SPRINT_FIELD_ID", value: "Backlog"}]}) {
        nodes {
          content {
            ... on Issue {
              title
              number
              repository { name }
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
```

## Create Issue

```bash
gh issue create \
  --repo ${repo} \
  --title "${title}" \
  --body "${description}" \
  --label "Type: ${type},Priority: ${priority}"
```

## Add to Project

```graphql
mutation {
  addProjectV2ItemById(input: {
    projectId: "PVT_kwHOCOopjs4BLVik"
    contentId: "${issueNodeId}"
  }) {
    item { id }
  }
}
```

## Set Field Value

```graphql
mutation {
  updateProjectV2ItemFieldValue(input: {
    projectId: "PVT_kwHOCOopjs4BLVik"
    itemId: "${itemId}"
    fieldId: "${fieldId}"
    value: { singleSelectOptionId: "${optionId}" }
  }) {
    projectV2Item { id }
  }
}
```
