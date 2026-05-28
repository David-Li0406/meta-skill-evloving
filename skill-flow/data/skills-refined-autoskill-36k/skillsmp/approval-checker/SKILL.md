---
name: approval-checker
description: Verifies that an authorized user has approved the fix plan before proceeding with implementation.
---

## Purpose

Check for:
1. Thumbs-up (👍) reaction on plan comment
2. "Approve" keyword in reply comments
3. User is authorized (maintainer/admin)

Only authorized approvals count - ignore others safely.

## Usage

Include this file when checking approval:

```
Use lib/approval-checker to verify approval before implementing
```

## Authorization

### Who Can Approve?

Users with **push** or **admin** permissions on the repository.

```bash
gh api repos/{owner}/{repo}/collaborators \
  --jq '[.[] | select(.permissions.push == true or .permissions.admin == true) | .login]'
```

**Example output:**
```json
["alice", "bob", "charlie"]
```

These are the authorized approvers.

### Why This Matters

Security: Prevents unauthorized code changes.

**Scenario:**
- External contributor comments "approve" → Ignored (not authorized)
- Repository maintainer clicks 👍 → Accepted (authorized)

## Approval Methods

### Method 1: Thumbs Up Reaction (👍)

User clicks thumbs-up on the plan comment.

**Check:**
```bash
# Get plan comment ID from previous step
COMMENT_ID=<plan-comment-id>

# Fetch reactions
gh api repos/{owner}/{repo}/issues/comments/${COMMENT_ID}/reactions \
  --jq '.[] | select(.content == "+1") | .user.login'
```

**Output:** List of usernames who reacted with 👍

**Logic:**
```python
reactions = get_thumbs_up_reactions(comment_id)
authorized = get_authorized_users()

for user in reactions:
    if user in authorized:
        return {"approved": True, "approver": user, "method": "reaction"}

return {"approved": False}
```

### Method 2: Approval Comment

User replies with "approve", "approved", "lgtm", or "go ahead" (case-insensitive).

**Check:**
```bash
# Get all comments after the plan was posted
PLAN_TIMESTAMP="2026-01-16T10:00:00Z"

gh issue view <issue-number> --json comments \
  --jq '.comments[] | select(.createdAt > "'$PLAN_TIMESTAMP'") | {author: .author.login, body: .body}'
```

**Output:** Recent comments with author and body

**Logic:**
```python
import re

approval_keywords = ["approve", "approved", "lgtm", "go ahead"]
pattern = re.compile(r'\b(' + '|'.join(approval_keywords) + r')\b', re.IGNORECASE)

comments = get_comments_after(plan_timestamp)
authorized = get_authorized_users()

for comment in comments:
    if comment.author in authorized:
        if pattern.search(comment.body):
            return {"approved": True, "approver": comment.author, "method": "comment"}

return {"approved": False}
```

## Implementation Steps

### Step 1: Get Repository Info

```bash
# Extract owner and repo from git remote
REMOTE=$(git remote get-url origin)
# Parse: https://github.com/owner/repo.git or git@github.com:owner/repo.git

OWNER=$(echo $REMOTE | sed -E 's/.*github\.com[:/]([^/]+).*/\1/')
REPO=$(echo $REMOTE | sed -E 's/.*github\.com[:/][^/]+\/([^.]+).*/\1/')
```

### Step 2: Get Authorized Users

```bash
gh api repos/${OWNER}/${REPO}/collaborators \
  --jq '[.[] | select(.permissions.push == true or .permissions.admin == true) | .login]' \
  > /tmp/authorized_users.json
```

### Step 3: Find Plan Comment

```bash
gh issue view <issue-number> --json comments \
  --jq '.comments[] | select(.body | contains("🤖 Automated Fix Plan")) | {id: .id, createdAt: .createdAt}'
```

**Output:**
```json
{
  "id": "IC_kwDOA...",
  "createdAt": "2026-01-16T10:00:00Z"
}
```

### Step 4: Check Method 1 (Reactions)

```bash
COMMENT_ID="IC_kwDOA..."

gh api repos/${OWNER}/${REPO}/issues/comments/${COMMENT_ID}/reactions \
  --jq '.[] | select(.content == "+1") | .user.login' \
  > /tmp/reactions.txt
```

Check if any reactor is in authorized users:

```bash
while read user; do
  if grep -q "\"$user\"" /tmp/authorized_users.json; then
    echo "APPROVED by $user via reaction"
    exit 0
  fi
done < /tmp/reactions.txt
```

### Step 5: Check Method 2 (Comments)

