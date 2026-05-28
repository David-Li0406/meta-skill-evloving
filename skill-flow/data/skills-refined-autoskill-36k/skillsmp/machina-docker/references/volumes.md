# Volume Management Reference

Docker volumes for data persistence in the machina-meta workspace.

---

## Named Volumes Overview

| Volume | Service | Purpose | Data Type |
|--------|---------|---------|-----------|
| `postgres_data` | PostgreSQL | User data, sessions, app state | Relational |
| `neo4j_data` | Neo4j | Graph nodes and relationships | Graph |
| `neo4j_logs` | Neo4j | Database logs | Logs |
| `neo4j_import` | Neo4j | CSV/JSON import staging | Temp |
| `redis_data` | Redis | Cache persistence (AOF) | Key-value |
| `qdrant_storage` | Qdrant | Vector embeddings | Vectors |
| `redisinsight_data` | RedisInsight | UI configuration | Config |

---

## Volume Locations

Docker volumes are stored in Docker's data directory:

```bash
# List all volumes
docker volume ls

# Inspect volume details
docker volume inspect machina-meta_postgres_data

# Default location (Linux)
/var/lib/docker/volumes/
```

---

## Database Volumes

### PostgreSQL (`postgres_data`)

**Contents:** All application data including users, sessions, documents, observations.

**Persistence:** Required for development continuity.

**Reset:**
```bash
# Stop and remove volume
docker compose down -v

# Or specifically
docker volume rm machina-meta_postgres_data

# Then restart (will run migrations)
just dev-up
```

### Neo4j (`neo4j_data`, `neo4j_logs`)

**Contents:**
- `neo4j_data`: Graph database (nodes, relationships, indexes)
- `neo4j_logs`: Query logs, debug logs

**Persistence:** Required for graph data continuity.

**Reset:**
```bash
docker compose down
docker volume rm machina-meta_neo4j_data machina-meta_neo4j_logs
just dev-up
```

### Redis (`redis_data`)

**Contents:** Cached data, pub/sub state (AOF persistence enabled).

**Persistence:** Optional - can be recreated from source.

**Reset:**
```bash
docker volume rm machina-meta_redis_data
# Redis will start empty
```

### Qdrant (`qdrant_storage`)

**Contents:** Vector embeddings for semantic search.

**Persistence:** Important - contains catalog embeddings.

**Snapshot Restore:** `dev_stack.py` automatically restores snapshots on first startup.

---

## Qdrant Snapshot Management

### Automatic Restore

The `scripts/dev_stack.py` script:
1. Checks if `qdrant_storage` volume exists
2. If empty, triggers snapshot restore from `repos/medical-catalog`
3. Restores biomarker embeddings automatically

### Manual Restore

```bash
# Restore all snapshots
(cd repos/medical-catalog && just snapshot-restore-all)

# Verify collections
curl http://localhost:6333/collections
```

### Creating Snapshots

```bash
# Create snapshot of a collection
curl -X POST http://localhost:6333/collections/biomarkers/snapshots

# List snapshots
curl http://localhost:6333/collections/biomarkers/snapshots
```

---

## Volume Operations

### List Volumes

```bash
# All Docker volumes
docker volume ls

# Filter by project
docker volume ls | grep machina-meta
```

### Inspect Volume

```bash
# Show volume details
docker volume inspect machina-meta_postgres_data

# Output includes:
# - Mountpoint (filesystem location)
# - Created timestamp
# - Driver info
```

### Remove Volumes

```bash
# Remove specific volume (container must be stopped)
docker volume rm machina-meta_postgres_data

# Remove all volumes for a compose project
docker compose down -v

# Remove all unused volumes (DANGEROUS)
docker volume prune -f
```

### Backup Volume Data

```bash
# PostgreSQL backup
docker exec machina-meta-postgres-1 pg_dump -U postgres demodemo > backup.sql

# Neo4j backup (export to Cypher)
(cd scripts && python neo4j-query.py --export-database --export-file neo4j_backup.json)

# Generic volume backup
docker run --rm -v machina-meta_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres_backup.tar.gz /data
```

### Restore Volume Data

```bash
# PostgreSQL restore
cat backup.sql | docker exec -i machina-meta-postgres-1 psql -U postgres demodemo

# Neo4j restore
(cd scripts && python neo4j-query.py --import-database --import-file neo4j_backup.json)
```

---

## Volume Cleanup Strategies

### Development Reset

When you want to start fresh:

```bash
# Stop everything
just dev-down

# Remove all volumes
docker volume prune -f

# Start fresh (will restore Qdrant snapshots)
just dev-up
```

### Selective Reset

Keep some data, reset others:

```bash
# Stop services
just dev-down

# Remove only specific volumes
docker volume rm machina-meta_postgres_data
docker volume rm machina-meta_neo4j_data

# Keep Qdrant (embeddings take time to generate)
# docker volume rm machina-meta_qdrant_storage  # Skip this

# Restart
just dev-up
```

### Preserve Qdrant Embeddings

Qdrant embeddings are expensive to regenerate. To preserve them:

```bash
# Don't use -v flag
docker compose down  # Not 'down -v'

# Or explicitly keep qdrant volume
docker volume rm machina-meta_postgres_data
docker volume rm machina-meta_neo4j_data
docker volume rm machina-meta_redis_data
# Leave qdrant_storage alone
```

---

## Langfuse Volumes

When running local Langfuse stack:

| Volume | Service | Purpose |
|--------|---------|---------|
| `postgres_data` | Langfuse PostgreSQL | Langfuse traces/spans |
| `redis_data` | Langfuse Redis | Langfuse cache |
| `clickhouse_data` | ClickHouse | Analytics data |
| `minio_data` | MinIO | S3 event storage |

**Note:** These are separate from the main stack volumes due to different compose file context.

---

## gcloud-admin Volumes

Persistent credential storage:

| Volume | Purpose |
|--------|---------|
| `gcloud-config` | Google Cloud credentials |
| `kube-config` | Kubernetes configuration |
| `argocd-config` | ArgoCD authentication |
| `gh-config` | GitHub CLI authentication |

**Important:** These volumes persist authentication across container rebuilds.

```bash
# Reset all gcloud-admin auth
docker volume rm gcloud-admin_gcloud-config gcloud-admin_kube-config \
  gcloud-admin_argocd-config gcloud-admin_gh-config

# Re-authenticate
just gcloud-admin::setup-nonprod
```

---

## Best Practices

1. **Don't use `docker volume prune` casually** - it removes ALL unused volumes
2. **Backup before major changes** - especially PostgreSQL and Neo4j
3. **Keep Qdrant volumes** when possible - embeddings are expensive to regenerate
4. **Use `docker compose down` without `-v`** for normal stops
5. **Use `docker compose down -v`** only when you want a complete reset
