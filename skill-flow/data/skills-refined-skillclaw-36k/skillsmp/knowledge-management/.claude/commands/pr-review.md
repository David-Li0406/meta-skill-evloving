---
description: Review and respond to PR feedback from reviewers
---

# PR Review Handler

ตรวจสอบ PR ที่ได้รับ review และจัดการ feedback อัตโนมัติ

## Usage

```
/pr-review              # ตรวจสอบ PR ของ current branch
/pr-review [pr-number]  # ตรวจสอบ PR เฉพาะเจาะจง
```

## Instructions

### Step 1: Find Open PRs with Reviews

```bash
# Get current branch name
BRANCH=$(git branch --show-current)

# List open PRs authored by current user
echo "=== Open PRs ==="
gh pr list --author "@me" --state open --json number,title,url,headRefName,reviews,reviewDecision

# If specific PR number provided, use that instead
# gh pr view [pr-number] --json number,title,url,headRefName,reviews,reviewDecision,comments
```

### Step 2: Check Review Status

```bash
# Get PR reviews for the branch or specified PR
gh pr view --json reviews,reviewDecision,reviewRequests

# Check if PR has been reviewed
# reviewDecision: APPROVED, CHANGES_REQUESTED, REVIEW_REQUIRED, or null
```

**ถ้าไม่มี review:** แจ้งผู้ใช้ว่ายังไม่มี review และจบการทำงาน

**ถ้ามี review:** ดำเนินการต่อ Step 3

### Step 3: Display PR Details

แสดงข้อมูล PR ในรูปแบบที่อ่านง่าย:

```markdown
## PR #[number]: [title]

**URL**: [url]
**Branch**: [headRefName]
**Review Status**: [reviewDecision]

### Reviews
| Reviewer | State | Comment |
|----------|-------|---------|
| [author] | [state] | [body preview] |
```

### Step 4: Fetch and Analyze Review Comments

```bash
# Get PR comments (review comments)
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments --jq '.[] | {id, path, line, body, user: .user.login}'

# Get PR review comments
gh pr view --json reviews --jq '.reviews[] | {author: .author.login, state: .state, body: .body}'

# Get general PR comments (conversation)
gh api repos/{owner}/{repo}/issues/{pr_number}/comments --jq '.[] | {id, body, user: .user.login}'
```

### Step 5: Summarize Review Feedback

สรุป feedback ในรูปแบบ:

```markdown
## Review Summary

### Action Required (ต้องแก้ไข)
- [ ] [file:line] [description] - by @[reviewer]

### Suggestions (พิจารณา)
- [ ] [file:line] [description] - by @[reviewer]

### Deferred (สร้าง issue แล้วทำทีหลัง)
- [ ] [file:line] [description] - by @[reviewer] → #[issue-number]

### Praise/Acknowledgments (รับทราบ)
- [x] [description] - by @[reviewer]

### Questions (ตอบคำถาม)
- [ ] [question] - by @[reviewer]
```

### Step 6: Handle Each Comment

**IMPORTANT: Reply แยกแต่ละ comment โดยตรง**
- ห้ามรวม reply หลาย comments ไว้ใน comment เดียว
- ห้ามสร้าง comment ใหม่แยกต่างหาก
- ต้อง reply ไปที่ comment นั้นๆ โดยตรงเท่านั้น

สำหรับ **แต่ละ comment** ให้ทำแยกกัน:

#### 6.1 Comment ที่ต้องแก้ไข

```bash
# 1. แก้โค้ดตาม review comment แล้ว commit
git add .
git commit -m "fix: [short description of fix]"

# 2. เก็บ hash ของ commit ที่เพิ่ง commit
COMMIT_HASH=$(git rev-parse --short HEAD)

# 3. Reply ไปที่ comment_id นั้นโดยตรง (ห้ามรวมกับ comment อื่น)
# IMPORTANT: ใส่ commit hash เพื่อให้ reviewer trace ได้
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -f body="Fixed in ${COMMIT_HASH}! [description of what was changed]"
```

