# Docker First-Time Setup

Detailed setup guide for configuring Docker development environments in new projects.

---

## Step 1: Answer Configuration Questions

Before setting up Docker for a new project, determine your requirements:

**Q1: Does your project use native Node.js modules?**

Native modules compile C/C++ code and have specific OS requirements.

| Module | Native? | Requires glibc? |
|--------|---------|-----------------|
| `better-sqlite3` | Yes | Yes |
| `onnxruntime-node` | Yes | Yes |
| `sharp` | Yes | Yes |
| `bcrypt` | Yes | Yes |
| `node-gyp` builds | Yes | Usually |
| Pure JS packages | No | No |

**Check your package.json:**
```bash
# Look for native module indicators
grep -E "node-gyp|prebuild|nan|napi" package.json package-lock.json 2>/dev/null | head -5
```

**Q2: What's your priority?**

| Priority | Recommended Base Image |
|----------|------------------------|
| Smallest image size | `node:20-alpine` (if no native modules) |
| Maximum compatibility | `node:20-slim` (Debian, has glibc) |
| Full tooling | `node:20` (full Debian) |

---

## Step 2: Create Project Configuration

Create `.claude/docker-config.json` in your project root:

```json
{
  "containerName": "my-project-dev-1",
  "baseImage": "node:20-slim",
  "port": 3000,
  "hasNativeModules": true,
  "devCommand": "npm run dev -- --host 0.0.0.0"
}
```

**Configuration Options:**

| Field | Description | Examples |
|-------|-------------|----------|
| `containerName` | Docker container name | `myapp-dev-1`, `api-dev-1` |
| `baseImage` | Base Docker image | `node:20-slim`, `node:20-alpine` |
| `port` | Dev server port | `3000`, `4321`, `5173` |
| `hasNativeModules` | Uses native modules? | `true`, `false` |
| `devCommand` | Command to start dev server | `npm run dev -- --host 0.0.0.0` |

---

## Step 3: Generate Docker Files

Based on your configuration, create these files:

### If `hasNativeModules: true` (Recommended Default)

**Dockerfile:**
```dockerfile
FROM node:20-slim

WORKDIR /app

# Install build tools for native modules (Debian/glibc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    make \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy package files for layer caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build if needed
RUN npm run build --if-present

# Default command
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

### If `hasNativeModules: false` (Smaller Image)

**Dockerfile:**
```dockerfile
FROM node:20-alpine

WORKDIR /app

# Alpine uses apk, not apt-get
RUN apk add --no-cache python3 make g++ git

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build --if-present

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

### docker-compose.yml (Both)

```yaml
services:
  dev:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ${COMPOSE_PROJECT_NAME:-my-project}-dev-1
    ports:
      - "${DEV_PORT:-3000}:3000"
    volumes:
      - .:/app
      - node_modules:/app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev -- --host 0.0.0.0
    profiles:
      - dev

volumes:
  node_modules:
```

---

## Step 4: Start Container

```bash
# Navigate to project root
cd /path/to/project

# Start the development container
docker compose --profile dev up -d

# Verify it's running
docker ps --filter "name=my-project"

# Install dependencies (first time)
docker exec my-project-dev-1 npm install
```

---

## Step 5: Verify Setup

Run this checklist:

```bash
# 1. Container running?
docker ps | grep <container-name>

# 2. Can execute commands?
docker exec my-project-dev-1 node --version

# 3. Dependencies installed?
docker exec my-project-dev-1 npm list --depth=0

# 4. Dev server accessible?
curl -s http://localhost:3000 > /dev/null && echo "OK" || echo "Not responding"
```

---

## Native Module Troubleshooting

### Error: `ERR_DLOPEN_FAILED`

**Symptom:**
```
Error: Error loading shared library ld-linux-aarch64.so.1: No such file or directory
```

**Cause:** Using Alpine image with modules that require glibc.

**Fix:**
1. Update Dockerfile to use `node:20-slim`
2. Change `apk` commands to `apt-get`
3. Rebuild container:

```bash
docker compose --profile dev down
docker volume rm <project>_node_modules
docker compose --profile dev build --no-cache
docker compose --profile dev up -d
docker exec <container> npm install
```

### Error: `Module not found` after switching images

**Fix:** Rebuild native modules inside container:

```bash
docker exec <container> npm rebuild
```

### Decision Tree: Alpine vs Slim

```
Does package.json contain native modules?
│
├─ YES → Use node:20-slim (glibc)
│        └─ Examples: sharp, bcrypt, sqlite3, onnxruntime
│
├─ UNSURE → Use node:20-slim (safe default)
│
└─ NO (pure JS only) → Use node:20-alpine (smaller)
         └─ Examples: express, react, typescript, lodash
```

---

## Project Configuration Reference

### .claude/docker-config.json

```json
{
  "containerName": "my-project-dev-1",
  "baseImage": "node:20-slim",
  "port": 3000,
  "hasNativeModules": true,
  "devCommand": "npm run dev -- --host 0.0.0.0",
  "envFile": ".env",
  "additionalVolumes": [],
  "buildArgs": {}
}
```

### Environment Variables

Required env vars load from `.env` via docker-compose:

```yaml
env_file:
  - .env
```

For command-specific env vars:

```bash
docker exec -e MY_VAR=value <container-name> <command>
```
