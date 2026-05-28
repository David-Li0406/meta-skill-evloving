---
name: pr-reviewer
description: Fetch PR comments, summarize issues, address them, commit and update PR
---

# PR Reviewer

Fetch all comments from a GitHub PR, summarize issues, address them, and update the PR.

## Workflow

### 1. Get Repository Info

```bash
gh repo view --json owner,name
```

### 2. Fetch PR Comments

Ask for the PR number, then fetch all comments:

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

### 3. Identify Reviewer Types

Known bots:
- `qodo-merge-pro[bot]` - Structured suggestions
- `coderabbitai[bot]` - Detailed analysis
- `gemini-code-assist[bot]` - Suggestions
- `copilot[bot]` - Code suggestions
- `sonarcloud[bot]` - Security/bugs

Tag each comment as 🤖 Bot or 👤 Human.

### 4. Summarize Issues

Present a table:
| # | File:Line | Reviewer | Type | Issue | Status |

Group by:
- 🔴 Blocking (changes requested, security)
- 🟠 Suggestions (improvements)
- 🟡 Nitpicks (style, minor)
- 💬 Questions/Discussion

### 5. Checkout PR Branch

```bash
gh pr checkout {PR_NUMBER}
```

### 6. Address Each Issue

- Read referenced files for full context
- Make necessary code changes
- For questions: prepare response comments
- Skip resolved threads

**Bot handling:**
- Evaluate, don't blindly apply
- Security issues: always investigate
- Human feedback takes priority over bot suggestions

### 7. Verify Changes

Run type checking and build commands.

### 8. Commit and Push

```bash
git add -A
git commit -m "Address PR review feedback"
git push
```

### 9. Report Summary

```
✅ Addressed: X issues (Y from bots, Z from humans)
💬 Responded: N comments  
⏭️ Skipped: M (resolved/false positives)
```

## Notes

- Always preserve the original PR author's intent
- If an issue is unclear, ask for clarification instead of guessing
- Human feedback takes priority over bot suggestions when they conflict
- Security issues from any source should always be addressed
