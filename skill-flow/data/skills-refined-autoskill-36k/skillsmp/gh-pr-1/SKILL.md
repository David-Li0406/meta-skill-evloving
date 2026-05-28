---
name: gh-pr
description: GitHub PR creation, update, and review-comment response using gh CLI. Use when asked to create/open a PR, draft a PR body, view PRs/diffs/comments, or reply to PR feedback.
---

# Gh Pr

## Overview

Create/update GitHub PRs and respond to review comments using gh CLI with clean, repeatable steps.

## Workflow Decision Tree

- **Create or update PR**: user asks to open/create/draft PR or wants a PR body.
- **Inspect PR**: user asks to view PR, diff, or status.
- **Reply to review comments**: user asks to address PR feedback or comment threads.

## Create or Update PR

1) **Preflight**

- Check branch and changes: `git status`, `git diff`, `git log -1`.
- Confirm base branch and target repo if unclear.
- Run smallest relevant test; note command and result.

1) **Draft PR body**

Use a short, concise body that explains the changes.

1) **Create or update PR**

- If creating: use `gh pr create` with title/body from above.
- If updating: `gh pr edit <num>` to adjust title/body.

## Inspect PR

- Active PR: `gh pr view --json number,title --jq '"PR #\(.number): \(.title)"'`.
- Diff: `gh pr diff <num>`.
- Status/checks: `gh pr view <num>`.

## Reply to Review Comments

1) **Load comments**

- `gh pr view <num> --comments`.
- If needed: `gh api repos/:owner/:repo/pulls/<num>/comments --paginate`.

1) **Respond**

- Cite fix with file/line: `path:line`.
- Resolve threads only after fix lands.

## Reporting

- Include: files touched, tests run, risks/unknowns.
- Keep short; bullet list ok.
