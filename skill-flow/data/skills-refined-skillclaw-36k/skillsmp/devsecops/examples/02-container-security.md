# Container Security with Docker and Kubernetes

Comprehensive guide to securing containers using Trivy, secure Dockerfile practices, and Kubernetes security policies.

## 📝 Prompt

```
Create a complete container security guide:

Context:
- Node.js microservices
- Docker containers
- Kubernetes deployment on AWS EKS
- Production workloads with PCI compliance requirements

Include:
- Secure Dockerfile with all best practices
- Multi-stage builds for minimal attack surface
- Trivy scanning configuration and automation
- Kubernetes security policies (NetworkPolicy, PodSecurityPolicy, RBAC)
- Security contexts and resource limits
- Secrets management in Kubernetes
- Runtime security monitoring
- Compliance checks (CIS benchmarks)

Provide complete, production-ready examples.
```

## 🐳 Secure Dockerfile

### Production-Ready Multi-Stage Dockerfile

**File:** `Dockerfile`

```dockerfile
# ===== STAGE 1: Build Stage =====
FROM node:18.19-alpine3.19 AS builder

# Add security labels
LABEL maintainer="security@example.com" \
      security.scan="trivy" \
      compliance="CIS Docker Benchmark v1.6"

# Install build dependencies with specific versions
RUN apk add --no-cache \
    python3=3.11.6-r0 \
    make=4.4.1-r1 \
    g++=13.2.1_git20231014-r0 \
    && rm -rf /var/cache/apk/*

# Create app directory
WORKDIR /build

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install ALL dependencies (including dev dependencies for building)
RUN npm ci --include=dev && \
    npm cache clean --force

# Copy source code
COPY src/ ./src/

# Build TypeScript to JavaScript
RUN npm run build && \
    npm prune --production

# ===== STAGE 2: Production Stage =====
FROM node:18.19-alpine3.19 AS production

# Security updates
RUN apk upgrade --no-cache && \
    apk add --no-cache \
    dumb-init=1.2.5-r2 \
    curl=8.5.0-r0 \
    && rm -rf /var/cache/apk/*

# Create non-root user with specific UID/GID
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs

# Set working directory
WORKDIR /app

# Copy only production node_modules from builder
COPY --from=builder --chown=nodejs:nodejs /build/node_modules ./node_modules

# Copy built application
COPY --from=builder --chown=nodejs:nodejs /build/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /build/package*.json ./

# Copy only necessary runtime files
COPY --chown=nodejs:nodejs healthcheck.js ./
COPY --chown=nodejs:nodejs config/ ./config/

# Set environment variables
ENV NODE_ENV=production \
    PORT=3000 \
    LOG_LEVEL=info

# Use non-root user
USER nodejs

# Expose port (non-privileged)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js || exit 1

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Run application
CMD ["node", "dist/server.js"]

# Add metadata
LABEL org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="Example Corp" \
      org.opencontainers.image.source="https://github.com/example/app" \
      org.opencontainers.image.title="Example API" \
      org.opencontainers.image.description="Secure Node.js API service"
```

### Dockerfile Security Checklist

```dockerfile
# ✅ DO THIS
# - Use specific base image versions (not 'latest')
FROM node:18.19-alpine3.19

# - Use multi-stage builds to minimize final image size
FROM node:18 AS builder
FROM node:18-alpine AS production

# - Run as non-root user
USER nodejs

# - Use COPY instead of ADD
COPY package.json ./

# - Minimize layers by combining RUN commands
RUN apk add --no-cache curl && \
    rm -rf /var/cache/apk/*

# - Use .dockerignore to exclude unnecessary files
# See .dockerignore section below

# - Set specific versions for packages
RUN apk add --no-cache curl=8.5.0-r0

# - Use HEALTHCHECK
HEALTHCHECK CMD curl -f http://localhost:3000/health || exit 1

# - Add security labels
LABEL security.scan="trivy"

# ❌ DON'T DO THIS
# - Don't use 'latest' tag
FROM node:latest  # ❌

# - Don't run as root
USER root  # ❌

# - Don't use ADD when COPY works
ADD package.json ./  # ❌

# - Don't install unnecessary packages
RUN apt-get install -y sudo vim  # ❌

# - Don't expose privileged ports
EXPOSE 80  # ❌ Use > 1024

# - Don't store secrets in the image
ENV DB_PASSWORD=secret123  # ❌

# - Don't create unnecessary layers
RUN npm install
RUN npm build
RUN npm test  # ❌ Combine these
```

