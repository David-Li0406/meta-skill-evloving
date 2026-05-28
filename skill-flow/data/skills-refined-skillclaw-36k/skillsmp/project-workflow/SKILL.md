---
name: project-workflow
description: Quick reference for the Guidr GitHub Projects workflow. Learn status transitions (Todo → In Progress → Done), linking commits/PRs to tickets, and best practices for tracking work through development.
---

# Project Workflow Skill

Quick reference for the Guidr GitHub Projects workflow.

## The Workflow

**Project Board**: https://github.com/users/stevendejongnl/projects/3

**Statuses**: Todo → In Progress → Done

## Key Steps

### 1️⃣ Before Starting Work

When you're ready to work on a ticket:

```bash
# Assign yourself to the issue
gh issue edit 123 --add-assignee @me

# Move it to "In Progress"
gh issue edit 123 --add-project "Guidr" --project-field "Status" --project-value "In Progress"
```

### 2️⃣ During Development

Keep the ticket informed about progress:

```bash
# Add progress comment
gh issue comment 123 --body "Started implementation, working on the service layer"

# Add blocker comment if needed
gh issue comment 123 --body "Blocked: need clarification on API contract"

# Reference the issue in commits
git commit -m "feat: add timer feature

Implements pause/resume functionality for guide sessions.
Closes #123"
```

### 3️⃣ After Completing Work

When work is done and merged:

```bash
# Option A: Use "Closes #123" in PR - auto-closes issue and moves to Done
# (Do this in PR description)

# Option B: Manually move to Done
gh issue edit 123 --add-project "Guidr" --project-field "Status" --project-value "Done"
```

## Common Commands Cheat Sheet

```bash
# View issue
gh issue view 123

# Assign yourself
gh issue edit 123 --add-assignee @me

# Update status to In Progress
gh issue edit 123 --add-project "Guidr" --project-field "Status" --project-value "In Progress"

# Update status to Done
gh issue edit 123 --add-project "Guidr" --project-field "Status" --project-value "Done"

# Add comment
gh issue comment 123 --body "Your message here"

# List your open issues
gh issue list --assignee @me --state open
```

## Status Transitions

```
Todo
  ↓
  (assign yourself + start work)
  ↓
In Progress
  ↓
  (develop + test)
  ↓
Done
  (after PR merge with "Closes #123")
```

## For Claude Code

When working on a Guidr ticket:

1. **Read the issue** to understand requirements
   ```bash
   gh issue view 123
   ```

2. **Assign yourself** immediately
   ```bash
   gh issue edit 123 --add-assignee @me
   ```

3. **Mark as In Progress** before implementation
   ```bash
   gh issue edit 123 --add-project "Guidr" --project-field "Status" --project-value "In Progress"
   ```

4. **Work on the feature/fix**
   - Write tests (TDD if possible)
   - Implement solution
   - Verify with `npm test`, `npm run lint`, `npm run typecheck`

5. **Commit with issue reference**
   ```bash
   git commit -m "feat: description

   Closes #123"
   ```

6. **Create PR** with "Closes #123" in description
   - This auto-links and will auto-close the issue when merged

7. **After merge**, status auto-updates to Done
   - Or manually: `gh issue edit 123 --add-project "Guidr" --project-field "Status" --project-value "Done"`

## Linking Issues to PRs

```bash
# In PR description, use "Closes #123"
# This automatically:
# - Links the PR to the issue
# - Closes the issue when PR is merged
# - Moves status to Done
```

## Common Scenarios

**Picking up work**:
```bash
gh issue view 123              # Read requirements
gh issue edit 123 --add-assignee @me
gh issue edit 123 --add-project "Guidr" --project-field "Status" --project-value "In Progress"
```

**Hit a blocker**:
```bash
gh issue comment 123 --body "Blocked: waiting for @someone's input on the API design"
```

**Ready for review**:
```bash
# Create PR with: "Closes #123" in the description
# This links the PR to the ticket
```

**Completed work**:
```bash
# Merge PR with "Closes #123" in description
# Issue auto-closes and status updates to Done
```

## Tips & Best Practices

- ✅ **Always** assign yourself before starting work
- ✅ **Always** include issue number in commit messages (`#123`)
- ✅ **Always** use "Closes #123" in PR description for auto-closure
- ✅ Add comments for blockers or progress updates
- ✅ Keep status current during development
- ❌ Don't leave issues assigned without status
- ❌ Don't forget to update status when moving between phases

## Why This Matters

- **Visibility**: Team can see what's being worked on
- **Traceability**: Commits are linked to issues
- **Automation**: "Closes #123" auto-closes issues on merge
- **History**: Project board shows complete workflow
- **Coordination**: Others know what's in progress and planned

## Need Help?

- Use `/manage-tickets` skill for issue operations
- Use `/create-issue` skill to create new issues
- Use `/board-overview` skill to check project status
- Check CONTRIBUTING.md for detailed workflow documentation
