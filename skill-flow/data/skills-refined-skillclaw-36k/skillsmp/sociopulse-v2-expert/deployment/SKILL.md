---
name: Deployment Expert
description: Expert knowledge of Docker multi-stage builds, Coolify 4.0 configuration, and Traefik routing.
---

# Deployment Skill - SocioPulse V2

## Overview

Deployment uses **Docker** containers orchestrated by **Coolify 4.0** with **Traefik** reverse proxy.

---

## 1. Docker Build Strategy

### Frontend Dockerfile

```dockerfile
# Multi-stage build
FROM node:20-alpine AS base
FROM base AS deps
FROM base AS builder
FROM base AS runner

# Build with brand mode
ARG NEXT_PUBLIC_APP_MODE=SOCIAL
ENV NEXT_PUBLIC_APP_MODE=$NEXT_PUBLIC_APP_MODE

# Standalone output for smaller image
ENV NEXTTELEMETRY_DISABLED=1
RUN npm run build
```

### Build Commands

```bash
# SocioPulse
docker build \
  --build-arg NEXT_PUBLIC_APP_MODE=SOCIAL \
  -t sociopulse-web .

# MedicoPulse
docker build \
  --build-arg NEXT_PUBLIC_APP_MODE=MEDICAL \
  -t medicopulse-web .

# API
docker build -f Dockerfile.api -t sociopulse-api .
```

---

## 2. Coolify Configuration

### docker-compose.prod.yml

```yaml
version: '3.8'
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - JWT_SECRET=${JWT_SECRET}
    labels:
      - traefik.enable=true
      - traefik.http.routers.api.rule=Host(`api.sociopulse.fr`)
      - traefik.http.routers.api.entrypoints=websecure
      - traefik.http.routers.api.tls.certresolver=letsencrypt

  sociopulse-web:
    build:
      context: .
      args:
        - NEXT_PUBLIC_APP_MODE=SOCIAL
    labels:
      - traefik.http.routers.sociopulse.rule=Host(`sociopulse.fr`) || Host(`dash.sociopulse.fr`)

  medicopulse-web:
    build:
      context: .
      args:
        - NEXT_PUBLIC_APP_MODE=MEDICAL
    labels:
      - traefik.http.routers.medicopulse.rule=Host(`medicopulse.fr`)
```

---

## 3. Environment Variables

### Required Variables

```env
# Database
DATABASE_URL="postgresql://user:pass@postgres:5432/sociopulse"

# Auth
JWT_SECRET="your-32-char-minimum-secret"

# Stripe
STRIPE_SECRET_KEY="sk_live_..."
STRIPE_WEBHOOK_SECRET="whsec_..."

# LiveKit
LIVEKIT_URL="wss://meet.sociopulse.fr"
LIVEKIT_API_KEY="APIxxx"
LIVEKIT_API_SECRET="secretxxx"

# Frontend
NEXT_PUBLIC_API_URL="https://api.sociopulse.fr"
NEXT_PUBLIC_APP_MODE="SOCIAL" # or "MEDICAL"
```

---

## 4. Traefik Routing

### Domain Mapping

```
api.sociopulse.fr          → api:4000
sociopulse.fr              → sociopulse-web:3000
dash.sociopulse.fr         → sociopulse-web:3000
medicopulse.fr             → medicopulse-web:3000
```

### SSL/TLS (Let's Encrypt)

```yaml
labels:
  - traefik.http.routers.api.tls=true
  - traefik.http.routers.api.tls.certresolver=letsencrypt
```

---

## 5. Healthchecks

### Frontend

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1
```

### Backend

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:4000/api/health || exit 1
```

---

## 6. Database Migrations

### Production Workflow

```bash
# 1. Build & push API image
docker build -f Dockerfile.api -t registry/sociopulse-api:latest .
docker push registry/sociopulse-api:latest

# 2. SSH into server
ssh deploy@server

# 3. Run migrations
docker exec sociopulse-api npx prisma migrate deploy

# 4. Restart services
docker-compose restart
```

---

## 7. Deployment Checklist

### Pre-Deployment

- [ ] Set all environment variables in Coolify
- [ ] Configure PostgreSQL (internal network preferred)
- [ ] Test build locally with correct `NEXT_PUBLIC_APP_MODE`
- [ ] Verify DNS records point to Coolify server

### Deployment

- [ ] Push code to main branch
- [ ] Trigger Coolify build (auto or manual)
- [ ] Monitor build logs for errors
- [ ] Run database migrations
- [ ] Test healthchecks

### Post-Deployment

- [ ] Verify all 3 domains are live
- [ ] Test critical user flows (register, login, mission creation)
- [ ] Check Stripe webhooks are receiving events
- [ ] Monitor application logs for errors

---

## 8. Best Practices

### DO

✅ Use multi-stage builds (smaller images)  
✅ Set healthchecks for all services  
✅ Use internal network for database  
✅ Enable HTTPS with Let's Encrypt  
✅ Test builds locally before deploying

### DON'T

❌ Hardcode secrets in Dockerfile  
❌ Skip database backups  
❌ Deploy without testing migrations  
❌ Forget to set `NEXT_PUBLIC_*` env vars

---

*This deployment architecture ensures reliable, scalable, and secure production deployments on Coolify 4.0.*
