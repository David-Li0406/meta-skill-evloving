---
name: pr-reviewer
description: Use this skill when asked to review a GitHub Pull Request, providing systematic feedback and ensuring code quality through automated tooling and industry-standard criteria.
---

# PR Reviewer Skill

Conduct comprehensive, professional code reviews for GitHub Pull Requests using industry-standard criteria and automated tooling.

## Purpose

This skill performs code reviews by:

1. **Automating data collection** - Fetching all PR-related information (metadata, diff, comments, commits, issues).
2. **Organizing review workspace** - Creating a structured directory with all artifacts.
3. **Applying systematic criteria** - Reviewing against a comprehensive quality checklist.
4. **Facilitating inline feedback** - Optionally adding comments directly to PR code.
5. **Ensuring completeness** - Checking functionality, security, testing, and maintainability.

## When to Use

Activate this skill when:
- A GitHub PR URL is provided with a review request.
- Receiving "review this PR" or "code review" requests.
- Checking PR quality before merging.
- Providing systematic feedback on proposed changes.
- GitHub PR review is mentioned in any context.

## Review Process Workflow

**IMPORTANT**: This skill uses a **two-stage approval process**. Nothing is posted to GitHub until explicit approval with `/send` or `/send-decline`.

### Overview

1. **Fetch PR data** - Collect all information.
2. **Generate review files** - Create detailed, human, and inline comment files.
3. **Review and edit** - Examine files, make changes as needed (use `/show`).
4. **Approve and post** - Use `/send` to submit your review.

## Common Commands

```bash
# Basic PR info
gh pr view <PR>                    # Overview
gh pr view <PR> --comments         # PR-level comments only (NOT inline!)
gh pr diff <PR>                    # View the diff

# Review comments (inline) - USE THE SCRIPT
gh-pr-review-comments <PR>         # ✅ Gets inline code review comments

# Or manually via API
gh api repos/OWNER/REPO/pulls/PR/comments | jq '.[] | {path, line, body}'

# Reviews (approve/request changes)
gh pr review <PR> --approve
gh pr review <PR> --request-changes --body "Please fix X"
gh pr review <PR> --comment --body "Looks good overall"

# Checks
gh pr checks <PR>                  # CI status
gh run view <RUN_ID> --log-failed  # Failed job logs
```

## Tips for Effective Reviews

- Be constructive and specific in your feedback.
- Focus on code quality, readability, and maintainability.
- Ensure that all tests pass before approving a PR.