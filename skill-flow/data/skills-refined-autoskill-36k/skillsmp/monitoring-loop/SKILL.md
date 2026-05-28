---
name: monitoring-loop
description: Wave-based monitoring algorithm for teamwork orchestration. Handles wave completion detection, verification triggering, conflict detection, and failure recovery.
---

# Monitoring Loop

This skill provides the complete wave monitoring algorithm for teamwork orchestrators. Use this to continuously monitor wave execution, trigger verification, and handle failures.

## When to Use This Skill

- Orchestrating multi-wave teamwork projects
- Monitoring task completion and wave progression
- Triggering wave verification at appropriate times
- Detecting and resolving file conflicts
- Handling verification failures with fix tasks

## Input Format

Your prompt includes:

```
TEAMWORK_DIR: {path to teamwork directory}
PROJECT: {project name}
SUB_TEAM: {sub-team name}
SCRIPTS_PATH: {path to scripts directory}

Options:
- monitor_interval: {seconds, default 10}
- max_iterations: {number, default 1000}
```

---

## Loop Structure

The monitoring loop continuously checks wave status, triggers verification, and handles failures.

### Pseudocode

```javascript
// Monitoring loop structure
const MONITOR_INTERVAL = options.monitor_interval || 10; // seconds
const MAX_ITERATIONS = options.max_iterations || 1000;
let iteration = 0;

while (!isProjectComplete() && iteration < MAX_ITERATIONS) {
  iteration++;

  // 1. Get current wave status
  const waveState = getCurrentWaveStatus();

  // 2. Check if wave is complete
  if (isWaveComplete(waveState)) {
    // 3. Trigger wave verification
    const verificationResult = verifyWave(waveState.current_wave);

    // 4. Handle verification result
    if (verificationResult.verdict === 'PASS') {
      // Mark wave as verified
      updateWaveStatus(waveState.current_wave, 'verified');

      // Move to next wave
      if (hasNextWave()) {
        moveToNextWave();
        updateWaveStatus(getCurrentWave(), 'in_progress');
      } else {
        // Last wave completed - do final verification
        performFinalVerification();
        markProjectComplete();
        break;
      }
    } else {
      // Verification FAILED
      handleVerificationFailure(verificationResult);
    }
  }

  // 5. Detect file conflicts
  const conflicts = detectFileConflicts(waveState);
  if (conflicts.length > 0) {
    signalConflicts(conflicts);
  }

  // 6. Sleep before next check
  sleep(MONITOR_INTERVAL);
}
```

---

## Step 1: Check Wave Status

Query the current wave status to determine completion.

```bash
# Get current wave status
bun "$SCRIPTS_PATH/wave-status.js" --project {PROJECT} --team {SUB_TEAM} --format json
```

### Expected Status Format

```json
{
  "total_waves": 4,
  "current_wave": 2,
  "summary": {
    "completed": 1,
    "in_progress": 1,
    "remaining": 2
  },
  "waves": [
    {
      "id": 2,
      "status": "in_progress",
      "tasks": ["3", "4", "5"],
      "task_details": [
        {"id": "3", "status": "resolved"},
        {"id": "4", "status": "resolved"},
        {"id": "5", "status": "in_progress"}
      ]
    }
  ]
}
```

### Wave Completion Check

A wave is complete when ALL tasks in the wave have status "resolved":

```javascript
function isWaveComplete(waveStatus) {
  const currentWave = waveStatus.waves.find(w => w.id === waveStatus.current_wave);
  const allResolved = currentWave.task_details.every(t => t.status === 'resolved');
  return allResolved;
}
```

---

## Step 2: Trigger Wave Verification

When a wave is complete, spawn the wave-verifier agent to check for conflicts and integration issues.

### Spawn Wave-Verifier

```markdown
Spawn Agent: wave-verifier

TEAMWORK_DIR: {TEAMWORK_DIR}
PROJECT: {PROJECT}
SUB_TEAM: {SUB_TEAM}
WAVE_ID: {current_wave}

Verify all tasks in wave {current_wave} for conflicts and integration issues.
```

### Read Verification Result

After wave-verifier completes, read the verification result file:

```bash
# Read verification result
cat {TEAMWORK_DIR}/verification/wave-{current_wave}.json
```

