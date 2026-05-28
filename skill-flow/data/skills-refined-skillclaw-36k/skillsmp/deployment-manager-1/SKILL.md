---
name: deployment-manager
description: Deploy NutriProfile to production. Use this skill when deploying backend to Fly.io, frontend to Cloudflare Pages, managing secrets, running health checks, or troubleshooting deployment issues.
allowed-tools: Read,Write,Edit,Grep,Glob,Bash
---

# NutriProfile Deployment Manager Skill

You are a deployment expert for the NutriProfile application. This skill helps you deploy and manage the application on Fly.io (backend) and Cloudflare Pages (frontend).

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRODUCTION                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────┐      ┌──────────────────────┐        │
│  │   Cloudflare Pages   │      │       Fly.io         │        │
│  │   (Frontend)         │      │     (Backend)        │        │
│  │                      │      │                      │        │
│  │  nutriprofile.pages  │─────▶│  nutriprofile-api    │        │
│  │  .dev                │      │  .fly.dev            │        │
│  └──────────────────────┘      └──────────┬───────────┘        │
│                                           │                     │
│                                           ▼                     │
│                                ┌──────────────────────┐        │
│                                │   Fly Postgres       │        │
│                                │   (Database)         │        │
│                                │                      │        │
│                                │  nutriprofile-db     │        │
│                                └──────────────────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Fly.io CLI Setup

### Installation (Windows)
```powershell
# Already installed at:
# C:\Users\badre zouiri\.fly\bin\flyctl.exe

# Alias for convenience
$flyctl = "C:\Users\badre zouiri\.fly\bin\flyctl.exe"
```

### Authentication
```bash
# Login
flyctl auth login

# Check auth status
flyctl auth whoami
```

## Backend Deployment (Fly.io)

### Configuration
```toml
# backend/fly.toml
app = "nutriprofile-api"
primary_region = "cdg"  # Paris

[build]

[env]
  PORT = "8000"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[services]]
  protocol = "tcp"
  internal_port = 8000

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

  [[services.http_checks]]
    interval = "30s"
    timeout = "5s"
    path = "/health"
```

### Dockerfile
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Deploy Commands
```bash
# Navigate to backend directory
cd backend

# Deploy (uses fly.toml)
"C:\Users\badre zouiri\.fly\bin\flyctl.exe" deploy

# Deploy with specific strategy
flyctl deploy --strategy immediate

# Deploy without cache (for troubleshooting)
flyctl deploy --strategy immediate --no-cache

# Deploy with remote builder
flyctl deploy --strategy immediate --remote-only
```

### Environment Secrets
```bash
# List secrets
flyctl secrets list --app nutriprofile-api

# Set single secret
flyctl secrets set SECRET_KEY="your-secret-key" --app nutriprofile-api

# Set multiple secrets
flyctl secrets set \
  DATABASE_URL="postgres://..." \
  HUGGINGFACE_TOKEN="hf_..." \
  LEMONSQUEEZY_API_KEY="eyJ..." \
  --app nutriprofile-api

# Required secrets:
# - SECRET_KEY (JWT signing)
# - DATABASE_URL (Postgres connection)
# - HUGGINGFACE_TOKEN (AI models)
# - LEMONSQUEEZY_API_KEY (Payments)
# - LEMONSQUEEZY_WEBHOOK_SECRET (Webhook validation)
# - USDA_API_KEY (Food database)
```

### Monitoring
```bash
# View logs
flyctl logs --app nutriprofile-api

# View logs without following
flyctl logs --app nutriprofile-api --no-tail

# Check status
flyctl status --app nutriprofile-api

# Scale resources
flyctl scale show --app nutriprofile-api
flyctl scale memory 1024 --app nutriprofile-api
flyctl scale count 2 --app nutriprofile-api
```

### Database Operations
```bash
# Connect to database
flyctl postgres connect --app nutriprofile-db

# Proxy for local connection
flyctl proxy 5432 --app nutriprofile-db

# Run migrations
flyctl ssh console --app nutriprofile-api
cd /app
alembic upgrade head
```

## Frontend Deployment (Cloudflare Pages)

### Setup
Frontend auto-deploys from GitHub on push to main branch.

### Build Configuration
```
# Cloudflare Pages settings
Build command: npm run build
Build output directory: dist
Root directory: frontend
Node version: 18
```

