---
name: openspec-archive-change
description: Use this skill when you want to finalize and archive a completed change in the experimental workflow.
---

# Skill body

Archive a completed change in the experimental workflow.

**Input**: Optionally specify a change name. If omitted, prompt for available changes.

**Steps**

1. **If no change name provided, prompt for selection**
   - Run `openspec list --json` to get available changes. Use the **AskUserQuestion tool** to let the user select.
   - Show only active changes (not already archived) and include the schema used for each change if available.
   - **IMPORTANT**: Do NOT guess or auto-select a change. Always let the user choose.

2. **Check artifact completion status**
   - Run `openspec status --change "<name>" --json` to check artifact completion.
   - Parse the JSON to understand:
     - `schemaName`: The workflow being used
     - `artifacts`: List of artifacts with their status (`done` or other)
   - **If any artifacts are not `done`:**
     - Display a warning listing incomplete artifacts.
     - Use **AskUserQuestion tool** to confirm if the user wants to proceed.
     - Proceed if the user confirms.

3. **Check task completion status**
   - Read the tasks file (typically `tasks.md`) to check for incomplete tasks.
   - Count tasks marked with `- [ ]` (incomplete) vs `- [x]` (complete).
   - **If incomplete tasks found:**
     - Display a warning showing the count of incomplete tasks.
     - Use **AskUserQuestion tool** to confirm if the user wants to proceed.
     - Proceed if the user confirms.
   - **If no tasks file exists:** Proceed without task-related warning.

4. **Assess delta spec sync state**
   - Check for delta specs at `openspec/changes/<name>/specs/`. If none exist, proceed without sync prompt.
   - **If delta specs exist:**
     - Compare each delta spec with its corresponding main spec at `openspec/specs/<capability>/spec.md`.
     - Determine what changes would be applied (adds, modifications, removals, renames).
     - Show a combined summary before prompting.
   - **Prompt options:**
     - If changes needed: "Sync now (recommended)", "Archive without syncing".
     - If already synced: "Archive now", "Sync anyway", "Cancel".
   - If the user chooses to sync, execute `/opsx:sync` logic (use the openspec-sync-specs skill). Proceed to archive regardless of choice.

5. **Perform the archive**
   - Create the archive directory if it doesn't exist.
   - Archive the change and confirm completion to the user.