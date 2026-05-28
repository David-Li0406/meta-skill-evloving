---
name: devops-patterns
description: Use this skill when containerizing applications, setting up CI/CD pipelines, or deploying services across various platforms.
---

# DevOps Patterns

This skill provides best practices and patterns for DevOps practices, supporting on-demand loading across multiple platforms.

## Trigger Conditions

- Containerizing applications (Docker)
- Configuring CI/CD pipelines
- Deploying services to cloud platforms
- Setting up monitoring and alerts
- Infrastructure as Code (IaC)

## Platform-Specific Patterns

Load the corresponding platform-specific files based on project requirements:

| Platform   | Load File     | Content                          |
|------------|---------------|----------------------------------|
| Docker     | `docker.md`   | Containerization, Compose, Image Optimization |
| CI/CD      | `ci-cd.md`    | GitHub Actions, GitLab CI       |
| Kubernetes | `kubernetes.md`| K8s Deployment, Services, Configuration |

**Loading Method**: Detect project files such as `Dockerfile`, `.github/workflows`, or `k8s/` to determine requirements.

---

## General DevOps Principles

### 12-Factor App Principles

```
┌─────────────────────────────────────────────────────────────┐
│                    12-Factor App Core Principles            │
├─────────────────────────────────────────────────────────────┤
│  1. Codebase        One codebase, many deploys               │
│  2. Dependencies    Explicitly declare dependencies           │
│  3. Config          Store configuration in environment variables|
│  4. Backing Services Treat backing services as attached resources|
│  5. Build/Release/Run Strictly separate build, release, run  │
│  6. Processes       Execute the app as one or more stateless processes|
│  7. Port Binding    Export services via port binding         │
│  8. Concurrency     Scale out via the process model         │
│  9. Disposability   Maximize robustness with fast startup and graceful shutdown|
│ 10. Dev/Prod Parity Keep development, staging, and production as similar as possible|
│ 11. Logs            Treat logs as event streams               │
│ 12. Admin Processes Run admin/management tasks as one-off processes|
└─────────────────────────────────────────────────────────────┘
```

### Environment Management

```
┌─────────────────────────────────────────────────────────────┐
│                      Environment Flow                        │
├─────────────────────────────────────────────────────────────┤
│  Development → Staging → Production                         │
│       ↓           ↓           ↓                             │
│   Local Dev      Pre-release   Production Environment      │
│   .env.local     .env.staging  .env.production              │
└─────────────────────────────────────────────────────────────┘
```

**Environment Variable Management**:

```bash
# .env.example (commit to Git as a template)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379
API_KEY=your-api-key-here

# .env.local (do not commit, local development)
DATABASE_URL=postgresql://dev:dev@localhost:5432/myapp_dev
```

---

## Deployment Strategies

### Blue-Green Deployment

```
         ┌──────────────┐
         │   Load Balancer │
         └──────┬───────┘
                │
        ┌───────┴───────┐
        ↓               ↓
  ┌──────────┐    ┌──────────┐
  │  Blue Environment │    │  Green Environment │
  │ (Current Version) │    │ (New Version)      │
  │  Active           │    │ Standby            │
  └──────────┘    └──────────┘
```

**Switching Process**:
1. Deploy the new version to the Standby environment.
2. Validate the new version.
3. Switch the load balancer to the new environment.
4. Retain the old environment as a rollback backup.

### Rolling Deployment

```
Initial State:  [v1] [v1] [v1] [v1]
Step 1:        [v2] [v1] [v1] [v1]
Step 2:        [v2] [v2] [v1] [v1]
Step 3:        [v2] [v2] [v2] [v1]
Complete:      [v2] [v2] [v2] [v2]
```

**Configuration Example**:
```yaml
# Rolling update strategy
maxSurge: 25%        # Maximum 25% extra Pods
maxUnavailable: 25%  # Maximum 25% Pods unavailable
```

### Canary Release

```
         ┌──────────────┐
         │   Load Balancer │
         └──────┬───────┘
                │
        ┌───────┴───────┐
        │  90%          │  10%
        ↓               ↓
  ┌──────────┐    ┌──────────┐
  │  Stable Version  │    │  New Version   │
  │   v1.0          │    │   v1.1         │
  └──────────┘    └──────────┘
```

**Process**:
1. The new version receives 5-10% of traffic.
2. Monitor error rates and performance metrics.
3. Gradually increase traffic percentage.
4. Full release or rollback.

---

## Monitoring and Observability

### Three Pillars

