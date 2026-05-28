# Docker Security Patterns

## Image Security

### Base Image Selection

```dockerfile
# ✅ Use specific versions, not latest
FROM node:20.10-alpine3.18

# ✅ Use minimal base images
FROM gcr.io/distroless/static-debian12

# ✅ Use official images
FROM python:3.12-slim

# ❌ Avoid
FROM ubuntu:latest  # Unpredictable
FROM random/image   # Unknown provenance
```

### Multi-Stage Builds

```dockerfile
# Build stage
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage - minimal image
FROM node:20-alpine AS production
WORKDIR /app

# Copy only what's needed
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

USER node
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### Vulnerability Scanning

```bash
# Scan with Trivy
trivy image myapp:latest

# Scan with Docker Scout
docker scout cves myapp:latest

# Scan in CI
trivy image --exit-code 1 --severity HIGH,CRITICAL myapp:latest
```

## Runtime Security

### Non-Root User

```dockerfile
# Create user and group
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

# Set ownership
COPY --chown=appuser:appgroup . /app

# Switch to non-root
USER appuser

# Or use numeric IDs
USER 1001:1001
```

### Read-Only Filesystem

```yaml
# docker-compose.yml
services:
  app:
    image: myapp:latest
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
    security_opt:
      - no-new-privileges:true
```

### Drop Capabilities

```yaml
services:
  app:
    image: myapp:latest
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if needed for port < 1024
```

### Seccomp and AppArmor

```yaml
services:
  app:
    image: myapp:latest
    security_opt:
      - seccomp:./seccomp-profile.json
      - apparmor:myapp-profile
```

## Dockerfile Best Practices

### Minimize Layers and Attack Surface

```dockerfile
# ✅ Combine RUN commands
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        package1 \
        package2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ❌ Creates extra layers and leaves cache
RUN apt-get update
RUN apt-get install -y package1
RUN apt-get install -y package2
```

### No Secrets in Images

```dockerfile
# ❌ Never do this
COPY .env /app/.env
ENV API_KEY=secret123

# ✅ Use runtime secrets
# docker run -e API_KEY=$API_KEY myapp

# ✅ Use Docker secrets
# docker secret create api_key ./secret.txt
```

### Use .dockerignore

```
# .dockerignore
.git
.env
*.md
node_modules
**/*.test.js
coverage/
.github/
```

### COPY vs ADD

```dockerfile
# ✅ Use COPY for local files
COPY ./src /app/src
COPY package.json ./

# ADD only when you need its special features
# - Extracting tar archives
# - Fetching remote URLs (prefer curl/wget)
ADD archive.tar.gz /app/
```

## Network Security

### Isolate Networks

```yaml
# docker-compose.yml
services:
  web:
    networks:
      - frontend
      - backend

  api:
    networks:
      - backend

  db:
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

### Limit Exposed Ports

```yaml
services:
  app:
    # ✅ Bind to localhost only
    ports:
      - "127.0.0.1:3000:3000"

    # ❌ Exposes to all interfaces
    ports:
      - "3000:3000"
```

## Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

    # Prevent fork bombs
    ulimits:
      nproc: 100
      nofile:
        soft: 1024
        hard: 2048
```

## Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
```

```yaml
# docker-compose.yml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Secrets Management

### Docker Secrets (Swarm)

```yaml
services:
  app:
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true  # Created with `docker secret create`
```

### Environment Files

```yaml
services:
  app:
    env_file:
      - .env.production
    environment:
      - NODE_ENV=production
      # Don't put secrets in compose file
```

## Audit Checklist

| Check | Command |
|-------|---------|
| Running as root? | `docker inspect --format='{{.Config.User}}' image` |
| Exposed ports? | `docker inspect --format='{{.Config.ExposedPorts}}' image` |
| Environment secrets? | `docker inspect --format='{{.Config.Env}}' image` |
| Image vulnerabilities? | `trivy image image:tag` |
| Privileged mode? | `docker inspect --format='{{.HostConfig.Privileged}}' container` |
| Capabilities? | `docker inspect --format='{{.HostConfig.CapAdd}}' container` |

## Security Scanning in CI

```yaml
# GitHub Actions
- name: Build image
  run: docker build -t myapp:${{ github.sha }} .

- name: Scan image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    exit-code: '1'
    severity: 'CRITICAL,HIGH'

- name: Check for secrets
  run: |
    docker history --no-trunc myapp:${{ github.sha }} | grep -i -E "(password|secret|key|token)" && exit 1 || true
```