---

## 🔒 .dockerignore File

**File:** `.dockerignore`

```plaintext
# Version control
.git
.gitignore
.github

# Documentation
README.md
CONTRIBUTING.md
docs/
*.md

# Testing
tests/
test/
**/*.test.js
**/*.test.ts
**/*.spec.js
**/*.spec.ts
coverage/
.nyc_output

# Development
.env
.env.local
.env.*.local
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode
.idea
*.swp
*.swo
*~

# Dependencies (will be installed in container)
node_modules/

# Build artifacts (from host)
dist/
build/

# CI/CD
.gitlab-ci.yml
.github/
Jenkinsfile
azure-pipelines.yml

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore

# OS
.DS_Store
Thumbs.db

# Temporary files
tmp/
temp/
*.tmp
```

---

## 🔍 Trivy Scanning

### Trivy Configuration

**File:** `.trivy.yaml`

```yaml
# Trivy configuration
format: table
severity: UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL
exit-code: 1
vuln-type:
  - os
  - library
security-checks:
  - vuln
  - config
  - secret
scanners:
  - vuln
  - misconfig
  - secret

# Ignore specific vulnerabilities (with justification)
ignoredVulnerabilities:
  # CVE-2023-12345: False positive, not applicable to our use case
  - CVE-2023-12345

# Severity threshold
severity-threshold: HIGH

# Timeout
timeout: 10m

# Cache
cache:
  ttl: 24h
```

### Trivy Scan Script

**File:** `scripts/scan-container.sh`

