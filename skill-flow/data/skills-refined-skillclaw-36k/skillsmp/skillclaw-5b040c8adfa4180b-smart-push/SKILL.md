---
name: smart-push
description: Use this skill when you want to analyze changes, generate appropriate commit messages, and safely push to a remote repository.
---

# Smart Push Workflow

1. **Commit Message Suggestion**: Based on the analysis, suggest a commit message in the format 'type(scope): content'.
2. **Security Check**: Perform a final check to ensure that no sensitive information (e.g., passwords) is included in the files to be pushed.
3. **Execute Git Commands**: Run the following commands sequentially:
   ```bash
   git add .
   git commit -m "<suggested_commit_message>"
   git push origin main
   ```

## Execution Guide
1. Follow these instructions when the user requests to push changes.