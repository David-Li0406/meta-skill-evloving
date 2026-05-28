---
name: clean-branch
description: Clean up merged branches, close issues, and extract compound learning insights
model: claude-sonnet-4-5
context: fork
agent: general-purpose
allowed-tools:
  - Bash(*)
  - Read
  - Edit
  - Write
  - Task
extended-thinking: true
---

# Branch Cleanup & PR Retrospective

You've just merged a PR to dev. Now complete the post-merge cleanup workflow.

## Workflow

### Phase 1: Identify Current State

First, determine what branch you're on and find the associated merged PR and issue:

```bash
# Get current branch name
git branch --show-current

# Find merged PR for this branch
gh pr list --state merged --head $(git branch --show-current) --limit 1

# Get full PR details to find issue number
gh pr view <PR_NUMBER> --json number,title,body
```

### Phase 2: Branch Cleanup

Perform standard cleanup operations:

```bash
# Switch to dev and pull latest
git checkout dev
git pull origin dev

# Delete local feature branch
git branch -d <BRANCH_NAME>

# Delete remote feature branch
git push origin --delete <BRANCH_NAME>
```

### Phase 3: Close Associated Issue

Close the GitHub issue with a summary of what was completed:

```bash
# View issue to understand what was done
gh issue view <ISSUE_NUMBER>

# Close issue with comment summarizing the work
gh issue close <ISSUE_NUMBER> --comment "Completed in PR #<PR_NUMBER>.

<Brief 1-2 sentence summary of what was implemented/fixed>

Changes merged to dev."
```

## Important Notes

- **PR Analysis**: Compound engineering analysis happens automatically via the Stop hook
- **No manual telemetry**: The telemetry system will detect this command and analyze the PR for learning opportunities
- **Summary format**: Keep issue close comments concise but informative

## What Happens Automatically

After you complete the cleanup, the telemetry system will:

1. Analyze the merged PR for patterns (review iterations, fix commits, common themes)
2. Identify compound engineering opportunities (automation, systematization, delegation)
3. Save insights to `meta/telemetry.json` in the `compound_learnings[]` array
4. Log suggestions for preventing similar issues in future PRs

This analysis looks for:
- **Delegation opportunities**: When specialized agents could have helped
- **Automation candidates**: Recurring manual processes
- **Systematization targets**: Knowledge for documentation
- **Prevention patterns**: Issues needing earlier intervention
