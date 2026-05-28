---
name: code-review
description: A skill for reviewing software changes. It helps analyze differences between git references (branches, tags, commits), review history, and provide feedback to ensure code quality and adherence to project conventions.
metadata:
  version: "1.1"
---

# Review Changes

## When to use this skill

Use this skill when a user wants to review changes in a git repository. This includes:

- Comparing a feature branch to a target branch (e.g., `main`).
- Comparing two specific tags (e.g., `v1.0.0` vs `v1.1.0`).
- comparing arbitrary commits.
- Performing a pre-merge inspection.

This is useful for identifying potential bugs, ensuring consistent coding style, verifying commit message standards, and understanding the scope of changes between any two points in history.

## Instructions

### 1. Identify the Scope of Review

- **Identify References**: determine the `base_ref` (the starting point or "server" version) and the `target_ref` (the new changes or "feature" version).
  - Examples:
    - Feature Review: `base_ref` = `main`, `target_ref` = `feature/login`.
    - Release Comparison: `base_ref` = `v1.0.0`, `target_ref` = `v1.1.0`.
    - Commit Inspection: `base_ref` = `a1b2c3d`, `target_ref` = `e5f6g7h`.
- **Fetch Changes**: Ensure you have the latest objects from the remote if reviewing remote branches.
  - `git fetch --all`
  - **Note**: For PRs, you can fetch the PR head to a local branch using: `git fetch origin pull/<pr-number>/head:pr-<pr-number>`

### 2. Gather Context

- **Check Status**: Run `git status` to ensure your current working directory is clean if checking out files.
- **Review History**: Run `git log <base_ref>..<target_ref>` to review the commit history, messages, and authorship between the two references.
- **View Changes**:
  - **For Feature Branches (Divergence)**: Use `git diff <base_ref>...<target_ref>` (triple-dot). This shows changes in `target_ref` since it diverged from `base_ref`. This is usually what you want for Code Reviews / PRs.
  - **For Strict Comparison (Tags/Commits)**: Use `git diff <base_ref> <target_ref>` (two-dot or space). This shows the exact difference between the two snapshots, regardless of common history.

### 3. Analyze Commits

- **Commit Messages**: Check if they follow the project's format (e.g., Conventional Commits).
- **Commit Granularity**: Ensure commits are logical and atomic over the range being reviewed.

### 4. Analyze Code Changes

- **Conventions**: Verify adherence to project naming, formatting, and architectural patterns.
- **Safety & Security**: Look for hardcoded secrets, unsafe operations, or lack of error handling.
- **Test Coverage**: Check if new features or bug fixes include corresponding tests.
- **Difference Scope**: Be aware if you are looking at a diff of statics (two-dot) vs a diff of changes (triple-dot).

### 5. Provide Feedback

- Generate a structured review report highlighting:
  - **Summary**: High-level overview of the changes.
  - **References**: Clearly state which `base_ref` and `target_ref` were compared.
  - **Strengths**: What was done well.
  - **Issues/Suggestions**: Clear, actionable items for improvement, categorized by severity.
  - **Verification Status**: Mention if tests pass or if new tests are missing.

### 6. Finalize

- Ask the user if they would like you to automaticall fix any identified minor issues or if they need more deep-dive into specific files.
