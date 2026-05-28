# Docker Containerization

## Patterns


---
  #### **Name**
Production Multi-Stage Build
  #### **Description**
Separate build dependencies from runtime for minimal, secure images
  #### **When**
Any production container image
  #### **Example**
    # Build stage - has all build tools
    FROM node:20-alpine AS builder
    WORKDIR /app
    
    # Copy package files first for layer caching
    COPY package*.json ./
    RUN npm ci --only=production
    
    # Copy source and build
    COPY . .
    RUN npm run build
    
    # Production stage - minimal runtime
    FROM node:20-alpine AS production
    WORKDIR /app
    
    # Create non-root user
    RUN addgroup -g 1001 -S nodejs && \
        adduser -S nodejs -u 1001
    
    # Copy only production artifacts
    COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
    COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
    COPY --from=builder --chown=nodejs:nodejs /app/package.json ./
    
    # Security hardening
    USER nodejs
    EXPOSE 3000
    
    # Health check
    HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
      CMD node healthcheck.js || exit 1
    
    # Use exec form for proper signal handling
    CMD ["node", "dist/server.js"]
    

---
  #### **Name**
Optimal Layer Caching
  #### **Description**
Order Dockerfile commands to maximize cache hits
  #### **When**
Any Dockerfile that takes too long to build
  #### **Example**
    # WRONG: Copy everything, then install - cache busted on any file change
    COPY . .
    RUN npm install
    
    # RIGHT: Copy dependency files first, then install, then copy rest
    # Base image (changes rarely)
    FROM node:20-alpine
    WORKDIR /app
    
    # Dependencies (changes occasionally) - cached unless package.json changes
    COPY package.json package-lock.json ./
    RUN npm ci
    
    # Source code (changes frequently) - only rebuilds from here
    COPY . .
    RUN npm run build
    
    # For Python:
    COPY requirements.txt ./
    RUN pip install -r requirements.txt
    COPY . .
    
    # For Go:
    COPY go.mod go.sum ./
    RUN go mod download
    COPY . .
    

---
  #### **Name**
Distroless Production Image
  #### **Description**
Minimal base image with no shell, no package manager, minimal CVEs
  #### **When**
Maximum security requirements, Go/Rust/Java applications
  #### **Example**
    # Build stage
    FROM golang:1.22-alpine AS builder
    WORKDIR /app
    COPY go.mod go.sum ./
    RUN go mod download
    COPY . .
    RUN CGO_ENABLED=0 GOOS=linux go build -o /app/server
    
    # Production - distroless has no shell, minimal attack surface
    FROM gcr.io/distroless/static-debian12
    
    # Copy binary
    COPY --from=builder /app/server /server
    
    # Run as non-root (distroless supports numeric UID)
    USER 1000
    
    ENTRYPOINT ["/server"]
    
    # Note: Can't use shell form, can't docker exec into container
    # For debugging, use a debug variant:
    # FROM gcr.io/distroless/static-debian12:debug
    # This adds busybox shell at /busybox/sh
    

---
  #### **Name**
Proper Signal Handling
  #### **Description**
Handle SIGTERM for graceful shutdown
  #### **When**
Any container that needs graceful shutdown
  #### **Example**
    # WRONG: Shell form - shell is PID 1, doesn't forward signals
    CMD npm start
    # Docker sends SIGTERM to sh, not to node
    
    # RIGHT: Exec form - node is PID 1, receives signals directly
    CMD ["node", "server.js"]
    
    # RIGHT: If you need shell script, use exec
    # entrypoint.sh
    #!/bin/sh
    # Setup code here...
    exec node server.js  # exec replaces shell process
    
    # RIGHT: Use tini for proper init
    FROM node:20-alpine
    RUN apk add --no-cache tini
    ENTRYPOINT ["/sbin/tini", "--"]
    CMD ["node", "server.js"]
    
    # RIGHT: Use --init flag at runtime
    docker run --init myimage
    
    # In your Node.js code, handle SIGTERM:
    process.on('SIGTERM', async () => {
      console.log('SIGTERM received, shutting down gracefully');
      server.close(() => {
        console.log('HTTP server closed');
        process.exit(0);
      });
      // Force exit after timeout
      setTimeout(() => process.exit(1), 30000);
    });
    

