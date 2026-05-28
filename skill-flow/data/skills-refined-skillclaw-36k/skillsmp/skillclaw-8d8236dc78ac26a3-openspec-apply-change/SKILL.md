---
name: openspec-apply-change
description: Use this skill when you want to start implementing, continue implementation, or work through tasks from an OpenSpec change.
---

# Skill body

Implement tasks from an OpenSpec change.

**Input**: Optionally specify a change name. If omitted, you MUST prompt for available changes.

**Steps**

1. **Select the change**
   - If a name is provided, use it. Otherwise, run `openspec list --json` to get available changes and use the **AskUserQuestion tool** to let the user select. Show only changes that are implementation-ready (have tasks artifact) and include the schema used for each change. Mark changes with incomplete tasks as "(In Progress)".

2. **Check status to understand the schema**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to understand:
   - `schemaName`: The workflow being used (e.g., "spec-driven", "tdd")
   - Which artifact contains the tasks (typically "tasks" for spec-driven, check status for others)

3. **Get apply instructions**
   ```bash
   openspec instructions apply --change "<name>" --json
   ```
   This returns:
   - Context file paths (varies by schema - could be proposal/specs/design/tasks or spec/tests/implementation/docs)
   - Progress (total, complete, remaining)
   - Task list with status
   - Dynamic instruction based on current state

   **Handle states:**
   - If `state: "blocked"` (missing artifacts): show message, suggest using openspec-continue-change.
   - If `state: "all_done"`: congratulate, suggest archiving.
   - Otherwise: proceed to implementation.

4. **Read context files**
   Read the files listed in `contextFiles` from the apply instructions output. The files depend on the schema being used:
   - **spec-driven**: proposal, specs, design, tasks
   - **tdd**: spec, tests, implementation, docs
   - Other schemas: follow the contextFiles from CLI output.

5. **Show current progress**
   Display:
   - Schema being used
   - Progress: "N/M tasks complete"
   - Remaining tasks overview
   - Dynamic instruction from CLI.

6. **Implement tasks (loop until done or blocked)**
   For each pending task:
   - Show which task is being worked on.
   - Make the code changes required.
   - Keep changes minimal and focused.
   - Mark task complete in the tasks file: `- [ ]` → `- [x]`.
   - Continue to the next task.

   **Pause if:**
   - Task is unclear → ask for clarification.
   - You encounter a blocking issue.