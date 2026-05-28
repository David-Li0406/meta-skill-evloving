---
name: pr-review-and-address
description: Use this skill to fetch PR comments, summarize issues, address them, and update the PR.
---

# PR Review and Address

Automates the process of reviewing PR feedback, summarizing issues, addressing them, and updating the PR.

## Workflow

1. **Get Repository Info** - Retrieve the repository details.
2. **Fetch PR Comments** - Get all review comments from the specified PR.
3. **Identify Reviewer Types** - Tag comments as from bots or humans.
4. **Summarize Issues** - Present a summary of issues categorized by their urgency and type.
5. **Checkout PR Branch** - Switch to the branch associated with the PR.
6. **Address Each Issue** - Read relevant files, apply necessary code changes, and prepare responses for questions.
7. **Verify Changes** - Run type checking and build commands to ensure code integrity.
8. **Commit and Push** - Create a commit with a summary of changes and push to the remote branch.
9. **Report Summary** - Provide a summary of addressed issues and comments.

## Instructions

### Step 1: Get Repository Info

Run the following command to get repository details:

```bash
gh repo view --json owner,name
```

### Step 2: Fetch PR Comments

Ask for the PR number and fetch comments using:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      title
      body
      author { login }
      reviews(first: 100) {
        nodes {
          author { login }
          body
          state
          comments(first: 100) {
            nodes {
              body
              path
              line
              author { login }
            }
          }
        }
      }
      comments(first: 100) {
        nodes {
          author { login }
          body
        }
      }
      reviewThreads(first: 100) {
        nodes {
          isResolved
          path
          line
          comments(first: 50) {
            nodes {
              author { login }
              body
            }
          }
        }
      }
    }
  }
}' -F owner='{owner}' -F repo='{repo}' -F pr={PR_NUMBER}
```

### Step 3: Identify Reviewer Types

Tag each comment as 🤖 Bot or 👤 Human based on the author.

### Step 4: Summarize Issues

Present a summary table of issues categorized by urgency and type:

| # | File:Line | Reviewer | Type | Issue | Status |
|---|-----------|----------|------|-------|--------|

Group issues into:
- 🔴 Blocking (changes requested, security)
- 🟠 Suggestions (improvements)
- 🟡 Nitpicks (style, minor)
- 💬 Questions/Discussion

### Step 5: Checkout PR Branch

Switch to the PR branch:

```bash
gh pr checkout {PR_NUMBER}
```

### Step 6: Address Each Issue

For each open issue:
1. Read the relevant files.
2. Apply the necessary code changes.
3. Prepare responses for any questions.
4. Skip resolved threads.

### Step 7: Verify Changes

Run type checking and build commands to ensure the code is functioning correctly.

### Step 8: Commit and Push

Create a commit with a summary of changes:

```bash
git add -A
git commit -m "Address PR review feedback"
git push
```

### Step 9: Report Summary

Provide a summary of addressed issues:

```
✅ Addressed: X issues (Y from bots, Z from humans)
💬 Responded: N comments  
⏭️ Skipped: M (resolved/false positives)
```

## Notes

- Always confirm the list of open issues with the user before fixing.
- Preserve the original PR author's intent and prioritize human feedback over bot suggestions.
- Investigate security issues thoroughly before applying fixes.