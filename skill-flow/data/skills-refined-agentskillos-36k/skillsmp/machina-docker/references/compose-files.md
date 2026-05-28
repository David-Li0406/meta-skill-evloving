# Docker Compose Files Reference

Complete documentation of all Docker Compose files in the machina-meta workspace.

---

## Primary Stack

### Root docker-compose.yaml

**Location:** `machina-meta/docker-compose.yaml`
**Purpose:** Main workspace stack - the primary development environment
**Profile:** `dev`

**Services:**

| Service | Image | Ports | Purpose |
|---------|-------|-------|---------|
| postgres | postgres:17.5-bookworm | 5432 | Primary database |
| neo4j | neo4j:5.26 | 7474, 7687 | Graph database |
| redis | redis:7-alpine | 6379 | Cache and pub/sub |
| qdrant | qdrant/qdrant:v1.15.4 | 6333, 6334 | Vector embeddings |
| redisinsight | redis/redisinsight:latest | 5540 | Redis admin UI |
| backend | (built locally) | 8000 | FastAPI backend |
| medical-catalog | (built locally) | 8001 | Catalog service |
| frontend | (built locally) | 3000 | Next.js frontend |

**Volumes:**
- `postgres_data` - PostgreSQL data
- `neo4j_data` - Neo4j graph data
- `neo4j_logs` - Neo4j logs
- `neo4j_import` - Neo4j import directory
- `redis_data` - Redis persistence
- `qdrant_storage` - Vector storage
- `redisinsight_data` - RedisInsight settings

**Key Configuration:**
```yaml
# Neo4j APOC plugin enabled
NEO4J_PLUGINS: '["apoc"]'
NEO4J_dbms_security_procedures_unrestricted: apoc.*

# Redis AOF persistence
command: redis-server --appendonly yes

# Health checks on all services
healthcheck:
  test: ["CMD", "pg_isready", "-U", "postgres"]
  interval: 10s
  timeout: 5s
  retries: 5
```

**Usage:**
```bash
# Start (via dev_stack.py)
just dev-up

# Direct docker compose
docker compose --profile dev up -d
```

---

## Backend Development

### repos/dem2/infrastructure/docker-compose.yaml

**Location:** `repos/dem2/infrastructure/docker-compose.yaml`
**Purpose:** Backend development environment (databases)
**Profiles:** `dev`, `test`

**Services:**

| Service | Profile | Image | Ports |
|---------|---------|-------|-------|
| neo4j | dev, test | neo4j:5.26 | 7474, 7687 |
| qdrant | dev | qdrant/qdrant:v1.15.4 | 6333, 6334 |
| postgres | dev, test | postgres:17.5-bookworm | 5432 |
| redis | dev, test | redis:7-alpine | 6379 |
| redisinsight | dev, test | redis/redisinsight:latest | 5540 |
| machina-med-api | test | (built locally) | 8000 |

**Key Configuration:**
- Uses `.env.postgres` for PostgreSQL credentials
- Dynaconf environment settings via `DYNACONF_*` variables
- Profile-based selective startup

**Usage (DEPRECATED - use workspace commands):**
```bash
# Deprecated - use `just dev-up` instead
(cd repos/dem2 && docker compose -f infrastructure/docker-compose.yaml --profile dev up -d)
```

---

## Observability

### repos/dem2/infrastructure/docker-compose.langfuse.local.yaml

**Location:** `repos/dem2/infrastructure/docker-compose.langfuse.local.yaml`
**Purpose:** Local Langfuse observability stack

**Services:**

| Service | Image | Ports | Purpose |
|---------|-------|-------|---------|
| langfuse-web | langfuse/langfuse:3 | 3003 | Web UI |
| langfuse-worker | langfuse/langfuse:3 | 3030 | Background worker |
| postgres | postgres:15 | 5433 | Langfuse database |
| redis | redis:7 | 6380 | Langfuse cache |
| clickhouse | clickhouse/clickhouse-server:latest | 8123, 9005 | Analytics |
| minio | minio/minio:latest | 9090, 9091 | S3-compatible storage |

