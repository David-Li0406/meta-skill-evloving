# Troubleshooting GitHub CLI

Common problems and solutions when working with GitHub CLI.

## Authentication Issues

### Error: HTTP 401: Unauthorized

**Symptom:**
```
! error: HTTP 401: Unauthorized (https://api.github.com/...)
```

**Causes:**
- Not authenticated with `gh`
- Token expired or revoked
- Invalid token

**Solutions:**

1. **Check authentication status:**
```bash
gh auth status
```

2. **If not authenticated, login:**
```bash
gh auth login
```

3. **If using GitHub Enterprise:**
```bash
gh auth login --hostname github.company.com
```

4. **If token exists but doesn't work, refresh:**
```bash
gh auth logout
gh auth login
```

5. **Verify token has required scopes:**
```bash
gh auth status --show-token
```

Check that scopes include `repo`, `workflow`, etc. as needed.

### Error: HTTP 403: Forbidden

**Symptom:**
```
! error: HTTP 403: Forbidden (https://api.github.com/...)
! Resource not accessible by integration
```

**Causes:**
- Insufficient permissions
- Token lacks required scopes
- Rate limit exceeded
- Repository/organization restrictions

**Solutions:**

1. **Check rate limit:**
```bash
gh api rate_limit
```

If rate limited:
```json
{
  "rate": {
    "remaining": 0,
    "reset": 1234567890
  }
}
```

Wait until reset time, or authenticate to increase limit (5000/hour vs 60/hour).

2. **Check repository permissions:**
```bash
gh repo view
```

Verify you have write access if trying to create/edit resources.

3. **Check token scopes:**
```bash
gh auth status --show-token
```

Re-authenticate with additional scopes:
```bash
gh auth refresh --scopes repo,workflow,admin:org
```

4. **Check organization restrictions:**

Some organizations restrict OAuth app access. Contact org admin or use personal access token with appropriate permissions.

### Token Scopes Required

Different operations require different token scopes:

| Operation | Required Scope |
|-----------|----------------|
| Read public repos | `public_repo` |
| Read/write private repos | `repo` |
| Create/manage workflows | `workflow` |
| Manage org settings | `admin:org` |
| Manage secrets | `repo` (full) |
| Delete repositories | `delete_repo` |
| Manage webhooks | `admin:repo_hook` |

**Add scopes:**
```bash
gh auth refresh --scopes repo,workflow,admin:org
```

### GitHub Enterprise Authentication

**Connect to Enterprise instance:**
```bash
gh auth login --hostname github.company.com
```

**Switch between accounts:**
```bash
# Use specific hostname
gh api repos/{owner}/{repo} --hostname github.company.com

# Or set environment variable
export GH_HOST=github.company.com
gh repo list
```

## Repository Access Issues

### Error: Could not resolve to a Repository

**Symptom:**
```
! could not resolve to a Repository with the name 'owner/repo'
```

**Causes:**
- Repository doesn't exist
- Private repository without access
- Typo in repository name
- Not authenticated (for private repos)

**Solutions:**

1. **Verify repository exists:**
```bash
# Visit in browser
gh browse --repo owner/repo

# Or check with API
gh api repos/owner/repo
```

2. **Check spelling:**
```bash
# Search for repository
gh repo list owner --limit 100 | grep -i repo-name
```

3. **Verify access to private repo:**
```bash
# Ensure authenticated
gh auth status

# Check permissions
gh api repos/owner/repo --jq '.permissions'
```

### Error: Not in a Git Repository

**Symptom:**
```
! not a git repository (or any of the parent directories): .git
```

**Cause:**
- Command requires git repository context
- Not in a directory tracked by git

**Solution:**

1. **Navigate to git repository:**
```bash
cd /path/to/your/repo
```

2. **Or specify repository explicitly:**
```bash
gh pr list --repo owner/repo
```

3. **Initialize git repository if needed:**
```bash
git init
git remote add origin https://github.com/owner/repo
```

## Pull Request Issues

### Error: Pull Request Already Exists

