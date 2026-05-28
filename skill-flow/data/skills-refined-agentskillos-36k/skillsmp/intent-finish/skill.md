---
name: intent-finish
description: Mark an intent as complete and move to done folder. Use when the user has finished working on an intent and wants to document completion, add PR links, and archive it.
user-invocable: true
---

# Intent Finish

You are helping the user mark an intent as complete.

## Workflow

1. Check `~/.claude-intents/in-progress/` for intents filtered by current repository:
   - Get current repository name: `basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $(pwd)`
   - List only intents where the folder name contains the current repository name
   - Intent folder format: `YYYY-mm-dd-{repository-name}-{intent-description}`
2. Ask which intent to mark as done (if multiple) or confirm the intent
3. Read the spec.md to understand the intent
4. Generate a **summary.md** file with a concise summary:
   - **Title**: Brief, clear title from the spec
   - **Problem**: Short description of the issue (1-2 sentences from spec's Problem section)
   - **Solution**: How it was fixed (2-3 bullet points from spec's Solution section)
   - **Key Changes**: List the main files/components modified
   - **Testing**: Steps to verify the fix
   - Keep it concise - this is a quick reference, not a copy of the full spec
5. Generate a **fix.diff** file with the changes made:
   - Run `git diff` from the main/master branch to capture all changes
   - Use: `git diff $(git rev-parse --verify main 2>/dev/null || git rev-parse --verify master 2>/dev/null || echo HEAD~10)..HEAD`
   - If no git repo, skip this step and note that no diff is available
   - Save the raw diff output to `fix.diff`
6. Ask: "Was a PR created for this intent? If yes, provide the PR URL"
7. Ask: "Any final notes or learnings to document?"
8. Update the spec.md:
   - Change status from "In Progress" to "Completed"
   - Add completion date
   - Add PR link (if provided)
   - Add "## Completion Summary" section with final notes
9. Move the entire intent folder from `~/.claude-intents/in-progress/` to `~/.claude-intents/done/`
10. Confirm the intent has been marked as complete and show the summary.md content

## Example spec.md update

```diff
- **Status:** In Progress
+ **Status:** Completed
+ **Date Completed:** YYYY-MM-DD
+ **PR:** [Link to PR](url)

+## Completion Summary
+[Final notes and learnings]
```

## Example summary.md format

```markdown
# [Title from spec]

## Problem
[Short description of the issue - 1-2 sentences]

## Solution
- Change 1
- Change 2
- Change 3

## Key Changes
- `path/to/file1.ts` - Description of change
- `path/to/file2.ts` - Description of change

## Testing
1. Step 1 to test
2. Step 2 to test
3. Expected result

## PR
[Link to PR](url) (if applicable)
```

## Example fix.diff

The `fix.diff` file contains the raw git diff output:

```diff
diff --git a/src/component.ts b/src/component.ts
index abc123..def456 100644
--- a/src/component.ts
+++ b/src/component.ts
@@ -10,6 +10,8 @@ export function example() {
+  // New code added
+  return result;
}
```

## Important Notes

- **Intents folder:** All intents are stored in `~/.claude-intents/`
- **Repository filtering:** Only show intents that match the current repository name. Get repository name with: `basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $(pwd)`
- Intent folder naming format: `YYYY-mm-dd-{repository-name}-{intent-description}`
- Search for intents in `~/.claude-intents/in-progress/`
- Move completed intents to `~/.claude-intents/done/`
- Create `~/.claude-intents/done/` directory if it doesn't exist
- Preserve all files when moving (spec.md, notes.md, summary.md, fix.diff)
- Show before/after path for confirmation
- The summary.md should be an extra short, concise summary - not a copy of the full spec
- The fix.diff captures all code changes for future reference
