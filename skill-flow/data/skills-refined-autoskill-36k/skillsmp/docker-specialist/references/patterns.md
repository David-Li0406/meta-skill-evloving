# Docker Specialist

## Patterns


---
  #### **Name**
Optimized Multi-Stage Build
  #### **Description**
Minimal production images with fast builds
  #### **When**
Any production Docker image
  #### **Example**
    # Build stage - has all build tools
    FROM node:20-alpine AS builder
    
    WORKDIR /app
    
    # Copy package files first (rarely change)
    COPY package*.json ./
    
    # Install dependencies (cached unless package.json changes)
    RUN npm ci --only=production && \
        npm cache clean --force
    
    # Install dev dependencies for build
    RUN npm ci
    
    # Copy source (changes frequently - last layer)
    COPY . .
    
    # Build application
    RUN npm run build
    
    # Production stage - minimal image
    FROM node:20-alpine AS production
    
    # Don't run as root
    RUN addgroup -g 1001 -S nodejs && \
        adduser -S nextjs -u 1001
    
    WORKDIR /app
    
    # Copy only production dependencies from builder
    COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
    COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
    COPY --from=builder --chown=nextjs:nodejs /app/package.json ./
    
    USER nextjs
    
    EXPOSE 3000
    
    ENV NODE_ENV=production
    
    CMD ["node", "dist/index.js"]
    

---
  #### **Name**
Docker Compose for Development
  #### **Description**
Local development environment with services
  #### **When**
Multi-service development setup
  #### **Example**
    version: '3.8'
    
    services:
      app:
        build:
          context: .
          dockerfile: Dockerfile
          target: development  # Use dev stage
        ports:
          - "3000:3000"
        volumes:
          # Mount source for hot reload
          - .:/app
          # Don't mount node_modules (use container's)
          - /app/node_modules
        environment:
          - NODE_ENV=development
          - DATABASE_URL=postgres://user:pass@db:5432/app
          - REDIS_URL=redis://cache:6379
        depends_on:
          db:
            condition: service_healthy
          cache:
            condition: service_started
    
      db:
        image: postgres:16-alpine
        environment:
          POSTGRES_USER: user
          POSTGRES_PASSWORD: pass
          POSTGRES_DB: app
        volumes:
          - postgres_data:/var/lib/postgresql/data
          - ./init.sql:/docker-entrypoint-initdb.d/init.sql
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U user -d app"]
          interval: 5s
          timeout: 5s
          retries: 5
    
      cache:
        image: redis:7-alpine
        volumes:
          - redis_data:/data
    
    volumes:
      postgres_data:
      redis_data:
    

---
  #### **Name**
Security Hardening
  #### **Description**
Secure container configuration
  #### **When**
Production containers
  #### **Example**
    # Use specific version, not :latest
    FROM node:20.10.0-alpine3.19
    
    # Update packages and remove cache
    RUN apk update && \
        apk upgrade && \
        apk add --no-cache dumb-init && \
        rm -rf /var/cache/apk/*
    
    # Create non-root user
    RUN addgroup -g 1001 -S appgroup && \
        adduser -u 1001 -S appuser -G appgroup
    
    WORKDIR /app
    
    # Copy with correct ownership
    COPY --chown=appuser:appgroup . .
    
    # Switch to non-root user
    USER appuser
    
    # Use dumb-init to handle signals properly
    ENTRYPOINT ["dumb-init", "--"]
    
    # Health check
    HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
        CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
    
    CMD ["node", "dist/index.js"]
    
    # In docker run or compose:
    # --security-opt=no-new-privileges:true
    # --read-only
    # --cap-drop=ALL
    

---
  #### **Name**
Layer Caching Strategy
  #### **Description**
Maximizing Docker build cache hits
  #### **When**
Optimizing build times
  #### **Example**
    # LAYERS ORDERED BY CHANGE FREQUENCY (least → most)
    
    # 1. Base image and system packages (rarely change)
    FROM python:3.12-slim
    
    RUN apt-get update && \
        apt-get install -y --no-install-recommends \
          build-essential \
          libpq-dev && \
        rm -rf /var/lib/apt/lists/*
    
    WORKDIR /app
    
    # 2. Dependency files (change occasionally)
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # 3. Source code (changes frequently)
    COPY . .
    
    # .dockerignore is critical:
    # .git
    # __pycache__
    # *.pyc
    # .env*
    # .venv
    # node_modules
    # dist
    # *.log
    # .DS_Store
    # Dockerfile*
    # docker-compose*
    # README.md
    # tests/
    # .github/
    

## Anti-Patterns


---
  #### **Name**
Using :latest Tag
  #### **Description**
Pulling images without specific version
  #### **Why**
Non-reproducible builds, surprise breaking changes
  #### **Instead**
Pin exact version (node:20.10.0-alpine3.19)

---
  #### **Name**
Running as Root
  #### **Description**
Container processes running as root user
  #### **Why**
Container escape = root on host, massive security risk
  #### **Instead**
Create non-root user, use USER directive

---
  #### **Name**
Secrets in Image
  #### **Description**
Embedding API keys, passwords in Dockerfile
  #### **Why**
Secrets in image layers, visible in registry
  #### **Instead**
Use Docker secrets, environment variables, mounted files

---
  #### **Name**
Installing SSH/Debug Tools
  #### **Description**
Including debugging utilities in production images
  #### **Why**
Increases attack surface, image size, CVE exposure
  #### **Instead**
Use ephemeral debug containers when needed

---
  #### **Name**
Single Massive Layer
  #### **Description**
One RUN command with everything
  #### **Why**
No cache reuse, slow builds, hard to debug
  #### **Instead**
Logical layer separation by change frequency