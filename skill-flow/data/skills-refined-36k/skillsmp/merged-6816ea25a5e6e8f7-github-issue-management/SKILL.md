---
name: github-issue-management
description: Use this skill to create, retrieve, update, and manage GitHub issues, including adding comments and tracking workflows.
---

# GitHub Issue Management

Manage GitHub issues using the `gh` CLI and GitHub MCP tools.

## When to Use This Skill

Activate this skill when:
- You want to create a new GitHub issue.
- You need to view or retrieve issue details.
- You want to update an existing issue or list issues in a repository.
- You need to manage issue workflows, including closing or modifying issues.
- You want to add comments or labels to issues.

## Core Commands

### Creating a New Issue

When creating issues, gather complete context:

**Required Information:**
- `owner`: Repository owner (organization or user)
- `repo`: Repository name
- `title`: Clear, descriptive issue title

**Optional but Recommended:**
- `body`: Detailed description in Markdown format
- `labels`: Array of label names (e.g., ["bug", "enhancement"])
- `assignees`: Array of usernames to assign
- `milestone`: Milestone number (integer)

### Fetching Issue Details

Use the following command to fetch issue details:

```bash
gh issue view <number> --json number,title,body,state,labels,comments
```

### Updating an Issue

When updating issues, only provide changed fields:

```bash
gh issue edit <number> --body "$(cat <<'EOF'
Updated description...
EOF
)"
```

### Adding Comments

To add a comment to an issue, use:

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Progress Update

**Status:** [analyzing|in_progress|blocked|ready_for_review]

- Point 1
- Point 2
EOF
)"
```

### Closing an Issue

To close an issue, use:

```bash
gh issue close <number> --reason completed
```

## Workflow

### 1. Gather Context

Collect information about the current repository and context:
- Identify the repository (owner and repo name)
- Understand the type of issue (bug, feature, task, etc.)
- Gather relevant labels, milestones, and assignees if applicable

### 2. Repository Verification

Before any operation, verify you have the correct repository identifier:
- Confirm repository exists
- Understand repository structure
- Check available labels and milestones

### 3. Execute Operations (Requires Confirmation)

**CRITICAL: Confirm with user before creating or modifying issues**

After gathering all information, present a summary for user approval.

## Comment Templates

**Implementation Analysis:**
```markdown
## Implementation Analysis

**Already implemented:** [list]
**Test coverage:** [list]
**Still needed:** [list]
```

**Completion Summary:**
```markdown
## Implementation Complete

PR: #<number>

**Changes:** [summary]
**Testing:** [how tested]
```

## Important Notes

- **Always verify repository access** - Ensure you have permission to create/modify issues.
- **Use labels consistently** - Follow repository labeling conventions.
- **Be specific in titles** - Prefix with [Bug], [Feature], [Task] for clarity.
- **Include reproduction steps** - Essential for bug reports.
- **Define acceptance criteria** - Clear "definition of done" for features/tasks.
- **Link related issues** - Use "Related to #XX" or "Blocks #XX" in descriptions.
- **Mention users with @username** - For visibility and notifications.
- **Use milestones** - Associate issues with releases when applicable.

## GitHub Issue Best Practices

### Writing Effective Titles
- Be concise but descriptive.
- Include issue type prefix: [Bug], [Feature], [Task], [Docs].
- Mention affected component if applicable.

### Structuring Descriptions
- Use Markdown formatting for readability.
- Include all relevant context upfront.
- Add screenshots or logs when helpful.

### Label Strategy
- Combine type labels (`bug`, `enhancement`) with area labels (`frontend`, `api`).
- Use priority labels when needed (`priority-high`, `priority-low`).

### Assignment and Workflow
- Assign issues to specific team members.
- Use milestones for release planning.
- Update issue status as work progresses.
- Close issues with reference to fixing PR: "Fixes #XX".

## Common Labels

Use these standard labels when applicable:

| Label | Use For |
|-------|---------|
| `bug` | Something isn't working |
| `enhancement` | New feature or improvement |
| `documentation` | Documentation updates |
| `good first issue` | Good for newcomers |
| `help wanted` | Extra attention needed |
| `question` | Further information requested |
| `wontfix` | Will not be addressed |
| `duplicate` | Already exists |
| `invalid` | Not a valid issue |