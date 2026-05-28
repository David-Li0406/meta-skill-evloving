---
name: resume
description: Resume working on an in-progress implementation plan. Finds incomplete plans and provides context to continue.
---

# Resume Skill

Find and resume work on an in-progress implementation plan.

## Process

1. **Scan for in-progress plans:**
   - Look for `plans/*/task-list.md` files (exclude `plans/archive/`)
   - A plan is "in-progress" if it has unchecked task boxes: `- [ ]`

2. **For each in-progress plan found, gather context:**
   - Read `.plan-state.json` if it exists:
     - `created_at` - when the plan was created
     - `updated_at` - last state update
     - `planning_agent_id` - agent ID from original planning session (for resumption)
     - `current_task` - task that was in progress
     - `last_session_notes` - notes from previous session
     - `progress.completed` / `progress.total` - task counts
   - If no state file, calculate progress by counting checkboxes in task-list.md:
     - `- [x]` = completed
     - `- [ ]` = incomplete
   - Extract the first 3-5 uncompleted task descriptions

3. **Handle different scenarios:**

   **No plans found:**
   ```
   No in-progress plans found in `plans/`.

   To create a new plan, use `/plan <feature description>`.
   ```

   **One plan found:**
   Display the resume output (see format below).

   **Multiple plans found:**
   List all plans and ask user to choose:
   ```
   Found multiple in-progress plans:

   1. `plans/0006-rust-parser/` - 3/12 tasks (25%)
   2. `plans/0007-output-formats/` - 0/8 tasks (0%)

   Which plan would you like to resume? Enter the number or plan name.
   ```
   Then display resume output for the chosen plan.

4. **Display resume output:**
   ```
   **Resuming plan:** `plans/NNNN-feature-name/`

   **Progress:** N/M tasks complete (X%)
   **Created:** YYYY-MM-DD HH:MM UTC
   **Last session:** YYYY-MM-DD HH:MM UTC (or "No previous session" if no state file)
   **Planning agent:** `{agentId}` (or omit if not in state file)
   **Last notes:** "Notes from previous session" (or omit if null)

   **Next tasks:**
   - [ ] **2.1** First incomplete task
   - [ ] **2.2** Second incomplete task
   - [ ] **2.3** Third incomplete task
   ```

5. **Begin implementing the plan:**
   - Work through tasks, marking them complete in task-list.md
   - Update .plan-state.json with current_task and progress.completed
   - **When completing a phase:** Create a commit with message format:
     `feat(plan-NNNN): Phase N - <phase description>`
   - Add each commit SHA to the `commits` array in .plan-state.json

## Example Outputs

### Single Plan Found

---

**Resuming plan:** `plans/0008-rust-parser/`

**Progress:** 3/12 tasks complete (25%)
**Created:** 2026-01-22 14:30 UTC
**Last session:** 2026-01-23 16:45 UTC
**Planning agent:** `a1b2c3d4-e5f6-7890-abcd-ef1234567890`
**Last notes:** "Completed data model, starting parser implementation"

**Next tasks:**
- [ ] **2.1** Implement panic message regex
- [ ] **2.2** Parse backtrace frame format
- [ ] **2.3** Handle thread panic variants

---

### Multiple Plans Found

---

Found multiple in-progress plans:

1. `plans/0006-rust-parser/` - 3/12 tasks (25%)
2. `plans/0007-output-formats/` - 0/8 tasks (0%)

Which plan would you like to resume? Enter the number or plan name.

---

### No Plans Found

---

No in-progress plans found in `plans/`.

All plans are either completed (in `plans/archive/`) or none exist yet.

To create a new plan, use `/plan <feature description>`.

---
