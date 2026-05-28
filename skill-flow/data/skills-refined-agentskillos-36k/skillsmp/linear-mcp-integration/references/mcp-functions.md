# Linear MCP Functions Reference

Complete reference for all available Linear MCP server functions.

> **Note:** The MCP server provides authoritative function definitions with complete parameter types, descriptions, and schemas. This reference provides a human-readable summary with examples. For the most up-to-date function signatures, refer to the MCP server's tool definitions.

## Issue Operations

### mcp_Linear_get_issue

Get detailed issue information including title, description, state, assignee, labels, project, and comments.

**Parameters:**
- `id` (string, required): The issue ID or identifier (e.g., "LIN-123" or UUID)
- `includeRelations` (boolean, optional): Whether to include blocking, related, and duplicate relations

**Example:**
```typescript
mcp_Linear_get_issue({
  id: "LIN-123",
  includeRelations: true
})
```

**Returns:** Issue object with fields: `id`, `title`, `description`, `state`, `assignee`, `labels`, `project`, `comments`, `createdAt`, `updatedAt`, and optionally `blocks`, `blockedBy`, `relatedTo`, `duplicateOf` if `includeRelations` is true.

### mcp_Linear_list_issues

List and filter issues with various criteria. Supports pagination and ordering.

**Parameters:**
- `team` (string, optional): Team name or ID to filter by
- `state` (string, optional): State name or ID to filter by
- `assignee` (string, optional): Assignee to filter by (User ID, name, email, or "me")
- `label` (string, optional): Label name or ID to filter by
- `project` (string, optional): Project name or ID to filter by
- `cycle` (string, optional): Cycle name or ID to filter by
- `query` (string, optional): Search query for issue title or description
- `limit` (number, optional): Number of results to return (max 250, default 50)
- `before` (string, optional): Issue ID to end at (for pagination)
- `after` (string, optional): Issue ID to start from (for pagination)
- `orderBy` (string, optional): Order results by "createdAt" or "updatedAt" (default: "updatedAt")
- `includeArchived` (boolean, optional): Whether to include archived issues (default: true)
- `createdAt` (string, optional): ISO-8601 date-time or duration filter (e.g., "-P1D")
- `updatedAt` (string, optional): ISO-8601 date-time or duration filter (e.g., "-P1D")
- `parentId` (string, optional): Parent issue ID to filter by
- `delegate` (string, optional): Agent name or ID to filter by

**Example:**
```typescript
mcp_Linear_list_issues({
  team: "Engineering",
  state: "In Progress",
  assignee: "me",
  limit: 25
})
```

**Returns:** Array of issue objects matching the filter criteria.

### mcp_Linear_update_issue

Update an existing Linear issue.

**Parameters:**
- `id` (string, required): The issue ID to update
- `title` (string, optional): New issue title
- `description` (string, optional): New issue description (Markdown)
- `state` (string, optional): Issue state type, name, or ID
- `assignee` (string, optional): User to assign (User ID, name, email, or "me")
- `labels` (array of strings, optional): Array of label names or IDs
- `project` (string, optional): Project name or ID to add the issue to
- `priority` (number, optional): Priority (0 = No priority, 1 = Urgent, 2 = High, 3 = Normal, 4 = Low)
- `dueDate` (string, optional): Due date in ISO format
- `estimate` (number, optional): Numerical issue estimate value
- `cycle` (string, optional): Cycle name, number, or ID
- `milestone` (string, optional): Milestone name or ID
- `parentId` (string, optional): Parent issue ID (if this is a sub-issue)
- `blocks` (array of strings, optional): Array of issue IDs that this issue blocks (REPLACES existing relations)
- `blockedBy` (array of strings, optional): Array of issue IDs that block this issue (REPLACES existing relations)
- `relatedTo` (array of strings, optional): Array of issue IDs related to this issue (REPLACES existing relations)
- `duplicateOf` (string | null, optional): Issue ID this is a duplicate of (null to remove)
- `links` (array of objects, optional): Array of link objects with `url` and `title` fields

