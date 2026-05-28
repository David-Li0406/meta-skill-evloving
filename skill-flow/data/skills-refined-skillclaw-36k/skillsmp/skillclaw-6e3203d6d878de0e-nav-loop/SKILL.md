---
name: nav-loop
description: Use this skill to execute tasks iteratively until completion, utilizing structured completion signals and stagnation detection.
---

# Navigator Loop Skill

Execute tasks iteratively until completion with structured signals, stagnation detection, and dual-condition exit gates.

## Why This Exists

Traditional AI coding requires manual "keep going" prompts. Navigator Loop provides:
- **Structured completion signals** (NAVIGATOR_STATUS block)
- **Dual-condition exit gate** (heuristics + explicit signal)
- **Stagnation detection** (circuit breaker for stuck loops)
- **Progress visibility** (phases: INIT → RESEARCH → IMPL → VERIFY → COMPLETE)

## When to Invoke

**Auto-invoke when**:
- User says "run until done", "keep going until complete"
- User says "iterate until finished", "autonomous mode"
- User says "loop mode", "don't stop until done"
- Task document has `loop_mode: true`

**DO NOT invoke if**:
- Single-step task (no iteration needed)
- User says "just do this once"
- Already in loop mode (prevent nested loops)
- User explicitly disabled loop mode

## Configuration

Loop mode settings in `.agent/.nav-config.json`:

```json
{
  "loop_mode": {
    "enabled": false,
    "max_iterations": 5,
    "stagnation_threshold": 3,
    "exit_requires_explicit_signal": true,
    "show_status_block": true
  }
}
```

**Options**:
- `enabled`: Default state for new tasks
- `max_iterations`: Hard cap to prevent infinite loops (1-20)
- `stagnation_threshold`: Same-state count before pause (2-5)
- `exit_requires_explicit_signal`: Require EXIT_SIGNAL alongside heuristics

## Execution Steps

### Step 1: Initialize Loop State

**Load configuration**:
```bash
python3 functions/phase_detector.py --init
```

**Initialize tracking variables**:
```bash
iteration = 1
max_iterations = config.loop_mode.max_iterations or 5
stagnation_threshold = config.loop_mode.stagnation_threshold or 3
hash_history = []
phase = "INIT"
```

**Display loop start**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOOP MODE ACTIVATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task: {TASK_DESCRIPTION}
Max iterations: {max_iterations}
Stagnation threshold: {stagnation_threshold}

Starting iteration 1...
```