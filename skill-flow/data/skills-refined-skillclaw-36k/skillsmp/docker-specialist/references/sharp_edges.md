# Docker Specialist - Sharp Edges

## Running As Root

### **Id**
running-as-root
### **Summary**
Container running as root allows host compromise
### **Severity**
critical
### **Situation**
Production containers
### **Why**
  Container escape vulnerability + root = root on host. CVEs like
  CVE-2019-5736 (runc) allowed exactly this. Even without escape,
  root can modify mounted volumes, access secrets, compromise
  the entire deployment.
  
### **Solution**
  1. Create and use non-root user:
     FROM node:20-alpine
     RUN addgroup -g 1001 -S nodejs && \
         adduser -S nextjs -u 1001
  
     USER nextjs
     CMD ["node", "server.js"]
  
  2. Use --user flag at runtime:
     docker run --user 1001:1001 myimage
  
  3. In Kubernetes, set securityContext:
     securityContext:
       runAsNonRoot: true
       runAsUser: 1001
  
  4. For images that require root (e.g., nginx):
     - Use unprivileged variants (nginx-unprivileged)
     - Or start as root, drop privileges in entrypoint
  
  5. Scan images for root usage:
     docker inspect --format='{{.Config.User}}' image
  
### **Symptoms**
  - Security audit failures
  - Container escape possible
  - Production policy violations
### **Detection Pattern**
USER root|ENTRYPOINT.*root|runAsUser.*0

## Secrets In Image

### **Id**
secrets-in-image
### **Summary**
Secrets baked into Docker image are visible
### **Severity**
critical
### **Situation**
Needing credentials during build
### **Why**
  ARG API_KEY=secret
  RUN curl -H "Auth: $API_KEY" https://...
  
  The secret is now in image layers. Anyone with image access (registry,
  developer, logs) can extract it. docker history shows all ARGs.
  This has caused countless credential leaks.
  
### **Solution**
  1. Use build secrets (BuildKit):
     # syntax=docker/dockerfile:1.4
     RUN --mount=type=secret,id=api_key \
         API_KEY=$(cat /run/secrets/api_key) && \
         curl -H "Auth: $API_KEY" https://...
  
     # Build with:
     docker build --secret id=api_key,src=./api_key.txt .
  
  2. Use runtime environment variables:
     docker run -e API_KEY=secret myimage
  
  3. Use mounted secret files:
     docker run -v ./secrets:/run/secrets:ro myimage
  
  4. In Kubernetes, use Secrets:
     volumes:
       - name: secrets
         secret:
           secretName: api-secrets
  
  5. Never commit secrets to Dockerfile or .env
  
### **Symptoms**
  - Credentials in container logs
  - Secrets visible in registry
  - Security audit failure
### **Detection Pattern**
ARG.*KEY|ARG.*SECRET|ARG.*PASSWORD|ENV.*=.*secret

## Latest Tag

### **Id**
latest-tag
### **Summary**
Using :latest tag breaks reproducibility
### **Severity**
high
### **Situation**
Image references in production
### **Why**
  FROM node:latest
  Today: Node 20. Tomorrow: Node 22 (breaking changes).
  Your CI passes, production breaks. Different machines pull
  different versions. Debugging becomes impossible.
  
### **Solution**
  1. Always use specific tags:
     FROM node:20.10.0-alpine3.19
  
  2. For even more reproducibility, use digest:
     FROM node@sha256:abc123...
  
  3. Pin in compose/K8s too:
     image: myapp:1.2.3
     # Not: image: myapp:latest
  
  4. Use semantic versioning in your images:
     docker build -t myapp:1.2.3 -t myapp:1.2 -t myapp:1 .
  
  5. Exception: Development/local where latest is convenient
  
### **Symptoms**
  - Works locally, fails in CI
  - Inconsistent behavior across environments
  - Unable to reproduce issues
### **Detection Pattern**
:latest|FROM.*:(?!.*\.)

## No Healthcheck

### **Id**
no-healthcheck
### **Summary**
No health check means dead containers appear healthy
### **Severity**
high
### **Situation**
Production containers
### **Why**
  Your app crashes but process stays alive. Or it's deadlocked.
  Container status: running. Reality: not serving requests.
  Load balancer keeps sending traffic. Users see errors.
  
### **Solution**
  1. Add HEALTHCHECK in Dockerfile:
     HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
         CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
  
  2. Health endpoint should check dependencies:
     app.get('/health', async (req, res) => {
       try {
         await db.query('SELECT 1');
         await redis.ping();
         res.json({ status: 'healthy' });
       } catch (err) {
         res.status(503).json({ status: 'unhealthy' });
       }
     });
  
  3. In Kubernetes, use probes:
     livenessProbe:
       httpGet:
         path: /health
         port: 3000
       initialDelaySeconds: 10
       periodSeconds: 30
  
  4. Distinguish liveness vs readiness:
     - Liveness: Is the process alive? (restart if not)
     - Readiness: Can it serve traffic? (remove from LB if not)
  
### **Symptoms**
  - Traffic sent to dead containers
  - Cascading failures
  - Long MTTR for incidents
### **Detection Pattern**
HEALTHCHECK(?!.*CMD)|docker run(?!.*health)

