---
name: github-expert
description: Complete toolset for GitHub repository management. Search code, manage issues/PRs, browse files, and perform git operations remotely. Use this skill to navigate codebases, track tasks, review code, and contribute changes via pull requests effectively.
compatibility: Requires github-mcp-server
---

# GitHub Expert

## Tools Overview

| Category | Tools | Use Case |
|----------|-------|----------|
| **Discovery** | `search_repositories`, `search_code`, `search_issues`, `search_users` | Finding repos, code snippets, bugs, or people |
| **Reading** | `get_file_contents`, `list_branches`, `list_commits`, `get_commit` | Exploring codebase state and history |
| **Issues** | `issue_read`, `issue_write`, `mcp_github_add_issue_comment` | Managing feature requests and bug reports |
| **PRs** | `list_pull_requests`, `pull_request_read`, `create_pull_request`, `pull_request_review_write` | Code review and merging changes |
| **Write** | `create_or_update_file`, `push_files`, `create_branch` | Modifying code and content remotely |

## Common Workflows

### 1. Repository Exploration
Before working, get context:
```javascript
// Find relevant repo
search_repositories(query: "topic:dotnet org:my-org")

// specific repo contents
get_file_contents(owner: "my-org", repo: "my-repo", path: "README.md")
list_branches(owner: "my-org", repo: "my-repo")
```

### 2. Code Search (Global & Local)
Use `search_code` to find usage patterns across the organization or within a repo.
```javascript
// Find call sites of a deprecated function
search_code(query: "MyDeprecatedFunction org:my-org")

// Find implementation of an interface
search_code(query: "interface IMyService repo:my-org/backend")
```

### 3. Issue Management
Read context before acting:
```javascript
// Search for existing bugs
search_issues(query: "is:issue is:open crash repo:my-org/app")

// Get full thread including comments
issue_read(owner: "my-org", repo: "app", issue_number: 123)

// Comment on issue
add_issue_comment(owner: "my-org", repo: "app", issue_number: 123, body: "Fixed in PR #456")
```

### 4. Pull Request Workflow
Standard contribution flow:
1. **Check Base**: `get_file_contents` to ensure you have latest state.
2. **Create Branch**: `create_branch(repo: "...", branch: "feature/login")`
3. **Commit Changes**: `create_or_update_file` or `push_files`
4. **Open PR**: 
```javascript
create_pull_request(
  owner: "my-org", 
  repo: "app", 
  title: "feat: Add login", 
  head: "feature/login", 
  base: "main",
  body: "Implements OAuth2..."
)
```

## Best Practices
- **Search First**: Before creating an issue, use `search_issues` to check for duplicates.
- **Context Awareness**: Use `get_file_contents` to read `CONTRIBUTING.md` if available.
- **Precision**: When searching code, scope to `org:` or `repo:` to reduce noise.
- **Reviews**: Use `pull_request_read` with `method: "get_review_comments"` to understand PR history before commenting.
