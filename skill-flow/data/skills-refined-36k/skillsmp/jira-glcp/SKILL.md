---
name: jira-glcp
description: Work with Jira and Atlassian for the GLCP project using Atlassian MCP server tools. Use when (1) querying Jira issues, sprints, or boards, (2) creating or updating GLCP stories, (3) accessing Green Team or Magenta Team boards, (4) working with GLCP project issues, or (5) any Jira/Confluence operations for GLCP.
---

# Jira GLCP

## ⚠️ CRITICAL: Tool Usage

**ALWAYS use Atlassian MCP server FUNCTION TOOLS for all Jira operations.**

These are **function calls**, NOT bash/CLI commands:
- ✅ Invoke them directly as tools (e.g., `Atlassian-searchJiraIssuesUsingJql`)
- ❌ DO NOT run them as bash commands (e.g., `bash: acli jira ...`)
- ❌ DO NOT use `mcp__atlassian` as a CLI command
- ❌ DO NOT fall back to `acli` or other CLI tools

See [examples/tool-invocation-examples.md](examples/tool-invocation-examples.md) for detailed usage examples.

## Project Context

- **Project**: GLCP (GreenLake Cloud Platform)
- **Cloud ID**: b26ad273-0621-4dd6-8915-78cfbe11048e

## Scrum Boards

### Green Team Scrum Board
- **Board ID**: 214
- **Names**: "Green Team Scrum Board", "Green Team"
- **Use for**: Green Team work items and sprints

### GLCP Magenta (Magenta Team)
- **Board ID**: 317  
- **Names**: "GLCP Magenta", "Magenta Team Scrum Board", "Magenta Team"
- **Use for**: Magenta Team work items and sprints

## Common Operations

### Quick Reference

**Get my sprint issues:**
```
Atlassian-searchJiraIssuesUsingJql
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  jql: "assignee = currentUser() AND sprint in openSprints() AND project = GLCP"
```

**Get issue details:**
```
Atlassian-getJiraIssue
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  issueIdOrKey: "GLCP-317168"
```

For more examples, see [examples/tool-invocation-examples.md](examples/tool-invocation-examples.md).

### Board-Specific Queries

When user mentions "Green Team" or "Magenta Team", they are referring to the scrum boards above. Use board filters or JQL to scope queries appropriately.

### Common JQL Patterns

See [references/jql-patterns.md](references/jql-patterns.md) for additional query examples.

## Tool Usage

All available Atlassian MCP tools (invoke as function calls):

### Query Operations
- **Atlassian-searchJiraIssuesUsingJql** - Search issues with JQL
- **Atlassian-search** - General Rovo search across Jira/Confluence
- **Atlassian-getJiraIssue** - Get single issue by key/id

### Create/Update Operations
- **Atlassian-createJiraIssue** - Create new issue (use projectKey: "GLCP")
- **Atlassian-editJiraIssue** - Update existing issue
- **Atlassian-addCommentToJiraIssue** - Add comment to issue
- **Atlassian-transitionJiraIssue** - Change issue status
- **Atlassian-addWorklogToJiraIssue** - Log work time

### Project Operations  
- **Atlassian-getVisibleJiraProjects** - List accessible projects
- **Atlassian-getJiraProjectIssueTypesMetadata** - Get issue types for project
- **Atlassian-getTransitionsForJiraIssue** - Get available status transitions

### Link Operations
- **Atlassian-getJiraIssueRemoteIssueLinks** - Get remote links (Confluence, etc.)

### User Operations
- **Atlassian-lookupJiraAccountId** - Find users by name/email
- **Atlassian-atlassianUserInfo** - Get current user info

**Remember**: Always use `cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"` for GLCP project.