```bash
#!/bin/bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

IMAGE_NAME="${1:-app:latest}"
REPORT_DIR="security-reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🔍 Starting container security scan..."
echo "📦 Image: $IMAGE_NAME"

# Create report directory
mkdir -p "$REPORT_DIR"

# ===== VULNERABILITY SCANNING =====
echo ""
echo "🐛 Scanning for vulnerabilities..."
trivy image \
  --severity CRITICAL,HIGH,MEDIUM \
  --format table \
  --output "$REPORT_DIR/vulnerabilities_${TIMESTAMP}.txt" \
  "$IMAGE_NAME"

# Check for critical vulnerabilities
CRITICAL_COUNT=$(trivy image --severity CRITICAL --format json "$IMAGE_NAME" | jq '[.Results[].Vulnerabilities[]? | select(.Severity == "CRITICAL")] | length')
HIGH_COUNT=$(trivy image --severity HIGH --format json "$IMAGE_NAME" | jq '[.Results[].Vulnerabilities[]? | select(.Severity == "HIGH")] | length')

echo ""
echo "📊 Vulnerability Summary:"
echo "   Critical: $CRITICAL_COUNT"
echo "   High: $HIGH_COUNT"

# ===== MISCONFIGURATION SCANNING =====
echo ""
echo "⚙️  Scanning for misconfigurations..."
trivy config \
  --severity CRITICAL,HIGH \
  --format table \
  --output "$REPORT_DIR/misconfig_${TIMESTAMP}.txt" \
  .

# ===== SECRET SCANNING =====
echo ""
echo "🔐 Scanning for secrets..."
trivy filesystem \
  --scanners secret \
  --format table \
  --output "$REPORT_DIR/secrets_${TIMESTAMP}.txt" \
  .

# ===== GENERATE JSON REPORT =====
echo ""
echo "📄 Generating JSON report..."
trivy image \
  --format json \
  --output "$REPORT_DIR/full_report_${TIMESTAMP}.json" \
  "$IMAGE_NAME"

# ===== SARIF FORMAT FOR GITHUB =====
echo ""
echo "📝 Generating SARIF report for GitHub..."
trivy image \
  --format sarif \
  --output "$REPORT_DIR/trivy_${TIMESTAMP}.sarif" \
  "$IMAGE_NAME"

# ===== SBOM GENERATION =====
echo ""
echo "📋 Generating Software Bill of Materials (SBOM)..."
trivy image \
  --format cyclonedx \
  --output "$REPORT_DIR/sbom_${TIMESTAMP}.json" \
  "$IMAGE_NAME"

# ===== COMPLIANCE CHECK =====
echo ""
echo "✅ Running compliance checks..."
trivy image \
  --compliance docker-cis \
  --format table \
  --output "$REPORT_DIR/compliance_${TIMESTAMP}.txt" \
  "$IMAGE_NAME"

# ===== DECISION LOGIC =====
echo ""
if [ "$CRITICAL_COUNT" -gt 0 ]; then
  echo -e "${RED}❌ FAIL: $CRITICAL_COUNT critical vulnerabilities found!${NC}"
  echo "🔧 Fix these critical issues before deploying."
  exit 1
elif [ "$HIGH_COUNT" -gt 5 ]; then
  echo -e "${YELLOW}⚠️  WARNING: $HIGH_COUNT high severity vulnerabilities found!${NC}"
  echo "📋 Review and plan remediation."
  exit 0
else
  echo -e "${GREEN}✅ PASS: No critical vulnerabilities found.${NC}"
  echo "📊 Reports saved to: $REPORT_DIR/"
  exit 0
fi
```

### Automated Scanning with GitHub Actions

```yaml
name: Container Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: '0 0 * * *' # Daily at midnight

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t ${{ github.repository }}:${{ github.sha }} .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: '${{ github.repository }}:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Upload Trivy results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'

      - name: Generate HTML report
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: '${{ github.repository }}:${{ github.sha }}'
          format: 'template'
          template: '@/contrib/html.tpl'
          output: 'trivy-report.html'

      - name: Upload HTML report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: trivy-report
          path: trivy-report.html
```

---

## ☸️ Kubernetes Security

### Pod Security Standards

**File:** `k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  namespace: production
  labels:
    app: secure-app
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
        version: v1
      annotations:
        # Security scanning
        trivy.aquasecurity.github.io/scan: "true"
        # Prometheus monitoring
        prometheus.io/scrape: "true"
        prometheus.io/port: "3000"
        prometheus.io/path: "/metrics"
    spec:
      # Security Context for Pod
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        runAsGroup: 1001
        fsGroup: 1001
        seccompProfile:
          type: RuntimeDefault

      # Service Account
      serviceAccountName: secure-app-sa
      automountServiceAccountToken: true

      # Container specification
      containers:
        - name: app
          image: ghcr.io/example/app:v1.0.0
          imagePullPolicy: Always

          # Security Context for Container
          securityContext:
            allowPrivilegeEscalation: false
            runAsNonRoot: true
            runAsUser: 1001
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
              add:
                - NET_BIND_SERVICE

          # Resource limits
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi

          # Ports
          ports:
            - name: http
              containerPort: 3000
              protocol: TCP

          # Liveness probe
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 3
            failureThreshold: 3

          # Readiness probe
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3

          # Environment variables from ConfigMap
          envFrom:
            - configMapRef:
                name: app-config

          # Sensitive environment variables from Secrets
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: password
            - name: API_KEY
              valueFrom:
                secretKeyRef:
                  name: api-credentials
                  key: api-key

          # Volume mounts
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /app/.cache
            - name: config
              mountPath: /app/config
              readOnly: true
            - name: secrets
              mountPath: /app/secrets
              readOnly: true

      # Volumes
      volumes:
        - name: tmp
          emptyDir: {}
        - name: cache
          emptyDir: {}
        - name: config
          configMap:
            name: app-config
        - name: secrets
          secret:
            secretName: app-secrets
            defaultMode: 0400

      # Image pull secrets
      imagePullSecrets:
        - name: ghcr-credentials

      # Node affinity and tolerations
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - secure-app
                topologyKey: kubernetes.io/hostname

      # DNS policy
      dnsPolicy: ClusterFirst

      # Restart policy
      restartPolicy: Always

      # Termination grace period
      terminationGracePeriodSeconds: 30
```

