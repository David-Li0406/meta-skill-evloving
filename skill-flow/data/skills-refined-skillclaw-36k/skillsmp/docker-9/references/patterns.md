# Docker & Containers

## Patterns


---
  #### **Name**
Multi-Stage Build
  #### **Description**
Separate build and runtime for smaller images
  #### **When**
Any compiled or bundled application
  #### **Example**
    # MULTI-STAGE BUILD:
    
    """
    Build stage has all build tools.
    Production stage has only runtime.
    Result: Smaller, more secure images.
    """
    
    # Node.js example
    # Build stage
    FROM node:20-alpine AS builder
    WORKDIR /app
    
    # Install dependencies first (cache layer)
    COPY package*.json ./
    RUN npm ci
    
    # Build application
    COPY . .
    RUN npm run build
    
    # Production stage
    FROM node:20-alpine AS production
    WORKDIR /app
    
    # Don't run as root
    RUN addgroup -S appgroup && adduser -S appuser -G appgroup
    
    # Copy only what's needed
    COPY --from=builder /app/dist ./dist
    COPY --from=builder /app/node_modules ./node_modules
    COPY --from=builder /app/package.json ./
    
    USER appuser
    EXPOSE 3000
    CMD ["node", "dist/index.js"]
    
    
    # Go example - even smaller
    FROM golang:1.22-alpine AS builder
    WORKDIR /app
    
    COPY go.mod go.sum ./
    RUN go mod download
    
    COPY . .
    RUN CGO_ENABLED=0 GOOS=linux go build -o main .
    
    # Scratch = empty image, ~5MB total
    FROM scratch
    COPY --from=builder /app/main /main
    COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
    ENTRYPOINT ["/main"]
    

---
  #### **Name**
Layer Caching Optimization
  #### **Description**
Order Dockerfile for maximum cache reuse
  #### **When**
Any Dockerfile with dependencies
  #### **Example**
    # LAYER CACHING:
    
    """
    Docker caches layers. If a layer changes, all following
    layers are rebuilt. Order from least to most frequently changed.
    """
    
    # WRONG: Copy everything first
    FROM node:20-alpine
    WORKDIR /app
    COPY . .                    # Any file change invalidates cache
    RUN npm ci                  # Reinstalls deps every time
    RUN npm run build
    
    # RIGHT: Dependencies before code
    FROM node:20-alpine
    WORKDIR /app
    
    # 1. Copy dependency files only
    COPY package.json package-lock.json ./
    
    # 2. Install dependencies (cached unless package*.json changes)
    RUN npm ci
    
    # 3. Copy source code (changes often, but deps are cached)
    COPY . .
    
    # 4. Build
    RUN npm run build
    
    
    # Python example
    FROM python:3.12-slim
    WORKDIR /app
    
    # Dependencies first
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Then code
    COPY . .
    CMD ["python", "main.py"]
    

---
  #### **Name**
Docker Compose for Development
  #### **Description**
Multi-container development environment
  #### **When**
App with database, cache, or other services
  #### **Example**
    # DOCKER COMPOSE:
    
    """
    Development environment with hot reload,
    databases, and service dependencies.
    """
    
    # docker-compose.yml
    version: '3.8'
    
    services:
      app:
        build:
          context: .
          dockerfile: Dockerfile.dev
        ports:
          - "3000:3000"
        volumes:
          # Mount code for hot reload
          - .:/app
          - /app/node_modules  # Preserve node_modules
        environment:
          - NODE_ENV=development
          - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
          - REDIS_URL=redis://redis:6379
        depends_on:
          db:
            condition: service_healthy
          redis:
            condition: service_started
    
      db:
        image: postgres:16-alpine
        environment:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: app
        volumes:
          - postgres_data:/var/lib/postgresql/data
        ports:
          - "5432:5432"
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U postgres"]
          interval: 5s
          timeout: 5s
          retries: 5
    
      redis:
        image: redis:7-alpine
        ports:
          - "6379:6379"
    
    volumes:
      postgres_data:
    
    
    # Dockerfile.dev (with hot reload)
    FROM node:20-alpine
    WORKDIR /app
    COPY package*.json ./
    RUN npm install
    # Don't copy code - mounted as volume
    CMD ["npm", "run", "dev"]
    

---
  #### **Name**
Security Hardening
  #### **Description**
Non-root user, minimal image, no secrets
  #### **When**
Any production image
  #### **Example**
    # SECURITY:
    
    """
    Production containers should:
    1. Run as non-root user
    2. Have minimal attack surface
    3. Never contain secrets
    """
    
    FROM node:20-alpine
    
    # Create non-root user
    RUN addgroup -S appgroup && \
        adduser -S appuser -G appgroup
    
    WORKDIR /app
    
    # Copy with correct ownership
    COPY --chown=appuser:appgroup package*.json ./
    RUN npm ci --only=production
    
    COPY --chown=appuser:appgroup . .
    
    # Switch to non-root user
    USER appuser
    
    # Don't expose unnecessary ports
    EXPOSE 3000
    
    # Health check
    HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
      CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
    
    CMD ["node", "index.js"]
    
    
    # Secrets at runtime, not build time
    # WRONG: ARG with secrets
    ARG API_KEY
    ENV API_KEY=$API_KEY
    
    # RIGHT: Runtime environment
    # docker run -e API_KEY=secret myimage
    # Or use Docker secrets / Kubernetes secrets
    
    
    # Use distroless for even smaller attack surface
    FROM gcr.io/distroless/nodejs20-debian12
    COPY --from=builder /app/dist /app
    WORKDIR /app
    CMD ["index.js"]
    

