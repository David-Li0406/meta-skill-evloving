---
name: github-issues
description: Use this skill when you want to create, update, or manage GitHub issues, including bug reports, feature requests, and task issues.
---

# GitHub Issues

Manage GitHub issues using the `@modelcontextprotocol/server-github` MCP server.

## Available MCP Tools

| Tool                             | Purpose                |
| -------------------------------- | ---------------------- |
| `mcp__github__create_issue`      | Create new issues      |
| `mcp__github__update_issue`      | Update existing issues |
| `mcp__github__get_issue`         | Fetch issue details    |
| `mcp__github__search_issues`     | Search issues          |
| `mcp__github__add_issue_comment` | Add comments           |
| `mcp__github__list_issues`       | List repository issues |

## Workflow

1. **Determine action**: Create, update, or query?
2. **Gather context**: Get repository info, existing labels, and milestones if needed.
3. **Structure content**: Use appropriate template based on the issue type.
4. **Execute**: Call the appropriate MCP tool.
5. **Confirm**: Report the issue URL to the user.

## Creating Issues

### Required Parameters

```yaml
owner: repository owner (org or user)
repo: repository name
title: clear, actionable title
body: structured markdown content
```

### Optional Parameters

```yaml
labels: ["bug", "enhancement", "documentation", ...]
assignees: ["username1", "username2"]
milestone: milestone number (integer)
```

### Title Guidelines

- Start with type prefix when useful: `[Bug]`, `[Feature]`, `[Docs]`
- Be specific and actionable
- Keep under 72 characters
- Examples:
  - `[Bug] Login fails with SSO enabled`
  - `[Feature] Add dark mode support`
  - `Add unit tests for auth module`

### Body Structure

Always use the templates based on issue type:

| User Request                    | Template        |
| ------------------------------- | --------------- |
| Bug, error, broken, not working | Bug Report      |
| Feature, enhancement, add, new  | Feature Request |
| Task, chore, refactor, update   | Task            |

## Updating Issues

Use `mcp__github__update_issue` with:

```yaml
owner: repository owner (org or user)
repo: repository name
issue_number: required
title: optional
body: optional
state: optional (open/closed)
labels: optional
assignees: optional
milestone: optional
```