### Network Policy

**File:** `k8s/network-policy.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: secure-app-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: secure-app

  policyTypes:
    - Ingress
    - Egress

  # Ingress rules - who can connect to this app
  ingress:
    # Allow from ingress controller
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
        - podSelector:
            matchLabels:
              app: nginx-ingress
      ports:
        - protocol: TCP
          port: 3000

    # Allow from monitoring (Prometheus)
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
        - podSelector:
            matchLabels:
              app: prometheus
      ports:
        - protocol: TCP
          port: 3000

  # Egress rules - where this app can connect to
  egress:
    # Allow DNS
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
        - podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53

    # Allow to database
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - protocol: TCP
          port: 5432

    # Allow to Redis
    - to:
        - podSelector:
            matchLabels:
              app: redis
      ports:
        - protocol: TCP
          port: 6379

    # Allow HTTPS to external APIs
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: TCP
          port: 443

---
# Deny all traffic by default (fallback)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

### RBAC Configuration

**File:** `k8s/rbac.yaml`

```yaml
---
# Service Account
apiVersion: v1
kind: ServiceAccount
metadata:
  name: secure-app-sa
  namespace: production
automountServiceAccountToken: true

---
# Role - namespace-specific permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secure-app-role
  namespace: production
rules:
  # Allow reading ConfigMaps
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list", "watch"]
    resourceNames: ["app-config"]

  # Allow reading Secrets
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get"]
    resourceNames: ["app-secrets", "db-credentials", "api-credentials"]

  # Allow reading own Pod info
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]

---
# RoleBinding - bind role to service account
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: secure-app-rolebinding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: secure-app-sa
    namespace: production
roleRef:
  kind: Role
  name: secure-app-role
  apiGroup: rbac.authorization.k8s.io
```

### Pod Security Admission

**File:** `k8s/pod-security.yaml`

```yaml
# Enforce Pod Security Standards at namespace level
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    # Enforce restricted policy
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest

    # Audit violations
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: latest

    # Warn about violations
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: latest
```

---

## 🔐 Secrets Management

### Sealed Secrets Example

```yaml
# Install Sealed Secrets controller
# kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml

---
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: db-credentials
  namespace: production
spec:
  encryptedData:
    # These are encrypted and safe to commit to git
    password: AgBxyz123encrypted...
    username: AgAabc456encrypted...
  template:
    metadata:
      name: db-credentials
      namespace: production
    type: Opaque
```

### External Secrets Operator (AWS Secrets Manager)

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
  namespace: production
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: app-secrets
    creationPolicy: Owner
  data:
    - secretKey: api-key
      remoteRef:
        key: prod/app/api-key
    - secretKey: db-password
      remoteRef:
        key: prod/app/db-password
```

---

## 📊 Runtime Security Monitoring

### Falco Rules

**File:** `falco-rules.yaml`