**Symptom:**
```
! a pull request for branch "feature-x" into branch "main" already exists
```

**Cause:**
- PR already created for this head/base branch combination

**Solution:**

1. **Find existing PR:**
```bash
gh pr list --head feature-x
```

2. **View existing PR:**
```bash
PR_NUM=$(gh pr list --head feature-x --json number --jq '.[0].number')
gh pr view "$PR_NUM"
```

3. **Update existing PR or close and create new one:**
```bash
# Update title/body
gh pr edit "$PR_NUM" --title "New title"

# Or close and create new
gh pr close "$PR_NUM"
gh pr create --title "..." --body "..."
```

### Error: No Commits Between Branches

**Symptom:**
```
! pull request create failed: no commits between main and feature-x
```

**Cause:**
- Feature branch has no unique commits compared to base branch

**Solution:**

1. **Verify commits exist:**
```bash
git log main..feature-x
```

If no output, branches are identical.

2. **Ensure changes are committed:**
```bash
git status
git add .
git commit -m "Your changes"
```

3. **Push commits:**
```bash
git push
```

### Error: Branch Not Found on Remote

**Symptom:**
```
! error: branch not found on remote
```

**Cause:**
- Branch not pushed to remote repository

**Solution:**

```bash
# Push current branch
git push -u origin $(git branch --show-current)

# Then create PR
gh pr create
```

## Issue/PR Editing Issues

### Error: Issue/PR Not Found

**Symptom:**
```
! issue not found
! pull request not found
```

**Causes:**
- Wrong issue/PR number
- Issue/PR in different repository
- Issue/PR deleted

**Solution:**

1. **Verify number:**
```bash
# List issues
gh issue list --limit 100

# Search for issue
gh issue list --search "some keywords"
```

2. **Check if in correct repository:**
```bash
gh repo view
```

3. **Specify repository explicitly:**
```bash
gh issue view 123 --repo owner/repo
```

### Error: Label Not Found

**Symptom:**
```
! label not found: xyz
```

**Cause:**
- Label doesn't exist in repository

**Solution:**

1. **List available labels:**
```bash
gh label list
```

2. **Create missing label:**
```bash
gh label create xyz --color ff0000 --description "Description"
```

3. **Use API for bulk label creation:**
```bash
gh api repos/{owner}/{repo}/labels \
  -f name=xyz \
  -f color=ff0000
```

## GitHub Actions Issues

### Error: Workflow Not Found

**Symptom:**
```
! could not find any workflows named "ci.yml"
```

**Causes:**
- Workflow file doesn't exist
- Wrong filename
- Workflow not in `.github/workflows/`

**Solution:**

1. **List available workflows:**
```bash
gh workflow list
```

2. **Check workflow file location:**
```bash
ls .github/workflows/
```

3. **Use correct workflow identifier:**
```bash
# By filename
gh workflow run ci.yml

# By workflow ID
gh workflow list
gh workflow run 123456
```

### Error: Workflow Run Not Found

**Symptom:**
```
! could not find any workflow run with ID "123456789"
```

**Causes:**
- Wrong run ID
- Run deleted
- Run in different repository

**Solution:**

1. **List recent runs:**
```bash
gh run list --limit 20
```

2. **Search for specific run:**
```bash
gh run list --workflow ci.yml
gh run list --branch main
gh run list --user @me
```

3. **Get latest run:**
```bash
LATEST=$(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')
gh run view "$LATEST"
```

## API-Specific Issues

### Error: HTTP 404: Not Found

**Symptom:**
```
! HTTP 404: Not Found (https://api.github.com/...)
```

**Causes:**
- Wrong endpoint path
- Resource doesn't exist
- Missing API version

**Solution:**

1. **Check endpoint in documentation:**
Visit https://docs.github.com/en/rest

2. **Verify resource exists:**
```bash
# Check repository
gh repo view owner/repo

# Check issue
gh issue view 123
```

3. **Use correct API version:**
```bash
gh api repos/owner/repo \
  -H "Accept: application/vnd.github.v3+json"
```

