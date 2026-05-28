---
name: pr-check
description: Check GitHub PRs for conflicts, CI status, and review comments. Use when the user asks to check PR status, review PRs, see open PRs, check for merge conflicts, or asks about PRs needing their review.
---

# PR Check Skill

Check the status of GitHub Pull Requests.

## Workflow

1. Verify GitHub CLI authentication: `gh auth status`
2. Fetch open PRs authored by user: `gh pr list --author "@me" --state open --json number,title,url,reviewDecision,statusCheckRollup,mergeable,isDraft`
3. Fetch PRs requesting user's review: `gh pr list --search "review-requested:@me" --state open --json number,title,url,author,reviewDecision`

## Classification

- **CRITICAL**: Merge conflicts, CI failing, changes requested
- **ACTION_REQUIRED**: Unresolved comments, pending reviews
- **READY**: All CI passing, approved, mergeable, not draft

## Output Format

Display a formatted table with:
- PR number and title
- Status (CRITICAL/ACTION_REQUIRED/READY)
- Key issues if any
