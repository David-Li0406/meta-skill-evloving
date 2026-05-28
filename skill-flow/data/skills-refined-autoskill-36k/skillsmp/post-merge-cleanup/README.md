# Post-Merge Cleanup Skill

Automated, safe cleanup of merged feature branches with comprehensive validation.

## Overview

This skill streamlines the post-merge cleanup process by:
1. Automatically detecting when you want to clean up a merged branch
2. Running comprehensive safety validations
3. Only deleting branches if ALL safety checks pass
4. Cleaning up both local and remote branches
5. Providing clear reporting of actions taken

## Quick Start

Simply say:
```
"Clean up after merge"
```

The skill auto-activates and handles everything safely.

## The Problem This Solves

### Before (Manual Process)

```
You: Create PR, get it merged
You: Manually switch to main
You: Manually pull updates
You: Try to delete branch
Git: Error! Branch not fully merged (even though it is)
You: Force delete with -D (risky!)
You: Forget to delete remote branch
Result: Cluttered repository, potential data loss
```

### After (With This Skill)

```
You: Create PR, get it merged
You: "Clean up after merge"
Skill: ✅ Validates everything, deletes safely, switches to main, done!
Result: Clean repository, zero risk
```

## How It Works

### Architecture

```
User Request
    ↓
[post-merge-cleanup Skill] ← Auto-activates
    ↓
[branch-cleanup Sub-agent] ← Validates and executes
    ↓
Git + GitHub CLI → Comprehensive safety checks
```

### Safety Validation Flow

```
1. Check uncommitted changes
   ↓
2. Verify branch merged to main (git)
   ↓
3. Confirm PR merged (GitHub)
   ↓
4. Check for unpushed commits
   ↓
ALL PASS? → Proceed with cleanup
ANY FAIL? → STOP and report
```

### Cleanup Steps (Only if ALL validations pass)

```
1. Switch to main
2. Pull latest changes
3. Delete local branch (with -d, safe delete)
4. Delete remote branch
5. Report success
```

## Components

### 1. Skill (This Directory)
**File**: `~/.claude/skills/post-merge-cleanup/SKILL.md`

**Purpose**: Auto-activation and delegation

**Trigger Phrases**:
- "Clean up after merge"
- "Delete merged branch"
- "Remove feature branch"
- "Post-merge cleanup"

### 2. Sub-agent
**File**: `~/.claude/agents/branch-cleanup.md`

**Purpose**: Validation and execution logic

**Capabilities**:
- Full tool access
- Git operations
- GitHub API via `gh` CLI
- Comprehensive error handling

## Safety Validations

### Validation 1: Uncommitted Changes

**Check**: `git status --porcelain`

**Purpose**: Prevent losing uncommitted work

**Fails if**: Working directory has any uncommitted changes

**Example failure**:
```
❌ Working directory has uncommitted changes:
M  src/User.cs
?? temp.txt

Please commit or stash changes before cleanup.
```

### Validation 2: Branch Merged to Main

**Check**: `git branch --merged main`

**Purpose**: Ensure branch is fully integrated

**Fails if**: Branch doesn't appear in merged branches list

**Example failure**:
```
❌ Branch feat/new-api is NOT fully merged to main

This branch contains commits that haven't been merged.
Use 'git log main..HEAD' to see 3 unmerged commits.

WILL NOT delete this branch for safety.
```

### Validation 3: GitHub PR Merged

**Check**: `gh pr view <PR> --json state,mergedAt`

**Purpose**: Verify PR was actually merged on GitHub

**Fails if**:
- No PR found for the branch
- PR is still open
- PR was closed without merging

**Example failure**:
```
❌ No merged GitHub PR found for branch feat/experimental

Possible reasons:
- PR was not created
- PR is still open
- PR was closed without merging

WILL NOT delete this branch for safety.
```

### Validation 4: No Unpushed Commits

**Check**: `git log origin/<branch>..HEAD`

**Purpose**: Prevent losing commits not yet pushed

**Fails if**: Local branch has commits not on remote

**Example failure**:
```
❌ Branch has unpushed commits:
a1b2c3d Fix typo
e4f5g6h Add tests

Push these commits first or they will be lost:
git push origin feat/my-feature

WILL NOT delete this branch for safety.
```

## Example Workflows

### Scenario 1: Successful Cleanup

```bash
# Your feature branch PR was merged on GitHub
git branch
# * feat/user-authentication
#   main

# You're ready to clean up
```

