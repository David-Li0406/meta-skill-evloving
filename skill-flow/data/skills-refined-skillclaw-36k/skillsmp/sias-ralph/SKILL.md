---
name: sias-ralph
description: "SIAS RALPH - Score Integrity Audit Loop. Autonomous batch processing of all users through SIAS validation. Trigger: /sias-ralph, run RALPH, batch audit, audit all users."
---

# SIAS RALPH - Reliable Autonomous Loop for Processing Humans

You are running the RALPH batch audit system. Your job is to process ALL users through SIAS validation until complete.

## AUTONOMOUS LOOP STRUCTURE

```
WHILE (unprocessed users exist):
    1. FETCH next batch from API
    2. FOR EACH user in batch (run 4 in parallel):
        a. Launch sias-auditor agent
        b. Agent performs: dry-run → rebuild → verify → validate UI → SAVE
    3. LOG batch results to progress.txt
    4. REPEAT (go back to step 1)
END WHEN batch returns 0 users
```

**CRITICAL**: After completing each batch, you MUST immediately fetch the next batch and continue. Do NOT stop or wait for user input between batches.

---

## Step 1: Fetch Next Batch

```bash
curl -s "https://28dayreset.com/api/admin/sias/next-batch?size=10" \
  -H "X-User-ID: 0f950f68-885c-47f9-9cb4-aabbb8bea55f"
```

Parse the response to get the user list. If `batch` is empty, RALPH is complete.

## Step 2: Process Users in Parallel (4 at a time)

For each user, launch a Task with `subagent_type: sias-auditor`:

```
Task(
  description: "SIAS audit {userName}",
  prompt: "Run a FULL SIAS audit on user: {userName}
    User ID: {userId}
    Email: {email}
    Phone: {phone}

    MANDATORY STEPS:
    1. Run dry-run analysis
    2. Rebuild if discrepancies exist
    3. Verify fix with another dry-run
    4. VALIDATE: Check /api/course/history matches ledger
    5. SAVE: POST to /api/admin/sias/audit-results
    6. Report auditId

    DO NOT EXIT without completing SAVE step.",
  subagent_type: "sias-auditor"
)
```

Launch 4 Tasks simultaneously, wait for all to complete, then launch next 4.

## Step 3: Log Batch Results

After all users in batch complete, append to `.claude/ralph/progress.txt`:

```
=== Batch Completed: {timestamp} ===
Users: {count}
PASSED: {n} | FIXED: {n} | FAILED: {n} | ERROR: {n}
Overall: {audited}/{total} ({percent}%)
```

## Step 4: Loop to Next Batch

**IMMEDIATELY** fetch the next batch and continue processing. Do not pause.

---

## IMPORTANT RULES

1. **Never stop between batches** - Keep processing until API returns 0 users
2. **Always save results** - Every audit MUST save to the API
3. **Parallel processing** - Run 4 audits simultaneously for efficiency
4. **Log everything** - Update progress.txt after each batch
5. **Handle errors** - If an audit fails, log ERROR and continue to next user

## Progress Tracking

- **API Dashboard**: Admin > SIAS Audits tab shows all results
- **Local Log**: `.claude/ralph/progress.txt` for session memory
- **Batch State**: Check `/api/admin/sias/next-batch` for remaining count

## When Complete

When the API returns an empty batch:
```
=== RALPH MISSION COMPLETE ===
Total users audited: {n}
PASSED: {n} | FIXED: {n} | FAILED: {n} | ERROR: {n}
```

---

## START NOW

Fetch the first batch and begin processing:

```bash
curl -s "https://28dayreset.com/api/admin/sias/next-batch?size=10" \
  -H "X-User-ID: 0f950f68-885c-47f9-9cb4-aabbb8bea55f"
```
