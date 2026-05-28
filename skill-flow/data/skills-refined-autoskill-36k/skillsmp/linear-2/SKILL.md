---
name: linear
description: Manage issues, projects, and workflows in Linear. View issues, create new ones, search documentation, and track project progress.
---

# Linear Issue Tracking

This skill provides access to Linear via the GraphQL API.

## Setup Required

**Create a Personal API Key:**

1. Go to Linear Settings → Account → Security & Access
2. Or visit: https://linear.app/settings/account/security
3. Under "Personal API keys", click "Create key"
4. Select permissions (Read, Write, etc.) and teams
5. Copy the key

Set as environment variable:
```bash
export LINEAR_API_KEY="lin_api_..."
```

## When to Use

Use this skill when the user:
- Asks about Linear issues, tickets, or bugs
- Wants to create a new issue or feature request
- Needs to check project or cycle progress
- Asks about team workload or assignments
- Mentions "Linear" or issue tracking

## API Endpoint

Linear uses GraphQL at: `https://api.linear.app/graphql`

All requests need:
```bash
-H "Authorization: $(printenv LINEAR_API_KEY)" \
-H "Content-Type: application/json"
```

Note: No "Bearer" prefix for Linear API keys.

## Common Queries

### List My Issues
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { assignedIssues(first: 20) { nodes { identifier title state { name } priority } } } }"}' | jq '.data.viewer.assignedIssues.nodes'
```

### List All Issues
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issues(first: 50) { nodes { identifier title state { name } assignee { name } priority } } }"}' | jq '.data.issues.nodes'
```

### Get Issue by ID
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issue(id: \"ISSUE_UUID\") { identifier title description state { name } assignee { name } priority labels { nodes { name } } } }"}'
```

### Search Issues by Identifier (e.g., ENG-123)
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issueSearch(query: \"ENG-123\", first: 5) { nodes { identifier title state { name } } } }"}'
```

### List Teams
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ teams { nodes { id name key } } }"}' | jq '.data.teams.nodes'
```

### List Projects
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ projects(first: 20) { nodes { id name state progress } } }"}' | jq '.data.projects.nodes'
```

### List Workflow States
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ workflowStates { nodes { id name type } } }"}' | jq '.data.workflowStates.nodes'
```

### List Labels
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issueLabels { nodes { id name color } } }"}' | jq '.data.issueLabels.nodes'
```

### Get Current User Info
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { id name email } }"}'
```

### List Current Cycle Issues
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ cycles(filter: { isActive: { eq: true } }, first: 1) { nodes { name issues { nodes { identifier title state { name } } } } } }"}'
```

## Mutations (Creating/Updating)

### Create Issue
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation CreateIssue($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { identifier title url } } }",
    "variables": {
      "input": {
        "teamId": "TEAM_UUID",
        "title": "Issue title",
        "description": "Issue description",
        "priority": 2
      }
    }
  }'
```

### Add Comment to Issue
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation AddComment($input: CommentCreateInput!) { commentCreate(input: $input) { success comment { id body } } }",
    "variables": {
      "input": {
        "issueId": "ISSUE_UUID",
        "body": "Comment text here"
      }
    }
  }'
```

### Update Issue State
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) { issueUpdate(id: $id, input: $input) { success issue { identifier state { name } } } }",
    "variables": {
      "id": "ISSUE_UUID",
      "input": {
        "stateId": "STATE_UUID"
      }
    }
  }'
```

## Common Workflows

### Get My Open Issues
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { assignedIssues(filter: { state: { type: { nin: [\"completed\", \"canceled\"] } } }, first: 50) { nodes { identifier title state { name } priority dueDate } } } }"}' | jq '.data.viewer.assignedIssues.nodes'
```

### Get High Priority Issues
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issues(filter: { priority: { lte: 2 } }, first: 20) { nodes { identifier title priority state { name } assignee { name } } } }"}' | jq '.data.issues.nodes'
```

### Get Issues in a Project
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ project(id: \"PROJECT_UUID\") { name issues { nodes { identifier title state { name } } } } }"}'
```

### Search Issues
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(printenv LINEAR_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issueSearch(query: \"search term\", first: 10) { nodes { identifier title description state { name } } } }"}'
```

## Filter Syntax

Linear supports filtering with comparison operators:

| Operator | Example | Description |
|----------|---------|-------------|
| `eq` | `{ state: { name: { eq: "In Progress" } } }` | Equals |
| `neq` | `{ priority: { neq: 0 } }` | Not equals |
| `in` | `{ state: { type: { in: ["started"] } } }` | In list |
| `nin` | `{ state: { type: { nin: ["completed"] } } }` | Not in list |
| `lt`, `lte` | `{ priority: { lte: 2 } }` | Less than (=) |
| `gt`, `gte` | `{ priority: { gte: 1 } }` | Greater than (=) |

## Priority Values

- `0` - No priority
- `1` - Urgent
- `2` - High
- `3` - Medium
- `4` - Low

## State Types

- `backlog` - Not started
- `unstarted` - To do
- `started` - In progress
- `completed` - Done
- `canceled` - Canceled

## Notes

- Linear uses UUIDs for IDs (not the ENG-123 identifiers)
- Use `issueSearch` to find issues by identifier
- GraphQL requires exact field selection - add fields you need
- API key permissions control what you can access
- Get your API key at: https://linear.app/settings/account/security

## Sources

- [Linear GraphQL API](https://developers.linear.app/docs/graphql/working-with-the-graphql-api)
- [Linear Developer Docs](https://linear.app/developers)
