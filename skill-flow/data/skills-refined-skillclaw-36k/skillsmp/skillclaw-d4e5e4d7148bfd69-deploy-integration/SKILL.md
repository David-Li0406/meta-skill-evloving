---
name: deploy-integration
description: Use this skill when deploying applications powered by various integrations (e.g., Instantly, Replit, Vast.ai, Windsurf, CodeRabbit) to production on platforms like Vercel, Fly.io, and Google Cloud Run, while managing platform-specific secrets.
---

# Skill body

## Overview
Deploy applications powered by various integrations to popular platforms with proper secrets management.

## Prerequisites
- API keys for the respective integration in the production environment
- Platform CLI installed (vercel, fly, or gcloud)
- Application code ready for deployment
- Environment variables documented

## Vercel Deployment

### Environment Setup
```bash
# Add integration secrets to Vercel
vercel secrets add <integration>_api_key sk_live_***
vercel secrets add <integration>_webhook_secret whsec_***

# Link to project
vercel link

# Deploy preview
vercel

# Deploy production
vercel --prod
```

### vercel.json Configuration
```json
{
  "env": {
    "<INTEGRATION>_API_KEY": "@<integration>_api_key"
  },
  "functions": {
    "api/**/*.ts": {
      "maxDuration": 30
    }
  }
}
```

## Fly.io Deployment

### fly.toml
```toml
app = "my-<integration>-app"
primary_region = "iad"

[env]
  NODE_ENV = "production"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
```

### Secrets
```bash
# Set integration secrets
fly secrets set <INTEGRATION>_API_KEY=sk_live_***
fly secrets set <INTEGRATION>_WEBHOOK_SECRET=whsec_***

# Deploy
fly deploy
```

## Google Cloud Run

### Dockerfile
```dockerfile
FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["npm", "start"]
```

### Deploy Script
```bash
#!/bin/bash
# deploy-cloud-run.sh

PROJECT_ID="${GOOGLE_CLOUD_PROJECT}"
SERVICE_NAME="<integration>-service"
REGION="us-central1"

# Build and push image
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --set-secrets=<INTEGRATION>_API_KEY=<integration>-api-key:latest
```

## Environment Configuration Pattern

```typescript
// config/<integration>.ts
interface <Integration>Config {
  apiKey: string;
  environment: 'development' | 'production';
}
```