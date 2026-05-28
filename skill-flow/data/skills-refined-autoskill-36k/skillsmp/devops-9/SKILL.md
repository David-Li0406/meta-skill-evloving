---
name: devops
description: "DevOps and infrastructure review process. Use when reviewing Dockerfiles, analyzing Kubernetes manifests, evaluating Terraform or CloudFormation, reviewing CI/CD pipelines, or setting up monitoring. Also use when containers run as root, CI/CD uses unpinned action versions, secrets appear in configs, no resource limits are set, or security scanning is missing. Essential for container security, GitOps, Helm charts, and infrastructure scanning with Trivy, Checkov, or tfsec."
---

# DevOps Skill

## Overview

Infrastructure mistakes are expensive to fix in production. This skill guides systematic review of DevOps configurations for security, reliability, and maintainability.

**Core principle:** Infrastructure as code should be reviewed like application code. Security misconfigurations are the #1 cloud breach cause.

## The DevOps Review Process

### Phase 1: Security First

**Before reviewing functionality:**

1. **Check Secrets Management**
   - No secrets in code, configs, or logs?
   - Using external secrets manager?
   - Secrets rotatable without deploy?

2. **Check Least Privilege**
   - Containers run as non-root?
   - Minimal IAM/RBAC permissions?
   - Network policies restrict traffic?

3. **Check Supply Chain**
   - Dependencies pinned to SHA/digest?
   - Images from trusted registries?
   - CI actions pinned, not floating?

### Phase 2: Reliability

**Then check for operational concerns:**

1. **Resource Management**
   - CPU/memory limits set?
   - Autoscaling configured?
   - Graceful shutdown handled?

2. **Health Checks**
   - Liveness and readiness probes?
   - Appropriate timeouts?
   - Startup probes for slow apps?

3. **Observability**
   - Metrics exposed?
   - Structured logging?
   - Traces for distributed systems?

### Phase 3: Maintainability

**Finally, check for long-term health:**

1. **Reproducibility**
   - Builds deterministic?
   - Versions pinned?
   - State managed remotely?

2. **Documentation**
   - Runbooks for incidents?
   - Architecture documented?
   - Deployment process clear?

## Red Flags - STOP and Fix

### Container Red Flags

```dockerfile
# Running as root
USER root

# Unpinned base image
FROM node:latest

# Secrets in environment
ENV API_KEY=sk-live-xxx

# ADD instead of COPY
ADD . /app

# No .dockerignore
# (secrets and node_modules in image)
```

### Kubernetes Red Flags

```yaml
# Privileged container
securityContext:
  privileged: true

# No resource limits
# (missing resources.limits)

# Running as root
# (missing runAsNonRoot: true)

# No network policies
# (pods can reach anything)

# No probes
# (unhealthy pods serve traffic)
```

### CI/CD Red Flags

```yaml
# Unpinned action (supply chain risk)
uses: actions/checkout@v4

# Broad permissions
permissions: write-all

# Secrets in logs
run: echo ${{ secrets.API_KEY }}

# pull_request_target (code injection)
on: pull_request_target
```

### Terraform Red Flags

```hcl
# Unpinned provider
provider "aws" {}

# Local state
# (no backend block)

# Hardcoded secrets
password = "supersecret"

# No state locking
# (missing dynamodb_table)
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "It's only internal" | Internal doesn't mean safe. Apply same standards. |
| "We'll add security later" | Security debt compounds. Fix now. |
| "Root is easier" | Root enables container escapes. Use non-root. |
| "Pinning is annoying" | Unpinned = supply chain attacks. Pin everything. |
| "Limits cause restarts" | No limits = noisy neighbor. Set appropriate limits. |
| "It works in dev" | Dev ≠ prod. Test in realistic conditions. |

## DevOps Checklist

Before approving infrastructure changes:

- [ ] **Non-root**: Containers don't run as root
- [ ] **Pinned**: Images, actions, providers version-pinned
- [ ] **No secrets**: No hardcoded credentials anywhere
- [ ] **Limits set**: CPU/memory limits configured
- [ ] **Probes**: Health checks configured
- [ ] **Scanned**: Security scanning in pipeline
- [ ] **Least privilege**: Minimal permissions granted

## Quick Security Scans

```bash
# Container scanning
trivy image myapp:latest
hadolint Dockerfile

# Kubernetes scanning
kubesec scan deployment.yaml
kube-score score deployment.yaml

# Terraform scanning
tfsec .
checkov -d .

# CI/CD scanning
# Use GitHub's security features or similar
```

## Quick Patterns

### Secure Dockerfile

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine
RUN adduser -D appuser
USER appuser
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

### Secure K8s Pod

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
resources:
  limits:
    memory: "256Mi"
    cpu: "500m"
livenessProbe:
  httpGet:
    path: /health
    port: 8080
```

### Secure CI Action

```yaml
uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608
permissions:
  contents: read
timeout-minutes: 10
```

## References

Detailed patterns and examples in `references/`:
- `docker-security.md` - Container security patterns
- `kubernetes-security.md` - K8s hardening guide
- `cicd-security.md` - Pipeline security
- `terraform-patterns.md` - IaC best practices
