---
name: hub-deploy
permissionMode: bypassPermissions
description: Deploy MCP Hub to production server. Supports Docker Compose deployment, health checks, and service status monitoring.
---

# Hub Deploy Skill

Deployment of MCP Hub to production.

## Deployment Options

| Option | When to use |
|--------|-------------|
| **A: Deploy Script** | Automated server deployment |
| **B: GitHub Actions** | CI/CD on push to main |
| **C: Local Docker Compose** | Development and testing |
| **D: Manual Deploy** | Fallback / debugging |

---

### Option A: Deploy Script (Recommended)

Use the provided deploy script on your server:

```bash
# SSH to server
ssh user@your-server.com

# Run deploy script (deploys all services)
bash .claude/skills/hub-deploy/scripts/deploy.sh

# Deploy specific service
bash .claude/skills/hub-deploy/scripts/deploy.sh hub
```

**First-time setup:** Edit `scripts/deploy.sh` and configure:
- `ROOT` - Server path where repo lives
- `GIT_REMOTE` - Your Git repository URL
- `HEALTH_BASE_URL` - Your production domain
- `ALL_SERVICES` - Services to deploy

---

### Option B: GitHub Actions

Automatic deployment on push to main branch.

**Setup:**
1. Add secrets in GitHub repo settings:
   - `DEPLOY_HOST` - Server hostname or IP
   - `DEPLOY_USER` - SSH username
   - `DEPLOY_SSH_KEY` - SSH private key
   - `ANTHROPIC_API_KEY_LIMITED` (optional)

2. Edit `.github/workflows/deploy.yml`:
   - Update `REPO_PATH` to match your server setup

3. Push to main → automatic deploy

---

### Option C: Local Docker Compose

For local development:

```bash
# Start all services
docker compose -f deploy/docker-compose.yml up -d

# Start development mode with hot-reload
docker compose -f deploy/docker-compose.dev.yml up -d

# View logs
docker compose -f deploy/docker-compose.yml logs -f hub

# Restart specific service
docker compose -f deploy/docker-compose.yml restart hub
```

---

### Option D: Manual Deploy (Fallback)

When scripts/CI don't work:

```bash
# SSH to server
ssh user@your-server.com
cd /path/to/hub

# Pull latest
git stash && git pull && git stash drop

# Rebuild and restart
docker compose -f deploy/docker-compose.yml build hub
docker compose -f deploy/docker-compose.yml up -d --no-deps hub
```

**IMPORTANT:** Always use `--no-deps` to avoid restarting other services!

---

### Manual Container Restart

When you only need to restart a service:

```bash
# Restart hub only
docker compose restart hub

# Restart with rebuild
docker compose build hub && docker compose up -d --no-deps hub
```

---

## Services & Ports

| Service | Port | Health Endpoint |
|---------|------|-----------------|
| hub | 8080 | `/health` |
| notion | 3015 | Internal |
| agent-worker | 3007 | `/health` |
| dashboard | 3000 | `/` |

---

## Health Checks

```bash
# Local
curl http://localhost:8080/health

# Production (replace with your domain)
curl https://your-domain.com/health
```

Expected response:
```json
{
  "status": "ok",
  "services": {
    "hub": "healthy",
    "notion": "available",
    "agent-worker": "available"
  }
}
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Container won't start | `docker logs hub --tail 50` |
| Port conflict | Use `--no-deps` when restarting |
| Git pull conflict | `git stash && git pull && git stash pop` |
| Health check fails | Check logs, verify env vars |

### Common Errors

**"Port already allocated":**
```bash
# Check what's using the port
docker ps | grep 8080

# Restart only the hub service
docker compose up -d --no-deps hub
```

**Container not found:**
```bash
# List all containers
docker ps -a | grep hub

# Start manually
docker compose up -d hub
```

---

## Deployment Checklist

### Before Deploy
- [ ] Changes committed and pushed
- [ ] Tests passing locally
- [ ] .env file current on server

### After Deploy
- [ ] Health check returns 200
- [ ] Ping tool works
- [ ] Services show expected status

---

## Best Practices

1. **Before Deploy:**
   - Ensure changes are committed
   - Test locally with `docker-compose.dev.yml`

2. **After Deploy:**
   - Check health endpoint
   - Test connection from IDE or claude.ai

3. **On Problems:**
   - Check logs first
   - Document issues for future reference
