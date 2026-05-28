---
name: git-jira-integration
description: Integration between Git workflows and Jira issues. Generates branch names from issues, validates commit messages, and provides PR context from Jira specifications.
license: MIT
compatibility: Requires mcp-jira with configured Jira instance
metadata:
  author: ximplicity
  version: "1.0"
  category: integration
---

# Git-Jira Integration Skill

Bridges Git workflows with Jira project management. Provides consistent naming, validation, and context generation to maintain traceability between code and issues.

## Allowed Operations

- Link Git repositories to Jira projects
- Generate branch names from Jira issues
- Validate commit messages against conventions
- Generate PR context from Jira specifications
- List linked repositories

## Forbidden Operations

These are NOT performed by this skill - agents have their own Git tools:

- Execute Git commands (clone, pull, push, commit)
- Create/merge Pull Requests directly
- Modify repository settings
- Access repository files or code

## MCP Tools

| Tool | Purpose |
|------|---------|
| `devflow_git_link_repo` | Link repository to Jira project |
| `devflow_git_get_repos` | List linked repositories |
| `devflow_git_branch_name` | Generate branch name from issue |
| `devflow_git_validate_commit` | Validate commit message format |
| `devflow_git_pr_context` | Generate PR title, body, checklist |

## Constraints

- Branch names follow pattern: `{type}/{issueKey}-{slug}`
- Commit messages should follow Conventional Commits
- Commit messages should include issue key reference
- PR context requires existing Jira issues

## Quick Reference

### Branch Naming

Generate branch name:
```
devflow_git_branch_name(issueKey: "PROJ-123")
```

Result: `feature/proj-123-add-user-authentication`

### Commit Validation

Validate commit message:
```
devflow_git_validate_commit(
  message: "feat(auth): add login page\n\nRefs: PROJ-123",
  projectKey: "PROJ",
  requireIssueKey: true
)
```

### PR Context

Generate PR context:
```
devflow_git_pr_context(
  issueKeys: ["PROJ-123", "PROJ-124"],
  includeAcceptanceCriteria: true
)
```

For detailed conventions, see [BRANCH-CONVENTIONS.md](references/BRANCH-CONVENTIONS.md).

For commit message format, see [COMMIT-MESSAGE-FORMAT.md](references/COMMIT-MESSAGE-FORMAT.md).

For PR templates, see [PR-TEMPLATES.md](references/PR-TEMPLATES.md).

## Example Workflow

1. **Start work on issue:**
   ```
   # Get branch name from Jira issue
   devflow_git_branch_name(issueKey: "PROJ-123")
   # Agent creates branch with their git tools
   ```

2. **Validate commits:**
   ```
   # Before committing, validate message
   devflow_git_validate_commit(message: "feat: add login")
   ```

3. **Create PR:**
   ```
   # Get PR context from Jira
   devflow_git_pr_context(issueKeys: ["PROJ-123"])
   # Agent creates PR with their gh/git tools
   ```

## Repository Linking

Link a repository to get project-specific defaults:

```
devflow_git_link_repo(
  projectKey: "PROJ",
  repositoryUrl: "https://github.com/company/project",
  defaultBranch: "develop",
  branchPattern: "{type}/{key}-{slug}"
)
```

List linked repositories:
```
devflow_git_get_repos()
devflow_git_get_repos(projectKey: "PROJ")
```
