# Branch Naming Conventions

Standard conventions for Git branch names when working with Jira issues.

## Branch Name Format

```
{type}/{issueKey}-{slug}
```

**Components:**
- `type`: Branch purpose (feature, fix, hotfix, etc.)
- `issueKey`: Jira issue key (e.g., PROJ-123)
- `slug`: URL-safe summary derived from issue title

## Branch Types

| Type | Purpose | Example |
|------|---------|---------|
| `feature` | New functionality | `feature/proj-123-add-login` |
| `fix` | Bug fixes | `fix/proj-456-null-pointer` |
| `hotfix` | Urgent production fixes | `hotfix/proj-789-security-patch` |
| `release` | Release preparation | `release/proj-100-v2.0` |
| `docs` | Documentation changes | `docs/proj-200-api-docs` |
| `refactor` | Code refactoring | `refactor/proj-300-auth-module` |
| `test` | Test additions/fixes | `test/proj-400-unit-tests` |
| `chore` | Maintenance tasks | `chore/proj-500-deps-update` |

## Issue Type Mapping

Jira issue types automatically map to branch types:

| Jira Issue Type | Branch Type |
|-----------------|-------------|
| Bug, Defect | `fix` |
| Story, Task, New Feature | `feature` |
| Enhancement, Improvement | `feature` |
| Documentation | `docs` |
| Technical Debt | `refactor` |
| Hotfix | `hotfix` |

## Naming Rules

### Do's
- Use lowercase letters only
- Use hyphens to separate words
- Keep issue key visible for traceability
- Keep total length under 100 characters

### Don'ts
- Avoid spaces (use hyphens)
- Avoid special characters except hyphens
- Avoid uppercase letters
- Avoid very long branch names

## Examples

### From Issue: PROJ-123 "Add user authentication feature"
```
feature/proj-123-add-user-authentication-feature
```

### From Issue: PROJ-456 "Fix login timeout error"
```
fix/proj-456-fix-login-timeout-error
```

### From Issue: PROJ-789 "Critical security vulnerability"
```
hotfix/proj-789-critical-security-vulnerability
```

## Custom Patterns

Override the default pattern per project:

```
devflow_git_link_repo(
  projectKey: "PROJ",
  repositoryUrl: "https://github.com/company/repo",
  branchPattern: "{key}-{type}-{slug}"
)
```

This produces: `proj-123-feature-add-login`

## Pattern Placeholders

| Placeholder | Description |
|-------------|-------------|
| `{type}` | Branch type (feature, fix, etc.) |
| `{key}` | Issue key in lowercase |
| `{slug}` | Slugified issue summary |

## Slug Generation

The slug is created from the issue summary:
1. Convert to lowercase
2. Replace spaces with hyphens
3. Remove special characters
4. Collapse multiple hyphens
5. Truncate to fit within max length
