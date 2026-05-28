---
name: check-pipeline
description: Check GitLab CI pipeline status and investigate failures. Use when user asks about CI status, pipeline failures, or wants to debug failed jobs.
allowed-tools:
  - Bash(~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh:*)
  - Bash(glab ci status:*)
  - Bash(glab mr list:*)
  - Bash(glab mr view:*)
  - Bash(git rev-parse:*)
  - Bash(git branch:*)
  - Read
  - Grep
---

# Check GitLab CI Pipeline

Investigate GitLab CI pipeline status and debug failures.

## Key Concept: MR Pipelines vs Branch Pipelines

GitLab often creates **two pipelines** for merge requests:

1. **Branch Pipeline** (`ref: branch-name`)
   - Triggered by pushing to the branch
   - Often runs only security scans or limited tests
   - Status shown: "success" even when MR pipeline fails

2. **MR Pipeline** (`ref: refs/merge-requests/<number>/head`)
   - Triggered by the merge request
   - Runs the full test suite from `.gitlab-ci.yml`
   - **This is the one that matters for merge readiness**

The helper script filters out `source: "external"` pipelines (security scans) automatically.

## Helper Script

Use the allowlisted helper script for all API calls:

```bash
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh <command> [args]
```

Commands:
- `mr-pipelines <mr-number>` - List pipelines for an MR
- `branch-pipelines [branch]` - List pipelines for a branch (defaults to current)
- `pipeline-jobs <pipeline-id>` - List all jobs in a pipeline
- `failed-jobs <pipeline-id>` - List only failed jobs
- `job-trace <job-id>` - Get job log output
- `job-info <job-id>` - Get job metadata
- `pipeline-info <pipeline-id>` - Get pipeline metadata

## Investigation Workflow

### Step 1: Find the MR

```bash
# Get current branch
git rev-parse --abbrev-ref HEAD

# Find MR for this branch
glab mr list --source-branch $(git rev-parse --abbrev-ref HEAD)
```

### Step 2: Get MR Pipelines

```bash
# List pipelines for the MR (MR number from step 1)
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh mr-pipelines <mr-number>
```

Look at the output:
- Find pipelines where `ref` starts with `refs/merge-requests/` - these are MR pipelines
- Check the `status` field: `success`, `failed`, `running`, `pending`
- Note the `id` of the failed pipeline

### Step 3: Find Failed Jobs

```bash
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh failed-jobs <pipeline-id>
```

This shows failed job names and URLs.

### Step 4: Get Job Logs

```bash
# Get full trace (may be large)
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh job-trace <job-id>

# Get last 200 lines
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh job-trace <job-id> | tail -200

# Search for errors
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh job-trace <job-id> | grep -E "(FAIL|Error|error:|failed)" | head -30
```

### Step 5: Get Job Details

```bash
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh job-info <job-id>
```

Returns: `id`, `name`, `status`, `failure_reason`, `started_at`, `finished_at`, `duration`, `web_url`

## Common Patterns

### Quick Status Check

```bash
glab ci status
```

Shows current branch pipeline status (but remember: this may show branch pipeline, not MR pipeline).

### Check if Branch Pipeline Passed but MR Pipeline Failed

This is common! The branch pipeline may run only security scans while the MR pipeline runs full tests.

```bash
# Compare branch vs MR pipelines
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh branch-pipelines
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh mr-pipelines <mr-number>
```

### Find Test Failures in Logs

Job logs can be large and truncated. Search strategically:

```bash
# Look for test failures
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh job-trace <job-id> | grep -E "(FAIL|✗|×|Test Files.*failed)" | head -20

# Look for build errors
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh job-trace <job-id> | grep -E "(Error:|error:|ELIFECYCLE|exit code)" | head -20

# Get context around errors
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh job-trace <job-id> | grep -B5 -A10 "FAIL" | head -50
```

### Check Pipeline Source

```bash
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh pipeline-info <pipeline-id> | jq -r '.source'
```

Common sources:
- `push` - triggered by git push
- `merge_request_event` - triggered by MR
- `external` - security scan (Semgrep, etc.) - usually ignore these

## Integration Tests vs Unit Tests

In this monorepo:
- **Unit tests**: Run in CI and should pass
- **Integration tests**: Connect to real services, can be flaky, may be configured to not block

If integration tests fail but unit tests pass, check if integration test failures block the pipeline.

## Retry a Pipeline

If you suspect a flaky failure, push an empty commit to retrigger:

```bash
git commit --allow-empty -m "Retrigger CI"
git push
```

Then watch the new pipeline.

## Example Session

```
User: "CI failed, can you check what went wrong?"

Claude: Let me check the pipeline status for your branch.

# Find the MR
glab mr list --source-branch $(git rev-parse --abbrev-ref HEAD)
# Output: !4674 modernize-document-context

# Get MR pipelines
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh mr-pipelines 4674
# Output shows pipeline 4467641 failed

# Find failed jobs
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh failed-jobs 4467641
# Output: unit tests: failed - https://...

# Get logs
~/.claude/skills/check-pipeline/scripts/glab-pipeline.sh job-trace 62708639 | tail -200
# Analyze the failure...
```
