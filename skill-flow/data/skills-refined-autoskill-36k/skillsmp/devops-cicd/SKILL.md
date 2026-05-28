---
name: devops-cicd
description: Build robust CI/CD pipelines with GitHub Actions, Docker containers, infrastructure as code, deployment strategies (blue-green, canary), and monitoring. Automate everything from commit to production.
---

# DevOps & CI/CD

Complete framework for building automated pipelines that let you ship faster with confidence.

## When to Use

- Setting up CI/CD for new projects
- Improving existing deployment pipelines
- Dockerizing applications
- Implementing infrastructure as code
- Choosing deployment strategies
- Setting up monitoring and alerts

## Core DevOps Principles

**Automate Everything:**
- If you do it twice, script it
- If you script it twice, make it a pipeline
- Reduce manual intervention

**Shift Left:**
- Test early
- Security early
- Quality early
- Catch issues before production

**Infrastructure as Code:**
- Version control your infrastructure
- Review changes like code
- Reproducible environments

---

## Workflow

### Step 1: CI/CD Pipeline Design

**Pipeline Stages:**
```
COMMIT → BUILD → TEST → SECURITY → DEPLOY → MONITOR

1. COMMIT
   ├── Code pushed to GitHub
   ├── Trigger pipeline
   └── Validate commit message

2. BUILD
   ├── Install dependencies
   ├── Compile/bundle
   ├── Build Docker image
   └── Cache for speed

3. TEST
   ├── Lint code
   ├── Type check
   ├── Unit tests
   ├── Integration tests
   └── Coverage check

4. SECURITY
   ├── SAST (static analysis)
   ├── Dependency scan
   ├── Secret detection
   └── Container scan

5. DEPLOY
   ├── Deploy to environment
   ├── Run migrations
   ├── Health checks
   └── Smoke tests

6. MONITOR
   ├── Performance metrics
   ├── Error rates
   ├── Alerting
   └── Rollback if needed
```

### Step 2: GitHub Actions CI/CD

**Complete Pipeline Example:**
```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # Build and test
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run typecheck

      - name: Unit tests
        run: npm test -- --coverage

      - name: Build
        run: npm run build

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  # Security scanning
  security:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk to check for vulnerabilities
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Check for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./

  # Build and push Docker image
  docker:
    needs: [build, security]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: myapp/api:${{ github.sha }},myapp/api:latest
          cache-from: type=registry,ref=myapp/api:latest
          cache-to: type=inline

  # Deploy to staging
  deploy-staging:
    needs: [docker]
    runs-on: ubuntu-latest
    environment: staging

    steps:
      - name: Deploy to staging
        run: |
          # SSH into staging server and deploy
          ssh ${{ secrets.STAGING_USER }}@${{ secrets.STAGING_HOST }} << 'EOF'
            docker pull myapp/api:${{ github.sha }}
            docker-compose up -d
          EOF

      - name: Run E2E tests
        run: npm run test:e2e
        env:
          BASE_URL: https://staging.myapp.com

      - name: Smoke tests
        run: |
          curl -f https://staging.myapp.com/health || exit 1

  # Deploy to production (manual approval required)
  deploy-production:
    needs: [deploy-staging]
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Deploy to production
        run: |
          ssh ${{ secrets.PROD_USER }}@${{ secrets.PROD_HOST }} << 'EOF'
            docker pull myapp/api:${{ github.sha }}
            docker-compose up -d --no-deps api
          EOF

      - name: Health check
        run: |
          curl -f https://myapp.com/health || exit 1

      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "Deployed ${{ github.sha }} to production ✅"
            }
```

### Step 3: Docker Best Practices

**Multi-Stage Dockerfile:**
```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first (cache optimization)
COPY package*.json ./

# Install ALL dependencies (including devDependencies for build)
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Stage 2: Production
FROM node:20-alpine

WORKDIR /app

# Install only production dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy built files from builder stage
COPY --from=builder /app/dist ./dist

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Change ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD node healthcheck.js || exit 1

CMD ["node", "dist/index.js"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  api:
    image: myapp/api:latest
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - db
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 3s
      retries: 3

  db:
    image: postgres:15-alpine
    restart: unless-stopped
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=myapp

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Step 4: Deployment Strategies

**Blue-Green Deployment:**
```
CONCEPT:
├── Two identical environments (Blue/Green)
├── One serves traffic, one is idle
├── Deploy to idle, then switch traffic
└── Instant rollback by switching back

FLOW:
1. Blue is live, Green is idle
2. Deploy new version to Green
3. Test Green thoroughly
4. Switch load balancer to Green
5. Green is now live (Blue becomes rollback target)
```

**Kubernetes Blue-Green:**
```yaml
# green-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
      version: green
  template:
    metadata:
      labels:
        app: api
        version: green
    spec:
      containers:
        - name: api
          image: myapp/api:v2.0.0

