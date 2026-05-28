---
name: ticket-management
description: Use this skill when you want to create an implementation plan for a GitHub issue and then implement that plan step by step.
---

# Ticket Management

## Purpose

This skill allows you to create a detailed implementation plan for a GitHub issue and then execute that plan to implement the changes.

## Workflow

### Step 1: Verify Environment

Check that you have a GitHub remote and are on a clean, up-to-date main/master branch:

```bash
git remote -v
git status
git fetch origin
git rev-parse --abbrev-ref HEAD
git status -uno
```

**STOP if:**
- No remote exists → "This skill requires a GitHub remote. Please add one with `git remote add origin <url>` first."
- Not on main/master → "Please switch to main/master first: `git checkout main`"
- Uncommitted changes → "Please commit or stash your changes first."
- Behind remote → "Please pull latest changes: `git pull`"

### Step 2: Identify the Ticket

User will provide a GitHub issue number (e.g., `#12` or `12`). If not clear, ask which ticket to plan or implement.

### Step 3: Create Implementation Plan

If planning a ticket, read the ticket details:

```bash
gh issue view <number>
```

Understand:
- What needs to be done
- Why it's needed
- Any constraints or notes

Write a plan that:
- Lists concrete steps in order
- Names specific files/modules that will be touched
- Describes what each step accomplishes
- Makes success criteria obvious

**Plan format:**

```markdown
## Implementation Plan

### Steps

1. **<Action>** - <What this accomplishes>
   - Files: `path/to/file.py`
   - <Brief description of the change>

...

### Success Criteria

- [ ] <Observable outcome 1>
- [ ] <Observable outcome 2>
```

### Step 4: Setup Working Branch

**Ask the user:** "Do you want to use a worktree (allows parallel work on other tickets) or branch in place?"

#### Option A: Worktree (recommended for parallel work)

Use the `/worktree create <branch-name>` skill to create an isolated working directory.

#### Option B: Branch in place

Standard approach, switches the current repo to a new branch:

```bash
git checkout main && git pull
git checkout -b <branch-name>
```

### Step 5: Execute the Plan

Work through each step in the plan:

1. Read the step
2. Implement it
3. Verify it works
4. Move to next step

If you hit a blocker:
- Ask the user how to proceed
- Document the issue

### Step 6: Verify Success Criteria

Go through each success criterion and verify it's met:
- Run tests if mentioned
- Check behaviour manually if needed

### Step 7: Create PR

Commit and push your changes:

```bash
git add .
git commit -m "<summary of changes>"
git push -u origin HEAD
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary

<Brief summary of what was done>

Closes #<issue-number>
EOF
)"
```

### Step 8: Request Review

Inform the user about what was implemented and provide the PR URL for review.

### Step 9: Clean Up (if using worktree)

Once the user confirms the PR is merged, clean up the worktree:

1. **Verify PR is merged**
   ```bash
   gh pr view <pr-number> --json state,mergedAt
   ```

2. **Return to main repo**
   ```bash
   cd <main-repo-path>
   git fetch origin
   git checkout main && git pull
   ```

3. **Remove the worktree**
   Use `/worktree clean <branch-name>` to remove the worktree and delete the branch.

## Guidelines

**DO**:
- Follow the plan in order
- Verify each step works before moving on
- Ask if something is unclear or blocked
- Run tests frequently
- Commit logical chunks of work

**DON'T**:
- Implement on main/master branch
- Skip steps without asking
- Leave tests failing

## Checklist

- [ ] Verify GitHub remote exists and on clean, up-to-date main/master
- [ ] Identify which issue to plan or implement
- [ ] Setup working environment (worktree or branch)
- [ ] Read issue and extract plan
- [ ] Execute each step in order
- [ ] Verify all success criteria
- [ ] Create PR with "Closes #X"
- [ ] Request review from user
- [ ] Wait for user to confirm ready for cleanup
- [ ] Clean up worktree (if used)