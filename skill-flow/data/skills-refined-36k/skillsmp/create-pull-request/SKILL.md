---
name: create-pull-request
description: Creates a GitHub pull request using the project's PR template and standard workflows. Handles branch pushing and PR creation via GitHub CLI. Use when you have finished a task and are ready to submit changes for review.
---

# Create Pull Request

Creates a GitHub pull request using the project's PR template and standard workflows.

## Project Documentation References

- **[AGENTS.md](../../../AGENTS.md)** - Central reference for all project documentation
- **[@git-conventions.md](../../.agent/rules/shared/git/git-conventions.md)** - Conventional commits and git workflows
- **[@github-automation.md](../../.agent/rules/shared/git/github-automation.md)** - GitHub project automation

## Workflow

### Step 1: Pre-Submission Checks

1. **Lint and Typecheck**: Ensure all checks pass.
   ```bash
   bun run lint && bun run typecheck
   ```
2. **Tests**: Ensure tests pass.
   ```bash
   bun run test
   ```

### Step 2: Push Changes

1. **Commit**: Use conventional commits as per @git-conventions.md.
2. **Push**: Push the current branch to origin.
   ```bash
   git push -u origin HEAD
   ```

### Step 3: Create PR

1. **Template**: The PR will automatically use the template in `.github/pull_request_template.md` when created via `gh pr create`.
2. **Execute**: Use the `gh` CLI to create the PR.
   ```bash
   gh pr create --title "feat: <description>" --body "$(cat .github/pull_request_template.md)" --draft (if needed)
   ```

## Instructions

1. **Analyze Changes**: Briefly summarize the changes for the PR body.
2. **Fill Template**: Use the sections from the template in `.github/pull_request_template.md`.
3. **Tenant Isolation**: Explicitly confirm tenant isolation is maintained in the PR summary.
4. **Link Issues**: Link related GitHub issues to the PR.

## Best Practices

- **Small PRs**: Keep PRs focused on a single change.
- **Succinct Descriptions**: Focus on the "why" and "how to test".
- **Draft PRs**: Use draft status if the work is still in progress but you want feedback.