---
  #### **Name**
.dockerignore
  #### **Description**
Exclude files from build context
  #### **When**
Every Dockerfile
  #### **Example**
    # .DOCKERIGNORE:
    
    """
    Like .gitignore but for Docker build context.
    Reduces build time and image size.
    Prevents secrets from accidentally being copied.
    """
    
    # .dockerignore
    # Dependencies (reinstalled in container)
    node_modules
    vendor
    __pycache__
    
    # Build outputs
    dist
    build
    *.pyc
    *.pyo
    
    # Development files
    .git
    .gitignore
    .env
    .env.*
    *.md
    docs
    
    # IDE
    .vscode
    .idea
    *.swp
    
    # Tests
    tests
    __tests__
    *.test.js
    *.spec.js
    coverage
    
    # Docker files (prevent recursion)
    Dockerfile*
    docker-compose*
    .docker
    
    # Secrets (CRITICAL)
    *.pem
    *.key
    .env.local
    secrets/
    

---
  #### **Name**
Health Checks
  #### **Description**
Container health monitoring
  #### **When**
Production deployments
  #### **Example**
    # HEALTH CHECKS:
    
    """
    Health checks let orchestrators know if container is ready.
    Kubernetes, Docker Swarm, and ECS all use them.
    """
    
    # In Dockerfile
    HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
      CMD curl -f http://localhost:3000/health || exit 1
    
    # For containers without curl
    HEALTHCHECK --interval=30s --timeout=3s \
      CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
    
    # In docker-compose.yml
    services:
      app:
        build: .
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
          interval: 30s
          timeout: 10s
          retries: 3
          start_period: 40s
    
    
    # Application health endpoint
    // Node.js
    app.get('/health', (req, res) => {
      // Check dependencies
      const healthy = await checkDatabase() && await checkRedis();
      if (healthy) {
        res.status(200).json({ status: 'healthy' });
      } else {
        res.status(503).json({ status: 'unhealthy' });
      }
    });
    

## Anti-Patterns


---
  #### **Name**
Huge Base Images
  #### **Description**
Using full OS images when slim/alpine works
  #### **Why**
    A full Ubuntu image is 70MB+. Alpine is 5MB. Larger images mean
    slower pulls, more storage, larger attack surface, more CVEs.
    
  #### **Instead**
    # WRONG: Full image
    FROM node:20
    FROM python:3.12
    FROM ubuntu:22.04
    
    # RIGHT: Minimal images
    FROM node:20-alpine
    FROM python:3.12-slim
    FROM alpine:3.19
    
    # BEST: Distroless (no shell, minimal attack surface)
    FROM gcr.io/distroless/nodejs20
    

---
  #### **Name**
Running as Root
  #### **Description**
Container process running as UID 0
  #### **Why**
    If an attacker breaks out of your app, they're root in the container.
    Container escapes are real, and root makes them much worse.
    
  #### **Instead**
    # Create and use non-root user
    RUN addgroup -S app && adduser -S app -G app
    USER app
    
    # Or use numeric UID
    USER 1000:1000
    

---
  #### **Name**
Latest Tag
  #### **Description**
Using :latest or no tag for base images
  #### **Why**
    :latest changes unpredictably. Your build works today, fails tomorrow.
    You can't reproduce builds, can't audit dependencies.
    
  #### **Instead**
    # WRONG
    FROM node:latest
    FROM node
    
    # RIGHT: Pin major.minor at minimum
    FROM node:20.10-alpine
    
    # BEST: Pin digest for reproducibility
    FROM node:20.10-alpine@sha256:abc123...
    

---
  #### **Name**
Secrets in Image
  #### **Description**
Baking secrets into the image at build time
  #### **Why**
    Anyone with access to the image can extract secrets. Image layers
    are visible. Even "deleted" secrets exist in layer history.
    
  #### **Instead**
    # WRONG: Secret in image
    ENV API_KEY=sk_live_xxxxx
    COPY .env /app/.env
    
    # RIGHT: Runtime injection
    # docker run -e API_KEY=xxx myimage
    
    # RIGHT: Docker secrets
    # docker secret create api_key key.txt
    # In compose: secrets: [api_key]
    
    # RIGHT: Mount read-only secrets
    # docker run -v ./secrets:/run/secrets:ro myimage
    

---
  #### **Name**
No .dockerignore
  #### **Description**
Missing .dockerignore file
  #### **Why**
    Without .dockerignore, COPY . . includes everything: node_modules,
    .git, secrets, test files. Builds are slow, images are huge,
    secrets may leak.
    
  #### **Instead**
    # Always create .dockerignore
    node_modules
    .git
    .env*
    *.md
    tests
    coverage
    