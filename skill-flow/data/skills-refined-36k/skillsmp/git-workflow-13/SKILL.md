---
name: git-workflow
description: A skill that outlines best practices for using Git in a collaborative development environment, including branching strategies, commit conventions, and pull request workflows.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Git Workflow Skill

## Tooling Notes

This skill should only use read-only commands and avoid modifying files.

## Workflow

Copy this checklist and use it to track your progress through the Git workflow process:

```markdown
Git Workflow Checklist

- [ ] Create a feature branch from the main branch.
- [ ] Make changes and commit frequently with clear, descriptive messages, using atomic commits.
- [ ] Rebase your feature branch onto the latest main branch to keep it up to date.
- [ ] Run tests and ensure all checks pass before pushing changes.
- [ ] Push your feature branch to the remote repository.
- [ ] Open a pull request (PR) against the main branch with a clear description of changes.
- [ ] Request reviews from team members and address any feedback.
- [ ] Once approved, merge the PR using a squash merge to maintain a clean commit history.
- [ ] Delete the feature branch after merging.
```

## Branching Strategy

Adopt the following branching strategy for effective collaboration:

- **Main Branch**: The stable branch that always reflects production-ready code.
- **Feature Branches**: Created from the main branch for developing new features or bug fixes. Named descriptively (e.g., `feature/user-authentication`).
- **Release Branches**: Optional branches created from the main branch for preparing a new production release.
- **Hotfix Branches**: Created from the main branch to quickly address critical bugs in production.

Here's a visual representation of the branching strategy:

```plaintext
        main
         |
    -----------------
    |       |       |
 feature1 feature2 hotfix1
```

## Commit Conventions

Follow these the Conventional Commits specification for commit messages:

- **Format**: `<type>(<scope>): <description>`
- **Types**:
  - `feat`: A new feature
  - `fix`: A bug fix
  - `docs`: Documentation changes
  - `style`: Code style changes (formatting, missing semicolons, etc.)
  - `refactor`: Code changes that neither fix a bug nor add a feature
  - `test`: Adding or updating tests
  - `chore`: Maintenance tasks (build process, dependencies, etc.)
- **Example**: `feat(auth): add user login functionality`

## Pull Request Workflow

When creating and managing pull requests, follow these best practices:

1. **Descriptive Title and Description**: Provide a clear title and detailed description of the changes made in the PR.
2. **Link Issues**: Reference any related issues in the PR description.
3. **Request Reviews**: Assign reviewers who are familiar with the codebase or the feature being changed.
4. **Address Feedback**: Respond to reviewer comments and make necessary changes promptly.
5. **Merge Strategy**: Use squash merging to combine all commits from the feature branch into a single commit on the main branch for a cleaner history.
6. **Post-Merge Actions**: Delete the feature branch and ensure the main branch is up to date locally.

## Branch Naming Conventions

Use the following conventions for naming branches:

- **Feature Branches**: `feature/<descriptive-name>`
- **Bugfix Branches**: `bugfix/<descriptive-name>`
- **Hotfix Branches**: `hotfix/<descriptive-name>`
- **Release Branches**: `release/<version-number>`
- **Example**: `feature/user-authentication`, `bugfix/login-error`, `hotfix/payment-issue`, `release/1.2.0`

## Common Git Commands

- Create a new branch:
  ```bash
  git checkout -b feature/your-feature-name
  ```
- Commit changes:
  ```bash
  git add .
  git commit -m "feat(scope): descriptive message"
  ```
- Rebase onto main:
  ```bash
  git fetch origin
  git rebase origin/main
  ```
- Push branch to remote:
  ```bash
  git push origin feature/your-feature-name
  ```
- Merge pull request (squash):
  ```bash
  git checkout main
  git pull origin main
  git merge --squash feature/your-feature-name
  git commit -m "Merge feature/your-feature-name"
  git push origin main
  ```
- Delete a branch:
  ```bash
  git branch -d feature/your-feature-name
  git push origin --delete feature/your-feature-name
  ```
