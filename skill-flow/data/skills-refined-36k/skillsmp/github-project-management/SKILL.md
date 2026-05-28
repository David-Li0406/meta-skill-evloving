---
name: github-project-management
description: Creates and manages GitHub issues and project items. Use when the user asks to create GitHub issues, add items to projects, set project fields, or manage GitHub Project boards. Works with GitHub Projects v2 via MCP tools.
allowed-tools:
  - mcp_github_issue_write
  - mcp_github_issue_read
  - mcp_github_list_issues
  - mcp_github_search_issues
---

# GitHub Project Management

## Overview

This Skill enables creating GitHub issues and managing them in GitHub Projects v2. Use GitHub MCP tools to interact with issues and projects.

## Creating Issues

### Basic Issue Creation

Use `mcp_github_issue_write` with method `create`:

```yaml
method: create
owner: repository owner (username or org)
repo: repository name
title: Issue title
body: Issue description (markdown supported)
labels: [optional array of label names]
assignees: [optional array of usernames]
```

**Example:**

```typescript
mcp_github_issue_write({
  method: "create",
  owner: "yuriolive",
  repo: "vendin",
  title: "[P0] Control Plane API",
  body: "Build the central orchestration API...",
  labels: ["P0", "backend"],
});
```

### Issue Structure Best Practices

**Title format:**

- Use prefixes for categorization: `[P0]`, `[P1]`, `[Epic]`, `[Bug]`
- Be specific and actionable
- Keep under 100 characters

**Body structure:**

```markdown
# [Issue Title]

## Description

Clear description of what needs to be done.

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Requirements

- Requirement 1
- Requirement 2

## Dependencies

- Related issue #123
- Blocks issue #456

## Related Issues

- Part of epic #789
```

## Adding Issues to Projects

After creating an issue, add it to a GitHub Project using `gh` CLI or GitHub API:

**Using gh CLI:**

```bash
gh project item-add <project-number> --owner <owner> --url <issue-url>
```

**Using GitHub API (GraphQL):**

```graphql
mutation {
  addProjectV2ItemById(
    input: {
      projectId: "PVT_..."
      contentId: "I_..." # Issue node ID
    }
  ) {
    item {
      id
    }
  }
}
```

## Setting Project Fields

To set custom fields (like Priority) on project items:

1. Get the project item ID after adding the issue
2. Get the field ID for the custom field
3. Update the field value using GraphQL mutation

**Example workflow:**

```bash
# 1. Add issue to project
gh project item-add 3 --owner yuriolive --url https://github.com/yuriolive/vendin/issues/1

# 2. Get project item ID and field ID (via GraphQL)
# 3. Update priority field
gh api graphql -f query='mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $project,
    itemId: $item,
    fieldId: $field,
    value: { singleSelectOptionId: $value }
  }) { projectV2Item { id } }
}' -f project=PVT_... -f item=PVTI_... -f field=PVTSSF_... -f value=79628723
```

## Priority Mapping

When creating issues from PRD tasks, map priorities:

- **P0 (Must Have)** -> Priority: P0
- **P1 (Production Ready)** -> Priority: P1
- **P2 (Enhanced Features)** -> Priority: P2

Include priority in both the issue label and project field.

## Workflow for Bulk Issue Creation

When creating multiple issues from a PRD or task list:

1. **Create all issues first** using `mcp_github_issue_write`
2. **Collect issue URLs** from responses
3. **Add to project** using `gh project item-add` or GraphQL
4. **Set project fields** (priority, status, etc.) via GraphQL

**Batch processing:**

- Create issues sequentially to avoid rate limits
- Use parallel processing only for adding to projects (safer operation)
- Verify each issue was created before proceeding

## Error Handling

**Issue creation failures:**

- Check repository permissions
- Verify owner/repo names are correct
- Ensure labels exist in repository
- Check for duplicate issues

**Project operations failures:**

- Verify project number and owner
- Check project permissions
- Ensure issue is accessible
- Verify field IDs are correct

## Common Patterns

### Creating Issues from PRD Sections

When converting PRD sections to issues:

1. Extract title from section heading
2. Use section content as issue body
3. Add acceptance criteria from PRD
4. Set priority based on PRD priority level
5. Add appropriate labels (epic, infrastructure, testing, etc.)

### Linking Related Issues

Use issue references in body:

- `Related to #123`
- `Part of epic #456`
- `Blocks #789`
- `Depends on #101`

### Issue Templates

For consistent structure, use this template:

```markdown
# [Title]

## Priority

[P0/P1/P2]

## Description

[What needs to be done]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Technical Requirements

- Requirement 1
- Requirement 2

## Dependencies

- Related issue #X

## Success Criteria

- [How to verify completion]
```

## MCP Tool Reference

**Fully qualified tool names:**

- `github:issue_write` - Create or update issues
- `github:issue_read` - Get issue details
- `github:list_issues` - List repository issues
- `github:search_issues` - Search issues with filters

Always use fully qualified names: `github:issue_write` not just `issue_write`.

## Best Practices

1. **Always verify repository exists** before creating issues
2. **Use descriptive titles** with priority prefixes
3. **Include acceptance criteria** for actionable issues
4. **Link related issues** to show dependencies
5. **Set project fields** after adding to project
6. **Handle errors gracefully** with clear messages
7. **Batch operations** when creating many issues
8. **Verify success** before proceeding to next issue