```bash
PLAN_TIMESTAMP="2026-01-16T10:00:00Z"

gh issue view <issue-number> --json comments \
  --jq '.comments[] | select(.createdAt > "'$PLAN_TIMESTAMP'") | {author: .author.login, body: .body}' \
  > /tmp/recent_comments.json
```

Check for approval keywords from authorized users:

```bash
jq -r '.[] | "\(.author)|\(.body)"' /tmp/recent_comments.json | while IFS='|' read author body; do
  # Check if author is authorized
  if grep -q "\"$author\"" /tmp/authorized_users.json; then
    # Check for approval keywords (case-insensitive)
    if echo "$body" | grep -iE '\b(approve|approved|lgtm|go ahead)\b' > /dev/null; then
      echo "APPROVED by $author via comment"
      exit 0
    fi
  fi
done
```

### Step 6: Not Approved Response

If no approval found after checking both methods:

```bash
gh issue comment <issue-number> --body "⚠️ **Approval Required**

No approval detected yet. To proceed:
- 👍 Add thumbs up reaction to the plan comment above, OR
- 💬 Reply with 'approve' or 'lgtm'

Note: Only repository maintainers can approve.

Current authorized approvers: $(cat /tmp/authorized_users.json | jq -r '.[] | "@" + .')"
```

**Example output:**
```
⚠️ **Approval Required**

No approval detected yet. To proceed:
- 👍 Add thumbs up reaction to the plan comment above, OR
- 💬 Reply with 'approve' or 'lgtm'

Note: Only repository maintainers can approve.

Current authorized approvers: @alice @bob @charlie
```

## Output Format

Return approval status:

```json
{
  "approved": true,
  "approver": "alice",
  "method": "reaction",
  "timestamp": "2026-01-16T10:05:00Z"
}
```

Or:

```json
{
  "approved": false,
  "reason": "No approval from authorized users",
  "authorized_users": ["alice", "bob", "charlie"]
}
```

## Error Handling

### GitHub API Error

```bash
gh api repos/${OWNER}/${REPO}/collaborators 2>&1
```

If fails:

```markdown
⚠️ **Approval Check Failed**

Couldn't verify approval due to API error:
\`\`\`
<error message>
\`\`\`

**Troubleshooting:**
1. Check GitHub CLI authentication: \`gh auth status\`
2. Verify repository access: \`gh repo view ${OWNER}/${REPO}\`
3. Try again: \`/continue-issue <issue-number>\`

If error persists, you can implement the plan manually.
```

### Plan Comment Not Found

```markdown
⚠️ **Plan Comment Not Found**

Couldn't find the automated fix plan comment on this issue.

Did you run \`/handle-issue <issue-number>\` first?

**To proceed:**
1. Run \`/handle-issue <issue-number>\` to generate plan
2. Review and approve the plan
3. Run \`/continue-issue <issue-number>\`
```

### Multiple Approvals

If multiple authorized users approve:

```python
# Use first approval found (earliest timestamp)
approvals.sort(key=lambda x: x.timestamp)
return approvals[0]
```

## Integration with continue-issue

```markdown
1. Parse issue number
2. Check approval (lib/approval-checker) ← YOU ARE HERE
3. If approved → Create worktree → Implement
4. If not approved → Post helpful message → Exit
```

**Flow:**
```
/continue-issue 42
    ↓
Get authorized users from GitHub
    ↓
Find plan comment
    ↓
Check reactions (Method 1)
    ↓
    ├─ Approved → Proceed
    └─ Not approved
        ↓
    Check comments (Method 2)
        ↓
        ├─ Approved → Proceed
        └─ Not approved → Post message → Exit
```

## Security Considerations

**No bypass mechanisms:**
- Can't override with flags
- Can't skip check
- Can't fake authorization

**Safe handling of unknowns:**
- Unknown users → Ignored
- Partial approval → Not sufficient
- Ambiguous comments → Not approved

**Principle:** Fail closed, not open.

## Testing Approach

**Test cases:**
1. ✅ Authorized user reacts 👍 → Approved
2. ✅ Authorized user comments "approve" → Approved
3. ✅ Authorized user comments "LGTM" → Approved
4. ❌ Unauthorized user reacts 👍 → Not approved
5. ❌ Unauthorized user comments "approve" → Not approved
6. ❌ Authorized user comments "looks good" → Not approved (no keyword)
7. ✅ Multiple approvals → Use first one
8. ❌ GitHub API error → Fail gracefully with message

## YAGNI Notes

**Not included:**
- Multi-level approval (single maintainer sufficient)
- Approval expiration (valid until revoked)
- Approval delegation (direct authorization only)
- Vote counting (single approval sufficient)

Keep it simple: one authorized approval proceeds.
