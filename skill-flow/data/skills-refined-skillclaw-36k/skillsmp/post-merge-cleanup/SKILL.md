---
name: post-merge-cleanup
description: Use when the user asks to clean up, delete, or remove a merged feature branch. Delegates to the specialized branch-cleanup sub-agent to safely delete both local and remote branches after comprehensive validation (merge status, PR status, unpushed commits, uncommitted changes).
allowed-tools: ["Task"]
---

# Post-Merge Cleanup Skill

This skill provides automated cleanup of merged feature branches with comprehensive safety validation.

## When This Skill Activates

Use this skill when you detect the user wants to clean up a merged branch. Common trigger phrases:

- "Clean up after merge"
- "Delete merged branch"
- "Remove feature branch"
- "Post-merge cleanup"
- "Clean up my branch"
- "Delete the feature branch"
- "Cleanup after PR merge"

**Key indicators**:
1. Mentions cleanup, delete, or remove
2. References branch, merge, or PR completion
3. Implies post-merge housekeeping

## What This Skill Does

When activated, immediately delegate to the `branch-cleanup` sub-agent by using the Task tool:

```
Use the Task tool with:
- subagent_type: "branch-cleanup"
- description: "Clean up merged branch"
- prompt: "Clean up the current merged feature branch. Validate it's fully merged, then switch to main, pull latest changes, and delete both local and remote branches."
```

## Why Delegate to Sub-agent?

The `branch-cleanup` sub-agent is specialized for this workflow and will:
1. Detect the current feature branch
2. Run comprehensive safety validations:
   - ✅ Check for uncommitted changes
   - ✅ Verify branch is merged to main
   - ✅ Confirm GitHub PR is merged
   - ✅ Ensure no unpushed commits
3. Switch to main and pull latest
4. Delete local feature branch
5. Delete remote feature branch
6. **STOP if any validation fails** 🛡️

## User Experience

**Before this skill:**
```
User: "Switch to main, update it, then delete my feature branch"
Claude: [Runs commands manually without validation, may delete unmerged work]
```

**With this skill:**
```
User: "Clean up after merge"
Skill: [Auto-activates]
Sub-agent: [Validates thoroughly, then cleans up safely]
Result: ✅ Done automatically with comprehensive safety checks
```

## Safety Features

The branch-cleanup sub-agent includes critical safety checks:
- **Never deletes unmerged branches** - Dual validation (git + GitHub)
- **Prevents data loss** - Checks for unpushed commits and uncommitted changes
- **Protected branch detection** - Never deletes main, master, develop, etc.
- **Clear failure reporting** - Shows exactly which validation failed and why
- **Fail-fast behavior** - Stops at first validation failure

## Supporting Files

This skill directory includes:
- `SKILL.md` (this file) - Skill definition and activation logic
- `README.md` - Detailed workflow documentation and examples

## Configuration

No configuration required. The skill uses:
- Sub-agent: `branch-cleanup` (must exist in ~/.claude/agents/)
- Git commands for local validation
- GitHub CLI (`gh`) for PR status validation
- Remote: `origin` (standard git remote name)

## Troubleshooting

### If the skill doesn't activate:
1. Check that the user's message includes cleanup/delete + branch keywords
2. Ensure the branch-cleanup sub-agent exists
3. Verify you're in a git repository

### If validation fails:
- The sub-agent will report exactly which check failed
- This is CORRECT behavior - it's protecting you from data loss
- Follow the sub-agent's recommendations to resolve the issue

### If GitHub PR validation fails:
- Ensure `gh` CLI is installed and authenticated
- The sub-agent can fall back to git-only validation if needed
- Squash/rebase merges may show as unmerged in git (expected)

## Edge Cases Handled

### Squash/Rebase Merges

GitHub's squash and rebase merges don't preserve commits, so git may not recognize the branch as merged. The sub-agent will:
1. Check GitHub PR status first
2. If PR is merged but git doesn't show it, inform the user
3. Recommend manual deletion with `-D` flag if confident

### Remote Already Deleted

GitHub can auto-delete branches after merge. The sub-agent will:
1. Skip or handle the "unpushed commits" validation gracefully
2. Only delete the local branch
3. Report that remote was already deleted

### Protected Branches

If you're on main, master, develop, etc., the sub-agent will:
1. Immediately refuse to proceed
2. Explain it's a protected branch
3. Suggest switching to a feature branch first
