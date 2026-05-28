---
skill: nexus-production-deployment
description: Production deployment patterns, Docker, Kubernetes, scaling, and best practices
priority: MEDIUM
tags: [nexus, production, deployment, docker, kubernetes, scaling]
---

# Nexus Production Deployment

Deploy Nexus to production with Docker and Kubernetes.

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose ports
EXPOSE 8000 3001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "app.py"]
```

### requirements.txt

```
kailash-nexus>=1.0.0
kailash-dataflow>=0.5.0  # If using DataFlow
uvicorn[standard]>=0.24.0
gunicorn>=21.2.0
redis>=5.0.0
psycopg2-binary>=2.9.9  # If using PostgreSQL
```

### app.py

```python
import os
from nexus import Nexus

# Production configuration
app = Nexus(
    api_port=int(os.getenv("PORT", "8000")),
    mcp_port=int(os.getenv("MCP_PORT", "3001")),
    api_host="0.0.0.0",

    # Security
    enable_auth=True,
    enable_rate_limiting=True,
    rate_limit=5000,

    # Performance
    max_concurrent_workflows=200,
    enable_caching=True,

    # Monitoring
    enable_monitoring=True,
    monitoring_backend="prometheus",

    # Sessions (Redis for distributed)
    session_backend="redis",
    redis_url=os.getenv("REDIS_URL"),

    # Logging
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_format="json",

    # Discovery
    auto_discovery=False  # Manual registration
)

# Register workflows
from workflows import register_workflows
register_workflows(app)

if __name__ == "__main__":
    app.start()
```

### Build and Run

```bash
# Build image
docker build -t nexus-app:latest .

# Run container
docker run -d \
  --name nexus \
  -p 8000:8000 \
  -p 3001:3001 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e REDIS_URL="redis://redis:6379" \
  -e LOG_LEVEL="INFO" \
  nexus-app:latest

# Check logs
docker logs -f nexus

# Check health
curl http://localhost:8000/health
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  nexus:
    build: .
    ports:
      - "8000:8000"
      - "3001:3001"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/nexus
      - REDIS_URL=redis://redis:6379
      - LOG_LEVEL=INFO
    depends_on:
      - postgres
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=nexus
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

volumes:
  postgres_data:
  redis_data:
```

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f nexus

# Stop services
docker-compose down
```

## Production Security Configuration (v1.1.1+)

### Critical Security Fixes

Nexus v1.1.1 includes P0 security and reliability fixes for production environments.

### Environment Variables

Set `NEXUS_ENV=production` to enable production security features:

```bash
export NEXUS_ENV=production
```

**What this does**:
- ✅ Auto-enables authentication (unless explicitly disabled)
- ✅ Ensures rate limiting is active (100 req/min default)
- ✅ Adds security warnings if auth disabled

### Authentication in Production

**Recommended (Auto-Enable)**:
```python
import os
from nexus import Nexus

# Set environment variable
os.environ["NEXUS_ENV"] = "production"

# In production (NEXUS_ENV=production), this auto-enables auth
app = Nexus()  # enable_auth auto-set to True
```

**Explicit Override**:
```python
# Force enable in development
app = Nexus(enable_auth=True)

# Disable in production (NOT RECOMMENDED - logs critical warning)
app = Nexus(enable_auth=False)
# ⚠️  SECURITY WARNING: Authentication is DISABLED in production environment!
#    Set enable_auth=True to secure your API endpoints.
```

**Docker Environment**:
```yaml
# docker-compose.yml
services:
  nexus:
    environment:
      - NEXUS_ENV=production  # Auto-enables auth
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/nexus
      - REDIS_URL=redis://redis:6379
```

### Rate Limiting

**Default Configuration (v1.1.1+)**:
```python
app = Nexus()  # rate_limit defaults to 100 req/min
```

**Custom Rate Limits**:
```python
# Higher limit for high-traffic APIs
app = Nexus(rate_limit=1000)

# Disable (NOT RECOMMENDED - logs security warning)
app = Nexus(rate_limit=None)
# ⚠️  SECURITY WARNING: Rate limiting is DISABLED!
#    This allows unlimited requests and may lead to DoS attacks.
```

