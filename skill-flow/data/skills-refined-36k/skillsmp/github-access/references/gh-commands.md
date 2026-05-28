# GitHub CLI (`gh`) Commands Reference

This document provides `gh` CLI commands for common GitHub operations. Use these when the `gh` binary is available.

## Prerequisites

Ensure `GH_TOKEN` environment variable is set:
```bash
echo $GH_TOKEN
```

Check `gh` is available:
```bash
which gh
```

## Actions / Workflows

### List Workflows
```bash
gh workflow list --repo OWNER/REPO
```

### List Workflow Runs
```bash
# List all runs for a specific workflow
gh run list --workflow WORKFLOW_NAME --repo OWNER/REPO

# List runs with specific status
gh run list --workflow WORKFLOW_NAME --status failure --repo OWNER/REPO

# List runs for a specific branch
gh run list --branch BRANCH_NAME --repo OWNER/REPO
```

### Get Workflow Run Details
```bash
gh run view RUN_ID --repo OWNER/REPO
```

### Get Workflow Run Logs
```bash
# View logs for a specific run
gh run view RUN_ID --log --repo OWNER/REPO

# View logs for failed jobs only
gh run view RUN_ID --log-failed --repo OWNER/REPO
```

### Get Job Logs
```bash
# List jobs for a run
gh run view RUN_ID --json jobs --jq '.jobs[] | {id, name, status, conclusion}'

# Get specific job logs (requires downloading)
gh run view RUN_ID --log --job JOB_ID --repo OWNER/REPO
```

### Trigger a Workflow
```bash
# Trigger with default inputs
gh workflow run WORKFLOW_NAME --ref BRANCH --repo OWNER/REPO

# Trigger with inputs
gh workflow run WORKFLOW_NAME --ref BRANCH --repo OWNER/REPO -f key1=value1 -f key2=value2
```

### Rerun Workflow
```bash
# Rerun entire workflow
gh run rerun RUN_ID --repo OWNER/REPO

# Rerun only failed jobs
gh run rerun RUN_ID --failed --repo OWNER/REPO
```

### Cancel Workflow Run
```bash
gh run cancel RUN_ID --repo OWNER/REPO
```

### Download Workflow Artifacts
```bash
# List artifacts for a run
gh run view RUN_ID --repo OWNER/REPO --json artifacts

# Download all artifacts from a run
gh run download RUN_ID --repo OWNER/REPO

# Download specific artifact
gh run download RUN_ID --name ARTIFACT_NAME --repo OWNER/REPO
```

### Watch Workflow Run
```bash
# Watch a workflow run in real-time
gh run watch RUN_ID --repo OWNER/REPO
```

## Issues

### Search Issues
```bash
# Search issues in a repository
gh issue list --search "QUERY" --repo OWNER/REPO

# Search with filters
gh issue list --state open --label bug --repo OWNER/REPO

# Search across all repos
gh search issues "QUERY" --owner OWNER
```

### Get Issue Details
```bash
gh issue view ISSUE_NUMBER --repo OWNER/REPO

# Get issue with comments
gh issue view ISSUE_NUMBER --comments --repo OWNER/REPO

# Get issue as JSON
gh issue view ISSUE_NUMBER --json title,body,state,labels,comments --repo OWNER/REPO
```

### List Issue Comments
```bash
gh issue view ISSUE_NUMBER --comments --repo OWNER/REPO

# Get comments as JSON
gh issue view ISSUE_NUMBER --json comments --jq '.comments' --repo OWNER/REPO
```

### Create Issue
```bash
gh issue create --title "TITLE" --body "BODY" --repo OWNER/REPO

# With labels and assignees
gh issue create --title "TITLE" --body "BODY" --label bug --assignee USERNAME --repo OWNER/REPO
```

### Update Issue
```bash
# Update title
gh issue edit ISSUE_NUMBER --title "NEW_TITLE" --repo OWNER/REPO

# Update body
gh issue edit ISSUE_NUMBER --body "NEW_BODY" --repo OWNER/REPO

# Add labels
gh issue edit ISSUE_NUMBER --add-label LABEL --repo OWNER/REPO

# Close issue
gh issue close ISSUE_NUMBER --repo OWNER/REPO

# Reopen issue
gh issue reopen ISSUE_NUMBER --repo OWNER/REPO
```

### Add Comment to Issue
```bash
gh issue comment ISSUE_NUMBER --body "COMMENT" --repo OWNER/REPO
```

### List Issues
```bash
# List open issues
gh issue list --repo OWNER/REPO

# List with filters
gh issue list --state all --label bug --assignee USERNAME --repo OWNER/REPO

# List as JSON
gh issue list --json number,title,state,labels --repo OWNER/REPO
```

## Pull Requests

### Search Pull Requests
```bash
# Search PRs in a repository
gh pr list --search "QUERY" --repo OWNER/REPO

# Search with filters
gh pr list --state open --label bug --author USERNAME --repo OWNER/REPO

# Search across repos
gh search prs "QUERY" --owner OWNER
```

