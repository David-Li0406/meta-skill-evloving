---
name: development-workflow
description: Use this skill when managing development workflows, including branch creation, PR management, and review feedback.
---

# Skill body

## Getting Started

Run `make help` to see all available targets and understand the build workflow.

```bash
make help
```

## Creating Branches

Create a new branch off the latest default branch commit.

### Workflow

1. Fetch latest from remote.
2. Detect default branch (main or master).
3. Create branch with a descriptive name based on the task.
4. Switch to the new branch.

### Branch Naming

Generate a short, kebab-case name from the task:
- `add-user-auth` not `add-user-authentication-feature`
- `fix-login-bug` not `fix-the-bug-in-the-login-flow`
- `refactor-api` not `refactor-api-endpoints-for-better-performance`

Use a prefix if the repo convention requires one (check existing branches).

```bash
# Fetch and get default branch
git fetch origin
git remote show origin | sed -n '/HEAD branch/s/.*: //p'

# Create branch from latest default branch
git checkout -b <branch-name> origin/main

# See existing branch naming patterns
git branch -r | head -20
```

If branches use prefixes like `feature/`, `fix/`, or username prefixes like `wcm/`, follow that pattern.

## Pull Request Descriptions

**CRITICAL: You MUST create and maintain a PR description file for every branch.**

This file describes what's happening on the branch. Update it before every push.

1. Create `.github/pr/<slug>.md` with a descriptive slug (e.g., `add-auth-logging.md`, `fix-parser-edge-case.md`).
2. Use this format:

```markdown
# component: verb explanation

Brief description of what this change does and why.

## Changes

- `path/to/file.lua` - what it does
- `path/to/other.lua` - what it does
```

**Guidelines:**
- Choose a descriptive, kebab-case slug.
- Title format: `component: verb explanation` (sentence case).
- Keep descriptions concise but include key decisions and tradeoffs.
- **Update the file before every push** to reflect the current state of the branch.

## Review Feedback

Address GitHub PR review comments and reply to reviewers.

### Workflow

1. **Get pending review comments** - fetch unresolved comments.
2. **Address each comment** - make code changes to resolve feedback.
3. **Commit with a clear message** - reference what feedback was addressed.
4. **Reply to reviewer** - concise reply with commit SHA and explanation.

### Getting Review Comments

```bash
# All comments on a PR (includes replies)
gh pr view <pr-number> --comments --json comments

# Review comments (code-level feedback)
gh api repos/{owner}/{repo}/pulls/{pr}/comments --jq '.[] | {id, path, line, body, user: .user.login, in_reply_to_id}'

# Pending/unresolved comments (no replies yet)
gh api repos/{owner}/{repo}/pulls/{pr}/comments --jq '[.[] | select(.in_reply_to_id == null)] | .[] | {id, path, body: .body[0:100]}'
```

### Replying to Comments

```bash
# Reply to a review comment
gh api repos/{owner}/{repo}/pulls/{pr}/comments \
  --method POST \
  -f body="Fixed in abc1234 - renamed to run-test.js" \
  -F in_reply_to=<comment-id>
```

### Good Reply Format

Replies should be:
- **Concise** - one sentence is often enough.
- **Reference commit SHA** - so the reviewer can verify.
- **Explain how** - brief description of the fix.

Examples:
- `Fixed in abc1234 - renamed to run-test.js as suggested`
- `Addressed in def5678 - ...`