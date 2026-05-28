# GitHub REST API with `curl` Reference

This document provides `curl` commands for GitHub REST API operations when `gh` is not available.

**Official Documentation:**
- REST API Getting Started (curl): https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api?apiVersion=2022-11-28&tool=curl

## Prerequisites

Ensure `GH_TOKEN` environment variable is set:
```bash
echo $GH_TOKEN
```

## Common Headers

All requests should include:
```bash
-H "Accept: application/vnd.github+json" \
-H "Authorization: token $GH_TOKEN" \
-H "X-GitHub-Api-Version: 2022-11-28"
```

**Note**: Both `Authorization: token $GH_TOKEN` and `Authorization: Bearer $GH_TOKEN` formats work for personal access tokens. This reference uses `token` format for consistency and reliability.

## Actions / Workflows

### List Workflows
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows
```

### List Workflow Runs
```bash
# List all runs for a workflow
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/actions/workflows/WORKFLOW_ID/runs"

# With filters (status, branch, etc.)
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/actions/workflows/WORKFLOW_ID/runs?status=failure&branch=main"
```

### Get Workflow Run
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/runs/RUN_ID
```

### Get Workflow Run Logs
```bash
# Returns redirect URL to download logs archive
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/runs/RUN_ID/logs
```

### List Workflow Jobs
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/runs/RUN_ID/jobs

# Filter for failed jobs
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/actions/runs/RUN_ID/jobs?filter=failed"
```

### Get Job Logs
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/jobs/JOB_ID/logs
```

### Trigger Workflow
```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/WORKFLOW_ID/dispatches \
  -d '{"ref":"BRANCH","inputs":{"key1":"value1","key2":"value2"}}'
```

### Rerun Workflow
```bash
# Rerun entire workflow
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/runs/RUN_ID/rerun

# Rerun failed jobs
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/runs/RUN_ID/rerun-failed-jobs
```

### Cancel Workflow Run
```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/runs/RUN_ID/cancel
```

### List Workflow Run Artifacts
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/runs/RUN_ID/artifacts
```

### Download Workflow Artifact
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/artifacts/ARTIFACT_ID/zip \
  -o artifact.zip
```

### Delete Workflow Run Logs
```bash
curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/runs/RUN_ID/logs
```

## Issues

### Search Issues
```bash
# Search issues in a repository
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/search/issues?q=QUERY+repo:OWNER/REPO+type:issue"

# Example: Search open bugs
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/search/issues?q=is:open+label:bug+repo:OWNER/REPO+type:issue"
```

### Get Issue
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER
```

### List Issue Comments
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/comments
```

### Create Issue
```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues \
  -d '{"title":"TITLE","body":"BODY","labels":["bug"],"assignees":["USERNAME"]}'
```

### Update Issue
```bash
curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER \
  -d '{"title":"NEW_TITLE","state":"closed","labels":["bug","fixed"]}'
```

### Add Comment to Issue
```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/comments \
  -d '{"body":"COMMENT_TEXT"}'
```

### List Issues
```bash
# List issues with filters
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/issues?state=open&labels=bug&per_page=30&page=1"
```

## Pull Requests

### Search Pull Requests
```bash
# Search PRs in a repository
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/search/issues?q=QUERY+repo:OWNER/REPO+type:pr"

# Example: Search open PRs by author
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/search/issues?q=is:open+author:USERNAME+repo:OWNER/REPO+type:pr"
```

### Get Pull Request
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER
```

### Get PR Comments
```bash
# Get issue comments (regular comments)
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/PR_NUMBER/comments

# Get review comments (inline code comments)
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER/comments
```

### Get PR Reviews
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER/reviews
```

### Get PR Diff
```bash
curl -L \
  -H "Accept: application/vnd.github.diff" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER
```

### Get PR Files
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER/files
```

### Get PR Commits
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER/commits
```

### Get Combined Status (Checks)
```bash
# Get the combined status for the PR's HEAD commit
# First get the PR to find the HEAD SHA
PR_DATA=$(curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER)

HEAD_SHA=$(echo "$PR_DATA" | jq -r '.head.sha')

# Then get the combined status
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/commits/$HEAD_SHA/status

# Get check runs (newer checks API)
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/commits/$HEAD_SHA/check-runs
```

