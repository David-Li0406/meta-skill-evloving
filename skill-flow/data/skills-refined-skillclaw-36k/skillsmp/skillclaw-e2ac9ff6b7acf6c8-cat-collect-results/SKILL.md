---
name: cat:collect-results
description: Use this skill when you need to gather results from a completed subagent, including commits, metrics, and state updates for integration back into the parent task branch.
---

# Collect Results

## Purpose

Extract work products from a completed subagent's worktree, including commit history, code changes, token metrics, and status information. This prepares the subagent's work for integration back into the parent task branch.

## When to Use

- Subagent has signaled completion
- Subagent has hit context limits and partial results are needed
- Monitoring indicates subagent is stalled or needs intervention
- Before merging subagent branch to task branch

## Workflow

**Progress Output (MANDATORY):**

Display collection progress using visible feedback symbols:

**On collection start:**
```
◆ Collecting results: {subagent-id}...
```

**On successful collection:**
```
✓ Subagent complete: {N}K tokens · {N} commits
  → Files changed: {N}
  → Status: {success|partial|failed}
```

**On collection with issues:**
```
⚠ Subagent complete with concerns: {N}K tokens · {N} commits
  → Compaction events: {N}
  → Discovered issues: {N}
```

These symbols match the phase-based progress format used in `/cat:work`.

### Steps

1. **Verify Subagent Completion**

   Check for completion marker file (fast path, no session parsing):

   ```bash
   WORKTREE=".worktrees/${TASK}-sub-${UUID}"
   COMPLETION_FILE="${WORKTREE}/.completion.json"

   # Check for completion marker (preferred - lightweight)
   if [ -f "$COMPLETION_FILE" ]; then
     echo "Subagent completed"
     cat "$COMPLETION_FILE"  # Contains status, tokensUsed, compactionEvents, summary
   else
     echo "Subagent not yet complete or marker not written"
   fi
   ```

   **Why completion marker?** Reading `.completion.json` (~200 bytes) is far cheaper than parsing the session JSONL file (potentially megabytes of conversation history).

2. **Extract Commit History**

   ```bash
   cd "${WORKTREE}"

   # Get commits made by subagent (since branch creation)
   git log --oneline origin/HEAD..HEAD

   # Get detailed commit info
   git log --format="%H %s" origin/HEAD..HEAD > /tmp/subagent-commits.txt
   ```

3. **Parse Token Metrics**

   **CRITICAL: Token totals must span ALL compaction events.**

   Session files contain entries BEFORE and AFTER any compaction. The jq command below parses ALL assistant entries regardless of when compaction occurred, providing cumulative totals.

   **Preferred: Read from completion marker** (already computed).