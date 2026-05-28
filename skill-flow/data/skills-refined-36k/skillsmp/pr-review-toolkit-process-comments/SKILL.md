---
name: pr-review-toolkit-process-comments
description: |
  Process GitHub PR review comments and change requests - answer questions, make corrections, resolve threads.
  WHEN: Use after PR is created and has review comments. Invoke with "/pr-review-toolkit:process-comments".
  WHEN NOT: When PR has no comments or before PR is created.
---

# PR Review Process Comments

## Overview

This skill processes GitHub PR review comments and change requests:
1. Validate prerequisites (authentication, branch, permissions)
2. Fetch all comments and change requests
3. Categorize by type (question, change request, suggestion)
4. Answer questions with replies
5. Make code corrections for change requests
6. Mark threads as resolved after addressing

**Announce at start:** "I'm using the pr-review-toolkit:process-comments skill to process PR feedback."

---

## Step 0: Prerequisite Validation

Before processing comments, verify the following prerequisites:

### 0.1 Verify GitHub CLI Authentication

```bash
# Check if gh is authenticated
gh auth status
```

**Expected output:** Shows authenticated user and scopes.

**If authentication fails:**
- Error: `You are not logged in` - Run `gh auth login` to authenticate
- Error: `authentication token has expired` - Run `gh auth refresh`

### 0.2 Verify You're on the PR Branch

```bash
# Get current branch name
git branch --show-current

# Verify this branch has an associated PR
gh pr view --json number,headRefName -q '.headRefName'
```

**If not on PR branch:**
- Error: `no pull requests found for branch` - Switch to the correct branch with `git checkout <branch-name>`
- The branch name from `git branch --show-current` should match `headRefName` from the PR

### 0.3 Verify Write Permissions

```bash
# Check your permissions on the repository
# gh repo view uses the current git remote automatically
gh repo view --json viewerPermission -q '.viewerPermission'
```

**Expected output:** `ADMIN`, `MAINTAIN`, or `WRITE`

**Permission levels:**
- `ADMIN` / `MAINTAIN` / `WRITE` - Full access to push changes and resolve threads
- `TRIAGE` - Can manage issues/PRs but cannot push code
- `READ` - Can only view and comment

**If insufficient permissions:**
- You can still reply to comments but cannot push code changes
- You cannot programmatically resolve threads without write access

---

## Step 1: Fetch PR Comments

### 1.1 Get Repository and PR Information

The `gh` CLI automatically determines `{owner}` and `{repo}` from your git remote. For explicit API calls, extract them:

```bash
# Get owner and repo from current git remote
REPO_INFO=$(gh repo view --json owner,name -q '"\(.owner.login)/\(.name)"')
OWNER=$(echo $REPO_INFO | cut -d'/' -f1)
REPO=$(echo $REPO_INFO | cut -d'/' -f2)

# Get PR number for current branch
PR_NUM=$(gh pr view --json number -q '.number')

# Verify PR exists
echo "Processing PR #$PR_NUM in $OWNER/$REPO"
```

**If `gh pr view` fails:**
- Error: `no pull requests found` - Ensure you're on a branch with an open PR
- Error: `could not find any open pull requests` - The PR may be closed/merged
- Error: `authentication required` - Run `gh auth login`

### 1.2 Fetch All Review Comments

GitHub has three types of comments on PRs. Understanding when to use each:

| API Endpoint | What It Returns | Use When |
|--------------|-----------------|----------|
| `/pulls/{pr}/comments` | Inline code review comments (attached to specific lines) | Processing code-level feedback |
| `/issues/{pr}/comments` | General PR comments (not attached to code) | Processing high-level discussion |
| `/pulls/{pr}/reviews` | Review submissions (APPROVE, REQUEST_CHANGES, COMMENT) | Checking overall review status |

```bash
# Get PR review comments (inline code comments)
# Returns: comments attached to specific lines in the diff
gh api repos/$OWNER/$REPO/pulls/$PR_NUM/comments

# Get PR issue comments (general comments on the PR, not attached to code)
# Returns: comments in the main PR conversation thread
gh api repos/$OWNER/$REPO/issues/$PR_NUM/comments

# Get PR reviews (the review submissions themselves)
# Returns: APPROVED, CHANGES_REQUESTED, COMMENTED, PENDING, DISMISSED
gh api repos/$OWNER/$REPO/pulls/$PR_NUM/reviews
```

