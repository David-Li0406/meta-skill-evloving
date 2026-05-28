---
name: doctor
description: Diagnose environment issues, identify missing dependencies, and provide fix instructions
allowed-tools: Bash, Read, WebSearch
disable-model-invocation: true
argument-hint: [--fix|--infra|--db]
---

# Environment Diagnostics and Troubleshooting

Diagnose and fix issues with the devflow development environment.

## Usage

- `/devflow-doctor` - Full diagnostic scan
- `/devflow-doctor --fix` - Attempt automatic fixes where possible
- `/devflow-doctor --infra` - Focus on infrastructure issues (Traefik, network, certs)
- `/devflow-doctor --db` - Focus on database issues (connectivity, migrations)

## Diagnostic Steps

### Step 1: Run Built-in Doctor

```bash
devflow doctor
```

Parse the output to identify:
- Missing tools (gh, op, docker, supabase, psql, git)
- Authentication issues
- Configuration problems

### Step 2: Infrastructure Diagnostics (if --infra or full scan)

```bash
devflow infra doctor --json
```

Check:
- Docker daemon running
- mkcert installed and CA trusted
- devflow-proxy network exists
- Traefik container running
- TLS certificates valid

### Step 3: Database Diagnostics (if --db or full scan)

```bash
devflow db status --env local --json
```

Check:
- Database connectivity
- Migration table exists
- Any pending migrations
- Any failed migrations

### Step 4: Project Configuration

```bash
devflow config validate
```

Check:
- devflow.yml exists and is valid
- All required fields present
- Environment-specific configs correct

### Step 5: Docker Services

```bash
docker compose ps --format json
```

Check:
- All expected services defined
- Services are running
- No restart loops (check restart count)
- Port conflicts

## Common Issues and Fixes

### Docker Not Running

**Symptoms**: "Cannot connect to Docker daemon"

**Fix**:
- macOS/Windows: Start Docker Desktop
- Linux: `sudo systemctl start docker`

### mkcert CA Not Installed

**Symptoms**: "mkcert CA not installed"

**Fix**:
```bash
mkcert -install
```

### Port Already in Use

**Symptoms**: "port is already allocated"

**Diagnose**:
```bash
lsof -i :80
lsof -i :443
lsof -i :8088
```

**Fix**: Stop the conflicting process or change devflow ports in config.

### Database Connection Refused

**Symptoms**: "connection refused" or "could not connect"

**Check**:
1. Is the database container running?
2. Is DATABASE_URL correct?
3. Is the port exposed correctly?

### Traefik Not Routing

**Symptoms**: Services unreachable via domain names

**Check**:
1. Traefik container logs: `docker logs devflow-traefik`
2. Service has correct Traefik labels
3. Service is on devflow-proxy network
4. /etc/hosts has the domain entry

### Stale Network State

**Symptoms**: Network conflicts, orphaned containers

**Fix**:
```bash
devflow infra down --network
devflow infra up
```

## Output Format

Provide a clear summary:

```
DEVFLOW DOCTOR REPORT
=====================

Tools:
  [OK] docker (24.0.5)
  [OK] gh (2.40.0)
  [MISSING] op - Install: https://1password.com/downloads/command-line/

Infrastructure:
  [OK] Docker daemon running
  [OK] devflow-proxy network
  [WARN] Traefik not running - run: devflow infra up

Database:
  [OK] Connection successful
  [WARN] 3 pending migrations

Configuration:
  [OK] devflow.yml valid

Recommendations:
  1. Install 1Password CLI for secrets management
  2. Start infrastructure: devflow infra up
  3. Apply migrations: devflow db migrate --env local
```

## Auto-Fix Mode (--fix)

When --fix is specified, attempt to automatically resolve:
- Start Docker if not running (platform-specific)
- Run `devflow infra up` if infrastructure is down
- Run `mkcert -install` if CA not trusted
- Apply local migrations if pending

Always show what was fixed and what requires manual intervention.
