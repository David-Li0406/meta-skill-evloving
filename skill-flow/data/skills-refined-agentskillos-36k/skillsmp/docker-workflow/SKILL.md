---
name: docker-workflow
description: Comprehensive Docker workflow assistant for containers, images, Dockerfiles, docker-compose, and best practices. Use when working with Docker containers, building images, debugging Docker issues, or optimizing Docker workflows.
---

# Docker Workflow Skill

## When to Use This Skill

Use this skill when:

- Writing or optimizing Dockerfiles
- Building and managing Docker images
- Running and debugging containers
- Using docker-compose for multi-container apps
- Troubleshooting Docker issues
- Implementing Docker best practices
- Optimizing image size and build time
- Setting up development environments

## Dockerfile Best Practices

### Basic Structure

```dockerfile
# Use specific version tags, never :latest
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy dependency files first (better caching)
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Use non-root user
USER node

# Start application
CMD ["node", "server.js"]
```

### Multi-Stage Builds (reduce image size)

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --from=builder /app/dist ./dist
USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### Python Example

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["python", "app.py"]
```

### Dockerfile Optimization Rules

1. **Order matters for caching**
   - Put least-changing instructions first
   - Put most-changing instructions last
   - Copy dependency files before source code

2. **Minimize layers**
   - Combine RUN commands with &&
   - Clean up in same RUN command

3. **Use .dockerignore**

   ```
   node_modules
   npm-debug.log
   .git
   .env
   .DS_Store
   *.md
   .vscode
   .idea
   __pycache__
   *.pyc
   .pytest_cache
   coverage/
   dist/
   build/
   ```

4. **Use specific base images**
   - ✅ `node:18-alpine` (specific, small)
   - ❌ `node:latest` (unpredictable)
   - ❌ `node` (large, unpredictable)

5. **Security practices**
   - Don't run as root
   - Use minimal base images (alpine)
   - Don't include secrets in image
   - Scan images for vulnerabilities

## Docker Commands Reference

### Image Management

```bash
# Build image
docker build -t myapp:1.0 .
docker build -t myapp:latest -f Dockerfile.prod .

# List images
docker images
docker images --filter "dangling=true"

# Remove images
docker rmi myapp:1.0
docker rmi $(docker images -q -f "dangling=true")  # Remove dangling

# Pull/Push images
docker pull nginx:alpine
docker push myregistry.com/myapp:1.0

# Inspect image
docker inspect myapp:1.0
docker history myapp:1.0  # See layers

# Tag image
docker tag myapp:1.0 myregistry.com/myapp:1.0

# Save/Load images
docker save myapp:1.0 > myapp.tar
docker load < myapp.tar
```

### Container Management

```bash
# Run container
docker run -d --name myapp -p 3000:3000 myapp:1.0
docker run -it --rm ubuntu:22.04 bash  # Interactive, auto-remove

# List containers
docker ps                    # Running containers
docker ps -a                # All containers
docker ps -a --filter "status=exited"

# Stop/Start containers
docker stop myapp
docker start myapp
docker restart myapp
docker stop $(docker ps -q)  # Stop all running

# Remove containers
docker rm myapp
docker rm -f myapp           # Force remove running container
docker rm $(docker ps -aq)   # Remove all stopped

# View logs
docker logs myapp
docker logs -f myapp         # Follow logs
docker logs --tail 100 myapp # Last 100 lines
docker logs --since 30m myapp # Last 30 minutes

# Execute commands in container
docker exec -it myapp bash
docker exec myapp ls /app
docker exec -it myapp sh     # For alpine-based

# Copy files
docker cp myapp:/app/data.txt ./
docker cp ./config.json myapp:/app/

# View resource usage
docker stats
docker stats myapp

# Inspect container
docker inspect myapp
docker port myapp            # See port mappings
```

### Volume Management

```bash
# Create volume
docker volume create mydata

# List volumes
docker volume ls

# Inspect volume
docker volume inspect mydata

# Remove volumes
docker volume rm mydata
docker volume prune          # Remove unused volumes

# Use volumes
docker run -v mydata:/app/data myapp:1.0
docker run -v $(pwd):/app myapp:1.0  # Bind mount
docker run --mount type=bind,source=$(pwd),target=/app myapp:1.0
```

### Network Management

```bash
# Create network
docker network create mynetwork

# List networks
docker network ls

# Inspect network
docker network inspect mynetwork

# Connect container to network
docker network connect mynetwork myapp

# Remove network
docker network rm mynetwork
docker network prune

