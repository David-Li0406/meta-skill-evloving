# 🚀 Production-Level Microservices: Complete Guide

> A comprehensive guide to building, deploying, and maintaining production-ready microservices architecture.

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Service Design Patterns](#service-design-patterns)
5. [Inter-Service Communication](#inter-service-communication)
6. [Database Patterns](#database-patterns)
7. [API Gateway](#api-gateway)
8. [Service Discovery](#service-discovery)
9. [Authentication & Security](#authentication--security)
10. [Containerization with Docker](#containerization-with-docker)
11. [Kubernetes Deployment](#kubernetes-deployment)
12. [CI/CD Pipeline](#cicd-pipeline)
13. [Monitoring & Observability](#monitoring--observability)
14. [Resilience Patterns](#resilience-patterns)
15. [Testing Strategies](#testing-strategies)
16. [Production Checklist](#production-checklist)
17. [Cost Optimization](#cost-optimization)
18. [Troubleshooting Guide](#troubleshooting-guide)

---

## 🚢 Deployment Strategies: Monorepo vs Polyrepo

### Overview Comparison

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           MONOREPO APPROACH                                         │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│   microservices-platform/          ONE REPOSITORY                                   │
│   ├── services/                                                                     │
│   │   ├── user-service/       ─────┐                                               │
│   │   ├── product-service/    ─────┼──► All services in ONE Git repo               │
│   │   ├── order-service/      ─────┤                                               │
│   │   └── payment-service/    ─────┘                                               │
│   ├── libs/shared/                                                                  │
│   ├── k8s/                                                                          │
│   └── .github/workflows/                                                            │
│                                                                                     │
│   ✅ Shared code/libs        ✅ Atomic changes       ✅ Unified CI/CD              │
│   ❌ Large repo size         ❌ Coupled deployments  ❌ Complex permissions         │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           POLYREPO APPROACH                                         │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│   user-service/           ──► Own Git repo, own CI/CD, own team                    │
│   product-service/        ──► Own Git repo, own CI/CD, own team                    │
│   order-service/          ──► Own Git repo, own CI/CD, own team                    │
│   payment-service/        ──► Own Git repo, own CI/CD, own team                    │
│   shared-libs/            ──► Published as npm package                              │
│   k8s-manifests/          ──► Separate infra repo (GitOps)                         │
│                                                                                     │
│   ✅ Independent deploys   ✅ Clear ownership      ✅ Faster CI per service        │
│   ❌ Code duplication      ❌ Dependency hell      ❌ Cross-service changes hard   │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 🏢 MONOREPO: Production Deployment Guide

#### Folder Structure

```
microservices-platform/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Runs on all PRs
│       ├── deploy-staging.yml        # Deploy changed services to staging
│       └── deploy-production.yml     # Deploy to production
├── services/
│   ├── user-service/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── product-service/
│   ├── order-service/
│   └── payment-service/
├── libs/
│   ├── common/                       # Shared utilities
│   ├── database/                     # Shared DB config
│   └── contracts/                    # API contracts
├── k8s/
│   ├── base/                         # Base K8s manifests
│   └── overlays/
│       ├── staging/
│       └── production/
├── nx.json                           # Nx monorepo config
├── turbo.json                        # OR Turborepo config
└── package.json
```

#### CI/CD Pipeline for Monorepo

```yaml
# .github/workflows/ci.yml
name: Monorepo CI

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_PREFIX: ${{ github.repository }}

jobs:
  # ===========================================
  # DETECT WHICH SERVICES CHANGED
  # ===========================================
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      user-service: ${{ steps.changes.outputs.user-service }}
      product-service: ${{ steps.changes.outputs.product-service }}
      order-service: ${{ steps.changes.outputs.order-service }}
      payment-service: ${{ steps.changes.outputs.payment-service }}
      shared-libs: ${{ steps.changes.outputs.shared-libs }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Need full history for change detection

      - name: Detect changes
        id: changes
        uses: dorny/paths-filter@v2
        with:
          filters: |
            user-service:
              - 'services/user-service/**'
              - 'libs/**'
            product-service:
              - 'services/product-service/**'
              - 'libs/**'
            order-service:
              - 'services/order-service/**'
              - 'libs/**'
            payment-service:
              - 'services/payment-service/**'
              - 'libs/**'
            shared-libs:
              - 'libs/**'

  # ===========================================
  # TEST ONLY CHANGED SERVICES
  # ===========================================
  test:
    needs: detect-changes
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - service: user-service
            changed: ${{ needs.detect-changes.outputs.user-service }}
          - service: product-service
            changed: ${{ needs.detect-changes.outputs.product-service }}
          - service: order-service
            changed: ${{ needs.detect-changes.outputs.order-service }}
          - service: payment-service
            changed: ${{ needs.detect-changes.outputs.payment-service }}
    
    steps:
      - uses: actions/checkout@v4
        if: matrix.changed == 'true'

      - name: Setup Node.js
        if: matrix.changed == 'true'
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        if: matrix.changed == 'true'
        run: npm ci

      - name: Lint
        if: matrix.changed == 'true'
        run: npx nx lint ${{ matrix.service }}

      - name: Test
        if: matrix.changed == 'true'
        run: npx nx test ${{ matrix.service }} --coverage

      - name: Build
        if: matrix.changed == 'true'
        run: npx nx build ${{ matrix.service }}

  # ===========================================
  # BUILD & PUSH DOCKER IMAGES (Only changed)
  # ===========================================
  build-and-push:
    needs: [detect-changes, test]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - service: user-service
            changed: ${{ needs.detect-changes.outputs.user-service }}
          - service: product-service
            changed: ${{ needs.detect-changes.outputs.product-service }}
          - service: order-service
            changed: ${{ needs.detect-changes.outputs.order-service }}
          - service: payment-service
            changed: ${{ needs.detect-changes.outputs.payment-service }}
    
    permissions:
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v4
        if: matrix.changed == 'true'

      - name: Set up Docker Buildx
        if: matrix.changed == 'true'
        uses: docker/setup-buildx-action@v3

      - name: Log in to Registry
        if: matrix.changed == 'true'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        if: matrix.changed == 'true'
        uses: docker/build-push-action@v5
        with:
          context: .
          file: services/${{ matrix.service }}/Dockerfile
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/${{ matrix.service }}:${{ github.sha }}
            ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/${{ matrix.service }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ===========================================
  # DEPLOY TO STAGING
  # ===========================================
  deploy-staging:
    needs: [detect-changes, build-and-push]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
      - uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}

      - name: Deploy changed services
        run: |
          SERVICES=("user-service" "product-service" "order-service" "payment-service")
          CHANGES=("${{ needs.detect-changes.outputs.user-service }}" \
                   "${{ needs.detect-changes.outputs.product-service }}" \
                   "${{ needs.detect-changes.outputs.order-service }}" \
                   "${{ needs.detect-changes.outputs.payment-service }}")
          
          for i in "${!SERVICES[@]}"; do
            if [ "${CHANGES[$i]}" == "true" ]; then
              echo "🚀 Deploying ${SERVICES[$i]}..."
              kubectl set image deployment/${SERVICES[$i]} \
                ${SERVICES[$i]}=${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/${SERVICES[$i]}:${{ github.sha }} \
                -n microservices-staging
              kubectl rollout status deployment/${SERVICES[$i]} -n microservices-staging --timeout=300s
            fi
          done

  # ===========================================
  # DEPLOY TO PRODUCTION (Manual approval)
  # ===========================================
  deploy-production:
    needs: [detect-changes, deploy-staging]
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval in GitHub
    
    steps:
      - uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG_PRODUCTION }}

      - name: Deploy with Canary (10% traffic)
        run: |
          SERVICES=("user-service" "product-service" "order-service" "payment-service")
          CHANGES=("${{ needs.detect-changes.outputs.user-service }}" \
                   "${{ needs.detect-changes.outputs.product-service }}" \
                   "${{ needs.detect-changes.outputs.order-service }}" \
                   "${{ needs.detect-changes.outputs.payment-service }}")
          
          for i in "${!SERVICES[@]}"; do
            if [ "${CHANGES[$i]}" == "true" ]; then
              echo "🐤 Canary deploy ${SERVICES[$i]}..."
              
              # Update canary deployment (10% of pods)
              kubectl set image deployment/${SERVICES[$i]}-canary \
                ${SERVICES[$i]}=${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/${SERVICES[$i]}:${{ github.sha }} \
                -n microservices || true
            fi
          done

      - name: Monitor canary (5 minutes)
        run: |
          echo "⏳ Monitoring canary deployments for 5 minutes..."
          sleep 300
          
          # Check error rates via Prometheus
          # If error rate > 1%, fail and rollback

      - name: Promote to full deployment
        run: |
          SERVICES=("user-service" "product-service" "order-service" "payment-service")
          CHANGES=("${{ needs.detect-changes.outputs.user-service }}" \
                   "${{ needs.detect-changes.outputs.product-service }}" \
                   "${{ needs.detect-changes.outputs.order-service }}" \
                   "${{ needs.detect-changes.outputs.payment-service }}")
          
          for i in "${!SERVICES[@]}"; do
            if [ "${CHANGES[$i]}" == "true" ]; then
              echo "🚀 Full deploy ${SERVICES[$i]}..."
              kubectl set image deployment/${SERVICES[$i]} \
                ${SERVICES[$i]}=${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/${SERVICES[$i]}:${{ github.sha }} \
                -n microservices
              kubectl rollout status deployment/${SERVICES[$i]} -n microservices --timeout=300s
            fi
          done

      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "✅ Production deployment completed",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "Services deployed: user=${{ needs.detect-changes.outputs.user-service }}, product=${{ needs.detect-changes.outputs.product-service }}, order=${{ needs.detect-changes.outputs.order-service }}, payment=${{ needs.detect-changes.outputs.payment-service }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

#### Monorepo Dockerfile (with shared libs)

```dockerfile
# services/user-service/Dockerfile
# ===========================================
# MONOREPO DOCKERFILE
# ===========================================
# Must be built from the ROOT of the monorepo
# docker build -f services/user-service/Dockerfile .

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# Copy root package files
COPY package*.json ./
COPY nx.json ./
COPY tsconfig.base.json ./

# Copy service and libs
COPY services/user-service/package*.json ./services/user-service/
COPY libs/ ./libs/

RUN npm ci --workspace=services/user-service

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/services/user-service/node_modules ./services/user-service/node_modules
COPY . .

# Build shared libs first, then service
RUN npx nx build @libs/common
RUN npx nx build user-service

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nestjs

COPY --from=builder --chown=nestjs:nodejs /app/dist/services/user-service ./dist
COPY --from=builder --chown=nestjs:nodejs /app/node_modules ./node_modules

USER nestjs
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

---

### 📦 POLYREPO: Production Deployment Guide

#### Repository Structure

```
Organization GitHub:
├── user-service/              # github.com/myorg/user-service
│   ├── src/
│   ├── Dockerfile
│   ├── k8s/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── hpa.yaml
│   ├── .github/workflows/
│   │   └── ci-cd.yml
│   └── package.json
│
├── product-service/           # github.com/myorg/product-service
│   ├── src/
│   ├── Dockerfile
│   ├── k8s/
│   ├── .github/workflows/
│   └── package.json
│
├── order-service/             # github.com/myorg/order-service
├── payment-service/           # github.com/myorg/payment-service
│
├── shared-libs/               # github.com/myorg/shared-libs
│   ├── packages/
│   │   ├── common/            # @myorg/common (npm package)
│   │   ├── contracts/         # @myorg/contracts
│   │   └── database/          # @myorg/database
│   └── .github/workflows/
│       └── publish.yml        # Publishes to npm/GitHub Packages
│
└── k8s-infrastructure/        # github.com/myorg/k8s-infrastructure (GitOps)
    ├── clusters/
    │   ├── staging/
    │   │   ├── user-service/
    │   │   ├── product-service/
    │   │   └── ...
    │   └── production/
    └── .github/workflows/
        └── sync.yml           # ArgoCD sync
```

#### CI/CD Pipeline for Individual Service (Polyrepo)

```yaml
# user-service/.github/workflows/ci-cd.yml
name: User Service CI/CD

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  SERVICE_NAME: user-service
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ===========================================
  # TEST
  # ===========================================
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

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

      - name: Unit Tests
        run: npm run test:cov

      - name: Integration Tests
        run: npm run test:e2e
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  # ===========================================
  # BUILD & PUSH
  # ===========================================
  build:
    needs: test
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    
    permissions:
      contents: read
      packages: write
    
    outputs:
      image-tag: ${{ steps.meta.outputs.version }}
      image-digest: ${{ steps.build.outputs.digest }}

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Sign image
        run: |
          cosign sign --yes ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ steps.build.outputs.digest }}

  # ===========================================
  # UPDATE GITOPS REPO (Trigger ArgoCD)
  # ===========================================
  update-manifests:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout k8s-infrastructure repo
        uses: actions/checkout@v4
        with:
          repository: myorg/k8s-infrastructure
          token: ${{ secrets.GITOPS_TOKEN }}
          path: infra

      - name: Update staging manifest
        run: |
          cd infra/clusters/staging/${{ env.SERVICE_NAME }}
          
          # Update image tag in kustomization.yaml
          yq eval '.images[0].newTag = "${{ needs.build.outputs.image-tag }}"' \
            -i kustomization.yaml
          
          # Or update deployment directly
          yq eval '.spec.template.spec.containers[0].image = "${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ needs.build.outputs.image-tag }}"' \
            -i deployment.yaml

      - name: Commit and push
        run: |
          cd infra
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add .
          git commit -m "chore(${{ env.SERVICE_NAME }}): update staging to ${{ needs.build.outputs.image-tag }}"
          git push

  # ===========================================
  # DEPLOY TO STAGING (ArgoCD auto-syncs)
  # ===========================================
  wait-for-staging:
    needs: update-manifests
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
      - name: Wait for ArgoCD sync
        run: |
          # ArgoCD will automatically detect the change and deploy
          # Wait for the deployment to complete
          
          # Option 1: Use ArgoCD CLI
          argocd app wait ${{ env.SERVICE_NAME }}-staging --timeout 300
          
          # Option 2: Use kubectl
          # kubectl rollout status deployment/${{ env.SERVICE_NAME }} -n staging --timeout=300s

      - name: Run smoke tests
        run: |
          # Hit staging endpoints to verify deployment
          curl -f https://staging-api.myapp.com/users/health || exit 1

  # ===========================================
  # PROMOTE TO PRODUCTION
  # ===========================================
  promote-to-production:
    needs: [build, wait-for-staging]
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval
    
    steps:
      - name: Checkout k8s-infrastructure repo
        uses: actions/checkout@v4
        with:
          repository: myorg/k8s-infrastructure
          token: ${{ secrets.GITOPS_TOKEN }}
          path: infra

      - name: Update production manifest
        run: |
          cd infra/clusters/production/${{ env.SERVICE_NAME }}
          
          yq eval '.images[0].newTag = "${{ needs.build.outputs.image-tag }}"' \
            -i kustomization.yaml

      - name: Commit and push
        run: |
          cd infra
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add .
          git commit -m "chore(${{ env.SERVICE_NAME }}): promote to production ${{ needs.build.outputs.image-tag }}"
          git push

      - name: Wait for production sync
        run: |
          argocd app wait ${{ env.SERVICE_NAME }}-production --timeout 300

      - name: Notify team
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "✅ ${{ env.SERVICE_NAME }} deployed to production: ${{ needs.build.outputs.image-tag }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

#### Shared Libraries (Published to npm)

```yaml
# shared-libs/.github/workflows/publish.yml
name: Publish Shared Libraries

on:
  push:
    branches: [main]
    paths:
      - 'packages/**'
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://npm.pkg.github.com'

      - name: Install dependencies
        run: npm ci

      - name: Build all packages
        run: npm run build --workspaces

      - name: Publish packages
        run: |
          for package in packages/*; do
            if [ -f "$package/package.json" ]; then
              cd $package
              npm publish --access restricted
              cd ../..
            fi
          done
        env:
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### Polyrepo Dockerfile (with npm packages)

```dockerfile
# user-service/Dockerfile
# ===========================================
# POLYREPO DOCKERFILE
# ===========================================
# Uses published npm packages for shared code

FROM node:20-alpine AS deps
WORKDIR /app

# Configure private npm registry for @myorg packages
COPY .npmrc ./
COPY package*.json ./

# Install dependencies (including @myorg/common, @myorg/contracts)
ARG NPM_TOKEN
RUN echo "//npm.pkg.github.com/:_authToken=${NPM_TOKEN}" >> .npmrc && \
    npm ci && \
    rm -f .npmrc

# Build
FROM node:20-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production
FROM node:20-alpine AS runner
WORKDIR /app

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nestjs

# Only copy production dependencies
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder --chown=nestjs:nodejs /app/dist ./dist
COPY --from=builder /app/package.json ./

USER nestjs
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/main.js"]
```

---

### 🔄 GitOps with ArgoCD

#### ArgoCD Application Manifest

```yaml
# k8s-infrastructure/argocd/apps/user-service-staging.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: user-service-staging
  namespace: argocd
spec:
  project: default
  
  source:
    repoURL: https://github.com/myorg/k8s-infrastructure.git
    targetRevision: HEAD
    path: clusters/staging/user-service
  
  destination:
    server: https://kubernetes.default.svc
    namespace: staging
  
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

---
# Production (manual sync for safety)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: user-service-production
  namespace: argocd
spec:
  project: default
  
  source:
    repoURL: https://github.com/myorg/k8s-infrastructure.git
    targetRevision: HEAD
    path: clusters/production/user-service
  
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  
  syncPolicy:
    # NO automated sync for production
    syncOptions:
      - CreateNamespace=true
```

#### Kustomize Structure

```yaml
# k8s-infrastructure/clusters/staging/user-service/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: staging

resources:
  - ../../../base/user-service

images:
  - name: user-service
    newName: ghcr.io/myorg/user-service
    newTag: abc1234  # Updated by CI/CD

configMapGenerator:
  - name: user-service-config
    behavior: merge
    literals:
      - NODE_ENV=staging
      - LOG_LEVEL=debug

replicas:
  - name: user-service
    count: 2
```

---

### 📊 Comparison Summary

| Aspect | Monorepo | Polyrepo |
|--------|----------|----------|
| **Initial Setup** | Harder (Nx/Turborepo config) | Easier (standard repos) |
| **Code Sharing** | Easy (direct imports) | Harder (publish packages) |
| **CI/CD Complexity** | Complex (change detection) | Simple (per-repo) |
| **Build Time** | Can be slow (cache helps) | Fast (only one service) |
| **Atomic Changes** | ✅ Yes (single PR) | ❌ No (multiple PRs) |
| **Team Autonomy** | Lower | Higher |
| **Best For** | Small-medium teams, shared ownership | Large orgs, team-per-service |
| **Examples** | Google, Meta | Netflix, Amazon |

---

### 🎯 Deployment Flow Diagram

```
                            MONOREPO FLOW
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   Developer pushes to main                                              │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────────┐                                                   │
│   │ Detect Changes  │ ◄─── Which services/libs changed?                 │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────┐                                                   │
│   │  Test Changed   │ ◄─── Only test affected services                  │
│   │    Services     │                                                   │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────┐                                                   │
│   │ Build & Push    │ ◄─── Build Docker images for changed only         │
│   │  Docker Images  │                                                   │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────┐      ┌─────────────────┐                         │
│   │ Deploy Staging  │ ───► │ Deploy Production│ ◄─── Manual approval   │
│   └─────────────────┘      └─────────────────┘                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘


                            POLYREPO FLOW
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   Developer pushes to user-service repo                                 │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────────┐                                                   │
│   │  Test Service   │ ◄─── Simple: test this repo only                  │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────┐                                                   │
│   │ Build & Push    │ ◄─── One Docker image                             │
│   │  Docker Image   │                                                   │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────┐                                                   │
│   │ Update GitOps   │ ◄─── Push new image tag to k8s-infrastructure    │
│   │  Repository     │                                                   │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────┐      ┌─────────────────┐                         │
│   │ ArgoCD Syncs    │ ───► │ ArgoCD Syncs    │ ◄─── Manual approval    │
│   │   Staging       │      │   Production    │                          │
│   └─────────────────┘      └─────────────────┘                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Architecture Overview

### High-Level Architecture

```
                         ┌─────────────────────────────────────────────────────────────┐
                         │                        INTERNET                             │
                         └─────────────────────────────┬───────────────────────────────┘
                                                       │
                                                       ▼
                         ┌─────────────────────────────────────────────────────────────┐
                         │                     LOAD BALANCER                           │
                         │                  (AWS ALB / Nginx / Traefik)                │
                         └─────────────────────────────┬───────────────────────────────┘
                                                       │
                                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         API GATEWAY                                              │
│                              (Kong / Traefik / Custom NestJS)                                    │
│                                                                                                  │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│   │  Rate Limiting  │  │ Authentication  │  │  Request        │  │    Logging &    │            │
│   │                 │  │  & JWT Verify   │  │  Routing        │  │    Metrics      │            │
│   └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘            │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                       │
            ┌──────────────────────────────────────────┼──────────────────────────────────────────┐
            │                                          │                                          │
            ▼                                          ▼                                          ▼
┌─────────────────────┐                   ┌─────────────────────┐                   ┌─────────────────────┐
│    USER SERVICE     │                   │   PRODUCT SERVICE   │                   │   ORDER SERVICE     │
│                     │                   │                     │                   │                     │
│  • Registration     │                   │  • CRUD Operations  │                   │  • Order Creation   │
│  • Authentication   │                   │  • Search/Filter    │                   │  • Order Tracking   │
│  • Profile Mgmt     │                   │  • Inventory        │                   │  • Order History    │
│  • Permissions      │                   │  • Categories       │                   │  • Cart Management  │
└──────────┬──────────┘                   └──────────┬──────────┘                   └──────────┬──────────┘
           │                                         │                                         │
           ▼                                         ▼                                         ▼
┌─────────────────────┐                   ┌─────────────────────┐                   ┌─────────────────────┐
│     PostgreSQL      │                   │      MongoDB        │                   │      MongoDB        │
│   (User Database)   │                   │ (Product Database)  │                   │  (Order Database)   │
└─────────────────────┘                   └─────────────────────┘                   └─────────────────────┘

            ┌──────────────────────────────────────────┼──────────────────────────────────────────┐
            │                                          │                                          │
            ▼                                          ▼                                          ▼
┌─────────────────────┐                   ┌─────────────────────┐                   ┌─────────────────────┐
│  PAYMENT SERVICE    │                   │NOTIFICATION SERVICE │                   │  SHIPPING SERVICE   │
│                     │                   │                     │                   │                     │
│  • Process Payment  │                   │  • Email            │                   │  • Create Shipment  │
│  • Refunds          │                   │  • SMS              │                   │  • Track Package    │
│  • Transaction Logs │                   │  • Push Notify      │                   │  • Delivery Updates │
└──────────┬──────────┘                   └──────────┬──────────┘                   └──────────┬──────────┘
           │                                         │                                         │
           ▼                                         ▼                                         ▼
┌─────────────────────┐                   ┌─────────────────────┐                   ┌─────────────────────┐
│     PostgreSQL      │                   │       Redis         │                   │     PostgreSQL      │
│ (Payment Database)  │                   │   (Queue/Cache)     │                   │(Shipping Database)  │
└─────────────────────┘                   └─────────────────────┘                   └─────────────────────┘

                         ┌─────────────────────────────────────────────────────────────┐
                         │                    MESSAGE BROKER                           │
                         │               (RabbitMQ / Apache Kafka)                     │
                         │                                                             │
                         │  Events: order_created, payment_completed,                  │
                         │          inventory_updated, user_registered                 │
                         └─────────────────────────────────────────────────────────────┘
```

### Core Principles

| Principle | Description |
|-----------|-------------|
| **Single Responsibility** | Each service handles ONE business capability |
| **Loose Coupling** | Services are independent and communicate via APIs |
| **High Cohesion** | Related functionality is grouped within a service |
| **Database Per Service** | Each service owns its data exclusively |
| **Decentralized Governance** | Teams choose their own tech stack |
| **Design for Failure** | Assume things will break and plan accordingly |
| **Infrastructure Automation** | Everything as code (IaC) |

---

## 🛠️ Technology Stack

### Recommended Production Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend Framework** | NestJS / Node.js | Service development |
| **Language** | TypeScript | Type safety & maintainability |
| **API Protocol** | REST / gRPC | Synchronous communication |
| **Message Broker** | RabbitMQ / Kafka | Asynchronous communication |
| **Databases** | PostgreSQL, MongoDB, Redis | Data persistence & caching |
| **Container Runtime** | Docker | Application packaging |
| **Orchestration** | Kubernetes | Container orchestration |
| **Service Mesh** | Istio / Linkerd | Service-to-service security |
| **API Gateway** | Kong / Traefik | Traffic management |
| **CI/CD** | GitHub Actions / GitLab CI | Automation pipeline |
| **Monitoring** | Prometheus + Grafana | Metrics & visualization |
| **Logging** | ELK Stack / Loki | Centralized logging |
| **Tracing** | Jaeger / Zipkin | Distributed tracing |
| **Secrets** | HashiCorp Vault / AWS Secrets Manager | Secret management |
| **Infrastructure** | Terraform | Infrastructure as Code |

---

## 📁 Project Structure

### Monorepo Structure (Recommended for Teams)

```
microservices-platform/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # CI pipeline
│       ├── cd-staging.yml            # Deploy to staging
│       └── cd-production.yml         # Deploy to production
├── docker/
│   ├── docker-compose.yml            # Local development
│   ├── docker-compose.prod.yml       # Production compose
│   └── docker-compose.test.yml       # Testing environment
├── k8s/
│   ├── base/                         # Base Kubernetes configs
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   └── secrets.yaml
│   ├── services/
│   │   ├── user-service/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   ├── hpa.yaml
│   │   │   └── ingress.yaml
│   │   ├── product-service/
│   │   ├── order-service/
│   │   └── ...
│   ├── overlays/
│   │   ├── staging/
│   │   └── production/
│   └── helm/
│       └── microservices-chart/
├── services/
│   ├── api-gateway/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── user-service/
│   │   ├── src/
│   │   │   ├── main.ts
│   │   │   ├── app.module.ts
│   │   │   ├── users/
│   │   │   │   ├── users.module.ts
│   │   │   │   ├── users.controller.ts
│   │   │   │   ├── users.service.ts
│   │   │   │   ├── dto/
│   │   │   │   │   ├── create-user.dto.ts
│   │   │   │   │   └── update-user.dto.ts
│   │   │   │   └── entities/
│   │   │   │       └── user.entity.ts
│   │   │   ├── auth/
│   │   │   └── health/
│   │   ├── test/
│   │   ├── Dockerfile
│   │   └── package.json
│   ├── product-service/
│   ├── order-service/
│   ├── payment-service/
│   ├── notification-service/
│   └── shipping-service/
├── libs/
│   ├── common/                       # Shared utilities
│   │   ├── src/
│   │   │   ├── decorators/
│   │   │   ├── filters/
│   │   │   ├── guards/
│   │   │   ├── interceptors/
│   │   │   └── pipes/
│   │   └── package.json
│   ├── contracts/                    # API contracts/schemas
│   └── proto/                        # gRPC proto files
├── scripts/
│   ├── setup-local.sh
│   ├── run-migrations.sh
│   └── seed-data.sh
├── docs/
│   ├── architecture/
│   ├── api/
│   └── runbooks/
├── terraform/
│   ├── modules/
│   ├── environments/
│   │   ├── staging/
│   │   └── production/
│   └── main.tf
├── .env.example
├── package.json                      # Root package.json (workspace)
├── nx.json                           # Nx monorepo config
└── README.md
```

### Individual Service Structure

```
user-service/
├── src/
│   ├── main.ts                       # Entry point
│   ├── app.module.ts                 # Root module
│   ├── config/
│   │   ├── configuration.ts          # Environment config
│   │   └── validation.schema.ts      # Config validation
│   ├── common/
│   │   ├── decorators/
│   │   ├── filters/
│   │   │   └── http-exception.filter.ts
│   │   ├── guards/
│   │   │   └── jwt-auth.guard.ts
│   │   ├── interceptors/
│   │   │   └── logging.interceptor.ts
│   │   └── pipes/
│   │       └── validation.pipe.ts
│   ├── users/
│   │   ├── users.module.ts
│   │   ├── users.controller.ts
│   │   ├── users.service.ts
│   │   ├── users.repository.ts
│   │   ├── dto/
│   │   │   ├── create-user.dto.ts
│   │   │   ├── update-user.dto.ts
│   │   │   └── user-response.dto.ts
│   │   ├── entities/
│   │   │   └── user.entity.ts
│   │   ├── interfaces/
│   │   │   └── user.interface.ts
│   │   └── __tests__/
│   │       ├── users.controller.spec.ts
│   │       └── users.service.spec.ts
│   ├── auth/
│   │   ├── auth.module.ts
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── strategies/
│   │   │   ├── jwt.strategy.ts
│   │   │   └── local.strategy.ts
│   │   └── dto/
│   │       ├── login.dto.ts
│   │       └── register.dto.ts
│   ├── health/
│   │   ├── health.module.ts
│   │   └── health.controller.ts
│   └── database/
│       ├── database.module.ts
│       └── migrations/
├── test/
│   ├── app.e2e-spec.ts
│   └── jest-e2e.json
├── Dockerfile
├── Dockerfile.dev
├── .dockerignore
├── package.json
├── tsconfig.json
├── tsconfig.build.json
├── nest-cli.json
├── .env.example
└── README.md
```

---

## 🎨 Service Design Patterns

### 1. Module Pattern (NestJS)

```typescript
// users.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { UsersRepository } from './users.repository';
import { User } from './entities/user.entity';

@Module({
  imports: [
    TypeOrmModule.forFeature([User]),
  ],
  controllers: [UsersController],
  providers: [UsersService, UsersRepository],
  exports: [UsersService], // Export for other modules
})
export class UsersModule {}
```

### 2. Repository Pattern

```typescript
// users.repository.ts
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './entities/user.entity';

@Injectable()
export class UsersRepository {
  constructor(
    @InjectRepository(User)
    private readonly repo: Repository<User>,
  ) {}

  async findById(id: string): Promise<User | null> {
    return this.repo.findOne({ where: { id } });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.repo.findOne({ where: { email } });
  }

  async create(userData: Partial<User>): Promise<User> {
    const user = this.repo.create(userData);
    return this.repo.save(user);
  }

  async update(id: string, userData: Partial<User>): Promise<User> {
    await this.repo.update(id, userData);
    return this.findById(id);
  }

  async delete(id: string): Promise<void> {
    await this.repo.delete(id);
  }
}
```

### 3. DTO Pattern with Validation

```typescript
// dto/create-user.dto.ts
import { 
  IsEmail, 
  IsString, 
  MinLength, 
  MaxLength, 
  IsOptional,
  IsEnum,
  Matches 
} from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  MODERATOR = 'moderator',
}

export class CreateUserDto {
  @ApiProperty({ example: 'john@example.com' })
  @IsEmail({}, { message: 'Please provide a valid email address' })
  email: string;

  @ApiProperty({ example: 'John Doe' })
  @IsString()
  @MinLength(2, { message: 'Name must be at least 2 characters' })
  @MaxLength(100, { message: 'Name cannot exceed 100 characters' })
  name: string;

  @ApiProperty({ example: 'SecureP@ss123' })
  @IsString()
  @MinLength(8, { message: 'Password must be at least 8 characters' })
  @Matches(
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$/,
    { message: 'Password must contain uppercase, lowercase, number and special character' }
  )
  password: string;

  @ApiProperty({ enum: UserRole, default: UserRole.USER })
  @IsOptional()
  @IsEnum(UserRole)
  role?: UserRole = UserRole.USER;
}
```

### 4. Entity Pattern with TypeORM

```typescript
// entities/user.entity.ts
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  Index,
  BeforeInsert,
  BeforeUpdate,
} from 'typeorm';
import * as bcrypt from 'bcrypt';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Index({ unique: true })
  @Column({ length: 255 })
  email: string;

  @Column({ length: 100 })
  name: string;

  @Column({ select: false }) // Don't return password by default
  password: string;

  @Column({ type: 'enum', enum: ['admin', 'user', 'moderator'], default: 'user' })
  role: string;

  @Column({ default: true })
  isActive: boolean;

  @Column({ nullable: true })
  lastLoginAt: Date;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @BeforeInsert()
  @BeforeUpdate()
  async hashPassword() {
    if (this.password) {
      this.password = await bcrypt.hash(this.password, 10);
    }
  }

  async validatePassword(password: string): Promise<boolean> {
    return bcrypt.compare(password, this.password);
  }
}
```

### 5. Service Layer Pattern

```typescript
// users.service.ts
import { 
  Injectable, 
  NotFoundException, 
  ConflictException,
  Logger 
} from '@nestjs/common';
import { UsersRepository } from './users.repository';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { User } from './entities/user.entity';
import { EventEmitter2 } from '@nestjs/event-emitter';

@Injectable()
export class UsersService {
  private readonly logger = new Logger(UsersService.name);

  constructor(
    private readonly usersRepository: UsersRepository,
    private readonly eventEmitter: EventEmitter2,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<User> {
    // Check if user already exists
    const existingUser = await this.usersRepository.findByEmail(createUserDto.email);
    if (existingUser) {
      throw new ConflictException('User with this email already exists');
    }

    // Create user
    const user = await this.usersRepository.create(createUserDto);
    
    // Emit event for other services
    this.eventEmitter.emit('user.created', {
      userId: user.id,
      email: user.email,
      name: user.name,
    });

    this.logger.log(`User created: ${user.id}`);
    return user;
  }

  async findById(id: string): Promise<User> {
    const user = await this.usersRepository.findById(id);
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    return user;
  }

  async update(id: string, updateUserDto: UpdateUserDto): Promise<User> {
    await this.findById(id); // Verify user exists
    return this.usersRepository.update(id, updateUserDto);
  }

  async delete(id: string): Promise<void> {
    await this.findById(id); // Verify user exists
    await this.usersRepository.delete(id);
    
    this.eventEmitter.emit('user.deleted', { userId: id });
    this.logger.log(`User deleted: ${id}`);
  }
}
```

### 6. Controller Pattern with Swagger

```typescript
// users.controller.ts
import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Body,
  Param,
  Query,
  UseGuards,
  HttpStatus,
  ParseUUIDPipe,
} from '@nestjs/common';
import {
  ApiTags,
  ApiOperation,
  ApiResponse,
  ApiBearerAuth,
  ApiParam,
  ApiQuery,
} from '@nestjs/swagger';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { UserResponseDto } from './dto/user-response.dto';

@ApiTags('Users')
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  @ApiOperation({ summary: 'Create a new user' })
  @ApiResponse({ status: HttpStatus.CREATED, type: UserResponseDto })
  @ApiResponse({ status: HttpStatus.CONFLICT, description: 'User already exists' })
  async create(@Body() createUserDto: CreateUserDto): Promise<UserResponseDto> {
    return this.usersService.create(createUserDto);
  }

  @Get(':id')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Get user by ID' })
  @ApiParam({ name: 'id', type: 'string', format: 'uuid' })
  @ApiResponse({ status: HttpStatus.OK, type: UserResponseDto })
  @ApiResponse({ status: HttpStatus.NOT_FOUND, description: 'User not found' })
  async findOne(
    @Param('id', ParseUUIDPipe) id: string,
  ): Promise<UserResponseDto> {
    return this.usersService.findById(id);
  }

  @Put(':id')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Update user' })
  async update(
    @Param('id', ParseUUIDPipe) id: string,
    @Body() updateUserDto: UpdateUserDto,
  ): Promise<UserResponseDto> {
    return this.usersService.update(id, updateUserDto);
  }

  @Delete(':id')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Delete user (Admin only)' })
  async delete(@Param('id', ParseUUIDPipe) id: string): Promise<void> {
    return this.usersService.delete(id);
  }
}
```

---

## 📡 Inter-Service Communication

### Synchronous Communication (HTTP/REST)

```typescript
// http-client.service.ts
import { Injectable, HttpException, Logger } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { ConfigService } from '@nestjs/config';
import { firstValueFrom, timeout, retry, catchError } from 'rxjs';
import { AxiosError } from 'axios';

@Injectable()
export class HttpClientService {
  private readonly logger = new Logger(HttpClientService.name);

  constructor(
    private readonly httpService: HttpService,
    private readonly configService: ConfigService,
  ) {}

  async get<T>(serviceUrl: string, path: string): Promise<T> {
    const url = `${serviceUrl}${path}`;
    
    try {
      const response = await firstValueFrom(
        this.httpService.get<T>(url).pipe(
          timeout(5000), // 5 second timeout
          retry(3),      // Retry 3 times
          catchError((error: AxiosError) => {
            this.logger.error(`HTTP GET failed: ${url}`, error.message);
            throw new HttpException(
              error.response?.data || 'Service unavailable',
              error.response?.status || 503,
            );
          }),
        ),
      );
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async post<T, D>(serviceUrl: string, path: string, data: D): Promise<T> {
    const url = `${serviceUrl}${path}`;
    
    const response = await firstValueFrom(
      this.httpService.post<T>(url, data).pipe(
        timeout(10000),
        retry(2),
        catchError((error: AxiosError) => {
          this.logger.error(`HTTP POST failed: ${url}`, error.message);
          throw new HttpException(
            error.response?.data || 'Service unavailable',
            error.response?.status || 503,
          );
        }),
      ),
    );
    return response.data;
  }
}

// Usage in a service
@Injectable()
export class OrdersService {
  constructor(
    private readonly httpClient: HttpClientService,
    private readonly configService: ConfigService,
  ) {}

  async createOrder(orderData: CreateOrderDto) {
    const productServiceUrl = this.configService.get('PRODUCT_SERVICE_URL');
    
    // Verify product exists
    const product = await this.httpClient.get<Product>(
      productServiceUrl,
      `/products/${orderData.productId}`,
    );

    // Continue with order creation...
  }
}
```

### Asynchronous Communication (RabbitMQ)

```typescript
// rabbitmq.module.ts
import { Module } from '@nestjs/common';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { ConfigService } from '@nestjs/config';

@Module({
  imports: [
    ClientsModule.registerAsync([
      {
        name: 'ORDERS_SERVICE',
        useFactory: (configService: ConfigService) => ({
          transport: Transport.RMQ,
          options: {
            urls: [configService.get<string>('RABBITMQ_URL')],
            queue: 'orders_queue',
            queueOptions: {
              durable: true,
            },
          },
        }),
        inject: [ConfigService],
      },
      {
        name: 'NOTIFICATIONS_SERVICE',
        useFactory: (configService: ConfigService) => ({
          transport: Transport.RMQ,
          options: {
            urls: [configService.get<string>('RABBITMQ_URL')],
            queue: 'notifications_queue',
            queueOptions: {
              durable: true,
            },
          },
        }),
        inject: [ConfigService],
      },
    ]),
  ],
  exports: [ClientsModule],
})
export class RabbitMQModule {}
```

```typescript
// Event Publisher
import { Inject, Injectable } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';

@Injectable()
export class OrdersService {
  constructor(
    @Inject('NOTIFICATIONS_SERVICE') 
    private readonly notificationsClient: ClientProxy,
  ) {}

  async createOrder(orderData: CreateOrderDto) {
    // Save order to database
    const order = await this.ordersRepository.create(orderData);

    // Publish event (non-blocking)
    this.notificationsClient.emit('order_created', {
      orderId: order.id,
      customerId: order.customerId,
      total: order.total,
      items: order.items,
    });

    return order;
  }
}
```

```typescript
// Event Consumer (Notification Service)
import { Controller } from '@nestjs/common';
import { EventPattern, Payload, Ctx, RmqContext } from '@nestjs/microservices';

@Controller()
export class NotificationsController {
  @EventPattern('order_created')
  async handleOrderCreated(
    @Payload() data: OrderCreatedEvent,
    @Ctx() context: RmqContext,
  ) {
    const channel = context.getChannelRef();
    const originalMsg = context.getMessage();

    try {
      // Send email notification
      await this.emailService.sendOrderConfirmation({
        orderId: data.orderId,
        customerEmail: data.customerEmail,
      });

      // Acknowledge message
      channel.ack(originalMsg);
    } catch (error) {
      // Reject and requeue
      channel.nack(originalMsg, false, true);
    }
  }
}
```

### gRPC Communication (High Performance)

```protobuf
// proto/user.proto
syntax = "proto3";

package user;

service UserService {
  rpc GetUser (GetUserRequest) returns (UserResponse);
  rpc CreateUser (CreateUserRequest) returns (UserResponse);
  rpc UpdateUser (UpdateUserRequest) returns (UserResponse);
  rpc DeleteUser (DeleteUserRequest) returns (DeleteUserResponse);
}

message GetUserRequest {
  string id = 1;
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
  string password = 3;
}

message UpdateUserRequest {
  string id = 1;
  optional string email = 2;
  optional string name = 3;
}

message DeleteUserRequest {
  string id = 1;
}

message UserResponse {
  string id = 1;
  string email = 2;
  string name = 3;
  string role = 4;
  string createdAt = 5;
}

message DeleteUserResponse {
  bool success = 1;
}
```

```typescript
// gRPC Server (User Service)
// main.ts
import { NestFactory } from '@nestjs/core';
import { MicroserviceOptions, Transport } from '@nestjs/microservices';
import { join } from 'path';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.createMicroservice<MicroserviceOptions>(
    AppModule,
    {
      transport: Transport.GRPC,
      options: {
        package: 'user',
        protoPath: join(__dirname, './proto/user.proto'),
        url: '0.0.0.0:5000',
      },
    },
  );

  await app.listen();
  console.log('gRPC User Service is running on port 5000');
}
bootstrap();
```

```typescript
// gRPC Client (Order Service calling User Service)
import { Injectable, OnModuleInit } from '@nestjs/common';
import { Client, ClientGrpc, Transport } from '@nestjs/microservices';
import { join } from 'path';
import { Observable } from 'rxjs';

interface UserServiceClient {
  getUser(data: { id: string }): Observable<any>;
}

@Injectable()
export class UserGrpcService implements OnModuleInit {
  @Client({
    transport: Transport.GRPC,
    options: {
      package: 'user',
      protoPath: join(__dirname, './proto/user.proto'),
      url: 'user-service:5000',
    },
  })
  private client: ClientGrpc;

  private userService: UserServiceClient;

  onModuleInit() {
    this.userService = this.client.getService<UserServiceClient>('UserService');
  }

  async getUser(userId: string) {
    return this.userService.getUser({ id: userId }).toPromise();
  }
}
```

---

## 🗄️ Database Patterns

### Database-Per-Service Pattern

```yaml
# docker-compose.yml - Each service has its own database
version: '3.8'

services:
  user-service:
    build: ./services/user-service
    environment:
      DATABASE_URL: postgresql://user:pass@user-db:5432/users
    depends_on:
      - user-db

  user-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: users
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - user_data:/var/lib/postgresql/data

  product-service:
    build: ./services/product-service
    environment:
      MONGODB_URI: mongodb://product-db:27017/products
    depends_on:
      - product-db

  product-db:
    image: mongo:6
    volumes:
      - product_data:/data/db

  order-service:
    build: ./services/order-service
    environment:
      DATABASE_URL: postgresql://order:pass@order-db:5432/orders
    depends_on:
      - order-db

  order-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: orders
      POSTGRES_USER: order
      POSTGRES_PASSWORD: pass
    volumes:
      - order_data:/var/lib/postgresql/data

volumes:
  user_data:
  product_data:
  order_data:
```

### Saga Pattern Implementation

```typescript
// saga/order-saga.orchestrator.ts
import { Injectable, Logger } from '@nestjs/common';
import { EventEmitter2 } from '@nestjs/event-emitter';

interface SagaStep {
  name: string;
  execute: () => Promise<void>;
  compensate: () => Promise<void>;
}

interface OrderSagaData {
  orderId: string;
  customerId: string;
  items: Array<{ productId: string; quantity: number; price: number }>;
  totalAmount: number;
  paymentMethod: string;
  shippingAddress: string;
}

@Injectable()
export class OrderSagaOrchestrator {
  private readonly logger = new Logger(OrderSagaOrchestrator.name);

  constructor(
    private readonly inventoryService: InventoryServiceClient,
    private readonly paymentService: PaymentServiceClient,
    private readonly shippingService: ShippingServiceClient,
    private readonly eventEmitter: EventEmitter2,
  ) {}

  async execute(data: OrderSagaData): Promise<SagaResult> {
    const completedSteps: string[] = [];
    const sagaId = `saga-${data.orderId}-${Date.now()}`;

    this.logger.log(`Starting order saga: ${sagaId}`);

    const steps: SagaStep[] = [
      {
        name: 'RESERVE_INVENTORY',
        execute: async () => {
          await this.inventoryService.reserveItems({
            orderId: data.orderId,
            items: data.items,
          });
        },
        compensate: async () => {
          await this.inventoryService.releaseItems({
            orderId: data.orderId,
          });
        },
      },
      {
        name: 'PROCESS_PAYMENT',
        execute: async () => {
          await this.paymentService.charge({
            orderId: data.orderId,
            customerId: data.customerId,
            amount: data.totalAmount,
            method: data.paymentMethod,
          });
        },
        compensate: async () => {
          await this.paymentService.refund({
            orderId: data.orderId,
          });
        },
      },
      {
        name: 'CREATE_SHIPMENT',
        execute: async () => {
          await this.shippingService.createShipment({
            orderId: data.orderId,
            items: data.items,
            address: data.shippingAddress,
          });
        },
        compensate: async () => {
          await this.shippingService.cancelShipment({
            orderId: data.orderId,
          });
        },
      },
    ];

    try {
      for (const step of steps) {
        this.logger.log(`Executing step: ${step.name}`);
        await step.execute();
        completedSteps.push(step.name);
        this.logger.log(`Completed step: ${step.name}`);
      }

      this.eventEmitter.emit('saga.completed', {
        sagaId,
        orderId: data.orderId,
        status: 'SUCCESS',
      });

      return {
        success: true,
        orderId: data.orderId,
        status: 'CONFIRMED',
      };
    } catch (error) {
      this.logger.error(`Saga failed at step: ${error.step}`, error.message);
      
      // Run compensations in reverse order
      await this.compensate(steps, completedSteps, data.orderId);

      this.eventEmitter.emit('saga.failed', {
        sagaId,
        orderId: data.orderId,
        failedStep: error.step,
        error: error.message,
      });

      return {
        success: false,
        orderId: data.orderId,
        status: 'CANCELLED',
        reason: error.message,
      };
    }
  }

  private async compensate(
    steps: SagaStep[],
    completedSteps: string[],
    orderId: string,
  ): Promise<void> {
    const stepsToCompensate = steps
      .filter((step) => completedSteps.includes(step.name))
      .reverse();

    for (const step of stepsToCompensate) {
      try {
        this.logger.log(`Compensating step: ${step.name}`);
        await step.compensate();
        this.logger.log(`Compensation completed: ${step.name}`);
      } catch (compensationError) {
        this.logger.error(
          `Compensation failed for ${step.name}`,
          compensationError.message,
        );
        // Alert operations team for manual intervention
        await this.alertOpsTeam(orderId, step.name, compensationError);
      }
    }
  }

  private async alertOpsTeam(
    orderId: string,
    step: string,
    error: Error,
  ): Promise<void> {
    // Send alert to PagerDuty/Slack/etc.
    this.eventEmitter.emit('saga.compensation.failed', {
      orderId,
      step,
      error: error.message,
      requiresManualIntervention: true,
    });
  }
}
```

### Event Sourcing Pattern

```typescript
// event-store/event-store.service.ts
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { EventStore } from './entities/event-store.entity';

@Injectable()
export class EventStoreService {
  constructor(
    @InjectRepository(EventStore)
    private readonly eventStoreRepository: Repository<EventStore>,
  ) {}

  async appendEvent(
    aggregateId: string,
    aggregateType: string,
    eventType: string,
    eventData: any,
    version: number,
  ): Promise<EventStore> {
    const event = this.eventStoreRepository.create({
      aggregateId,
      aggregateType,
      eventType,
      eventData,
      version,
      timestamp: new Date(),
    });

    return this.eventStoreRepository.save(event);
  }

  async getEvents(
    aggregateId: string,
    fromVersion: number = 0,
  ): Promise<EventStore[]> {
    return this.eventStoreRepository.find({
      where: {
        aggregateId,
        version: MoreThan(fromVersion),
      },
      order: { version: 'ASC' },
    });
  }

  async replayEvents(aggregateId: string): Promise<any> {
    const events = await this.getEvents(aggregateId);
    let state = {};

    for (const event of events) {
      state = this.applyEvent(state, event);
    }

    return state;
  }

  private applyEvent(state: any, event: EventStore): any {
    switch (event.eventType) {
      case 'OrderCreated':
        return { ...state, ...event.eventData, status: 'CREATED' };
      case 'OrderPaid':
        return { ...state, status: 'PAID', paidAt: event.timestamp };
      case 'OrderShipped':
        return { ...state, status: 'SHIPPED', shippedAt: event.timestamp };
      case 'OrderDelivered':
        return { ...state, status: 'DELIVERED', deliveredAt: event.timestamp };
      default:
        return state;
    }
  }
}
```

---

## 🚪 API Gateway

### Kong Gateway Configuration

```yaml
# kong.yml - Declarative configuration
_format_version: "3.0"

services:
  - name: user-service
    url: http://user-service:3000
    routes:
      - name: user-routes
        paths:
          - /api/users
        strip_path: false
    plugins:
      - name: rate-limiting
        config:
          minute: 100
          policy: local
      - name: jwt
        config:
          secret_is_base64: false

  - name: product-service
    url: http://product-service:3001
    routes:
      - name: product-routes
        paths:
          - /api/products
        strip_path: false
    plugins:
      - name: rate-limiting
        config:
          minute: 500
      - name: proxy-cache
        config:
          response_code:
            - 200
          request_method:
            - GET
          content_type:
            - application/json
          cache_ttl: 300

  - name: order-service
    url: http://order-service:3002
    routes:
      - name: order-routes
        paths:
          - /api/orders
        strip_path: false
    plugins:
      - name: jwt
      - name: rate-limiting
        config:
          minute: 50

plugins:
  - name: correlation-id
    config:
      header_name: X-Correlation-ID
      generator: uuid
      echo_downstream: true

  - name: prometheus
    config:
      per_consumer: true

consumers:
  - username: mobile-app
    custom_id: mobile-app-client
    jwt_secrets:
      - key: mobile-app-key
        algorithm: HS256

  - username: web-app
    custom_id: web-app-client
```

### Custom NestJS Gateway

```typescript
// api-gateway/src/main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import helmet from 'helmet';
import * as compression from 'compression';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Security
  app.use(helmet());
  app.enableCors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
    credentials: true,
  });

  // Compression
  app.use(compression());

  // Validation
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  );

  // Swagger
  const config = new DocumentBuilder()
    .setTitle('Microservices API Gateway')
    .setDescription('Unified API Gateway for all microservices')
    .setVersion('1.0')
    .addBearerAuth()
    .build();

  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('docs', app, document);

  await app.listen(process.env.PORT || 8080);
}
bootstrap();
```

```typescript
// api-gateway/src/gateway/gateway.controller.ts
import {
  Controller,
  All,
  Req,
  Res,
  UseGuards,
  UseInterceptors,
} from '@nestjs/common';
import { Request, Response } from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { RateLimitGuard } from '../guards/rate-limit.guard';
import { LoggingInterceptor } from '../interceptors/logging.interceptor';
import { ConfigService } from '@nestjs/config';

@Controller()
@UseInterceptors(LoggingInterceptor)
export class GatewayController {
  private serviceMap: Map<string, string>;

  constructor(private readonly configService: ConfigService) {
    this.serviceMap = new Map([
      ['users', this.configService.get('USER_SERVICE_URL')],
      ['products', this.configService.get('PRODUCT_SERVICE_URL')],
      ['orders', this.configService.get('ORDER_SERVICE_URL')],
      ['payments', this.configService.get('PAYMENT_SERVICE_URL')],
    ]);
  }

  @All('api/:service/*')
  @UseGuards(JwtAuthGuard, RateLimitGuard)
  async proxy(@Req() req: Request, @Res() res: Response) {
    const service = req.params.service;
    const targetUrl = this.serviceMap.get(service);

    if (!targetUrl) {
      return res.status(404).json({ error: 'Service not found' });
    }

    const proxy = createProxyMiddleware({
      target: targetUrl,
      changeOrigin: true,
      pathRewrite: {
        [`^/api/${service}`]: '',
      },
      onProxyReq: (proxyReq, req) => {
        // Add correlation ID
        const correlationId = req.headers['x-correlation-id'] || uuidv4();
        proxyReq.setHeader('X-Correlation-ID', correlationId);
        
        // Add user info from JWT
        if (req.user) {
          proxyReq.setHeader('X-User-ID', req.user.id);
          proxyReq.setHeader('X-User-Role', req.user.role);
        }
      },
      onError: (err, req, res) => {
        res.status(503).json({
          error: 'Service temporarily unavailable',
          service,
        });
      },
    });

    return proxy(req, res, () => {});
  }
}
```

---

## 🔍 Service Discovery

### Kubernetes DNS (Built-in)

```yaml
# k8s/services/user-service/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: user-service  # This becomes the DNS name!
  namespace: microservices
  labels:
    app: user-service
spec:
  selector:
    app: user-service
  ports:
    - port: 80
      targetPort: 3000
      protocol: TCP
  type: ClusterIP
---
# Any pod in the cluster can now call:
# http://user-service.microservices.svc.cluster.local
# or simply: http://user-service (within same namespace)
```

### Consul Service Discovery

```typescript
// consul/consul.module.ts
import { Module, Global } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import Consul from 'consul';

@Global()
@Module({
  imports: [ConfigModule],
  providers: [
    {
      provide: 'CONSUL_CLIENT',
      useFactory: (configService: ConfigService) => {
        return new Consul({
          host: configService.get('CONSUL_HOST', 'localhost'),
          port: configService.get('CONSUL_PORT', '8500'),
        });
      },
      inject: [ConfigService],
    },
  ],
  exports: ['CONSUL_CLIENT'],
})
export class ConsulModule {}
```

```typescript
// consul/consul.service.ts
import { Injectable, Inject, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import Consul from 'consul';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class ConsulService implements OnModuleInit, OnModuleDestroy {
  private serviceId: string;
  private serviceName: string;
  private servicePort: number;
  private checkInterval: NodeJS.Timer;

  constructor(
    @Inject('CONSUL_CLIENT') private readonly consul: Consul,
    private readonly configService: ConfigService,
  ) {
    this.serviceName = this.configService.get('SERVICE_NAME');
    this.servicePort = this.configService.get('PORT');
    this.serviceId = `${this.serviceName}-${uuidv4()}`;
  }

  async onModuleInit() {
    await this.register();
  }

  async onModuleDestroy() {
    await this.deregister();
  }

  private async register() {
    const registration = {
      id: this.serviceId,
      name: this.serviceName,
      port: this.servicePort,
      check: {
        http: `http://localhost:${this.servicePort}/health`,
        interval: '10s',
        timeout: '5s',
        deregistercriticalserviceafter: '1m',
      },
      tags: ['microservice', 'nestjs'],
    };

    await this.consul.agent.service.register(registration);
    console.log(`Service registered: ${this.serviceId}`);
  }

  private async deregister() {
    await this.consul.agent.service.deregister(this.serviceId);
    console.log(`Service deregistered: ${this.serviceId}`);
  }

  async discoverService(serviceName: string): Promise<string[]> {
    const services = await this.consul.health.service({
      service: serviceName,
      passing: true,
    });

    return services.map(
      (entry) => `http://${entry.Service.Address}:${entry.Service.Port}`,
    );
  }
}
```

---

## 🔐 Authentication & Security

### JWT Authentication Strategy

```typescript
// auth/strategies/jwt.strategy.ts
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { ConfigService } from '@nestjs/config';

export interface JwtPayload {
  sub: string;
  email: string;
  role: string;
  iat: number;
  exp: number;
}

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(private readonly configService: ConfigService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: configService.get<string>('JWT_SECRET'),
      algorithms: ['HS256'],
    });
  }

  async validate(payload: JwtPayload) {
    if (!payload.sub) {
      throw new UnauthorizedException('Invalid token');
    }

    return {
      id: payload.sub,
      email: payload.email,
      role: payload.role,
    };
  }
}
```

### Auth Service Implementation

```typescript
// auth/auth.service.ts
import { Injectable, UnauthorizedException, ConflictException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';
import * as bcrypt from 'bcrypt';
import { UsersService } from '../users/users.service';
import { RegisterDto } from './dto/register.dto';
import { LoginDto } from './dto/login.dto';

@Injectable()
export class AuthService {
  constructor(
    private readonly usersService: UsersService,
    private readonly jwtService: JwtService,
    private readonly configService: ConfigService,
  ) {}

  async register(registerDto: RegisterDto) {
    const existingUser = await this.usersService.findByEmail(registerDto.email);
    if (existingUser) {
      throw new ConflictException('Email already registered');
    }

    const hashedPassword = await bcrypt.hash(registerDto.password, 12);
    const user = await this.usersService.create({
      ...registerDto,
      password: hashedPassword,
    });

    const tokens = await this.generateTokens(user);

    return {
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
      },
      ...tokens,
    };
  }

  async login(loginDto: LoginDto) {
    const user = await this.usersService.findByEmailWithPassword(loginDto.email);
    if (!user) {
      throw new UnauthorizedException('Invalid credentials');
    }

    const isPasswordValid = await bcrypt.compare(loginDto.password, user.password);
    if (!isPasswordValid) {
      throw new UnauthorizedException('Invalid credentials');
    }

    // Update last login
    await this.usersService.updateLastLogin(user.id);

    const tokens = await this.generateTokens(user);

    return {
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
      },
      ...tokens,
    };
  }

  async refreshToken(refreshToken: string) {
    try {
      const payload = this.jwtService.verify(refreshToken, {
        secret: this.configService.get('JWT_REFRESH_SECRET'),
      });

      const user = await this.usersService.findById(payload.sub);
      if (!user) {
        throw new UnauthorizedException('User not found');
      }

      return this.generateTokens(user);
    } catch (error) {
      throw new UnauthorizedException('Invalid refresh token');
    }
  }

  private async generateTokens(user: any) {
    const payload = {
      sub: user.id,
      email: user.email,
      role: user.role,
    };

    const [accessToken, refreshToken] = await Promise.all([
      this.jwtService.signAsync(payload, {
        secret: this.configService.get('JWT_SECRET'),
        expiresIn: '15m',
      }),
      this.jwtService.signAsync(payload, {
        secret: this.configService.get('JWT_REFRESH_SECRET'),
        expiresIn: '7d',
      }),
    ]);

    return {
      accessToken,
      refreshToken,
      expiresIn: 900, // 15 minutes in seconds
    };
  }
}
```

### Role-Based Access Control (RBAC)

```typescript
// auth/guards/roles.guard.ts
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { ROLES_KEY } from '../decorators/roles.decorator';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<string[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    if (!requiredRoles) {
      return true;
    }

    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some((role) => user?.role === role);
  }
}

// auth/decorators/roles.decorator.ts
import { SetMetadata } from '@nestjs/common';

export const ROLES_KEY = 'roles';
export const Roles = (...roles: string[]) => SetMetadata(ROLES_KEY, roles);

// Usage:
// @UseGuards(JwtAuthGuard, RolesGuard)
// @Roles('admin', 'moderator')
// @Get('admin-only')
// adminOnlyRoute() { ... }
```

### Service-to-Service Authentication

```typescript
// auth/guards/service-auth.guard.ts
import { Injectable, CanActivate, ExecutionContext, UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class ServiceAuthGuard implements CanActivate {
  private readonly serviceKeys: Map<string, string>;

  constructor(private readonly configService: ConfigService) {
    // In production, load from Vault or AWS Secrets Manager
    this.serviceKeys = new Map([
      ['order-service', this.configService.get('ORDER_SERVICE_KEY')],
      ['payment-service', this.configService.get('PAYMENT_SERVICE_KEY')],
      ['notification-service', this.configService.get('NOTIFICATION_SERVICE_KEY')],
    ]);
  }

  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const serviceName = request.headers['x-service-name'];
    const serviceKey = request.headers['x-service-key'];

    if (!serviceName || !serviceKey) {
      throw new UnauthorizedException('Missing service credentials');
    }

    const expectedKey = this.serviceKeys.get(serviceName);
    if (!expectedKey || expectedKey !== serviceKey) {
      throw new UnauthorizedException('Invalid service credentials');
    }

    // Add service info to request
    request.service = { name: serviceName };
    return true;
  }
}
```

---

## 🐳 Containerization with Docker

### Production Dockerfile (Multi-Stage)

```dockerfile
# Dockerfile
# ===========================================
# STAGE 1: Dependencies
# ===========================================
FROM node:20-alpine AS deps

WORKDIR /app

# Install dependencies only when needed
COPY package*.json ./
COPY prisma ./prisma/

RUN npm ci --only=production && npm cache clean --force

# ===========================================
# STAGE 2: Builder
# ===========================================
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# ===========================================
# STAGE 3: Production Runner
# ===========================================
FROM node:20-alpine AS runner

# Security: Don't run as root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nestjs

WORKDIR /app

# Copy built application
COPY --from=builder --chown=nestjs:nodejs /app/dist ./dist
COPY --from=deps --chown=nestjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nestjs:nodejs /app/package*.json ./

# Environment
ENV NODE_ENV=production
ENV PORT=3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

USER nestjs

EXPOSE 3000

CMD ["node", "dist/main.js"]
```

### Docker Compose for Local Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  # ===========================================
  # INFRASTRUCTURE
  # ===========================================
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: microservices
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  mongodb:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: rabbit
      RABBITMQ_DEFAULT_PASS: rabbit
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: rabbitmq-diagnostics -q ping
      interval: 10s
      timeout: 5s
      retries: 5

  # ===========================================
  # API GATEWAY
  # ===========================================
  api-gateway:
    build:
      context: ./services/api-gateway
      dockerfile: Dockerfile.dev
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
      - USER_SERVICE_URL=http://user-service:3000
      - PRODUCT_SERVICE_URL=http://product-service:3001
      - ORDER_SERVICE_URL=http://order-service:3002
      - JWT_SECRET=your-super-secret-key
    depends_on:
      - user-service
      - product-service
      - order-service
    volumes:
      - ./services/api-gateway:/app
      - /app/node_modules

  # ===========================================
  # MICROSERVICES
  # ===========================================
  user-service:
    build:
      context: ./services/user-service
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    environment:
      - PORT=3000
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/users
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://rabbit:rabbit@rabbitmq:5672
      - JWT_SECRET=your-super-secret-key
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    volumes:
      - ./services/user-service:/app
      - /app/node_modules

  product-service:
    build:
      context: ./services/product-service
      dockerfile: Dockerfile.dev
    ports:
      - "3001:3001"
    environment:
      - PORT=3001
      - MONGODB_URI=mongodb://mongodb:27017/products
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://rabbit:rabbit@rabbitmq:5672
    depends_on:
      mongodb:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./services/product-service:/app
      - /app/node_modules

  order-service:
    build:
      context: ./services/order-service
      dockerfile: Dockerfile.dev
    ports:
      - "3002:3002"
    environment:
      - PORT=3002
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/orders
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://rabbit:rabbit@rabbitmq:5672
      - USER_SERVICE_URL=http://user-service:3000
      - PRODUCT_SERVICE_URL=http://product-service:3001
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    volumes:
      - ./services/order-service:/app
      - /app/node_modules

  notification-service:
    build:
      context: ./services/notification-service
      dockerfile: Dockerfile.dev
    ports:
      - "3003:3003"
    environment:
      - PORT=3003
      - RABBITMQ_URL=amqp://rabbit:rabbit@rabbitmq:5672
      - SMTP_HOST=mailhog
      - SMTP_PORT=1025
    depends_on:
      rabbitmq:
        condition: service_healthy
    volumes:
      - ./services/notification-service:/app
      - /app/node_modules

  # ===========================================
  # DEV TOOLS
  # ===========================================
  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"
      - "8025:8025"

volumes:
  postgres_data:
  mongo_data:
  redis_data:
  rabbitmq_data:

networks:
  default:
    name: microservices-network
```

---

## ☸️ Kubernetes Deployment

### Namespace & ConfigMap

```yaml
# k8s/base/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: microservices
  labels:
    name: microservices
    istio-injection: enabled  # If using Istio
```

```yaml
# k8s/base/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: microservices-config
  namespace: microservices
data:
  NODE_ENV: "production"
  LOG_LEVEL: "info"
  RABBITMQ_URL: "amqp://rabbitmq.microservices.svc.cluster.local:5672"
  REDIS_URL: "redis://redis.microservices.svc.cluster.local:6379"
```

### Secrets Management

```yaml
# k8s/base/secrets.yaml
# Note: In production, use External Secrets Operator with AWS Secrets Manager or Vault
apiVersion: v1
kind: Secret
metadata:
  name: microservices-secrets
  namespace: microservices
type: Opaque
stringData:
  JWT_SECRET: "your-production-secret"
  DATABASE_PASSWORD: "secure-password"
  RABBITMQ_PASSWORD: "secure-password"
```

### Service Deployment

```yaml
# k8s/services/user-service/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: microservices
  labels:
    app: user-service
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: user-service
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "3000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: user-service
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
        - name: user-service
          image: myregistry/user-service:v1.0.0
          imagePullPolicy: Always
          ports:
            - containerPort: 3000
              protocol: TCP
          env:
            - name: NODE_ENV
              valueFrom:
                configMapKeyRef:
                  name: microservices-config
                  key: NODE_ENV
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: user-service-secrets
                  key: DATABASE_URL
            - name: JWT_SECRET
              valueFrom:
                secretKeyRef:
                  name: microservices-secrets
                  key: JWT_SECRET
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: user-service
                topologyKey: kubernetes.io/hostname
```

### Service & Ingress

```yaml
# k8s/services/user-service/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: microservices
  labels:
    app: user-service
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 3000
      protocol: TCP
      name: http
  selector:
    app: user-service
```

```yaml
# k8s/services/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: microservices-ingress
  namespace: microservices
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
    - hosts:
        - api.myapp.com
      secretName: api-tls-secret
  rules:
    - host: api.myapp.com
      http:
        paths:
          - path: /api/users
            pathType: Prefix
            backend:
              service:
                name: user-service
                port:
                  number: 80
          - path: /api/products
            pathType: Prefix
            backend:
              service:
                name: product-service
                port:
                  number: 80
          - path: /api/orders
            pathType: Prefix
            backend:
              service:
                name: order-service
                port:
                  number: 80
```

### Horizontal Pod Autoscaler

```yaml
# k8s/services/user-service/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-hpa
  namespace: microservices
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
  minReplicas: 3
  maxReplicas: 20
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
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 4
          periodSeconds: 15
      selectPolicy: Max
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ===========================================
  # LINT & TEST
  # ===========================================
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [user-service, product-service, order-service]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: services/${{ matrix.service }}/package-lock.json
      
      - name: Install dependencies
        working-directory: services/${{ matrix.service }}
        run: npm ci
      
      - name: Lint
        working-directory: services/${{ matrix.service }}
        run: npm run lint
      
      - name: Unit Tests
        working-directory: services/${{ matrix.service }}
        run: npm run test:cov
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          directory: services/${{ matrix.service }}/coverage
          flags: ${{ matrix.service }}

  # ===========================================
  # BUILD & PUSH DOCKER IMAGES
  # ===========================================
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    strategy:
      matrix:
        service: [user-service, product-service, order-service]
    
    permissions:
      contents: read
      packages: write
    
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/${{ matrix.service }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: services/${{ matrix.service }}
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ===========================================
  # DEPLOY TO STAGING
  # ===========================================
  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: staging
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}
      
      - name: Update image tags
        run: |
          for service in user-service product-service order-service; do
            kubectl set image deployment/$service \
              $service=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/$service:${{ github.sha }} \
              -n microservices-staging
          done
      
      - name: Wait for rollout
        run: |
          for service in user-service product-service order-service; do
            kubectl rollout status deployment/$service -n microservices-staging --timeout=300s
          done

  # ===========================================
  # DEPLOY TO PRODUCTION
  # ===========================================
  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG_PRODUCTION }}
      
      - name: Deploy with Canary
        run: |
          # Deploy canary (10% traffic)
          kubectl apply -f k8s/overlays/production/canary/
          
          # Wait and monitor
          sleep 300
          
          # Check error rate
          ERROR_RATE=$(kubectl exec -n monitoring prometheus-0 -- \
            promtool query instant 'rate(http_requests_total{status=~"5.."}[5m])')
          
          if [ "$ERROR_RATE" -gt "0.01" ]; then
            echo "Error rate too high, rolling back"
            kubectl rollout undo deployment/user-service -n microservices
            exit 1
          fi
          
          # Promote to full deployment
          kubectl apply -f k8s/overlays/production/
      
      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "🚀 Production deployment completed for ${{ github.sha }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 📊 Monitoring & Observability

### Prometheus Configuration

```yaml
# monitoring/prometheus/prometheus.yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: prometheus
  namespace: monitoring
spec:
  serviceAccountName: prometheus
  serviceMonitorSelector:
    matchLabels:
      team: microservices
  resources:
    requests:
      memory: 400Mi
  enableAdminAPI: false
  storage:
    volumeClaimTemplate:
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 50Gi
```

```yaml
# monitoring/prometheus/service-monitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: microservices-monitor
  namespace: monitoring
  labels:
    team: microservices
spec:
  selector:
    matchLabels:
      monitoring: enabled
  namespaceSelector:
    matchNames:
      - microservices
  endpoints:
    - port: http
      path: /metrics
      interval: 15s
```

### Grafana Dashboard (JSON)

```json
{
  "dashboard": {
    "title": "Microservices Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (service) / sum(rate(http_requests_total[5m])) by (service) * 100",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "title": "Response Time (p99)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "title": "Pod CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(container_cpu_usage_seconds_total{namespace=\"microservices\"}[5m])) by (pod)",
            "legendFormat": "{{pod}}"
          }
        ]
      }
    ]
  }
}
```

### Distributed Tracing with Jaeger

```typescript
// tracing/tracing.module.ts
import { Module } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { JaegerExporter } from '@opentelemetry/exporter-jaeger';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

@Module({})
export class TracingModule {
  static forRoot(serviceName: string) {
    const sdk = new NodeSDK({
      resource: new Resource({
        [SemanticResourceAttributes.SERVICE_NAME]: serviceName,
      }),
      traceExporter: new JaegerExporter({
        endpoint: process.env.JAEGER_ENDPOINT || 'http://jaeger:14268/api/traces',
      }),
      instrumentations: [getNodeAutoInstrumentations()],
    });

    sdk.start();

    process.on('SIGTERM', () => {
      sdk.shutdown().finally(() => process.exit(0));
    });

    return {
      module: TracingModule,
    };
  }
}
```

### Centralized Logging with ELK

```typescript
// logging/logger.service.ts
import { Injectable, LoggerService } from '@nestjs/common';
import * as winston from 'winston';
import { ElasticsearchTransport } from 'winston-elasticsearch';

@Injectable()
export class CustomLogger implements LoggerService {
  private logger: winston.Logger;

  constructor() {
    const esTransport = new ElasticsearchTransport({
      level: 'info',
      clientOpts: {
        node: process.env.ELASTICSEARCH_URL || 'http://elasticsearch:9200',
      },
      indexPrefix: 'microservices-logs',
    });

    this.logger = winston.createLogger({
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json(),
      ),
      defaultMeta: {
        service: process.env.SERVICE_NAME,
        version: process.env.APP_VERSION,
        environment: process.env.NODE_ENV,
      },
      transports: [
        new winston.transports.Console({
          format: winston.format.combine(
            winston.format.colorize(),
            winston.format.simple(),
          ),
        }),
        esTransport,
      ],
    });
  }

  log(message: string, context?: string) {
    this.logger.info(message, { context });
  }

  error(message: string, trace?: string, context?: string) {
    this.logger.error(message, { trace, context });
  }

  warn(message: string, context?: string) {
    this.logger.warn(message, { context });
  }

  debug(message: string, context?: string) {
    this.logger.debug(message, { context });
  }
}
```

---

## 🛡️ Resilience Patterns

### Circuit Breaker Implementation

```typescript
// resilience/circuit-breaker.service.ts
import { Injectable, Logger } from '@nestjs/common';
import CircuitBreaker from 'opossum';

interface CircuitBreakerOptions {
  timeout?: number;
  errorThresholdPercentage?: number;
  resetTimeout?: number;
  volumeThreshold?: number;
}

@Injectable()
export class CircuitBreakerService {
  private readonly logger = new Logger(CircuitBreakerService.name);
  private breakers: Map<string, CircuitBreaker> = new Map();

  createBreaker<T>(
    name: string,
    action: (...args: any[]) => Promise<T>,
    options: CircuitBreakerOptions = {},
  ): CircuitBreaker {
    const breaker = new CircuitBreaker(action, {
      timeout: options.timeout || 3000,
      errorThresholdPercentage: options.errorThresholdPercentage || 50,
      resetTimeout: options.resetTimeout || 30000,
      volumeThreshold: options.volumeThreshold || 5,
    });

    breaker.on('open', () => {
      this.logger.warn(`Circuit breaker ${name} OPENED`);
    });

    breaker.on('halfOpen', () => {
      this.logger.log(`Circuit breaker ${name} HALF-OPEN`);
    });

    breaker.on('close', () => {
      this.logger.log(`Circuit breaker ${name} CLOSED`);
    });

    breaker.on('fallback', () => {
      this.logger.warn(`Circuit breaker ${name} FALLBACK executed`);
    });

    this.breakers.set(name, breaker);
    return breaker;
  }

  async execute<T>(
    name: string,
    action: () => Promise<T>,
    fallback?: () => T,
  ): Promise<T> {
    let breaker = this.breakers.get(name);
    
    if (!breaker) {
      breaker = this.createBreaker(name, action);
    }

    if (fallback) {
      breaker.fallback(fallback);
    }

    return breaker.fire();
  }

  getStats(name: string) {
    const breaker = this.breakers.get(name);
    return breaker?.stats;
  }
}
```

### Retry with Exponential Backoff

```typescript
// resilience/retry.service.ts
import { Injectable, Logger } from '@nestjs/common';

interface RetryOptions {
  maxRetries?: number;
  initialDelay?: number;
  maxDelay?: number;
  backoffMultiplier?: number;
  retryableErrors?: string[];
}

@Injectable()
export class RetryService {
  private readonly logger = new Logger(RetryService.name);

  async execute<T>(
    action: () => Promise<T>,
    options: RetryOptions = {},
  ): Promise<T> {
    const {
      maxRetries = 3,
      initialDelay = 1000,
      maxDelay = 10000,
      backoffMultiplier = 2,
      retryableErrors = ['ECONNREFUSED', 'ETIMEDOUT', 'ENOTFOUND'],
    } = options;

    let lastError: Error;
    let delay = initialDelay;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await action();
      } catch (error) {
        lastError = error;
        
        const isRetryable = retryableErrors.some(
          (code) => error.code === code || error.message?.includes(code),
        );

        if (!isRetryable || attempt === maxRetries) {
          throw error;
        }

        this.logger.warn(
          `Attempt ${attempt}/${maxRetries} failed. Retrying in ${delay}ms...`,
        );

        await this.sleep(delay);
        delay = Math.min(delay * backoffMultiplier, maxDelay);
      }
    }

    throw lastError;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
```

### Bulkhead Pattern

```typescript
// resilience/bulkhead.service.ts
import { Injectable, Logger } from '@nestjs/common';
import PQueue from 'p-queue';

interface BulkheadOptions {
  concurrency?: number;
  timeout?: number;
  queueSize?: number;
}

@Injectable()
export class BulkheadService {
  private readonly logger = new Logger(BulkheadService.name);
  private pools: Map<string, PQueue> = new Map();

  createPool(name: string, options: BulkheadOptions = {}): PQueue {
    const pool = new PQueue({
      concurrency: options.concurrency || 10,
      timeout: options.timeout || 30000,
      throwOnTimeout: true,
    });

    pool.on('active', () => {
      this.logger.debug(
        `Pool ${name}: Size: ${pool.size}, Pending: ${pool.pending}`,
      );
    });

    this.pools.set(name, pool);
    return pool;
  }

  async execute<T>(
    poolName: string,
    action: () => Promise<T>,
    options: BulkheadOptions = {},
  ): Promise<T> {
    let pool = this.pools.get(poolName);
    
    if (!pool) {
      pool = this.createPool(poolName, options);
    }

    // Check if queue is full
    if (options.queueSize && pool.size >= options.queueSize) {
      throw new Error(`Bulkhead ${poolName} is full`);
    }

    return pool.add(action);
  }

  getPoolStats(name: string) {
    const pool = this.pools.get(name);
    return pool
      ? {
          size: pool.size,
          pending: pool.pending,
          isPaused: pool.isPaused,
        }
      : null;
  }
}
```

---

## 🧪 Testing Strategies

### Unit Test Example

```typescript
// users/users.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { UsersService } from './users.service';
import { UsersRepository } from './users.repository';
import { EventEmitter2 } from '@nestjs/event-emitter';
import { ConflictException, NotFoundException } from '@nestjs/common';

describe('UsersService', () => {
  let service: UsersService;
  let repository: jest.Mocked<UsersRepository>;
  let eventEmitter: jest.Mocked<EventEmitter2>;

  const mockUser = {
    id: '123',
    email: 'test@example.com',
    name: 'Test User',
    role: 'user',
    createdAt: new Date(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: UsersRepository,
          useValue: {
            findById: jest.fn(),
            findByEmail: jest.fn(),
            create: jest.fn(),
            update: jest.fn(),
            delete: jest.fn(),
          },
        },
        {
          provide: EventEmitter2,
          useValue: {
            emit: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<UsersService>(UsersService);
    repository = module.get(UsersRepository);
    eventEmitter = module.get(EventEmitter2);
  });

  describe('create', () => {
    it('should create a new user successfully', async () => {
      repository.findByEmail.mockResolvedValue(null);
      repository.create.mockResolvedValue(mockUser);

      const result = await service.create({
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123',
      });

      expect(result).toEqual(mockUser);
      expect(eventEmitter.emit).toHaveBeenCalledWith('user.created', {
        userId: mockUser.id,
        email: mockUser.email,
        name: mockUser.name,
      });
    });

    it('should throw ConflictException if email exists', async () => {
      repository.findByEmail.mockResolvedValue(mockUser);

      await expect(
        service.create({
          email: 'test@example.com',
          name: 'Test User',
          password: 'password123',
        }),
      ).rejects.toThrow(ConflictException);
    });
  });

  describe('findById', () => {
    it('should return user if found', async () => {
      repository.findById.mockResolvedValue(mockUser);

      const result = await service.findById('123');

      expect(result).toEqual(mockUser);
    });

    it('should throw NotFoundException if user not found', async () => {
      repository.findById.mockResolvedValue(null);

      await expect(service.findById('999')).rejects.toThrow(NotFoundException);
    });
  });
});
```

### Integration Test with TestContainers

```typescript
// test/users.e2e-spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../src/app.module';
import { PostgreSqlContainer, StartedPostgreSqlContainer } from '@testcontainers/postgresql';
import { DataSource } from 'typeorm';

describe('UsersController (e2e)', () => {
  let app: INestApplication;
  let postgresContainer: StartedPostgreSqlContainer;
  let dataSource: DataSource;

  beforeAll(async () => {
    // Start PostgreSQL container
    postgresContainer = await new PostgreSqlContainer()
      .withDatabase('test_db')
      .withUsername('test')
      .withPassword('test')
      .start();

    process.env.DATABASE_URL = postgresContainer.getConnectionUri();

    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
    await app.init();

    dataSource = app.get(DataSource);
    await dataSource.runMigrations();
  });

  afterAll(async () => {
    await dataSource.destroy();
    await app.close();
    await postgresContainer.stop();
  });

  beforeEach(async () => {
    // Clean up database before each test
    await dataSource.query('TRUNCATE TABLE users CASCADE');
  });

  describe('POST /users', () => {
    it('should create a new user', async () => {
      const response = await request(app.getHttpServer())
        .post('/users')
        .send({
          email: 'test@example.com',
          name: 'Test User',
          password: 'SecureP@ss123',
        })
        .expect(201);

      expect(response.body).toMatchObject({
        email: 'test@example.com',
        name: 'Test User',
      });
      expect(response.body.id).toBeDefined();
      expect(response.body.password).toBeUndefined();
    });

    it('should return 400 for invalid email', async () => {
      await request(app.getHttpServer())
        .post('/users')
        .send({
          email: 'invalid-email',
          name: 'Test User',
          password: 'SecureP@ss123',
        })
        .expect(400);
    });

    it('should return 409 for duplicate email', async () => {
      await request(app.getHttpServer())
        .post('/users')
        .send({
          email: 'test@example.com',
          name: 'Test User',
          password: 'SecureP@ss123',
        });

      await request(app.getHttpServer())
        .post('/users')
        .send({
          email: 'test@example.com',
          name: 'Another User',
          password: 'SecureP@ss123',
        })
        .expect(409);
    });
  });

  describe('GET /users/:id', () => {
    it('should return user by id', async () => {
      const createResponse = await request(app.getHttpServer())
        .post('/users')
        .send({
          email: 'test@example.com',
          name: 'Test User',
          password: 'SecureP@ss123',
        });

      const response = await request(app.getHttpServer())
        .get(`/users/${createResponse.body.id}`)
        .expect(200);

      expect(response.body.id).toBe(createResponse.body.id);
    });

    it('should return 404 for non-existent user', async () => {
      await request(app.getHttpServer())
        .get('/users/00000000-0000-0000-0000-000000000000')
        .expect(404);
    });
  });
});
```

### Contract Testing with Pact

```typescript
// test/contracts/user-service.pact.ts
import { Pact } from '@pact-foundation/pact';
import { like, eachLike } from '@pact-foundation/pact/src/dsl/matchers';
import path from 'path';
import axios from 'axios';

describe('User Service Contract', () => {
  const provider = new Pact({
    consumer: 'OrderService',
    provider: 'UserService',
    port: 1234,
    log: path.resolve(process.cwd(), 'logs', 'pact.log'),
    dir: path.resolve(process.cwd(), 'pacts'),
  });

  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());
  afterEach(() => provider.verify());

  describe('GET /users/:id', () => {
    it('should return a user', async () => {
      await provider.addInteraction({
        state: 'user with id 123 exists',
        uponReceiving: 'a request for user 123',
        withRequest: {
          method: 'GET',
          path: '/users/123',
          headers: {
            Accept: 'application/json',
          },
        },
        willRespondWith: {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
          },
          body: {
            id: like('123'),
            email: like('user@example.com'),
            name: like('John Doe'),
            role: like('user'),
          },
        },
      });

      const response = await axios.get('http://localhost:1234/users/123');
      
      expect(response.status).toBe(200);
      expect(response.data.id).toBe('123');
    });
  });
});
```

---

## ✅ Production Checklist

### Security Checklist

- [ ] **Secrets Management**: All secrets stored in Vault/AWS Secrets Manager
- [ ] **TLS/SSL**: HTTPS enabled everywhere (including internal traffic)
- [ ] **Authentication**: JWT with short expiration (15 min access, 7 day refresh)
- [ ] **Authorization**: RBAC implemented and tested
- [ ] **Input Validation**: All inputs validated with class-validator
- [ ] **SQL Injection**: Using parameterized queries/ORM
- [ ] **Rate Limiting**: Configured on API Gateway
- [ ] **CORS**: Properly configured for production domains only
- [ ] **Security Headers**: Helmet.js middleware enabled
- [ ] **Container Security**: Images scanned for vulnerabilities
- [ ] **Network Policies**: Inter-service communication restricted

### Reliability Checklist

- [ ] **Health Checks**: Liveness and readiness probes configured
- [ ] **Circuit Breakers**: Implemented for all external calls
- [ ] **Retry Logic**: With exponential backoff
- [ ] **Timeouts**: Configured for all HTTP clients
- [ ] **Graceful Shutdown**: Handling SIGTERM properly
- [ ] **Database Connections**: Connection pooling configured
- [ ] **Message Queue**: Dead letter queues configured
- [ ] **Data Backups**: Automated daily backups with tested restore

### Observability Checklist

- [ ] **Logging**: Centralized logging (ELK/Loki)
- [ ] **Metrics**: Prometheus metrics exposed
- [ ] **Tracing**: Distributed tracing with Jaeger
- [ ] **Dashboards**: Grafana dashboards for all services
- [ ] **Alerting**: PagerDuty/Slack alerts configured
- [ ] **Error Tracking**: Sentry or similar configured
- [ ] **Correlation IDs**: Passed through all service calls

### Performance Checklist

- [ ] **Load Testing**: Completed with k6 or similar
- [ ] **Auto-scaling**: HPA configured and tested
- [ ] **Caching**: Redis caching for hot data
- [ ] **CDN**: Static assets served via CDN
- [ ] **Database Indexes**: Query performance optimized
- [ ] **Connection Pooling**: Database connections pooled
- [ ] **Compression**: Gzip/Brotli enabled

### Deployment Checklist

- [ ] **CI/CD Pipeline**: Fully automated
- [ ] **Staging Environment**: Mirrors production
- [ ] **Rollback Plan**: One-click rollback tested
- [ ] **Blue-Green/Canary**: Deployment strategy defined
- [ ] **Database Migrations**: Zero-downtime migrations
- [ ] **Feature Flags**: For gradual rollouts
- [ ] **Runbooks**: Documented for common issues

---

## 💰 Cost Optimization

### Resource Right-Sizing

```yaml
# Start small, scale based on actual usage
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Spot Instances for Non-Critical Workloads

```yaml
# k8s/node-selector-spot.yaml
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 1
          preference:
            matchExpressions:
              - key: node.kubernetes.io/lifecycle
                operator: In
                values:
                  - spot
```

### Cost Monitoring

```yaml
# Deploy Kubecost or similar
# Track cost per service, namespace, team
```

---

## 🔧 Troubleshooting Guide

### Common Issues & Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Pod CrashLoopBackOff** | Pod restarts repeatedly | Check logs: `kubectl logs <pod> --previous` |
| **Service Unreachable** | 503 errors | Verify service selector matches pod labels |
| **High Latency** | Slow response times | Check distributed tracing, database queries |
| **Memory OOM** | Pod killed | Increase limits or fix memory leak |
| **Connection Refused** | ECONNREFUSED | Check if target pod is ready, network policies |
| **Database Connection** | Pool exhausted | Increase pool size or reduce connection lifetime |
| **Message Queue Backup** | Growing queue size | Scale consumers, check for stuck messages |

### Useful Commands

```bash
# Get pod logs
kubectl logs -f <pod-name> -n microservices

# Get previous crash logs
kubectl logs <pod-name> -n microservices --previous

# Describe pod (events, conditions)
kubectl describe pod <pod-name> -n microservices

# Execute shell in pod
kubectl exec -it <pod-name> -n microservices -- /bin/sh

# Port forward for debugging
kubectl port-forward svc/user-service 3000:80 -n microservices

# Get all events
kubectl get events -n microservices --sort-by='.lastTimestamp'

# Check HPA status
kubectl get hpa -n microservices

# View resource usage
kubectl top pods -n microservices
```

---

## 📚 Additional Resources

### Books
- "Building Microservices" by Sam Newman
- "Microservices Patterns" by Chris Richardson
- "Release It!" by Michael Nygard

### Tools
- **API Design**: Swagger/OpenAPI, Stoplight
- **Load Testing**: k6, Artillery, Locust
- **Chaos Engineering**: Chaos Monkey, Gremlin
- **Service Mesh**: Istio, Linkerd

### Learning Platforms
- [microservices.io](https://microservices.io)
- [12factor.net](https://12factor.net)
- [Kubernetes.io](https://kubernetes.io/docs)

---

## 🏁 Conclusion

Building production-level microservices requires careful attention to:

1. **Architecture**: Clear service boundaries, proper communication patterns
2. **Security**: Defense in depth, zero trust
3. **Reliability**: Expect failure, design for resilience
4. **Observability**: You can't fix what you can't see
5. **Automation**: CI/CD, infrastructure as code
6. **Team Structure**: Conway's Law - align teams with services

Start simple, iterate, and always prioritize **working software over perfect architecture**.

---

*Last updated: January 2026*
*Version: 2.0.0*