```yaml
# Custom Falco rules for runtime security
- rule: Unexpected Network Connection
  desc: Detect unexpected outbound network connections
  condition: >
    outbound and
    container and
    container.image.repository="ghcr.io/example/app" and
    not fd.sip in (allowed_ips)
  output: >
    Unexpected outbound connection
    (container=%container.name image=%container.image.repository
    connection=%fd.name user=%user.name)
  priority: WARNING

- rule: Write to Non-Temp Directory
  desc: Detect writes to read-only filesystem
  condition: >
    open_write and
    container and
    container.image.repository="ghcr.io/example/app" and
    not fd.directory in (/tmp, /app/.cache)
  output: >
    Write to unexpected directory
    (file=%fd.name container=%container.name)
  priority: ERROR

- rule: Sensitive File Read
  desc: Detect reads of sensitive files
  condition: >
    open_read and
    container and
    fd.name in (/etc/shadow, /etc/passwd, /root/.ssh/id_rsa)
  output: >
    Sensitive file accessed
    (file=%fd.name container=%container.name user=%user.name)
  priority: CRITICAL
```

---

## ✅ Security Compliance Checklist

### CIS Docker Benchmark Compliance

```bash
#!/bin/bash
# CIS Docker Benchmark automated check

echo "Running CIS Docker Benchmark checks..."

# Check 1: Use trusted base images
trivy image --severity HIGH,CRITICAL node:18-alpine

# Check 2: Scan for vulnerabilities
docker scout cves ghcr.io/example/app:latest

# Check 3: Verify image signatures
cosign verify --key cosign.pub ghcr.io/example/app:latest

# Check 4: Check for secrets
trivy filesystem --scanners secret .

# Check 5: Verify user is non-root
docker inspect ghcr.io/example/app:latest | jq '.[0].Config.User'

# Check 6: Verify security options
docker inspect ghcr.io/example/app:latest | jq '.[0].HostConfig.SecurityOpt'

# Check 7: Check resource limits
kubectl get deployment secure-app -o json | jq '.spec.template.spec.containers[].resources'

# Check 8: Network policies exist
kubectl get networkpolicy -n production

# Check 9: Pod security standards
kubectl get namespace production -o yaml | grep pod-security

# Check 10: RBAC properly configured
kubectl auth can-i --list --as=system:serviceaccount:production:secure-app-sa
```

---

## 💡 Best Practices Summary

### Container Image Security
1. ✅ Use minimal base images (Alpine, Distroless)
2. ✅ Multi-stage builds to reduce final image size
3. ✅ Run as non-root user
4. ✅ Scan images before deployment
5. ✅ Sign images with Cosign/Notation
6. ✅ Use specific image tags, never `:latest`
7. ✅ Regular base image updates
8. ✅ Remove unnecessary packages and files

### Kubernetes Security
1. ✅ Enable Pod Security Standards
2. ✅ Implement Network Policies
3. ✅ Use RBAC with least privilege
4. ✅ Run as non-root with security contexts
5. ✅ Read-only root filesystem
6. ✅ Drop all capabilities, add only needed
7. ✅ Resource limits on all containers
8. ✅ Regular security audits

### Secrets Management
1. ✅ Never hardcode secrets
2. ✅ Use external secret managers (Vault, AWS Secrets Manager)
3. ✅ Encrypt secrets at rest
4. ✅ Rotate secrets regularly
5. ✅ Audit secret access
6. ✅ Use short-lived credentials
7. ✅ Principle of least privilege

### Monitoring & Response
1. ✅ Runtime security monitoring (Falco)
2. ✅ Log aggregation and analysis
3. ✅ Alert on security events
4. ✅ Regular vulnerability scans
5. ✅ Incident response procedures
6. ✅ Security metrics dashboard
7. ✅ Compliance reporting

---

## 🎯 Quick Start

```bash
# 1. Build secure image
docker build -t myapp:v1 .

# 2. Scan with Trivy
trivy image myapp:v1

# 3. Run security checks
./scripts/scan-container.sh myapp:v1

# 4. Deploy to Kubernetes
kubectl apply -f k8s/

# 5. Verify security
kubectl get psp,networkpolicy,securitycontext -n production

# 6. Monitor runtime
kubectl logs -n falco -l app=falco --tail=100
```
