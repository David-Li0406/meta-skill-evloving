---
name: pr-management
description: "Use when addressing PR review feedback, resolving review threads, replying to comments, or consolidating multiple PRs/branches. Covers the complete PR review lifecycle from feedback collection through thread resolution and branch integration."
---

# PR Management Skill

Procedural knowledge for managing pull request reviews, threads, and branch consolidation using GitHub PR review tools.

## Core MCP Tools

### Thread Discovery

```javascript
// Get all review threads for a PR
get_pull_request_threads({
  owner: "org-name",
  repo: "repo-name",
  pull_number: 123,
});
```

Returns: Thread IDs, status (resolved/unresolved), file paths, line numbers, and comment content.

### Replying to Comments

```javascript
// Reply to a specific comment in a thread
reply_to_pull_request_comment({
  owner: "org-name",
  repo: "repo-name",
  pull_number: 123,
  comment_id: "PRRC_kwDOP3aAEM5knHc7",
  body: "Fixed in commit abc1234. Replaced the nested callback with async/await.",
});
```

**Important**: Use the comment ID from the thread, not the thread ID. Reply to the latest comment in a thread to maintain conversation flow.

### Resolving Threads

```javascript
// Resolve a thread after addressing feedback
resolve_pull_request_review_thread({
  thread_id: "PRRT_kwDOP3aAEM5knHc7",
});
```

**Note**: Thread IDs typically start with `PRRT_`, comment IDs with `PRRC_`.

### Checking Resolution Status

```javascript
// Verify thread resolution status
check_pull_request_review_resolution({
  owner: "org-name",
  repo: "repo-name",
  pull_number: 123,
});
```

Use after batch resolutions to confirm all intended threads were resolved.

---

## Workflow 1: Addressing PR Feedback

### Step 1: Collect All Feedback

1. Use `get_pull_request_threads` to fetch all review threads
2. Check CI status for build/test failures
3. Review CodeQL or security scan findings if present
4. Note pending comments that haven't been submitted yet

### Step 2: Categorize Feedback

| Category    | Description             | Action Required        |
| ----------- | ----------------------- | ---------------------- |
| Blocking    | Must fix before merge   | Implement fix          |
| Improvement | Should fix, better code | Implement fix          |
| Question    | Needs clarification     | Reply with explanation |
| Suggestion  | Optional enhancement    | Consider or defer      |
| CI Failure  | Build/test broken       | Fix immediately        |

### Step 3: Implement Fixes Locally

For each blocking/improvement item:

1. Make the code change
2. Run relevant tests
3. Verify the fix addresses the feedback
4. **Do NOT commit yet** — batch all fixes together

### Step 4: Prepare Responses

Draft replies for each thread before posting. Match the response type:

| Situation | Reply Template                                                  |
| --------- | --------------------------------------------------------------- |
| Fixed     | "Fixed in commit {sha} — {brief description}."                  |
| Explained | "This is intentional because {reason}. {justification}."        |
| Deferred  | "Created issue #{num} to track this. Out of scope for this PR." |
| Declined  | "Respectfully declining because {reason}. Happy to discuss."    |
| Outdated  | "This code was removed/refactored in {commit}."                 |

### Step 5: Commit, Reply, Resolve

After user confirms:

1. Commit and push all fixes in one commit
2. Reply to each thread using `reply_to_pull_request_comment`
3. Resolve fixed threads using `resolve_pull_request_review_thread`
4. Verify resolution with `check_pull_request_review_resolution`

---

## Workflow 2: Resolving Review Threads

### Resolution Decision Matrix

| Thread Type             | Action                          |
| ----------------------- | ------------------------------- |
| Code fixed              | ✅ Reply then resolve           |
| Question answered       | ✅ Reply then resolve           |
| Design explained        | 💬 Reply only (reviewer closes) |
| Deferred to issue       | 💬 Reply only                   |
| Disagreement            | 💬 Reply only (discuss further) |
| Outdated (code removed) | ✅ Reply then resolve           |

### Resolution Procedure

```
FOR each unresolved thread:
    1. Verify the feedback was addressed (check diff, run tests)
    2. Craft appropriate reply with commit reference
    3. Post reply via reply_to_pull_request_comment
    4. IF thread is resolvable (fixed/answered/outdated):
           resolve via resolve_pull_request_review_thread
    5. IF design discussion or disagreement:
           Leave open for reviewer to close
```

### Batch Resolution Example

```javascript
// 1. Get threads
const threads = await get_pull_request_threads({
  owner: "myorg",
  repo: "myrepo",
  pull_number: 42,
});

// 2. Reply to fixed thread
await reply_to_pull_request_comment({
  owner: "myorg",
  repo: "myrepo",
  pull_number: 42,
  comment_id: "PRRC_kwDOP3aAEM5knHc7",
  body: "Fixed in commit 186e28a. Replaced setTimeout with requestAnimationFrame.",
});

// 3. Resolve the thread
await resolve_pull_request_review_thread({
  thread_id: "PRRT_kwDOP3aAEM5knHc7",
});

// 4. Reply to design question (don't resolve)
await reply_to_pull_request_comment({
  owner: "myorg",
  repo: "myrepo",
  pull_number: 42,
  comment_id: "PRRC_kwDOP3aAEM5knHco",
  body: "The current approach optimizes by checking sort_order before updating. A batch API would require interface changes beyond this PR's scope.",
});

// 5. Verify all resolutions
await check_pull_request_review_resolution({
  owner: "myorg",
  repo: "myrepo",
  pull_number: 42,
});
```

