---
name: pull-request-workflow
description: Use this skill when you need to create a pull request (PR) following a structured workflow, ensuring all necessary checks and documentation are completed.
---

# Pull Request Creation Workflow

This skill guides you through the process of creating a pull request (PR) in a structured manner, ensuring that all necessary steps are followed for a successful submission.

## Steps

1. **Check for Existing PRs**
   - Verify if there are any unmerged PRs in the repository.

2. **Update Main Branch**
   - Ensure your main branch is up to date:
     ```bash
     git checkout main
     git pull origin main
     ```

3. **Create a Feature Branch**
   - Create a new branch for your changes:
     ```bash
     git checkout -b feature/{feature-name}
     ```

4. **Make Changes and Commit**
   - Make your changes and commit them with a clear message:
     ```bash
     git add .
     git commit -m "feat({feature-name}): implement {feature-description}"
     ```

5. **Run Tests and Linting**
   - Execute the project's test and linting commands to ensure code quality:
     ```bash
     # Example for Node.js projects
     npm run lint
     npm test
     ```

6. **Push Changes and Create PR**
   - Push your changes to the remote repository:
     ```bash
     git push -u origin feature/{feature-name}
     ```
   - Create the PR using the GitHub CLI:
     ```bash
     gh pr create --base main --title "[{feature-name}] Implementation" --body "$(cat <<'EOF'
## Overview
{feature-description}

## Verification Status
- [x] Build passed
- [x] Tests passed
- [x] Security checks passed
- [x] Documentation consistency checked
EOF
)"
     ```

7. **Fill Out PR Template**
   - Ensure the PR description includes:
     - Summary of changes
     - Steps to verify functionality
     - Any relevant issue links

8. **Final Checks**
   - Confirm that no sensitive information (like `.env` files) is included in the commit.
   - Provide the PR URL to the user after creation.

## Checklist Before PR Creation
- [ ] Confirm that all changes are committed and pushed.
- [ ] Ensure that tests and linters have passed.
- [ ] Review the PR description for completeness.
- [ ] Obtain user confirmation before creating the PR.

## Error Handling
- If tests or linters fail, halt the PR creation process and prompt the user to fix the issues.
- If there are merge conflicts, guide the user to resolve them before proceeding.