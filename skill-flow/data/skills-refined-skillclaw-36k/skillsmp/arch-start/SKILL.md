---
name: arch-start
description: Start executing the architecture plan from step 1
disable-model-invocation: true
---

# /arch-start Skill

**Status: Active**

Begin executing the architecture plan by starting from step 1. This skill transitions from planning to execution and implements the first step.

## Usage

```
/arch-start
```

## Prerequisites

Run `/arch [request]` first to generate the architecture artifacts.

---

## Step 1: Verify Artifacts Exist

Confirm these files exist:
- `.claude/arch/TASK_GRAPH.json`
- `.claude/arch/state.json`

If either is missing, stop and output:

```
Error: Architecture artifacts not found.
Run /arch [request] first to generate the plan.
```

---

## Step 2: Start the Session

Run this command:

```bash
python scripts/arch_session.py start
```

This will:
- Set `phase` to `"executing"`
- Set `current_step` to the first step ID
- Print the current step details

---

## Step 3: Read Current Step Details

Read `.claude/arch/TASK_GRAPH.json` and find the current step. Display:

```
Current Step: [id] - [title]
Goal: [goal]
Allowed Paths: [allowed_paths]
Verification: [verification commands]
Success Criteria: [success_criteria]
```

---

## Step 4: Implement the Step

Implement the goal described in the current step.

**CRITICAL CONSTRAINTS:**
- **ONLY modify files that match `allowed_paths`** for this step
- Do NOT touch any files outside the allowed paths
- Do NOT skip ahead to other steps
- Keep changes minimal and focused on the step's goal

---

## Step 5: Run Verification

After implementing, run each verification command listed for the step:

```bash
# Run each command from the step's "verification" array
[verification command 1]
[verification command 2]
...
```

---

## Step 6: Report and Stop

After verification, output the results and stop:

**If verification passes:**
```
Step [id] implementation complete.
Verification passed.

Run /arch-next to advance to the next step.
```

**If verification fails:**
```
Step [id] implementation complete.
Verification FAILED:
[error output]

Fix the issues and re-run verification, then run /arch-next.
```

---

## Constraints

- **Write boundaries enforced**: Only modify files matching `allowed_paths` for the current step
- **One step at a time**: Do not implement multiple steps in one invocation
- **Verification required**: Always run verification commands before stopping
- **User controls progression**: Wait for user to run `/arch-next` to advance
