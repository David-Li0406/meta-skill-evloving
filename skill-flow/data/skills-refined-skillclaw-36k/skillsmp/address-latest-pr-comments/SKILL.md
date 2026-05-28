---
name: address-latest-pr-comments
description: Fetch latest PR review comments, summarize fixed vs open issues, fix open issues, commit and push.
---

# Address Latest PR Comments

Automates the PR review feedback loop for the current branch.

## Workflow

1. **Fetch PR comments** - Get all review comments from the current branch's PR
2. **Summarize status** - Show which issues are fixed vs still open
3. **Fix open issues** - Apply code changes to address remaining feedback
4. **Commit fixes** - Create atomic commits with clear messages
5. **Push changes** - Push to remote branch

## Instructions

### Step 1: Fetch and Display Comments

Run this to get the PR number and fetch comments:

```bash
BRANCH=$(git branch --show-current)
PR_NUMBER=$(gh pr list --head "$BRANCH" --json number --jq '.[0].number')
echo "PR #$PR_NUMBER"
gh api repos/:owner/:repo/pulls/$PR_NUMBER/comments --jq '.[].body'
gh pr view $PR_NUMBER --json reviews --jq '.reviews[].body'
```

### Step 2: Analyze and Summarize

Read through the comments and categorize:
- **Fixed**: Issues already addressed in the codebase
- **Open**: Issues still needing fixes

Present a summary to the user for confirmation before proceeding.

### Step 3: Fix Open Issues

For each open issue:
1. Read the relevant files
2. Apply the fix
3. Verify the build still passes

### Step 4: Commit and Push

Use the `/commit` skill to create atomic commits from the changes:

```
/commit
```

Then push:

```bash
git push
```

## Skills Used

- `/commit` - Creates atomic commits from current branch changes

## Notes

- Always confirm the list of open issues with the user before fixing
- Run build verification after changes when applicable
- Let `/commit` handle grouping and commit message formatting