```
You: "Clean up after merge"

Skill Output:
🔍 Running safety checks for branch: feat/user-authentication

1. Checking working directory...
   ✅ No uncommitted changes

2. Verifying branch is merged to main...
   ✅ Branch is fully merged

3. Checking GitHub PR status...
   ✅ PR #456 merged on 2025-10-23T14:20:00Z

4. Checking for unpushed commits...
   ✅ All commits pushed to remote

All safety checks passed! Proceeding with cleanup...

🔄 Switched to main branch
📥 Pulled latest changes from origin/main
🗑️  Deleted local branch: feat/user-authentication
🗑️  Deleted remote branch: origin/feat/user-authentication

✅ Branch cleanup complete!

Summary:
- Switched to: main
- Deleted local: feat/user-authentication
- Deleted remote: origin/feat/user-authentication
```

```bash
# Verify cleanup
git branch
# * main

git branch -r | grep user-authentication
# (no results - remote deleted)
```

### Scenario 2: Prevented Data Loss (Uncommitted Changes)

```bash
# You have uncommitted changes
git status
# M  src/important-file.cs
```

```
You: "Clean up after merge"

Skill Output:
🔍 Running safety checks for branch: feat/new-feature

1. Checking working directory...
   ❌ Working directory has uncommitted changes:
   M  src/important-file.cs

🛑 Branch cleanup STOPPED due to failed validation

Failed check: Uncommitted changes
Reason: Working directory has 1 uncommitted file

Please commit or stash changes before cleanup:
  git add .
  git commit -m "Your message"

No branches were deleted. Your repository is unchanged.
```

**Result**: Your uncommitted work is safe! ✅

### Scenario 3: Prevented Accidental Deletion (Unmerged Branch)

```bash
# You forgot to merge your PR
gh pr view
# state: OPEN
```

```
You: "Clean up after merge"

Skill Output:
🔍 Running safety checks for branch: feat/experimental

1. Checking working directory...
   ✅ No uncommitted changes

2. Verifying branch is merged to main...
   ❌ Branch is NOT fully merged to main

🛑 Branch cleanup STOPPED due to failed validation

Failed check: Branch merge verification
Reason: Branch feat/experimental contains unmerged commits

Use 'git log main..HEAD' to see 5 unmerged commits.

No branches were deleted. Your repository is unchanged.
```

**Result**: Your unmerged work is safe! ✅

### Scenario 4: Protected Branch Prevention

```bash
# You're on main branch
git branch
# * main
```

```
You: "Clean up after merge"

Skill Output:
❌ Cannot clean up protected branch: main

This workflow is only for feature branches.
Protected branches: main, master, develop, production, staging, release

If you want to clean up a feature branch, switch to it first:
  git checkout feat/your-branch
  Then try cleanup again.
```

**Result**: Main branch is protected! ✅

## Edge Cases & Special Situations

### Squash/Rebase Merges

GitHub's squash and rebase merges don't preserve original commits, so git may not recognize the branch as merged.

**What happens**:
```
🔍 Running safety checks for branch: feat/squashed-feature

1. Checking working directory...
   ✅ No uncommitted changes

2. Verifying branch is merged to main...
   ❌ Branch not shown as merged in git

3. Checking GitHub PR status...
   ✅ PR #789 merged on 2025-10-23T15:00:00Z (squash merge)

⚠️  GitHub PR #789 is merged, but git doesn't show branch as merged
This happens with squash or rebase merges.

Recommendation: The branch is safe to delete manually:
  git checkout main
  git pull origin main
  git branch -D feat/squashed-feature
  git push origin --delete feat/squashed-feature

I cannot auto-delete due to git merge check failing.
```

**Solution**: Follow the recommendation to delete manually with `-D` flag.

### Remote Branch Already Deleted

GitHub can auto-delete branches after PR merge.

**What happens**:
```
🔍 Running safety checks for branch: feat/auto-deleted

1. Checking working directory...
   ✅ No uncommitted changes

2. Verifying branch is merged to main...
   ✅ Branch is fully merged

3. Checking GitHub PR status...
   ✅ PR #234 merged on 2025-10-23T12:00:00Z

4. Checking for unpushed commits...
   ℹ️  Remote branch already deleted (skipping check)

All safety checks passed! Proceeding with cleanup...

🔄 Switched to main branch
📥 Pulled latest changes from origin/main
🗑️  Deleted local branch: feat/auto-deleted
ℹ️  Remote branch already deleted on origin

✅ Branch cleanup complete!
```

**Result**: Only local branch is deleted (as expected).

### GitHub CLI Not Available

If `gh` CLI is not installed or authenticated:

```
🔍 Running safety checks for branch: feat/my-feature

1. Checking working directory...
   ✅ No uncommitted changes

2. Verifying branch is merged to main...
   ✅ Branch is fully merged

3. Checking GitHub PR status...
   ⚠️  GitHub CLI (gh) not found or not authenticated
   Skipping GitHub PR validation

   Install with: brew install gh
   Authenticate: gh auth login

4. Checking for unpushed commits...
   ✅ All commits pushed to remote

⚠️  Proceeding without GitHub PR validation
Only using git merge status checks.

All safety checks passed! Proceeding with cleanup...
```

