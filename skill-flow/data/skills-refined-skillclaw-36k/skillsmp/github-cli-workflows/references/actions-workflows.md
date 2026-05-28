# GitHub Actions Workflows

Comprehensive patterns for monitoring and managing GitHub Actions using GitHub CLI.

## Quick Reference

```bash
gh run list              # List workflow runs
gh run view [id]         # View run details
gh run watch [id]        # Watch run in real-time
gh run rerun [id]        # Rerun workflow
gh run cancel [id]       # Cancel running workflow
gh run download [id]     # Download run artifacts
gh run delete [id]       # Delete run

gh workflow list         # List workflows
gh workflow view [id]    # View workflow details
gh workflow enable [id]  # Enable workflow
gh workflow disable [id] # Disable workflow
gh workflow run [id]     # Manually trigger workflow
```

**Remember:** Use `gh run --help` and `gh workflow --help` for detailed options.

## Listing Workflow Runs

### Basic Listing

```bash
gh run list                    # Recent runs in current repo
gh run list --limit 50         # Limit number of results
gh run list --workflow ci.yml  # Runs for specific workflow
```

### Filtering Runs

**By status:**
```bash
gh run list --status completed
gh run list --status in_progress
gh run list --status queued
gh run list --status failure
gh run list --status success
```

**By branch:**
```bash
gh run list --branch main
gh run list --branch develop
```

**By user:**
```bash
gh run list --user username
gh run list --user @me
```

**By event:**
```bash
gh run list --event push
gh run list --event pull_request
gh run list --event schedule
gh run list --event workflow_dispatch
```

### Listing with JSON

```bash
# Get structured data
gh run list \
  --json databaseId,status,conclusion,workflowName,createdAt,event,headBranch \
  --limit 100

# Get only failed runs
gh run list --json databaseId,status,conclusion,workflowName \
  --jq '.[] | select(.conclusion == "failure")'

# Count runs by status
gh run list --json status \
  --jq 'group_by(.status) | map({status: .[0].status, count: length})'
```

## Viewing Run Details

### Basic View

```bash
gh run view 123456789         # View in terminal
gh run view 123456789 --web   # Open in browser
```

### Detailed Information

```bash
# View with logs
gh run view 123456789 --log

# View failed logs only
gh run view 123456789 --log-failed

# View specific job
gh run view 123456789 --job 987654321

# View with JSON output
gh run view 123456789 --json status,conclusion,workflowName,jobs
```

### Get Run URL

```bash
gh run view 123456789 --json url --jq '.url'
```

## Watching Runs in Real-Time

### Live Status Updates

```bash
gh run watch 123456789           # Watch until completion
gh run watch 123456789 --exit-status  # Exit with run's exit code
gh run watch --interval 5        # Custom polling interval (seconds)
```

**Use case:** Monitor CI/CD while making changes, exit when run completes.

## Downloading Run Logs and Artifacts

### Download Logs

```bash
# Download all logs for a run
gh run view 123456789 --log > run-logs.txt

# Download logs for specific job
gh run view 123456789 --job 987654321 --log > job-logs.txt

# Download only failed job logs
gh run view 123456789 --log-failed > failed-logs.txt
```

### Download Artifacts

```bash
# Download all artifacts from run
gh run download 123456789

# Download to specific directory
gh run download 123456789 --dir ./artifacts

# Download specific artifact
gh run download 123456789 --name coverage-report

# List available artifacts
gh run view 123456789 --json artifacts --jq '.artifacts[].name'
```

## Rerunning Workflows

### Rerun Entire Workflow

```bash
gh run rerun 123456789
```

### Rerun Failed Jobs Only

```bash
gh run rerun 123456789 --failed
```

### Rerun with Debug Logging

```bash
gh run rerun 123456789 --debug
```

## Canceling Workflows

### Cancel Single Run

```bash
gh run cancel 123456789
```

### Cancel All In-Progress Runs

```bash
gh run list --status in_progress --json databaseId \
  | jq -r '.[].databaseId' \
  | while read run; do
    gh run cancel "$run"
  done
```

### Cancel Runs for Specific Branch

```bash
gh run list --branch feature-x --status in_progress --json databaseId \
  | jq -r '.[].databaseId' \
  | while read run; do
    gh run cancel "$run"
  done
```

## Deleting Runs

**Use with caution - this removes run history:**

```bash
gh run delete 123456789
gh run delete 123456789 --yes  # Skip confirmation
```

### Delete Old Runs

```bash
# Delete runs older than 90 days
gh run list --json databaseId,createdAt \
  --jq '.[] | select(.createdAt < (now - 7776000 | todate)) | .databaseId' \
  | while read run; do
    gh run delete "$run" --yes
  done
```

## Managing Workflows

### List Workflows

```bash
gh workflow list              # All workflows in repo
gh workflow list --all        # Include disabled workflows
```

### View Workflow Details