---
  #### **Name**
Secure .dockerignore
  #### **Description**
Prevent secrets and unnecessary files from entering build context
  #### **When**
Every Dockerfile (no exceptions)
  #### **Example**
    # .dockerignore - MUST be in root of build context
    
    # Git
    .git
    .gitignore
    
    # Dependencies (reinstalled in container)
    node_modules
    __pycache__
    venv
    .venv
    vendor
    
    # Secrets and environment
    .env
    .env.*
    *.pem
    *.key
    .aws
    .npmrc
    .docker
    credentials.json
    secrets/
    
    # Build artifacts
    dist
    build
    coverage
    .nyc_output
    
    # IDE and editor
    .vscode
    .idea
    *.swp
    *.swo
    
    # Docker files (recursive builds)
    Dockerfile*
    docker-compose*
    .dockerignore
    
    # Logs and temp
    *.log
    tmp
    temp
    
    # Documentation
    README*
    docs
    *.md
    
    # Tests (unless needed in image)
    test
    tests
    __tests__
    *.test.js
    *.spec.js
    

---
  #### **Name**
Health Check Configuration
  #### **Description**
Enable container orchestrators to detect unhealthy containers
  #### **When**
Any production container
  #### **Example**
    # In Dockerfile
    HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
      CMD curl -f http://localhost:3000/health || exit 1
    
    # For images without curl
    HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
      CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"
    
    # For Go binaries
    HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
      CMD ["/app/healthcheck"]
    
    # Health check endpoints should:
    # 1. Be fast (< 1 second)
    # 2. Check internal state only (not dependencies)
    # 3. Return 200 if healthy, non-200 if not
    # 4. Not have authentication
    

## Anti-Patterns


---
  #### **Name**
Running as Root
  #### **Description**
Container processes running as root user
  #### **Why**
Container escapes become full node compromises. 58% of production containers still run as root (Sysdig 2024). One vulnerability and attacker has root access.
  #### **Instead**
Create non-root user in Dockerfile. Use USER directive. Set runAsNonRoot in Kubernetes.

---
  #### **Name**
Using :latest Tag
  #### **Description**
Base images or your own images with :latest tag
  #### **Why**
Non-deterministic builds. "Works on my machine" but fails in production. Can't rollback - :latest already changed. No audit trail of what version deployed.
  #### **Instead**
Pin exact versions (node:20.10.0-alpine). Use SHA digests for maximum reproducibility.

---
  #### **Name**
No .dockerignore
  #### **Description**
Missing or incomplete .dockerignore file
  #### **Why**
Build context includes secrets (.env, .aws, credentials), node_modules (wrong platform binaries), git history. 2GB context uploaded for 50MB image.
  #### **Instead**
Create comprehensive .dockerignore. Review before every build what's included.

---
  #### **Name**
Single-Stage Builds for Production
  #### **Description**
Including build tools in production image
  #### **Why**
Image has gcc, make, npm, dev dependencies - 2GB instead of 200MB. More CVEs, slower deploys, larger attack surface.
  #### **Instead**
Multi-stage builds. Build in one stage, copy artifacts to minimal production stage.

---
  #### **Name**
Shell Form CMD
  #### **Description**
Using CMD npm start instead of CMD ["node", "server.js"]
  #### **Why**
Shell becomes PID 1. Signals not forwarded to application. SIGTERM ignored. Container takes 30 seconds to stop (timeout + SIGKILL). Requests in flight lost.
  #### **Instead**
Use exec form. Use tini/dumb-init. Use --init flag. Handle signals in application.

---
  #### **Name**
One Big RUN Layer
  #### **Description**
Combining everything into single RUN command for "smaller image"
  #### **Why**
Cache invalidation. Change one package, rebuild everything. 20-minute builds because apt-get runs every time.
  #### **Instead**
Logical layer separation. Dependencies in one layer, app in another. Use BuildKit cache mounts.

---
  #### **Name**
ADD Instead of COPY
  #### **Description**
Using ADD for simple file copies
  #### **Why**
ADD auto-extracts archives, downloads URLs - unexpected behavior. Security risk if URL content changes. Less explicit than COPY.
  #### **Instead**
Use COPY for files. Use RUN curl for downloads (explicit, cacheable).