**Result**: Falls back to git-only validation (still safe).

## Configuration Requirements

### Prerequisites

1. **Git**: Obviously required (you're in a git repo)

2. **GitHub CLI (optional but recommended)**: For PR status validation
   ```bash
   brew install gh
   gh auth login
   ```

3. **Remote**: Must have `origin` remote configured
   ```bash
   git remote -v
   # origin  https://github.com/user/repo.git (fetch)
   # origin  https://github.com/user/repo.git (push)
   ```

4. **Main branch**: Default is `main`, but works with `master` too

### Optional Configuration

None! The skill works out of the box.

## Protected Branches

The sub-agent will NEVER delete these branches:
- `main`
- `master`
- `develop` / `development`
- `production` / `prod`
- `staging` / `stage`
- `release`
- `hotfix` (exact match only)

If you're on one of these, the sub-agent immediately refuses.

## Troubleshooting

### Skill Doesn't Activate

**Problem**: You say "delete my branch" but nothing happens

**Solutions**:
- Use clearer trigger phrases: "clean up after merge"
- Include the word "merge" or "merged"
- Ensure you're in a git repository

### Validation Always Fails

**Problem**: "Branch not fully merged" even though PR is merged

**Likely Cause**: Squash or rebase merge on GitHub

**Solution**:
1. Check the sub-agent's output for the GitHub PR status
2. If PR shows as merged, it's safe to delete manually
3. Use the commands recommended by the sub-agent

### Can't Delete Remote Branch

**Problem**: Error deleting `origin/<branch>`

**Possible Causes**:
1. Remote already deleted (this is fine, ignore the error)
2. No permissions (check GitHub repo access)
3. Branch protected on GitHub (shouldn't be for feature branches)

**Solution**: Check GitHub repo settings or permissions

### Wrong Main Branch

**Problem**: Your repo uses `master` instead of `main`

**Solution**: The sub-agent detects the default branch automatically. If it doesn't work, you may need to manually check the sub-agent logic, but it should handle both.

## Tips and Best Practices

### 1. Clean Up Immediately After Merge

```
PR merged → You: "Clean up after merge" → Done!
```

Don't wait - clean up right away while context is fresh.

### 2. Trust the Validations

If a validation fails, there's a good reason. Don't try to force it.

### 3. Squash Merges Require Manual Cleanup

If your team uses squash merges:
1. Let the skill validate (it will detect the squash)
2. Follow the manual cleanup recommendation
3. Or adjust your GitHub settings to preserve commits

### 4. Enable GitHub Auto-Delete

Configure GitHub to auto-delete branches after merge:
- Repo Settings → General → "Automatically delete head branches"

Then the skill only needs to clean up local branches.

### 5. Review the Summary

Always read the final summary to confirm what was deleted.

## File Locations

```
~/.claude/
├── agents/
│   └── branch-cleanup.md            # Sub-agent definition
└── skills/
    └── post-merge-cleanup/
        ├── SKILL.md                  # Skill activation logic
        └── README.md                 # This file

~/.claude/CLAUDE.md                   # Global config (documents workflow)
```

## Advanced Usage

### Manual Invocation

If the skill doesn't auto-activate, you can invoke the sub-agent directly:

```
You: "Run the branch-cleanup sub-agent to clean up my current branch"
```

### Specify Different Main Branch

```
You: "Clean up after merge, but compare against develop instead of main"
```

The sub-agent should adapt, but this may require mentioning it explicitly.

### Review Before Deletion

```
You: "Check if my branch is safe to delete, but don't delete it yet"
```

The sub-agent can run validations without executing the deletion.

## Integration with Other Workflows

This skill complements:
- **CodeRabbit workflow**: Fix issues → Merge → Clean up
- **Feature development**: Create branch → Develop → PR → Merge → Clean up
- **Hotfix workflow**: Create hotfix → Merge → Clean up immediately

## Safety Philosophy

This skill follows the principle:

**"Better to refuse than to lose data"**

Every validation serves a purpose:
- Uncommitted changes → Protect active work
- Merge status → Prevent losing unmerged code
- PR status → Verify actual merge happened
- Unpushed commits → Prevent losing local-only work

If ANY validation fails, the entire cleanup is cancelled. No exceptions.

## Contributing

To enhance this workflow:

1. **Sub-agent logic**: Edit `~/.claude/agents/branch-cleanup.md`
2. **Activation triggers**: Edit `~/.claude/skills/post-merge-cleanup/SKILL.md`
3. **Documentation**: Edit this README

All changes are local and take effect immediately.

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the sub-agent's validation output
3. Test git/GitHub CLI commands manually
4. Verify you're not on a protected branch

---

**Happy branch cleaning! 🧹✨**