```bash
gh workflow view ci.yml       # By filename
gh workflow view 123456       # By workflow ID
gh workflow view ci.yml --web # Open in browser

# Get workflow YAML content
gh workflow view ci.yml --yaml

# Get workflow metadata as JSON
gh workflow view ci.yml --json name,path,state
```

### Enable/Disable Workflows

```bash
gh workflow enable ci.yml
gh workflow disable ci.yml
```

### Manually Trigger Workflow

**Trigger with default inputs:**
```bash
gh workflow run deploy.yml
gh workflow run deploy.yml --ref main  # Specific branch/ref
```

**Trigger with inputs:**
```bash
gh workflow run deploy.yml \
  --ref main \
  --field environment=production \
  --field version=2.0.0
```

**Trigger with JSON inputs:**
```bash
gh workflow run deploy.yml \
  --ref main \
  --raw-field config='{"replicas":3,"timeout":30}'
```

## Fixing Failing CI/CD Workflows

### Complete Diagnostic Workflow

```bash
# 1. Identify failing runs
gh run list --status failure --limit 10

# 2. Get details about most recent failure
LATEST_FAILURE=$(gh run list --status failure --limit 1 --json databaseId --jq '.[0].databaseId')

# 3. View run summary
gh run view "$LATEST_FAILURE"

# 4. Download failed job logs
gh run view "$LATEST_FAILURE" --log-failed > failed-logs.txt

# 5. Analyze logs (view in editor or search for errors)
grep -i "error\|fail\|exception" failed-logs.txt

# 6. Identify root cause from logs

# 7. Make fixes to code

# 8. Commit and push (triggers new run)
git add .
git commit -m "fix: Resolve CI failure in test suite"
git push

# 9. Watch new run
NEW_RUN=$(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$NEW_RUN"

# 10. If new run fails, repeat; otherwise done
```

### Targeted Log Analysis

**Extract specific job logs:**
```bash
# Get job IDs
gh run view 123456789 --json jobs --jq '.jobs[] | {id: .databaseId, name: .name, conclusion: .conclusion}'

# Download specific job log
JOB_ID=987654321
gh run view 123456789 --job "$JOB_ID" --log > specific-job.txt
```

**Search logs for patterns:**
```bash
# Download and search in one command
gh run view 123456789 --log | grep -A 5 -B 5 "Error:"

# Find all test failures
gh run view 123456789 --log | grep "FAILED\|AssertionError"

# Extract stack traces
gh run view 123456789 --log | sed -n '/Traceback/,/Error:/p'
```

### Rerun After Fix

**Determine if rerun is needed:**

Based on workflow trigger:
- **Push event**: New commit triggers automatically, don't rerun
- **Pull request**: New commit triggers automatically, don't rerun
- **Schedule/workflow_dispatch**: Rerun manually if needed

```bash
# Check run trigger
EVENT=$(gh run view 123456789 --json event --jq '.event')

if [ "$EVENT" = "push" ] || [ "$EVENT" = "pull_request" ]; then
  echo "New run will trigger automatically on push"
else
  echo "Consider manual rerun with: gh run rerun 123456789"
fi
```

## Common CI/CD Patterns

### Monitor PR Checks

**Check all PRs with failing checks:**
```bash
# Get PRs with failing checks
gh pr list --json number,title \
  --jq '.[] | {number: .number, title: .title}' \
  | while read -r pr; do
    PR_NUM=$(echo "$pr" | jq -r '.number')
    gh pr checks "$PR_NUM" --json name,status,conclusion \
      --jq '.[] | select(.conclusion == "failure")'
  done
```

**Watch PR checks in real-time:**
```bash
gh pr checks 123 --watch
```

### Retry Flaky Tests

**Identify flaky test patterns:**
```bash
# Get last 20 runs for test workflow
gh run list --workflow tests.yml --limit 20 --json databaseId,conclusion

# Count failures
gh run list --workflow tests.yml --limit 50 --json conclusion \
  | jq '[.[].conclusion] | group_by(.) | map({conclusion: .[0], count: length})'
```

**Auto-rerun failed tests:**
```bash
# Get most recent failed test run
FAILED_RUN=$(gh run list --workflow tests.yml --status failure --limit 1 --json databaseId --jq '.[0].databaseId')

# Rerun failed jobs only
gh run rerun "$FAILED_RUN" --failed
```

### Deployment Workflows

**Check deployment status:**
```bash
gh run list --workflow deploy.yml --limit 5 --json databaseId,status,conclusion,createdAt

# Get most recent deploy
LATEST_DEPLOY=$(gh run list --workflow deploy.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run view "$LATEST_DEPLOY"
```

**Trigger production deployment:**
```bash
# Ensure you're on the right branch
git checkout main
git pull

# Trigger deploy workflow
gh workflow run deploy.yml \
  --ref main \
  --field environment=production \
  --field version=$(git describe --tags)

# Watch deployment
DEPLOY_RUN=$(gh run list --workflow deploy.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$DEPLOY_RUN" --exit-status
```

### Cleanup Old Runs