### Error: HTTP 422: Validation Failed

**Symptom:**
```
! HTTP 422: Validation Failed
! Errors:
!   - field: required
```

**Causes:**
- Missing required fields
- Invalid field values
- Wrong field types

**Solution:**

1. **Check API documentation for required fields**

2. **Verify field types:**
```bash
# Use -F for typed fields (numbers, booleans)
gh api repos/owner/repo/issues \
  -F assignees='["user1"]' \  # Array
  -F milestone=1              # Number

# Use -f for strings
gh api repos/owner/repo/issues \
  -f title="String title"
```

3. **Read validation error details:**
```bash
gh api repos/owner/repo/issues -X POST -f title="" 2>&1 | jq .
```

### API Rate Limit Exceeded

**Symptom:**
```
! API rate limit exceeded for user ID 12345
```

**Cause:**
- Exceeded API rate limit (60/hour unauthenticated, 5000/hour authenticated)

**Solution:**

1. **Check rate limit status:**
```bash
gh api rate_limit
```

Output:
```json
{
  "rate": {
    "limit": 5000,
    "remaining": 0,
    "reset": 1234567890
  }
}
```

2. **Wait until reset time:**
```bash
RESET=$(gh api rate_limit --jq '.rate.reset')
NOW=$(date +%s)
WAIT=$((RESET - NOW))
echo "Wait $WAIT seconds"
sleep $WAIT
```

3. **Authenticate for higher limit:**
```bash
gh auth login
```

4. **Use GraphQL for complex queries** (counts as 1 request instead of many):
```bash
gh api graphql -f query='
  query {
    repository(owner: "owner", name: "repo") {
      issues(first: 100) {
        nodes { number title }
      }
    }
  }
'
```

5. **Cache results:**
```bash
gh api repos/owner/repo/issues --cache 1h
```

## Permission Issues

### Error: Resource Not Accessible by Integration

**Symptom:**
```
! Resource not accessible by integration
```

**Cause:**
- Token/app lacks required permissions
- Workflow GITHUB_TOKEN has insufficient permissions

**Solution:**

1. **For personal access tokens, add scopes:**
```bash
gh auth refresh --scopes repo,workflow,admin:org
```

2. **For workflow GITHUB_TOKEN, update workflow permissions:**
```yaml
permissions:
  contents: write
  pull-requests: write
  issues: write
```

3. **Check organization settings:**
Some organizations restrict app permissions. Contact org admin.

### Error: Protected Branch Update Failed

**Symptom:**
```
! Required status check "ci" is expected
! Cannot merge because required reviews are not satisfied
```

**Cause:**
- Branch protection rules not satisfied

**Solution:**

1. **Check branch protection settings:**
```bash
gh api repos/owner/repo/branches/main/protection
```

2. **Ensure all checks pass:**
```bash
gh pr checks 123
```

3. **Get required approvals:**
```bash
gh pr review 123 --approve
```

4. **Bypass protection (if admin):**
```bash
gh pr merge 123 --admin
```

## Command-Specific Errors

### Error: Unknown Flag

**Symptom:**
```
! unknown flag: --invalid-flag
```

**Solution:**

**Always check help for correct flags:**
```bash
gh pr create --help
gh issue list --help
gh run view --help
```

Each subcommand has specific flags. Don't assume flags work across commands.

### Error: Ambiguous Argument

**Symptom:**
```
! ambiguous argument '123': both revision and filename
```

**Cause:**
- Git command confusion with gh command

**Solution:**

Make sure you're using `gh` commands, not `git`:
```bash
# Wrong
git pr view 123

# Correct
gh pr view 123
```

## Output and Formatting Issues

### Error: Parse Error in JSON

**Symptom:**
```
! parse error: Invalid numeric literal
```

**Cause:**
- Invalid jq query
- Malformed JSON output

**Solution:**

1. **Test jq query separately:**
```bash
gh pr view 123 --json title | jq '.'
gh pr view 123 --json title | jq '.title'
```