---
# Switch traffic by updating service selector
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
    version: green  # Change from "blue" to "green"
  ports:
    - port: 80
      targetPort: 3000
```

**Canary Deployment:**
```
CONCEPT:
├── Release to small subset first (5% traffic)
├── Monitor for issues
├── Gradually increase traffic (25%, 50%, 100%)
└── Rollback if problems detected

KUBERNETES EXAMPLE:
# 95% traffic to stable, 5% to canary
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-stable
spec:
  selector:
    app: api
    version: stable
  ports:
    - port: 80

---
apiVersion: v1
kind: Service
metadata:
  name: api-canary
spec:
  selector:
    app: api
    version: canary
  ports:
    - port: 80

---
# Ingress splits traffic
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "5"  # 5% to canary
spec:
  rules:
    - host: api.myapp.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-canary
                port:
                  number: 80
```

**Rolling Deployment:**
```yaml
# Kubernetes rolling update
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1   # Max pods down during update
      maxSurge: 1         # Max extra pods during update
  template:
    spec:
      containers:
        - name: api
          image: myapp/api:v2.0.0
```

### Step 5: Infrastructure as Code

**Terraform Example:**
```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name        = "${var.project}-vpc"
    Environment = var.environment
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# RDS Database
resource "aws_db_instance" "main" {
  identifier           = "${var.project}-${var.environment}"
  engine               = "postgres"
  engine_version       = "15.4"
  instance_class       = var.db_instance_class
  allocated_storage    = 20
  storage_encrypted    = true
  skip_final_snapshot  = var.environment != "production"

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = var.environment == "production" ? 7 : 0

  tags = {
    Name        = "${var.project}-db"
    Environment = var.environment
  }
}
```

### Step 6: Monitoring & Health Checks

**Health Endpoints:**
```javascript
// health.js
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: process.env.VERSION || 'unknown',
    uptime: process.uptime()
  });
});

// Readiness check (can serve traffic)
app.get('/ready', async (req, res) => {
  try {
    // Check database
    await db.query('SELECT 1');

    // Check cache
    await redis.ping();

    // Check critical dependencies
    // await externalAPI.healthCheck();

    res.json({
      status: 'ready',
      checks: {
        database: 'ok',
        redis: 'ok'
      }
    });
  } catch (error) {
    res.status(503).json({
      status: 'not ready',
      error: error.message
    });
  }
});
```

**Key Metrics (Golden Signals):**
```
LATENCY: How long requests take
TRAFFIC: Requests per second
ERRORS: Error rate percentage
SATURATION: Resource utilization (CPU, memory)
```

---

## DevOps Checklist

```markdown
## DevOps Review: [Project]

### CI/CD
- [ ] Pipeline runs on every PR
- [ ] Tests pass before merge
- [ ] Security scans included
- [ ] Automated deployment to staging
- [ ] Manual approval for production
- [ ] Rollback mechanism in place

### Docker
- [ ] Multi-stage builds
- [ ] Non-root user
- [ ] Health checks defined
- [ ] Secrets via env vars
- [ ] Image scanning for vulnerabilities

### Infrastructure
- [ ] Infrastructure as code (Terraform/CloudFormation)
- [ ] Secrets managed securely (not in code)
- [ ] Environments are reproducible
- [ ] Backups configured and tested
- [ ] Disaster recovery plan documented

### Monitoring
- [ ] Health endpoints implemented
- [ ] Metrics collected (Golden Signals)
- [ ] Logging centralized
- [ ] Alerts configured (PagerDuty, Slack)
- [ ] Dashboards created (Grafana, Datadog)

### Security
- [ ] Dependencies scanned automatically
- [ ] Secrets not in code or logs
- [ ] Network policies defined
- [ ] Least privilege access (IAM, RBAC)
- [ ] Security headers configured
```

---

## Common Pitfalls

| Don't | Do |
|-------|-----|
| Manual deployments | Automate with CI/CD |
| Skip tests in pipeline | Run all tests before deploy |
| Use `latest` tag | Use specific versions/SHAs |
| Run as root in containers | Create non-root user |
| Commit secrets to git | Use secrets management |
| Deploy straight to prod | Deploy to staging first |
| No rollback plan | Test rollback procedure |
| Ignore failed health checks | Fail deployment if unhealthy |

---

## Tools & Technologies

**CI/CD:**
- GitHub Actions
- GitLab CI
- CircleCI
- Jenkins

**Containers:**
- Docker
- Kubernetes
- Docker Compose
- Podman

**Infrastructure as Code:**
- Terraform
- AWS CloudFormation
- Pulumi
- Ansible

**Monitoring:**
- Prometheus + Grafana
- Datadog
- New Relic
- Sentry

---

## Related Skills

- `/testing-strategies` - Running tests in CI/CD
- `/security-review` - Security scanning in pipelines
- `/performance-optimization` - Performance monitoring

---

**Last Updated**: 2026-01-22
