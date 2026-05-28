---
name: buildkite-cli
description: CLI scripts for common Buildkite operations. Rebuild failed builds, retry jobs, get logs, trigger builds - all by passing URLs directly. Supports both Buildkite build URLs and GitHub PR URLs.
---

# Buildkite CLI

Simple `pnpm tsx` scripts for common Buildkite operations. Pass URLs directly - supports both Buildkite build URLs and GitHub PR URLs.

## Setup

```bash
# Install deps
pnpm install

# Required env vars
export BUILDKITE_TOKEN="bkua_xxx"  # API token with read/write builds

# Optional - for default org/pipeline
export BUILDKITE_ORG="my-org"
export BUILDKITE_PIPELINE="my-pipeline"

# Optional - for GitHub PR URL support
export GITHUB_TOKEN="ghp_xxx"
```

## Commands

### Rebuild a Failed Build

```bash
# From Buildkite URL
pnpm rebuild https://buildkite.com/org/pipeline/builds/123

# From GitHub PR URL (requires --pipeline or BUILDKITE_PIPELINE)
pnpm rebuild https://github.com/org/repo/pull/456 --pipeline my-pipeline
```

### Retry Failed Jobs Only

```bash
pnpm retry-failed https://buildkite.com/org/pipeline/builds/123
```

### Get Build Status

```bash
pnpm status https://buildkite.com/org/pipeline/builds/123
```

### Get Job Logs

```bash
# First failed job (default)
pnpm logs https://buildkite.com/org/pipeline/builds/123

# Specific job by index
pnpm logs <url> --job 2

# Specific job by name match
pnpm logs <url> --job "playwright"

# Last N lines
pnpm logs <url> --tail 50
```

### Cancel Build

```bash
pnpm cancel https://buildkite.com/org/pipeline/builds/123
```

### Unblock Blocked Step

```bash
pnpm unblock https://buildkite.com/org/pipeline/builds/123

# With field values for block step
pnpm unblock <url> --fields env=production,confirm=yes
```

### Trigger New Build

```bash
pnpm trigger --pipeline my-pipeline
pnpm trigger --pipeline my-pipeline --branch feature/x --message "Deploy fix"
```

### List Recent Failed Builds

```bash
pnpm list-failed --pipeline my-pipeline
pnpm list-failed --pipeline my-pipeline --limit 20
```

## URL Formats Supported

**Buildkite URLs:**
- `https://buildkite.com/org/pipeline/builds/123`
- `https://buildkite.com/org/pipeline/builds/123#job-uuid`

**GitHub PR URLs:**
- `https://github.com/owner/repo/pull/123`
- Requires `--pipeline` flag or `BUILDKITE_PIPELINE` env var
- Looks up PR head commit and finds corresponding Buildkite build

## File Structure

```
buildkite-cli/
├── package.json
├── src/
│   ├── api.ts         # Core API helpers, URL parsing
│   ├── rebuild.ts     # Rebuild entire build
│   ├── retry-failed.ts # Retry only failed jobs
│   ├── cancel.ts      # Cancel running build
│   ├── status.ts      # Get build status
│   ├── logs.ts        # Get job logs
│   ├── list-failed.ts # List recent failures
│   ├── trigger.ts     # Trigger new build
│   └── unblock.ts     # Unblock blocked steps
└── SKILL.md
```