### Environment Variables
Set in Cloudflare Pages dashboard:
```
VITE_API_URL=https://nutriprofile-api.fly.dev
```

### Manual Deploy (if needed)
```bash
cd frontend

# Build
npm run build

# Deploy with wrangler
npx wrangler pages deploy dist --project-name=nutriprofile
```

## Health Checks

### Backend Health Endpoint
```python
# backend/app/api/v1/health.py
@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/health/detailed")
async def detailed_health(db: AsyncSession = Depends(get_db)):
    # Check database
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "version": "1.0.0"
    }
```

### Testing Health
```bash
# Check basic health
curl https://nutriprofile-api.fly.dev/health

# Check detailed health
curl https://nutriprofile-api.fly.dev/api/v1/health

# Expected response
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-01-15T10:00:00Z"
}
```

## Deployment Checklist

### Pre-Deployment
- [ ] All tests pass locally (`npm test`, `pytest`)
- [ ] No TypeScript errors (`npx tsc --noEmit`)
- [ ] Environment variables documented
- [ ] Database migrations ready
- [ ] Health check endpoint working

### Backend Deployment
```bash
# 1. Run tests
cd backend
pytest

# 2. Check migrations
alembic current
alembic upgrade head --sql  # Preview SQL

# 3. Deploy
flyctl deploy --app nutriprofile-api

# 4. Wait for deployment
timeout /t 60 /nobreak

# 5. Verify health
curl https://nutriprofile-api.fly.dev/health

# 6. Check logs for errors
flyctl logs --app nutriprofile-api --no-tail

# 7. Run migrations in production
flyctl ssh console --app nutriprofile-api
alembic upgrade head
```

### Frontend Deployment
```bash
# 1. Run tests
cd frontend
npm test

# 2. Build locally
npm run build

# 3. Push to GitHub (auto-deploys)
git add -A
git commit -m "feat: new feature"
git push

# 4. Monitor Cloudflare Pages dashboard

# 5. Test production frontend
curl https://nutriprofile.pages.dev
```

## Troubleshooting

### Backend Won't Start
```bash
# Check logs
flyctl logs --app nutriprofile-api

# Common issues:
# - Missing secrets: flyctl secrets list
# - Database connection: Check DATABASE_URL
# - Port mismatch: Ensure PORT=8000

# Restart
flyctl apps restart nutriprofile-api
```

### Database Connection Failed
```bash
# Check database status
flyctl status --app nutriprofile-db

# Check connection string
flyctl config env --app nutriprofile-api | grep DATABASE

# Test connection
flyctl postgres connect --app nutriprofile-db
```

### Migration Errors
```bash
# SSH into container
flyctl ssh console --app nutriprofile-api

# Check current state
alembic current

# Stamp to specific revision if needed
alembic stamp head

# Create fresh migration
alembic revision --autogenerate -m "fix"
```

### Out of Memory
```bash
# Check current allocation
flyctl scale show --app nutriprofile-api

# Increase memory
flyctl scale memory 1024 --app nutriprofile-api

# Or use smaller machine
flyctl scale vm shared-cpu-1x --app nutriprofile-api
```

### Slow Responses
```bash
# Check metrics
flyctl status --app nutriprofile-api

# Scale horizontally
flyctl scale count 2 --app nutriprofile-api

# Check for slow queries in logs
flyctl logs --app nutriprofile-api | grep "slow"
```

## Rollback

### Backend Rollback
```bash
# List deployments
flyctl releases --app nutriprofile-api

# Rollback to previous version
flyctl deploy --image registry.fly.io/nutriprofile-api:previous-sha

# Or restart with previous image
flyctl releases rollback --app nutriprofile-api
```

### Database Rollback
```bash
# Rollback one migration
flyctl ssh console --app nutriprofile-api
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>
```

## CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Fly
        uses: superfly/flyctl-actions/setup-flyctl@master

      - name: Deploy Backend
        run: flyctl deploy --remote-only
        working-directory: backend
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}

  # Frontend auto-deploys via Cloudflare Pages GitHub integration
```

## Production URLs

| Service | URL |
|---------|-----|
| Frontend | https://nutriprofile.pages.dev |
| Backend API | https://nutriprofile-api.fly.dev |
| API Docs | https://nutriprofile-api.fly.dev/docs |
| Health Check | https://nutriprofile-api.fly.dev/health |
