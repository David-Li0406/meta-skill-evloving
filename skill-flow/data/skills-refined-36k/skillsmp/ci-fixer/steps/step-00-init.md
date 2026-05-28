---
name: step-00-init
description: Initialize ci-fixer workflow - parse flags, detect branch, setup state
next_step: steps/step-01-watch-ci.md
---

# Step 0: Initialization

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER skip flag parsing
- ✅ ALWAYS detect the current git branch
- 📋 Parse ALL flags before any other action
- 💬 FOCUS on initialization only - don't start watching CI yet
- 🚫 FORBIDDEN to proceed without proper state setup

## EXECUTION PROTOCOLS:

- 🎯 Parse flags first, then setup state
- 💾 Initialize all state variables
- 📖 Complete this step fully before loading next
- 🚫 FORBIDDEN to load step-01 until init complete

## YOUR TASK:

Initialize the workflow by parsing flags, detecting the current branch, and setting up the execution environment.

---

## DEFAULTS CONFIGURATION:

```yaml
auto_mode: false # -a, --auto: Skip confirmations
max_attempts: 5 # -m N, --max-attempts=N: Max fix attempts
current_attempt: 0 # Starts at 0
fixes_applied: [] # Empty list
local_verified: false # Not verified yet
```

---

## INITIALIZATION SEQUENCE:

### 1. Parse Flags and Input

**Step 1: Load defaults from config above**

**Step 2: Parse user input and override defaults:**

```
Enable flags:
  -a, --auto → {auto_mode} = true

Set values:
  -m N, --max-attempts=N → {max_attempts} = N
```

### 2. Detect Current Branch

Run this command to get the current branch:

```bash
git branch --show-current
```

Store result in `{branch}`.

**If no branch detected (detached HEAD):**
→ Use `git rev-parse --short HEAD` as identifier
→ Warn user: "Running in detached HEAD mode"

### 3. Verify Git Status

Run:

```bash
git status --porcelain
```

**If there are uncommitted changes:**
→ Warn user: "You have uncommitted changes. They may interfere with CI fixes."

**If `{auto_mode}` = false:**
Use AskUserQuestion:

```yaml
questions:
  - header: "Changes"
    question: "You have uncommitted changes. How should we proceed?"
    options:
      - label: "Continue anyway (Recommended)"
        description: "Proceed with uncommitted changes"
      - label: "Stash changes"
        description: "Stash changes before proceeding (git stash)"
      - label: "Cancel"
        description: "Stop and handle changes manually"
    multiSelect: false
```

### 4. Initialize State

Set all state variables:

```yaml
auto_mode: { parsed value }
max_attempts: { parsed value }
current_attempt: 0
branch: { detected branch }
run_id: null
error_source: null
error_logs: null
fixes_applied: []
local_verified: false
```

### 5. Confirm Start

**If `{auto_mode}` = true:**
→ Proceed directly to step-01

**If `{auto_mode}` = false:**
Use AskUserQuestion:

```yaml
questions:
  - header: "Start"
    question: "CI Fixer ready. Watch CI on branch '{branch}'?"
    options:
      - label: "Start watching (Recommended)"
        description: "Begin monitoring CI pipeline"
      - label: "Change settings"
        description: "Modify configuration before starting"
      - label: "Cancel"
        description: "Don't start the workflow"
    multiSelect: false
```

---

## SUCCESS METRICS:

✅ All flags correctly parsed
✅ Current branch detected
✅ Git status checked
✅ State variables initialized
✅ User confirmed start (if not auto_mode)

## FAILURE MODES:

❌ Not detecting the current branch
❌ Proceeding with git errors
❌ Missing state variables
❌ Not warning about uncommitted changes

---

## NEXT STEP:

After initialization, load `./step-01-watch-ci.md`

<critical>
Remember: Init is ONLY about setup - don't start watching CI here!
</critical>
