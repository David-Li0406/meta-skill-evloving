/**
 * Production Guide Data
 * Complete structured data for the production microservices deployment guide
 */

export const productionGuideData = {
    title: "Production-Level Microservices Deployment Guide",
    description: "A comprehensive guide to deploying and maintaining production-ready microservices",
    lastUpdated: "January 2026",
    version: "2.0.0",

    sections: [
        // Section 1: Deployment Strategies Overview
        {
            id: "deployment-strategies",
            emoji: "🚢",
            shortTitle: "Monorepo vs Polyrepo",
            title: "Deployment Strategies: Monorepo vs Polyrepo",
            subtitle: "Understanding the two main approaches to organizing microservices repositories",
            description: `Before deploying microservices, you need to decide how to organize your code repositories. This fundamental decision affects your CI/CD pipelines, team workflows, and deployment strategies.`,
            diagram: `┌─────────────────────────────────────────────────────────────────────────────────────┐
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
└─────────────────────────────────────────────────────────────────────────────────────┘`,
            comparison: [
                { aspect: "Initial Setup", monorepo: "Harder (Nx/Turborepo config)", polyrepo: "Easier (standard repos)" },
                { aspect: "Code Sharing", monorepo: "Easy (direct imports)", polyrepo: "Harder (publish packages)" },
                { aspect: "CI/CD Complexity", monorepo: "Complex (change detection)", polyrepo: "Simple (per-repo)" },
                { aspect: "Build Time", monorepo: "Can be slow (cache helps)", polyrepo: "Fast (only one service)" },
                { aspect: "Atomic Changes", monorepo: "✅ Yes (single PR)", polyrepo: "❌ No (multiple PRs)" },
                { aspect: "Team Autonomy", monorepo: "Lower", polyrepo: "Higher" },
                { aspect: "Best For", monorepo: "Small-medium teams", polyrepo: "Large orgs, team-per-service" },
                { aspect: "Examples", monorepo: "Google, Meta", polyrepo: "Netflix, Amazon" },
            ],
            tip: "**Start with Monorepo** if you're a small team (< 20 developers). It's easier to refactor and share code. Move to Polyrepo when teams grow and need more autonomy."
        },

        // Section 2: Monorepo CI/CD
        {
            id: "monorepo-cicd",
            emoji: "🏢",
            shortTitle: "Monorepo CI/CD",
            title: "Monorepo: Production Deployment Guide",
            subtitle: "Complete CI/CD pipeline with change detection for monorepo setups",
            description: `In a monorepo, the key challenge is **only building and deploying what changed**. You don't want to rebuild all 50 services when only one file changed!`,
            subsections: [
                {
                    title: "Folder Structure",
                    content: `The recommended monorepo structure uses **Nx** or **Turborepo** for efficient builds:`,
                    code: `microservices-platform/
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
└── package.json`,
                    codeLanguage: "text",
                    codeFilename: "monorepo-structure"
                },
                {
                    title: "CI/CD Pipeline with Change Detection",
                    content: `The key to efficient monorepo CI/CD is **detecting which services changed** and only building those:`,
                    code: `# .github/workflows/ci.yml
name: Monorepo CI

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_PREFIX: \${{ github.repository }}

jobs:
  # ═══════════════════════════════════════════════════════════
  # STEP 1: DETECT WHICH SERVICES CHANGED
  # ═══════════════════════════════════════════════════════════
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      user-service: \${{ steps.changes.outputs.user-service }}
      product-service: \${{ steps.changes.outputs.product-service }}
      order-service: \${{ steps.changes.outputs.order-service }}
      payment-service: \${{ steps.changes.outputs.payment-service }}
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

  # ═══════════════════════════════════════════════════════════
  # STEP 2: TEST ONLY CHANGED SERVICES
  # ═══════════════════════════════════════════════════════════
  test:
    needs: detect-changes
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - service: user-service
            changed: \${{ needs.detect-changes.outputs.user-service }}
          - service: product-service
            changed: \${{ needs.detect-changes.outputs.product-service }}
          - service: order-service
            changed: \${{ needs.detect-changes.outputs.order-service }}
          - service: payment-service
            changed: \${{ needs.detect-changes.outputs.payment-service }}
    
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
        run: npx nx lint \${{ matrix.service }}

      - name: Test
        if: matrix.changed == 'true'
        run: npx nx test \${{ matrix.service }} --coverage

      - name: Build
        if: matrix.changed == 'true'
        run: npx nx build \${{ matrix.service }}

  # ═══════════════════════════════════════════════════════════
  # STEP 3: BUILD & PUSH DOCKER IMAGES (Only changed)
  # ═══════════════════════════════════════════════════════════
  build-and-push:
    needs: [detect-changes, test]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - service: user-service
            changed: \${{ needs.detect-changes.outputs.user-service }}
          - service: product-service
            changed: \${{ needs.detect-changes.outputs.product-service }}
    
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
          registry: \${{ env.REGISTRY }}
          username: \${{ github.actor }}
          password: \${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        if: matrix.changed == 'true'
        uses: docker/build-push-action@v5
        with:
          context: .
          file: services/\${{ matrix.service }}/Dockerfile
          push: true
          tags: |
            \${{ env.REGISTRY }}/\${{ env.IMAGE_PREFIX }}/\${{ matrix.service }}:\${{ github.sha }}
            \${{ env.REGISTRY }}/\${{ env.IMAGE_PREFIX }}/\${{ matrix.service }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ═══════════════════════════════════════════════════════════
  # STEP 4: DEPLOY TO STAGING
  # ═══════════════════════════════════════════════════════════
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
          kubeconfig: \${{ secrets.KUBE_CONFIG_STAGING }}

      - name: Deploy changed services
        run: |
          SERVICES=("user-service" "product-service" "order-service" "payment-service")
          CHANGES=("\${{ needs.detect-changes.outputs.user-service }}" \\
                   "\${{ needs.detect-changes.outputs.product-service }}" \\
                   "\${{ needs.detect-changes.outputs.order-service }}" \\
                   "\${{ needs.detect-changes.outputs.payment-service }}")
          
          for i in "\${!SERVICES[@]}"; do
            if [ "\${CHANGES[$i]}" == "true" ]; then
              echo "🚀 Deploying \${SERVICES[$i]}..."
              kubectl set image deployment/\${SERVICES[$i]} \\
                \${SERVICES[$i]}=\${{ env.REGISTRY }}/\${{ env.IMAGE_PREFIX }}/\${SERVICES[$i]}:\${{ github.sha }} \\
                -n microservices-staging
              kubectl rollout status deployment/\${SERVICES[$i]} -n microservices-staging --timeout=300s
            fi
          done

  # ═══════════════════════════════════════════════════════════
  # STEP 5: DEPLOY TO PRODUCTION (Manual approval)
  # ═══════════════════════════════════════════════════════════
  deploy-production:
    needs: [detect-changes, deploy-staging]
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval in GitHub
    
    steps:
      - uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: \${{ secrets.KUBE_CONFIG_PRODUCTION }}

      - name: Deploy with Canary
        run: |
          # Deploy canary first (10% of traffic)
          echo "🐤 Starting canary deployment..."
          # ... canary logic here ...

      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "✅ Production deployment completed"
            }
        env:
          SLACK_WEBHOOK_URL: \${{ secrets.SLACK_WEBHOOK }}`,
                    codeLanguage: "yaml",
                    codeFilename: ".github/workflows/ci.yml",
                    keyPoints: [
                        "Use `dorny/paths-filter` to detect which services changed",
                        "Only test, build, and deploy services that actually changed",
                        "Use GitHub matrix strategy to run jobs in parallel",
                        "Require manual approval for production deployments",
                        "Use Docker layer caching (type=gha) for faster builds"
                    ]
                },
                {
                    title: "Monorepo Dockerfile (with shared libs)",
                    content: `In a monorepo, your Dockerfile must be built from the **root** of the repository to access shared libraries:`,
                    code: `# services/user-service/Dockerfile
# ═══════════════════════════════════════════════════════════
# MONOREPO DOCKERFILE
# ═══════════════════════════════════════════════════════════
# Must be built from the ROOT of the monorepo:
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
CMD ["node", "dist/main.js"]`,
                    codeLanguage: "dockerfile",
                    codeFilename: "services/user-service/Dockerfile"
                }
            ],
            tip: "Use **Nx Cloud** or **Turborepo Remote Caching** to speed up builds dramatically. If a teammate already built the same code, you skip the build entirely!"
        },

        // Section 3: Polyrepo CI/CD
        {
            id: "polyrepo-cicd",
            emoji: "📦",
            shortTitle: "Polyrepo CI/CD",
            title: "Polyrepo: Production Deployment Guide",
            subtitle: "Individual service repositories with GitOps deployment",
            description: `In a polyrepo setup, each service lives in its own repository with its own CI/CD pipeline. The key pattern here is **GitOps** - using a separate infrastructure repository as the source of truth for deployments.`,
            subsections: [
                {
                    title: "Repository Structure",
                    content: `Each service has its own Git repository, plus a shared infrastructure repository:`,
                    code: `Organization GitHub:
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
│   └── ... (same structure)
│
├── order-service/             # github.com/myorg/order-service
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
        └── sync.yml           # ArgoCD sync`,
                    codeLanguage: "text",
                    codeFilename: "polyrepo-structure"
                },
                {
                    title: "Individual Service CI/CD Pipeline",
                    content: `Each service has a **self-contained pipeline** that builds, tests, and triggers deployment via GitOps:`,
                    code: `# user-service/.github/workflows/ci-cd.yml
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
  IMAGE_NAME: \${{ github.repository }}

jobs:
  # ═══════════════════════════════════════════════════════════
  # TEST
  # ═══════════════════════════════════════════════════════════
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

  # ═══════════════════════════════════════════════════════════
  # BUILD & PUSH
  # ═══════════════════════════════════════════════════════════
  build:
    needs: test
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    
    permissions:
      contents: read
      packages: write
    
    outputs:
      image-tag: \${{ steps.meta.outputs.version }}
      image-digest: \${{ steps.build.outputs.digest }}

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Registry
        uses: docker/login-action@v3
        with:
          registry: \${{ env.REGISTRY }}
          username: \${{ github.actor }}
          password: \${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: \${{ env.REGISTRY }}/\${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}

      - name: Build and push
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: \${{ steps.meta.outputs.tags }}
          labels: \${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Sign image with Cosign
        run: |
          cosign sign --yes \${{ env.REGISTRY }}/\${{ env.IMAGE_NAME }}@\${{ steps.build.outputs.digest }}

  # ═══════════════════════════════════════════════════════════
  # UPDATE GITOPS REPO (Triggers ArgoCD)
  # ═══════════════════════════════════════════════════════════
  update-manifests:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout k8s-infrastructure repo
        uses: actions/checkout@v4
        with:
          repository: myorg/k8s-infrastructure
          token: \${{ secrets.GITOPS_TOKEN }}
          path: infra

      - name: Update staging manifest
        run: |
          cd infra/clusters/staging/\${{ env.SERVICE_NAME }}
          
          # Update image tag in kustomization.yaml
          yq eval '.images[0].newTag = "\${{ needs.build.outputs.image-tag }}"' \\
            -i kustomization.yaml

      - name: Commit and push
        run: |
          cd infra
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add .
          git commit -m "chore(\${{ env.SERVICE_NAME }}): update staging to \${{ needs.build.outputs.image-tag }}"
          git push

  # ═══════════════════════════════════════════════════════════
  # PROMOTE TO PRODUCTION (After staging verification)
  # ═══════════════════════════════════════════════════════════
  promote-to-production:
    needs: [build, update-manifests]
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval
    
    steps:
      - name: Checkout k8s-infrastructure repo
        uses: actions/checkout@v4
        with:
          repository: myorg/k8s-infrastructure
          token: \${{ secrets.GITOPS_TOKEN }}
          path: infra

      - name: Update production manifest
        run: |
          cd infra/clusters/production/\${{ env.SERVICE_NAME }}
          yq eval '.images[0].newTag = "\${{ needs.build.outputs.image-tag }}"' \\
            -i kustomization.yaml

      - name: Commit and push
        run: |
          cd infra
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add .
          git commit -m "chore(\${{ env.SERVICE_NAME }}): promote to production \${{ needs.build.outputs.image-tag }}"
          git push

      - name: Notify team
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "✅ \${{ env.SERVICE_NAME }} deployed to production"
            }
        env:
          SLACK_WEBHOOK_URL: \${{ secrets.SLACK_WEBHOOK }}`,
                    codeLanguage: "yaml",
                    codeFilename: ".github/workflows/ci-cd.yml",
                    keyPoints: [
                        "Each service has a completely independent pipeline",
                        "CI pushes new image tag to GitOps repository",
                        "ArgoCD watches GitOps repo and auto-deploys to staging",
                        "Production requires manual approval before promotion",
                        "Use Cosign to sign container images for security"
                    ]
                },
                {
                    title: "Polyrepo Dockerfile (with npm packages)",
                    content: `In a polyrepo, shared code is published as **npm packages** and installed as dependencies:`,
                    code: `# user-service/Dockerfile
# ═══════════════════════════════════════════════════════════
# POLYREPO DOCKERFILE
# ═══════════════════════════════════════════════════════════
# Uses published npm packages for shared code

FROM node:20-alpine AS deps
WORKDIR /app

# Configure private npm registry for @myorg packages
COPY .npmrc ./
COPY package*.json ./

# Install dependencies (including @myorg/common, @myorg/contracts)
ARG NPM_TOKEN
RUN echo "//npm.pkg.github.com/:_authToken=\${NPM_TOKEN}" >> .npmrc && \\
    npm ci && \\
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

RUN addgroup --system --gid 1001 nodejs && \\
    adduser --system --uid 1001 nestjs

# Only copy production dependencies
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder --chown=nestjs:nodejs /app/dist ./dist
COPY --from=builder /app/package.json ./

USER nestjs
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/main.js"]`,
                    codeLanguage: "dockerfile",
                    codeFilename: "Dockerfile"
                },
                {
                    title: "Publishing Shared Libraries",
                    content: `Shared code is published to npm (or GitHub Packages) and versioned independently:`,
                    code: `# shared-libs/.github/workflows/publish.yml
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
          NODE_AUTH_TOKEN: \${{ secrets.GITHUB_TOKEN }}`,
                    codeLanguage: "yaml",
                    codeFilename: "publish.yml"
                }
            ],
            warning: "In polyrepo, updating a shared library requires **releasing a new version** and then updating all services that use it. This can be slow for urgent cross-cutting changes."
        },

        // Section 4: GitOps with ArgoCD
        {
            id: "gitops-argocd",
            emoji: "🔄",
            shortTitle: "GitOps & ArgoCD",
            title: "GitOps with ArgoCD",
            subtitle: "Using Git as the single source of truth for deployments",
            description: `**GitOps** is the practice of using Git repositories as the source of truth for your infrastructure. Instead of running \`kubectl apply\` directly, you commit changes to Git, and a tool like **ArgoCD** automatically syncs your cluster to match.`,
            diagram: `┌─────────────────────────────────────────────────────────────────────────────────┐
│                           GITOPS FLOW                                           │
└─────────────────────────────────────────────────────────────────────────────────┘

  Developer                 CI Pipeline                GitOps Repo              Kubernetes
     │                          │                          │                        │
     │  Push code               │                          │                        │
     ├─────────────────────────►│                          │                        │
     │                          │                          │                        │
     │                          │  Build & Push            │                        │
     │                          │  Docker Image            │                        │
     │                          │                          │                        │
     │                          │  Update image tag        │                        │
     │                          ├─────────────────────────►│                        │
     │                          │                          │                        │
     │                          │                          │  ArgoCD detects        │
     │                          │                          │  Git change            │
     │                          │                          ├───────────────────────►│
     │                          │                          │                        │
     │                          │                          │  Sync (kubectl apply)  │
     │                          │                          │                        │
     │                          │                          │                        │
     │  ◄──────────────────────────────────────────────────────────────────────────┤
     │                    Deployment Complete!                                      │
     │                                                                              │`,
            subsections: [
                {
                    title: "ArgoCD Application Manifest",
                    content: `ArgoCD uses **Application** resources to define what to deploy and where:`,
                    code: `# argocd/apps/user-service-staging.yaml
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
      prune: true      # Delete resources removed from Git
      selfHeal: true   # Revert manual changes
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

---
# Production (NO automated sync - requires manual approval)
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
    # NO automated sync for production!
    # Manual sync required via ArgoCD UI or CLI
    syncOptions:
      - CreateNamespace=true`,
                    codeLanguage: "yaml",
                    codeFilename: "argocd-application.yaml"
                },
                {
                    title: "Kustomize Overlays",
                    content: `Use **Kustomize** to manage environment-specific configurations:`,
                    code: `# k8s-infrastructure/clusters/staging/user-service/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: staging

resources:
  - ../../../base/user-service

images:
  - name: user-service
    newName: ghcr.io/myorg/user-service
    newTag: abc1234  # ← Updated by CI/CD pipeline

configMapGenerator:
  - name: user-service-config
    behavior: merge
    literals:
      - NODE_ENV=staging
      - LOG_LEVEL=debug

replicas:
  - name: user-service
    count: 2  # Fewer replicas in staging

# Production has different settings
# k8s-infrastructure/clusters/production/user-service/kustomization.yaml
# replicas: 5, LOG_LEVEL=info, etc.`,
                    codeLanguage: "yaml",
                    codeFilename: "kustomization.yaml",
                    keyPoints: [
                        "Git is the single source of truth - all changes are traceable",
                        "ArgoCD continuously monitors Git and syncs the cluster",
                        "Staging auto-syncs, production requires manual approval",
                        "Kustomize allows environment-specific configurations without duplication",
                        "Rollback = revert Git commit, ArgoCD will automatically sync"
                    ]
                }
            ],
            tip: "Enable **ArgoCD notifications** to get Slack/Teams alerts when deployments succeed or fail. You can also integrate with PagerDuty for production incidents."
        },

        // Section 5: Deployment Flow Diagrams
        {
            id: "deployment-flows",
            emoji: "📊",
            shortTitle: "Deployment Flows",
            title: "Complete Deployment Flow Diagrams",
            subtitle: "Visual representation of both deployment strategies",
            description: `Understanding the complete flow from code push to production deployment:`,
            diagram: `═══════════════════════════════════════════════════════════════════════════════════
                            MONOREPO DEPLOYMENT FLOW
═══════════════════════════════════════════════════════════════════════════════════

   Developer pushes to main
          │
          ▼
   ┌─────────────────┐
   │ Detect Changes  │ ◄─── Which services/libs changed?
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │  Test Changed   │ ◄─── Only test affected services (parallel)
   │    Services     │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Build & Push    │ ◄─── Build Docker images for changed only
   │  Docker Images  │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐      ┌─────────────────┐
   │ Deploy Staging  │ ───► │ Deploy Production│ ◄─── Manual approval required
   └─────────────────┘      └─────────────────┘


═══════════════════════════════════════════════════════════════════════════════════
                            POLYREPO DEPLOYMENT FLOW
═══════════════════════════════════════════════════════════════════════════════════

   Developer pushes to user-service repo
          │
          ▼
   ┌─────────────────┐
   │  Test Service   │ ◄─── Simple: test this repo only
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Build & Push    │ ◄─── One Docker image
   │  Docker Image   │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Update GitOps   │ ◄─── Push new image tag to k8s-infrastructure repo
   │  Repository     │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐      ┌─────────────────┐
   │ ArgoCD Syncs    │ ───► │ ArgoCD Syncs    │ ◄─── Manual approval required
   │   Staging       │      │   Production    │
   └─────────────────┘      └─────────────────┘`,
            keyPoints: [
                "Monorepo: Change detection is key to efficiency",
                "Polyrepo: Each service is completely independent",
                "Both: Production should always require manual approval",
                "Both: Use canary or blue-green deployments for safety"
            ]
        },

        // Section 6: Kubernetes Manifests
        {
            id: "kubernetes-manifests",
            emoji: "☸️",
            shortTitle: "Kubernetes",
            title: "Kubernetes Production Manifests",
            subtitle: "Production-ready Kubernetes configurations",
            description: `Complete Kubernetes manifests for production deployment including Deployments, Services, HPA, and Ingress.`,
            subsections: [
                {
                    title: "Production Deployment",
                    content: `A production-ready Deployment with proper resource limits, health checks, and security settings:`,
                    code: `# k8s/base/user-service/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
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
      maxSurge: 1        # Allow 1 extra pod during update
      maxUnavailable: 0  # Never go below desired count
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
          image: ghcr.io/myorg/user-service:latest
          imagePullPolicy: Always
          
          ports:
            - containerPort: 3000
              protocol: TCP
          
          env:
            - name: NODE_ENV
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: NODE_ENV
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: user-service-secrets
                  key: DATABASE_URL
            - name: JWT_SECRET
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: JWT_SECRET
          
          # Resource limits (CRITICAL for production!)
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          
          # Liveness: Is the container alive?
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          
          # Readiness: Is the container ready for traffic?
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          
          # Security hardening
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
      
      # Anti-affinity: Don't put all pods on same node
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: user-service
                topologyKey: kubernetes.io/hostname`,
                    codeLanguage: "yaml",
                    codeFilename: "deployment.yaml"
                },
                {
                    title: "Horizontal Pod Autoscaler",
                    content: `Automatically scale pods based on CPU/memory usage:`,
                    code: `# k8s/base/user-service/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-hpa
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
      stabilizationWindowSeconds: 300  # Wait 5 min before scaling down
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0    # Scale up immediately
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 4
          periodSeconds: 15
      selectPolicy: Max`,
                    codeLanguage: "yaml",
                    codeFilename: "hpa.yaml"
                },
                {
                    title: "Ingress with TLS",
                    content: `Route external traffic to your services with HTTPS:`,
                    code: `# k8s/base/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: microservices-ingress
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
                  number: 80`,
                    codeLanguage: "yaml",
                    codeFilename: "ingress.yaml",
                    keyPoints: [
                        "Always set resource requests AND limits",
                        "Use liveness probes to restart unhealthy containers",
                        "Use readiness probes to control traffic routing",
                        "Run as non-root user for security",
                        "Use pod anti-affinity to spread pods across nodes"
                    ]
                }
            ]
        },

        // Section 7: Production Checklist
        {
            id: "production-checklist",
            emoji: "✅",
            shortTitle: "Checklist",
            title: "Production Deployment Checklist",
            subtitle: "Don't deploy without checking these",
            description: `A comprehensive checklist to ensure your microservices are production-ready:`,
            checklist: [
                "✅ All secrets stored in Vault/AWS Secrets Manager (not in Git!)",
                "✅ HTTPS/TLS enabled everywhere (including internal traffic)",
                "✅ JWT tokens have short expiration (15 min access, 7 day refresh)",
                "✅ Rate limiting configured on API Gateway",
                "✅ Health checks (liveness + readiness) configured",
                "✅ Resource limits set on all containers",
                "✅ HPA configured for auto-scaling",
                "✅ Centralized logging (ELK/Loki) configured",
                "✅ Metrics exported to Prometheus",
                "✅ Distributed tracing (Jaeger) enabled",
                "✅ Alerting rules configured (PagerDuty/Slack)",
                "✅ Database backups automated and tested",
                "✅ Rollback procedure documented and tested",
                "✅ CI/CD pipeline includes security scanning",
                "✅ Container images scanned for vulnerabilities",
                "✅ Load testing completed (k6/Artillery)",
                "✅ Runbooks documented for common issues",
                "✅ On-call rotation scheduled"
            ],
            warning: "**Never deploy on Friday afternoon!** If something goes wrong, you'll be debugging over the weekend."
        },

        // Section 8: Troubleshooting
        {
            id: "troubleshooting",
            emoji: "🔧",
            shortTitle: "Troubleshooting",
            title: "Troubleshooting Guide",
            subtitle: "Common issues and how to fix them",
            description: `Quick reference for debugging deployment issues:`,
            subsections: [
                {
                    title: "Useful kubectl Commands",
                    code: `# Get pod logs
kubectl logs -f <pod-name> -n microservices

# Get previous crash logs
kubectl logs <pod-name> -n microservices --previous

# Describe pod (events, conditions)
kubectl describe pod <pod-name> -n microservices

# Execute shell in pod
kubectl exec -it <pod-name> -n microservices -- /bin/sh

# Port forward for debugging
kubectl port-forward svc/user-service 3000:80 -n microservices

# Get all events (sorted by time)
kubectl get events -n microservices --sort-by='.lastTimestamp'

# Check HPA status
kubectl get hpa -n microservices

# View resource usage
kubectl top pods -n microservices

# Force restart a deployment
kubectl rollout restart deployment/user-service -n microservices

# Rollback to previous version
kubectl rollout undo deployment/user-service -n microservices`,
                    codeLanguage: "bash",
                    codeFilename: "kubectl-commands.sh"
                },
                {
                    title: "Common Issues",
                    content: `
| Issue | Symptoms | Solution |
|-------|----------|----------|
| **CrashLoopBackOff** | Pod restarts repeatedly | Check logs: \`kubectl logs <pod> --previous\` |
| **ImagePullBackOff** | Image can't be pulled | Verify image exists, check registry credentials |
| **OOMKilled** | Pod killed for memory | Increase memory limits or fix memory leak |
| **Service Unreachable** | 503 errors | Verify service selector matches pod labels |
| **High Latency** | Slow responses | Check distributed tracing, database queries |
| **Connection Refused** | ECONNREFUSED | Check if target pod is ready, network policies |
`
                }
            ],
            tip: "Set up **kubectl aliases** to save time: `alias k=kubectl`, `alias kgp='kubectl get pods'`, `alias kl='kubectl logs -f'`"
        }
    ]
};
