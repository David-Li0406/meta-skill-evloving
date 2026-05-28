---
name: create-pull-request
description: Use this skill when you need to create a pull request from the current branch to the main branch.
---

# Create Pull Request

## Instructions

1. Ensure you are on a branch that is not `main` or `master`.
2. Check for uncommitted changes and resolve them if present.
3. Compare the current branch with the `main` branch to review changes:
   ```bash
   git log origin/main..HEAD --oneline
   git diff origin/main...HEAD --stat
   ```
4. Generate a clear and descriptive title and summary for the pull request:
   - **Title Format**: `Feature: [Descriptive title based on commits]`
   - **Body Structure**:
     ```markdown
     ## Summary
     - Key functionality delivered
     - Major components implemented
     - Value provided to users

     ## Implementation Details
     - Technical approach and architecture decisions
     - Integration points with existing codebase
     - Notable patterns or utilities used

     ## Testing
     - Unit tests added for core functionality
     - Integration tests for end-to-end workflows
     - Manual testing performed
     ```
5. Push the branch to the remote repository if it hasn't been pushed yet:
   ```bash
   git push origin HEAD
   ```
6. Create the pull request using the GitHub CLI:
   ```bash
   gh pr create --title "Feature: [Generated title]" --body "$(cat <<'EOF'
   [Generated PR body]
   EOF
   )"
   ```
7. Display the URL of the created pull request.

## Notes
- Ensure that the PR title and body are clear and professional.
- The PR should be created with the assignee set to `@me`.