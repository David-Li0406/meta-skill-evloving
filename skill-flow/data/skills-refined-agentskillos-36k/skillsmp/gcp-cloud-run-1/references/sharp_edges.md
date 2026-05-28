# Gcp Cloud Run - Sharp Edges

## /tmp Filesystem Counts Against Memory

### **Id**
tmp-memory-consumption
### **Severity**
high
### **Situation**
Writing files to /tmp directory in Cloud Run
### **Symptom**
  Container killed with OOM error.
  Memory usage spikes unexpectedly.
  File operations cause container restarts.
  "Container memory limit exceeded" in logs.
  
### **Why**
  Cloud Run uses an in-memory filesystem for /tmp. Any files written
  to /tmp consume memory from your container's allocation.
  
  Common scenarios:
  - Downloading files temporarily
  - Creating temp processing files
  - Libraries caching to /tmp
  - Large log buffers
  
  A 512MB container that downloads a 200MB file to /tmp only has
  ~300MB left for the application.
  
### **Solution**
  ## Calculate memory including /tmp usage
  
  ```yaml
  # cloudbuild.yaml
  steps:
    - name: 'gcr.io/cloud-builders/gcloud'
      args:
        - 'run'
        - 'deploy'
        - 'my-service'
        - '--memory=1Gi'  # Include /tmp overhead
        - '--image=gcr.io/$PROJECT_ID/my-service'
  ```
  
  ## Stream instead of buffering
  
  ```python
  # BAD - buffers entire file in /tmp
  def process_large_file(bucket_name, blob_name):
      blob = bucket.blob(blob_name)
      blob.download_to_filename('/tmp/large_file')
      with open('/tmp/large_file', 'rb') as f:
          process(f.read())
  
  # GOOD - stream processing
  def process_large_file(bucket_name, blob_name):
      blob = bucket.blob(blob_name)
      with blob.open('rb') as f:
          for chunk in iter(lambda: f.read(8192), b''):
              process_chunk(chunk)
  ```
  
  ## Use Cloud Storage for large files
  
  ```python
  from google.cloud import storage
  
  def process_with_gcs(bucket_name, input_blob, output_blob):
      client = storage.Client()
      bucket = client.bucket(bucket_name)
  
      # Process directly to/from GCS
      input_blob = bucket.blob(input_blob)
      output_blob = bucket.blob(output_blob)
  
      with input_blob.open('rb') as reader:
          with output_blob.open('wb') as writer:
              for chunk in iter(lambda: reader.read(65536), b''):
                  processed = transform(chunk)
                  writer.write(processed)
  ```
  
  ## Monitor memory usage
  
  ```python
  import psutil
  import logging
  
  def log_memory():
      memory = psutil.virtual_memory()
      logging.info(f"Memory: {memory.percent}% used, "
                  f"{memory.available / 1024 / 1024:.0f}MB available")
  ```
  
### **Detection Pattern**
  - /tmp
  - memory
  - OOM
  - out of memory

## Concurrency=1 Causes Scaling Bottlenecks

### **Id**
concurrency-one-scaling
### **Severity**
high
### **Situation**
Setting concurrency to 1 for request isolation
### **Symptom**
  Auto-scaling creates many container instances.
  High latency during traffic spikes.
  Increased cold starts.
  Higher costs from more instances.
  
### **Why**
  Setting concurrency to 1 means each container handles only one
  request at a time. During traffic spikes:
  
  - 100 concurrent requests = 100 container instances
  - Each instance has cold start overhead
  - More instances = higher costs
  - Scaling takes time, requests queue up
  
  This should only be used when:
  - Processing is truly single-threaded
  - Memory-heavy per-request processing
  - Using thread-unsafe libraries
  
### **Solution**
  ## Set appropriate concurrency
  
  ```bash
  # For I/O-bound workloads (most web apps)
  gcloud run deploy my-service \
    --concurrency=80 \
    --max-instances=100
  
  # For CPU-bound workloads
  gcloud run deploy my-service \
    --concurrency=4 \
    --cpu=2
  
  # Only use 1 when absolutely necessary
  gcloud run deploy my-service \
    --concurrency=1 \
    --max-instances=1000  # Be prepared for many instances
  ```
  
  ## Node.js - use async properly
  
  ```javascript
  // With high concurrency, ensure async operations
  const express = require('express');
  const app = express();
  
  app.get('/api/data', async (req, res) => {
    // All I/O should be async
    const data = await fetchFromDatabase();
    const enriched = await enrichData(data);
    res.json(enriched);
  });
  
  // Concurrency 80+ is safe for async I/O workloads
  ```
  
  ## Python - use async framework
  
  ```python
  from fastapi import FastAPI
  import asyncio
  import httpx
  
  app = FastAPI()
  
  @app.get("/api/data")
  async def get_data():
      # Async I/O allows high concurrency
      async with httpx.AsyncClient() as client:
          response = await client.get("https://api.example.com/data")
          return response.json()
  
  # Concurrency 80+ safe with async framework
  ```
  
  ## Calculate concurrency
  
  ```
  concurrency = memory_limit / per_request_memory
  
  Example:
  - 512MB container
  - 20MB per request overhead
  - Safe concurrency: ~25
  ```
  
