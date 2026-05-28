---
name: circleci
description: Troubleshoot CircleCI pipelines and jobs using the CircleCI CLI and API, including checking cloud job status, fetching logs/errors, and running jobs locally on macOS Apple Silicon with Docker emulation. Use when requests mention CircleCI CLI, pipeline/workflow/job status, CircleCI API v2, or local execute on ARM/Apple Silicon.
---

# CircleCI

## Overview

Use the CircleCI CLI plus CircleCI API v2 to inspect pipelines/workflows/jobs and to run jobs locally on macOS Apple Silicon.

## Quick start

1. Authenticate the CLI with `circleci setup` or set `CIRCLECI_CLI_TOKEN` (script also reads `~/.circleci/cli.yml`).
2. For cloud job status and logs, follow `references/cloud-status.md`.
3. For local execution on Apple Silicon, follow `references/local-execute-apple-silicon.md`.

## Tasks

### Check cloud job status

- Use `circleci pipeline list <project-id>` to find recent pipeline IDs.
- Use the API to list workflows for a pipeline, then jobs for a workflow (see `references/cloud-status.md`).
- Or run `python3 scripts/cc_status.py pipelines gh/org/repo` for a quick list.

### Pull job error details

- Use the job number from workflow jobs to query job details and step output URLs (see `references/cloud-status.md`).
- Or run `python3 scripts/cc_status.py job gh/org/repo <job-number> --steps`.

### Run job locally on Apple Silicon

- Process config with `circleci config process` and run `circleci local execute` with amd64 emulation (see `references/local-execute-apple-silicon.md`).

## Resources

### scripts/

- `scripts/cc_status.py`: List pipelines, workflows, jobs, and job details without manual curl.

### references/

- `references/cloud-status.md`: CLI + API commands to list pipelines, workflows, jobs, logs, and use `cc_status.py`.
- `references/local-execute-apple-silicon.md`: Apple Silicon local execute workflow, Docker settings, and common fixes.
