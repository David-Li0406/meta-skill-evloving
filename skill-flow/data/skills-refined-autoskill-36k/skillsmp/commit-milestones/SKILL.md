---
name: commit-milestones
description: Automatically commit changes when reaching major milestones
---

# Auto-Commit at Milestones

You should proactively commit changes to git whenever you complete a significant milestone, such as:

- Completing a feature implementation
- Fixing a bug
- Finishing a refactor
- Completing a set of tests
- Reaching a natural stopping point in work

When committing:
1. Review the changes with `git status` and `git diff`
2. Stage relevant files with `git add`
3. Create a descriptive commit message that explains what was accomplished
4. Commit with the standard co-authored format
5. Ask the user if they want to push to GitHub

Do this automatically without asking permission unless the changes are unclear or sensitive.