### Create Pull Request
```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls \
  -d '{"title":"TITLE","body":"BODY","head":"HEAD_BRANCH","base":"BASE_BRANCH","draft":false}'
```

### Update Pull Request
```bash
curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER \
  -d '{"title":"NEW_TITLE","body":"NEW_BODY","state":"open"}'
```

### Merge Pull Request
```bash
curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER/merge \
  -d '{"commit_title":"TITLE","commit_message":"MESSAGE","merge_method":"merge"}'

# merge_method can be: "merge", "squash", or "rebase"
```

### Request Reviewers
```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER/requested_reviewers \
  -d '{"reviewers":["USERNAME1","USERNAME2"]}'
```

### Add Comment to PR
```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/PR_NUMBER/comments \
  -d '{"body":"COMMENT_TEXT"}'
```

### List Pull Requests
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/pulls?state=open&per_page=30&page=1"
```

## Discussions (GraphQL)

GitHub Discussions use the GraphQL API. Use the following pattern:

```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/graphql \
  -d '{"query":"GRAPHQL_QUERY_HERE"}'
```

### List Discussions
```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/graphql \
  -d '{
    "query": "query($owner: String!, $repo: String!) { repository(owner: $owner, name: $repo) { discussions(first: 10) { nodes { id title body number } } } }",
    "variables": {
      "owner": "OWNER",
      "repo": "REPO"
    }
  }'
```

### Get Discussion with Comments
```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/graphql \
  -d '{
    "query": "query($owner: String!, $repo: String!, $number: Int!) { repository(owner: $owner, name: $repo) { discussion(number: $number) { id title body comments(first: 10) { nodes { body author { login } } } } } }",
    "variables": {
      "owner": "OWNER",
      "repo": "REPO",
      "number": DISCUSSION_NUMBER
    }
  }'
```

## Common Patterns

### Extract Owner/Repo from URL
```bash
# From https://github.com/owner/repo/issues/123
# Extract with sed or parameter expansion
URL="https://github.com/owner/repo/issues/123"
OWNER_REPO=$(echo "$URL" | sed -E 's|https://github.com/([^/]+/[^/]+)/.*|\1|')
OWNER=$(echo "$OWNER_REPO" | cut -d'/' -f1)
REPO=$(echo "$OWNER_REPO" | cut -d'/' -f2)
```

### Check PR Workflow Status and Get Failure Logs

```bash
# 1. Get PR details
PR_DATA=$(curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER)

# 2. Extract HEAD SHA
HEAD_SHA=$(echo "$PR_DATA" | jq -r '.head.sha')

# 3. Get check runs for that SHA
curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/commits/$HEAD_SHA/check-runs | jq '.check_runs[] | {name, status, conclusion}'

# 4. Get workflow runs for the HEAD SHA
RUNS=$(curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/actions/runs?head_sha=$HEAD_SHA")

# 5. Get first failed run ID
FAILED_RUN_ID=$(echo "$RUNS" | jq -r '.workflow_runs[] | select(.conclusion == "failure") | .id' | head -1)

# 6. Get failed jobs for that run
curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/actions/runs/$FAILED_RUN_ID/jobs?filter=failed" | jq '.jobs[] | {name, conclusion}'

# 7. Get logs for a specific failed job
JOB_ID=$(curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/actions/runs/$FAILED_RUN_ID/jobs?filter=failed" | jq -r '.jobs[0].id')

curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/jobs/$JOB_ID/logs
```

## Pagination

Most list endpoints support pagination:
```bash
# Use per_page and page parameters
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/issues?per_page=100&page=2"

# Parse Link header for next page
curl -I -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/issues" | grep -i "link:"
```

## Rate Limiting

Check rate limit status:
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/rate_limit
```

## Tips

- Always include the three standard headers: Accept, Authorization, and X-GitHub-Api-Version
- Use `jq` to parse JSON responses
- The `-L` flag follows redirects (important for some endpoints like log downloads)
- GitHub API uses cursor-based pagination for some endpoints (GraphQL) and page-based for REST
- Search queries use special syntax: `is:open`, `label:bug`, `author:username`, etc.
- For binary content (like artifacts), use `-o filename` to save to file

## Troubleshooting

If you encounter authentication issues (401, 403, 404 errors) or need help with authorization headers, see `references/troubleshooting.md` for detailed troubleshooting guidance.