**Example:**
```typescript
mcp_Linear_update_issue({
  id: "LIN-123",
  state: "In Review",
  priority: 2,
  labels: ["bug", "high-priority"]
})
```

**Returns:** Updated issue object.

### mcp_Linear_create_comment

Create a comment on a specific Linear issue.

**Parameters:**
- `issueId` (string, required): The issue ID
- `body` (string, required): The comment content as Markdown
- `parentId` (string, optional): Parent comment ID to reply to

**Example:**
```typescript
mcp_Linear_create_comment({
  issueId: "LIN-123",
  body: "## PR Review Summary\n\n✅ Requirements met: ...\n⚠️ Gaps identified: ..."
})
```

**Returns:** Created comment object with fields: `id`, `body`, `createdAt`, `user`, etc.

## Project Operations

**List/Get Projects:**
- `mcp_Linear_list_projects` - List projects with filters
- `mcp_Linear_get_project` - Get project details
- `mcp_Linear_create_project` - Create new projects
- `mcp_Linear_update_project` - Update projects

## Team Operations

**List/Get Teams:**
- `mcp_Linear_list_teams` - List teams in workspace
- `mcp_Linear_get_team` - Get team details

## User Operations

**List/Get Users:**
- `mcp_Linear_list_users` - List workspace users
- `mcp_Linear_get_user` - Get user details
  - Use `"me"` as query to get current user

## Status and Labels

**Issue Statuses:**
- `mcp_Linear_list_issue_statuses` - List available statuses for a team
- `mcp_Linear_get_issue_status` - Get status details

**Issue Labels:**
- `mcp_Linear_list_issue_labels` - List labels
- `mcp_Linear_create_issue_label` - Create new labels

## Cycles

**List Cycles:**
- `mcp_Linear_list_cycles` - List cycles for a team
  - Types: `current`, `previous`, `next`

## Documents

**Document Operations:**
- `mcp_Linear_list_documents` - List documents
- `mcp_Linear_get_document` - Get document by ID or slug
- `mcp_Linear_create_document` - Create documents
- `mcp_Linear_update_document` - Update documents

## Issue ID Formats

Linear issues can be referenced by:
- **Issue ID**: Full UUID (e.g., `"550e8400-e29b-41d4-a716-446655440000"`)
- **Issue Identifier**: Team key + number (e.g., `"LIN-123"`)
- **Issue Key**: Just the number (e.g., `"123"`) - requires team context

**Best Practice:** Use full issue identifier (`"LIN-123"`) when possible for clarity.

## Filtering and Search

### List Issues with Filters

**By Team:**
```typescript
mcp_Linear_list_issues({
  team: "Engineering",
  state: "In Progress"
})
```

**By Assignee:**
```typescript
mcp_Linear_list_issues({
  assignee: "me", // or user ID/email
  state: "Todo"
})
```

**By Label:**
```typescript
mcp_Linear_list_issues({
  label: "bug",
  state: "Backlog"
})
```

**By Query (Full-text Search):**
```typescript
mcp_Linear_list_issues({
  query: "authentication",
  team: "Engineering"
})
```

## Error Handling

- **Issue not found:** Verify issue ID format and workspace access
- **Authentication errors:** Check MCP server configuration
- **Rate limiting:** Linear API has rate limits; implement retry logic
- **Missing permissions:** Verify workspace access and API token scope

## Best Practices

1. **Cache issue data** when reviewing multiple PRs
2. **Use includeRelations** when checking dependencies
3. **Filter efficiently** using team/state/assignee filters
4. **Handle pagination** for large result sets (use `limit`, `after`)
5. **Extract issue IDs** from PR context before fetching
6. **Update issues** with review findings for traceability

## References

- Linear API Documentation: [developers.linear.app/docs](https://developers.linear.app/docs)
- Linear GraphQL API: [developers.linear.app/docs/graphql](https://developers.linear.app/docs/graphql)
- Linear API Reference: [developers.linear.app/docs/api-reference](https://developers.linear.app/docs/api-reference)
