---
name: end-development-session
description: Use this skill when you want to conclude a development session and document the progress made.
---

# Skill body

End the current development session by following these steps:

1. **Check Active Session**: 
   - Read the contents of `.claude/sessions/.current-session` to find the active session filename.
   - If no active session exists, inform the user that there is nothing to end.

2. **Append Summary**: 
   - If a session exists, append a comprehensive summary to the session log, including:
     - **Session Duration**: Calculate and record the total time spent on the session.
     - **Git Summary**:
       - Total files changed (added/modified/deleted).
       - List all changed files with their change types.
       - Number of commits made (if any).
       - Final git status.
     - **TODO Summary**:
       - Total tasks completed and remaining.
       - List all completed tasks.
       - List any incomplete tasks with their status.
     - **Key Accomplishments**: Summarize significant achievements during the session.
     - **Features Implemented**: Document all features that were completed.
     - **Problems Encountered**: Note any issues faced and their solutions.
     - **Breaking Changes**: Highlight any important findings or changes that could affect future work.
     - **Dependencies**: List any dependencies that were added or removed.
     - **Configuration Changes**: Document any changes made to the configuration.
     - **Deployment Steps**: Outline any deployment actions taken.
     - **Lessons Learned**: Share insights gained during the session.
     - **Unfinished Work**: Note what was not completed and any follow-up actions needed.
     - **Tips for Future Developers**: Provide advice for others who may work on this project.

3. **Cleanup**: 
   - Clear the contents of the `.claude/sessions/.current-session` file (do not delete the file itself).

4. **Inform User**: 
   - Notify the user that the session has been documented successfully.
   - Optionally, display a summary of the session duration and completed goals.

The summary should be detailed enough for another developer (or AI) to understand everything that occurred during the session without needing to read the entire log.