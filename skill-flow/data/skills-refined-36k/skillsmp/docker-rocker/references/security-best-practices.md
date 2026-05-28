# Docker Security Best Practices

Security hardening for containerized FastAPI applications.

---

## Non-Root User

### Why Non-Root?

Running as root in containers:
- Allows container escape vulnerabilities
- Gives unnecessary filesystem access
- Violates principle of least privilege

### Implementation

```dockerfile
# Create user with specific UID/GID
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Set ownership when copying files
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app ./app ./app

# Switch to non-root user
USER app
```

### Verification

```bash
# Check running user
docker run --rm myapp:prod whoami
# Output: app

# Check process user
docker run --rm myapp:prod ps aux
# Processes should show 'app' not 'root'
```

---

## Secrets Management

### Never Do

```dockerfile
# NEVER hardcode secrets
ENV DATABASE_URL=postgresql://user:password@host/db
ENV SECRET_KEY=mysecretkey123

# NEVER copy .env files
COPY .env /app/.env
```

### Always Do

```dockerfile
# Set placeholders, inject at runtime
ENV DATABASE_URL="" \
    SECRET_KEY=""
```

```yaml
# docker-compose.yml
services:
  api:
    environment:
      - DATABASE_URL=${DATABASE_URL}  # From host environment
      - SECRET_KEY=${SECRET_KEY}
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### Docker Secrets (Swarm/Compose)

```yaml
services:
  api:
    secrets:
      - source: db_password
        target: /run/secrets/db_password
        mode: 0400

secrets:
  db_password:
    external: true  # Created via `docker secret create`
```

```python
# Read secret in application
from pathlib import Path

def get_secret(name: str) -> str:
    secret_file = Path(f"/run/secrets/{name}")
    if secret_file.exists():
        return secret_file.read_text().strip()
    return os.getenv(name.upper(), "")
```

---

## Image Security

### Minimal Base Images

```dockerfile
# Prefer slim images
FROM python:3.12-slim

# If using alpine, be aware of compatibility
FROM python:3.12-alpine  # Smaller but may have issues
```

### Vulnerability Scanning

```bash
# Docker Scout (built-in)
docker scout cves myapp:latest

# Trivy
trivy image myapp:latest

# Snyk
snyk container test myapp:latest
```

### Pin Image Versions

```dockerfile
# BAD: Latest can change unexpectedly
FROM python:latest

# BETTER: Pin major.minor
FROM python:3.12-slim

# BEST: Pin digest for reproducibility
FROM python:3.12-slim@sha256:abc123...
```

### Multi-Stage Security

```dockerfile
# Builder has build tools (potential vulnerabilities)
FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y gcc

# Runtime has minimal surface area
FROM python:3.12-slim AS runtime
# No gcc, no apt cache, no build tools
```

---

## Network Security

### Expose vs Ports

```yaml
# INTERNAL only (accessed by other containers)
services:
  api:
    expose:
      - "80"

# EXTERNAL (accessed from host)
services:
  api:
    ports:
      - "8080:80"
```

### Network Isolation

```yaml
services:
  api:
    networks:
      - frontend
      - backend

  db:
    networks:
      - backend  # Only accessible from backend network

networks:
  frontend:
  backend:
    internal: true  # No external access
```

### TLS/HTTPS

```dockerfile
# FastAPI handles HTTP, terminate TLS at proxy
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

```yaml
# Nginx handles TLS
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./certs:/etc/nginx/certs:ro
```

---

## Filesystem Security

### Read-Only Root

```yaml
services:
  api:
    read_only: true
    tmpfs:
      - /tmp
      - /app/cache
```

### No New Privileges

```yaml
services:
  api:
    security_opt:
      - no-new-privileges:true
```

### Drop Capabilities

```yaml
services:
  api:
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if needed for port < 1024
```

---

## Environment Hardening

### Python Security Settings

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
```

### Disable Debug in Production

```dockerfile
ENV DEBUG=false \
    ENVIRONMENT=production
```

```python
# app/core/config.py
class Settings(BaseSettings):
    debug: bool = False
    environment: str = "production"

# app/main.py
app = FastAPI(
    debug=settings.debug,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
)
```

---

## Health & Resource Limits

### Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:80/health')" || exit 1
```

### Resource Limits

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
          pids: 100
        reservations:
          cpus: '0.25'
          memory: 256M
```

### Restart Policy

```yaml
services:
  api:
    restart: unless-stopped
    # or for production
    deploy:
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
```

---

## .dockerignore Security

Prevent sensitive files from entering image:

```dockerignore
# Secrets
.env
.env.*
*.pem
*.key
secrets/
credentials/

# Git (may contain sensitive history)
.git
.gitignore

# IDE (may contain local configs)
.idea
.vscode

# Tests (may contain test credentials)
tests/fixtures/secrets/
```

---

## Security Checklist

### Build Time
- [ ] Using slim/minimal base image
- [ ] Pinned image versions
- [ ] Multi-stage build (no build tools in runtime)
- [ ] No secrets in Dockerfile or image
- [ ] .dockerignore excludes sensitive files
- [ ] Scanned for vulnerabilities

### Runtime
- [ ] Running as non-root user
- [ ] Read-only filesystem (where possible)
- [ ] Dropped unnecessary capabilities
- [ ] Resource limits configured
- [ ] Health checks enabled
- [ ] Debug disabled in production
- [ ] Network isolation configured

### Secrets
- [ ] No hardcoded secrets
- [ ] Using environment variables or Docker secrets
- [ ] Secrets not logged or exposed in errors
- [ ] .env files not in image

---

## Compliance Considerations

### OWASP Docker Security

1. Keep images minimal
2. Use non-root users
3. Sign and verify images
4. Scan for vulnerabilities
5. Limit resource usage
6. Use read-only filesystems
7. Enable logging and monitoring

### CIS Docker Benchmark

Key recommendations:
- Don't run containers as root
- Don't expose unnecessary ports
- Use trusted base images
- Implement resource limits
- Enable content trust
