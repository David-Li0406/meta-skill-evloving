# Detailed Workflow Reference

This document provides step-by-step instructions for processing PR review comments.

## Complete Workflow

### Step 1: Initialize Session

Before processing comments, gather essential information:

```bash
# Get PR details
gh pr view <NUMBER> --json number,title,headRefName,baseRefName,url

# Ensure on correct branch
git checkout <headRefName>
git pull origin <headRefName>
```

### Step 2: Fetch All Review Comments

Retrieve unresolved review threads:

```bash
gh pr view <NUMBER> --json reviewThreads --jq '
  [.reviewThreads[] | select(.isResolved == false) | {
    id: .id,
    path: .path,
    line: .line,
    comments: [.comments[] | {
      id: .id,
      author: .author.login,
      body: .body,
      createdAt: .createdAt
    }]
  }]
'
```

### Step 3: Build Comment Queue

Organize comments for processing:

```
Queue Structure:
[
  {
    threadId: "thread-1",
    filePath: "src/auth.ts",
    lineNumber: 42,
    originalComment: "Add null check here",
    author: "reviewer1",
    status: "pending"  // pending | processing | fixed | skipped | uncertain
  },
  ...
]
```

### Step 4: Process Each Comment

For each comment in the queue:

#### 4.1 Read Context

Use the **Read tool** to read file contents:

```
Read file: <filePath>

# For specific line ranges, use offset and limit parameters:
Read file: <filePath> (offset: <start>, limit: <count>)
```

> **Note:** In Claude Code, always use the Read tool instead of bash commands like `cat` or `sed` for reading files. The Read tool provides better integration and avoids permission issues.

#### 4.2 Analyze Comment

**First, critically evaluate whether the comment is correct:**

| Verification Check | Questions to Ask |
|-------------------|------------------|
| Technical accuracy | Is the suggestion based on correct understanding of the code? |
| Architecture fit | Does it align with existing patterns and design principles? |
| Side effects | Would implementing this introduce bugs or break other code? |
| Context awareness | Does the reviewer have full context of the implementation? |

**Then determine action based on assessment:**

| Comment Type | Example | Action |
|--------------|---------|--------|
| Valid bug fix | "This will throw if x is null" (verified true) | Fix and commit |
| Valid style suggestion | "Use const instead of let" | Fix and commit |
| Question | "Why is this needed?" | Reply with explanation |
| Design discussion | "Should this be a class?" | Ask user |
| Already done | "Add logging" (logging exists) | Reply explaining it's done |
| Out of scope | "Refactor entire module" | Reply explaining scope |
| **Incorrect suggestion** | "Add null check" (but value is guaranteed non-null) | Politely disagree with evidence |
| **Would introduce bug** | "Remove this validation" (validation is necessary) | Explain why change is problematic |
| **Misunderstands architecture** | "Use pattern X" (conflicts with existing design) | Explain architectural constraints |

#### 4.3 Execute Fix (if needed)

```bash
# Make changes to file
# (Use Edit tool or manual editing)

# Stage changes
git add <filePath>

# Commit with descriptive message (describe the change, not the comment)
git commit -m "fix(<scope>): <description>

<why this change was needed - optional>"

# Get commit info for reply
COMMIT_HASH=$(git rev-parse --short HEAD)
COMMIT_URL="https://github.com/<owner>/<repo>/commit/$(git rev-parse HEAD)"
```

#### 4.4 Push Changes

```bash
git push origin <branchName>
```

### Step 5: Reply and Resolve

#### Using GraphQL API

```bash
# Add reply comment
gh api graphql -f query='
  mutation($body: String!, $threadId: ID!) {
    addPullRequestReviewThreadReply(input: {
      pullRequestReviewThreadId: $threadId,
      body: $body
    }) {
      comment { id }
    }
  }
' -f threadId="<THREAD_ID>" -f body="<REPLY_BODY>"

# Resolve the thread
gh api graphql -f query='
  mutation($threadId: ID!) {
    resolveReviewThread(input: {
      threadId: $threadId
    }) {
      thread { isResolved }
    }
  }
' -f threadId="<THREAD_ID>"
```

### Step 6: Commit by Topic

**Principle:** Group commits by **logical change**, not by comment count.

#### Same topic → One commit, multiple replies

```
Comment A (thread-1): "Add null check for session"
Comment B (thread-3): "Session might be undefined"
Comment C (thread-5): "Handle missing session"

All three are about session null safety → ONE topic

Action:
1. Implement session null check
2. Commit: "fix(auth): add null check for user session"
3. Reply to thread-1, thread-3, thread-5 with same commit link
4. Resolve all three
```

#### Different topics → Separate commits

```
Comment A (thread-1): "Add input validation"
Comment B (thread-3): "Improve performance"
Comment C (thread-5): "Fix typo in error message"

Three different concerns → THREE commits

Action:
1. Fix A → Commit "fix(form): add input validation" → Reply thread-1
2. Fix B → Commit "perf(query): optimize database call" → Reply thread-3
3. Fix C → Commit "fix(error): correct typo in message" → Reply thread-5
```

#### Decision guide

