# Worktree Troubleshooting Guide

Common issues and their solutions when managing worktrees.

## Issue 1: "My worktree isn't working"

### Symptoms
- User can't access the worktree
- Services appear down
- URLs not responding

### Diagnosis Steps
1. Run `/git-simple:list_worktrees_prompt` to check status
2. Look for service status (running/stopped)
3. Check port configuration

### Solutions
- If services are stopped, recreate the worktree
- If ports conflict, use a different port offset
- Check if processes crashed (look at PIDs)

### What to tell the user
> Let me check the status of your worktrees...
> [run /git-simple:list_worktrees_prompt]
> I see the issue - [explain problem and solution]

---

## Issue 2: "I can't create a worktree"

### Symptoms
- Creation command fails
- Error messages about existing worktrees
- Port conflicts

### Common Causes
1. **Worktree already exists** - Branch already has a worktree
2. **Invalid branch name** - Branch doesn't exist in repository
3. **Port already in use** - Another service using the ports

### Solutions
1. Check existing worktrees: `/git-simple:list_worktrees_prompt`
2. Verify branch exists: `git branch -a`
3. Try a different port offset if ports conflict
4. Remove old worktree first if recreating

### What to tell the user
> It looks like [diagnosis]. Let me [solution approach].

---

## Issue 3: "How do I access my worktree?"

### User doesn't know the URLs

### Solution
1. Run `/git-simple:list_worktrees_prompt` to see access URLs
2. Show the Dashboard URL for their specific worktree
3. Explain the port scheme

---

## Issue 6: "Worktree directory exists but not listed"

### Symptoms
- Directory in `trees/` folder
- Not showing in `/git-simple:list_worktrees_prompt`
- Git doesn't recognize it

### Likely Cause
Incomplete removal or manual deletion

### Solutions
1. Check `git worktree list` to see git's view
2. If orphaned, remove directory manually: `rm -rf trees/branch-name`
3. If needed, prune git worktrees: `git worktree prune`

### What to tell the user
> It looks like there's an orphaned worktree. Let me clean it up...

---

## General Debugging Approach

When user reports any issue:

1. **Gather information**
   - Run `/git-simple:list_worktrees_prompt` first
   - Ask which specific worktree
   - Ask what they were trying to do

2. **Resolve**
   - Use appropriate command
   - Verify fix worked
   - Explain what happened

3. **Prevent**
   - Suggest best practices
   - Recommend cleanup of unused worktrees
   - Note any configuration issues

---

## Quick Diagnostic Checklist

When troubleshooting, check:

- ✓ Does worktree directory exist? (`ls trees/`)
- ✓ Is git aware of it? (`git worktree list`)
- ✓ Are services running? (`/git-simple:list_worktrees_prompt`)
- ✓ Are ports available? (check PIDs)
- ✓ Is configuration correct? (check .env, settings.json)
- ✓ Did dependencies install? (check node_modules)
