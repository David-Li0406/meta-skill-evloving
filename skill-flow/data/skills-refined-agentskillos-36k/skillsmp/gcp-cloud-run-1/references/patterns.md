# GCP Cloud Run

## Patterns


---
  #### **Name**
Cloud Run Service Pattern
  #### **Description**
Containerized web service on Cloud Run
  #### **When To Use**
    - Web applications and APIs
    - Need any runtime or library
    - Complex services with multiple endpoints
    - Stateless containerized workloads
  #### **Structure**
    project/
    ├── Dockerfile
    ├── .dockerignore
    ├── src/
    │   ├── index.js
    │   └── routes/
    ├── package.json
    └── cloudbuild.yaml
    
  #### **Implementation**
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
          - '--concurrency=80'
          - '--cpu-boost'
    
    images:
      - 'gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA'
    ```
    
  #### **Gcloud Deploy**
    # Direct gcloud deployment
    gcloud run deploy my-service \
      --source . \
      --region us-central1 \
      --allow-unauthenticated \
      --memory 512Mi \
      --cpu 1 \
      --min-instances 1 \
      --max-instances 100 \
      --concurrency 80 \
      --cpu-boost
    

---
  #### **Name**
Cloud Run Functions Pattern
  #### **Description**
Event-driven functions (formerly Cloud Functions)
  #### **When To Use**
    - Simple event handlers
    - Pub/Sub message processing
    - Cloud Storage triggers
    - HTTP webhooks
  #### **Implementation**
    ```javascript
    // HTTP Function
    // index.js
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
      // Decode Pub/Sub message
      const message = cloudEvent.data.message;
      const data = message.data
        ? JSON.parse(Buffer.from(message.data, 'base64').toString())
        : {};
    
      console.log('Received message:', data);
    
      // Process message
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
    

---
  #### **Name**
Cold Start Optimization Pattern
  #### **Description**
Minimize cold start latency for Cloud Run
  #### **When To Use**
    - Latency-sensitive applications
    - User-facing APIs
    - High-traffic services
  #### **Implementation**
    ## 1. Enable Startup CPU Boost
    
    ```bash
    gcloud run deploy my-service \
      --cpu-boost \
      --region us-central1
    ```
    
    ## 2. Set Minimum Instances
    
    ```bash
    gcloud run deploy my-service \
      --min-instances 1 \
      --region us-central1
    ```
    
    ## 3. Optimize Container Image
    
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
    
    ## 4. Lazy Initialize Heavy Dependencies
    
    ```javascript
    // Lazy load heavy libraries
    let bigQueryClient = null;
    
    function getBigQueryClient() {
      if (!bigQueryClient) {
        const { BigQuery } = require('@google-cloud/bigquery');
        bigQueryClient = new BigQuery();
      }
      return bigQueryClient;
    }
    
    // Only initialize when needed
    app.get('/api/analytics', async (req, res) => {
      const client = getBigQueryClient();
      const results = await client.query({...});
      res.json(results);
    });
    ```
    
    ## 5. Increase Memory (More CPU)
    
    ```bash
    # Higher memory = more CPU during startup
    gcloud run deploy my-service \
      --memory 1Gi \
      --cpu 2 \
      --region us-central1
    ```
    
  #### **Optimization Impact**
    ##### **Startup Cpu Boost**
50% faster cold starts
    ##### **Min Instances**
Eliminates cold starts for traffic spikes
    ##### **Distroless Image**
Smaller attack surface, faster pull
    ##### **Lazy Init**
Defers heavy loading to first request

---
  #### **Name**
Concurrency Configuration Pattern
  #### **Description**
Proper concurrency settings for Cloud Run
  #### **When To Use**
    - Need to optimize instance utilization
    - Handle traffic spikes efficiently
    - Reduce cold starts
  #### **Implementation**
    ## Understanding Concurrency
    
    ```bash
    # Default concurrency is 80
    # Adjust based on your workload
    
    # For I/O-bound workloads (most web apps)
    gcloud run deploy my-service \
      --concurrency 80 \
      --cpu 1
    
    # For CPU-bound workloads
    gcloud run deploy my-service \
      --concurrency 1 \
      --cpu 1
    
    # For memory-intensive workloads
    gcloud run deploy my-service \
      --concurrency 10 \
      --memory 2Gi
    ```
    
    ## Node.js Concurrency
    
    ```javascript
    // Node.js is single-threaded but handles I/O concurrently
    // Use async/await for all I/O operations
    
    // GOOD - async I/O
    app.get('/api/data', async (req, res) => {
      const [users, products] = await Promise.all([
        fetchUsers(),
        fetchProducts()
      ]);
      res.json({ users, products });
    });
    
    // BAD - blocking operation
    app.get('/api/compute', (req, res) => {
      const result = heavyCpuOperation(); // Blocks other requests!
      res.json(result);
    });
    ```
    
    ## Python Concurrency with Gunicorn
    
    ```dockerfile
    FROM python:3.11-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    
    # 4 workers for concurrency
    CMD exec gunicorn --bind :$PORT --workers 4 --threads 2 main:app
    ```
    
    ```python
    # main.py
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/api/data')
    def get_data():
        return {'status': 'ok'}
    ```
    
  #### **Concurrency Guidelines**
    ##### **Concurrency=1**
