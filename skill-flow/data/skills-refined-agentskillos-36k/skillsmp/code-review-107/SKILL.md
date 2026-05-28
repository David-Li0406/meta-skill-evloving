---
name: code-review
description: This skill should be used when reviewing GitHub Pull Requests to provide comprehensive code quality, security, and architecture analysis with optional JIRA ticket integration.
allowed-tools:
  - Bash
  - Task
  - Read
  - AskUserQuestion
---

# Review PR Skill

## Overview

Perform comprehensive code reviews of GitHub Pull Requests using the `gh` CLI, analyzing code quality, security, and architecture with automatic JIRA ticket context when available.

## When to Use

Use this skill when:
- User explicitly requests a PR review ("/review-pr", "review this PR", "analyze PR #123")
- User asks to review changes before merging
- User requests feedback on a pull request
- User wants security or code quality analysis of a PR

Do NOT use this skill for:
- Creating pull requests (use `create-pr` instead)
- Reviewing uncommitted local changes
- General code review without a PR context

## Quick Reference

```bash
# Get PR details
gh pr view <number> --json number,title,body,headRefName,baseRefName,commits,author,state,url

# Get full diff
gh pr diff <number>

# Get changed files
gh pr view <number> --json files

# Check current branch PR status
gh pr status --json number,title,url

# Fetch JIRA ticket (if reference found)
acli jira workitem search --jql "key = PROJ-123" --limit 1 --json
```

**Note: You should use the Atlassian MCP Server with the `getJiraIssue` tool if it is available**

## Step-by-Step Process

### 1. Identify the Pull Request

Extract PR reference from user input:
- PR number (e.g., "123", "#123")
- PR URL (e.g., "https://github.com/owner/repo/pull/123")
- Current branch (check for associated PR if not specified)

If not specified:
```bash
gh pr status --json number,title,url
```

### 2. Fetch PR Information

```bash
gh pr view <number> --json number,title,body,headRefName,baseRefName,commits,author,state,url
gh pr diff <number>
gh pr view <number> --json files
```

### 3. Extract JIRA Ticket (If Found)

Parse PR title for ticket reference using patterns:
- `feat(PROJ-123): Title`
- `fix: [PROJ-123] Title`
- `PROJ-123 - Title`
- Regex: `([A-Z]+-\d+)`

If found, fetch ticket details:
```bash
acli jira workitem search \
  --jql "key = PROJ-123" \
  --fields "key,summary,description,status,assignee,priority,labels" \
  --limit 1 --json
```

### 4. Dispatch to Code Reviewer Agent

Use Task tool with `subagent_type: "code-reviewer"` and comprehensive context including:
- PR metadata (number, title, author, URL)
- PR description
- JIRA ticket requirements (if found)
- Changed files summary
- Full diff

Direct the agent to use `references/review_criteria.md` for evaluation standards.

### 5. Format Review Output

Structure the review as:

```markdown
# Pull Request Review: PR #123

**Title**: feat(PROJ-456): Add user authentication
**Author**: @username
**URL**: https://github.com/owner/repo/pull/123
**JIRA Ticket**: [PROJ-456](link)

---

## Executive Summary
[High-level assessment with recommendation: Approve / Request Changes / Needs Work]

## Requirements Alignment
**Acceptance Criteria Coverage**:
- ✅ Criterion met - location
- ❌ Criterion missing

## Critical Issues
### 🔴 [Issue Title]
**Location**: `file.ts:67-72`
**Category**: Security
**Description**: ...
**Recommendation**: ...

## Important Issues
### 🟡 [Issue Title]
...

## Suggestions
### 💡 [Suggestion]
...

## Positive Observations
- ✅ What was done well

## Summary Statistics
- Files Changed: N
- Critical Issues: N
- Important Issues: N
- Suggestions: N
```

### 6. Present Review and Offer Actions

Display formatted review and offer:
1. Post as PR comment using `gh pr comment`
2. Export to file
3. Discuss specific findings
4. Re-review after changes

## Common Mistakes

| Mistake | Solution |
|---------|----------|
| Not fetching full diff | Always run `gh pr diff` to see actual changes |
| Skipping JIRA lookup | Always check for ticket reference in title/body |
| Generic findings | Reference specific files and line numbers |
| Missing positive feedback | Balance criticism with acknowledgment of good work |
| Not checking authentication | Verify `gh auth status` if commands fail |

## PR Title Parsing Patterns

| Pattern | Example |
|---------|---------|
| Prefix with colon | `PROJ-123: Add feature` |
| Conventional commits | `feat(PROJ-123): Add feature` |
| Square brackets | `feat: [PROJ-123] Add feature` |
| Suffix in parens | `feat: Add feature (PROJ-123)` |

## Resources

This skill uses `references/review_criteria.md` for detailed code review criteria organized by:
- Code Quality & Standards
- Security
- Architecture & Design
- Alignment with Requirements
- Documentation

The code-reviewer agent references this document for consistent, thorough reviews.

## Troubleshooting

- **"gh: command not found"**: Install with `brew install gh`
- **"acli: command not found"**: JIRA integration skipped, proceed without ticket context
- **"API rate limit"**: Wait or authenticate with `gh auth login`
- **"Could not resolve to a PullRequest"**: Verify PR number and repository access
- **Large PRs (500+ lines)**: Consider asking for focused review on specific aspects
