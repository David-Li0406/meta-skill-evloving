---
name: planning-and-execution
description: Use this skill when you need to execute tasks in a structured manner while maintaining detailed records of progress and findings.
---

# Skill body

## Overview
This skill combines task execution and planning using three key files: `task_plan.md`, `findings.md`, and `progress.md`. It ensures that tasks are completed step-by-step while documenting discoveries and progress.

## Execution Rules
1. **Read the Plan**: Before starting, read the current phase and steps from `task_plan.md`.
2. **Step-by-Step Execution**: Execute one step at a time. Only proceed to the next step after completing the current one.
3. **Record Discoveries**: Any new findings must be documented in `findings.md`.
4. **Log Progress**: Document actions, results, and any modifications in `progress.md` after each step.
5. **Update Phase**: After completing a phase, update the status in `task_plan.md`.

## Maintenance Requirements
- **`task_plan.md`**: Keep track of phase progress and decision updates.
- **`findings.md`**: Record discoveries and evidence.
- **`progress.md`**: Maintain a log of actions and errors encountered.

## Output Requirements
- All outputs should be in Chinese.
- Do not skip or merge steps.
- If any gaps are identified, mark them in the plan and request a re-evaluation. 

## File Locations
Templates for the three files can be found in the skill's directory, but the actual planning files should be created in the project's root directory.