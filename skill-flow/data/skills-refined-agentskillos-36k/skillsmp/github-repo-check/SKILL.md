---
name: github-repo-check
description: Verify implementation status by querying GitHub API for PRs, issues, Actions, and deployments. Use when checking remote repo activity.
---

## Purpose

Query GitHub API to verify implementation status of components/features. Returns evidence-based status levels using PR, issue, Actions, and deployment data.

## When to Use

- Directly invoked: `/github-repo-check authentication`
- Checking PR/issue status for a component
- Verifying CI/CD and deployment status
- When invoked by other skills (like `/project-status`)

## Input

Component or feature name(s) to verify. Examples:
- `/github-repo-check authentication`
- `/github-repo-check user-dashboard payments`

**Note:** Component searches are case-insensitive. `/github-repo-check Auth` and `/github-repo-check auth` will find the same PRs and issues.

---

## Authentication

### Step 1: Check gh CLI Availability

The `gh` CLI is preferred because it handles authentication automatically.

```bash
gh auth status 2>/dev/null && echo "gh available" || echo "gh not available"
```

### Step 2: Authentication Method

**If gh CLI is available and authenticated:**
Use `gh api` commands directly. No additional configuration needed.

**If gh CLI is unavailable:**
Fall back to `GITHUB_TOKEN` environment variable from `.env.local`:

```bash
# .env.local
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
```

Use curl with the token:
```bash
curl -H "Authorization: token $TOKEN" "https://api.github.com/..."
```

---

## Configuration Discovery

### Step 1: Check for Config File

Use the Read tool to check if `.entourage/repos.json` exists.

**If the file does not exist:**
```
> No repository configuration found. Create `.entourage/repos.json` with your repository settings.
```

### Step 2: Extract GitHub Repos

Look for `github` field in each repo entry (format: `owner/repo`):

```json
{
  "repos": [
    {
      "name": "entourage-web",
      "path": "~/code/entourage-web",
      "github": "my-entourage/entourage-web"
    }
  ]
}
```

### Step 3: No GitHub Configuration

If no repos have a `github` field configured:
```
> No GitHub configuration found. Add `github` field to repos in `.entourage/repos.json`.
```

---

## GitHub API Queries

For each component/feature, run these queries against each configured GitHub repo:

### 1. Search PRs Mentioning Component

```bash
# Using gh CLI
gh api "search/issues?q=repo:OWNER/REPO+type:pr+COMPONENT_NAME" --jq '.items[] | {number, title, state, merged_at}'

# Using curl
curl -H "Authorization: token $TOKEN" \
  "https://api.github.com/search/issues?q=repo:OWNER/REPO+type:pr+COMPONENT_NAME"
```

### 2. Recent Merged PRs

```bash
gh api "repos/OWNER/REPO/pulls?state=closed&base=main&per_page=20" \
  --jq '.[] | select(.merged_at != null) | {number, title, merged_at}'
```

### 3. Search Issues

```bash
gh api "search/issues?q=repo:OWNER/REPO+type:issue+COMPONENT_NAME" \
  --jq '.items[] | {number, title, state, labels: [.labels[].name]}'
```

### 4. GitHub Actions Status

```bash
gh api "repos/OWNER/REPO/actions/runs?branch=main&per_page=5" \
  --jq '.workflow_runs[] | {name, conclusion, created_at}'
```

### 5. Deployments (if configured)

```bash
gh api "repos/OWNER/REPO/deployments?environment=production&per_page=5" \
  --jq '.[] | {environment, created_at, description}'
```

### 6. Check PR Reviews (for open PRs)

```bash
gh api "repos/OWNER/REPO/pulls/PR_NUMBER/reviews" \
  --jq '.[] | {state, user: .user.login}'
```

---

## Evidence Synthesis

Apply this decision tree to determine component status:

```
1. Deployment to production exists for this component?
   YES -> Status: Shipped (Very High confidence)

2. PR merged + most recent Actions run passing?
   YES -> Status: Done (Very High confidence)

3. PR merged to main?
   YES -> Status: Done (High confidence)

4. Open PR with approving reviews?
   YES -> Status: In Review (High confidence)

5. Open PR (review requested)?
   YES -> Status: In Review (Medium confidence)

6. Open PR (no reviews)?
   YES -> Status: In Progress (Medium confidence)

7. GitHub Issue with "in progress" or similar label?
   YES -> Status: In Progress (Medium confidence)

8. GitHub Issue exists (open)?
   YES -> Status: Backlog (High confidence)

9. No GitHub evidence found?
   -> Status: Unknown
   -> Output: "No GitHub evidence found. Defer to /local-repo-check for local evidence."
```

---

## Error Handling

### gh CLI Not Authenticated
```
> gh CLI not authenticated. Run `gh auth login` or add `GITHUB_TOKEN` to `.env.local`.
```

### Token Invalid/Expired
If API returns 401:
```
> GitHub API error: 401 Unauthorized. Run `gh auth login` or check your token.
```

### Rate Limited
If API returns 403 with rate limit headers:
```
> GitHub API rate limit reached. Resets at [time]. Using local evidence only.
```

### Repository Not Found
If API returns 404:
```
> Repository 'owner/repo' not found or not accessible. Check `github` field in repos.json.
```

---

## Output Format

### With GitHub Configuration

```markdown
## GitHub Scan: [Component Name]

| Repository | Evidence | Status | Confidence |
|------------|----------|--------|------------|
| owner/repo | PR #42 merged, CI passing | Done | Very High |

### GitHub Details

**owner/repo:**
- PR: #42 "Add authentication" - merged Jan 8
- Actions: Build, Test passed
- Deployment: prod-v1.2.0 (Jan 8 14:32 UTC)
```

### Without GitHub Configuration

```markdown
## GitHub Scan

No GitHub configuration found. Add `github` field to repos in `.entourage/repos.json`.

Example:
{
  "repos": [
    {
      "name": "my-repo",
      "path": "~/code/my-repo",
      "github": "owner/my-repo"
    }
  ]
}
```

### Multiple Components

When checking multiple components, output a summary table followed by details:

```markdown
## GitHub Scan Summary

| Component | Status | Evidence | Source | Confidence |
|-----------|--------|----------|--------|------------|
| auth | Done | PR #42 merged, CI passing | owner/repo | Very High |
| dashboard | In Review | PR #48 open, 2 approvals | owner/repo | High |
| payments | Backlog | Issue #52 created | owner/repo | High |

### Details

[Per-component GitHub details...]
```

---

## Example

**Query:** `/github-repo-check clerk-auth`

**Output:**

```markdown
## GitHub Scan: clerk-auth

| Repository | Evidence | Status | Confidence |
|------------|----------|--------|------------|
| my-entourage/entourage-web | PR #42 merged, CI passing | Done | Very High |

### GitHub Details

**my-entourage/entourage-web:**
- PR: #42 "Add Clerk authentication provider" - merged Jan 8
- Actions: Build (success), Test (success), Lint (success)
- Reviews: 2 approvals from @alice, @bob
- Deployment: prod-v1.2.0 deployed Jan 8 14:32 UTC
```

---

## After Output

This skill returns results to the calling context (usually `/project-status`). **Do not stop execution.**
Continue with the next step in the workflow or TODO list.
