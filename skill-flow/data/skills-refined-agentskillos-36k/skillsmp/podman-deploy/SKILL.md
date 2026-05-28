---
name: podman-deploy
description: Builds and deploys containers using Podman. Covers multi-stage builds, rootless containers, Compose workflows, and systemd Quadlet integration. Use when creating Containerfiles, setting up container deployments, or configuring container orchestration.
---

# Podman Container Deployment

## Containerfile (Multi-stage)

```dockerfile
# Build stage
FROM docker.io/library/golang:1.22-alpine AS builder
RUN apk add --no-cache git ca-certificates
WORKDIR /build
COPY go.mod go.sum ./
RUN go mod download
COPY . .
ARG VERSION=dev
RUN CGO_ENABLED=0 go build -ldflags="-s -w -X main.Version=${VERSION}" -o /app ./cmd/app

# Runtime stage
FROM docker.io/library/alpine:3.19
RUN apk add --no-cache ca-certificates tzdata && \
    addgroup -g 1000 app && adduser -u 1000 -G app -D app
COPY --from=builder /app /usr/local/bin/app
USER app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -q --spider http://localhost:8080/health || exit 1
ENTRYPOINT ["/usr/local/bin/app"]
```

## .containerignore

```
.git
node_modules
vendor
*.md
.env*
secrets/
```

## Build Commands

```bash
# Development build (latest ok for dev)
podman build -t myapp:dev .

# Versioned build (use for staging/prod)
VERSION=$(git describe --tags --always)
podman build --build-arg VERSION=${VERSION} -t myapp:${VERSION} .

# Multi-platform versioned
podman build --platform linux/amd64,linux/arm64 -t myapp:${VERSION} .
```

## Run Commands

```bash
# Development
podman run -d --name myapp -p 8080:8080 myapp:dev

# Production (always use version tag)
podman run -d --name myapp -p 8080:8080 myapp:v1.2.3

# With environment
podman run -d --name myapp --env-file .env -p 8080:8080 myapp:v1.2.3

# With secrets
podman secret create db_pass ./secrets/db_password.txt
podman run -d --secret db_pass,type=env,target=DB_PASSWORD myapp:v1.2.3

# With volume
podman run -d -v myapp_data:/data:Z myapp:v1.2.3
```

## Compose

### compose.yaml

```yaml
services:
  app:
    build: .
    ports: ["8080:8080"]
    environment:
      DATABASE_URL: postgres://db:5432/myapp
    depends_on:
      db: { condition: service_healthy }

  db:
    image: docker.io/library/postgres:16-alpine
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_pass
    volumes: [db_data:/var/lib/postgresql/data]
    secrets: [db_pass]
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s

volumes:
  db_data:

secrets:
  db_pass:
    file: ./secrets/db_password.txt
```

```bash
podman-compose up -d
podman-compose logs -f app
podman-compose down
```

## Systemd Quadlet

Deploy as systemd service (rootless):

### ~/.config/containers/systemd/app.container

```ini
[Unit]
Description=My App
After=network-online.target

[Container]
# Use versioned tag, not :latest
Image=ghcr.io/org/myapp:v1.2.3
PublishPort=8080:8080
Environment=APP_ENV=production
Secret=db_pass,type=env,target=DB_PASSWORD
Volume=app_data:/data:Z
HealthCmd=wget -q --spider http://localhost:8080/health

[Service]
Restart=always

[Install]
WantedBy=default.target
```

```bash
# Deploy
systemctl --user daemon-reload
systemctl --user start app
systemctl --user enable app

# Manage
systemctl --user status app
journalctl --user -u app -f
```

## Registry Operations

```bash
# Login
podman login ghcr.io -u USERNAME

# Tag and push
podman tag myapp:latest ghcr.io/org/myapp:v1.0
podman push ghcr.io/org/myapp:v1.0

# Pull
podman pull ghcr.io/org/myapp:v1.0
```

## Security Scan

```bash
# With Trivy
trivy image myapp:latest
trivy image --exit-code 1 --severity HIGH,CRITICAL myapp:latest
```

## Best Practices

1. **Non-root user**: Always `USER app` in Containerfile
2. **Multi-stage builds**: Minimize final image size
3. **Health checks**: Always define HEALTHCHECK
4. **Secrets**: Use `podman secret`, never embed in image
5. **Read-only**: Use `--read-only` when possible
6. **No latest in prod**: Use specific version tags

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Permission denied | Add `:Z` to volume mounts (SELinux) |
| Port in use | `podman ps -a`, stop conflicting container |
| Out of space | `podman system prune -a --volumes` |
| Can't pull | Check `podman login` to registry |