**Volumes:**
- `postgres_data` - Langfuse PostgreSQL
- `redis_data` - Langfuse Redis
- `clickhouse_data` - ClickHouse analytics
- `minio_data` - MinIO object storage

**Key Configuration:**
- ClickHouse runs as user 101:101
- Redis has password authentication
- MinIO configured for S3 event uploading

**Usage:**
```bash
(cd repos/dem2/infrastructure && docker compose -f docker-compose.langfuse.local.yaml up -d)
```

---

### repos/dem2-infra/infrastructure/docker/google_cloud/monitoring/docker-compose.langfuse.yaml

**Location:** `repos/dem2-infra/infrastructure/docker/google_cloud/monitoring/docker-compose.langfuse.yaml`
**Purpose:** Production Langfuse with OpenTelemetry collector
**Profile:** `monitoring`

**Additional Services:**
- `otel-collector` - OpenTelemetry collector (ports 4317, 4318, 8889)

**Key Configuration:**
- OTEL gRPC receiver on 4317
- OTEL HTTP receiver on 4318
- Prometheus metrics on 8889

---

## Debugging Tools

### repos/dem2/infrastructure/remote-debug/docker-compose.yml

**Location:** `repos/dem2/infrastructure/remote-debug/docker-compose.yml`
**Purpose:** Remote debugging utilities

**Services:**

| Service | Image | Ports | Purpose |
|---------|-------|-------|---------|
| pgadmin | dpage/pgadmin4:latest | 5050 | PostgreSQL admin |
| neo4j | neo4j:2025.08.0 | 17474 | Neo4j browser (newer version) |

**Key Configuration:**
- pgAdmin with extra hosts for docker.internal
- PostgreSQL server config mounted
- Different Neo4j version for testing

**Usage:**
```bash
(cd repos/dem2/infrastructure/remote-debug && docker compose up -d)
```

---

## Standalone Services

### repos/dem2/services/indicators-catalog/docker-compose.qdrant.yaml

**Location:** `repos/dem2/services/indicators-catalog/docker-compose.qdrant.yaml`
**Purpose:** Standalone Qdrant for indicators development

**Services:**
- `qdrant` - qdrant/qdrant:v1.12.5 (ports 6333, 6334)

**Usage:**
```bash
(cd repos/dem2/services/indicators-catalog && docker compose -f docker-compose.qdrant.yaml up -d)
```

---

### repos/medical-catalog/infra/docker-compose.yaml

**Location:** `repos/medical-catalog/infra/docker-compose.yaml`
**Purpose:** Medical catalog Qdrant (different ports)
**Profile:** `dev`

**Services:**
- `qdrant` - qdrant/qdrant:v1.15.5 (ports **16333**, **16334**)

**Note:** Uses non-standard ports to avoid conflicts with main Qdrant.

**Usage (DEPRECATED):**
```bash
# Deprecated - conflicts avoided by using main stack
(cd repos/medical-catalog && docker compose -f infra/docker-compose.yaml --profile dev up -d)
```

---

## DevOps Container

### gcloud-admin/docker-compose.yaml

**Location:** `gcloud-admin/docker-compose.yaml`
**Purpose:** DevOps admin container for GKE operations

**Services:**
- `gcloud-admin` - Built from local Dockerfile

**Volumes:**
- `gcloud-config` - GCP credentials (persistent)
- `kube-config` - Kubernetes config (persistent)
- `argocd-config` - ArgoCD auth (persistent)
- `gh-config` - GitHub CLI auth (persistent)

**Key Configuration:**
- Interactive mode (`-it` flags)
- Docker socket mounted for image builds
- Network capabilities (NET_ADMIN, NET_RAW)
- Workspace mounted at `/workspace`
- Host SSH keys (read-only)

**Usage:**
```bash
just gcloud-admin::shell
just gcloud-admin::kubectl get pods
```

---

## Gateway Infrastructure

### repos/dem2-infra/infrastructure/docker/google_cloud/gateway/docker-compose.ngrok-nginx.yaml

