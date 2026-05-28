# Example PRD: Voice-Driven Schedule Update

## Overview

This example PRD demonstrates how to use the P6 Voice Agent to update a project schedule through voice commands.

## Scenario

You need to update the GEMCO L1 project schedule with the following changes:

1. Extend activity "MT-001" (Mobilization) duration from 5 to 10 days
2. Set a constraint on activity "MT-002" (Site Prep) to start on or after February 1, 2025
3. Update activity "MT-003" (Foundation) duration to 15 days
4. Run the schedule to recalculate dates

## Voice Commands

### Step 1: Open the Agent

```bash
cd "P6 GUI Automation"
python main.py --unsafe  # Enable editing mode
```

Wait for "Whisper Ready" status.

### Step 2: Select and Edit First Activity

**Voice Command:**
> "Select activity MT-001"

*Expected Response:* Agent opens Find dialog, types MT-001, and selects the activity.

**Voice Command:**
> "Change duration to 10 days"

*Expected Response:* Agent tabs to Duration column, enters edit mode, types "10d", confirms.

### Step 3: Set Constraint on Second Activity

**Voice Command:**
> "Select activity MT-002"

**Voice Command:**
> "Set constraint start on or after February 1st 2025"

*Expected Response:* Agent opens activity details, navigates to Constraints tab, sets constraint type and date.

### Step 4: Update Third Activity

**Voice Command:**
> "Find activity MT-003 and change duration to 15 days"

*Expected Response:* Agent executes compound command - select then edit.

### Step 5: Reschedule

**Voice Command:**
> "Run the schedule"

*Expected Response:* Agent presses F9, waits for schedule dialog, confirms execution.

## Expected Outcome

After completing these commands:
- MT-001 duration = 10 days
- MT-002 has "Start On or After" constraint = Feb 1, 2025
- MT-003 duration = 15 days
- Schedule dates recalculated

## Verification

Use these voice commands to verify:

> "Select activity MT-001"  
> "What are the visible columns?"

## Tips

1. **Speak clearly** - Whisper works best with clear pronunciation
2. **Wait for confirmation** - The overlay shows status after each command
3. **Use SAFE_MODE first** - Test with `--safe-mode` to see what would happen without executing
4. **Check the logs** - View `logs/app.log` for detailed operation history

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Activity not found" | Check the activity ID exists in current view |
| "Column not visible" | Add required columns to P6 layout |
| "SAFE_MODE active" | Restart with `--unsafe` flag |
| "Whisper not ready" | Wait for model to load (~10-30 seconds) |
| "Could not focus P6" | Click on P6 window once, then retry |
