---
name: dtctl
description: Use this skill when you need to query observability data in Dynatrace via DQL and manage various Dynatrace platform resources using the dtctl CLI tool.
---

# Skill body

## Syntax
```bash
dtctl <verb> <resource> [name/id] [flags]
```

**Verbs:** get, describe, create, edit, apply, delete, exec, query, logs, wait, history, restore, share/unshare

**Key Resources:** workflow (wf), dashboard (dash), notebook (nb), slo, bucket (bkt), lookup (lkup), settings, analyzer (az), copilot (cp)

**Global Flags:**
- `--context` - Switch environment
- `-o, --output` - json|yaml|table|wide|csv|chart|sparkline|barchart
- `--dry-run` - Preview without executing
- `--plain` - Machine-readable output

## Setup
```bash
# Configure context
dtctl config set-context prod --environment "https://abc.apps.dynatrace.com" --token-ref prod-token --safety-level readonly
dtctl config set-credentials prod-token --token "dt0s16.YOUR_TOKEN"
dtctl config use-context prod

# Safety levels: readonly | readwrite-mine | readwrite-all | dangerously-unrestricted
```

## Common Commands

### Workflows
```bash
dtctl get workflows --mine
dtctl edit workflow <id>
dtctl apply -f workflow.yaml --set env=prod
dtctl exec workflow <id> --wait --timeout 10m
dtctl logs wfe <execution-id> --follow
dtctl history workflow <id>
```

### Dashboards/Notebooks
```bash
dtctl get dashboards --mine
dtctl edit dashboard <id>
dtctl share dashboard <id> --user user@example.com --access read-write
dtctl history dashboard <id>
dtctl restore dashboard <id> 3
```

### DQL Queries
```bash
dtctl query 'fetch logs | filter status="ERROR" | limit 100'
dtctl query -f query.dql --set host=h-123 --set timerange=2h
dtctl query 'timeseries avg(dt.host.cpu.usage)' -o chart
dtctl wait query 'fetch spans | filter test_id == "test-123"' --for=count=1 --timeout 5m
```

**Wait conditions:** count=N, count-gte=N, count-gt=N, count-lte=N, count-lt=N, any, none

**Template syntax in .dql files:**
```dql
fetch logs
| filter host.name = "{{.host}}"
| filter timestamp > now() - {{.timerange | default "1h"}}
```

### Lookup Tables
```bash
dtctl create lookup -f data.csv --path /lookups/grail/pm/errors --lookup-field code
dtctl get lookups
dtctl get lookup /lookups/grail/pm/errors -o csv > backup.csv

# Use in DQL
dtctl query "fetch logs | lookup [load '/lookups/grail/pm/errors'], lookupField:status_code"
```