**Rate Limiting:** If you see `API rate limit exceeded`:
- Wait for the reset time shown in the error
- Use `gh api rate_limit` to check your remaining requests
- Consider using `--paginate` for repos with many comments

### 1.3 Parse and Display Comments

For each **review comment** (from `/pulls/{pr}/comments`), extract:
- **id**: Numeric comment ID (used for REST API replies)
- **node_id**: GraphQL node ID (used for thread resolution - starts with `PRRC_`)
- **path**: File path where comment was made
- **line** or **original_line**: Line number in the diff
- **body**: Comment text
- **user.login**: Who wrote it
- **in_reply_to_id**: If this comment is a reply to another (indicates threading)

For each **review** (from `/pulls/{pr}/reviews`), the **state** field indicates:
- `APPROVED` - Reviewer approved the PR
- `CHANGES_REQUESTED` - Reviewer requested changes
- `COMMENTED` - Reviewer left comments without approval/rejection
- `PENDING` - Review not yet submitted
- `DISMISSED` - Review was dismissed

**Note:** Individual comments don't have a state field - the state belongs to the parent review.

Display in table format:

```
| # | Type | File | Line | Comment | Author |
|---|------|------|------|---------|--------|
| 1 | Question | backend/package.json | 11 | Why is axios here? | user |
| 2 | Change Request | src/Controller.php | 45 | Add validation | user |
```

---

## Step 2: Categorize Comments

### Categories

| Type | Indicators | Action |
|------|------------|--------|
| **Question** | "?", "why", "what", "how", "could you explain" | Reply with answer |
| **Change Request** | "please", "should", "must", "change", "fix", "add", "remove" | Make code change |
| **Suggestion** | "consider", "might", "could", "optional", "nit" | Evaluate and decide |
| **Approval** | "LGTM", "looks good", "approved" | No action needed |

### Create Todo List

```
For each actionable comment, create a todo:
- [ ] Comment #1: [Question] Answer why axios is in devDependencies
- [ ] Comment #2: [Change] Add input validation to Controller.php:45
```

---

## Step 3: Process Each Comment

### 3.1 For Questions - Reply with Answer

```bash
# Reply to a PR review comment (inline code comment)
# Using variables set in Step 1.1
gh api repos/$OWNER/$REPO/pulls/$PR_NUM/comments/$COMMENT_ID/replies \
  -f body="<your answer here>"

# For issue comments (general PR conversation), create a new comment instead
gh pr comment $PR_NUM --body "Re: @username's question about X - <your answer>"
```

**Guidelines for answers:**
- Be concise and technical
- Reference documentation or code if helpful
- If you don't know, say so and ask for clarification

**Note on threading:**
- **Review comments** (inline code comments) support replies via the `/replies` endpoint, creating threaded conversations
- **Issue comments** (general PR comments) do not have a reply endpoint - create a new comment and @mention the person

### 3.2 For Change Requests - Make Corrections

1. **Read the file** mentioned in the comment
2. **Understand the request** - what change is needed?
3. **Make the change** using Edit tool
4. **Verify** the change doesn't break tests:
   ```bash
   # Run your project's test suite - examples for common frameworks:
   # JavaScript/Node: npm test
   # Python: pytest / python -m pytest
   # Go: go test ./...
   # Rust: cargo test
   # Java/Maven: mvn test
   # Ruby: bundle exec rspec
   # PHP: ./vendor/bin/phpunit
   # Or check package.json/Makefile for project-specific test commands
   ```
5. **Commit** with descriptive message:
   ```bash
   git add <file>
   git commit -m "fix: <description of change>

   Addresses PR comment #<comment_id>"
   ```

### 3.3 For Suggestions - Evaluate

