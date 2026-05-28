---
name: manage-tickets
description: Commands for viewing, assigning, and updating ticket status on the Guidr GitHub Projects board. Includes workflows for starting, progressing, and completing tickets.
---

# Manage Tickets Skill

Commands for viewing, assigning, and updating ticket status on the Guidr GitHub Projects board.

## View Issues

```bash
# View a specific issue
gh issue view 123

# List all open issues
gh issue list --state open

# List issues assigned to you
gh issue list --assignee @me

# List issues by status (requires project context)
gh issue list --label "status: in-progress"

# List issues with details
gh issue list --json number,title,assignees,projectItems
```

## Assign Yourself to an Issue

```bash
# Assign yourself
gh issue edit 123 --add-assignee @me

# Assign another person
gh issue edit 123 --add-assignee username

# Remove assignee
gh issue edit 123 --remove-assignee @me
```

## Update Issue Status

```bash
# Move to "In Progress"
gh issue edit 123 --add-project "Guidr" --project-field "Status" --project-value "In Progress"

# Move to "Done"
gh issue edit 123 --add-project "Guidr" --project-field "Status" --project-value "Done"

# Move to "Todo"
gh issue edit 123 --add-project "Guidr" --project-field "Status" --project-value "Todo"
```

## Add Comments and Updates

```bash
# Add a comment to track progress
gh issue comment 123 --body "Progress update: completed step 1"

# Add a comment with code example
gh issue comment 123 --body "Fixed in commit abc123. See the changes here: \`\`\`typescript\n...\n\`\`\`"

# Reference issue in commit
# Use "Closes #123" or "Fixes #123" in commit message to auto-link
```

## Link Commits to Issues

```bash
# In commit message (auto-links the issue)
git commit -m "feat: add timer feature

Closes #123"

# Update issue with commit reference
gh issue comment 123 --body "Fixed in commit $(git rev-parse --short HEAD)"
```

## Common Workflows

**Starting work on a ticket**:
```bash
gh issue edit 123 --add-assignee @me
gh issue edit 123 --add-project "Guidr" --project-field "Status" --project-value "In Progress"
```

**Finishing a ticket**:
```bash
# Reference in PR description: "Closes #123"
# After PR merge, status auto-updates to "Done" (if using Closes)
# Or manually update:
gh issue edit 123 --add-project "Guidr" --project-field "Status" --project-value "Done"
```

**Requesting help on a ticket**:
```bash
gh issue comment 123 --body "Blocked: waiting for @someone's input on architecture decision"
```

## Project Board

**Board URL**: https://github.com/users/stevendejongnl/projects/3

**Statuses**: Todo → In Progress → Done

## Tips

- Always assign yourself before starting work
- Keep status updated during development
- Use issue comments to track blockers and progress
- Include issue number in commit messages for automatic linking
- Use "Closes #123" in PR descriptions for automatic status closure
