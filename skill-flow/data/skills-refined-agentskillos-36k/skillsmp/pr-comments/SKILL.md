---
name: pr-comments
description: Read and analyze GitHub pull request review comments. Use when reviewing PR feedback, understanding code review comments, or preparing responses to reviewers.
argument-hint: <PR-number or URL>
allowed-tools: Bash(gh:*)
---

# PR Review Comments Reader

Fetch and analyze review comments from a GitHub pull request.

## Instructions

When this skill is invoked, follow these steps:

### Step 1: Parse the argument

The argument can be:
- A PR number (e.g., `123`)
- A full GitHub URL (e.g., `https://github.com/owner/repo/pull/123`)

If no argument is provided, ask the user for the PR number.

### Step 2: Fetch PR information

Run these commands to gather PR data:

```bash
# Get PR metadata
gh pr view <PR> --json number,title,state,author,reviewDecision,reviews

# Get review comments (the actual review feedback)
gh api repos/{owner}/{repo}/pulls/<PR>/comments --jq '.[] | {path: .path, line: .line, body: .body, user: .user.login, created_at: .created_at}'

# Get general PR comments (conversation)
gh pr view <PR> --comments

# Get the diff for context
gh pr diff <PR> --stat
```

### Step 3: Analyze and present

Organize the review feedback into these sections:

1. **PR Summary**
   - Title, author, current state
   - Review decision (approved, changes requested, pending)
   - List of reviewers and their verdicts

2. **Code Review Comments** (grouped by file)
   - File path and line number
   - Reviewer name
   - Comment content
   - Whether it's blocking or a suggestion

3. **General Discussion**
   - Conversation thread highlights
   - Questions that need answers
   - Resolved vs unresolved discussions

4. **Action Items**
   - Changes that must be made (blocking)
   - Suggestions to consider
   - Questions to answer

### Step 4: Offer next steps

After presenting the review comments, offer to:
- Help address specific feedback
- Draft responses to reviewers
- Make the requested code changes
- Use `/superpowers:receiving-code-review` for deeper analysis

## Example Usage

```text
/pr-comments 51
/pr-comments https://github.com/malston/diego-capacity-analyzer/pull/51
```

## Requirements

- GitHub CLI (`gh`) must be installed and authenticated
- You must have access to the repository