| Question | If Yes | If No |
|----------|--------|-------|
| Same logical change? | One commit | Separate commits |
| Can be reverted independently? | Separate commits | Consider grouping |
| Different code areas but same topic? | One commit | - |

## Interactive Mode Flow

```
┌────────────────────────────────────────────────────────────┐
│                    INTERACTIVE MODE                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  For each comment:                                         │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Comment #1 of 5                                       │ │
│  │ File: src/auth.ts:42                                  │ │
│  │ Author: @reviewer                                     │ │
│  │                                                       │ │
│  │ "Consider adding a null check for the session        │ │
│  │  object before accessing its properties"             │ │
│  │                                                       │ │
│  │ Analysis: Session is guaranteed non-null by          │ │
│  │ middleware. Adding check would be redundant.         │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  Options:                                                  │
│  [1] Fix this issue (comment is valid)                     │
│  [2] No fix needed (already addressed/out of scope)        │
│  [3] Disagree (comment is incorrect - explain why)         │
│  [4] Skip for now                                          │
│  [5] Discuss with user (need clarification)                │
│                                                            │
│  User selects → Execute → Next comment                     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Auto Mode Flow

```
┌────────────────────────────────────────────────────────────┐
│                      AUTO MODE                              │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Processing 6 comments automatically...                    │
│                                                            │
│  [1/6] src/auth.ts:42 - Null check                        │
│        → Verifying... Comment is valid                     │
│        → Fixing... Done                                    │
│        → Committed: abc1234                                │
│        → Replied and resolved ✓                            │
│                                                            │
│  [2/6] src/api.ts:87 - Error handling                     │
│        → Verifying... Comment is valid                     │
│        → Fixing... Done                                    │
│        → Committed: def5678                                │
│        → Replied and resolved ✓                            │
│                                                            │
│  [3/6] src/utils.ts:15 - "Why this approach?"             │
│        → Analyzing... Question, no fix needed              │
│        → Replied with explanation ✓                        │
│        → Resolved ✓                                        │
│                                                            │
│  [4/6] src/config.ts:33 - Ambiguous request               │
│        → PAUSED: Need user input                           │
│        → [Asking user for clarification...]                │
│                                                            │
│  [5/6] src/db.ts:99 - "Remove this validation"            │
│        → Verifying... DISAGREE - would introduce bug       │
│        → PAUSED: Reviewer suggestion may be incorrect      │
│        → [Presenting analysis to user...]                  │
│                                                            │
│  [6/6] Waiting...                                          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

> **Note:** In Auto Mode, the system will automatically PAUSE and ask for user confirmation when:
> - The comment is ambiguous or unclear
> - **The comment appears to be incorrect or would introduce issues**
>
> Auto Mode will NEVER auto-reply disagreements without user approval.

## Edge Cases

### Incorrect or Harmful Suggestions

When you determine a reviewer's suggestion is technically incorrect:

1. **Verify your assessment thoroughly**
   - Read the surrounding code context
   - Check if there are edge cases the reviewer might be considering
   - Understand why the reviewer might have made this suggestion

2. **Document your reasoning**
   - What specifically is incorrect about the suggestion?
   - What evidence from the codebase supports your position?
   - What would happen if the suggestion were implemented?

3. **Present to user before responding**
   - Explain your analysis to the user
   - Let them decide whether to push back or defer to the reviewer

4. **Respond politely with evidence**
   - Acknowledge the reviewer's concern
   - Explain the technical reasons for disagreement
   - Provide code references or examples
   - Offer to discuss further

5. **Do NOT auto-resolve**
   - Leave the thread open for the reviewer to respond
   - Only resolve after reaching consensus or user instruction

### Comment on Deleted Lines

If the comment references lines that no longer exist:

1. Check git history to understand context
2. Determine if the issue is already resolved by recent changes
3. Reply explaining the situation
4. Resolve with appropriate explanation

### Conflicting Comments

When two reviewers give contradictory feedback:

1. Do NOT attempt to resolve automatically
2. Present both comments to user
3. Ask for direction
4. Proceed only after clarification

### Large Refactoring Requests

When a comment suggests extensive changes:

1. Acknowledge the suggestion
2. Explain it's out of scope for this PR
3. Offer to create a follow-up issue
4. Resolve with the explanation

## Verification Checklist

Before resolving each comment:

- [ ] Fix is correct and complete
- [ ] Code compiles without errors
- [ ] Linting passes (if configured)
- [ ] Commit message is descriptive
- [ ] Changes are pushed to remote
- [ ] Reply includes commit link
- [ ] Reply explains the change

## Recovery from Errors

### Commit Failed

```bash
# Check status
git status

# If staged files have issues, fix them
# Then retry commit
git commit -m "..."
```

### Push Failed

```bash
# Pull latest changes
git pull origin <branch> --rebase

# Resolve any conflicts
# Then push again
git push origin <branch>
```

### GraphQL API Error

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Re-authenticate with `gh auth login` |
| 404 Not Found | Wrong thread ID | Re-fetch thread IDs |
| 422 Unprocessable | Thread already resolved | Skip to next comment |
