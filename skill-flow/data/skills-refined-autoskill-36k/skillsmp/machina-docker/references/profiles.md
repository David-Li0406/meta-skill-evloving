# Docker Compose Profiles Reference

Docker Compose profiles allow selective service startup based on use case.

---

## Unified Profile: `dev`

All services in the machina-meta workspace use a single unified `dev` profile.

| Profile | Services Included | Use Case |
|---------|-------------------|----------|
| `dev` | All services (databases + backend + frontend + catalog) | Full stack development |

---

## Services in `dev` Profile

**Database Services:**
- postgres (PostgreSQL relational database)
- neo4j (Graph database)
- redis (Cache/pub-sub)
- qdrant (Vector search)
- redisinsight (Redis admin UI)

**Application Services:**
- backend (FastAPI backend)
- medical-catalog (Catalog service)
- frontend (Next.js frontend)

---

## Starting the Stack

**Recommended Method:**
```bash
# Use just command (handles health checks, snapshot restore)
just dev-up
```

**Direct Docker Compose:**
```bash
docker compose --profile dev up -d
```

**With Rebuild:**
```bash
docker compose --profile dev up -d --build
# Or
just dev-restart
```

---

## Stopping the Stack

```bash
# Via just command
just dev-down

# Direct docker compose
docker compose --profile dev down
```

---

## When Profile is Required

**Required for lifecycle operations:**
- `docker compose --profile dev up`
- `docker compose --profile dev down`
- `docker compose --profile dev restart`
- `docker compose --profile dev build`

**NOT required for querying running containers:**
- `docker compose ps`
- `docker compose logs <service>`
- `docker compose exec <service> <command>`
- `docker stats`

---

## Typical Workflow

```bash
# Start full stack
just dev-up

# Check status
just dev-status

# Access services
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/docs
# Neo4j: http://localhost:7474
# Qdrant: http://localhost:6333/dashboard
# RedisInsight: http://localhost:5540

# View logs
docker compose logs backend --tail 50

# Stop when done
just dev-down
```

---

## Backend-Only Development

If you want to run the backend locally instead of in a container:

```bash
# Start full stack
just dev-up

# Stop the containerized backend
docker stop machina-meta-backend-1

# Run backend locally
(cd repos/dem2 && just run)
```

---

## Profile Definition in docker-compose.yaml

All services are assigned to the `dev` profile:

```yaml
services:
  postgres:
    image: postgres:17.5-bookworm
    # ... configuration ...
    profiles: ["dev"]

  neo4j:
    image: neo4j:5.26
    # ... configuration ...
    profiles: ["dev"]

  backend:
    build: ./repos/dem2
    # ... configuration ...
    profiles: ["dev"]

  # ... all services have profiles: ["dev"]
```

---

## Child Repository Compose Files

The child repositories (`repos/dem2/infrastructure/docker-compose.yaml`, etc.) may still have their own profile systems for legacy support. However, these are **deprecated** and should not be used directly.

**Always use workspace-level commands from machina-meta root:**
- `just dev-up` instead of `(cd repos/dem2 && just dev-env-up)`
- `just dev-down` instead of `(cd repos/dem2 && just dev-env-down)`

---

## Environment Variable Alternative

You can also set the profile via environment variable:

```bash
export COMPOSE_PROFILES=dev
docker compose up -d
```

Or inline:
```bash
COMPOSE_PROFILES=dev docker compose up -d
```
