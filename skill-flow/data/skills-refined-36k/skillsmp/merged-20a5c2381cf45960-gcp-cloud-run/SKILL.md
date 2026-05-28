---
name: gcp-cloud-run
description: Use this skill when building production-ready serverless applications on GCP, covering Cloud Run services, Cloud Run Functions, cold start optimization, and event-driven architecture with Pub/Sub.
---

# GCP Cloud Run

## Patterns

### Cloud Run Service Pattern

Containerized web service on Cloud Run

**When to use**: Web applications and APIs, need any runtime or library, complex services with multiple endpoints, stateless containerized workloads.

```dockerfile
# Dockerfile - Multi-stage build for smaller image
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-slim
WORKDIR /app

# Copy only production dependencies
COPY --from=builder /app/node_modules ./node_modules
COPY src ./src
COPY package.json ./

# Cloud Run uses PORT env variable
ENV PORT=8080
EXPOSE 8080

# Run as non-root user
USER node

CMD ["node", "src/index.js"]
```

```javascript
// src/index.js
const express = require('express');
const app = express();

app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

// API routes
app.get('/api/items/:id', async (req, res) => {
  try {
    const item = await getItem(req.params.id);
    res.json(item);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});

const PORT = process.env.PORT || 8080;
const server = app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
```

```yaml
# cloudbuild.yaml
steps:
  # Build the container image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA', '.']

  # Push the container image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA']

  # Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'my-service'
      - '--image=gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA'
      - '--region=us-central1'
      - '--platform=managed'
      - '--allow-unauthenticated'
      - '--memory=512Mi'
      - '--cpu=1'
      - '--min-instances=1'
      - '--max-instances=100'
```

### Cloud Run Functions Pattern

Event-driven functions (formerly Cloud Functions)

**When to use**: Simple event handlers, Pub/Sub message processing, Cloud Storage triggers, HTTP webhooks.

```javascript
// HTTP Function
const functions = require('@google-cloud/functions-framework');

functions.http('helloHttp', (req, res) => {
  const name = req.query.name || req.body.name || 'World';
  res.send(`Hello, ${name}!`);
});
```

```javascript
// Pub/Sub Function
const functions = require('@google-cloud/functions-framework');

functions.cloudEvent('processPubSub', (cloudEvent) => {
  const message = cloudEvent.data.message;
  const data = message.data
    ? JSON.parse(Buffer.from(message.data, 'base64').toString())
    : {};

  console.log('Received message:', data);
  processMessage(data);
});
```

```javascript
// Cloud Storage Function
const functions = require('@google-cloud/functions-framework');

functions.cloudEvent('processStorageEvent', async (cloudEvent) => {
  const file = cloudEvent.data;

  console.log(`Event: ${cloudEvent.type}`);
  console.log(`Bucket: ${file.bucket}`);
  console.log(`File: ${file.name}`);

  if (cloudEvent.type === 'google.cloud.storage.object.v1.finalized') {
    await processUploadedFile(file.bucket, file.name);
  }
});
```

```bash
# Deploy HTTP function
gcloud functions deploy hello-http \
  --gen2 \
  --runtime nodejs20 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1

# Deploy Pub/Sub function
gcloud functions deploy process-messages \
  --gen2 \
  --runtime nodejs20 \
  --trigger-topic my-topic \
  --region us-central1

# Deploy Cloud Storage function
gcloud functions deploy process-uploads \
  --gen2 \
  --runtime nodejs20 \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=my-bucket" \
  --region us-central1
```

### Cold Start Optimization Pattern

Minimize cold start latency for Cloud Run

**When to use**: Latency-sensitive applications, user-facing APIs, high-traffic services.

1. **Enable Startup CPU Boost**
   ```bash
   gcloud run deploy my-service \
     --cpu-boost \
     --region us-central1
   ```

2. **Set Minimum Instances**
   ```bash
   gcloud run deploy my-service \
     --min-instances 1 \
     --region us-central1
   ```

3. **Optimize Container Image**
   ```dockerfile
   # Use distroless for minimal image
   FROM node:20-slim AS builder
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci --only=production

   FROM gcr.io/distroless/nodejs20-debian12
   WORKDIR /app
   COPY --from=builder /app/node_modules ./node_modules
   COPY src ./src
   CMD ["src/index.js"]
   ```

4. **Lazy Initialize Heavy Dependencies**
   ```javascript
   let bigQueryClient = null;

   function getBigQueryClient() {
     if (!bigQueryClient) {
       const { BigQuery } = require('@google-cloud/bigquery');
       bigQueryClient = new BigQuery();
     }
     return bigQueryClient;
   }

   app.get('/api/analytics', async (req, res) => {
     const client = getBigQueryClient();
     const results = await client.query({...});
     res.json(results);
   });
   ```

5. **Increase Memory (More CPU)**
   ```bash
   gcloud run deploy my-service \
     --memory 1Gi \
     --cpu 2 \
     --region us-central1
   ```

## Anti-Patterns

- **❌ CPU-Intensive Work Without Concurrency=1**: CPU is shared across concurrent requests, causing timeouts.
- **❌ Writing Large Files to /tmp**: Large files consume memory allocation and can cause OOM errors.
- **❌ Long-Running Background Tasks**: Background tasks will be extremely slow or stall.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| High | Calculate memory including /tmp usage |
| High | Set appropriate concurrency |
| High | Enable CPU always allocated |
| Medium | Configure connection pool with keep-alive |
| High | Enable startup CPU boost |
| Medium | Explicitly set execution environment |
| Medium | Set consistent timeouts |