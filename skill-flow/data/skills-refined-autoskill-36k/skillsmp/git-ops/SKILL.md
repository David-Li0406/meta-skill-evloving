---
name: git-ops
description: Get information about the state of a git repo, get diffs, make commits, make PRs, etc.. Use this skill when the user needs to accomplish git tasks.
user-invocable: true
allowed-tools:
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(ls:*)
  - Bash(pwd)
---

# Git & GitHub Workflow

## User Confirmation Required

**Use `AskUserQuestion` before these potentially destructive operations**:
- Creating commits (`git commit`)
- Pushing to remote (`git push`)
- Creating pull requests (`gh pr create`)
- Merging PRs (`gh pr merge`)
- Any destructive operation (hard reset, force push, delete branch)

**No confirmation needed for read-only or local operations**:
- `git status`, `git diff`, `git log`, `git branch`
- `git add` (staging)
- `git checkout`, `git switch` (switching branches)
- `git fetch`
- `gh pr view`, `gh pr list`, `gh issue list`

## Conventions

### Commits
- Messages: 1-2 sentences describing the change
- If many changes, break into multiple atomic commits
- Use imperative mood ("Add feature" not "Added feature")
- Never use `--amend` unless explicitly requested

### Branches
- Simple hyphenated names describing purpose
- Examples: `add-user-auth`, `fix-null-pointer`, `refactor-api-client`

### Pull Requests
- Title: concise summary of the change
- Description must include:
  1. **What**: Simple explanation of changes
  2. **Testing**: How changes were tested
  3. **Deploy**: Steps to deploy

## Common Workflows

### Check repo state
```bash
git status
git log --oneline -10
git branch -a
```

### View diffs
Staged changes (ready to commit):
```bash
git diff --cached          # full diff
git diff --cached --stat   # summary
```

Unstaged changes (modified but not staged):
```bash
git diff                   # full diff
git diff --stat            # summary
```

All changes in current branch vs base (for PR context):
```bash
git diff main...HEAD --stat   # summary
git diff main...HEAD          # full diff
git log main..HEAD --oneline  # commits that would be in PR
```

### Create a commit
```bash
git add <files>
git commit -m "Commit message here."
```

For multi-line messages:
```bash
git commit -m "$(cat <<'EOF'
Short summary of changes.

Additional context if needed.
EOF
)"
```

### Create a branch and PR
```bash
git checkout -b descriptive-branch-name
# ... make changes and commits ...
git push -u origin HEAD
gh pr create --title "Title here" --body "$(cat <<'EOF'
## Description

Brief description of changes.

## Testing

How this was tested.

## Deployment

Steps to deploy this change.
EOF
)"
```

### Get PR info
```bash
gh pr view --json number -q .number  # get PR number for current branch
gh pr list                            # list open PRs
```

### Review a PR
```bash
gh pr view <number>
gh pr diff <number>
gh pr checks <number>
gh api repos/{owner}/{repo}/pulls/<number>/comments  # view PR comments
gh pr review <number> --approve
gh pr review <number> --request-changes --body "Feedback here"
```

### Merge a PR
```bash
gh pr merge <number> --squash --delete-branch
```

### Working with issues
```bash
gh issue list
gh issue view <number>
gh issue create --title "Title" --body "Description"
gh issue close <number>
```

## Safety Rules

- Never force push to main
- Never use `--no-verify` unless explicitly requested
- Never amend commits that have been pushed
- Always verify before destructive operations (hard reset, etc.)
- Prefer merge commits over rebases to preserve history
- Flag potential secrets or sensitive files before committing (.env, credentials, API keys)
