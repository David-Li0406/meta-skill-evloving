# Docker - Sharp Edges

## Secrets In Layers

### **Id**
secrets-in-layers
### **Summary**
Secrets in image layers are visible even if "deleted"
### **Severity**
critical
### **Situation**
  You copy a .env file, use it, then delete it. Or you pass secrets
  as build args. The secret is visible in image layer history.
  Anyone with docker history or image pull can see it.
  
### **Why**
  Docker images are layers stacked on top of each other. Each layer
  is immutable. "Deleting" a file in a later layer just hides it -
  the original layer still contains it.
  
### **Solution**
  # NEVER PUT SECRETS IN IMAGES
  
  # WRONG: Secret in build arg (visible in history)
  ARG API_KEY
  ENV API_KEY=$API_KEY
  
  # WRONG: Copy then delete (still in layer)
  COPY .env /app/
  RUN source .env && rm .env
  
  # RIGHT: Runtime environment variable
  CMD ["node", "index.js"]
  # docker run -e API_KEY=secret myimage
  
  # RIGHT: Docker BuildKit secrets (never in layer)
  # syntax=docker/dockerfile:1
  RUN --mount=type=secret,id=api_key \
      API_KEY=$(cat /run/secrets/api_key) ./configure
  
  # docker build --secret id=api_key,src=./api_key.txt .
  
  # RIGHT: Multi-stage (secret only in build stage)
  FROM builder AS authenticated
  ARG NPM_TOKEN
  RUN echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc
  RUN npm ci
  RUN rm .npmrc
  
  FROM node:alpine
  COPY --from=authenticated /app/node_modules ./node_modules
  # NPM_TOKEN not in final image
  
### **Symptoms**
  - Secrets visible in docker history
  - Credentials in pulled images
  - Security audit failures
### **Detection Pattern**
ARG\s+(API_KEY|SECRET|PASSWORD|TOKEN)

## Root User Default

### **Id**
root-user-default
### **Summary**
Container runs as root by default
### **Severity**
high
### **Situation**
  You don't specify a USER in your Dockerfile. The container runs
  as root (UID 0). If your app is compromised, the attacker has
  root access inside the container.
  
### **Why**
  Docker defaults to root. Container escape vulnerabilities exist.
  With root, an attacker can modify system files, install packages,
  and potentially break out to the host.
  
### **Solution**
  # RUN AS NON-ROOT USER
  
  # Create user in Dockerfile
  FROM node:20-alpine
  
  # Create non-root user
  RUN addgroup -S appgroup && \
      adduser -S appuser -G appgroup
  
  WORKDIR /app
  
  # Change ownership of app files
  COPY --chown=appuser:appgroup . .
  
  # Switch to non-root before running
  USER appuser
  
  CMD ["node", "index.js"]
  
  
  # Verify at runtime
  docker run myimage whoami  # Should not be "root"
  
  # Or use numeric UID (works even without user in image)
  docker run --user 1000:1000 myimage
  
  # In Kubernetes
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
  
### **Symptoms**
  - whoami returns "root"
  - Process runs as UID 0
  - Security scan warnings