### Expected Result Format

```json
{
  "wave_id": 2,
  "verified_at": "2026-01-15T11:00:00Z",
  "verdict": "PASS",
  "summary": {
    "total_tasks": 3,
    "resolved_tasks": 3,
    "conflicts_detected": 0,
    "build_passed": true,
    "tests_passed": true
  },
  "conflicts": [],
  "issues": []
}
```

---

## Step 3: Handle Verification Results

Process the verification result and take appropriate action.

### Case A: Verification PASS

Mark wave as verified and proceed to next wave.

```bash
# Mark wave as verified
bun "$SCRIPTS_PATH/wave-update.js" --project {PROJECT} --team {SUB_TEAM} \
  --wave {current_wave} --status verified

# Check if more waves exist
WAVE_STATUS=$(bun "$SCRIPTS_PATH/wave-status.js" --project {PROJECT} --team {SUB_TEAM} --format json)

# If next wave exists, start it
if [ {current_wave} -lt {total_waves} ]; then
  NEXT_WAVE=$((current_wave + 1))
  bun "$SCRIPTS_PATH/wave-update.js" --project {PROJECT} --team {SUB_TEAM} \
    --wave $NEXT_WAVE --status in_progress
fi
```

**Progress Report:**

```markdown
Wave {current_wave} VERIFIED ✅
- All tasks completed successfully
- No conflicts detected
- Build and tests passed

Starting Wave {next_wave}...
```

### Case B: Verification FAIL

Create fix tasks and handle the failure.

**Example Failure Result:**

```json
{
  "wave_id": 2,
  "verified_at": "2026-01-15T11:00:00Z",
  "verdict": "FAIL",
  "summary": {
    "total_tasks": 3,
    "resolved_tasks": 3,
    "conflicts_detected": 2,
    "build_passed": false,
    "tests_passed": false
  },
  "conflicts": [
    {
      "file": "src/routes/auth.ts",
      "tasks": ["3", "4"],
      "severity": "critical"
    }
  ],
  "issues": [
    {
      "type": "conflict",
      "severity": "critical",
      "description": "Tasks 3 and 4 both modified auth.ts function authenticate()",
      "affected_tasks": ["3", "4"],
      "affected_files": ["src/routes/auth.ts"]
    },
    {
      "type": "test_failure",
      "severity": "critical",
      "description": "5 tests failed in auth.test.ts",
      "details": "Expected 200, got 500"
    }
  ]
}
```

### Failure Handling Strategy

1. **Analyze issues** - Read verification result issues array
2. **Create fix tasks** - One fix task per issue
3. **Add to new wave** - Insert fix wave (e.g., Wave 2b)
4. **Update wave dependencies** - Later waves blocked by fix wave
5. **Mark original wave as failed**
6. **Resume monitoring** - Continue loop with fix wave

### Create Fix Tasks

```bash
# Get next available task ID
NEXT_ID=$(bun "$SCRIPTS_PATH/task-list.js" --project {PROJECT} --team {SUB_TEAM} --format json | jq '.tasks | length + 1')

# Create fix task for conflict
bun "$SCRIPTS_PATH/task-create.js" --project {PROJECT} --team {SUB_TEAM} \
  --id "$NEXT_ID" \
  --title "Resolve auth.ts conflict between task-3 and task-4" \
  --description "Merge conflicting changes in authenticate() function. Task-3 added JWT validation, Task-4 added rate limiting. Need to integrate both features." \
  --role backend \
  --blocked-by "3,4"

# Create fix task for test failures
bun "$SCRIPTS_PATH/task-create.js" --project {PROJECT} --team {SUB_TEAM} \
  --id "$((NEXT_ID + 1))" \
  --title "Fix auth.test.ts failures (5 tests)" \
  --description "Investigate and fix 5 failing tests in auth.test.ts. Expected 200 responses but getting 500 errors." \
  --role test \
  --blocked-by "$NEXT_ID"
```

### Recalculate Waves

After creating fix tasks, recalculate waves to integrate them:

```bash
bun "$SCRIPTS_PATH/wave-calculate.js" --project {PROJECT} --team {SUB_TEAM}
```

### Failure Report

