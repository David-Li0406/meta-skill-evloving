---
name: commit
description: Run tests and commit changes if tests pass
---

Run tests and commit changes if tests pass.

## Instructions

0. Run the elm compiler on all changed or added files.  If there are any errors, display the and stop here.
1. Run `elm-test` to execute all tests
2. If tests fail:
   - Display the failure message to the user
   - Do NOT proceed with the commit
   - Stop here
3. If tests pass:
   - Run `git status` to see all changes
   - Run `git diff` to see the actual changes
   - Run `git log --oneline -3` to see recent commit style
   - Stage all relevant changed files (do not stage files that contain secrets)
   - Create a detailed commit message that:
     - Has a concise summary line explaining the purpose of the changes
     - Includes a body with bullet points describing the substance of changes
     - Ends with `Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>`
   - Commit the changes
   - Display the commit hash and summary to the user
