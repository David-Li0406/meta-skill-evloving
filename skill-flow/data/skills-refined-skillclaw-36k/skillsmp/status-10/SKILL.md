---
name: status
description: Show comprehensive status of project health including services, database, and infrastructure
allowed-tools: Bash, Read
disable-model-invocation: true
argument-hint: [--json|--watch]
---

# Comprehensive Project Status

Show a unified view of project health: services, database, infrastructure, and configuration.

## Usage

- `/devflow-status` - Full status report
- `/devflow-status --json` - Machine-readable output
- `/devflow-status --watch` - Continuous monitoring (refresh every 5s)

## Status Check Steps

### Step 1: Configuration Status

```bash
devflow config validate
```

Report:
- Config file location
- Validation status
- Current environment

### Step 2: Infrastructure Status

```bash
devflow infra status --json
```

Report:
- Network: devflow-proxy exists?
- Traefik: running? dashboard URL?
- Certificates: valid? expiry?
- Registered projects

### Step 3: Database Status

```bash
devflow db status --env local --json
```

Report:
- Connection: successful?
- Executor type
- Migrations: applied/pending/total
- List pending migrations if any

### Step 4: Service Status

```bash
docker compose ps --format json
```

For each service, report:
- Name
- Status (running/stopped/restarting)
- Health (if health check defined)
- Ports exposed
- Uptime

### Step 5: Resource Usage

```bash
docker stats --no-stream --format json
```

For running services, show:
- CPU usage
- Memory usage
- Network I/O

### Step 6: Recent Logs Check

For each service, check for errors in recent logs:

```bash
docker compose logs --tail 20 <service> 2>&1 | grep -i "error\|exception\|fatal"
```

Flag services with recent errors.

## Output Format

```
DEVFLOW STATUS
==============

Project: aocodex
Environment: local
Config: devflow.yml [VALID]

INFRASTRUCTURE
--------------
Network:      devflow-proxy [OK]
Traefik:      running (dashboard: http://localhost:8088)
Certificates: valid (expires: 2026-03-15)
Projects:     2 registered

DATABASE
--------
Connection:   postgresql://localhost:5432/aocodex [OK]
Migrations:   15 applied, 2 pending
  - 20250120_add_user_preferences.sql
  - 20250121_add_audit_log.sql

SERVICES
--------
┌─────────────┬──────────┬────────┬───────────────┬────────┐
│ Service     │ Status   │ Health │ Ports         │ Uptime │
├─────────────┼──────────┼────────┼───────────────┼────────┤
│ api         │ running  │ OK     │ 3000→3000     │ 2h 15m │
│ web         │ running  │ OK     │ 3001→3001     │ 2h 15m │
│ postgres    │ running  │ OK     │ 5432→5432     │ 2h 15m │
│ redis       │ running  │ OK     │ 6379→6379     │ 2h 15m │
│ worker      │ running  │ -      │ -             │ 2h 15m │
└─────────────┴──────────┴────────┴───────────────┴────────┘

RESOURCES
---------
┌─────────────┬───────┬────────────┐
│ Service     │ CPU   │ Memory     │
├─────────────┼───────┼────────────┤
│ api         │ 2.3%  │ 256MB/512MB│
│ postgres    │ 0.5%  │ 128MB/256MB│
└─────────────┴───────┴────────────┘

ISSUES
------
[WARN] 2 pending migrations - run: devflow db migrate --env local
[WARN] worker: 3 errors in last 20 log lines

QUICK ACTIONS
-------------
• Apply migrations:  devflow db migrate --env local
• View worker logs:  devflow dev logs worker
• Open dashboard:    open http://localhost:8088
```

## Watch Mode

When `--watch` is specified:

1. Clear screen and redraw status every 5 seconds
2. Highlight changes since last refresh
3. Show timestamp of last update
4. Exit with Ctrl+C

## Error States to Detect

| Condition | Severity | Message |
|-----------|----------|---------|
| Config invalid | ERROR | "devflow.yml has validation errors" |
| Docker not running | ERROR | "Docker daemon not accessible" |
| Network missing | WARN | "devflow-proxy network not found" |
| Traefik down | WARN | "Traefik not running" |
| DB unreachable | ERROR | "Cannot connect to database" |
| Pending migrations | WARN | "N pending migrations" |
| Service down | ERROR | "Service X is not running" |
| Service restarting | WARN | "Service X is restart-looping" |
| Recent errors | WARN | "Service X has errors in logs" |
| High resource usage | WARN | "Service X using >80% memory" |
