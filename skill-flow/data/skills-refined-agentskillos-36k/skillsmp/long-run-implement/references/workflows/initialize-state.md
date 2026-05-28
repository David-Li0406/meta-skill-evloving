# Initialize Long-Run State

## Purpose
Set up or restore execution state for a long-run implementation session.

## Inputs
- `spec_path`: Path to the spec folder (e.g., `agent-os/specs/my-feature/`)
- OR prompt user if not provided

## Workflow

### Step 1: Locate Spec Folder
```
IF spec_path not provided:
  - List available specs in agent-os/specs/
  - Ask user to select one
  - Set spec_path = selected spec
```

### Step 2: Validate Inputs
```
REQUIRED files:
  - {spec_path}/tasks.md
  - {spec_path}/spec.md OR {spec_path}/planning/requirements.md

IF missing:
  - Stop and inform user which files are missing
  - Suggest running /create-tasks first if tasks.md missing
```

### Step 3: Check for Existing State
```
IF {spec_path}/.long-run/ exists:
  - Read STATE.md
  - Check current status
  - GOTO Step 4 (Resume Detection)
ELSE:
  - GOTO Step 5 (Initialize New)
```

### Step 4: Resume Detection
```
IF .long-run/current-agent-id.txt exists:
  - Read agent_id
  - Find entry in agent-history.json
  - Present options:
    1. Resume interrupted execution
    2. Start fresh (clear .long-run/)
    3. Skip to next plan
  - Wait for user choice

IF STATE.md shows "Stopped at: Awaiting clarification":
  - Read clarifications.md for pending question
  - Re-present clarification request
  - Wait for response
```

### Step 5: Initialize New State
```
# NOTE: For fresh starts, .long-run/ directory and STATE.md are created
# by plan-fixer Phase 4, NOT here. This step only applies to resume scenarios.

IF resuming from existing .long-run/:
  # State files already exist, just validate
  1. Verify {spec_path}/.long-run/STATE.md exists
  2. Verify {spec_path}/.long-run/agent-history.json exists
  3. Verify {spec_path}/.long-run/plans/ contains NN-PLAN.md files

ELSE (fresh start):
  # Skip directory/state creation - plan-fixer Phase 4 handles this
  # Phase 4 will create:
  #   - .long-run/ directory structure
  #   - STATE.md (from template: templates/long-run-state.md)
  #   - agent-history.json (with { "version": "1.0", "agents": [] })
  #   - ISSUES.md (empty)
  #   - plans/ with split NN-PLAN.md files
  #   - summaries/ (empty)
  Log: "Deferring state initialization to plan-fixer Phase 4"

# Pre-flight checks (run for both fresh and resume)
1. Record start commit:
   start_commit = $(git rev-parse HEAD)
   # Note: Written to STATE.md after plan-fixer creates it

2. Check for uncommitted changes:
   IF git status --porcelain returns output:
     Present options:
       1. Stash changes (git stash)
       2. Commit changes first
       3. Abort and resolve manually
     Wait for user choice
```

### Step 6: Output
```
Return:
  - spec_path: validated spec path
  - state_path: path to .long-run/ directory
  - is_resume: boolean
  - resume_point: plan number if resuming, null otherwise
```

## Error Handling

```
ON any error:
  - Log error to STATE.md Issues section
  - Present error to user
  - Offer: Retry / Abort / Manual intervention
```