### **Detection Pattern**
  - concurrency
  - --concurrency=1
  - scaling
  - max-instances

## CPU Throttled When Not Handling Requests

### **Id**
cpu-throttled-outside-requests
### **Severity**
high
### **Situation**
Running background tasks or processing between requests
### **Symptom**
  Background tasks run extremely slowly.
  Scheduled work doesn't complete.
  Metrics collection fails.
  Connection keep-alive breaks.
  
### **Why**
  By default, Cloud Run throttles CPU to near-zero when not actively
  handling a request. This is "CPU only during requests" mode.
  
  Affected operations:
  - Background threads
  - Connection pool maintenance
  - Metrics/telemetry emission
  - Scheduled tasks within container
  - Cleanup operations after response
  
### **Solution**
  ## Enable CPU always allocated
  
  ```bash
  # CPU allocated even outside requests
  gcloud run deploy my-service \
    --cpu-throttling=false \
    --min-instances=1
  
  # Note: This increases costs but enables background work
  ```
  
  ## Use startup CPU boost for initialization
  
  ```bash
  # Boost CPU during cold start only
  gcloud run deploy my-service \
    --cpu-boost \
    --cpu-throttling=true  # Default, throttle after request
  ```
  
  ## Move background work to Cloud Tasks
  
  ```python
  from google.cloud import tasks_v2
  import json
  
  def create_background_task(payload):
      client = tasks_v2.CloudTasksClient()
      parent = client.queue_path(
          "my-project", "us-central1", "my-queue"
      )
  
      task = {
          "http_request": {
              "http_method": tasks_v2.HttpMethod.POST,
              "url": "https://my-service.run.app/process",
              "body": json.dumps(payload).encode(),
              "headers": {"Content-Type": "application/json"}
          }
      }
  
      client.create_task(parent=parent, task=task)
  
  # Handle response immediately, background via Cloud Tasks
  @app.post("/api/order")
  async def create_order(order: Order):
      order_id = await save_order(order)
  
      # Queue background processing
      create_background_task({"order_id": order_id})
  
      return {"order_id": order_id, "status": "processing"}
  ```
  
  ## Use Pub/Sub for async processing
  
  ```yaml
  # Move heavy processing to separate service
  steps:
    # Main service - responds quickly
    - name: 'gcr.io/cloud-builders/gcloud'
      args: ['run', 'deploy', 'api-service',
             '--cpu-throttling=true']
  
    # Worker service - processes messages
    - name: 'gcr.io/cloud-builders/gcloud'
      args: ['run', 'deploy', 'worker-service',
             '--cpu-throttling=false',
             '--min-instances=1']
  ```
  
### **Detection Pattern**
  - cpu-throttling
  - background
  - async
  - slow

## VPC Connector 10-Minute Idle Timeout

### **Id**
vpc-idle-timeout
### **Severity**
medium
### **Situation**
Cloud Run service connecting to VPC resources
### **Symptom**
  Connection errors after period of inactivity.
  "Connection reset" or "Connection refused" errors.
  Sporadic failures to VPC resources.
  Database connections drop unexpectedly.
  
### **Why**
  Cloud Run's VPC connector has a 10-minute idle timeout on connections.
  If a connection is idle for 10 minutes, it's silently closed.
  
  Affects:
  - Database connection pools
  - Redis connections
  - Internal API connections
  - Any persistent VPC connection
  