1. **Consider** if the suggestion improves the code
2. **If yes**: Apply like a change request
3. **If no**: Reply explaining why not:
   ```bash
   gh api repos/$OWNER/$REPO/pulls/$PR_NUM/comments/$COMMENT_ID/replies \
     -f body="Thanks for the suggestion. I chose not to apply this because..."
   ```

---

## Step 4: Mark as Resolved

### 4.1 Understanding Thread Resolution

GitHub review threads can be resolved programmatically, but there are important caveats:

**Thread Node IDs:**
- Review comments have a `node_id` (e.g., `PRRC_kwDOABC123...`) - this is the **comment** node ID
- To resolve a thread, you need the **thread** node ID, not the comment node ID
- Thread node IDs start with `PRRT_` (Pull Request Review Thread)

### 4.2 Get Thread Node ID from Comment

First, get the thread ID associated with a comment:

```bash
# Get thread information for all review comments
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes {
              id
              body
              path
            }
          }
        }
      }
    }
  }
}' -f owner="$OWNER" -f repo="$REPO" -F pr="$PR_NUM"
```

This returns threads with their `id` (the thread node ID starting with `PRRT_`) and the associated comments.

### 4.3 Resolve the Thread

Once you have the thread node ID:

```bash
# Set the thread ID (starts with PRRT_)
THREAD_ID="PRRT_kwDOABC123..."

# Resolve the thread using GraphQL mutation
gh api graphql -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread {
      id
      isResolved
    }
  }
}' -f threadId="$THREAD_ID"
```

**Quick reference - mapping comment to thread:**
```bash
# Get a mapping of comment paths/bodies to thread IDs for easy lookup
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          path
          comments(first: 1) {
            nodes {
              body
            }
          }
        }
      }
    }
  }
}' -f owner="$OWNER" -f repo="$REPO" -F pr="$PR_NUM" \
  --jq '.data.repository.pullRequest.reviewThreads.nodes[] | "\(.path): \(.id) (resolved: \(.isResolved)) - \(.comments.nodes[0].body | .[0:50])..."'
```

### 4.4 Thread Resolution Permissions and Limitations

**GitHub Plan Requirements:**
- Thread resolution is available on all GitHub plans (Free, Team, Enterprise)
- However, **who** can resolve threads depends on repository settings

**Permission Requirements:**
- Repository collaborators with write access can resolve any thread
- PR authors can typically resolve threads on their own PRs
- Comment authors can resolve their own threads

**Common Error Messages:**

| Error | Meaning | Solution |
|-------|---------|----------|
| `Could not resolve to a node with the global id` | Invalid thread ID | Ensure you're using `PRRT_` thread ID, not `PRRC_` comment ID |
| `Resource not accessible by integration` | Insufficient permissions | You may not have write access; ask reviewer to resolve |
| `NOT_FOUND` | Thread doesn't exist or no access | Verify PR number and your repository access |

### 4.5 Alternative: Reply and Let Author Resolve

If you cannot resolve programmatically (permissions issue or API error), reply with:
```
"Addressed in commit <sha>. Please resolve this thread if satisfied."
```

This is often the safest approach as it lets the reviewer verify the fix before resolving.

---

## Step 5: Push Changes and Update PR

### 5.1 Push All Commits

```bash
git push
```

### 5.2 Add Summary Comment to PR

```bash
gh pr comment $PR_NUM --body "## PR Feedback Addressed

### Questions Answered
- Comment #1: Explained why axios is included

### Changes Made
- Comment #2: Added validation (commit abc123)

### Suggestions
- Comment #3: Applied suggestion for better naming

All review feedback has been addressed. Ready for re-review."
```

---

## Step 6: Request Re-review (Optional)

If the PR had "Changes Requested" status:

```bash
# Get the username of the reviewer who requested changes
REVIEWER=$(gh api repos/$OWNER/$REPO/pulls/$PR_NUM/reviews \
  --jq '[.[] | select(.state == "CHANGES_REQUESTED")] | .[0].user.login')

# Request re-review
gh pr edit $PR_NUM --add-reviewer "$REVIEWER"
```

---

## Complete Workflow Example