2. **Check for empty results:**
```bash
gh pr list --json number | jq 'if length == 0 then "No PRs" else .[].number end'
```

3. **Handle nulls:**
```bash
gh issue view 123 --json milestone --jq '.milestone.title // "No milestone"'
```

## Environment Issues

### Error: GH_TOKEN or GITHUB_TOKEN Not Set

**Symptom:**
```
! gh_token or github_token environment variable required
```

**Cause:**
- Running in CI/CD without token
- Token environment variable not set

**Solution:**

1. **Use gh auth:**
```bash
gh auth login
```

2. **Or set environment variable:**
```bash
export GH_TOKEN=ghp_xxxxxxxxxxxxx
```

3. **In GitHub Actions:**
```yaml
- name: Do something with gh
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: gh pr list
```

### Error: Command Not Found: gh

**Symptom:**
```
bash: gh: command not found
```

**Cause:**
- GitHub CLI not installed
- Not in PATH

**Solution:**

1. **Install GitHub CLI:**
```bash
# macOS
brew install gh

# Linux (Debian/Ubuntu)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Windows
winget install gh
```

2. **Verify installation:**
```bash
gh --version
```

## Debugging Tips

### Enable Verbose Output

```bash
# See full HTTP request/response
gh api repos/owner/repo --verbose

# Debug gh commands
GH_DEBUG=1 gh pr list

# See API calls
GH_DEBUG=api gh pr list
```

### Check Configuration

```bash
# View gh configuration
gh config list

# View specific config value
gh config get git_protocol

# Set config value
gh config set git_protocol ssh
```

### Test Authentication

```bash
# Check auth status
gh auth status

# Test API access
gh api user

# Test with specific hostname
gh auth status --hostname github.company.com
```

### Validate JSON

```bash
# Pretty-print JSON
gh pr view 123 --json title,body | jq '.'

# Validate JSON structure
gh pr list --json number | jq type
```

## Getting Help

### Built-in Help

**Always start with --help:**
```bash
gh --help                # List all commands
gh pr --help             # PR commands
gh pr create --help      # Specific command
gh api --help            # API usage with examples
```

### Check Version

```bash
gh --version
```

Update if outdated:
```bash
# macOS
brew upgrade gh

# Linux
sudo apt update && sudo apt upgrade gh

# Or download latest from https://cli.github.com/
```

### Community Resources

- **GitHub CLI Manual:** https://cli.github.com/manual/
- **GitHub CLI Repository:** https://github.com/cli/cli
- **GitHub Community:** https://github.community/
- **Stack Overflow:** Tag questions with `github-cli`

### Report Bugs

```bash
# Create issue in gh repository
gh repo view cli/cli --web
# Then click "Issues" -> "New Issue"
```

## Prevention Strategies

1. **Always check --help first** before guessing command syntax
2. **Test with --json output** to see raw data structure
3. **Use --dry-run** where available to preview changes
4. **Check authentication** before starting operations
5. **Verify repository context** for repo-specific commands
6. **Handle rate limits** in batch operations
7. **Save work frequently** in long-running scripts
8. **Use verbose/debug modes** when troubleshooting
9. **Keep gh updated** to latest version
10. **Read error messages carefully** - they often contain the solution

## Quick Diagnostics Checklist

When something isn't working:

- [ ] Run `gh auth status` - Am I authenticated?
- [ ] Run `gh repo view` - Am I in the right repository?
- [ ] Run `gh <command> --help` - Am I using the right syntax?
- [ ] Check error message - What does it say?
- [ ] Search this troubleshooting guide for the error
- [ ] Try with `--verbose` or `GH_DEBUG=1` for more details
- [ ] Check GitHub Status - Is there an outage? (https://www.githubstatus.com/)
- [ ] Try the operation in web UI - Same issue?
- [ ] Check rate limits - `gh api rate_limit`
- [ ] Update gh - `gh version` and compare to latest

Most issues can be resolved by checking these basics!