Only for CPU-bound or unsafe code
    ##### **Concurrency=8-20**
Memory-intensive workloads
    ##### **Concurrency=80**
Default, good for I/O-bound
    ##### **Concurrency=250**
Maximum, for very lightweight handlers

---
  #### **Name**
Pub/Sub Integration Pattern
  #### **Description**
Event-driven processing with Cloud Pub/Sub
  #### **When To Use**
    - Asynchronous message processing
    - Decoupled microservices
    - Event-driven architecture
  #### **Implementation**
    ## Push Subscription to Cloud Run
    
    ```bash
    # Create topic
    gcloud pubsub topics create orders
    
    # Create push subscription to Cloud Run
    gcloud pubsub subscriptions create orders-push \
      --topic orders \
      --push-endpoint https://my-service-xxx.run.app/pubsub \
      --ack-deadline 600
    ```
    
    ```javascript
    // Handle Pub/Sub push messages
    const express = require('express');
    const app = express();
    app.use(express.json());
    
    app.post('/pubsub', async (req, res) => {
      // Verify the request is from Pub/Sub
      if (!req.body.message) {
        return res.status(400).send('Invalid Pub/Sub message');
      }
    
      try {
        // Decode message data
        const message = req.body.message;
        const data = message.data
          ? JSON.parse(Buffer.from(message.data, 'base64').toString())
          : {};
    
        console.log('Processing order:', data);
    
        await processOrder(data);
    
        // Return 200 to acknowledge
        res.status(200).send('OK');
      } catch (error) {
        console.error('Processing failed:', error);
        // Return 500 to trigger retry
        res.status(500).send('Processing failed');
      }
    });
    ```
    
    ## Publishing Messages
    
    ```javascript
    const { PubSub } = require('@google-cloud/pubsub');
    const pubsub = new PubSub();
    
    async function publishOrder(order) {
      const topic = pubsub.topic('orders');
      const messageBuffer = Buffer.from(JSON.stringify(order));
    
      const messageId = await topic.publishMessage({
        data: messageBuffer,
        attributes: {
          type: 'order_created',
          priority: 'high'
        }
      });
    
      console.log(`Published message ${messageId}`);
      return messageId;
    }
    ```
    
    ## Dead Letter Queue
    
    ```bash
    # Create DLQ topic
    gcloud pubsub topics create orders-dlq
    
    # Update subscription with DLQ
    gcloud pubsub subscriptions update orders-push \
      --dead-letter-topic orders-dlq \
      --max-delivery-attempts 5
    ```
    

---
  #### **Name**
Cloud SQL Connection Pattern
  #### **Description**
Connect Cloud Run to Cloud SQL securely
  #### **When To Use**
    - Need relational database
    - Migrating existing applications
    - Complex queries and transactions
  #### **Implementation**
    ```bash
    # Deploy with Cloud SQL connection
    gcloud run deploy my-service \
      --add-cloudsql-instances PROJECT:REGION:INSTANCE \
      --set-env-vars INSTANCE_CONNECTION_NAME="PROJECT:REGION:INSTANCE" \
      --set-env-vars DB_NAME="mydb" \
      --set-env-vars DB_USER="myuser"
    ```
    
    ```javascript
    // Using Unix socket connection
    const { Pool } = require('pg');
    
    const pool = new Pool({
      user: process.env.DB_USER,
      password: process.env.DB_PASS,
      database: process.env.DB_NAME,
      // Cloud SQL connector uses Unix socket
      host: `/cloudsql/${process.env.INSTANCE_CONNECTION_NAME}`,
      max: 5,  // Connection pool size
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 10000,
    });
    
    app.get('/api/users', async (req, res) => {
      const client = await pool.connect();
      try {
        const result = await client.query('SELECT * FROM users LIMIT 100');
        res.json(result.rows);
      } finally {
        client.release();
      }
    });
    ```
    
    ```python
    # Python with SQLAlchemy
    import os
    from sqlalchemy import create_engine
    
    def get_engine():
        instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
        db_user = os.environ["DB_USER"]
        db_pass = os.environ["DB_PASS"]
        db_name = os.environ["DB_NAME"]
    
        engine = create_engine(
            f"postgresql+pg8000://{db_user}:{db_pass}@/{db_name}",
            connect_args={
                "unix_sock": f"/cloudsql/{instance_connection_name}/.s.PGSQL.5432"
            },
            pool_size=5,
            max_overflow=2,
            pool_timeout=30,
            pool_recycle=1800,
        )
        return engine
    ```
    
  #### **Best Practices**
    - Use connection pooling (max 5-10 per instance)
    - Set appropriate idle timeouts
    - Handle connection errors gracefully
    - Consider Cloud SQL Proxy for local development