```bash
# 0. Validate prerequisites
gh auth status
git branch --show-current

# 1. Set up variables
REPO_INFO=$(gh repo view --json owner,name -q '"\(.owner.login)/\(.name)"')
OWNER=$(echo $REPO_INFO | cut -d'/' -f1)
REPO=$(echo $REPO_INFO | cut -d'/' -f2)
PR_NUM=$(gh pr view --json number -q '.number')

echo "Processing PR #$PR_NUM in $OWNER/$REPO"

# 2. Fetch comments
gh api repos/$OWNER/$REPO/pulls/$PR_NUM/comments

# 3. Process each comment (done manually with tools)

# 4. After all changes, push
git push

# 5. Add summary comment
gh pr comment $PR_NUM --body "All feedback addressed. See commits for changes."
```

---

## Error Handling

### Authentication Failures

| Error | Cause | Solution |
|-------|-------|----------|
| `gh: authentication required` | Not logged in | Run `gh auth login` |
| `401 Unauthorized` | Token expired or revoked | Run `gh auth refresh` |
| `403 Forbidden` | Insufficient token scopes | Re-authenticate with `gh auth login --scopes repo` |

### Rate Limiting

```bash
# Check current rate limit status
gh api rate_limit --jq '.resources.core'
```

| Error | Solution |
|-------|----------|
| `API rate limit exceeded` | Wait until reset time shown in error, or authenticate for higher limits |
| `secondary rate limit` | You're making requests too fast; add delays between API calls |

### Comment Not Found

```bash
# Refresh the comment list to get current state
gh api repos/$OWNER/$REPO/pulls/$PR_NUM/comments

# If comment was part of a pending review, check reviews
gh api repos/$OWNER/$REPO/pulls/$PR_NUM/reviews
```

Possible causes:
- Comment was deleted by the author
- Comment is part of a pending (not yet submitted) review
- You're looking in the wrong endpoint (issue comments vs review comments)

### Cannot Resolve Thread

| Error | Cause | Solution |
|-------|-------|----------|
| `Could not resolve to a node` | Wrong ID type (used comment ID instead of thread ID) | Use `PRRT_` thread ID from GraphQL query |
| `Resource not accessible` | Insufficient permissions | Reply with "Addressed in commit X" and let reviewer resolve |
| `NOT_FOUND` | Thread doesn't exist | Verify PR number and refresh thread list |

### Tests Fail After Change
- Revert the change: `git checkout -- <file>`
- Reply to comment asking for clarification
- Do NOT push broken code

### Push Rejected

| Error | Cause | Solution |
|-------|-------|----------|
| `rejected: non-fast-forward` | Remote has new commits | `git pull --rebase` then push again |
| `protected branch` | Branch has protection rules | Create commits meeting requirements (tests pass, reviews approved) |
| `permission denied` | No write access | Request access from repository maintainers |

---

## Checklist

Before completing:

- [ ] Prerequisites validated (auth, branch, permissions)
- [ ] All comments fetched and categorized
- [ ] All questions answered with replies
- [ ] All change requests addressed with code changes
- [ ] All suggestions evaluated (applied or explained why not)
- [ ] All changes committed with references to comment IDs
- [ ] Tests still pass after changes
- [ ] Changes pushed to PR branch
- [ ] Summary comment added to PR
- [ ] Threads marked as resolved (if possible)

---

## Quick Reference: GitHub API Endpoints

| Endpoint | Returns | Node ID Prefix |
|----------|---------|----------------|
| `GET /repos/{owner}/{repo}/pulls/{pr}/comments` | Inline code review comments | `PRRC_` (comment) |
| `GET /repos/{owner}/{repo}/issues/{pr}/comments` | General PR conversation comments | `IC_` (issue comment) |
| `GET /repos/{owner}/{repo}/pulls/{pr}/reviews` | Review submissions (APPROVE, etc.) | `PRR_` (review) |
| `POST .../comments/{id}/replies` | Reply to inline comment | - |
| GraphQL `reviewThreads` | Thread objects for resolution | `PRRT_` (thread) |

**Key distinction:**
- **Review comments** = attached to specific code lines in the diff
- **Issue comments** = in the main PR conversation (like GitHub Issues)
- **Reviews** = the approval/rejection action (contains a state and optional body)
