---
name: gitlab-ci-pipeline-debugging
description: Use this skill to check GitLab CI pipeline status, investigate failures, and debug jobs when issues arise in CI/CD processes.
---

# GitLab CI Pipeline Debugging

This skill enables the investigation of GitLab CI pipeline failures by checking pipeline statuses, identifying failed jobs, retrieving job logs, and analyzing error messages to suggest fixes.

## Prerequisites

- Git repository with GitLab remote configured
- GitLab authentication via `GITLAB_TOKEN` environment variable or `.netrc` file

The script will fail if it detects any missing configuration. Interpret the error message and provide instructions for setting up the required configuration.

## Instructions

**IMPORTANT**: Always run the script from the user's current working directory (where the agent was launched), NOT from the skill directory. The script needs access to the git repository context. Use the base directory (`<base_path>`) for this skill to execute the script with an absolute path.

### Checking Pipeline Status

1. **Check Current Pipeline Status**
    - Run `<base_path>/scripts/check_pipeline.py` without arguments to check the current branch's pipeline status.
    - The script will display all jobs grouped by stage with status indicators.

2. **Check Specific Branch**
    - Use the `-b` or `--branch` option to specify a different branch.
        - Example: `<base_path>/scripts/check_pipeline.py -b feature-branch`

3. **Check Specific Pipeline by ID**
    - Use the `-p` or `--pipeline-id` option to inspect a specific pipeline.
        - Example: `<base_path>/scripts/check_pipeline.py -p <pipeline-id>`
    - Note: `--pipeline-id` and `--branch` are mutually exclusive.

### Investigating Failed Jobs

1. **Find the Merge Request (MR)**
    - Get the current branch: `git rev-parse --abbrev-ref HEAD`
    - Find MR for this branch: `glab mr list --source-branch $(git rev-parse --abbrev-ref HEAD)`

2. **Get MR Pipelines**
    - List pipelines for the MR: `<base_path>/scripts/glab-pipeline.sh mr-pipelines <mr-number>`
    - Look for pipelines where `ref` starts with `refs/merge-requests/`.

3. **Find Failed Jobs**
    - List only failed jobs: `<base_path>/scripts/glab-pipeline.sh failed-jobs <pipeline-id>`

4. **Get Job Logs**
    - Retrieve full job log output: `<base_path>/scripts/glab-pipeline.sh job-trace <job-id>`
    - For the last 200 lines: `<base_path>/scripts/glab-pipeline.sh job-trace <job-id> | tail -200`
    - Search for errors: `<base_path>/scripts/glab-pipeline.sh job-trace <job-id> | grep -E "(FAIL|Error|error:|failed)" | head -30`

5. **Get Job Details**
    - Retrieve job metadata: `<base_path>/scripts/glab-pipeline.sh job-info <job-id>`

### Common Patterns

- **Quick Status Check**: `glab ci status` shows the current branch pipeline status.
- **Check if Branch Pipeline Passed but MR Pipeline Failed**: Compare branch vs MR pipelines using the respective commands.
- **Retry a Pipeline**: If you suspect a flaky failure, push an empty commit to retrigger: 
    ```bash
    git commit --allow-empty -m "Retrigger CI"
    git push
    ```

## Example Session

```
User: "CI failed, can you check what went wrong?"

Claude: Let me check the pipeline status for your branch.

# Find the MR
glab mr list --source-branch $(git rev-parse --abbrev-ref HEAD)
# Output: !4674 modernize-document-context

# Get MR pipelines
<base_path>/scripts/glab-pipeline.sh mr-pipelines 4674
# Output shows pipeline 4467641 failed

# Find failed jobs
<base_path>/scripts/glab-pipeline.sh failed-jobs 4467641
# Output: unit tests: failed - https://...

# Get logs
<base_path>/scripts/glab-pipeline.sh job-trace 62708639 | tail -200
# Analyze the failure...
```