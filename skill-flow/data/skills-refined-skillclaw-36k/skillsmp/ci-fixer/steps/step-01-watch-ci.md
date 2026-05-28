---
name: step-01-watch-ci
description: Find CI run and monitor status - no upfront wait
prev_step: steps/step-00-init.md
next_step_success: steps/step-05-cleanup.md
next_step_failure: steps/step-02-analyze-errors.md
---

# Step 1: Watch CI

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER sleep upfront - check for CI immediately
- ✅ ALWAYS check for CI run first, only wait if not found
- 📋 YOU ARE A CI MONITOR, not a fixer (that comes later)
- 💬 FOCUS on detecting CI status only
- 🚫 FORBIDDEN to start fixing before CI has run

## EXECUTION PROTOCOLS:

- 🎯 Check immediately → Wait only if needed → Watch → Report
- 💾 Store run_id when found
- 📖 Complete monitoring before loading next step
- 🚫 FORBIDDEN to load step-02 until CI status is known

## CONTEXT BOUNDARIES:

From step-00-init:

| Variable            | Description                                          |
| ------------------- | ---------------------------------------------------- |
| `{auto_mode}`       | Skip confirmations                                   |
| `{max_attempts}`    | Max fix attempts                                     |
| `{current_attempt}` | Current attempt number                               |
| `{branch}`          | Current git branch                                   |
| `{last_commit_sha}` | SHA of the commit we're watching                     |
| `{artifacts_dir}`   | Path to artifacts (may exist from previous attempts) |

## YOUR TASK:

Find the CI run for the current branch, wait only if not triggered yet (max 1 minute), then monitor until completion.

---

## EXECUTION SEQUENCE:

### 1. Get Current Commit SHA

First, capture the commit we're watching:

```bash
git rev-parse HEAD
```

Store as `{last_commit_sha}` (short: first 7 chars).

### 2. Check for CI Run (Immediate - No Sleep)

**Check immediately for a workflow run:**

```bash
gh run list --branch {branch} --limit 5 --json databaseId,status,conclusion,name,headSha
```

**Find run matching our commit:**

- Look for a run where `headSha` starts with `{last_commit_sha}`
- If found → Extract `databaseId` as `{run_id}`, go to step 3
- If NOT found → Go to wait loop (step 2b)

### 2b. Wait Loop (Only If No CI Found)

**If no CI run found for our commit:**

```
wait_seconds = 0
max_wait = 60  # 1 minute max

WHILE wait_seconds < max_wait:
    Display: "No CI run found yet. Waiting... ({wait_seconds}s / 60s)"

    sleep 10
    wait_seconds += 10

    # Check again
    gh run list --branch {branch} --limit 5 --json databaseId,status,conclusion,name,headSha

    IF run found for {last_commit_sha}:
        → Extract run_id, BREAK loop
        → Go to step 3

IF wait_seconds >= 60 AND still no run:
    → Display: "⚠️ No CI configured for this repository"
    → Display: "No GitHub Actions workflow triggered after 1 minute"
    → Load step-05-cleanup.md (cleanup and exit)
```

### 3. Monitor Run Progress

**If status = "in_progress" or "queued":**

```bash
gh run watch {run_id}
```

This command blocks until the run completes.

**Display:**

- "Watching run #{run_id} for commit {last_commit_sha}..."
- Show job statuses as they complete

### 4. Determine Outcome

After run completes, check final status:

```bash
gh run view {run_id} --json conclusion,jobs
```

**If conclusion = "success":**
→ Display: "✅ CI passed! All checks green."
→ Load `step-05-cleanup.md` (cleanup and summary)

**If conclusion = "failure":**
→ Display: "❌ CI failed. Analyzing errors..."
→ Increment `{current_attempt}`
→ Proceed to step-02

**If conclusion = "cancelled":**
→ Display: "⚠️ CI was cancelled"
→ Ask user what to do

### 5. Check Attempt Limit

**If `{current_attempt}` >= `{max_attempts}`:**
→ Display: "Maximum attempts ({max_attempts}) reached."

**If `{auto_mode}` = false:**
Use AskUserQuestion:

```yaml
questions:
  - header: "Max Attempts"
    question: "Reached {max_attempts} attempts. What should we do?"
    options:
      - label: "Continue trying"
        description: "Keep attempting to fix (reset counter)"
      - label: "Stop here"
        description: "Stop and show summary"
    multiSelect: false
```

**If user chooses "Stop here" OR `{auto_mode}` = true:**
→ Load `step-05-cleanup.md` (cleanup and summary)

---

## SUCCESS METRICS:

✅ Checked for CI immediately (no upfront sleep)
✅ Run ID captured for correct commit
✅ Run monitored to completion
✅ Status correctly determined (success/failure)
✅ Attempt counter updated
✅ Detected "no CI" after 1 minute if applicable
✅ Routes to step-05 on success or stop

## FAILURE MODES:

❌ Sleeping before checking for CI
❌ Waiting longer than 1 minute for non-existent CI
❌ Missing run ID
❌ Not matching run to correct commit SHA
❌ Not incrementing attempt counter
❌ Not routing to cleanup on success

## WATCH PROTOCOLS:

- Check immediately, don't assume CI needs time
- Only wait if no run found (CI might be slow to trigger)
- Max wait: 1 minute, then conclude no CI configured
- Always match run to our specific commit SHA
- Use `gh run watch` for real-time monitoring

---

## NEXT STEP:

**If CI passed:** Load `./step-05-cleanup.md`

**If no CI configured:** Load `./step-05-cleanup.md`

**If max attempts reached and user stops:** Load `./step-05-cleanup.md`

**If CI failed and attempts remaining:** Load `./step-02-analyze-errors.md`

<critical>
Remember: Check first, wait only if needed. Route to cleanup (step-05) on success or stop!
</critical>
