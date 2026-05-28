---
name: Docker & Containers
description: Docker containerization, multi-stage builds, Docker Compose, and container best practices.
---

# Docker & Containers

## Context

Lumira V2 is fully containerized:

| Service | Image | Purpose |
|---------|-------|---------|
| `web` | Custom (Next.js) | Frontend application |
| `api` | Custom (NestJS) | Backend API |
| `postgres` | postgres:16-alpine | Database |
| `gotenberg` | gotenberg/gotenberg:8 | PDF generation |

---

## Directory Structure

```
lumira-monorepo/
├── apps/
│   ├── api/
│   │   └── Dockerfile
│   └── web/
│       └── Dockerfile
└── docker/
    └── docker-compose.yml
```

---

## Docker Compose

### Location: `docker/docker-compose.yml`

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

---

## Multi-Stage Dockerfile (API)

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

---

## Multi-Stage Dockerfile (Web)

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

---

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

---

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

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Prisma client not found | Ensure `pnpm db:generate` runs in build stage |
| Container can't reach DB | Check network and service names |
| Gotenberg OOM | Increase container memory limit |
| Build cache issues | Use `docker-compose build --no-cache` |
