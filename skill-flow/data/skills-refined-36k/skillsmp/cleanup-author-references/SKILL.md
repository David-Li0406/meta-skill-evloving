---
name: Cleanup Author References
description: Remove all Claude/AI authorship references from git history including commit messages, co-authored-by lines, and generated-with markers. Uses git-filter-repo for safe history rewriting.
version: 1.0.0
---

# Cleanup Author References Skill

## Overview

This skill removes AI authorship references from git repositories, cleaning up:
- "🤖 Generated with [Claude Code](https://claude.com/claude-code)" lines
- "Co-Authored-By: Claude..." lines (case-insensitive)
- "Co-authored-by: Claude..." lines
- Other mentions of Claude in commit messages
- Branch names containing "claude" references

## Prerequisites

**git-filter-repo is required** - it's the modern, safe way to rewrite git history.

```bash
# Install via Homebrew (macOS)
brew install git-filter-repo

# Or via pip
pip install git-filter-repo
```

## Pre-Cleanup Checklist

Before running cleanup:

1. **Backup your repository** - history rewriting is destructive
2. **Ensure working directory is clean** - no uncommitted changes
3. **Coordinate with team** - force pushes will be required
4. **Note current remote** - you'll need to re-add it after cleanup

```bash
# Check status
git status

# Store remote URL for later
git remote get-url origin

# Create a backup branch
git branch backup-before-cleanup
```

## Cleanup Commands

### Step 1: Preview Affected Commits

First, see which commits will be modified:

```bash
# Find commits mentioning claude (case-insensitive)
git log --all --oneline --grep="claude" -i

# Count affected commits
git log --all --oneline --grep="claude" -i | wc -l

# Find Co-Authored-By mentions
git log --all --oneline --grep="Co-Authored-By.*Claude" -i

# Find Generated with Claude Code
git log --all --oneline --grep="Generated with.*Claude" -i
```

### Step 2: Run git-filter-repo

**IMPORTANT**: git-filter-repo requires a fresh clone OR the `--force` flag. It also removes the origin remote as a safety measure.

```bash
# Store remote URL before cleanup
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")

# Run the cleanup with message callback
git-filter-repo --message-callback '
import re
msg = message.decode("utf-8", errors="replace")

# Patterns to remove
patterns = [
    # Generated with Claude Code (with and without emoji/link)
    r"\n*\s*🤖\s*Generated with \[Claude Code\]\(https://claude\.com/claude-code\)\s*\n*",
    r"\n*\s*🤖\s*Generated with Claude Code\s*\n*",
    r"\n*\s*Generated with \[Claude Code\]\(https://claude\.com/claude-code\)\s*\n*",
    r"\n*\s*Generated with Claude Code\s*\n*",
    # Co-Authored-By variations
    r"\n*\s*Co-Authored-By:\s*Claude[^\n]*\n*",
    r"\n*\s*Co-authored-by:\s*Claude[^\n]*\n*",
    r"\n*\s*co-authored-by:\s*Claude[^\n]*\n*",
    # Anthropic email variations
    r"\n*\s*Co-Authored-By:[^\n]*@anthropic\.com[^\n]*\n*",
    r"\n*\s*Co-authored-by:[^\n]*@anthropic\.com[^\n]*\n*",
]

for pattern in patterns:
    msg = re.sub(pattern, "\n", msg, flags=re.IGNORECASE)

# Clean up excessive newlines
msg = msg.rstrip() + "\n"
msg = re.sub(r"\n{3,}", "\n\n", msg)

return msg.encode("utf-8")
' --force

# Re-add the remote if it existed
if [ -n "$REMOTE_URL" ]; then
    git remote add origin "$REMOTE_URL"
fi
```

### Step 3: Verify Cleanup

```bash
# Check for any remaining Claude references
git log --all --oneline --grep="claude" -i

# Should return empty or 0
git log --all --oneline --grep="claude" -i | wc -l

# Check for remaining Co-Authored-By
git log --all --grep="Co-Authored-By.*Claude" -i
```

### Step 4: Force Push (if needed)

**WARNING**: This rewrites remote history. Coordinate with your team.

```bash
# Force push all branches
git push origin --force --all

# Force push tags
git push origin --force --tags
```

## Branch Name Cleanup

If you have branches with "claude" in the name:

```bash
# List branches containing "claude"
git branch -a | grep -i claude

# Rename a local branch
git branch -m old-claude-branch new-branch-name

# Delete remote branch and push renamed one
git push origin :old-claude-branch
git push origin -u new-branch-name
```

## Batch Cleanup Script

For cleaning multiple repositories at once, create this script:

```bash
#!/bin/bash
# cleanup_repos.sh - Clean Claude references from multiple repos

REPOS_DIR="${1:-.}"
cd "$REPOS_DIR"

for dir in */; do
    if [ -d "$dir/.git" ]; then
        echo "=== Processing $dir ==="
        cd "$dir"

        # Check for Claude references
        COUNT=$(git log --all --oneline --grep="claude" -i 2>/dev/null | wc -l | tr -d ' ')

        if [ "$COUNT" -gt 0 ]; then
            echo "Found $COUNT commits with Claude references"

            # Store remote
            REMOTE=$(git remote get-url origin 2>/dev/null || echo "")

            # Run cleanup
            git-filter-repo --message-callback '
import re
msg = message.decode("utf-8", errors="replace")
patterns = [
    r"\n*\s*🤖\s*Generated with \[Claude Code\]\(https://claude\.com/claude-code\)\s*\n*",
    r"\n*\s*🤖\s*Generated with Claude Code\s*\n*",
    r"\n*\s*Co-Authored-By:\s*Claude[^\n]*\n*",
    r"\n*\s*Co-authored-by:\s*Claude[^\n]*\n*",
]
for pattern in patterns:
    msg = re.sub(pattern, "\n", msg, flags=re.IGNORECASE)
msg = msg.rstrip() + "\n"
msg = re.sub(r"\n{3,}", "\n\n", msg)
return msg.encode("utf-8")
' --force

            # Restore remote
            if [ -n "$REMOTE" ]; then
                git remote add origin "$REMOTE"
            fi

            echo "Cleaned $dir"
        else
            echo "No Claude references found in $dir"
        fi

        cd ..
    fi
done
```

## Dry Run / Preview Mode

To preview what would be changed without modifying anything:

```bash
# Clone to a temp directory for testing
git clone --mirror . /tmp/test-cleanup
cd /tmp/test-cleanup

# Run cleanup on the test clone
git-filter-repo --message-callback '...' --force

# Compare before/after
git log --all --oneline | head -20

# Clean up test directory
rm -rf /tmp/test-cleanup
```

## Troubleshooting

### "refusing to run on a repo that already has history"

Solution: Use `--force` flag or start with a fresh clone.

### "git-filter-repo: command not found"

Solution: Install git-filter-repo:
```bash
brew install git-filter-repo
# or
pip install git-filter-repo
```

### Remote was removed

This is expected behavior. Re-add it:
```bash
git remote add origin <your-remote-url>
```

### Team members have old history

After force pushing, team members need to:
```bash
git fetch origin
git reset --hard origin/main  # or their branch
```

## Safety Notes

- Always backup before rewriting history
- Coordinate force pushes with team members
- This modifies commit hashes - any external references (issues, PRs) may break
- Consider using `git reflog` as emergency recovery within 90 days
