---
name: tech-stack-advisor
description: Advise on technology choices for new full-stack projects using the user's preferred stack (FastAPI + React + PostgreSQL). Use when starting a new project, discussing architecture decisions, choosing frameworks, scaffolding an application, or when the user asks what stack to use.
allowed-tools: Read, Grep, Glob, mcp__memory__search_nodes, mcp__memory__open_nodes, mcp__github__get_file_contents
---

# Tech Stack Advisor

This user has a well-established preferred technology stack for full-stack applications. Always recommend this stack unless there's a specific reason not to.

## Authoritative Source

**GitHub Template**: https://github.com/guthdx/fastapi-react-postgres-template

This is the canonical, production-ready template. Clone from here when starting new projects.

## Preferred Stack Summary

| Layer | Technology |
|-------|------------|
| Backend | FastAPI 0.115+ + SQLAlchemy 2.0 (async) + Alembic |
| Frontend | React 18 + Vite 5 + Axios |
| Database | PostgreSQL 16 Alpine |
| Infrastructure | Docker Compose + Nginx (production) |

## When to Use This Skill

- User is starting a new full-stack project
- User asks "what stack should I use?"
- User is choosing between frameworks
- User wants to scaffold a new application
- User mentions building an API with a frontend
- User discusses architecture decisions

## Instructions

1. **Check memory first** for the "Preferred Tech Stack" entity
2. **Recommend the FastAPI + React + PostgreSQL stack**
3. **Reference the GitHub template** as the source to clone
4. **Offer to scaffold** by cloning the template
5. **Remind about key patterns**:
   - Python 3.13 via `/opt/local/bin/python3.13` (not system Python 3.10)
   - Async SQLAlchemy with `asyncpg` driver
   - Pydantic Settings for configuration
   - Three-tier Docker architecture with health checks

## Quick Start Command

```bash
git clone https://github.com/guthdx/fastapi-react-postgres-template.git PROJECT_NAME
cd PROJECT_NAME
cp .env.production.example .env
# Edit .env
docker compose -f docker-compose.production.yml up -d --build
```

## Key Architecture Decisions

1. **Async by default**: FastAPI + async SQLAlchemy
2. **Environment-based config**: Pydantic BaseSettings
3. **Health checks everywhere**: db, backend, frontend all have health endpoints
4. **Docker-first**: Production uses docker-compose.production.yml
5. **Nginx for frontend**: Multi-stage build, serves static React build
6. **Traefik for local dev**: Route via `*.localhost` domains instead of port numbers

## Traefik Development Proxy (Required for New Projects)

All new projects MUST include Traefik labels for local development routing.

### Start Traefik First (Once)
```bash
cd ~/terminal_projects/claude_code/traefik && docker compose up -d
```

### Add to docker-compose.yml
```yaml
services:
  backend:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.PROJECTNAME-api.rule=Host(`PROJECTNAME-api.localhost`)"
      - "traefik.http.services.PROJECTNAME-api.loadbalancer.server.port=8000"
    networks:
      - traefik-dev
      - default

  frontend:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.PROJECTNAME.rule=Host(`PROJECTNAME.localhost`)"
      - "traefik.http.services.PROJECTNAME.loadbalancer.server.port=5173"
    networks:
      - traefik-dev
      - default

  db:
    # NO Traefik labels - database stays internal
    networks:
      - default

networks:
  traefik-dev:
    external: true
```

### Access Pattern
- Frontend: `http://PROJECTNAME.localhost`
- Backend API: `http://PROJECTNAME-api.localhost`
- Dashboard: `http://traefik.localhost` or `http://localhost:8080`

## Port Management

### PORT_REGISTRY.md
Always check `~/terminal_projects/claude_code/PORT_REGISTRY.md` before allocating ports.

### Reserved Port Ranges
| Range | Purpose |
|-------|---------|
| 5432-5439 | PostgreSQL databases |
| 8000-8099 | Backend APIs |
| 5173-5179 | Vite dev servers |
| 3000-3099 | Next.js / other frontends |

### Environment Variable Pattern
```yaml
ports:
  - "${POSTGRES_PORT:-5433}:5432"   # Use env var with unique default
  - "${BACKEND_PORT:-8002}:8000"
  - "${FRONTEND_PORT:-5174}:5173"
```

## Health Check Patterns

### FastAPI Backend (Python)
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

### PostgreSQL Database
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres}"]
  interval: 5s
  timeout: 5s
  retries: 5
```

### Vite Frontend (Skip for Dev)
Vite dev server doesn't work well with health checks. Disable in development:
```yaml
# healthcheck: disabled for Vite dev server
```

For production with Nginx:
```yaml
healthcheck:
  test: ["CMD", "wget", "-q", "--spider", "http://localhost/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## CORS Configuration for Traefik

Update CORS origins to include `.localhost` domains:
```yaml
environment:
  - BACKEND_CORS_ORIGINS=http://localhost:5173,http://PROJECTNAME.localhost,http://PROJECTNAME-api.localhost
```

## Local Working Examples

- `~/terminal_projects/claude_code/cyoa-honky-tonk` - Original stack demo
- `~/terminal_projects/claude_code/csep_barter_bank` - Traefik-enabled example
