---
name: Coolify v4 Deployment
description: Complete guide for deploying and managing Lumira V2 on Coolify v4.
---

# Coolify v4 Deployment

## Context

Lumira V2 is deployed on **Coolify v4**, a self-hosted PaaS alternative to Vercel/Heroku.

| App | Type | Domain |
|-----|------|--------|
| Web (SocioPulse) | Next.js | sociopulse.fr |
| Web (MedicoPulse) | Next.js | medicopulse.fr |
| API | NestJS | api.sociopulse.fr |
| PostgreSQL | Database | Internal |

---

## Coolify Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Coolify Server                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Web App    │  │  API App    │  │  PostgreSQL │     │
│  │  (Next.js)  │  │  (NestJS)   │  │  (Database) │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          │                              │
│  ┌───────────────────────▼────────────────────────┐    │
│  │              Traefik Reverse Proxy              │    │
│  │         (SSL, Load Balancing, Routing)          │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## Application Configuration

### Web Application (Next.js)

**Settings:**

| Setting | Value |
|---------|-------|
| Build Pack | Dockerfile |
| Dockerfile | `apps/web/Dockerfile` |
| Build Context | `/` (root) |
| Port | 3000 |
| Health Check | `/api/health` |

**Environment Variables:**

```bash
NEXT_PUBLIC_API_URL=https://api.sociopulse.fr
NEXT_PUBLIC_BRAND=sociopulse
NEXTAUTH_URL=https://sociopulse.fr
NEXTAUTH_SECRET=your-secret-key
```

---

### API Application (NestJS)

**Settings:**

| Setting | Value |
|---------|-------|
| Build Pack | Dockerfile |
| Dockerfile | `apps/api/Dockerfile` |
| Build Context | `/` (root) |
| Port | 3001 |
| Health Check | `/health` |

**Environment Variables:**

```bash
DATABASE_URL=postgresql://user:pass@postgres:5432/lumira
NODE_ENV=production
JWT_SECRET=your-jwt-secret
CORS_ORIGINS=https://sociopulse.fr,https://medicopulse.fr
GOTENBERG_URL=http://gotenberg:3000
VERTEX_AI_PROJECT_ID=your-project-id
VERTEX_AI_CREDENTIALS={"type":"service_account",...}
```

---

### PostgreSQL Database

**Settings:**

| Setting | Value |
|---------|-------|
| Type | PostgreSQL |
| Version | 16 |
| Port | 5432 (internal) |
| Volume | Persistent |

**Initial Setup:**

```sql
CREATE DATABASE lumira;
CREATE USER lumira WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE lumira TO lumira;
```

---

## Domain Configuration

### DNS Setup

```
# A Records
sociopulse.fr      -> Coolify Server IP
medicopulse.fr     -> Coolify Server IP
api.sociopulse.fr  -> Coolify Server IP

# CNAME (optional)
www.sociopulse.fr  -> sociopulse.fr
```

### SSL Certificates

Coolify automatically provisions Let's Encrypt certificates. Ensure:

1. DNS is properly configured
2. Port 80/443 are accessible
3. Domain is added in Coolify app settings

---

## GitHub Integration

### Webhook Setup

1. In Coolify: Copy webhook URL from app settings
2. In GitHub: Settings → Webhooks → Add webhook
3. Payload URL: Coolify webhook URL
4. Content type: `application/json`
5. Events: `push` (main branch)

### Auto-Deploy

Configure in Coolify:

- **Branch**: `main`
- **Auto-deploy**: Enabled
- **Build on push**: Yes

---

## Database Migrations

### Automatic (Recommended)

Add to Dockerfile:

```dockerfile
# After build, before CMD
RUN npx prisma migrate deploy
```

### Manual Migration

1. SSH into Coolify server
2. Access container: `docker exec -it [container_id] sh`
3. Run: `npx prisma migrate deploy`

Or via Coolify Terminal:

```bash
npx prisma migrate deploy
```

---

## Rollback Strategies

### Quick Rollback

1. In Coolify → Deployments
2. Find previous successful deployment
3. Click "Redeploy"

### Git-Based Rollback

```bash
git revert HEAD
git push origin main
# Coolify will auto-deploy the revert
```

### Manual Rollback

1. Disable auto-deploy temporarily
2. Change branch to specific commit/tag
3. Trigger manual deployment

---

## Environment Variables Management

### Secrets (Sensitive)

Use Coolify's built-in secrets management:

1. Settings → Secrets
2. Add secret with name and value
3. Reference in app: `${SECRET_NAME}`

### Environment Groups

Create groups for:

- `production` - All prod variables
- `staging` - Staging overrides
- `shared` - Common across all apps

---

## Logs & Monitoring

### View Logs

```bash
# In Coolify UI
Applications → [App] → Logs

# Or via SSH
docker logs -f [container_id]
```

### Log Persistence

Configure in Coolify:

- Log retention: 7 days
- Log driver: json-file
- Max size: 100MB

---

## Health Checks

### API Health Endpoint

```typescript
// apps/api/src/health/health.controller.ts
@Controller('health')
export class HealthController {
  @Get()
  check() {
    return { status: 'ok', timestamp: new Date().toISOString() };
  }
}
```

### Coolify Configuration

```yaml
Health Check:
  Path: /health
  Interval: 30s
  Timeout: 10s
  Retries: 3
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check Dockerfile path and context |
| Container exits | Check logs for errors |
| Database connection | Verify DATABASE_URL format |
| SSL not working | Check DNS propagation |
| Webhook not triggering | Verify webhook secret |
| Out of memory | Increase container limits |

### Common Commands

```bash
# Restart app
coolify app:restart [app-id]

# View build logs
coolify app:logs:build [app-id]

# Force rebuild
coolify app:build [app-id] --no-cache
```

---

## Best Practices

| ✅ DO | ❌ DON'T |
|-------|----------|
| Use secrets for sensitive data | Hardcode credentials |
| Enable health checks | Skip monitoring setup |
| Set up webhooks | Manually deploy each time |
| Test in staging first | Deploy directly to prod |
| Keep backups of DB | Rely on single instance |
| Monitor disk space | Ignore volume growth |
