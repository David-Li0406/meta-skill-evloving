---
name: infra-operations
description: Infrastructure operations, deployment, debugging, and monitoring. Use when deploying services, managing secrets, checking health, viewing logs, or troubleshooting infrastructure issues. Covers both finance_report app and infra2 platform components.
---

# Infrastructure Operations

> Operations guide for finance_report and infra2 platform.

## Prerequisites

```bash
# Initialize repo/ submodule (infra2)
git submodule update --init --recursive
cd repo && uv run invoke --list
```

---

## Tool Priority

1. **`invoke`** — Primary (type-safe, idempotent)
2. **`scripts/debug.py`** — Unified debugging
3. **`libs` API** — For automation
4. **SSH** — Emergency only (read-only)

---

## Debug Commands

### Logs & Status

```bash
# View logs
python scripts/debug.py logs backend [--env production] [--tail 50] [--follow]

# Check health
python scripts/debug.py status backend --env production

# List containers
python scripts/debug.py containers --env production

# SigNoz (historical)
python scripts/debug.py logs backend --env production --method signoz
```

### Container Naming

⚠️ **Production uses underscore**: `finance_report-*` (not hyphen)

| Environment | Backend | PostgreSQL | Redis |
|-------------|---------|------------|-------|
| **Production** | `finance_report-backend` | `finance_report-postgres` | `finance_report-redis` |
| Staging | `finance-report-backend-staging` | `finance-report-db-staging` | `finance-report-redis-staging` |
| PR | `finance-report-backend-pr-47` | `finance-report-db-pr-47` | `finance-report-redis-pr-47` |

**Critical**: Container name = hostname in Dokploy network.

**Note**: `scripts/debug.py` currently only supports hyphenated patterns (staging/PR).
For production, use direct SSH: `ssh root@$VPS_HOST "docker logs finance_report-backend"`

---

## Invoke Commands

All commands from `repo/tasks.py`:

### Secrets (`env.*`)

```bash
invoke env.get DATABASE_URL                  # Defaults: project=platform, env=production
invoke env.get DATABASE_URL finance_report app production  # Full form: key first
invoke env.set DATABASE_URL "postgresql://..." finance_report app production
invoke env.list-all finance_report app production
```

### Finance Report (`fr-*`)

```bash
invoke fr-app.setup       # Deploy app
invoke fr-app.status      # Check health
invoke fr-postgres.setup  # Deploy PostgreSQL
invoke fr-redis.setup     # Deploy Redis
```

### Platform Services

```bash
invoke postgres.setup              # Shared PostgreSQL
invoke redis.setup                 # Shared Redis
invoke vault.setup                 # Vault cluster
invoke authentik.setup             # Authentik SSO
invoke minio.setup                 # MinIO storage
invoke signoz.setup                # SigNoz observability
```

---

## Python APIs

> **Context**: These APIs are in `repo/` submodule (infra2).
> Run from `repo/` directory: `cd repo && python -c "from libs.env import ..."`

### Secrets (`libs/env.py`)

```python
from libs.env import get_secrets

secrets = get_secrets("finance_report", "app", "production")
print(secrets["DATABASE_URL"])
```

### Dokploy (`libs/dokploy.py`)

```python
from libs.dokploy import get_dokploy

client = get_dokploy()
compose = client.get_compose("A6V-hbJlgHMwgPDoTDnhH")
compose_id = compose["composeId"]  # Extract ID
client.update_compose_env(compose_id, {"DEBUG": "true"})
client.deploy_compose(compose_id)
```

### Deployer (`libs/deployer.py`)

```python
from libs.deployer import Deployer
from libs.config import VPS

deployer = Deployer(vps=VPS.MAIN)
deployer.compose_up("finance_report", "production", "docker-compose.prod.yml")
```

---

## Troubleshooting

### Container Not Found

**Symptoms**: `No such container`

**Fix**:
```bash
python scripts/debug.py containers --env production
invoke fr-app.setup
```

### Env Var Missing

**Symptoms**: `KeyError: 'DATABASE_URL'`

**Fix**:
```bash
invoke env.set DATABASE_URL "postgresql://..." finance_report app production
invoke fr-app.setup
```

### Deployment Failed

**Symptoms**: Deployment stuck