**Per-Endpoint Rate Limiting**:
```python
from nexus import Nexus

app = Nexus()

# Custom endpoint with specific rate limit
@app.endpoint("/api/search", rate_limit=50)
async def search_endpoint(q: str):
    """Search endpoint with lower rate limit."""
    return await app._execute_workflow("search", {"query": q})
```

### Input Validation (v1.1.1+)

All channels (API, MCP, CLI) now validate inputs automatically:

**Protections Enabled**:
- ✅ **Dangerous Keys Blocked**: `__import__`, `eval`, `exec`, `compile`, `globals`, `locals`, etc.
- ✅ **Input Size Limits**: 10MB default (configurable)
- ✅ **Path Traversal Prevention**: Blocks `../`, `..\\`, absolute paths
- ✅ **Key Length Limits**: 256 characters max

**Configuration**:
```python
# Default (10MB input limit)
app = Nexus()

# Custom input size limit
app._max_input_size = 20 * 1024 * 1024  # 20MB
```

**No configuration needed** - automatically applied across all channels.

### Production Deployment Example

Complete production-ready configuration:

```python
import os
from nexus import Nexus

# Production configuration with all security features
app = Nexus(
    # Environment
    # Set NEXUS_ENV=production to auto-enable auth

    # Server
    api_port=int(os.getenv("PORT", "8000")),
    api_host="0.0.0.0",

    # Security (P0 fixes)
    enable_auth=True,          # P0-1: Explicit enable (or use NEXUS_ENV=production)
    rate_limit=1000,           # P0-2: DoS protection (default 100)
    auto_discovery=False,      # P0-3: No blocking (manual registration)

    # Performance
    max_concurrent_workflows=200,
    enable_caching=True,
    request_timeout=60,

    # Monitoring
    enable_monitoring=True,
    monitoring_interval=30,

    # Sessions
    session_backend="redis",
    redis_url=os.getenv("REDIS_URL"),

    # Logging
    log_level="INFO",
    log_format="json",
    log_file="/var/log/nexus/app.log"
)

# Register workflows explicitly (no auto-discovery)
from workflows import user_workflow, order_workflow
app.register("users", user_workflow.build())
app.register("orders", order_workflow.build())

if __name__ == "__main__":
    app.start()
```

### Docker Production Deployment

**Dockerfile** (with security):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set production environment
ENV NEXUS_ENV=production

# Expose ports
EXPOSE 8000 3001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run with production settings
CMD ["python", "app.py"]
```

**docker-compose.yml** (with security):
```yaml
version: '3.8'

services:
  nexus:
    build: .
    ports:
      - "8000:8000"
      - "3001:3001"
    environment:
      # Security
      - NEXUS_ENV=production              # Auto-enable auth
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/nexus
      - REDIS_URL=redis://redis:6379

      # Logging
      - LOG_LEVEL=INFO
    depends_on:
      - postgres
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=nexus
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

volumes:
  postgres_data:
  redis_data:
```

### Security Monitoring

**Monitor security events**:
```python
# Check auth status
health = app.health_check()
print(f"Auth Enabled: {health.get('auth_enabled', False)}")

# Monitor rate limiting
print(f"Rate Limit: {app._rate_limit} req/min")

# Get security logs
# Security warnings logged at CRITICAL level
```

### Common Security Mistakes

❌ **DON'T**:
```python
# Disable auth in production
app = Nexus(enable_auth=False)  # CRITICAL WARNING

# Disable rate limiting
app = Nexus(rate_limit=None)    # SECURITY WARNING

# Enable auto-discovery in production
app = Nexus(auto_discovery=True)  # 5-10s blocking delay
```

✅ **DO**:
```python
# Use environment variable
export NEXUS_ENV=production
app = Nexus()  # Auth auto-enabled

# Or explicit enable
app = Nexus(enable_auth=True, rate_limit=1000, auto_discovery=False)
```

## Kubernetes Deployment

### Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexus
  labels:
    app: nexus
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nexus
  template:
    metadata:
      labels:
        app: nexus
    spec:
      containers:
      - name: nexus
        image: nexus-app:latest
        ports:
        - containerPort: 8000
          name: api
        - containerPort: 3001
          name: mcp
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: nexus-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: nexus-secrets
              key: redis-url
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Service

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nexus
spec:
  selector:
    app: nexus
  ports:
  - name: api
    port: 8000
    targetPort: 8000
  - name: mcp
    port: 3001
    targetPort: 3001
  type: LoadBalancer
```