| Pillar    | Purpose                | Tools                     |
|-----------|-----------------------|---------------------------|
| **Metrics** | Aggregated numerical data | Prometheus, Datadog      |
| **Logs**    | Discrete event records | ELK, Loki                 |
| **Traces**  | Distributed request tracing | Jaeger, Zipkin           |

### Key Metrics (Golden Signals)

```
┌─────────────────────────────────────────────────────────────┐
│                   Four Golden Signals                       │
├─────────────────────────────────────────────────────────────┤
│  Latency    Response time - p50, p95, p99                   │
│  Traffic    Traffic - QPS, requests per second               │
│  Errors     Error rate - 5xx ratio, failed requests          │
│  Saturation Saturation - CPU, memory, disk usage             │
└─────────────────────────────────────────────────────────────┘
```

### Alerting Rules Example

```yaml
# Prometheus alerting rules
groups:
  - name: application
    rules:
      # High error rate alert
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate: {{ $value | humanizePercentage }}"

      # High latency alert
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P95 latency exceeds 1s"
```

---

## Infrastructure as Code (IaC)

### Directory Structure

```
infrastructure/
├── terraform/
│   ├── environments/
│   │   ├── dev/
│   │   │   └── main.tf
│   │   ├── staging/
│   │   │   └── main.tf
│   │   └── production/
│   │       └── main.tf
│   ├── modules/
│   │   ├── vpc/
│   │   ├── database/
│   │   └── kubernetes/
│   └── variables.tf
├── ansible/
│   ├── playbooks/
│   └── inventory/
└── scripts/
    ├── deploy.sh
    └── rollback.sh
```

### Terraform Basic Example

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

variable "environment" {
  description = "Deployment environment"
  type        = string
}

resource "aws_instance" "app" {
  ami           = var.ami_id
  instance_type = var.environment == "production" ? "t3.medium" : "t3.micro"

  tags = {
    Name        = "app-${var.environment}"
    Environment = var.environment
  }
}

output "instance_ip" {
  value = aws_instance.app.public_ip
}
```

---

## Security Best Practices

### Image Security

```dockerfile
# ✅ Use specific versions, not latest
FROM node:20-alpine

# ✅ Run as non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# ✅ Scan for vulnerabilities
# docker scan myimage:tag
```

### Key Management

| Solution               | Use Case          | Tools                          |
|-----------------------|-------------------|--------------------------------|
| Environment Variables  | Development/Simple Deployment | .env files                  |
| Secrets Management Service | Production Environment | AWS Secrets Manager, Vault   |
| K8s Secrets           | Kubernetes        | kubectl create secret         |

```bash
# Create K8s Secret
kubectl create secret generic app-secrets \
  --from-literal=db-password=mysecretpassword \
  --from-literal=api-key=myapikey
```

### Network Security

```yaml
# Network policy example - allow access only from specific sources
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
spec:
  podSelector:
    matchLabels:
      app: api
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - port: 8080
```

---

## Logging Management

### Structured Logging

```json
{
  "timestamp": "2025-01-23T10:00:00Z",
  "level": "info",
  "service": "user-service",
  "traceId": "abc123",
  "message": "User login successful",
  "userId": "user_456",
  "duration": 45,
  "environment": "production"
}
```

### Logging Level Guide

| Level  | Purpose               | Production Environment |
|--------|----------------------|------------------------|
| DEBUG  | Detailed debug info  | Off                    |
| INFO   | Normal operational events | On                  |
| WARN   | Potential issues      | On                     |
| ERROR  | Recoverable errors    | On                     |
| FATAL  | Fatal errors          | On                     |

---

## Best Practices

1. **Externalize Configuration** - Do not hardcode configuration in code.
2. **Stateless Design** - Application instances can be destroyed and rebuilt at any time.
3. **Health Checks** - Configure liveness and readiness probes.
4. **Graceful Termination** - Handle SIGTERM signals to complete ongoing requests.
5. **Log Standardization** - Use structured logs with a unified format.
6. **Monitoring Alerts** - Monitor key metrics and alert promptly.
7. **Rollback Capability** - Retain multiple versions to support quick rollbacks.
8. **Security Scanning** - Scan images for vulnerabilities and check dependencies.
9. **Resource Limits** - Set CPU/memory limits to prevent resource exhaustion.
10. **Documentation** - Document deployment processes and troubleshooting steps.

---

## Maintenance

- Sources: 12-Factor App, CNCF, various cloud platform documentation
- Last updated: 2025-01-23
- Pattern: General principles + on-demand loading of platform-specific content