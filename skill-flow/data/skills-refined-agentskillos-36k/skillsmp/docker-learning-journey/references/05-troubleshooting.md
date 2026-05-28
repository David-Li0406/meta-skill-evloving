# Docker Troubleshooting Guide

Common errors and how to fix them.

---

## Container Won't Start

### "port is already allocated"

```
Error: Bind for 0.0.0.0:8000 failed: port is already allocated
```

**Cause**: Another process is using that port.

**Solutions**:
```bash
# Find what's using the port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux

# Use different port
docker run -p 8001:8000 myapp

# Or stop the other container
docker ps
docker stop <container-using-port>
```

---

### "image not found"

```
Error: pull access denied, repository does not exist or requires authentication
```

**Cause**: Image name typo or private image.

**Solutions**:
```bash
# Check spelling
docker pull python:3.12-slim  # Correct
docker pull pytohn:3.12-slim  # Typo!

# For private images
docker login

# Check available tags
# Visit https://hub.docker.com/_/python
```

---

### "executable file not found"

```
Error: exec: "python": executable file not found
```

**Cause**: Wrong base image or PATH issue.

**Solutions**:
```bash
# Check what's in the image
docker run -it myimage /bin/sh
which python

# Use full path
CMD ["/usr/local/bin/python", "main.py"]
```

---

## Build Failures

### "COPY failed: file not found"

```
COPY failed: file not found in build context
```

**Cause**: File doesn't exist or is in .dockerignore.

**Solutions**:
```bash
# Check file exists
ls requirements.txt

# Check .dockerignore doesn't exclude it
cat .dockerignore

# Use correct path (relative to build context)
COPY ./requirements.txt .
```

---

### "pip install failed"

```
ERROR: Could not install packages due to an OSError
```

**Causes & Solutions**:

1. **Missing system dependencies**:
```dockerfile
RUN apt-get update && apt-get install -y gcc libpq-dev
RUN pip install psycopg2
```

2. **Network issues**:
```bash
docker build --network=host .
```

3. **Out of space**:
```bash
docker system prune -a
```

---

### "no space left on device"

```
Error: no space left on device
```

**Solution**:
```bash
# See what's using space
docker system df

# Clean up
docker system prune -a
docker volume prune

# Remove old images
docker image prune -a
```

---

## Runtime Errors

### Container exits immediately

**Cause**: Main process finished or crashed.

**Debug**:
```bash
# Check logs
docker logs <container>

# Check exit code
docker ps -a  # Look at STATUS column

# Run interactively
docker run -it myimage /bin/sh
```

**Common fixes**:
```dockerfile
# Keep container running for debugging
CMD ["tail", "-f", "/dev/null"]

# Or use exec form
CMD ["python", "main.py"]  # Not: CMD python main.py
```

---

### "connection refused" to database

```
sqlalchemy.exc.OperationalError: connection refused
```

**Causes & Solutions**:

1. **Database not ready yet**:
```yaml
# docker-compose.yml
api:
  depends_on:
    db:
      condition: service_healthy
db:
  healthcheck:
    test: ["CMD-SHELL", "pg_isready"]
```

2. **Wrong hostname**:
```python
# In Docker Compose, use service name
DATABASE_URL = "postgresql://user:pass@db:5432/app"
#                                      ^^ service name, not localhost!
```

3. **Network isolation**:
```yaml
# Ensure same network
services:
  api:
    networks:
      - app-network
  db:
    networks:
      - app-network
networks:
  app-network:
```

---

### "permission denied"

```
PermissionError: [Errno 13] Permission denied
```

**Cause**: Running as non-root without write access.

**Solutions**:
```dockerfile
# Option 1: Set ownership when copying
COPY --chown=app:app . .

# Option 2: Create directory with permissions
RUN mkdir -p /app/data && chown app:app /app/data

# Option 3: Run as root (not recommended for production)
USER root
```

---

## Docker Compose Issues

### "service not found"

```
Error: no such service: api
```

**Solutions**:
```bash
# Check you're in right directory
cat docker-compose.yml

# Check service name spelling
docker compose config

# Specify file explicitly
docker compose -f docker-compose.yml up
```

---

### Changes not reflected

**Cause**: Using cached image.

**Solutions**:
```bash
# Rebuild
docker compose up --build

# Force recreate
docker compose up --force-recreate

# Clear everything
docker compose down -v
docker compose build --no-cache
docker compose up
```

---

### Volume permissions on Linux

```
Error: permission denied when accessing mounted volume
```

**Solution**:
```bash
# Match container user to host user
docker run -u $(id -u):$(id -g) -v ./:/app myimage
```

Or in docker-compose.yml:
```yaml
services:
  api:
    user: "${UID}:${GID}"
```

---

## Network Issues

### Container can't reach internet

**Solutions**:
```bash
# Check DNS
docker run --rm alpine ping google.com

# Use host network
docker run --network host myimage

# Check Docker DNS settings
docker info | grep -i dns
```

---

### Containers can't reach each other

**Cause**: Different networks.

**Solutions**:
```bash
# Check networks
docker network ls
docker inspect <container> | grep NetworkMode

# Create shared network
docker network create mynet
docker run --network mynet --name app1 image1
docker run --network mynet --name app2 image2

# Now app2 can reach app1 by name
```

---

## Quick Diagnostics

### Check Container Status
```bash
docker ps -a
docker logs <container>
docker inspect <container>
```

### Check Image
```bash
docker images
docker history <image>
docker inspect <image>
```

### Check Resources
```bash
docker stats
docker system df
```

### Check Network
```bash
docker network ls
docker network inspect <network>
```

### Interactive Debug
```bash
# Shell into running container
docker exec -it <container> /bin/bash

# Run image with shell
docker run -it <image> /bin/bash
```

---

## Reset Everything

When all else fails:
```bash
# Stop all containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Remove all volumes
docker volume prune -f

# Remove all networks
docker network prune -f

# Nuclear option
docker system prune -a --volumes
```

**Warning**: This deletes ALL Docker data!
