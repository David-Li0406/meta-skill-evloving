---
name: openspec-archive-change
description: Use this skill to archive a completed change in the experimental workflow after implementation is complete.
---

Archive a completed change in the experimental workflow.

**Input**: Optionally specify a change name. If omitted, prompt for available changes.

**Steps**

1. **If no change name provided, prompt for selection**

   Run `openspec list --json` to get available changes. Use the **AskUserQuestion tool** to let the user select.

   Show only active changes (not already archived) and include the schema used for each change if available.

   **IMPORTANT**: Do NOT guess or auto-select a change. Always let the user choose.

2. **Check artifact completion status**

   Run `openspec status --change "<name>" --json` to check artifact completion.

   Parse the JSON to understand:
   - `schemaName`: The workflow being used
   - `artifacts`: List of artifacts with their status (`done` or other)

   **If any artifacts are not `done`:**
   - Display a warning listing incomplete artifacts.
   - Use **AskUserQuestion tool** to confirm if the user wants to proceed.
   - Proceed if the user confirms.

3. **Check task completion status**

   Read the tasks file (typically `tasks.md`) to check for incomplete tasks.

   Count tasks marked with `- [ ]` (incomplete) vs `- [x]` (complete).

   **If incomplete tasks found:**
   - Display a warning showing the count of incomplete tasks.
   - Use **AskUserQuestion tool** to confirm if the user wants to proceed.
   - Proceed if the user confirms.

   **If no tasks file exists:** Proceed without task-related warning.

4. **Check if delta specs need syncing**

   Check for delta specs at `openspec/changes/<name>/specs/`. If none exist, proceed without sync prompt.

   **If delta specs exist:**
   - For each delta spec, extract requirement names and note which sections exist (ADDED, MODIFIED, REMOVED).
   - Check the corresponding main spec at `openspec/specs/<capability>/spec.md`:
     - If the main spec doesn't exist or if any ADDED requirements are missing, prompt the user to sync before archiving.
     - Use **AskUserQuestion tool** with options: "Sync now", "Archive without syncing".
     - If the user chooses to sync, execute /opsx:sync logic (use the openspec-sync-specs skill).

   **If already synced:** Proceed without prompting.

5. **Perform the archive**

   Create the archive directory if it doesn't exist:

   ```bash
   mkdir -p openspec/changes/archive
   ```

   Generate target name using the current date: `YYYY-MM-DD-<change-name>`.

   **Check if target already exists:**
   - If yes: Fail with an error, suggesting renaming the existing archive or using a different date.
   - If no: Move the change directory to archive.

   ```bash
   mv openspec/changes/<name> openspec/changes/archive/YYYY-MM-DD-<name>
   ```

6. **Display summary**

   Show archive completion summary including:
   - Change name
   - Schema that was used
   - Archive location
   - Whether specs were synced (if applicable)
   - Note about any warnings (incomplete artifacts/tasks)

**Output On Success**

```
## Archive Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Archived to:** openspec/changes/archive/YYYY-MM-DD-<name>/
**Specs:** ✓ Synced to main specs (or "No delta specs" or "⚠️ Not synced")

All artifacts complete. All tasks complete.
```

**Guardrails**
- Always prompt for change selection if not provided.
- Use artifact graph (openspec status --json) for completion checking.
- Don't block archive on warnings - just inform and confirm.
- Preserve .openspec.yaml when moving to archive (it moves with the directory).
- Show a clear summary of what happened.
- If sync is requested, use openspec-sync-specs approach (agent-driven).