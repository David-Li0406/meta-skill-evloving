---
name: deployment
description: Render deployment instructions for LogiAccounting Pro. Use when deploying to production or configuring hosting.
tools:
  - read
  - write
  - bash
metadata:
  version: "1.0"
  category: devops
  platform: render
---

# Deployment Skill

This skill provides guidance for deploying LogiAccounting Pro to Render.

## Prerequisites

- GitHub repository with the project
- Render account (free tier works)
- Environment variables configured

## Quick Deploy

### Option 1: Blueprint (Recommended)

The project includes `render.yaml` for automatic configuration:

```bash
# Just push to GitHub and connect to Render
git push origin main
```

Then in Render:
1. New → Blueprint
2. Connect GitHub repo
3. Select `render.yaml`
4. Deploy

### Option 2: Manual Setup

1. **Create Web Service**
   - Environment: Python 3
   - Build Command: `cd frontend && npm install && npm run build && cd ../backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables**
   ```
   SECRET_KEY=<generate-random-string>
   PYTHON_VERSION=3.11.0
   NODE_VERSION=20
   ```

## render.yaml Reference

```yaml
services:
  - type: web
    name: logiaccounting-pro
    runtime: python
    region: oregon
    plan: free
    buildCommand: |
      cd frontend && npm install && npm run build &&
      cd ../backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: NODE_VERSION
        value: 20
    healthCheckPath: /health
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | JWT signing key (auto-generated) |
| `PYTHON_VERSION` | Yes | Python runtime version |
| `NODE_VERSION` | Yes | Node.js for frontend build |
| `DATABASE_URL` | No | PostgreSQL connection (future) |

## Health Check

The API exposes `/health` endpoint:

```bash
curl https://your-app.onrender.com/health
# {"status": "healthy"}
```

## Troubleshooting

### Build Fails

```bash
# Check Node.js version
node --version  # Should be 20+

# Check Python version
python --version  # Should be 3.11+

# Manual build test
cd frontend && npm run build
cd backend && pip install -r requirements.txt
```

### 502 Bad Gateway

- Check start command is correct
- Verify PORT environment variable
- Check Render logs for errors

### Static Files Not Loading

Ensure FastAPI serves the frontend build:

```python
# backend/app/main.py
app.mount("/", StaticFiles(directory="../frontend/dist", html=True))
```

## Post-Deployment

1. Test all demo credentials work
2. Verify API endpoints respond
3. Check CORS allows your domain
4. Monitor for errors in Render dashboard