### Ingress

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nexus-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - nexus.example.com
    secretName: nexus-tls
  rules:
  - host: nexus.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nexus
            port:
              number: 8000
```

### ConfigMap

```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nexus-config
data:
  LOG_LEVEL: "INFO"
  MONITORING_ENABLED: "true"
  RATE_LIMIT: "5000"
```

### Secrets

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: nexus-secrets
type: Opaque
stringData:
  database-url: "postgresql://user:password@postgres:5432/nexus"
  redis-url: "redis://redis:6379"
  jwt-secret: "your-secret-key"
```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace nexus

# Apply configurations
kubectl apply -f k8s/configmap.yaml -n nexus
kubectl apply -f k8s/secrets.yaml -n nexus
kubectl apply -f k8s/deployment.yaml -n nexus
kubectl apply -f k8s/service.yaml -n nexus
kubectl apply -f k8s/ingress.yaml -n nexus

# Check deployment
kubectl get pods -n nexus
kubectl get services -n nexus
kubectl get ingress -n nexus

# View logs
kubectl logs -f deployment/nexus -n nexus

# Scale deployment
kubectl scale deployment/nexus --replicas=5 -n nexus
```

## Scaling Strategies

### Horizontal Scaling

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nexus-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nexus
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Vertical Scaling

Adjust resource limits in deployment:

```yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "1000m"
  limits:
    memory: "4Gi"
    cpu: "4000m"
```

## Production Best Practices

### 1. Use Redis for Sessions

```python
app = Nexus(
    session_backend="redis",
    redis_url=os.getenv("REDIS_URL"),
    session_timeout=3600
)
```

### 2. Enable Monitoring

```python
app = Nexus(
    enable_monitoring=True,
    monitoring_backend="prometheus",
    monitoring_interval=30
)
```

### 3. Configure Logging

```python
app = Nexus(
    log_level="INFO",
    log_format="json",
    log_file="/var/log/nexus/app.log"
)
```

### 4. Disable Auto-Discovery

```python
app = Nexus(
    auto_discovery=False  # Manual registration only
)

# Register workflows explicitly
from workflows import workflow1, workflow2
app.register("workflow1", workflow1.build())
app.register("workflow2", workflow2.build())
```

### 5. Enable Security Features

```python
app = Nexus(
    enable_auth=True,
    enable_rate_limiting=True,
    rate_limit=5000,
    force_https=True,
    ssl_cert="/path/to/cert.pem",
    ssl_key="/path/to/key.pem"
)
```

### 6. Health Checks

```python
# Configure health check endpoints
@app.health_check_handler("database")
def check_database():
    # Verify database connectivity
    return {"status": "healthy"}

@app.health_check_handler("cache")
def check_cache():
    # Verify Redis connectivity
    return {"status": "healthy"}
```

### 7. Graceful Shutdown

```python
import signal
import sys

def graceful_shutdown(signum, frame):
    print("Shutting down gracefully...")
    app.stop()
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)
```

## Monitoring in Production

### Prometheus Metrics

```bash
# Metrics endpoint
curl http://nexus:8000/metrics

# Add to Prometheus config
scrape_configs:
  - job_name: 'nexus'
    static_configs:
      - targets: ['nexus:8000']
```

### Grafana Dashboard

Import Nexus Grafana dashboard for visualization.

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: docker build -t nexus-app:${{ github.sha }} .

      - name: Push to registry
        run: |
          docker tag nexus-app:${{ github.sha }} registry.example.com/nexus-app:${{ github.sha }}
          docker push registry.example.com/nexus-app:${{ github.sha }}

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/nexus nexus=registry.example.com/nexus-app:${{ github.sha }} -n nexus
          kubectl rollout status deployment/nexus -n nexus
```

## Key Takeaways

- Use Docker for containerization
- Deploy to Kubernetes for orchestration
- Enable Redis for distributed sessions
- Configure monitoring and logging
- Implement health checks
- Use horizontal scaling for high load
- Enable security features
- Automate deployments with CI/CD

## Related Skills

- [nexus-config-options](#) - Configuration reference
- [nexus-enterprise-features](#) - Production features
- [nexus-health-monitoring](#) - Monitor production
- [nexus-troubleshooting](#) - Fix production issues
