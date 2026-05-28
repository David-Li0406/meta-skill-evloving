---
name: datadog-cli
description: Use this skill when you need to debug and triage using Datadog logs and metrics, including searching logs, querying metrics, tracing requests, and managing dashboards.
---

# Datadog CLI

A CLI tool for AI agents to debug and triage using Datadog logs and metrics.

## Required Reading

**You MUST read the relevant reference docs before using any command:**
- [Log Commands](references/logs-commands.md)
- [Metrics](references/metrics.md)
- [Query Syntax](references/query-syntax.md)
- [Workflows](references/workflows.md)
- [Dashboards](references/dashboards.md)

## Setup

### Environment Variables (Required)

```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-app-key"
```

Get keys from: https://app.datadoghq.com/organization-settings/api-keys

### Running the CLI

```bash
npx @leoflores/datadog-cli <command>
```

For non-US Datadog sites, use `--site` flag:
```bash
npx @leoflores/datadog-cli logs search --query "*" --site datadoghq.eu
```

## Commands Overview

| Command | Description |
|---------|-------------|
| `logs search` | Search logs with filters |
| `logs tail` | Stream logs in real-time |
| `logs trace` | Find logs for a distributed trace |
| `logs context` | Get logs before/after a timestamp |
| `logs patterns` | Group similar log messages |
| `logs compare` | Compare log counts between periods |
| `logs multi` | Run multiple queries in parallel |
| `logs agg` | Aggregate logs by facet |
| `metrics query` | Query timeseries metrics |
| `errors` | Quick error summary by service/type |
| `services` | List services with log activity |
| `dashboards` | Manage dashboards (CRUD) |
| `dashboard-lists` | Manage dashboard lists |

## Quick Examples

### Search Errors
```bash
npx @leoflores/datadog-cli logs search --query "status:error" --from 1h --pretty
```

### Tail Logs (Real-time)
```bash
npx @leoflores/datadog-cli logs tail --query "service:api status:error" --pretty
```

### Error Summary
```bash
npx @leoflores/datadog-cli errors --from 1h --pretty
```

### Trace Correlation
```bash
npx @leoflores/datadog-cli logs trace --id "abc123def456" --pretty
```

### Query Metrics
```bash
npx @leoflores/datadog-cli metrics query --query "avg:system.cpu.user{*}" --from 1h --pretty
```

### Compare Periods
```bash
npx @leoflores/datadog-cli logs compare --query "status:error" --period 1h --pretty
```

## Global Flags

| Flag | Description |
|------|-------------|
| `--pretty` | Human-readable output with colors |
| `--output <file>` | Export results to JSON file |
| `--site <site>` | Datadog site (e.g., `datadoghq.eu`) |

## Time Formats

- **Relative**: `30m`, `1h`, `6h`, `24h`, `7d`
- **ISO 8601**: `2024-01-15T10:30:00Z`

## Common Workflows

### Incident Triage

```bash
# 1. Quick error overview
npx @leoflores/datadog-cli errors --from 1h --pretty

# 2. Is this new? Compare to previous period
npx @leoflores/datadog-cli logs compare --query "status:error" --period 1h --pretty

# 3. Find error patterns
npx @leoflores/datadog-cli logs patterns --query "status:error" --from 1h --pretty

# 4. Narrow down by service
npx @leoflores/datadog-cli logs search --query "status:error service:api" --from 1h --pretty

# 5. Get context around a timestamp
npx @leoflores/datadog-cli logs context --timestamp "2024-01-15T10:30:00Z" --service api --pretty

# 6. Follow the distributed trace
npx @leoflores/datadog-cli logs trace --id "TRACE_ID" --pretty
```

### Real-time Debugging

```bash
# Stream errors as they happen
npx @leoflores/datadog-cli logs tail --query "status:error"

# Watch specific service
npx @leoflores/datadog-cli logs tail --query "service:api status:error"
```

### Service Health Check

```bash
# List services
npx @leoflores/datadog-cli services --from 24h

# Check error distribution
npx @leoflores/datadog-cli logs agg --query "service:api" --facet status --from 1h

# Check CPU/memory
npx @leoflores/datadog-cli metrics query --query "avg:system.cpu.user{service:api}" --from 1h
```

### Export for Sharing

```bash
# Save search results
npx @leoflores/datadog-cli logs search --query "status:error" --from 1h --output errors.json

# Save error summary
npx @leoflores/datadog-cli errors --from 24h --output error-report.json
```

## Datadog Query Syntax

| Operator  | Example                       | Description        |
| --------- | ----------------------------- | ------------------ |
| `AND`     | `service:api status:error`    | Both conditions    |
| `OR`      | `status:error OR status:warn` | Either condition   |
| `-`       | `-status:info`                | Exclude            |
| `*`       | `service:api-*`               | Wildcard           |
| `>=` `<=` | `@http.status_code:>=400`     | Numeric comparison |
| `[TO]`    | `@duration:[1000 TO 5000]`    | Range              |

### Common Attributes

- `service` - Service name
- `status` - Log level (error, warn, info, debug)
- `host` - Hostname
- `@http.status_code` - HTTP status code
- `@error.kind` - Error type
- `@trace_id` / `@dd.trace_id` - Trace ID