---
  #### **Name**
Secret Manager Integration
  #### **Description**
Securely manage secrets in Cloud Run
  #### **When To Use**
    - API keys, database passwords
    - Service account keys
    - Any sensitive configuration
  #### **Implementation**
    ```bash
    # Create secret
    echo -n "my-secret-value" | gcloud secrets create my-secret --data-file=-
    
    # Mount as environment variable
    gcloud run deploy my-service \
      --update-secrets=API_KEY=my-secret:latest
    
    # Mount as file volume
    gcloud run deploy my-service \
      --update-secrets=/secrets/api-key=my-secret:latest
    ```
    
    ```javascript
    // Access mounted as environment variable
    const apiKey = process.env.API_KEY;
    
    // Access mounted as file
    const fs = require('fs');
    const apiKey = fs.readFileSync('/secrets/api-key', 'utf8');
    
    // Access via Secret Manager API (when not mounted)
    const { SecretManagerServiceClient } = require('@google-cloud/secret-manager');
    const client = new SecretManagerServiceClient();
    
    async function getSecret(name) {
      const [version] = await client.accessSecretVersion({
        name: `projects/${projectId}/secrets/${name}/versions/latest`
      });
      return version.payload.data.toString();
    }
    ```
    

## Anti-Patterns


---
  #### **Name**
CPU-Intensive Work Without Concurrency=1
  #### **Description**
Running CPU-bound code with high concurrency
  #### **Why Bad**
    CPU is shared across concurrent requests. CPU-bound work
    will starve other requests, causing timeouts.
    
  #### **Bad Example**
    // High concurrency (default 80) with CPU-bound work
    app.get('/api/process', (req, res) => {
      const result = heavyCpuOperation();  // Blocks CPU
      res.json(result);
    });
    
  #### **Good Example**
    # Set concurrency=1 for CPU-bound workloads
    gcloud run deploy my-service --concurrency 1 --cpu 2
    
    # Or move CPU work to Cloud Tasks/separate service
    

---
  #### **Name**
Writing Large Files to /tmp
  #### **Description**
Using /tmp without considering memory limits
  #### **Why Bad**
    /tmp is an in-memory filesystem. Large files consume
    your memory allocation and can cause OOM errors.
    
  #### **Bad Example**
    // Writing large files to /tmp
    const largePdf = generateLargePdf();  // 500MB
    fs.writeFileSync('/tmp/report.pdf', largePdf);
    // Uses 500MB of your memory allocation!
    
  #### **Good Example**
    // Stream directly to Cloud Storage
    const { Storage } = require('@google-cloud/storage');
    const storage = new Storage();
    
    const file = storage.bucket('my-bucket').file('report.pdf');
    const writeStream = file.createWriteStream();
    generatePdfStream().pipe(writeStream);
    

---
  #### **Name**
Long-Running Background Tasks
  #### **Description**
CPU is throttled between requests
  #### **Why Bad**
    Cloud Run throttles CPU to near-zero when not handling
    requests. Background tasks will be extremely slow or stall.
    
  #### **Good Example**
    // Use Cloud Tasks for background work
    const { CloudTasksClient } = require('@google-cloud/tasks');
    const client = new CloudTasksClient();
    
    app.post('/api/order', async (req, res) => {
      // Respond immediately
      res.json({ status: 'processing' });
    
      // Queue background task
      await client.createTask({
        parent: queuePath,
        task: {
          httpRequest: {
            url: 'https://my-service/process-order',
            body: Buffer.from(JSON.stringify(req.body)).toString('base64')
          }
        }
      });
    });
    