---
name: pr-review
description: Use this skill when you need to conduct a comprehensive review of GitHub pull requests, providing structured feedback and actionable comments.
---

# Skill body

## Overview

This skill helps you conduct thorough reviews of GitHub pull requests (PRs) by generating summaries, analyzing changes, and providing structured feedback.

## When to Use This Skill

Use this skill when the user asks you to review a GitHub pull request. The user will typically provide a PR URL or PR number.

## Steps to Review a PR

### Step 1: Generate PR Summary

Start by generating a comprehensive summary of the PR. This gives you the complete picture before diving deep:

```bash
scripts/summarize-pr.py <OWNER> <REPO> <PR_NUMBER>
```

**This script provides:**
- PR metadata (title, author, status, branch, stats)
- Description
- Files changed with additions/deletions
- Discussion & Reviews - Chronological timeline of all comments and reviews
- Unresolved Review Comments - Code review threads that need addressing (with diff context)

**Read and analyze this output carefully:**
- What problem is being solved?
- What's the current discussion context?
- What unresolved issues already exist?
- Who has reviewed and what are their concerns?

### Step 2: Prepare Git Worktree

Create a clean worktree for reviewing the PR and initialize review tracking:

```bash
WORKTREE_PATH=$(scripts/prepare-worktree.py <repository_directory> <PR_NUMBER>)
cd "$WORKTREE_PATH"
```

**What this does:**
- Creates a new worktree in `<repository>/git-worktrees/<branch-name>`
- Creates a review notes directory in `<repository>/review-notes/<branch-name>`
- Generates a `README.md` template in the review notes directory for tracking progress
- Fetches and checks out the PR branch in the worktree

### Step 3: Conduct the Review

1. **Functionality Check**: Ensure the code does what the PR description claims and handles edge cases appropriately.
2. **Security Review**: Check for hardcoded secrets, input validation, and vulnerabilities.
3. **Testing Assessment**: Verify that tests cover new functionality and edge cases.
4. **Code Quality Evaluation**: Ensure the code is readable, follows conventions, and has no unnecessary complexity.
5. **Performance Review**: Look for performance issues and ensure resource cleanup.
6. **Documentation Check**: Confirm that public APIs are documented and complex logic is commented.

### Step 4: Provide Feedback

- Be constructive: Suggest improvements, don't just criticize.
- Be specific: Point to exact lines and provide examples.
- Be timely: Aim to complete the first review within 4 hours.
- Be educational: Explain the "why" behind your suggestions.
- Be respectful: Assume good intent and praise good work.

### Step 5: Submit Review Comments

Use the following command to add comments to the PR:

```bash
gh pr comment <PR_NUMBER> --body "<Your feedback here>"
```

### Step 6: Follow Up

Check for any responses to your comments and be prepared to engage in further discussion if needed.

## Important Notes

- Always ensure that you are reviewing the most recent version of the PR.
- Focus on providing new insights rather than duplicating existing comments.