**Location:** `repos/dem2-infra/infrastructure/docker/google_cloud/gateway/docker-compose.ngrok-nginx.yaml`
**Purpose:** Public tunnel and reverse proxy

**Services:**

| Service | Image | Ports | Purpose |
|---------|-------|-------|---------|
| ngrok | ngrok/ngrok:3.25.0-alpine | 4040 | Secure tunnel |
| nginx | nginx:alpine | 80, 443 | Reverse proxy |

**Key Configuration:**
- External network: `ngrok-network` (must pre-exist)
- OAuth configuration for ngrok
- SSL/HTTPS support
- nginx depends on ngrok health

**Environment Variables:**
- `NGROK_AUTHTOKEN`
- `OAUTH_CLIENT_ID` / `OAUTH_CLIENT_SECRET`
- `API_KEY`

---

## LLM Experiment Stacks

### repos/dem2-infra/infrastructure/docker/google_cloud/experiment-setup/docker-compose.ollama.yml

**Location:** `repos/dem2-infra/infrastructure/docker/google_cloud/experiment-setup/docker-compose.ollama.yml`
**Purpose:** Local LLM server with GPU

**Services:**
- `ollama` - ollama/ollama:latest (port 11434)

**Key Configuration:**
```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
environment:
  OLLAMA_ORIGINS: "*"
```

**Usage:**
```bash
(cd repos/dem2-infra/infrastructure/docker/google_cloud/experiment-setup && \
  docker compose -f docker-compose.ollama.yml up -d)

# Pull model
docker exec ollama ollama pull llama3.2
```

---

### repos/dem2-infra/infrastructure/docker/google_cloud/experiment-setup/docker-compose.vllm.yml

**Location:** `repos/dem2-infra/infrastructure/docker/google_cloud/experiment-setup/docker-compose.vllm.yml`
**Purpose:** vLLM OpenAI-compatible inference server

**Services:**
- `vllm` - vllm/vllm-openai:latest (port 8000)

**Key Configuration:**
```yaml
# Model and quantization
--model unsloth/medgemma-27b-it
--quantization bitsandbytes
--tensor-parallel-size 1
--max-model-len 8192
--enable-prefix-caching
```

**Volume:**
- `vllm_cache` - HuggingFace model cache

---

### repos/dem2-infra/infrastructure/docker/google_cloud/experiment-setup/docker-compose.litellm-langfuse.yml

**Location:** `repos/dem2-infra/infrastructure/docker/google_cloud/experiment-setup/docker-compose.litellm-langfuse.yml`
**Purpose:** LiteLLM proxy with Langfuse monitoring (experimental)

**Note:** LiteLLM configuration mostly commented out - experimental setup.

---

## Compose File Summary

| File | Primary Use | Profiles |
|------|-------------|----------|
| `docker-compose.yaml` (root) | **Main dev stack** | dev |
| `dem2/infrastructure/docker-compose.yaml` | Backend databases | dev, test |
| `dem2/infrastructure/docker-compose.langfuse.local.yaml` | Local observability | - |
| `dem2/infrastructure/remote-debug/docker-compose.yml` | Debug tools | - |
| `dem2/services/indicators-catalog/docker-compose.qdrant.yaml` | Standalone Qdrant | - |
| `medical-catalog/infra/docker-compose.yaml` | Catalog Qdrant | dev |
| `gcloud-admin/docker-compose.yaml` | DevOps container | - |
| `dem2-infra/.../gateway/docker-compose.ngrok-nginx.yaml` | Public gateway | - |
| `dem2-infra/.../monitoring/docker-compose.langfuse.yaml` | Prod monitoring | monitoring |
| `dem2-infra/.../experiment-setup/docker-compose.ollama.yml` | Local LLM | - |
| `dem2-infra/.../experiment-setup/docker-compose.vllm.yml` | vLLM inference | - |
| `dem2-infra/.../experiment-setup/docker-compose.litellm-langfuse.yml` | LiteLLM (experimental) | - |