### Get Pull Request Details
```bash
gh pr view PR_NUMBER --repo OWNER/REPO

# Get PR with comments
gh pr view PR_NUMBER --comments --repo OWNER/REPO

# Get PR as JSON
gh pr view PR_NUMBER --json title,body,state,commits,files --repo OWNER/REPO
```

### Get PR Comments
```bash
# Get all comments (regular + review comments)
gh pr view PR_NUMBER --comments --repo OWNER/REPO

# Get as JSON
gh pr view PR_NUMBER --json comments,reviews --repo OWNER/REPO
```

### Get PR Diff
```bash
gh pr diff PR_NUMBER --repo OWNER/REPO
```

### Get PR Status/Checks
```bash
# View PR checks
gh pr checks PR_NUMBER --repo OWNER/REPO

# View checks with detailed status
gh pr view PR_NUMBER --json statusCheckRollup --jq '.statusCheckRollup' --repo OWNER/REPO
```

### Get PR Files Changed
```bash
# List files changed in PR
gh pr view PR_NUMBER --json files --jq '.files[] | {path, additions, deletions}' --repo OWNER/REPO
```

### Create Pull Request
```bash
# Create PR (interactive)
gh pr create --repo OWNER/REPO

# Create PR with details
gh pr create --title "TITLE" --body "BODY" --base main --head BRANCH --repo OWNER/REPO

# Create draft PR
gh pr create --title "TITLE" --body "BODY" --draft --repo OWNER/REPO
```

### Update Pull Request
```bash
# Update title
gh pr edit PR_NUMBER --title "NEW_TITLE" --repo OWNER/REPO

# Update body
gh pr edit PR_NUMBER --body "NEW_BODY" --repo OWNER/REPO

# Mark as ready for review
gh pr ready PR_NUMBER --repo OWNER/REPO

# Convert to draft
gh pr edit PR_NUMBER --draft --repo OWNER/REPO

# Add reviewers
gh pr edit PR_NUMBER --add-reviewer USERNAME --repo OWNER/REPO
```

### Merge Pull Request
```bash
# Merge with default method
gh pr merge PR_NUMBER --repo OWNER/REPO

# Merge with specific method
gh pr merge PR_NUMBER --merge --repo OWNER/REPO    # merge commit
gh pr merge PR_NUMBER --squash --repo OWNER/REPO   # squash and merge
gh pr merge PR_NUMBER --rebase --repo OWNER/REPO   # rebase and merge

# Auto-merge when checks pass
gh pr merge PR_NUMBER --auto --repo OWNER/REPO
```

### Add Comment to PR
```bash
gh pr comment PR_NUMBER --body "COMMENT" --repo OWNER/REPO
```

### Review Pull Request
```bash
# Approve PR
gh pr review PR_NUMBER --approve --repo OWNER/REPO

# Request changes
gh pr review PR_NUMBER --request-changes --body "FEEDBACK" --repo OWNER/REPO

# Comment on PR
gh pr review PR_NUMBER --comment --body "COMMENT" --repo OWNER/REPO
```

### List Pull Requests
```bash
# List open PRs
gh pr list --repo OWNER/REPO

# List with filters
gh pr list --state all --label bug --author USERNAME --repo OWNER/REPO

# List as JSON
gh pr list --json number,title,state,headRefName --repo OWNER/REPO
```

## Discussions

### List Discussions
```bash
gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    discussions(first: 10) {
      nodes {
        id
        title
        body
        number
      }
    }
  }
}' -f owner=OWNER -f repo=REPO
```

### Get Discussion
```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    discussion(number: $number) {
      id
      title
      body
      comments(first: 10) {
        nodes {
          body
          author {
            login
          }
        }
      }
    }
  }
}' -f owner=OWNER -f repo=REPO -F number=DISCUSSION_NUMBER
```

## Common Patterns

### Check PR Workflow Status and Get Failure Logs

```bash
# 1. Get PR checks status
gh pr checks PR_NUMBER --repo OWNER/REPO

# 2. Get the most recent workflow run for the PR
RUN_ID=$(gh pr view PR_NUMBER --json headRefName --jq -r '.headRefName' | xargs -I {} gh run list --branch {} --limit 1 --json databaseId --jq '.[0].databaseId' --repo OWNER/REPO)

# 3. View failed logs
gh run view $RUN_ID --log-failed --repo OWNER/REPO
```

### Extract Owner/Repo from URL

```bash
# From a GitHub URL like https://github.com/owner/repo/issues/123
# Extract owner and repo using:
echo "https://github.com/owner/repo/issues/123" | sed -E 's|https://github.com/([^/]+)/([^/]+)/.*|\1/\2|'
```

## Tips

- Use `--json` flag to get structured output that can be parsed with `jq`
- Use `--repo OWNER/REPO` to specify repository, or run commands from within a git repository
- Set `GH_TOKEN` environment variable for authentication
- Use `gh api` for endpoints not covered by `gh` subcommands
- Many commands support `--web` flag to open the resource in a browser