### **Solution**
  ## Configure connection pool with keep-alive
  
  ```python
  # SQLAlchemy with connection recycling
  from sqlalchemy import create_engine
  
  engine = create_engine(
      DATABASE_URL,
      pool_size=5,
      max_overflow=2,
      pool_recycle=300,  # Recycle connections every 5 minutes
      pool_pre_ping=True  # Validate connection before use
  )
  ```
  
  ## TCP keep-alive for custom connections
  
  ```python
  import socket
  
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
  sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
  sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 60)
  sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
  ```
  
  ## Redis with connection validation
  
  ```python
  import redis
  
  pool = redis.ConnectionPool(
      host=REDIS_HOST,
      port=6379,
      socket_keepalive=True,
      socket_keepalive_options={
          socket.TCP_KEEPIDLE: 60,
          socket.TCP_KEEPINTVL: 60,
          socket.TCP_KEEPCNT: 5
      },
      health_check_interval=30
  )
  client = redis.Redis(connection_pool=pool)
  ```
  
  ## Use Cloud SQL Proxy sidecar
  
  ```yaml
  # Use Cloud SQL connector which handles reconnection
  # requirements.txt
  cloud-sql-python-connector[pg8000]
  ```
  
  ```python
  from google.cloud.sql.connector import Connector
  import sqlalchemy
  
  connector = Connector()
  
  def getconn():
      return connector.connect(
          "project:region:instance",
          "pg8000",
          user="user",
          password="password",
          db="database"
      )
  
  engine = sqlalchemy.create_engine(
      "postgresql+pg8000://",
      creator=getconn
  )
  ```
  
### **Detection Pattern**
  - VPC
  - connection
  - timeout
  - idle
  - reset

## Container Startup Timeout (4 minutes max)

### **Id**
container-startup-timeout
### **Severity**
high
### **Situation**
Deploying containers with slow initialization
### **Symptom**
  Deployment fails with "Container failed to start".
  Service never becomes healthy.
  "Revision failed to become ready" errors.
  Works locally but fails on Cloud Run.
  
### **Why**
  Cloud Run expects your container to start listening on PORT within
  4 minutes (240 seconds). If it doesn't, the instance is killed.
  
  Common causes:
  - Heavy framework initialization (ML models, etc.)
  - Waiting for external dependencies at startup
  - Large dependency loading
  - Database migrations on startup
  
### **Solution**
  ## Enable startup CPU boost
  
  ```bash
  gcloud run deploy my-service \
    --cpu-boost \
    --startup-cpu-boost
  ```
  
  ## Lazy initialization
  
  ```python
  from functools import lru_cache
  from fastapi import FastAPI
  
  app = FastAPI()
  
  # Don't load at import time
  model = None
  
  @lru_cache()
  def get_model():
      global model
      if model is None:
          # Load on first request, not at startup
          model = load_heavy_model()
      return model
  
  @app.get("/predict")
  async def predict(data: dict):
      model = get_model()  # Loads on first call only
      return model.predict(data)
  
  # Startup is fast - model loads on first request
  ```
  
  ## Start listening immediately
  
  ```python
  import asyncio
  from fastapi import FastAPI
  import uvicorn
  
  app = FastAPI()
  
  # Global state for async initialization
  initialized = asyncio.Event()
  
  @app.on_event("startup")
  async def startup():
      # Start background initialization
      asyncio.create_task(async_init())
  
  async def async_init():
      # Heavy initialization happens after server starts
      await load_models()
      await warm_up_connections()
      initialized.set()
  
  @app.get("/ready")
  async def ready():
      if not initialized.is_set():
          raise HTTPException(503, "Still initializing")
      return {"status": "ready"}
  
  @app.get("/health")
  async def health():
      # Always respond - health check passes
      return {"status": "healthy"}
  ```
  
  ## Use multi-stage builds
  
  ```dockerfile
  # Build stage - slow
  FROM python:3.11 as builder
  WORKDIR /app
  COPY requirements.txt .
  RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt
  
  # Runtime stage - fast startup
  FROM python:3.11-slim
  WORKDIR /app
  COPY --from=builder /wheels /wheels
  RUN pip install --no-cache /wheels/* && rm -rf /wheels
  COPY . .
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
  ```
  
  ## Run migrations separately
  
  ```bash
  # Don't migrate on startup - use Cloud Build
  steps:
    # Run migrations first
    - name: 'gcr.io/cloud-builders/gcloud'
      entrypoint: 'bash'
      args:
        - '-c'
        - |
          gcloud run jobs execute migrate-job --wait
  
    # Then deploy
    - name: 'gcr.io/cloud-builders/gcloud'
      args: ['run', 'deploy', 'my-service', ...]
  ```
  
### **Detection Pattern**
  - startup
  - failed to start
  - Container failed
  - timeout

## Second Generation Execution Environment Differences

### **Id**
second-gen-execution-environment
### **Severity**
medium
### **Situation**
Migrating to or using Cloud Run second-gen execution environment
### **Symptom**
  Network behavior changes.
  Different syscall support.
  File system behavior differences.
  Container behaves differently than in first-gen.
  
