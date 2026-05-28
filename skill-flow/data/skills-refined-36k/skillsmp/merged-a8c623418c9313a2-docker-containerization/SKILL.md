---
name: docker-containerization
description: Use this skill for best practices in Docker containerization, including image building, security, and orchestration with Docker Compose.
---

# Docker Containerization

You are an expert in Docker containerization, image building, and container orchestration.

## Core Principles

- Build minimal, secure container images.
- Follow the principle of one process per container.
- Use official base images when possible.
- Implement proper layer caching strategies.
- Never store secrets in images.

## Dockerfile Best Practices

### Multi-Stage Builds
- Use multi-stage builds to reduce image size.
- Separate build and runtime stages.
- Copy only necessary artifacts to the final image.

### Layer Optimization
- Order instructions from least to most frequently changing.
- Combine RUN commands to reduce layers.
- Use `.dockerignore` to exclude unnecessary files.
- Clean up package manager caches in the same layer.

### Base Images
- Use specific version tags, not `latest`.
- Prefer slim or alpine variants for smaller size.
- Scan base images for vulnerabilities.
- Consider distroless images for production.

## Security Best Practices

- Run containers as a non-root user.
- Use read-only file systems where possible.
- Implement health checks.
- Scan images for vulnerabilities regularly.
- Use secrets management, not environment variables for sensitive data.
- Implement resource limits (CPU, memory).

## Docker Compose

### Configuration
- Use version 3+ compose files.
- Define networks explicitly.
- Use volumes for persistent data.
- Implement `depends_on` with health checks.
- Use environment files for configuration.

### Development Workflow
- Mount source code for hot reloading.
- Use override files for environment-specific config.
- Implement proper logging drivers.
- Use build args for build-time variables.

### Example Docker Compose Configuration
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    restart: always
    environment:
      POSTGRES_USER: lumira
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: lumira
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - lumira-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U lumira"]
      interval: 10s
      timeout: 5s
      retries: 5

  gotenberg:
    image: gotenberg/gotenberg:8
    restart: always
    ports:
      - "3002:3000"
    networks:
      - lumira-network

  web:
    build:
      context: ..
      dockerfile: apps/web/Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://api:3001
    depends_on:
      - api
    networks:
      - lumira-network

  api:
    build:
      context: ..
      dockerfile: apps/api/Dockerfile
    ports:
      - "3001:3001"
    environment:
      - DATABASE_URL=postgresql://lumira:${POSTGRES_PASSWORD}@postgres:5432/lumira
      - GOTENBERG_URL=http://gotenberg:3000
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - lumira-network

networks:
  lumira-network:
    driver: bridge

volumes:
  postgres_data:
```

## Multi-Stage Dockerfile Example

### API Dockerfile
```dockerfile
# apps/api/Dockerfile

# Stage 1: Dependencies
FROM node:20-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install turbo
RUN npm install -g turbo pnpm

# Copy workspace files
COPY . .

# Prune for API only
RUN turbo prune api --docker

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app

RUN npm install -g pnpm

COPY --from=deps /app/out/json/ .
COPY --from=deps /app/out/pnpm-lock.yaml ./pnpm-lock.yaml
RUN pnpm install --frozen-lockfile

COPY --from=deps /app/out/full/ .
RUN pnpm db:generate
RUN pnpm turbo run build --filter=api

# Stage 3: Runner
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nestjs

COPY --from=builder --chown=nestjs:nodejs /app/apps/api/dist ./dist
COPY --from=builder --chown=nestjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nestjs:nodejs /app/packages/database ./packages/database

USER nestjs

EXPOSE 3001
CMD ["node", "dist/main.js"]
```

### Web Dockerfile
```dockerfile
# apps/web/Dockerfile

# Stage 1: Dependencies
FROM node:20-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

RUN npm install -g turbo pnpm

COPY . .
RUN turbo prune web --docker

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app

RUN npm install -g pnpm

COPY --from=deps /app/out/json/ .
COPY --from=deps /app/out/pnpm-lock.yaml ./pnpm-lock.yaml
RUN pnpm install --frozen-lockfile

COPY --from=deps /app/out/full/ .
RUN pnpm turbo run build --filter=web

# Stage 3: Runner
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/apps/web/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT=3000

CMD ["node", "server.js"]
```

## Commands

```bash
# Start all services
docker-compose up -d

# Build and start
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build api

# View logs
docker-compose logs -f api

# Stop all
docker-compose down

# Stop and remove volumes (careful!)
docker-compose down -v
```

## Health Checks

```yaml
# In docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3001/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Prisma client not found | Ensure `pnpm db:generate` runs in build stage. |
| Container can't reach DB | Check network and service names. |
| Gotenberg OOM | Increase container memory limit. |
| Build cache issues | Use `docker-compose build --no-cache`. |