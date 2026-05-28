# github-repo-check Skill

Queries GitHub API to verify implementation status of components/features using PRs, issues, Actions, and deployments.

## Overview

This skill checks GitHub for remote evidence to determine component status. It queries:

1. **Pull Requests** - Open, merged, closed PRs mentioning the component
2. **Issues** - Tracking issues and their labels
3. **GitHub Actions** - CI/CD status
4. **Deployments** - Production deployment evidence

## Status Levels

| Status | Evidence Required |
|--------|-------------------|
| Shipped | Deployment to production exists |
| Complete | PR merged + CI passing, or PR merged to main |
| In Progress | Open PR (with or without reviews), or issue with "in progress" label |
| Planned | Open GitHub issue |
| Unknown | No GitHub evidence found |

## When to Use

- Directly: `/github-repo-check authentication`
- Automatically invoked by `/project-status` when GitHub repos are configured

## Prerequisites

1. **GitHub CLI authenticated**:
   ```bash
   gh auth status
   ```

2. **Repository configuration** in `.entourage/repos.json`:
   ```json
   {
     "github": {
       "defaultOrg": "my-org"
     },
     "repos": [
       {
         "name": "my-project",
         "path": "~/code/my-project",
         "github": "my-org/my-project"
       }
     ]
   }
   ```

## Testing the Skill

### Running Evaluations

1. Navigate to your context database:
   ```bash
   cd ~/my-context   # or ~/other-context
   ```

2. Start Claude Code with the plugin:
   ```bash
   claude --plugin-dir ~/your-plugin
   ```

3. Test directly:
   ```
   /github-repo-check authentication
   /github-repo-check user-dashboard payments
   ```

### Example Test Queries

| Test Case | Query |
|-----------|-------|
| Single component | `/github-repo-check auth` |
| Multiple components | `/github-repo-check auth dashboard payments` |
| Non-existent component | `/github-repo-check nonexistent-feature` |

### Expected Output Format

```markdown
## GitHub Scan: auth

| Repository | Evidence | Status | Confidence |
|------------|----------|--------|------------|
| my-org/my-project | PR #42 merged, CI passing | Complete | Very High |

### GitHub Details

**my-org/my-project:**
- PR: #42 "Add authentication" - merged Jan 8
- Actions: Build (success), Test (success)
- Reviews: 2 approvals
- Deployment: prod-v1.2.0 deployed Jan 8
```

## Authentication

The skill prefers `gh` CLI for authentication. If unavailable, falls back to token in `.entourage/repos.json`:

```json
{
  "github": {
    "token": "ghp_..."
  }
}
```

## Error Handling

| Error | Behavior |
|-------|----------|
| gh CLI not authenticated | Returns authentication instructions |
| 401 Unauthorized | Reports token issue |
| 403 Rate Limited | Reports rate limit, suggests local-only |
| 404 Not Found | Reports repo not found/accessible |

## Evaluation Logs

This skill is typically invoked by `/project-status`. Evaluation logs are stored with project-status results:

```
~/my-context/evaluations/project-status/
~/other-context/evaluations/project-status/
```

## Test Cases

See `evaluations/evaluation.json` for the full test suite covering:
- PR status detection (open, merged, closed)
- Issue status and labels
- GitHub Actions integration
- Deployment detection
- Authentication scenarios
- Error handling