**หมายเหตุ:**
- ถ้าแก้หลาย comments ใน commit เดียว ทุก reply จะใช้ hash เดียวกัน
- สำหรับ reply ที่มี user content หรือ special characters ใช้ `-F` flag กับ temp file แทน:

```bash
# สำหรับ content ที่มี special chars (เช่น quotes, backticks)
REPLY_BODY="Fixed in ${COMMIT_HASH}!

$(echo "$USER_DESCRIPTION" | sed 's/[`$"\\]/\\&/g')"

echo "$REPLY_BODY" > /tmp/reply.txt
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -F body=@/tmp/reply.txt
rm /tmp/reply.txt
```

#### 6.2 Comment ที่ไม่ต้องแก้ไข

```bash
# Reply ไปที่ comment_id นั้นโดยตรง (ห้ามรวมกับ comment อื่น)
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -f body="Thanks for the suggestion!

[explanation why not changing]

[alternative approach if applicable]"
```

#### 6.3 Comment ที่เป็นคำถาม

```bash
# Reply ไปที่ comment_id นั้นโดยตรง (ห้ามรวมกับ comment อื่น)
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -f body="[answer to question]"
```

#### 6.4 Comment ที่เป็นคำชม

```bash
# Reply ไปที่ comment_id นั้นโดยตรง
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -f body="Thank you! [brief acknowledgment]"
```

#### 6.5 Comment ที่ต้อง Defer (งานที่จะทำภายหลัง)

**IMPORTANT:** ห้ามตอบลอยๆ เช่น "will do later", "added to backlog" โดยไม่มี tracking

เมื่อ review comment ต้องการงานที่ไม่สามารถทำใน PR นี้ได้:

```bash
# 1. สร้าง issue ก่อน
# IMPORTANT: ใช้ <<'EOF' (quoted) เพื่อป้องกัน shell expansion จาก reviewer comment
DEFER_ISSUE=$(gh issue create \
  --title "[type]: [descriptive title from comment]" \
  --label "enhancement" \
  --body "$(cat <<'EOF'
## Overview

From PR review comment by @[reviewer]

## Original Comment

> [quote the reviewer's comment]

## Context

- **PR:** #[pr_number]
- **File:** [file_path]
- **Line:** [line_number]

## Proposed Work

[description of what needs to be done]

## Acceptance Criteria

- [ ] [criteria based on reviewer's request]

---

*Created from PR review: [pr_url]*
EOF
)" --json number -q .number)

# 2. Reply พร้อม issue reference
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -f body="Thanks for the feedback! Created #$DEFER_ISSUE to track this work."
```

**ตัวอย่าง Defer Cases:**

| Review Comment | Issue Title | Label |
|----------------|-------------|-------|
| "Missing tests for this feature" | `test: add unit tests for [feature]` | `enhancement` |
| "Consider adding error handling" | `fix: improve error handling in [component]` | `enhancement` |
| "Documentation could be improved" | `docs: improve documentation for [feature]` | `enhancement` |
| "Performance could be better" | `perf: optimize [operation]` | `enhancement` |

**Example - Multiple Comments:**

```bash
# หลัง commit แก้ไขแล้ว - เก็บ hash
COMMIT_HASH=$(git rev-parse --short HEAD)  # e.g., ce97912

# Comment 1: ต้องแก้ไข (comment_id: 123)
# ใช้ heredoc เพื่อป้องกัน shell injection
gh api repos/owner/repo/pulls/42/comments/123/replies \
  -f body="Fixed in $COMMIT_HASH! Changed context.Background() to context.WithTimeout(ctx, 30*time.Second)"

# Comment 2: ไม่แก้ไข (comment_id: 124)
gh api repos/owner/repo/pulls/42/comments/124/replies \
  -f body="Good point! However, I kept this approach because..."

# Comment 3: คำถาม (comment_id: 125)
gh api repos/owner/repo/pulls/42/comments/125/replies \
  -f body="Yes, this handles the edge case by..."

# Comment 4: Defer - สร้าง issue ก่อน แล้ว reply (comment_id: 126)
DEFER_ISSUE=$(gh issue create \
  --title "test: add unit tests for auth handler" \
  --label "enhancement" \
  --body "From PR #42 review by @senior-dev..." \
  --json number -q .number)

gh api repos/owner/repo/pulls/42/comments/126/replies \
  -f body="Thanks for the feedback! Created #$DEFER_ISSUE to track this work."
```

### Step 7: Update Related Issues

```bash
# Get linked issues from PR
ISSUES=$(gh pr view --json closingIssuesReferences --jq '.closingIssuesReferences[].number')

# For each issue, add progress comment
for ISSUE in $ISSUES; do
  gh issue comment $ISSUE --body "## PR Review Progress

### Review Status: [status]

### Changes Made from Review
- [list of changes made]

### Pending Items
- [if any]

### Next Steps
- [what happens next]"
done
```

### Step 8: Create Learning Document

สร้าง learning document จาก review:

```bash
# Create learning file
TIMESTAMP=$(TZ='Asia/Bangkok' date '+%H.%M')
DATE_PATH=$(TZ='Asia/Bangkok' date '+%Y-%m/%d')
mkdir -p docs/learnings/$DATE_PATH
```

**Template:**

```markdown
---
type: review-learning
source: PR #[number]
reviewers: [@reviewer1, @reviewer2]
tags: [relevant-tags]
---

# [Title based on main feedback theme]

## Key Insights from Review

### What Reviewers Caught
- [issue 1]: [what was wrong and why]
- [issue 2]: [what was wrong and why]

### Patterns to Remember
- **Do**: [good practice learned]
- **Don't**: [anti-pattern identified]

## Code Examples

### Before (What I wrote)
```[lang]
[original code]
```

### After (Improved version)
```[lang]
[fixed code]
```

## Why This Matters
[explanation of why reviewer's suggestion is better]

## Apply To
- [future scenario 1]
- [future scenario 2]

## Related
- PR: [url]
- Issue: [url if any]
```

### Step 9: Auto-Resolve Addressed Comments

After addressing each comment, resolve the review thread to mark it as done:

```bash
# Get thread ID from comment ID using GraphQL (with pagination)
get_thread_id() {
    local pr_number="$1"
    local owner="${REPO%%/*}"
    local repo="${REPO##*/}"
    local cursor=""
    local all_threads="[]"

    # Paginate through all review threads
    while true; do
        local cursor_arg=""
        if [[ -n "$cursor" && "$cursor" != "null" ]]; then
            cursor_arg="-f cursor=$cursor"
        fi

        # shellcheck disable=SC2086
        local result=$(gh api graphql -f query='
            query($owner: String!, $repo: String!, $pr: Int!, $cursor: String) {
                repository(owner: $owner, name: $repo) {
                    pullRequest(number: $pr) {
                        reviewThreads(first: 100, after: $cursor) {
                            pageInfo {
                                hasNextPage
                                endCursor
                            }
                            nodes {
                                id
                                isResolved
                                comments(first: 1) {
                                    nodes {
                                        id
                                        databaseId
                                    }
                                }
                            }
                        }
                    }
                }
            }
        ' -f owner="$owner" -f repo="$repo" -F pr="$pr_number" $cursor_arg)

        # Accumulate threads with null-safe handling
        local page_threads=$(echo "$result" | jq '.data.repository.pullRequest.reviewThreads.nodes // []')
        all_threads=$(jq -n --argjson all "$all_threads" --argjson page "$page_threads" '$all + $page')

        # Check for more pages
        local has_next=$(echo "$result" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.hasNextPage')
        cursor=$(echo "$result" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.endCursor')

        if [[ "$has_next" != "true" || -z "$cursor" || "$cursor" == "null" ]]; then
            break
        fi
    done

    echo "$all_threads"
}

# Resolve a specific thread
resolve_thread() {
    local thread_id="$1"

    gh api graphql -f query='
        mutation($threadId: ID!) {
            resolveReviewThread(input: {threadId: $threadId}) {
                thread {
                    id
                    isResolved
                }
            }
        }
    ' -f threadId="$thread_id"
}
```

**When to resolve:**
- After replying with "Fixed in [commit]" - resolve the thread
- After answering a question satisfactorily - resolve the thread
- After explaining why not changing - resolve the thread
- After creating a defer issue - resolve the thread

**Do NOT resolve:**
- If reviewer needs to verify the fix
- If there's ongoing discussion
- If the comment is a blocking concern

**Example - Resolve after addressing:**

```bash
# 1. First, reply to the comment
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -f body="Fixed in abc1234! Changed to use context.WithTimeout"

# 2. Then resolve the thread
# Find thread_id that contains comment_id, then:
gh api graphql -f query='
    mutation($threadId: ID!) {
        resolveReviewThread(input: {threadId: $threadId}) {
            thread { isResolved }
        }
    }
' -f threadId="THREAD_ID_HERE"

echo "Thread resolved"
```

### Step 10: Push Changes

```bash
# Stage any remaining changes (learning docs, etc.)
git add -A

# Commit remaining changes if any
if ! git diff --cached --quiet; then
  git commit -m "docs: add learning from PR review

Responds to review by @[reviewer]"
fi

# Push all commits to update PR
git push
```

**หมายเหตุ:** Code fixes ถูก commit ไปแล้วใน Step 6.1 พร้อม hash ที่ใช้ใน reply

### Step 11: Final Summary

แสดงสรุปการทำงาน:

```markdown
## PR Review Complete

### PR: #[number] - [title]
**Reviewer**: @[reviewer] ([reviewer_type: human/copilot])

### Actions Taken
| Comment | Action | Status | Thread |
|---------|--------|--------|--------|
| [comment 1] | Fixed | Done | Resolved |
| [comment 2] | Replied | Done | Resolved |
| [comment 3] | Deferred → #[issue] | Done | Resolved |

### Summary Statistics
- Total comments: [N]
- Fixed: [N]
- Replied: [N]
- Deferred: [N]
- Threads resolved: [N]/[N]

### Deferred Items (Issues Created)
| Issue | Title | From Comment |
|-------|-------|--------------|
| #[number] | [title] | @[reviewer] on [file:line] |

### Files Modified
- [file1]: [change description]
- [file2]: [change description]

### Learning Document
Created: `docs/learnings/[path]/[filename].md`

### Next Steps
- [ ] Wait for reviewer to re-review
- [ ] Address any follow-up comments
- [ ] Merge when approved
- [ ] Work on deferred issues: #[number], #[number]

### Commands
- `gh pr view` - View PR status
- `/pr-review` - Run again if new comments
```

---

## Example Session

```bash
# User runs
/pr-review

# Output
## Checking PRs...

Found 1 open PR with reviews:

## PR #42: Add user authentication feature

**URL**: https://github.com/owner/repo/pull/42
**Review Status**: CHANGES_REQUESTED

### Review Comments (4)

1. 🔴 **@senior-dev** on `auth/handler.go:45`:
   > Consider using context.WithTimeout instead of context.Background()

2. 🟡 **@senior-dev** on `auth/handler.go:78`:
   > This error message could be more descriptive

3. 🟠 **@senior-dev** on `auth/handler.go:90`:
   > Missing unit tests for this handler

4. ✅ **@senior-dev** general:
   > Nice clean implementation overall!

### Processing...

#### Comment 1: Context timeout
- Status: **Fixed**
- Changed `context.Background()` to `context.WithTimeout(ctx, 30*time.Second)`
- Commit: `ce97912`
- Replied: "Fixed in ce97912! Added 30-second timeout for database operations"

#### Comment 2: Error message
- Status: **Fixed**
- Updated error message to include user ID and operation
- Commit: `ce97912` *(same commit as Comment 1 - both fixes were made together)*
- Replied: "Fixed in ce97912! Error now includes: user ID, operation type, and original error"

#### Comment 3: Missing tests
- Status: **Deferred**
- Created issue: #45 "test: add unit tests for auth handler"
- Replied: "Thanks for the feedback! Created #45 to track this work."

#### Comment 4: Praise
- Status: **Acknowledged**
- Replied: "Thank you! Appreciate the review"

### Deferred Items
| Issue | Title |
|-------|-------|
| #45 | test: add unit tests for auth handler |

### Learning Document Created
`docs/learnings/2026-01/08/14.30_context-timeout-best-practice.md`

### Pushed to Remote
All commits pushed successfully.

### Issue Updated
Added progress comment to Issue #38

## Done! Waiting for re-review.
```

---

## Handling Copilot Reviews

GitHub Copilot reviews are automatically triggered on PRs. They have some differences from human reviews:

### Detection

```bash
# Check if reviewer is Copilot
COPILOT_REVIEWER="copilot-pull-request-reviewer"

if [[ "$reviewer" == "$COPILOT_REVIEWER" ]]; then
    echo "This is a Copilot review"
fi
```

### Key Differences

| Aspect | Human Review | Copilot Review |
|--------|-------------|----------------|
| Review State | APPROVED, CHANGES_REQUESTED, COMMENTED | Usually COMMENTED |
| Response Time | Can wait | Can be processed immediately |
| Thread Resolution | Ask reviewer first | Can auto-resolve after fixing |
| Learning Value | High (contextual) | Medium (pattern-based) |

### Processing Copilot Comments

1. **All Copilot comments can be auto-resolved** after addressing
2. **No need to wait for re-review** - Copilot will review again on next push
3. **Batch process** - Fix all comments, then resolve all threads

```bash
# After fixing all Copilot comments:
# 1. Commit all fixes
git add -A
git commit -m "fix: address Copilot review comments"

# 2. Resolve all Copilot threads (with pagination for >100 threads)
resolve_all_copilot_threads() {
    local pr_number="$1"
    local cursor=""
    local owner="${REPO%%/*}"
    local repo="${REPO##*/}"

    while true; do
        local cursor_arg=""
        if [[ -n "$cursor" && "$cursor" != "null" ]]; then
            cursor_arg="-f cursor=$cursor"
        fi

        # shellcheck disable=SC2086
        local result=$(gh api graphql -f query='
            query($owner: String!, $repo: String!, $pr: Int!, $cursor: String) {
                repository(owner: $owner, name: $repo) {
                    pullRequest(number: $pr) {
                        reviewThreads(first: 100, after: $cursor) {
                            pageInfo {
                                hasNextPage
                                endCursor
                            }
                            nodes {
                                id
                                isResolved
                                comments(first: 1) {
                                    nodes {
                                        author { login }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        ' -f owner="$owner" -f repo="$repo" -F pr="$pr_number" $cursor_arg)

        # Resolve unresolved Copilot threads in this page
        echo "$result" | jq -r '
            .data.repository.pullRequest.reviewThreads.nodes[] |
            select(.isResolved == false) |
            select(.comments.nodes[0]?.author?.login == "copilot-pull-request-reviewer") |
            .id
        ' | while read -r thread_id; do
            [[ -z "$thread_id" ]] && continue
            gh api graphql -f query='
                mutation($threadId: ID!) {
                    resolveReviewThread(input: {threadId: $threadId}) {
                        thread { isResolved }
                    }
                }
            ' -f threadId="$thread_id"
        done

        # Check for more pages
        local has_next=$(echo "$result" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.hasNextPage')
        cursor=$(echo "$result" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.endCursor')

        if [[ "$has_next" != "true" || -z "$cursor" || "$cursor" == "null" ]]; then
            break
        fi
    done
}

resolve_all_copilot_threads "$pr_number"

# 3. Push to trigger new Copilot review
git push
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No PRs found | Check `gh auth status` and repo access |
| Can't reply to comment | Check write permissions on repo |
| API rate limit | Wait or use `gh auth refresh` |

---

## Related Commands

| Command | Purpose |
|---------|---------|
| `/td` | Create PR after task completion |
| `/commit` | Atomic commits |
| `/mem` | Quick knowledge capture |
| `/review` | Local code review before push |
| `/pr-poll` | Start PR review polling daemon |
