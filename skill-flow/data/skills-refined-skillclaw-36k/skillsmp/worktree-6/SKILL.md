---
name: worktree
description: "Create isolated git worktrees for ALL coding tasks with issue linking (discovery: implementation-clarity). Evaluate at implementation-clarity when task modifies code files. YOU MUST use for feature development, bug fixes, refactoring - no exceptions. Coding without worktree = no audit trail, no issue linking, no auto-close."
---

# Worktree Skill

Create isolated development environments for coding tasks, with automatic issue linking to deliverable-tracking.

## When to Use

ALL coding tasks. No exceptions.

- Feature development
- Bug fixes
- Refactoring
- Any work that modifies code files

**Invalid skip reasons:**
- "Working on main branch" - NOT a valid reason to skip
- "No parallel conflict risk" - NOT a valid reason to skip
- "Primary work focus" - NOT a valid reason to skip

**Failure mode:** Coding without worktree = no audit trail, no issue linking, no auto-close on PR merge. Every time.

## Workflow

### Step 1: Confirm Issue Context

Check for "Session linked to issue #N" in conversation.
- If linked: Use that issue number
- If not linked: Ask user to provide issue number (required for worktree naming)

### Step 2: Check for Existing Worktree

```bash
git worktree list | grep "issue-{number}"
```

**If worktree exists:**
- ANNOUNCE: "Using existing worktree for issue #{number}"
- Skip to Step 5 (do not create new worktree, do not change labels, do not create PR)

**If worktree does NOT exist:**
- ANNOUNCE: "Creating worktree for issue #{number}"
- Continue to Step 3

### Step 3: Create Worktree (only if not exists)

```bash
git gtr new issue-{number}
```

This creates:
- Sibling directory: `../{repo-name}-issue-{number}/`
- Branch: `issue-{number}`
- Copies `.env*` files automatically

Then move issue to in-progress:

```bash
gh issue edit {number} --repo DaveX2001/deliverable-tracking \
  --add-label "in-progress" --remove-label "to-do"
```

Then post worktree creation comment to issue:

```bash
gh issue comment {number} --repo DaveX2001/deliverable-tracking \
  --body "🌳 **Worktree created**

**Path:** \`$(pwd)/../{repo-name}-worktrees/issue-{number}/\`
**Branch:** \`issue-{number}\`
**Machine:** \`$(hostname)\`"
```

### Step 4: Create Draft PR

After worktree creation, create empty init commit, push, and create draft PR:

```bash
# Create empty init commit (required for PR creation)
git commit --allow-empty -m "chore: init issue-{number} branch"

# Push branch to remote
git push -u origin issue-{number}

# Get issue title for PR title
ISSUE_TITLE=$(gh issue view {number} --repo DaveX2001/deliverable-tracking --json title --jq '.title')

# Create draft PR with issue linking
gh pr create --draft \
  --title "Issue #{number}: $ISSUE_TITLE" \
  --body "**Task:** Fixes DaveX2001/deliverable-tracking#{number}

## How to Test
{Include success criteria from evaluation-clarity phase}"
```

**How to Test content:** Extract the success criteria defined during evaluation-clarity earlier in this session. The user already verified "how we know it worked" before implementation began.

ANNOUNCE: "Draft PR created: {PR_URL}"

### Step 5: Docker Volume Handling (if applicable)

Check if project uses Docker:
```bash
ls docker-compose*.yml 2>/dev/null || ls */docker-compose*.yml 2>/dev/null
```

**If Docker Compose files exist**, ask user via AskUserQuestion:
> "This project uses Docker. Copy existing volumes to worktree deployment?"
> - Options: "Yes, copy volumes" / "No, fresh volumes" / "Skip Docker setup"

**If user chooses "Yes, copy volumes":**
1. Identify the Docker Compose project name from Makefile or compose file
2. List existing volumes: `docker volume ls | grep {project-name}`
3. Guide user to either:
   - Use same project name (shares volumes automatically)
   - Or copy volume data: `docker run --rm -v {src}:/src -v {dst}:/dst alpine cp -a /src/. /dst/`

### Step 6: Announce New Context

REPORT to user:
- Worktree path: `../{repo-name}-issue-{number}/`
- Command to open: `git gtr editor issue-{number}`
- All commits MUST reference: `Refs DaveX2001/deliverable-tracking#{number}`

## PR Auto-Close

The draft PR created in Step 4 includes `Fixes DaveX2001/deliverable-tracking#{number}`. Issue auto-closes when PR merges to default branch.

## Cleanup

After PR merges:

```bash
git gtr rm issue-{number}
```
