---
name: gh-workflow
description: Manage project work via GitHub CLI. Use for ALL GitHub tasks including creating/viewing issues, organizing with milestones, establishing blocked-by/blocking dependencies, and responding to PR comments.
---

# GitHub Workflow Skill

## Issue Creation Template (MANDATORY)

Every issue created must follow this structure:

### Context
Describe WHAT the issue is about and WHY it matters. Never describe HOW to implement it.

### Investigation Starting Points
- File/code references that are relevant
- Specific functions, modules, or tests to look at

### Scope Constraints
- What is explicitly NOT in scope
- Boundaries to prevent scope creep

### Validation
- Testable acceptance criteria
- How to verify the issue is resolved

---

## Organization with Milestones

```bash
# Create issue in milestone
gh issue create --title "..." --body "..." --milestone "v1.0"

# List milestones
gh api repos/{owner}/{repo}/milestones

# Create milestone
gh api repos/{owner}/{repo}/milestones -f title="v1.0" -f description="..."
```

---

## Issue Dependencies (via REST API)

GitHub has native blocked-by/blocking support. The `gh` CLI doesn't have direct flags yet, but we use `gh api`:

```bash
# Mark issue #2 as blocked by issue #1 (need issue ID, not number)
# First get the issue ID:
gh api repos/{owner}/{repo}/issues/1 --jq '.id'

# Then add dependency:
gh api repos/{owner}/{repo}/issues/2/dependencies/blocked_by -f issue_id=<ID_FROM_ABOVE>

# List what blocks an issue
gh api repos/{owner}/{repo}/issues/2/dependencies/blocked_by

# List what an issue blocks
gh api repos/{owner}/{repo}/issues/1/dependencies/blocking

# Remove dependency
gh api -X DELETE repos/{owner}/{repo}/issues/2/dependencies/blocked_by/<blocking_issue_id>
```

---

## Core Issue Commands

```bash
# List issues
gh issue list
gh issue list --milestone "v1.0"

# View issue
gh issue view <number>

# Create issue
gh issue create --title "..." --body "..." --label "..." --milestone "..."

# Edit issue
gh issue edit <number> --add-label "..." --milestone "..."
```

---

## PR Comment Commands

```bash
# Add general comment to PR
gh pr comment <number> --body "..."

# View PR with comments
gh pr view <number> --comments

# Reply to a specific review comment (inline code comment)
gh api repos/{owner}/{repo}/pulls/<pr>/comments -f body="..." -F in_reply_to=<comment_id>

# List review comments to find comment IDs
gh api repos/{owner}/{repo}/pulls/<pr>/comments

# Reply to a general PR comment (issue comment)
gh api repos/{owner}/{repo}/issues/<pr>/comments -f body="..."
```
