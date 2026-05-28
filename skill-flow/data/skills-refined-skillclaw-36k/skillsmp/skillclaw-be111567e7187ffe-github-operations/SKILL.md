---
name: github-operations
description: Use this skill to automate and manage various GitHub operations via the `gh` CLI, including repositories, issues, pull requests, workflows, and more.
---

# Skill body

## Capabilities

- **Repositories**: Create, clone, fork, view, and manage repositories.
- **Issues**: Create, list, view, close, reopen, comment, and label issues.
- **Pull Requests**: Create, review, merge, list, and comment on pull requests.
- **Workflows**: View and manage GitHub Actions workflows.
- **Gists**: Create and manage gists.
- **Search**: Search repositories, issues, pull requests, code, and users.
- **Security**: Monitor code security alerts and manage discussions.

## Prerequisites

- **gh CLI installed**: Install from [GitHub CLI](https://cli.github.com/).
- **Authenticated**: Run `gh auth login` to authenticate.
- **Verify**: Run `gh auth status` to confirm authentication.

## Instructions

### Phase 1: Understand the Request
1. Clarify what GitHub operation the user needs.
2. Identify the target repository (if not specified, ask).
3. Confirm any destructive operations before executing.

### Phase 2: Execute the Operation
Use `gh` CLI commands. Common patterns:

**Repository Operations**
```bash
gh repo view <owner>/<repo>
gh repo clone <owner>/<repo>
gh repo create <name> --public/--private
gh repo list <owner>
```

**Issue Operations**
```bash
gh issue list --repo <owner>/<repo>
gh issue create --repo <owner>/<repo> --title "Title" --body "Body"
gh issue view <number> --repo <owner>/<repo>
gh issue close <number> --repo <owner>/<repo>
gh issue reopen <number> --repo <owner>/<repo>
gh issue comment <number> --repo <owner>/<repo> --body "Comment"
```

**Pull Request Operations**
```bash
gh pr list --repo <owner>/<repo>
gh pr create --repo <owner>/<repo> --title "Title" --body "Body"
gh pr view <number> --repo <owner>/<repo>
gh pr merge <number> --repo <owner>/<repo>
gh pr review <number> --repo <owner>/<repo> --approve/--comment/--request-changes
```

**Actions Workflows**
```bash
gh workflow list --repo <owner>/<repo>
gh workflow run <workflow.yml> --repo <owner>/<repo>
gh run list --repo <owner>/<repo>
gh run view <run-id> --repo <owner>/<repo>
```

**Releases**
```bash
gh release list --repo <owner>/<repo>
gh release create <tag> --repo <owner>/<repo>
```

**Search Operations**
```bash
gh search repos <query>
gh search issues <query>
gh search prs <query>
gh search code <query>
```