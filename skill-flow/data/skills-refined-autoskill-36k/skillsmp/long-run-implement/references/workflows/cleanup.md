# Cleanup Workflow

## Purpose

Handle cleanup and rollback operations when a long-run execution is aborted or needs to be reset.

## When Triggered

1. User requests abort during execution
2. Unrecoverable error encountered
3. User requests fresh start on resume prompt
4. Manual cleanup requested

## Cleanup Options

### Option A: Keep Partial Work (Default)

Preserves all commits and state, allowing later resume.

```
Partial work preserved. To see what was done:
  git log --oneline -10

Commits made this session:
  abc1234 feat(01): create database schema
  def5678 feat(01): add migration scripts
  ghi9012 feat(02): create API controller

STATE.md and tasks.md reflect current progress.
To continue later: /long-run-implement [spec-name]
```

**Actions:**
1. Update STATE.md with partial completion status
2. Clear current-agent-id.txt (no active agent)
3. Keep .long-run/ directory intact
4. Keep all commits

### Option B: Rollback All (User Requested)

Reverts all changes to pre-execution state.

**Confirmation Prompt:**
```
⚠️ ROLLBACK REQUESTED

This will:
1. Reset git to commit {start_commit_hash} (before long-run started)
2. Delete .long-run/ directory and all plans/summaries
3. Restore tasks.md to original state (all checkboxes unchecked)

This action CANNOT be undone.

Commits that will be removed:
  abc1234 feat(01): create database schema
  def5678 feat(01): add migration scripts
  ghi9012 feat(02): create API controller

Proceed with rollback? [yes/no]
```

**Rollback Procedure:**
```bash
#!/bin/bash
rollback_all() {
  local spec_path="$1"
  local state_path="${spec_path}/.long-run"

  # 1. Read start commit from STATE.md
  local start_hash=$(grep "start_commit:" "$state_path/STATE.md" | cut -d' ' -f2)

  if [ -z "$start_hash" ]; then
    echo "ERROR: Cannot find start_commit in STATE.md"
    echo "Manual rollback required. Check: git log --oneline"
    return 1
  fi

  # 2. Verify we're not losing unrelated work
  local current_hash=$(git rev-parse HEAD)
  local commits_to_remove=$(git log --oneline "$start_hash..$current_hash" | wc -l)

  echo "Will remove $commits_to_remove commits"

  # 3. Hard reset to start commit
  git reset --hard "$start_hash"

  # 4. Remove .long-run/ directory
  rm -rf "$state_path"

  # 5. Restore tasks.md (was backed up at initialization)
  if [ -f "${spec_path}/tasks.md.backup" ]; then
    mv "${spec_path}/tasks.md.backup" "${spec_path}/tasks.md"
  fi

  echo "Rollback complete. Repository state restored to: $start_hash"
}
```

### Option C: Manual Cleanup

Provides guidance for manual intervention.

```
Manual cleanup mode. Current state:

.long-run/ contents:
  STATE.md          - Execution state (Plan 2 of 5)
  agent-history.json - 3 agent entries
  plans/            - 5 plan files
  summaries/        - 2 summary files

Commits since start (abc1234):
  ghi9012 feat(02): create API controller
  def5678 feat(01): add migration scripts
  abc1234 feat(01): create database schema

Recommended actions:
1. Review commits: git log --oneline abc1234..HEAD
2. Cherry-pick keepers: git cherry-pick <hash>
3. Reset if needed: git reset --hard <hash>
4. Remove state: rm -rf .long-run/

Or re-run with: /long-run-implement --resume
```

## Cleanup Decision Flow

```
User Requests Abort
        │
        ▼
┌───────────────────┐
│ Present Options:  │
│ 1. Keep partial   │
│ 2. Rollback all   │
│ 3. Manual cleanup │
└───────────────────┘
        │
        ▼
    User Choice
        │
   ┌────┼────┐
   ▼    ▼    ▼
 Keep  Roll  Manual
   │   back    │
   │    │      │
   ▼    ▼      ▼
Update  Git   Show
STATE  Reset  Guide
```

## Partial Cleanup (After Failed Plan)

When a single plan fails but others succeeded:

```bash
cleanup_failed_plan() {
  local plan_number="$1"
  local state_path="$2"

  # 1. Mark plan as failed in agent-history.json
  update_json_atomic "$state_path/agent-history.json" \
    "(.agents[] | select(.plan == \"$plan_number\")).status = \"failed\""

  # 2. Create failed SUMMARY.md
  cat > "$state_path/summaries/${plan_number}-SUMMARY.md" << EOF
---
version: "1.0"
plan: $plan_number
status: failed
completed_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
---

# Plan $plan_number: FAILED

## Failure Details
Plan execution was aborted. See error details in execution log.

## Partial Work
Any commits from this plan have been preserved.
Review with: git log --oneline -5

## Recovery Options
1. Re-run plan: Resume and select "Retry failed plan"
2. Skip plan: Resume and select "Skip to next plan"
3. Rollback: Start fresh with /long-run-implement --clean
EOF

  # 3. Update STATE.md
  # ... (via update-state workflow)
}
```

## Cleanup on Interrupt (Ctrl+C / SIGINT)

```bash
handle_interrupt() {
  echo ""
  echo "Interrupt received. Saving state..."

  # 1. Write checkpoint if mid-task
  if [ -n "$CURRENT_TASK" ]; then
    save_checkpoint "$CURRENT_TASK" "interrupted"
  fi

  # 2. Update agent-history.json
  if [ -n "$CURRENT_AGENT_ID" ]; then
    update_json_atomic "$STATE_PATH/agent-history.json" \
      "(.agents[] | select(.agent_id == \"$CURRENT_AGENT_ID\")).status = \"interrupted\""
  fi

  # 3. Update STATE.md
  update_state_status "Interrupted" "User interrupt (Ctrl+C)"

  echo "State saved. Resume with: /long-run-implement [spec-name]"
  exit 130
}

trap handle_interrupt SIGINT SIGTERM
```

## Error Handling

| Error | Action |
|-------|--------|
| start_commit missing | Warn user, offer manual git log review |
| Git reset fails | Show git error, suggest manual intervention |
| Permission denied | Warn about file permissions, suggest sudo/admin |
| tasks.md.backup missing | Skip restore, warn user to check git history |
