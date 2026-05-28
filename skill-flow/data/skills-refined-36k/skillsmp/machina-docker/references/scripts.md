# Docker Scripts Reference

Documentation for helper scripts that manage Docker operations.

---

## scripts/dev_stack.py

**Location:** `machina-meta/scripts/dev_stack.py`
**Type:** Python 3.13+ UVX script
**Purpose:** Main orchestrator for development stack lifecycle

### Commands

| Command | Purpose |
|---------|---------|
| `up` | Start full stack with health monitoring |
| `down` | Stop all services |
| `status` | Check all service health |

### Usage

```bash
# Via just (recommended)
just dev-up
just dev-down
just dev-status

# Direct invocation
./scripts/dev_stack.py up
./scripts/dev_stack.py down
./scripts/dev_stack.py status --format json
```

### Options

```
./scripts/dev_stack.py <command> [--format FORMAT]

Commands:
  up       Start full stack (dev profile)
  down     Stop all services
  status   Check service health

Options:
  --format {markdown|json}  Output format for status (default: markdown)
```

### Features

**Health Monitoring:**
- 90-second timeout for service startup
- Polls container health status
- Validates HTTP endpoints for web services
- Reports detailed status with color coding

**Qdrant Snapshot Restore:**
- Detects if `qdrant_storage` volume exists
- If empty, triggers snapshot restore from medical-catalog
- Ensures biomarker embeddings are available

**Error Analysis:**
- On failure, analyzes container logs
- Provides troubleshooting guidance
- Shows relevant log excerpts

### Docker Commands Used

```python
# Check service status
docker compose ps --format json

# Start services
docker compose --profile dev up -d --build

# Stop services
docker compose --profile dev down
docker compose -p machina-med down  # Legacy project cleanup

# Get compose config
docker compose config --format json

# Check volume
docker volume inspect qdrant_storage

# List containers
docker ps --format {{.Names}}
```

### Status Output

**Markdown format:**
```
╔═══════════════════════════════════════════════════════════════════════╗
║               Development Stack Status                                  ║
╠═══════════════════════════════════════════════════════════════════════╣
│ Service          │ Status    │ Port  │ Health                         │
├──────────────────┼───────────┼───────┼────────────────────────────────┤
│ postgres         │ running   │ 5432  │ healthy                        │
│ neo4j            │ running   │ 7474  │ healthy                        │
│ redis            │ running   │ 6379  │ healthy                        │
...
```

**JSON format:**
```json
{
  "services": [
    {"name": "postgres", "status": "running", "port": 5432, "health": "healthy"},
    ...
  ],
  "overall": "healthy"
}
```

---

## scripts/neo4j-query.py

**Location:** `machina-meta/scripts/neo4j-query.py`
**Type:** Python 3.13+ UVX script
**Purpose:** Execute Cypher queries and manage Neo4j data

### Usage

```bash
# Via just
just neo4j-query "MATCH (n) RETURN count(n)"
just neo4j-query --count-biomarkers
just neo4j-query --list-biomarkers

# Direct invocation
./scripts/neo4j-query.py "MATCH (n:Patient) RETURN n LIMIT 5"
./scripts/neo4j-query.py --export-database --export-file backup.json
```

### Options

```
neo4j-query.py [query] [OPTIONS]

Positional:
  query                    Cypher query to execute

Options:
  -f, --file FILE         Read query from file
  --format FORMAT         Output format: table|rows|json|markdown|neo4j|count

  --clear-biomarkers      Clear biomarker nodes
  --count-biomarkers      Count biomarker nodes
  --list-biomarkers       List all biomarkers with documents

  --export-database       Export entire database
  --export-file FILE      Output filename for export
  --export-format FORMAT  Export format: json|cypher

  --import-database       Import from file
  --import-file FILE      Input filename (default: neo4j_export.json)
  --import-format FORMAT  Import format: json|cypher

  --clear-all-data        Clear entire database (WARNING!)
```

### Docker Integration

The script reads Neo4j connection details from `docker-compose.yaml`:
- Parses `NEO4J_AUTH` environment variable
- Extracts port mappings
- Connects to containerized Neo4j

---

## repos/dem2/scripts/wait-for-neo4j.sh

**Location:** `repos/dem2/scripts/wait-for-neo4j.sh`
**Type:** Bash shell script
**Purpose:** Wait for Neo4j container to be ready

### Usage

```bash
./scripts/wait-for-neo4j.sh
```

