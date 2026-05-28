---
name: github-issue-management
description: Use this skill to manage GitHub Issues, including creating, listing, and closing issues, as well as generating implementation tasks from issues.
---

# Skill body

## Overview

This skill allows you to manage GitHub Issues effectively, including creating new issues, listing existing ones, closing issues, and generating implementation tasks from issue content.

## Important Constraints

- This skill is restricted to the `sh1ma/blog` repository only. Do not specify other repositories using the `--repo` flag.

## Available Labels

When creating an issue, you must assign one or more of the following labels:

| Label          | Purpose                         |
| --------------- | ------------------------------ |
| `feature`       | Related to feature development  |
| `bug`           | Related to bugs                 |
| `refactoring`   | Related to refactoring          |
| `documentation` | Related to documentation        |
| `chore`         | Miscellaneous changes           |
| `AI`            | Related to AI                   |
| `test`          | Related to tests                |

## Creating an Issue (Recommended Flow)

### Step 1: Select Appropriate Labels

Choose one or more labels based on the issue content from the list above.

### Step 2: Create Issue Using Template

**Important**: Always use the `.github/ISSUE_TEMPLATE/default.md` template.

```bash
gh issue create \
  --title "Title" \
  --label "Label" \
  --assignee sh1ma \
  --template "default.md"
```

The template includes the following sections:
- **What to do**: What this issue will accomplish
- **Purpose**: Why this issue is being implemented
- **Policy**: How it will be achieved
- **Tasks**: Checklist of tasks to be performed

### Creating an Issue with Multiple Labels

```bash
gh issue create --title "Title" --label "feature" --label "AI" --assignee sh1ma --template "default.md"
```

## Listing Issues

```bash
gh issue list                     # List open issues
gh issue list --state all         # List all issues
gh issue list --state closed      # List closed issues
gh issue list --author @me        # List issues created by me
gh issue list --assignee @me      # List issues assigned to me
gh issue list --label "bug"       # Filter by label
gh issue list --milestone "v1.0"  # Filter by milestone
```

## Closing and Reopening Issues

```bash
gh issue close 123                # Close issue #123
gh issue close 123 -c "Reason"    # Close with a comment
gh issue reopen 123                # Reopen issue #123
```

## Generating Implementation Tasks from Issues

To generate a task list from a GitHub Issue, specify the issue number:

```
/issue-to-task <Issue number>
```

### Execution Process

1. **Retrieve Issue Information**:
   ```bash
   gh issue view <Issue number> --json title,body,labels,assignees
   ```

2. **Analyze Issue**:
   - Determine the type of issue (Feature, Bug, etc.) based on the title and labels.

3. **Decompose Tasks**:
   - Extract tasks based on the issue type and create a checklist.

4. **Identify Affected Files**:
   - List files that will be impacted based on the issue type.

5. **Extract Test Items**:
   - Create a list of test cases based on the tasks identified.

### Output Format

```
📋 Implementation task generation complete

Issue: #<number> - <title>
Type: <Feature/Bug/Refactor/etc>
Affected Areas: <Frontend/Backend/etc>
Tasks:
- [ ] Task 1
- [ ] Task 2
```