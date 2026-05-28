---
name: intent-list
description: List all open intents with progress tracking. Use when the user wants to see what intents are in progress, check completion status, or get an overview of their work.
user-invocable: true
---

# Intent List

You are helping the user view their intents.

## Workflow

1. Intents folder is `~/.claude-intents/`
2. Get current repository name for filtering:
   - Run: `basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $(pwd)`
3. Check if `{intents_folder}/in-progress/` exists
4. List all folders in `{intents_folder}/in-progress/`
5. Filter intents by current repository:
   - Intent folder format: `YYYY-mm-dd-{repository-name}-{intent-description}`
   - Only show intents where the folder name contains the current repository name
6. For each matching intent folder:
   - Read the spec.md file
   - Extract: title, date started, and status
   - Show a summary

7. Display in this format:
   ```
   ## Open Intents

   ### 1. [Intent Title]
   - **Folder:** {intents_folder}/in-progress/YYYY-mm-dd-{repo}-{description}/
   - **Started:** YYYY-MM-DD
   - **Status:** In Progress
   - **Requirements:** X/Y completed

   ### 2. [Another Intent]
   ...
   ```

8. If no open intents exist for the current repository, say: "No open intents found for this repository. Use `/intent-start` to begin a new intent."

9. Optionally, offer to show done intents if the user wants to see them

## Important Notes

- **Intents folder:** All intents are stored in `~/.claude-intents/`
- **Repository filtering:** Only show intents that match the current repository name
- To get the current repository name, run: `basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $(pwd)`
- Intent folder naming format: `YYYY-mm-dd-{repository-name}-{intent-description}`
- Search for open intents in `~/.claude-intents/in-progress/`
- Search for done intents in `~/.claude-intents/done/`
- Count checkboxes in spec.md to show progress (e.g., "3/5 requirements completed")
- Sort by date (newest first)
- Make the output scannable and concise