### Behavior

1. Attempts to connect to Neo4j via `docker exec`
2. Uses 60-second timeout with exponential backoff
3. Verifies with simple Cypher query
4. Adds 5-second delay for Bolt connection initialization
5. Double-verifies for stability

### Docker Commands Used

```bash
docker exec machina-med-neo4j-1 cypher-shell -u neo4j -p demodemo "RETURN 1;"
```

---

## repos/dem2/scripts/extract_backend_logs.sh

**Location:** `repos/dem2/scripts/extract_backend_logs.sh`
**Type:** Bash shell script
**Purpose:** Extract and filter Docker container logs

### Usage

```bash
./scripts/extract_backend_logs.sh [OPTIONS]

Options:
  -s, --service SERVICE    Filter by service name
  -t, --tail LINES        Number of lines (default: 100)
  -f, --follow            Follow log output
  -g, --grep PATTERN      Filter by pattern
  -l, --level LEVEL       Filter by log level (DEBUG|INFO|WARNING|ERROR)
  --since DURATION        Show logs from duration (5m, 1h, 2d)
  -h, --help              Show help
```

### Examples

```bash
# Get last 100 lines of all logs
./scripts/extract_backend_logs.sh

# Follow medical-data-engine logs
./scripts/extract_backend_logs.sh -s medical-data-engine -f

# Show errors from last 10 minutes
./scripts/extract_backend_logs.sh -l ERROR --since 10m

# Grep for specific pattern
./scripts/extract_backend_logs.sh -g "traceback" -s backend
```

### Docker Commands Used

```bash
docker ps --format '{{.Names}}'
docker logs <container> --tail <n> [--follow] [--since <duration>]
```

---

## gcloud-admin/gcloud_admin_run.sh

**Location:** `gcloud-admin/gcloud_admin_run.sh`
**Type:** Bash shell script
**Purpose:** Run commands in gcloud-admin container

### Usage

```bash
./gcloud_admin_run.sh <command> [args...]

# Examples
./gcloud_admin_run.sh gh pr view 91 --repo NumberOne-AI/dem2-infra
./gcloud_admin_run.sh kubectl get pods -n argocd
./gcloud_admin_run.sh argocd app list
```

### Behavior

1. Changes to gcloud-admin directory
2. Runs command via `docker compose run --rm gcloud-admin`
3. Removes container after execution

---

## repos/dem2/infrastructure/entrypoint.sh

**Location:** `repos/dem2/infrastructure/entrypoint.sh`
**Type:** Bash shell script
**Purpose:** Docker container entrypoint for backend

### Behavior (runs inside container)

1. Waits for PostgreSQL with `pg_isready`
2. Runs Alembic database migrations
3. Runs Neo4j graph migrator
4. Starts Uvicorn FastAPI application

### Key Commands

```bash
# Wait for Postgres
until pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
  sleep 2
done

# Run migrations
alembic upgrade head
python -m src.db.graph_migrator

# Start app
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

---

## Gateway Startup Script

**Location:** `repos/dem2-infra/infrastructure/docker/google_cloud/gateway/startup-gateway.sh`
**Type:** Bash shell script (GCP instance startup)
**Purpose:** Bootstrap Docker on GCP compute instance

### Behavior

1. Installs Docker and Docker Compose
2. Downloads compose files from GCP metadata
3. Creates `ngrok-network`
4. Generates self-signed SSL certificates
5. Starts gateway services
6. Configures cron for auto-restart

### Docker Commands Used

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
systemctl start docker && systemctl enable docker

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/..." -o /usr/local/bin/docker-compose

# Create network
docker network create ngrok-network

# Start services
docker compose -f docker-compose.ngrok-nginx.yaml pull
docker compose -f docker-compose.ngrok-nginx.yaml up -d
```

---

## Script Summary

| Script | Purpose | Invocation |
|--------|---------|------------|
| `dev_stack.py` | Main stack orchestration | `just dev-up/down/status` |
| `neo4j-query.py` | Neo4j queries and backup | `just neo4j-query` |
| `wait-for-neo4j.sh` | Neo4j health wait | Called during startup |
| `extract_backend_logs.sh` | Log extraction | Direct execution |
| `gcloud_admin_run.sh` | gcloud-admin wrapper | Direct execution |
| `entrypoint.sh` | Container entrypoint | Used by Docker |
| `startup-gateway.sh` | GCP instance bootstrap | GCP metadata |
