# Port Mappings Reference

Complete port allocation for all Docker services in the machina-meta workspace.

---

## Primary Development Ports

These ports are used by the main development stack (`just dev-up`).

| Port | Service | Protocol | Health Check | Description |
|------|---------|----------|--------------|-------------|
| 3000 | Frontend | HTTP | http://localhost:3000 | Next.js application |
| 5432 | PostgreSQL | TCP | `pg_isready -h localhost` | Primary database |
| 5540 | RedisInsight | HTTP | http://localhost:5540 | Redis admin UI |
| 6333 | Qdrant REST | HTTP | http://localhost:6333/healthz | Vector search API |
| 6334 | Qdrant UI | HTTP | http://localhost:6334/dashboard | Qdrant web interface |
| 6379 | Redis | TCP | `redis-cli ping` | Cache and pub/sub |
| 7474 | Neo4j Browser | HTTP | http://localhost:7474 | Graph database UI |
| 7687 | Neo4j Bolt | TCP | (application connections) | Graph database protocol |
| 8000 | Backend API | HTTP | http://localhost:8000/docs | FastAPI backend |
| 8001 | Medical Catalog | HTTP | http://localhost:8001/health | Catalog service |

---

## Langfuse Observability Ports

Used when running local Langfuse stack.

| Port | Service | Protocol | Description |
|------|---------|----------|-------------|
| 3003 | Langfuse Web | HTTP | Observability dashboard |
| 3030 | Langfuse Worker | HTTP | Background job processor |
| 5433 | Langfuse PostgreSQL | TCP | Langfuse database (different from main) |
| 6380 | Langfuse Redis | TCP | Langfuse cache (different from main) |
| 8123 | ClickHouse HTTP | HTTP | Analytics query interface |
| 9005 | ClickHouse Native | TCP | ClickHouse native protocol |
| 9090 | MinIO API | HTTP | S3-compatible storage |
| 9091 | MinIO Console | HTTP | MinIO admin interface |

---

## Specialized/Debug Ports

| Port | Service | Stack | Description |
|------|---------|-------|-------------|
| 4040 | ngrok Web UI | Gateway | Tunnel status dashboard |
| 5050 | pgAdmin | remote-debug | PostgreSQL admin |
| 11434 | Ollama | experiment | Local LLM inference |
| 16333 | Qdrant (catalog) | medical-catalog | Alternate Qdrant instance |
| 16334 | Qdrant UI (catalog) | medical-catalog | Alternate Qdrant UI |
| 17474 | Neo4j (remote) | remote-debug | Debug Neo4j instance |

---

## Monitoring/OTEL Ports

Used in production Langfuse setup.

| Port | Service | Protocol | Description |
|------|---------|----------|-------------|
| 4317 | OTEL gRPC | gRPC | OpenTelemetry collector |
| 4318 | OTEL HTTP | HTTP | OpenTelemetry HTTP receiver |
| 8889 | Prometheus | HTTP | Metrics endpoint |

---

## Port Conflict Detection

### Check if a port is in use

```bash
# Using lsof
lsof -i :8000

# Using ss
ss -tulpn | grep 8000

# Using netstat
netstat -tulpn | grep 8000
```

### Common Conflicts

| Conflict | Likely Cause | Resolution |
|----------|--------------|------------|
| 3000 busy | Another Next.js app | Stop other dev server |
| 5432 busy | System PostgreSQL | Stop system postgres or change port |
| 8000 busy | Previous backend instance | `docker stop` or kill process |
| 6379 busy | System Redis | Stop system redis |

### Resolving Conflicts

```bash
# Find what's using the port
lsof -i :8000

# If it's a Docker container
docker ps | grep 8000
docker stop <container-name>

# If it's a local process
kill <pid>
```

---

## Port Ranges by Category

### Application Services (3000-3999)
- 3000: Frontend
- 3003: Langfuse Web
- 3030: Langfuse Worker

### Databases (5000-7999)
- 5432/5433: PostgreSQL
- 5540: RedisInsight
- 6333/16333: Qdrant REST
- 6334/16334: Qdrant UI
- 6379/6380: Redis
- 7474/17474: Neo4j Browser
- 7687: Neo4j Bolt

### Backend Services (8000-8999)
- 8000: Backend API / vLLM
- 8001: Medical Catalog
- 8123: ClickHouse HTTP
- 8889: Prometheus

### Object Storage (9000-9999)
- 9005: ClickHouse Native
- 9090: MinIO API
- 9091: MinIO Console

### LLM/AI (11000+)
- 11434: Ollama

---

## Docker Compose Port Syntax

```yaml
services:
  backend:
    ports:
      # host:container
      - "8000:8000"

      # Only expose to localhost
      - "127.0.0.1:8000:8000"

      # Random host port
      - "8000"  # Docker assigns random host port
```

---

## Checking All Running Ports

```bash
# All Docker containers and their ports
docker ps --format "table {{.Names}}\t{{.Ports}}"

# Just the port mappings
docker ps --format "{{.Ports}}" | tr ',' '\n' | sort -u
```
