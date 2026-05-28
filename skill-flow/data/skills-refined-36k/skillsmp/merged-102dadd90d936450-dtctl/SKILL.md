---
name: dtctl
description: Use the dtctl CLI tool for querying observability data in Dynatrace via DQL and managing platform resources like workflows, dashboards, notebooks, SLOs, settings, buckets, and lookup tables.
---

# dtctl Command Reference

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
dtctl config set-context <context-name> --environment "<environment-url>" --token-ref <token-ref> --safety-level <safety-level>
dtctl config set-credentials <token-ref> --token "<your-token>"
dtctl config use-context <context-name>

# Safety levels: readonly | readwrite-mine | readwrite-all | dangerously-unrestricted
```

## Common Commands

### Workflows
```bash
dtctl get workflows --mine
dtctl edit workflow <id>
dtctl apply -f workflow.yaml --set env=<environment>
dtctl exec workflow <id> --wait --timeout <timeout>
dtctl logs wfe <execution-id> --follow
dtctl history workflow <id>
```

### Dashboards/Notebooks
```bash
dtctl get dashboards --mine
dtctl edit dashboard <id>
dtctl share dashboard <id> --user <user-email> --access <access-level>
dtctl history dashboard <id>
dtctl restore dashboard <id> <revision>
```

### DQL Queries
```bash
dtctl query 'fetch logs | filter status="ERROR" | limit 100'
dtctl query -f query.dql --set host=<host-id> --set timerange=<time-range>
dtctl query 'timeseries avg(dt.host.cpu.usage)' -o chart
dtctl wait query 'fetch spans | filter test_id == "<test-id>"' --for=count=1 --timeout <timeout>
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
dtctl create lookup -f <data-file> --path <lookup-path> --lookup-field <field>
dtctl get lookups
dtctl get lookup <lookup-path> -o csv > backup.csv

# Use in DQL
dtctl query "fetch logs | lookup [load '<lookup-path>'], lookupField:<lookup-field>"
```

### Settings API
```bash
dtctl get settings-schemas | grep <schema-name>
dtctl get settings --schema <schema>
dtctl edit setting <object-id>
dtctl apply -f config.yaml --set env=<environment>
```

### SLOs
```bash
dtctl get slos
dtctl describe slo <id>
dtctl exec slo <id> -o json
dtctl apply -f slo.yaml
```

### Davis AI
```bash
dtctl get analyzers
dtctl exec analyzer <analyzer-name> --query "timeseries avg(dt.host.cpu.usage)" -o chart
dtctl exec copilot "<question>"
dtctl exec copilot nl2dql "<natural-language-query>"
```

## Template Variables
```bash
# In YAML files: {{.variable}} or {{.variable | default "value"}}
dtctl apply -f workflow.yaml --set environment=<environment> --set owner=<owner>
```

## Troubleshooting
```bash
dtctl auth whoami                          # Check auth
dtctl auth can-i create workflows          # Check permissions
dtctl config set-credentials <context> --token "<new-token>"
dtctl --help                               # Command help
```

**Name resolution:** Use IDs instead of names if ambiguous (`dtctl get dashboards` to find ID)  
**Safety blocks:** Adjust context safety level or switch context  
**Permissions:** Check token scopes at https://github.com/dynatrace-oss/dtctl/blob/main/docs/TOKEN_SCOPES.md