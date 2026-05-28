# GitHub CLI Complete Reference for CI/CD

<workflow_runs>

## List Workflow Runs

```bash
gh run list                                    # All recent runs
gh run list --limit 20                        # Limit results
gh run list --workflow ci.yml                 # Specific workflow
gh run list --branch main                     # Specific branch
gh run list --user username                   # By user
gh run list --status failure                  # Failed only
gh run list --status success                  # Successful only
gh run list --status in_progress             # Currently running
gh run list --event push                      # By trigger event
gh run list --event pull_request             # PR triggered

# JSON output with specific fields
gh run list --json databaseId,status,conclusion,name,headBranch,createdAt
gh run list --json databaseId,conclusion -q '.[] | select(.conclusion=="failure")'
```

## View Run Details

```bash
gh run view <run-id>                          # Summary view
gh run view <run-id> --log                   # Full logs
gh run view <run-id> --log-failed            # Only failed job logs
gh run view <run-id> --exit-status           # Exit with run's status
gh run view <run-id> --web                   # Open in browser

# JSON output
gh run view <run-id> --json jobs
gh run view <run-id> --json jobs,status,conclusion
gh run view <run-id> --json jobs -q '.jobs[] | {name, conclusion, steps}'
```

## Watch Running Workflow

```bash
gh run watch                                  # Interactive selection
gh run watch <run-id>                        # Watch specific run
gh run watch <run-id> --exit-status          # Exit with final status
gh run watch <run-id> --interval 5           # Custom refresh interval
```

</workflow_runs>

<rerun_workflows>

## Re-run Workflows

```bash
gh run rerun <run-id>                         # Re-run all jobs
gh run rerun <run-id> --failed               # Re-run only failed jobs
gh run rerun <run-id> --debug                # Re-run with debug logging
gh run rerun <run-id> --job <job-id>         # Re-run specific job

# Get job IDs first
gh run view <run-id> --json jobs -q '.jobs[].databaseId'
```

## Cancel Running Workflow

```bash
gh run cancel <run-id>
```

</rerun_workflows>

<artifacts>
## Download Artifacts
```bash
gh run download <run-id>                      # All artifacts to current dir
gh run download <run-id> --dir ./artifacts   # Specific directory
gh run download <run-id> -n artifact-name    # Specific artifact
gh run download <run-id> -n "name-*"         # Pattern matching
gh run download <run-id> -p "*.zip"          # Glob pattern

# Download from multiple runs

gh run download -n test-results # Latest artifact with name

# Download interactively

gh run download

````

## List Artifacts via API
```bash
gh api repos/{owner}/{repo}/actions/artifacts
gh api repos/{owner}/{repo}/actions/runs/{run_id}/artifacts
gh api repos/{owner}/{repo}/actions/artifacts/{artifact_id}/zip > artifact.zip
````

</artifacts>

<workflow_management>

## List Workflows

```bash
gh workflow list                              # All workflows
gh workflow list --all                       # Include disabled
gh workflow list --json id,name,state
```

## View Workflow

```bash
gh workflow view <workflow>                   # Summary
gh workflow view <workflow> --yaml           # Show YAML content
gh workflow view <workflow> --web            # Open in browser
```

## Run Workflow Manually

```bash
gh workflow run <workflow>                    # Trigger on default branch
gh workflow run <workflow> --ref feature     # Specific branch
gh workflow run ci.yml -f input1=value       # With inputs
gh workflow run ci.yml --json                # Read inputs from stdin

# Example with JSON input
echo '{"environment": "staging"}' | gh workflow run deploy.yml --json
```

## Enable/Disable Workflow

```bash
gh workflow enable <workflow>
gh workflow disable <workflow>
```

</workflow_management>

<cache_management>

## Cache Commands

```bash
gh cache list                                 # List caches
gh cache list --limit 50
gh cache list --json id,key,sizeInBytes
gh cache list --key "npm-"                   # Filter by key prefix

gh cache delete <cache-id>                   # Delete specific cache
gh cache delete --all                        # Delete all caches
```

</cache_management>

<api_access>

## Direct API Access

```bash
# Get workflow runs
gh api repos/{owner}/{repo}/actions/runs
gh api repos/{owner}/{repo}/actions/runs?status=failure

# Get specific run
gh api repos/{owner}/{repo}/actions/runs/{run_id}

# Get jobs for a run
gh api repos/{owner}/{repo}/actions/runs/{run_id}/jobs

# Download logs (returns redirect URL)
gh api repos/{owner}/{repo}/actions/runs/{run_id}/logs

# Get artifacts
gh api repos/{owner}/{repo}/actions/artifacts
gh api repos/{owner}/{repo}/actions/runs/{run_id}/artifacts

# Re-run workflow
gh api -X POST repos/{owner}/{repo}/actions/runs/{run_id}/rerun

# Re-run failed jobs
gh api -X POST repos/{owner}/{repo}/actions/runs/{run_id}/rerun-failed-jobs

# Cancel run
gh api -X POST repos/{owner}/{repo}/actions/runs/{run_id}/cancel

# Delete run
gh api -X DELETE repos/{owner}/{repo}/actions/runs/{run_id}
```

## Using jq for Filtering

```bash
# Get failed runs
gh api repos/{owner}/{repo}/actions/runs \
  --jq '.workflow_runs[] | select(.conclusion=="failure") | {id, name, created_at}'

# Get latest successful run ID
gh api repos/{owner}/{repo}/actions/runs?status=success \
  --jq '.workflow_runs[0].id'

# Get failed job names
gh api repos/{owner}/{repo}/actions/runs/{run_id}/jobs \
  --jq '.jobs[] | select(.conclusion=="failure") | .name'
```

</api_access>

<pr_checks>

## Check PR Status

```bash
gh pr checks                                  # Current branch PR checks
gh pr checks <pr-number>                     # Specific PR
gh pr checks --required                      # Required checks only
gh pr checks --watch                         # Watch until complete
gh pr checks --fail-fast                     # Exit on first failure
gh pr checks --json name,state,conclusion
gh pr checks --web                           # Open in browser
```

</pr_checks>

<useful_scripts>

## Useful One-liners

```bash
# Get latest failed run ID
gh run list --status failure --limit 1 --json databaseId -q '.[0].databaseId'

# Re-run latest failed
gh run rerun $(gh run list --status failure -L1 --json databaseId -q '.[0].databaseId') --failed

# Watch latest run
gh run watch $(gh run list -L1 --json databaseId -q '.[0].databaseId')

# Download all failed run artifacts
for id in $(gh run list --status failure --json databaseId -q '.[].databaseId'); do
  gh run download $id --dir /tmp/artifacts/$id 2>/dev/null
done

# List all workflow files
ls .github/workflows/*.yml

# Get run URL
gh run view <run-id> --json url -q '.url'

# Check if workflow exists
gh workflow view ci.yml >/dev/null 2>&1 && echo "exists" || echo "not found"
```

</useful_scripts>

<environment_secrets>

## Secrets and Variables (for reference)

```bash
# List secrets (names only, not values)
gh secret list
gh secret list --env production

# Set secret
gh secret set SECRET_NAME
gh secret set SECRET_NAME --body "value"
gh secret set SECRET_NAME < secret.txt

# Delete secret
gh secret delete SECRET_NAME

# Variables
gh variable list
gh variable set VAR_NAME --body "value"
gh variable delete VAR_NAME
```

</environment_secrets>
