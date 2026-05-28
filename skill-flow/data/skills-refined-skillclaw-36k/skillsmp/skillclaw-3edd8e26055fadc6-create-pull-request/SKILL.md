---
name: create-pull-request
description: Use this skill when you have finished a task and are ready to submit changes for review by creating a GitHub pull request.
---

# Create Pull Request

Creates a GitHub pull request using the project's PR template and standard workflows.

## Workflow

### Step 1: Pre-Submission Checks

1. **Inspect Git State**: Run `git status -sb` to identify uncommitted or untracked changes and confirm which files to include. Avoid modifying unrelated files.
2. **Lint and Typecheck**: Ensure all checks pass.
   ```bash
   bun run lint && bun run typecheck
   ```
3. **Tests**: Ensure tests pass.
   ```bash
   bun run test
   ```

### Step 2: Stage and Commit Changes

1. **Stage Changes**: Use `git add <paths>` for the approved files only, then re-check status.
2. **Commit**: Generate a Conventional Commit message when requested and run:
   ```bash
   git commit -m "<message>"
   ```

### Step 3: Push Changes

1. **Push**: Push the current branch to origin.
   ```bash
   git push -u origin HEAD
   ```

### Step 4: Create PR

1. **Build PR Body**: Read `.github/pull_request_template.md` if present and fill required sections (Summary, Type of Change, Related Issues). Keep checkboxes accurate.
2. **Ask for Confirmation**: Confirm with the user before creating the PR.
3. **Execute**: Use the `gh` CLI to create the PR.
   ```bash
   gh pr create --title "feat: <description>" --body "$(cat .github/pull_request_template.md)" --draft (if needed)
   ```

## Best Practices

- **Small PRs**: Keep PRs focused on a single change.
- **Succinct Descriptions**: Focus on the "why" and "how to test".
- **Draft PRs**: Use draft status if the work is still in progress but you want feedback.
- **Link Issues**: Link related GitHub issues to the PR.

## Notes

- Follow repo conventions for templates and required sections.
- Require explicit confirmation before any network operations: `git push`, `gh pr create`.