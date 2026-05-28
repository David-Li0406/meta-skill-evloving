---
name: github-pr-management
description: Use this skill when you need to create, review, or manage GitHub pull requests (PRs) and related operations.
---

# Skill body

## Overview

This skill automates the workflow for creating and reviewing GitHub pull requests (PRs), including necessary checks and comments.

## Workflow

### 1. Create a Pull Request

Before creating a PR, ensure you have completed the following checks:

- Review the `CLAUDE.md` file for project-specific requirements.
- Run tests, linters, and build steps as specified.

#### Stage and Commit Changes

Stage files explicitly:

```bash
git add path/to/file1.txt path/to/file2.txt
```

Create a commit with a structured message:

```bash
git commit -m "$(cat <<'EOF'
<short description>

<detailed explanation (if necessary)>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

#### Push Changes

Push the current branch to the remote repository:

```bash
git push -u origin <branch-name>
```

#### Create the Pull Request

If a PR template exists at `.github/PULL_REQUEST_TEMPLATE.md`, use it; otherwise, create a PR with the following structure:

```markdown
## Overview
<Brief summary of changes in bullet points>

## Changes
<List of main changes>

## Testing
<How the changes were tested (if applicable)>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

Create the PR using:

```bash
gh pr create --title "<PR title>" --body "$(cat <<'EOF'
<PR body content>
EOF
)"
```

### 2. Review a Pull Request

To review a PR, ensure you have the `gh` CLI installed and authenticated.

#### Fetch PR Information

```bash
gh pr view <PR_NUMBER> --repo <OWNER/REPO>
```

#### Check Differences

```bash
gh pr diff <PR_NUMBER> --repo <OWNER/REPO>
```

#### Post Comments

To comment on a PR:

```bash
gh pr comment <PR_NUMBER> --repo <OWNER/REPO> --body "Your comment here"
```

#### Submit a Review

You can approve or request changes with:

```bash
gh pr review <PR_NUMBER> --repo <OWNER/REPO> --approve --body "Looks good!"
gh pr review <PR_NUMBER> --repo <OWNER/REPO> --request-changes --body "Please make the following changes."
```

### 3. Error Handling

- If any command fails, provide a clear error message in Japanese and suggest solutions.
- Always confirm with the user if there are any uncertainties during the process.

## Important Notes

1. Do not skip preparation steps; always follow the requirements in `CLAUDE.md`.
2. If tests or checks fail, resolve those issues before proceeding.
3. Always stage files explicitly; avoid using `git add .` or `git add -A`.
4. Communicate in Japanese unless specified otherwise.
5. If unsure about any step, ask the user for clarification.

## Output Files

Review results are saved automatically in the `.copilot-reviews/` directory with the format `{mode}_{context}_{timestamp}.md`.

**Example Output**:
```
.copilot-reviews/
├── staged_20231230_143052.md
└── branch_main-feature-auth_20231230_150123.md
```