### **Detection Pattern**
(?<!#.*)(FROM|ENTRYPOINT|CMD)(?![\s\S]*USER\s+\w)

## Cache Busting Unintentional

### **Id**
cache-busting-unintentional
### **Summary**
Copy order causes unnecessary rebuilds
### **Severity**
medium
### **Situation**
  You COPY . . early in the Dockerfile. Any file change invalidates
  the cache. Dependencies reinstall on every build. Build times
  are 5 minutes instead of 30 seconds.
  
### **Why**
  Docker caches layers. If a layer changes, all following layers
  rebuild. Copying all files early means dependency installation
  (a slow step) rebuilds on any code change.
  
### **Solution**
  # ORDER FOR CACHE EFFICIENCY
  
  # WRONG: Copy everything first
  FROM node:20-alpine
  WORKDIR /app
  COPY . .                    # Any change invalidates
  RUN npm ci                  # Reinstalls every time
  RUN npm run build
  
  # RIGHT: Dependencies before code
  FROM node:20-alpine
  WORKDIR /app
  
  # Step 1: Only dependency files
  COPY package.json package-lock.json ./
  
  # Step 2: Install (cached if package files unchanged)
  RUN npm ci
  
  # Step 3: Copy source (changes often)
  COPY . .
  
  # Step 4: Build
  RUN npm run build
  
  # Order from least to most frequently changed:
  # 1. Base image selection
  # 2. System dependencies (apt-get)
  # 3. Language dependencies (package.json, requirements.txt)
  # 4. Application code
  # 5. Build step
  
### **Symptoms**
  - Slow builds for small code changes
  - "npm install" runs every build
  - No layer cache hits
### **Detection Pattern**
COPY\s+\.\s+\.[\s\S]*RUN\s+(npm|pip|go)\s+(install|ci|build)

## Latest Tag

### **Id**
latest-tag
### **Summary**
Using :latest tag causes unpredictable builds
### **Severity**
medium
### **Situation**
  You use FROM node:latest or FROM python. Build works fine. A
  week later, the base image updates, and your build breaks with
  no code changes.
  
### **Why**
  :latest is a moving target. It points to whatever was pushed last.
  You can't reproduce builds, can't track what changed, can't roll
  back to a known-working state.
  
### **Solution**
  # PIN YOUR BASE IMAGES
  
  # WRONG: Latest (unpredictable)
  FROM node:latest
  FROM node
  FROM python
  
  # RIGHT: Pin major.minor
  FROM node:20.10-alpine
  FROM python:3.12-slim
  
  # BEST: Pin digest for exact reproducibility
  FROM node:20.10-alpine@sha256:abc123def456...
  
  # Find digest:
  docker pull node:20.10-alpine
  docker inspect node:20.10-alpine --format='{{index .RepoDigests 0}}'
  
  # Update intentionally:
  # 1. Update version in Dockerfile
  # 2. Test
  # 3. Commit change
  
### **Symptoms**
  - "Worked yesterday" failures
  - Different behavior across builds
  - Can't reproduce issues
### **Detection Pattern**
FROM\s+\w+:(latest|$)

## No Dockerignore

### **Id**
no-dockerignore
### **Summary**
Missing .dockerignore includes unnecessary files
### **Severity**
medium
### **Situation**
  You COPY . . without a .dockerignore. The entire .git folder,
  node_modules, test files, and maybe secrets get copied into
  the image.
  
### **Why**
  COPY sends the build context to the Docker daemon. Without
  .dockerignore, this includes everything. Builds are slow,
  images are huge, and secrets may leak.
  
### **Solution**
  # ALWAYS CREATE .DOCKERIGNORE
  
  # .dockerignore
  # Version control
  .git
  .gitignore
  .svn
  
  # Dependencies (install in container)
  node_modules
  vendor
  __pycache__
  *.pyc
  
  # Build artifacts
  dist
  build
  coverage
  
  # Development
  .env
  .env.*
  *.md
  docs
  tests
  __tests__
  
  # IDE
  .vscode
  .idea
  *.swp
  *.swo
  
  # Secrets
  *.pem
  *.key
  secrets/
  
  # Docker
  Dockerfile*
  docker-compose*
  
### **Symptoms**
  - Large build context
  - Slow docker build
  - node_modules in image
  - Secrets in image
### **Detection Pattern**


## Multiple Processes

### **Id**
multiple-processes
### **Summary**
Running multiple processes in one container
### **Severity**
medium
### **Situation**
  You run nginx, app server, and cron in one container. One crashes,
  and you can't tell. Container shows "running" but nginx is dead.
  
### **Why**
  Docker monitors PID 1. If you run multiple processes with a script,
  PID 1 is the script, not your app. When the app crashes, Docker
  doesn't know. Logs are mixed, health checks don't work.
  
### **Solution**
  # ONE PROCESS PER CONTAINER
  
  # WRONG: Multiple processes
  CMD ["sh", "-c", "nginx & node app.js"]
  
  # RIGHT: Separate containers
  # docker-compose.yml
  services:
    nginx:
      image: nginx:alpine
      volumes:
        - ./nginx.conf:/etc/nginx/nginx.conf
      depends_on:
        - app
  
    app:
      build: .
      command: ["node", "app.js"]
  
  # If you MUST run multiple (rare):
  # Use a process manager like tini or dumb-init as PID 1
  FROM node:alpine
  RUN apk add --no-cache tini
  ENTRYPOINT ["/sbin/tini", "--"]
  CMD ["node", "app.js"]
  
### **Symptoms**
  - Container "running" but app dead
  - Mixed logs, hard to debug
  - Health checks don't detect failures
### **Detection Pattern**
CMD.*&.*&|ENTRYPOINT.*&&

## Apt Get Upgrade

### **Id**
apt-get-upgrade
### **Summary**
Running apt-get upgrade in Dockerfile
### **Severity**
low
### **Situation**
  You run apt-get upgrade to "ensure security patches." Builds
  become unpredictable. Image size grows. You're doing the base
  image maintainer's job.
  
### **Why**
  Base image maintainers apply security patches. Running upgrade
  yourself creates inconsistency, larger images, and cache problems.
  If you need a patch, update to a newer base image tag.
  
### **Solution**
  # DON'T UPGRADE IN DOCKERFILE
  
  # WRONG: Upgrade packages
  RUN apt-get update && \
      apt-get upgrade -y && \
      apt-get install -y curl
  
  # RIGHT: Just install what you need
  RUN apt-get update && \
      apt-get install -y --no-install-recommends curl && \
      rm -rf /var/lib/apt/lists/*
  
  # For security updates, update base image:
  # FROM node:20.9-slim  ->  FROM node:20.10-slim
  
### **Symptoms**
  - Large image size
  - Slow builds
  - Inconsistent builds
### **Detection Pattern**
apt-get\s+upgrade