### **Why**
  Cloud Run's second-generation execution environment uses a different
  sandbox (gVisor) with different characteristics:
  
  - More Linux syscalls supported
  - Full /proc and /sys access
  - Different network stack
  - No automatic HTTPS redirect
  - Different tmp filesystem behavior
  
### **Solution**
  ## Explicitly set execution environment
  
  ```bash
  # First generation (legacy)
  gcloud run deploy my-service \
    --execution-environment=gen1
  
  # Second generation (recommended for most)
  gcloud run deploy my-service \
    --execution-environment=gen2
  ```
  
  ## Handle network differences
  
  ```python
  # Second-gen doesn't auto-redirect HTTP to HTTPS
  from fastapi import FastAPI, Request
  from fastapi.responses import RedirectResponse
  
  app = FastAPI()
  
  @app.middleware("http")
  async def redirect_https(request: Request, call_next):
      # Check X-Forwarded-Proto header
      if request.headers.get("X-Forwarded-Proto") == "http":
          url = request.url.replace(scheme="https")
          return RedirectResponse(url, status_code=301)
      return await call_next(request)
  ```
  
  ## GPU access (second-gen only)
  
  ```bash
  # GPUs only available in second-gen
  gcloud run deploy ml-service \
    --execution-environment=gen2 \
    --gpu=1 \
    --gpu-type=nvidia-l4
  ```
  
  ## Check execution environment
  
  ```python
  import os
  
  def get_execution_environment():
      # Second-gen has different /proc structure
      try:
          with open('/proc/version', 'r') as f:
              version = f.read()
              if 'gVisor' in version:
                  return 'gen2'
      except:
          pass
      return 'gen1'
  ```
  
### **Detection Pattern**
  - gen1
  - gen2
  - execution-environment
  - gVisor

## Request Timeout Configuration Mismatch

### **Id**
request-timeout-mismatch
### **Severity**
medium
### **Situation**
Long-running requests or background processing
### **Symptom**
  Requests terminated before completion.
  504 Gateway Timeout errors.
  Processing stops unexpectedly.
  Inconsistent timeout behavior.
  
### **Why**
  Cloud Run has multiple timeout configurations that must align:
  - Request timeout (default 300s, max 3600s for HTTP, 60m for gRPC)
  - Client timeout
  - Downstream service timeouts
  - Load balancer timeout (for external access)
  
### **Solution**
  ## Set consistent timeouts
  
  ```bash
  # Increase request timeout (max 3600s for HTTP)
  gcloud run deploy my-service \
    --timeout=900  # 15 minutes
  ```
  
  ## Handle long-running with webhooks
  
  ```python
  from fastapi import FastAPI, BackgroundTasks
  import httpx
  
  app = FastAPI()
  
  @app.post("/process")
  async def process(data: dict, background_tasks: BackgroundTasks):
      task_id = create_task_id()
  
      # Start background processing
      background_tasks.add_task(
          long_running_process,
          task_id,
          data,
          data.get("callback_url")
      )
  
      # Return immediately
      return {"task_id": task_id, "status": "processing"}
  
  async def long_running_process(task_id, data, callback_url):
      result = await heavy_computation(data)
  
      # Callback when done
      if callback_url:
          async with httpx.AsyncClient() as client:
              await client.post(callback_url, json={
                  "task_id": task_id,
                  "result": result
              })
  ```
  
  ## Use Cloud Tasks for reliable long-running
  
  ```python
  from google.cloud import tasks_v2
  
  def create_long_running_task(data):
      client = tasks_v2.CloudTasksClient()
      parent = client.queue_path(PROJECT, REGION, "long-tasks")
  
      task = {
          "http_request": {
              "http_method": tasks_v2.HttpMethod.POST,
              "url": "https://worker.run.app/process",
              "body": json.dumps(data).encode(),
              "headers": {"Content-Type": "application/json"}
          },
          "dispatch_deadline": {"seconds": 1800}  # 30 min
      }
  
      return client.create_task(parent=parent, task=task)
  ```
  
  ## Streaming for long responses
  
  ```python
  from fastapi import FastAPI
  from fastapi.responses import StreamingResponse
  
  @app.get("/large-report")
  async def large_report():
      async def generate():
          for chunk in process_large_data():
              yield chunk
  
      return StreamingResponse(generate(), media_type="text/plain")
  ```
  
### **Detection Pattern**
  - timeout
  - 504
  - Gateway Timeout
  - request timeout