## No Signal Handling

### **Id**
no-signal-handling
### **Summary**
Container doesn't handle SIGTERM gracefully
### **Severity**
medium
### **Situation**
Container shutdown and restarts
### **Why**
  Kubernetes sends SIGTERM, waits grace period, then SIGKILL.
  If your app ignores SIGTERM, connections drop mid-request,
  data corrupts, transactions abort. Every deployment causes errors.
  
### **Solution**
  1. Handle shutdown in application:
     process.on('SIGTERM', async () => {
       console.log('SIGTERM received, shutting down gracefully');
       await server.close();
       await db.end();
       process.exit(0);
     });
  
  2. Use dumb-init or tini as init:
     RUN apk add --no-cache tini
     ENTRYPOINT ["/sbin/tini", "--"]
     CMD ["node", "server.js"]
  
  3. Set appropriate grace period:
     terminationGracePeriodSeconds: 30
  
  4. For long-running tasks, checkpoint progress
  
  5. Test shutdown: docker stop (SIGTERM) vs docker kill (SIGKILL)
  
### **Symptoms**
  - Errors during deployments
  - In-flight requests fail
  - Data consistency issues
### **Detection Pattern**
CMD \[(?!.*tini|.*dumb-init)|ENTRYPOINT(?!.*init)

## Layer Cache Busting

### **Id**
layer-cache-busting
### **Summary**
Inefficient Dockerfile busts cache on every build
### **Severity**
medium
### **Situation**
Slow Docker builds
### **Why**
  COPY . .
  RUN npm install
  
  Every code change copies everything, busting cache, reinstalling
  all dependencies. 5 minute builds become the norm. Developers
  skip Docker, "works on my machine" returns.
  
### **Solution**
  1. Order by change frequency (least → most):
     # System packages (rarely change)
     RUN apt-get update && apt-get install -y ...
  
     # Dependencies (change occasionally)
     COPY package*.json ./
     RUN npm ci
  
     # Source code (changes frequently)
     COPY . .
     RUN npm run build
  
  2. Use .dockerignore aggressively:
     .git
     node_modules
     dist
     *.log
     .env*
     Dockerfile*
     README.md
  
  3. Use BuildKit cache mounts:
     RUN --mount=type=cache,target=/root/.npm npm ci
  
  4. Separate build and runtime stages:
     FROM node:20 AS builder
     # ... build steps
     FROM node:20-alpine AS production
     COPY --from=builder /app/dist ./dist
  
### **Symptoms**
  - Slow builds (minutes for small changes)
  - High CI costs
  - Developers avoid Docker
### **Detection Pattern**
COPY \. \./RUN npm|COPY.*RUN.*install

## Massive Image Size

### **Id**
massive-image-size
### **Summary**
Multi-gigabyte images slow deployments
### **Severity**
medium
### **Situation**
Production image deployment
### **Why**
  Development image: 2GB (includes build tools, source, everything).
  Pull time: minutes. Registry storage: expensive. Startup: slow.
  Rollback: even slower. Attack surface: massive.
  
### **Solution**
  1. Use alpine base images:
     FROM node:20-alpine  # ~100MB vs ~1GB for node:20
  
  2. Multi-stage builds:
     FROM node:20 AS builder
     RUN npm run build
  
     FROM node:20-alpine AS production
     COPY --from=builder /app/dist ./dist
     COPY --from=builder /app/node_modules ./node_modules
  
  3. Only install production dependencies:
     RUN npm ci --only=production
  
  4. Remove unnecessary files:
     RUN rm -rf /var/cache/apk/* /tmp/*
  
  5. Use distroless for compiled languages:
     FROM gcr.io/distroless/base
  
  6. Check image size regularly:
     docker images | sort -k7 -h
  
### **Symptoms**
  - Slow deployments
  - High registry costs
  - Long pod startup time
### **Detection Pattern**
FROM.*(?<!alpine|slim|distroless)$|npm install(?!.*production)

## Pid 1 Zombie

### **Id**
pid-1-zombie
### **Summary**
Zombie processes accumulate in container
### **Severity**
medium
### **Situation**
Long-running containers spawning child processes
### **Why**
  Docker runs your process as PID 1. Normal init reaps zombies.
  Your app doesn't. Each child process that terminates becomes
  a zombie. Eventually you hit process limits, container fails.
  
### **Solution**
  1. Use tini or dumb-init:
     FROM node:20-alpine
     RUN apk add --no-cache tini
  
     ENTRYPOINT ["/sbin/tini", "--"]
     CMD ["node", "server.js"]
  
  2. Docker's built-in init (simpler):
     docker run --init myimage
  
  3. In compose:
     services:
       app:
         init: true
  
  4. In Kubernetes:
     securityContext:
       # No direct support, use init in image
  
  5. Or handle signals yourself (harder):
     // node.js - not recommended for complex cases
     process.on('SIGCHLD', ...);
  
### **Symptoms**
  - `ps aux` shows many zombie processes
  - Container eventually fails
  - Resource exhaustion
### **Detection Pattern**
ENTRYPOINT(?!.*tini|.*dumb-init)|CMD(?!.*init)