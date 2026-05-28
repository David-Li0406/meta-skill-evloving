---
name: infra-ops
description: "Use when working with infrastructure, deployments, Docker, CI/CD, or server management. Covers containerization, deployment workflows, and DevOps patterns."
---

# Infrastructure Operations

## Overview

Infrastructure and operations patterns covering Docker containerization, deployment workflows, CI/CD pipelines, and server management. Focus on reliable, reproducible deployments.

## When to Use

- Setting up Docker containers
- Configuring CI/CD pipelines
- Deploying to VPS/cloud
- Managing server infrastructure
- Automating deployments

## Quick Reference

| Area | Key Tools |
|------|-----------|
| **Containers** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions, Vercel, Railway |
| **Cloud** | AWS, GCP, DigitalOcean, Hetzner |
| **Proxy** | nginx, Caddy, Traefik |
| **Monitoring** | Uptime Kuma, Grafana, Prometheus |

---

## Docker Patterns

### Multi-Stage Dockerfile (Node.js)

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app

# Install dependencies first (cache layer)
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy only necessary files
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT 3000

CMD ["node", "server.js"]
```

### Docker Compose (Full Stack)

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### Docker Commands

```bash
# Build image
docker build -t myapp:latest .

# Run container
docker run -d -p 3000:3000 --name myapp myapp:latest

# View logs
docker logs -f myapp

# Execute command in container
docker exec -it myapp sh

# Compose commands
docker-compose up -d
docker-compose logs -f
docker-compose down
docker-compose down -v  # Remove volumes too
```

---

## CI/CD with GitHub Actions

### Build and Deploy Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Run linter
        run: npm run lint

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            cd /opt/myapp
            docker-compose pull
            docker-compose up -d
            docker system prune -f
```

### Environment Secrets

```yaml
# Set in GitHub repo settings
# Settings > Secrets and variables > Actions

secrets:
  - SERVER_HOST      # Your server IP/domain
  - SERVER_USER      # SSH username
  - SERVER_SSH_KEY   # Private SSH key
  - DATABASE_URL     # Production database URL
```

---

## Server Setup (VPS)

### Initial Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin

# Setup firewall
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Create app directory
sudo mkdir -p /opt/myapp
sudo chown $USER:$USER /opt/myapp
```

### Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/myapp
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### SSL with Certbot

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renewal (runs automatically via systemd)
sudo certbot renew --dry-run
```

---

## Deployment Workflows

### Zero-Downtime Deployment

```bash
#!/bin/bash
# deploy.sh

set -e

echo "Pulling latest image..."
docker-compose pull

echo "Starting new container..."
docker-compose up -d --no-deps --scale app=2 app

echo "Waiting for health check..."
sleep 30

echo "Removing old container..."
docker-compose up -d --no-deps --scale app=1 app

echo "Cleaning up..."
docker system prune -f

echo "Deployment complete!"
```

### Rollback Script

```bash
#!/bin/bash
# rollback.sh

PREVIOUS_TAG=${1:-"previous"}

echo "Rolling back to $PREVIOUS_TAG..."
docker-compose down
docker tag myapp:latest myapp:failed
docker tag myapp:$PREVIOUS_TAG myapp:latest
docker-compose up -d

echo "Rollback complete"
```

---

## Monitoring

### Health Check Endpoint

```typescript
// app/api/health/route.ts
export async function GET() {
  try {
    // Check database
    await db.$queryRaw`SELECT 1`;

    // Check Redis
    await redis.ping();

    return Response.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      services: {
        database: 'up',
        redis: 'up',
      },
    });
  } catch (error) {
    return Response.json(
      {
        status: 'unhealthy',
        error: error.message,
      },
      { status: 503 }
    );
  }
}
```

### Docker Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1
```

### Uptime Monitoring

```yaml
# docker-compose.yml - Add Uptime Kuma
uptime-kuma:
  image: louislam/uptime-kuma:1
  volumes:
    - uptime_data:/app/data
  ports:
    - "3001:3001"
  restart: unless-stopped
```

---

## Common Patterns

### Environment Variables

```bash
# .env.production (never commit)
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
SECRET_KEY=your-secret-key

# docker-compose.yml
services:
  app:
    env_file:
      - .env.production
```

### Database Migrations

```yaml
# GitHub Action step
- name: Run migrations
  run: |
    docker-compose exec -T app npx prisma migrate deploy
```

### Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR=/backups
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
docker-compose exec -T db pg_dump -U user app > $BACKUP_DIR/db_$DATE.sql

# Compress
gzip $BACKUP_DIR/db_$DATE.sql

# Remove old backups (keep 7 days)
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "Backup complete: db_$DATE.sql.gz"
```

---

## Red Flags - STOP

**Never:**
- Commit secrets or .env files
- Run containers as root in production
- Skip health checks
- Deploy without testing
- Use `latest` tag in production compose

**Always:**
- Use non-root users in containers
- Implement health checks
- Set up monitoring/alerting
- Have rollback plan ready
- Test deployments in staging first

---

## Integration

**Related skills:** git-expert, testing-patterns
**Tools:** Docker, GitHub Actions, nginx, Certbot
