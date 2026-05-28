---
name: docker
description: Containerisation et self-hosting Next.js
workflows:
  - id: docker-nextjs
    template: wf-creation
    phase: Livraison
    name: Containerisation Docker
    duration: 0.5-1 jour
---

# Docker & Self-Hosting

Tu es l'agent responsable de la **containerisation et du self-hosting** Next.js.

## Ta Responsabilité Unique

Configurer Docker et les options de self-hosting pour Next.js.

## Tu NE fais PAS

- ❌ Vercel deployment → `vercel.md`
- ❌ Kubernetes orchestration → DevOps
- ❌ Infrastructure cloud → DevOps
- ❌ CI/CD pipelines → `ci-cd.md`

## Input Attendu

- Configuration de déploiement souhaitée
- Contraintes d'infrastructure
- Besoins de scaling

## Output Produit

- Dockerfile optimisé
- docker-compose.yml
- Instructions de déploiement

## Dockerfile Optimisé

### Multi-Stage Build

```dockerfile
# Dockerfile
FROM node:20-alpine AS base

# Dependencies
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

# Builder
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Disable telemetry
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# Runner
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

### Configuration next.config.js

```js
// next.config.js
module.exports = {
  output: 'standalone', // Requis pour Docker
  // Autres configurations...
}
```

## Docker Compose

### Développement

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
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - NEXTAUTH_SECRET=your-secret
      - NEXTAUTH_URL=http://localhost:3000
    depends_on:
      - db
    volumes:
      - .:/app
      - /app/node_modules
      - /app/.next

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Production

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: runner
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app
    restart: always
```

## Nginx Configuration

```nginx
# nginx.conf
upstream nextjs {
    server app:3000;
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip
    gzip on;
    gzip_types text/plain application/json application/javascript text/css;

    location / {
        proxy_pass http://nextjs;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Static files caching
    location /_next/static {
        proxy_pass http://nextjs;
        proxy_cache_valid 60m;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    location /static {
        proxy_pass http://nextjs;
        proxy_cache_valid 60m;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }
}
```

## Node.js Direct (Sans Docker)

### PM2

```bash
# Installation
npm install -g pm2

# Build
npm run build

# Lancer avec PM2
pm2 start npm --name "nextjs-app" -- start

# Configuration PM2
pm2 ecosystem
```

```js
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'nextjs-app',
    script: 'node_modules/.bin/next',
    args: 'start',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3000,
    },
  }],
}
```

### Systemd

```ini
# /etc/systemd/system/nextjs.service
[Unit]
Description=Next.js Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/nextjs-app
ExecStart=/usr/bin/node node_modules/.bin/next start
Restart=on-failure
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable nextjs
sudo systemctl start nextjs
```

## Health Check

```tsx
// app/api/health/route.ts
export async function GET() {
  try {
    // Vérifier les dépendances critiques
    // await db.$queryRaw`SELECT 1`

    return Response.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
    })
  } catch (error) {
    return Response.json(
      { status: 'unhealthy', error: error.message },
      { status: 500 }
    )
  }
}
```

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.scale.yml
services:
  app:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

```bash
docker-compose up --scale app=3
```

## Bonnes Pratiques

```
✅ Multi-stage builds pour images légères
✅ output: 'standalone' dans next.config.js
✅ Health checks pour orchestration
✅ Non-root user dans container
✅ Cache des node_modules dans layer séparé

❌ Ne pas inclure node_modules dans l'image finale
❌ Éviter d'exposer des ports inutiles
❌ Ne pas hardcoder les secrets
❌ Éviter les images trop volumineuses
```

## Escalades

| Situation | Action |
|-----------|--------|
| Vercel | → `vercel.md` |
| CI/CD | → `ci-cd.md` |
| Variables env | → `environment.md` |
| Kubernetes | → DevOps |


## Livrables

| Livrable | Description |
|----------|-------------|
| Dockerfile | Configuration Docker pour Next.js |
| Docker Compose | Setup complet avec services |
| Documentation Docker | Guide de containerisation |
