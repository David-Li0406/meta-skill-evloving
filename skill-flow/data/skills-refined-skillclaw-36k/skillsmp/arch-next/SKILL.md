---
name: arch-next
description: Verify current step and advance to the next step
disable-model-invocation: true
---

# /arch-next Skill

**Status: Active**

Verify the current step's implementation and advance to the next step in the plan.

## Usage

```
/arch-next
```

## Prerequisites

- Run `/arch [request]` to generate the plan
- Run `/arch-start` to begin execution
- Implement the current step

---

## Instructions

Run these commands in sequence:

```bash
# Step 1: Run verification for current step
python scripts/arch_session.py verify

# Step 2: If verification passed, advance to next step
python scripts/arch_session.py next
```

The `verify` command:
- Runs all verification commands from TASK_GRAPH.json for the current step
- Sets `step_verified: true/false` in state.json based on results
- Exits with code 0 if all commands pass, 1 if any fail

The `next` command:
- Requires `step_verified: true` before advancing
- If verification hasn't passed, it will error with instructions to run `verify` or `skip`
- After advancing, resets `step_verified: false` for the new step

---

## Bypassing Verification

If you need to skip verification (e.g., verification commands are incorrect):

```bash
python scripts/arch_session.py skip --reason "Reason for skipping"
```

---

## Constraints

- **Verification required**: `next` will not advance without passing verification
- **One step at a time**: Only advances one step per invocation
- **No implementation**: This skill only verifies and advances; implement the step first
