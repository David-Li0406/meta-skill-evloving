---
name: pr-review-comments
description: Fetches PR review comments from GitHub, batches similar comments together using semantic analysis, and walks through each batch one at a time with user confirmation between each. Tracks progress in REVIEW_COMMENT_WORK.md for resumability. Use when the user wants to address PR review feedback, fix review comments, or work through code review suggestions.
---

# PR Review Comments Skill

This skill helps you systematically work through PR review comments by batching similar ones together and addressing them one batch at a time with user feedback between each.

## Workflow Overview

1. Check if `REVIEW_COMMENT_WORK.md` exists in the current directory
2. If **resuming**: Read the work file and continue from where you left off
3. If **fresh start**: Fetch comments, analyze, batch, create work file, then begin
4. Work through batches ONE AT A TIME
5. After each batch: update work file, delete processed comment files, ask for feedback
6. WAIT for user response before proceeding to next batch

## Step 1: Check for Existing Work File

First, check if `REVIEW_COMMENT_WORK.md` exists in the current working directory:

```bash
ls -la REVIEW_COMMENT_WORK.md 2>/dev/null
```

- **If it exists**: Go to [Resuming Work](#resuming-work)
- **If it does not exist**: Go to [Fresh Start](#fresh-start)

---

## Fresh Start

### 1.1 Fetch PR Review Comments

Run the script to fetch unresolved PR review comments:

```bash
~/.pi/agent/skills/pr-review-comments/get_pr_review_comments
```

This will create individual `{comment-id}-review-feedback.md` files in the current directory.

### 1.2 Read All Comment Files

List all the generated comment files:

```bash
ls -la *-review-feedback.md 2>/dev/null
```

Each file contains:
- The file path and line number where the comment applies
- The review comment content
- Instructions for verification

### 1.3 Pre-analyze Comments for Validity (Use Parallel Tasks)

**Use the `task` tool to investigate comments in parallel.** Spawn a task for each comment file to analyze it independently. This significantly speeds up the triage process.

For each comment, the task should read the comment file, examine the relevant code and context, and determine:

- **Is it correct?** Does the suggestion actually apply? Is it based on a misunderstanding?
- **Is it appropriate for this PR?** Too minor? Too large/out of scope?
- **Is it already addressed?** Sometimes code has changed since the comment was made

Example task invocation:

```
task({
  tasks: [
    { description: "Analyze PR comment PRRC_abc-review-feedback.md: Read the comment file, examine the referenced code at [file:line], determine if the feedback is valid/applicable. Return: comment ID, file:line, issue summary, verdict (INCLUDE/QUESTIONABLE/EXCLUDE), and reasoning." },
    { description: "Analyze PR comment PRRC_def-review-feedback.md: Read the comment file, examine the referenced code at [file:line], determine if the feedback is valid/applicable. Return: comment ID, file:line, issue summary, verdict (INCLUDE/QUESTIONABLE/EXCLUDE), and reasoning." },
    // ... one task per comment file
  ]
})
```

Each task should classify its comment as:
- ✅ **INCLUDE**: Valid and should be addressed
- ⚠️ **QUESTIONABLE**: Might not be valid or appropriate (explain why)
- ❌ **EXCLUDE**: Incorrect or not applicable (explain why)

Collect results from all tasks before proceeding to batching.

### 1.4 Batch Comments by Semantic Similarity

Group **INCLUDE** comments into batches based on semantic similarity. Consider:

- Comments about the same type of issue (e.g., error handling, naming, performance)
- Comments in related files or the same module/feature area
- Comments that would benefit from being addressed together (shared context)

For each batch, note:
- Which comments are in the batch
- Why they were grouped together
- The files affected

**Important**: A batch can be a single comment if it's unique. Don't force unrelated comments together.

### 1.5 Create REVIEW_COMMENT_WORK.md

Create the work file as a scratchpad and todo list. Use whatever format feels natural, but include:

- **Triage Results**: Your analysis of each comment's validity
- **Batches**: List each batch with its comments and grouping reasoning (only INCLUDE comments)
- **Excluded**: Comments you recommend excluding with reasoning
- **Status**: Mark each batch as pending/in-progress/done
- **Current State**: Current phase (triage, awaiting approval, working, etc.)
- **Notes**: Space for observations, decisions, anything relevant

Example structure (adapt as needed):

```markdown
# PR Review Comment Work

## Current State
Phase: Awaiting triage approval

## Triage Summary

### Included (5 comments → 2 batches)
| Comment | File | Issue | Verdict |
|---------|------|-------|---------|
| PRR_abc | auth.py:45 | Add try/catch | ✅ Valid |
| PRR_def | user.py:112 | Handle network errors | ✅ Valid |
| PRR_ghi | Header.tsx:23 | Typo "recieve" | ✅ Valid |

### Questionable (1 comment)
| Comment | File | Issue | Concern |
|---------|------|-------|---------|
| PRR_jkl | api.py:89 | Add rate limiting | ⚠️ Out of scope for this PR |

### Excluded (1 comment)
| Comment | File | Issue | Reason |
|---------|------|-------|--------|
| PRR_mno | utils.py:34 | Unused import | ❌ Import is actually used on line 156 |

## Batches (pending approval)

### Batch 1: Error Handling
**Files**: auth.py, user.py
**Comments**: PRR_abc, PRR_def

### Batch 2: Typos
**Files**: Header.tsx
**Comments**: PRR_ghi

## Notes
- (scratchpad space)
```

### 1.6 Present Triage Overview and Get Approval

**STOP and present a CONCISE overview to the user.** Format:

> **PR Review Triage**
> 
> **Will address (N comments in M batches):**
> - Batch 1 - [Name]: [brief description] (N comments)
> - Batch 2 - [Name]: [brief description] (N comments)
> 
> **Questionable (need your input):**
> - [file:line] - [issue] — [your concern]
> 
> **Recommending to skip:**
> - [file:line] - [issue] — [reason]
>
> Let me know if you want to exclude anything, include something I flagged, or adjust the batches.

**WAIT for user response.** Do not proceed until they approve or provide feedback.

### 1.7 Handle Triage Feedback

Process user feedback:
- **Exclude comments**: Remove from batches, add to Excluded section with user's reasoning
- **Include comments**: Add to appropriate batch (or create new batch), move from Excluded/Questionable
- **Adjust batches**: Merge, split, or reorder as requested
- **Approve as-is**: Proceed to work

Update `REVIEW_COMMENT_WORK.md` with any changes.

If changes were made, present the updated overview and ask for approval again.

Once approved, update work file:
- Change "Phase" to "Working on Batch 1"
- Mark batches as `[PENDING]`

### 1.8 Begin Working

Proceed to [Working on a Batch](#working-on-a-batch).

---

## Resuming Work

### 2.1 Read the Work File

Read `REVIEW_COMMENT_WORK.md` to understand:
- Current phase (triage approval, working, etc.)
- Which batches exist and their status
- Which are already done
- Any notes or context from previous work

### 2.2 Determine Next Action

- If **awaiting triage approval**: Present the triage overview again and wait for approval (go to [Present Triage Overview](#16-present-triage-overview-and-get-approval))
- If there are **pending batches**: Continue to [Working on a Batch](#working-on-a-batch)
- If **all batches are done**: Inform the user that all review comments have been addressed

---

## Working on a Batch

### 3.1 Update Work File - Mark In Progress

Before starting work, update `REVIEW_COMMENT_WORK.md`:
- Mark the current batch as `[IN PROGRESS]`
- Update "Current State" to reflect what you're working on

### 3.2 Address the Comments

**Use tasks for investigation, but make edits sequentially.**

If the batch has multiple comments, consider using parallel tasks to investigate each comment's context before making changes:

```
task({
  tasks: [
    { description: "Investigate comment PRRC_abc: Read [file] around line [N], understand the current implementation, and recommend the specific change needed to address: '[comment summary]'. Do NOT make edits." },
    { description: "Investigate comment PRRC_def: Read [file] around line [N], understand the current implementation, and recommend the specific change needed to address: '[comment summary]'. Do NOT make edits." },
  ]
})
```

After gathering investigation results, make the actual code changes **sequentially** (to avoid edit conflicts):

1. Read the relevant file(s)
2. Understand the feedback and the surrounding code
3. Think carefully about whether the feedback is valid
4. Make the appropriate code changes
5. Verify your changes:
   - For backend code: `cd backend && make lint`
   - For frontend code: `cd frontend && ENV=local bun run lint`

**Important**: The comment files contain specific instructions. Follow them, especially the verification steps.

### 3.3 Resolve Comments on GitHub

After addressing each comment in the batch, resolve the thread on GitHub using the `resolve-pr-comment` skill:

1. Get the PR's review threads to find the thread ID for each comment:
   ```bash
   gh api graphql -f query='
   query {
     repository(owner: "OWNER", name: "REPO") {
       pullRequest(number: PR_NUMBER) {
         reviewThreads(first: 100) {
           nodes {
             id
             isResolved
             comments(first: 1) {
               nodes { id }
             }
           }
         }
       }
     }
   }'
   ```

2. Find the thread where `comments.nodes[0].id` matches your comment ID (e.g., `PRRC_...`). The parent `id` is the thread ID (`PRRT_...`).

3. Resolve the thread:
   ```bash
   gh api graphql -f query='
   mutation {
     resolveReviewThread(input: {threadId: "PRRT_..."}) {
       thread { isResolved }
     }
   }'
   ```

### 3.4 Update Work File - Mark Done

After completing the batch:

1. Update `REVIEW_COMMENT_WORK.md`:
   - Mark the batch as `[DONE]`
   - Add any notes about what was done or decisions made
   - Update "Current State" to indicate completion of this batch

2. Delete the processed comment files for this batch:
   ```bash
   rm {comment-id}-review-feedback.md
   ```

### 3.5 Ask for Feedback

**STOP and ask the user**:

> "Batch N complete. I [brief summary of changes made]. 
> 
> Any feedback on these changes, or should I proceed to Batch N+1?"

**WAIT for the user's response.** Do not proceed until they respond.

### 3.6 Handle User Response

- If user provides **feedback**: Address it, update work file with notes, then ask again if ready to proceed
- If user says to **proceed**: Go to the next pending batch and repeat from [Working on a Batch](#working-on-a-batch)
- If user says to **stop**: Update work file with current state and stop

---

## Completion

When all batches are marked as done:

1. Update `REVIEW_COMMENT_WORK.md` to reflect completion
2. Inform the user: "All PR review comments have been addressed."
3. Optionally summarize what was done across all batches

---

## Key Reminders

- **Use parallel tasks for comment investigation** - spawn tasks to analyze/investigate comments in parallel for faster triage and batch processing
- **Make code edits sequentially** - tasks are for read-only investigation; actual edits should be done one at a time to avoid conflicts
- **Always update REVIEW_COMMENT_WORK.md BEFORE asking for feedback**
- **Always WAIT for user response between batches** - never auto-proceed
- **Resolve comments on GitHub after addressing them** - use the `resolve-pr-comment` skill
- **Delete comment files after each batch** - not all at the end
- **Trust the work file on resume** - don't re-fetch comments
- **User can delete REVIEW_COMMENT_WORK.md to force a fresh start**
