# GraphQL Fallback for GitHub Projects

When the `gh project` CLI is insufficient, use `gh api graphql` with these templates.

## 1. Fetch Project Items with All Field Values

This query is useful for seeing exactly what data is stored in custom fields.

```graphql
query($owner: String!, $number: Int!) {
  organization(login: $owner) {
    projectV2(number: $number) {
      items(first: 20) {
        nodes {
          id
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2FieldCommon { name } }
              }
              ... on ProjectV2ItemFieldTextValue {
                text
                field { ... on ProjectV2FieldCommon { name } }
              }
            }
          }
          content {
            ... on Issue {
              title
              number
            }
          }
        }
      }
    }
  }
}
```

## 2. Bulk Add Items (Abstract Example)

Adding items in bulk requires a mutation.

```graphql
mutation($projectId: ID!, $contentId: ID!) {
  addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
    item {
      id
    }
  }
}
```

## Tips for GraphQL
- Use the **GitHub GraphQL Explorer** to test queries.
- Most `ProjectV2` objects are identified by global `ID`s (strings starting with `PVT`).
- `gh api graphql -f query='...' -f owner='...'` simplifies passing variables.
