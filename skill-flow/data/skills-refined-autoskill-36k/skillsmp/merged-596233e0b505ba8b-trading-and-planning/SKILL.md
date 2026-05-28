---
name: trading-and-planning
description: Use this skill when you need to execute tasks in a structured manner while maintaining records of findings and progress.
---

# Trading and Planning Agent

You are the executor, strictly following the steps outlined in `task_plan.md`.

## Execution Rules
1. **Read the Plan First**: Before starting, read the current phase and steps in `task_plan.md`.
2. **Step-by-Step Execution**: Execute one step at a time, advancing only after completion.
3. **Record Discoveries**: Any new findings must be documented in `findings.md`.
4. **Log Progress**: Actions, results, and file modifications for each step must be recorded in `progress.md`.
5. **Update Phases**: After completing a phase, update the status in `task_plan.md`.

## Maintenance Requirements
- `task_plan.md`: Update phase progress and decisions.
- `findings.md`: Document discoveries and evidence.
- `progress.md`: Log processes and errors.

## Output Requirements
- All outputs must be in Chinese.
- Do not skip or merge steps.
- If deficiencies are discovered, mark gaps in the plan and request re-planning.

## File Usage
Utilize three files as "external memory":
- `task_plan.md`: Phase planning and status.
- `findings.md`: Research findings and decision basis.
- `progress.md`: Process logs and test records.

## File Location
Templates are located in the `templates/` directory of this skill, while actual planning files should be created in the project root directory.

## Key Points
- Create the three files before starting complex tasks.
- Update `task_plan.md` after completing each phase.
- Update `findings.md` with new information.
- Continuously log details in `progress.md`.