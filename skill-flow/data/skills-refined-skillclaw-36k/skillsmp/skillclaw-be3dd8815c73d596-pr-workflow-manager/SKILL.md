---
name: pr-workflow-manager
description: Use this skill when you want to manage the complete pull request workflow from local changes to an opened PR.
---

# Skill body

1. **Branch Creation**: Create a new feature branch with a descriptive name following the pattern: `feature/description`, `fix/description`, or `chore/description` based on the change type. Never work directly on the main branch.

2. **Commit Changes**: Use the `git-commit-crafter` skill to create commits for your changes.

3. **Push Branch**: Push the new branch to the remote repository using:
   ```bash
   git push -u origin branch-name
   ```

4. **Create PR Body**: Generate a pull request description that matches the scope and complexity of the changes:
   - **For simple/focused changes** (e.g., documentation updates, single-file fixes):
     - Keep it concise (2-4 sentences)
     - State what was changed and why
     - Example: "Removes implementation details from README. Users don't need to know about internal algorithms. This keeps docs focused on user-facing functionality."
   - **For complex changes** (e.g., new features, multiple components):
     - **Summary**: Brief overview of changes
     - **What Changed**: Bullet points of specific modifications
     - **Why**: Motivation and context for the changes
     - **Testing**: (optional) How the changes were validated
     - **Related Issues**: (optional) Link any relevant issues

5. **Open Pull Request**: Use the following command to create the PR with the generated body:
   ```bash
   gh pr create
   ```
   Then open it in the browser using:
   ```bash
   gh pr view --web
   ```

**Important Guidelines**:
- Match verbosity to change complexity.
- Avoid unnecessary sections for simple changes.
- Include "Testing" only when meaningful validation was performed.
- Link related PRs when relevant.
- Keep language clear and direct.