**Fix**:
```bash
python scripts/debug.py logs backend --tail 100
# Fix issue, then:
invoke fr-app.setup
```

### DB Connection Failed

**Symptoms**: `psycopg2.OperationalError`

**Fix**:
```bash
invoke fr-postgres.status
# Verify DATABASE_URL container name matches environment
invoke fr-app.setup
```

### Secret Not Syncing

**Symptoms**: Old value persists

**Fix**:
```bash
invoke env.get <KEY> finance_report app production
invoke fr-app.setup
```

---

## SOPs

### Deploy New Service

```bash
# 1. Secrets
invoke env.set DATABASE_URL "postgresql://..." myapp api production

# 2. Dependencies
invoke postgres.setup
invoke redis.setup

# 3. Deploy
invoke myapp.setup

# 4. Verify
python scripts/debug.py logs myapp --tail 50
curl https://myapp.zitian.party/health
```

### Modify Config

```bash
invoke env.set DEBUG false finance_report app production
invoke fr-app.setup
curl https://report.zitian.party/health
```

### Rotate Secrets

```bash
NEW_PASSWORD=$(openssl rand -base64 32)
invoke env.set DB_PASSWORD "$NEW_PASSWORD" finance_report app production
docker exec finance_report-postgres psql -U postgres -c "ALTER USER myuser PASSWORD '$NEW_PASSWORD';"
invoke env.set DATABASE_URL "postgresql://myuser:$NEW_PASSWORD@finance_report-postgres:5432/finance_report" finance_report app production
invoke fr-app.setup
```

---

## Emergency Procedures

### System Down

```bash
ssh root@$VPS_HOST "uptime"
ssh root@$VPS_HOST "docker ps"
ssh root@$VPS_HOST "systemctl restart docker"  # If needed
invoke fr-app.setup
```

### Database Corruption

```bash
# Backup
docker exec finance_report-postgres pg_dumpall > /tmp/backup.sql
scp root@$VPS_HOST:/tmp/backup.sql ./

# Restore
docker exec -i finance_report-postgres psql -U postgres < backup.sql
invoke fr-app.setup
```

### Vault Sealed

```bash
# Get keys from 1Password (bootstrap/vault)
ssh root@$VPS_HOST
docker exec -it vault vault operator unseal <KEY>  # Repeat 3x
invoke fr-app.setup
```

---

## Observability

### SigNoz

- Staging: `https://signoz-staging.zitian.party`
- Production: `https://signoz.zitian.party`
- Query: `service_name = "finance-report-backend"`

### Health Checks

```bash
curl https://report.zitian.party/health
invoke fr-app.status
```

---

## Multi-Environment

### Environment Variables

```bash
# Production (default)
export DEPLOY_ENV=production
→ Container: finance-report-backend
→ Path: /data/finance-report

# Staging
export DEPLOY_ENV=staging
→ Container: finance-report-backend-staging
→ Path: /data/finance-report-staging

# PR
export DEPLOY_ENV=pr-47
→ Container: finance-report-backend-pr-47
→ Path: /data/finance-report-pr-47
```

### Dokploy Network

**Critical**: Use unique container names.

❌ Wrong: `container_name: postgres`
✅ Right: `container_name: finance-report-db-pr-47`

---

## Security Best Practices

**DO**:
- Use `invoke` for operations
- Read-only SSH for investigation
- Rotate secrets every 90 days
- Verify health after changes
- Use environment-specific container names

**DON'T**:
- Modify files on VPS (deploy via CI)
- Use browser for production ops
- Hardcode secrets
- Use generic container names
- Skip health checks

---

## Quick Reference

```bash
# Debug
python scripts/debug.py logs backend --env production
python scripts/debug.py status backend --env production

# Secrets
invoke env.get DATABASE_URL finance_report app production
invoke env.set DEBUG false finance_report app production
invoke env.list-all finance_report app production

# Deploy
invoke fr-app.setup
invoke fr-postgres.setup
invoke fr-redis.setup

# Health
invoke fr-app.status
curl https://report.zitian.party/health
```

---

## Related Docs

- [AGENTS.md](../../../AGENTS.md) — Behavioral guidelines
- [development.md](../../../docs/ssot/development.md) — Dev workflows
- [observability.md](../../../docs/ssot/observability.md) — Logging
- [secrets-management](../secrets-management/skill.md) — Env vars