---

## Workflow 3: Consolidating PRs/Branches

### Use Cases

- **Overlapping PRs**: Two PRs with similar scope → combine into one
- **Dependent PRs**: PR depends on another open PR → integrate for unified review
- **Agent branches**: Multiple agents worked on related branches → merge together

### Consolidation Procedure

```bash
# 1. Fetch all source branches
git fetch origin pull/123/head:pr-123
git fetch origin pull/456/head:pr-456

# 2. Create integration branch (if on protected branch)
git checkout -b integration/feature-combined

# 3. Merge each source (no auto-commit for inspection)
git merge pr-123 --no-commit -m "Integrate PR #123"
git merge pr-456 --no-commit -m "Integrate PR #456"

# 4. Resolve any conflicts
git diff --name-only --diff-filter=U  # List conflicts
# ... resolve conflicts ...

# 5. Commit the integration
git commit -m "Consolidate: Feature X

This branch integrates:
- PR #123: Add authentication
- PR #456: Add login UI

Closes #123
Closes #456"
```

### Conflict Resolution Strategy

1. **Identify conflict type**:
   - Both sides add to same location → combine additions
   - Both sides modify same code → understand intent, merge logic
   - Dependency version conflicts → use higher version (usually)

2. **Preserve all work** — goal is to combine, not discard

3. **Test after resolution** — run tests to verify combined code works

### Target Branch Selection

```
IF on protected branch (main/master/develop):
    Create new: integration/{summary}-{timestamp}
ELSE (on feature branch):
    Use current branch as target
```

---

## Reply Templates

### Fixed Code

```
Fixed in commit {sha}.

{Brief description of the change made to address the feedback.}
```

### Explained Design Decision

```
This is intentional because {reason}.

{Details about why the current approach was chosen.}
{Optional: reference to design doc or prior discussion.}
```

### Deferred to Issue

```
Good point. This is out of scope for this PR, but I've created #{issue_number} to track it.

We can address this in a follow-up.
```

### Declined with Rationale

```
I respectfully disagree with this suggestion because {reason}.

{Explanation of tradeoffs considered.}
{Offer to discuss further if needed.}
```

### Acknowledging Suggestion

```
Great suggestion! Implemented in commit {sha}.

{Brief note on how it improved the code.}
```

### Clarification Request

```
Could you clarify what you mean by "{quote from feedback}"?

I want to make sure I address your concern correctly. Are you suggesting {interpretation A} or {interpretation B}?
```

---

## Best Practices

### Before Resolving Threads

- [ ] Verify the fix is committed and pushed
- [ ] Run tests to confirm the fix works
- [ ] Reference the specific commit SHA in your reply
- [ ] Never resolve without replying first

### Reply Etiquette

- Be concise but complete
- Reference commit SHAs for traceability
- Acknowledge good suggestions graciously
- Explain disagreements professionally
- Ask clarifying questions before assuming intent

### Thread Management

- Reply to the latest comment in a thread
- Leave design discussions for the reviewer to close
- Batch related replies to avoid notification spam
- Use `check_pull_request_review_resolution` to verify state

### Branch Consolidation

- Always create a backup branch before merging
- Use `--no-commit` to inspect merges before committing
- Never force push or modify remote branches without confirmation
- Write descriptive commit messages listing all integrated sources
- Include `Closes #N` for each PR being consolidated

---

## Quick Reference

| Task                      | Tool/Command                                     |
| ------------------------- | ------------------------------------------------ |
| List all threads          | `get_pull_request_threads`                       |
| Reply to comment          | `reply_to_pull_request_comment`                  |
| Resolve thread            | `resolve_pull_request_review_thread`             |
| Check resolution status   | `check_pull_request_review_resolution`           |
| Fetch PR branch           | `git fetch origin pull/{n}/head:{local-branch}`  |
| View PR metadata          | `gh pr view {n} --json number,title,headRefName` |
| Merge without auto-commit | `git merge {branch} --no-commit`                 |
| List conflict files       | `git diff --name-only --diff-filter=U`           |
| Abort merge               | `git merge --abort`                              |

---

## Error Handling

### "Thread not found"

- Verify the thread ID format (should start with `PRRT_`)
- Refresh thread list with `get_pull_request_threads`
- Thread may have been deleted or already resolved

### "Comment not found"

- Verify the comment ID format (should start with `PRRC_`)
- Use the comment ID, not the thread ID, for replies
- Pending comments may not have IDs yet

### "Cannot resolve thread"

- Check if you have permission to resolve
- Some repos require the reviewer to resolve their own threads
- Thread may already be resolved

### Merge Conflicts

1. List conflicts: `git diff --name-only --diff-filter=U`
2. Open each file and look for conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
3. Resolve by editing to combine both changes
4. Stage resolved files: `git add {file}`
5. If stuck, abort: `git merge --abort`