# Run with network
docker run --network mynetwork myapp:1.0
```

### System Management

```bash
# View disk usage
docker system df

# Clean up everything
docker system prune          # Remove unused data
docker system prune -a       # Remove all unused images too
docker system prune -a --volumes  # Include volumes

# Remove specific unused resources
docker image prune
docker container prune
docker volume prune
docker network prune
```

## Docker Compose

### Basic docker-compose.yml

```yaml
version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://db:5432/mydb
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app
      - /app/node_modules
    networks:
      - mynetwork
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - mynetwork
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    networks:
      - mynetwork
    restart: unless-stopped

volumes:
  db_data:

networks:
  mynetwork:
    driver: bridge
```

### Full-Stack Example (Node + React + Postgres + Redis)

```yaml
version: "3.8"

services:
  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - app-network

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./backend:/app
      - /app/node_modules
    networks:
      - app-network
    restart: unless-stopped

  # Database
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis cache
  redis:
    image: redis:7-alpine
    networks:
      - app-network
    restart: unless-stopped

  # Nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - frontend
      - backend
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

### Docker Compose Commands

```bash
# Start services
docker-compose up
docker-compose up -d              # Detached mode
docker-compose up --build         # Rebuild images
docker-compose up -d app db       # Specific services

# Stop services
docker-compose stop
docker-compose down               # Stop and remove
docker-compose down -v            # Stop and remove volumes

# View logs
docker-compose logs
docker-compose logs -f app        # Follow specific service
docker-compose logs --tail=100    # Last 100 lines

# Execute commands
docker-compose exec app bash
docker-compose exec db psql -U postgres

# Build images
docker-compose build
docker-compose build --no-cache app

# Scale services
docker-compose up -d --scale app=3

# View status
docker-compose ps
docker-compose top

# Restart services
docker-compose restart
docker-compose restart app
```

### Environment Variables (.env file)

```bash
# .env file in same directory as docker-compose.yml
NODE_ENV=production
DATABASE_URL=postgresql://postgres:password@db:5432/myapp
JWT_SECRET=your-secret-key-here
REDIS_URL=redis://redis:6379
API_PORT=5000
```

Reference in docker-compose.yml:

```yaml
services:
  app:
    environment:
      - NODE_ENV=${NODE_ENV}
      - JWT_SECRET=${JWT_SECRET}
```

## Development vs Production Configurations

### docker-compose.dev.yml

```yaml
version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - ./src:/app/src # Hot reload
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=*
    ports:
      - "3000:3000"
      - "9229:9229" # Debug port
    command: npm run dev
```

### docker-compose.prod.yml

```yaml
version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    environment:
      - NODE_ENV=production
    ports:
      - "3000:3000"
    restart: always
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "0.50"
          memory: 512M
```

Usage:

```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Common Patterns & Solutions

### Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
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

### Wait for Database

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
```

Or use wait-for script:

```dockerfile
COPY wait-for.sh /wait-for.sh
RUN chmod +x /wait-for.sh
CMD ["/wait-for.sh", "db:5432", "--", "node", "server.js"]
```

### Multi-Architecture Builds

```bash
# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:1.0 .
```

### Secrets Management

```yaml
# docker-compose.yml
services:
  app:
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

## Debugging & Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs myapp

# Run in interactive mode
docker run -it myapp:1.0 bash

# Check container details
docker inspect myapp

# Override entrypoint for debugging
docker run -it --entrypoint /bin/sh myapp:1.0
```

### Permission Issues

```dockerfile
# Fix: Run as non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser
RUN chown -R appuser:appuser /app
USER appuser
```

### Image Too Large

```bash
# Check image size
docker images myapp

# See layer sizes
docker history myapp:1.0

# Solutions:
# 1. Use alpine base images
FROM node:18-alpine  # vs FROM node:18

# 2. Multi-stage builds
# 3. Minimize layers
# 4. Clean up in same RUN command
RUN apt-get update && apt-get install -y package && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 5. Use .dockerignore
```

### Slow Builds

```bash
# Use BuildKit (faster)
DOCKER_BUILDKIT=1 docker build -t myapp .

# Use build cache
docker build --cache-from myapp:latest -t myapp:1.0 .

# Layer caching tips:
# - Copy package files before source code
# - Don't invalidate cache unnecessarily
# - Order instructions from least to most frequently changing
```

### Networking Issues

```bash
# Check container network
docker inspect myapp | grep -A 20 NetworkSettings

# Test connectivity between containers
docker exec myapp ping db
docker exec myapp curl http://api:5000/health

# Check exposed ports
docker port myapp
```

