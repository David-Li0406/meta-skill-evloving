---
name: docker-infrastructure
description: Guide for Docker containerization and Traefik reverse proxy configuration. Use this when modifying Docker Compose files, adding new services, configuring Traefik routing, or managing container infrastructure.
---

# Docker & Infrastructure

This skill covers the Docker containerization and Traefik reverse proxy setup for this homelab project.

## Technology Stack

- **Docker** - Container runtime
- **Docker Compose** - Multi-container orchestration
- **Traefik v2.10** - Reverse proxy and load balancer
- **Redis** - In-memory cache (Alpine image)
- **NFS Volumes** - Network storage from Synology NAS

## Compose Files

### Development (`compose.dev.yml`)

Full development configuration with hot-reloading and all services.

```bash
# Start all development services
docker compose -f compose.dev.yml up

# Start specific service
docker compose -f compose.dev.yml up api dashboard

# Rebuild and start
docker compose -f compose.dev.yml up --build

# View logs
docker compose -f compose.dev.yml logs -f [service_name]
```

### Production (`compose.pro.yml`)

Production overrides extending development config.

```bash
# Start production stack
docker compose -f compose.dev.yml -f compose.pro.yml up -d
```

## Services Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Traefik (:81, :8080)                    │
│                       Reverse Proxy/Router                       │
└─────────────────┬────────────────┬────────────────┬─────────────┘
                  │                │                │
         ┌────────▼────────┐ ┌─────▼─────┐ ┌───────▼──────┐
         │   api (:8000)   │ │ dashboard │ │ diagnostics  │
         │    FastAPI      │ │  (:5173)  │ │   api (:8000)│
         └────────┬────────┘ └───────────┘ └──────────────┘
                  │
         ┌────────▼────────┐
         │  cache (:6379)  │
         │     Redis       │
         └─────────────────┘
```

## Adding a New Service

### 1. Create Dockerfile

```dockerfile
FROM python:3.14-bookworm

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt
```

### 2. Add to `compose.dev.yml`

```yaml
services:
  my_service:
    container_name: my_service
    build:
      context: ./my_service
    command: 'python3 main.py'
    volumes:
      - ./my_service:/app/my_service
    environment:
      SERVER_IP: '${SERVER_IP}'
    restart: 'unless-stopped'
    # If service needs Traefik routing:
    labels:
      - 'traefik.enable=true'
      - 'traefik.http.routers.my_service.entrypoints=web'
      - 'traefik.http.routers.my_service.rule=Host(`${SERVER_IP}`) && PathPrefix(`/my_service`)'
```

### 3. Add Traefik Labels (if web-accessible)

For services that need HTTP routing through Traefik:

```yaml
labels:
  - 'traefik.enable=true'
  - 'traefik.http.routers.ROUTER_NAME.entrypoints=web'
  - 'traefik.http.routers.ROUTER_NAME.rule=Host(`${SERVER_IP}`) && PathPrefix(`/PREFIX`)'
  # Optional: Strip prefix before forwarding to service
  - 'traefik.http.routers.ROUTER_NAME.middlewares=ROUTER_NAME-stripprefix'
  - 'traefik.http.middlewares.ROUTER_NAME-stripprefix.stripprefix.prefixes=/PREFIX'
```

## Traefik Configuration

Traefik is configured via command-line arguments in `compose.dev.yml`:

```yaml
traefik:
  command:
    - '--log.level=INFO' # Logging level
    - '--api.insecure=true' # Enable API/Dashboard (dev only)
    - '--api.dashboard=true' # Enable web dashboard
    - '--providers.docker=true' # Use Docker as provider
    - '--providers.docker.exposedbydefault=false' # Require explicit labels
    - '--entrypoints.web.address=:81' # HTTP entrypoint
```

### Traefik Dashboard

Access at `http://${SERVER_IP}:8080/dashboard` in development.

### Routing Rules

Common Traefik routing patterns used in this project:

```yaml
# Host + Path prefix
'traefik.http.routers.api.rule=Host(`${SERVER_IP}`) && PathPrefix(`/api`)'

# Path prefix only
'traefik.http.routers.whoami.rule=PathPrefix(`/whoami`)'
```

## Environment Variables

Environment variables are defined in `.env` (see `.env.template`):

```bash
SERVER_IP=192.168.x.x
LEETCODE_USERNAME=username
GITHUB_USERNAME=username
NAS_IP=192.168.x.x
NAS_PORT=5000
# ... etc
```

## Secrets Management

Secrets are mounted from the `./secrets/` directory:

```yaml
secrets:
  pihole_password:
    file: './secrets/pihole_password.txt'
  slack_bot_token:
    file: './secrets/slack_bot_token.txt'
```

Access in services via `/run/secrets/SECRET_NAME`.

## NFS Volumes

The project uses NFS volumes to mount media from Synology NAS:

```yaml
volumes:
  media:
    driver_opts:
      type: 'nfs'
      o: 'addr=${NAS_IP},nolock,soft,rw'
      device: ':/volume1/media/'
```

## Available Tools

### Container Management

```bash
# View running containers
docker compose -f compose.dev.yml ps

# View all containers (including stopped)
docker compose -f compose.dev.yml ps -a

# Stop all services
docker compose -f compose.dev.yml down

# Stop and remove volumes
docker compose -f compose.dev.yml down -v

# Rebuild specific service
docker compose -f compose.dev.yml build my_service

# View container logs
docker compose -f compose.dev.yml logs -f my_service

# Execute command in running container
docker compose -f compose.dev.yml exec my_service bash
```

### Debugging

```bash
# Check Traefik routing
curl http://localhost:8080/api/http/routers

# Test service directly (bypassing Traefik)
docker compose -f compose.dev.yml exec api curl http://localhost:8000/

# Check container health
docker compose -f compose.dev.yml ps
```

## Best Practices

1. **Use `restart: unless-stopped`** for production services
2. **Mount source code as volumes** in development for hot-reloading
3. **Use named volumes** for persistent data
4. **Expose only necessary ports** - let Traefik handle external routing
5. **Use environment variables** for configuration that varies between environments
6. **Store secrets in `./secrets/`** directory, never commit them
7. **Use `expose` instead of `ports`** for internal services routed through Traefik

## Service-Specific Notes

### API Service

- Runs on port 8000 internally
- Accessible via `/api` through Traefik
- Connected to Redis cache

### Dashboard

- Development: Vite dev server on port 5173
- Production: Static build served via `serve`

### Redis Cache

- Persists data every 60 seconds with at least 1 change
- Port 6379 exposed for development debugging
