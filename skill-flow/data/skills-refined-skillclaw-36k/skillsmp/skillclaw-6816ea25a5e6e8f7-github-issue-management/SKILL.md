---
name: github-issue-management
description: Use this skill when you need to create, retrieve, update, or manage GitHub issues, including adding comments and tracking progress.
---

# GitHub Issue Management

Manage GitHub issues using the `gh` CLI and GitHub API.

## When to Use This Skill

Activate this skill when:
- You want to create a new GitHub issue.
- You need to view or retrieve issue details.
- You want to update an existing issue or its description.
- You need to list issues in a repository.
- You want to manage issue workflows, including closing or reopening issues.
- You need to add comments or labels to issues.
- You want to search for issues.

## Core Commands

### Fetch Issue Details
```bash
gh issue view <number> --json number,title,body,state,labels,comments
```

### Create a New Issue
```bash
gh issue create --title "Issue Title" --body "Issue description..."
```

### Update Description
```bash
gh issue edit <number> --body "$(cat <<'EOF'
Updated description...
EOF
)"
```

### Add Comment
```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Progress Update

**Status:** [analyzing|in_progress|blocked|ready_for_review]

- Point 1
- Point 2
EOF
)"
```

### Close Issue
```bash
gh issue close <number> --reason completed
```

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

## Best Practices

- Always confirm the repository owner and name before creating or modifying issues.
- Use descriptive titles and structured descriptions for issues.
- Add comments to track progress and keep the issue updated.
- Reference related pull requests and issues.
- Avoid creating duplicate issues by searching existing ones first.
- Gather context about the issue type, labels, and milestones before operations.