### Volume Permission Issues

```bash
# On Linux: Match user IDs
docker run -u $(id -u):$(id -g) -v $(pwd):/app myapp

# Fix ownership
docker exec myapp chown -R node:node /app
```

### Out of Disk Space

```bash
# Check disk usage
docker system df

# Clean up
docker system prune -a --volumes

# Remove specific items
docker image prune -a
docker volume prune
docker container prune
```

## Security Best Practices

### Image Security

```dockerfile
# 1. Use minimal base images
FROM node:18-alpine  # Not FROM node:18

# 2. Don't run as root
USER node

# 3. Use specific versions
FROM node:18.17.1-alpine3.18

# 4. Scan for vulnerabilities
# Run: docker scan myapp:1.0

# 5. Don't include secrets
# Use build args for build-time secrets
ARG NPM_TOKEN
RUN echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc && \
    npm install && \
    rm -f .npmrc

# 6. Multi-stage builds to exclude dev dependencies
```

### Runtime Security

```yaml
services:
  app:
    # Read-only root filesystem
    read_only: true

    # Limit resources
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M

    # Drop capabilities
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE

    # Security options
    security_opt:
      - no-new-privileges:true
```

### Don't Commit Secrets

```bash
# Never do this:
ENV API_KEY=secret123  # ❌

# Instead use:
# 1. Environment variables at runtime
docker run -e API_KEY=secret123 myapp

# 2. Docker secrets (Swarm)
# 3. External secrets manager (AWS Secrets, Vault)
# 4. .env files (not committed to git)
```

## Performance Optimization

### Build Performance

```dockerfile
# Use BuildKit
# syntax=docker/dockerfile:1

# Leverage layer caching
COPY package*.json ./
RUN npm ci
COPY . .

# Parallel builds for multi-stage
```

### Runtime Performance

```yaml
services:
  app:
    # Resource limits
    deploy:
      resources:
        limits:
          cpus: "2"
          memory: 2G
        reservations:
          cpus: "1"
          memory: 1G

    # Logging driver (prevent log buildup)
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Quick Troubleshooting Checklist

### Container won't start

- [ ] Check logs: `docker logs container-name`
- [ ] Check if port is already in use
- [ ] Verify environment variables
- [ ] Check if dependencies are running
- [ ] Inspect health check status

### Can't connect to container

- [ ] Check port mapping: `docker port container-name`
- [ ] Verify container is running: `docker ps`
- [ ] Test from inside container: `docker exec container-name curl localhost:PORT`
- [ ] Check firewall/network settings
- [ ] Verify network configuration

### Build failures

- [ ] Check Dockerfile syntax
- [ ] Verify base image exists
- [ ] Check .dockerignore isn't excluding needed files
- [ ] Try building without cache: `docker build --no-cache`
- [ ] Check for network issues during build

### Permission errors

- [ ] Check user in Dockerfile
- [ ] Verify volume permissions
- [ ] Match host/container user IDs on Linux
- [ ] Check file ownership in container

## Common Use Cases

### Database with Persistent Data

```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Development Environment with Hot Reload

```yaml
services:
  app:
    build: .
    volumes:
      - ./src:/app/src
      - /app/node_modules # Prevent overwriting
    environment:
      - NODE_ENV=development
    command: npm run dev
```

### Microservices Architecture

```yaml
services:
  api-gateway:
    build: ./api-gateway
    ports:
      - "80:80"
    depends_on:
      - auth-service
      - user-service

  auth-service:
    build: ./auth-service
    environment:
      - SERVICE_NAME=auth

  user-service:
    build: ./user-service
    environment:
      - SERVICE_NAME=user
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Docker Build and Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: user/app:latest,user/app:${{ github.sha }}
```

## Tips for AI Collaboration

When working with AI agents and Docker:

1. **Provide context**: Share your Dockerfile, docker-compose.yml, and error messages
2. **Specify environment**: Mention OS, Docker version, resource constraints
3. **Clear requirements**: State what you're trying to achieve
4. **Include logs**: Share relevant error logs for debugging
5. **Iterative improvement**: Build and test incrementally

## Additional Resources

- Docker Documentation: https://docs.docker.com/
- Dockerfile Best Practices: https://docs.docker.com/develop/dev-best-practices/
- Docker Compose Spec: https://docs.docker.com/compose/compose-file/
- Docker Security: https://docs.docker.com/engine/security/
- Awesome Docker: https://github.com/veggiemonk/awesome-docker
