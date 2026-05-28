---
name: openspec-continue-change
description: Use this skill when you want to progress an OpenSpec change by creating the next artifact in your workflow.
---

# Skill body

Continue working on a change by creating the next artifact.

**Input**: Optionally specify a change name. If omitted, prompt for available changes.

**Steps**

1. **If no change name provided, prompt for selection**  
   Run `openspec list --json` to get available changes sorted by most recently modified. Use the **AskUserQuestion tool** to let the user select which change to work on. Present the top 3-4 most recently modified changes as options, showing:
   - Change name
   - Schema (from `schema` field if present, otherwise "spec-driven")
   - Status (e.g., "0/5 tasks", "complete", "no tasks")
   - How recently it was modified (from `lastModified` field)  
   Mark the most recently modified change as "(Recommended)" since it's likely what the user wants to continue.  
   **IMPORTANT**: Do NOT guess or auto-select a change. Always let the user choose.

2. **Check current status**  
   ```bash
   openspec status --change "<name>" --json
   ```  
   Parse the JSON to understand the current state. The response includes:
   - `schemaName`: The workflow schema being used (e.g., "spec-driven", "tdd")
   - `artifacts`: Array of artifacts with their status ("done", "ready", "blocked")
   - `isComplete`: Boolean indicating if all artifacts are complete

3. **Act based on status**:

   ---

   **If all artifacts are complete (`isComplete: true`)**:
   - Congratulate the user
   - Show final status including the schema used
   - Suggest: "All artifacts created! You can now implement this change or archive it."
   - STOP

   ---

   **If artifacts are ready to create** (status shows artifacts with `status: "ready"`):
   - Pick the FIRST artifact with `status: "ready"` from the status output
   - Get its instructions:
     ```bash
     openspec instructions <artifact-id> --change "<name>" --json
     ```
   - Parse the JSON to get template, dependencies, and what it unlocks
   - **Create the artifact file** using the template as a starting point:
     - Read any completed dependency files for context
     - Fill in the template based on context and user's goals
     - Write to the output path specified in instructions
   - Show what was created and what's now unlocked
   - STOP after creating ONE artifact

   ---

   **If no artifacts are ready**:
   - Inform the user that there are no artifacts ready to create at this time.
   - Suggest checking the status of existing artifacts or completing any blocked tasks.