```markdown
Wave {current_wave} FAILED ❌

Issues detected:
- Critical conflict: src/routes/auth.ts (tasks 3, 4)
- Test failures: 5 tests failed in auth.test.ts

Recovery actions:
- Created fix task-{id}: Resolve auth.ts conflict
- Created fix task-{id+1}: Fix auth.test.ts failures
- Recalculated waves: Added Wave {wave_id}b for fixes

Resuming monitoring...
```

---

## Step 4: Detect File Conflicts

Proactively detect file conflicts before verification to warn about potential issues.

### Conflict Detection Algorithm

```bash
# Get all resolved tasks in current wave
WAVE_TASKS=$(bun "$SCRIPTS_PATH/wave-status.js" --project {PROJECT} --team {SUB_TEAM} --format json \
  | jq ".waves[] | select(.id == $CURRENT_WAVE) | .tasks[]")

# For each task, extract file modifications from evidence
for TASK_ID in $WAVE_TASKS; do
  TASK=$(bun "$SCRIPTS_PATH/task-get.js" --project {PROJECT} --team {SUB_TEAM} --id $TASK_ID)
  # Parse evidence for "Created/Modified/Updated {file}" patterns
done
```

### Build Conflict Map

```javascript
// Example conflict detection
const fileMap = {
  "src/routes/auth.ts": ["3", "4"],
  "package.json": ["3", "5", "6"]
};

// Files modified by > 1 task = potential conflict
const conflicts = Object.entries(fileMap)
  .filter(([file, tasks]) => tasks.length > 1)
  .map(([file, tasks]) => ({ file, tasks }));
```

### Check Conflict Severity

```bash
# For each conflicting file, check if same function modified
for CONFLICT in $CONFLICTS; do
  FILE=$CONFLICT.file
  TASKS=$CONFLICT.tasks

  # Use git log to check modification overlap
  git log --oneline --all -- $FILE | head -10

  # Use grep to check if same function modified
  grep -n "function authenticate" $FILE
done
```

### Signal Conflicts

```markdown
⚠️  FILE CONFLICTS DETECTED

- src/routes/auth.ts
  - Modified by: task-3, task-4
  - Severity: CRITICAL (same function modified)

- package.json
  - Modified by: task-3, task-5, task-6
  - Severity: WARNING (different sections)

Action required:
- Review changes in conflicting files
- Wave verification will likely FAIL
- Fix tasks will be created automatically
```

---

## Step 5: Monitor Sleep Interval

Between monitoring iterations, sleep to avoid excessive resource usage.

```bash
# Sleep before next check
sleep $MONITOR_INTERVAL
```

### Monitoring Output During Sleep

```markdown
[Iteration {iteration}] Wave {current_wave}: {in_progress_count} tasks in progress, {resolved_count} resolved
Checking again in {MONITOR_INTERVAL} seconds...
```

---

## Error Handling

### Monitoring Loop Hangs

If wave never completes (tasks stuck):
- Report stuck tasks after N iterations (e.g., 50)
- Suggest manual intervention
- Continue monitoring (don't exit)

### Wave Verification Timeout

If wave-verifier doesn't complete:
- Wait up to 5 minutes
- If still not complete, mark as FAIL
- Create investigation task

### Script Failures

If utility scripts fail:
- Log error message
- Retry up to 3 times
- If still failing, report and exit loop

### Max Iterations Reached

If loop reaches max_iterations:
- Report incomplete status
- Show which wave/tasks are incomplete
- Suggest increasing max_iterations or checking for stuck tasks

---

## Best Practices

### Continuous Monitoring

- Run monitoring loop continuously until project complete
- Don't exit early even if issues detected
- Always complete full verification cycle

### Evidence-Based Decisions

- All decisions based on concrete status checks
- Never assume task completion without checking
- Read actual verification results, don't speculate

### Failure Recovery

- Always create fix tasks for verification failures
- Recalculate waves after adding fix tasks
- Resume monitoring automatically after recovery

### Conflict Detection

- Check for conflicts proactively during monitoring
- Warn users before verification fails
- Provide detailed conflict information

---

## Notes

- Monitoring loop is the core orchestration logic
- Always verify every wave before proceeding
- Handle failures gracefully with fix tasks
- Never skip verification steps
- Continuous monitoring ensures project progress