**Delete successful runs older than 30 days:**
```bash
gh run list --status success --json databaseId,createdAt \
  --jq '.[] | select(.createdAt < (now - 2592000 | todate)) | .databaseId' \
  | while read run; do
    gh run delete "$run" --yes
  done
```

**Keep only last 10 runs per workflow:**
```bash
for workflow in $(gh workflow list --json name --jq '.[].name'); do
  gh run list --workflow "$workflow" --json databaseId \
    | jq -r '.[10:][].databaseId' \
    | while read run; do
      gh run delete "$run" --yes
    done
done
```

## Analyzing Job Performance

### Get Job Timing Data

```bash
# Get job durations for run
gh run view 123456789 --json jobs \
  --jq '.jobs[] | {name: .name, duration: (.completedAt - .startedAt)}'

# Average job duration across runs
gh run list --workflow ci.yml --limit 20 --json jobs \
  | jq '[.[].jobs[].duration] | add / length'
```

### Identify Slow Jobs

```bash
gh run view 123456789 --json jobs \
  --jq '.jobs | sort_by(.completedAt - .startedAt) | reverse | .[] | {name: .name, minutes: ((.completedAt - .startedAt) / 60)}'
```

## Troubleshooting Workflows

### Common Failure Patterns

**Syntax errors in workflow YAML:**
```
! workflow file syntax error
```
**Solution:** View workflow YAML and validate syntax
```bash
gh workflow view ci.yml --yaml | yamllint -
```

**Missing secrets/variables:**
```
Error: Secret not found: API_KEY
```
**Solution:** Check repository secrets with `gh secret list`

**Permission errors:**
```
Error: Resource not accessible by integration
```
**Solution:** Check workflow permissions in YAML, verify token scopes

**Timeout errors:**
```
Error: The operation was canceled.
```
**Solution:** Increase `timeout-minutes` in workflow YAML

### Debugging Failed Steps

**Find exact failing step:**
```bash
# Get run with jobs and steps
gh run view 123456789 --json jobs \
  --jq '.jobs[] | select(.conclusion == "failure") | .steps[] | select(.conclusion == "failure")'
```

**Extract error messages:**
```bash
gh run view 123456789 --log | \
  grep -B 3 -A 3 "##\[error\]"
```

### Verify Workflow Triggers

**Check which events trigger workflow:**
```bash
gh workflow view ci.yml --yaml | grep -A 10 "^on:"
```

**Verify workflow ran for expected event:**
```bash
gh run view 123456789 --json event,headBranch,headSha
```

## Matrix Build Patterns

### View Matrix Job Results

```bash
# Get all matrix job outcomes
gh run view 123456789 --json jobs \
  --jq '.jobs[] | {name: .name, conclusion: .conclusion}'

# Find which matrix combinations failed
gh run view 123456789 --log | \
  grep "node-version\|python-version" | \
  grep -B 2 "failure\|error"
```

### Rerun Specific Matrix Jobs

Unfortunately, `gh` doesn't support rerunning individual matrix jobs directly. Rerun failed jobs only:

```bash
gh run rerun 123456789 --failed
```

## Workflow Dependencies

### Check Dependent Workflows

When workflows depend on each other (workflow_run event):

```bash
# View workflow triggers
gh workflow view deploy.yml --yaml | grep -A 5 "workflow_run"

# Find triggering run
gh run view 123456789 --json workflowName,event,headBranch
```

## Best Practices

1. **Monitor failures proactively** - Check failing runs regularly
2. **Download logs for analysis** - Don't rely on web UI for complex debugging
3. **Clean up old runs** - Keep run history manageable
4. **Use --watch for long-running workflows** - Get notified on completion
5. **Rerun only failed jobs** - Save compute time with `--failed` flag
6. **Cancel superseded runs** - Cancel old runs when new commits pushed
7. **Analyze trends** - Track failure rates and job durations
8. **Debug with artifacts** - Download artifacts for local inspection
9. **Verify triggers** - Ensure workflows run on expected events
10. **Check workflow permissions** - Verify GITHUB_TOKEN has required scopes

## Advanced: Using gh api for Workflows

### Get Workflow Run Logs via API

```bash
# Get log URL
gh api repos/{owner}/{repo}/actions/runs/123456789/logs --include | grep "location:"

# Download logs
gh api repos/{owner}/{repo}/actions/runs/123456789/logs > logs.zip
```

### List Workflow Run Artifacts

```bash
gh api repos/{owner}/{repo}/actions/runs/123456789/artifacts \
  | jq '.artifacts[] | {name: .name, size: .size_in_bytes}'
```

### Get Billing Information

```bash
# Get Actions usage
gh api repos/{owner}/{repo}/actions/runs \
  --jq '[.workflow_runs[] | {name: .name, created_at: .created_at, run_duration_ms: .run_duration_ms}]'
```

See `api-usage.md` for more advanced API operations.

## Related Commands

- `gh pr checks` - View PR check status
- `gh workflow` - Manage workflow definitions
- `gh secret` - Manage repository secrets
- `gh api` - Custom Actions API operations

For complete API reference, see https://docs.github.com/en/rest/actions
