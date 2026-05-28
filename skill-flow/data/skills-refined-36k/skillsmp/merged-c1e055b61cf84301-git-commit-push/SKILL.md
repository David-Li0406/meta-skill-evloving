---
name: git-commit-push
description: Use this skill when you want to stage, commit, and push git changes with conventional commit messages.
---

# Git Commit and Push Workflow

Stage all changes, create a conventional commit, and push to the remote branch.

## When to Use

Automatically activate when the user:
- Explicitly asks to push changes ("push this", "commit and push")
- Mentions saving work to remote ("save to github", "push to remote")
- Completes a feature and wants to share it
- Says phrases like "let's push this up" or "commit these changes"

## Workflow

**ALWAYS use the script** - do NOT use manual git commands:

```bash
bash skills/git-pushing/scripts/smart_commit.sh
```

With custom message:

```bash
bash skills/git-pushing/scripts/smart_commit.sh "<commit_message>"
```

PowerShell + Git Bash (Windows) alternative:

```bash
COMMIT_MSG_OVERRIDE="<commit_message>" bash skills/git-pushing/scripts/smart_commit.sh
```

The script handles staging, conventional commit messages, Claude footer, and pushes with the -u flag.