# Docker Layer Optimization Best Practices

Comprehensive guide for optimizing Docker image layers to minimize image size and maximize build cache efficiency.

## Why Layer Optimization Matters

- **Faster builds**: Reuse cached layers when dependencies haven't changed
- **Smaller images**: Reduce disk space usage (critical on 193 GB VPS with 30+ containers)
- **Faster deployments**: Smaller images = faster `docker pull` and container startup
- **Better security**: Fewer layers = smaller attack surface

## Core Principles

### 1. Leverage Build Cache

Docker builds layers sequentially. If a layer changes, all subsequent layers are rebuilt.

**Order layers from least to most frequently changed:**

```dockerfile
# ❌ BAD: Dependencies reinstalled every code change
FROM python:3.11-slim
WORKDIR /app
COPY . .                           # ← Changes frequently
RUN pip install -r requirements.txt  # ← Reinstalled every time!
CMD ["python", "app.py"]

# ✅ GOOD: Dependencies cached unless requirements.txt changes
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .            # ← Only changes when deps change
RUN pip install -r requirements.txt  # ← Cached most of the time
COPY . .                           # ← Code changes don't affect deps layer
CMD ["python", "app.py"]
```

**Layer ordering priority:**
1. Base image
2. System packages (`apt-get install`)
3. Dependency files (`requirements.txt`, `package.json`)
4. Install dependencies (`pip install`, `npm install`)
5. Application code (`COPY . .`)
6. Build/compile steps
7. Runtime configuration

### 2. Multi-Stage Builds

Separate build dependencies from runtime dependencies.

```dockerfile
# ❌ BAD: Build tools remain in final image (2.1 GB)
FROM python:3.11
WORKDIR /app
RUN apt-get update && apt-get install -y gcc build-essential
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]

# ✅ GOOD: Build tools discarded (665 MB)
FROM python:3.11 AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y gcc build-essential
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim AS runtime
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

**Benefits:**
- Builder stage: 2.1 GB (never deployed)
- Runtime stage: 665 MB (deployed)
- **Savings**: 1.4 GB per container (68% reduction)

### 3. Combine RUN Commands

Each `RUN` command creates a new layer. Combine related commands to reduce layer count.

```dockerfile
# ❌ BAD: 3 layers, larger total size
RUN apt-get update
RUN apt-get install -y curl wget
RUN rm -rf /var/lib/apt/lists/*

# ✅ GOOD: 1 layer, smaller size
RUN apt-get update && \
    apt-get install -y curl wget && \
    rm -rf /var/lib/apt/lists/*
```

**Why it matters:**
- Layer 1: `apt-get update` adds 50 MB
- Layer 2: `apt-get install` adds 100 MB
- Layer 3: `rm -rf` adds 0 bytes BUT previous layers still exist
- **Total**: 150 MB

Combined:
- Layer 1: Update, install, cleanup in one command
- **Total**: 100 MB (cleanup removes temp files in same layer)
- **Savings**: 50 MB

### 4. Use .dockerignore

Prevent unnecessary files from being copied into the image.

```bash
# .dockerignore
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.git/
.gitignore
.env
.vscode/
node_modules/
dist/
build/
*.log
README.md
docs/
tests/
```

**Benefits:**
- Faster `COPY . .` operations
- Smaller context sent to Docker daemon
- Prevents secrets from accidentally being copied

### 5. Install Only Production Dependencies

Separate dev and production dependencies.

**Python:**
```dockerfile
# ❌ BAD: Installs dev dependencies
RUN pip install -r requirements.txt

# ✅ GOOD: Production only
RUN pip install --no-cache-dir -r requirements.txt
# Or use poetry:
RUN poetry install --only main --no-dev
```

**Node.js:**
```dockerfile
# ❌ BAD: Installs devDependencies
RUN npm install

# ✅ GOOD: Production only
RUN npm ci --only=production
```

**Benefits:**
- Smaller image size (testing libs removed)
- Faster install time
- Reduced security vulnerabilities

### 6. Use Specific Base Image Tags

```dockerfile
# ❌ BAD: Unpredictable, breaks builds
FROM python:3

# ⚠️ BETTER: More specific but still risky
FROM python:3.11

# ✅ GOOD: Pinned version
FROM python:3.11.6-slim

# 🏆 BEST: Digest pinning (immutable)
FROM python:3.11.6-slim@sha256:abc123...
```

**Benefits:**
- Reproducible builds
- Prevents breaking changes
- Security audit trail

### 7. Minimize Layer Size with --no-cache Flags

```dockerfile
# Python: Remove pip cache
RUN pip install --no-cache-dir -r requirements.txt

# Node.js: Remove npm cache
RUN npm ci --only=production && npm cache clean --force

# APT: Remove package cache
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*
```

### 8. Order COPY Commands Strategically

Copy files that change least frequently first.

```dockerfile
# ❌ BAD: One big copy
COPY . .

# ✅ GOOD: Separate dependency files from code
COPY requirements.txt pyproject.toml ./
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY config/ ./config/
```

**Cache efficiency:**
- Change code → Only re-copy code, deps cached ✅
- Change deps → Reinstall deps + re-copy code ❌ (necessary)

## Real-World Examples

### Example 1: FastAPI Application

**Before (1.2 GB):**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

**After (333 MB) - 72% reduction:**
```dockerfile
# Build stage
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim AS runtime
WORKDIR /app

# Copy deps from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code (last to maximize cache)
COPY main.py .
COPY app/ ./app/

# Security: non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Key optimizations:**
1. Multi-stage build (builder + runtime)
2. `-slim` base image (reduces base from 1 GB to 150 MB)
3. `--no-cache-dir` flag
4. Dependencies copied before code
5. Non-root user for security

### Example 2: Streamlit Dashboard

**Before (2.8 GB):**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install streamlit pandas plotly
CMD ["streamlit", "run", "app.py"]
```

**After (778 MB) - 72% reduction:**
```dockerfile
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS runtime
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy only necessary files (not __pycache__, tests, etc.)
COPY app.py .
COPY data/ ./data/
COPY .streamlit/ ./.streamlit/

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Example 3: Next.js Application

**Before (1.8 GB):**
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
CMD ["npm", "start"]
```

**After (425 MB) - 76% reduction:**
```dockerfile
# Dependencies stage
FROM node:18-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Builder stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM node:18-alpine AS runtime
WORKDIR /app

ENV NODE_ENV=production

# Copy production dependencies
COPY --from=deps /app/node_modules ./node_modules
# Copy built application
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json

RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 && \
    chown -R nextjs:nodejs /app
USER nextjs

EXPOSE 3000

CMD ["npm", "start"]
```

**Key optimizations:**
1. Three-stage build (deps, builder, runtime)
2. `-alpine` base image (75% smaller than standard)
3. `npm ci --only=production` for runtime deps
4. Separate dependency installation from build
5. Only copy necessary artifacts to runtime

## Checklist for Optimal Layers

Before deploying:

- [ ] Multi-stage build implemented (builder + runtime)
- [ ] Base image uses `-slim` or `-alpine` variant
- [ ] `.dockerignore` file created (excludes tests, docs, .git)
- [ ] Dependencies installed before copying code
- [ ] `--no-cache-dir` flags used for package managers
- [ ] System packages cleaned up in same RUN command
- [ ] Only production dependencies installed in runtime stage
- [ ] Non-root user created for security
- [ ] Health check added (for services with HTTP endpoints)
- [ ] Related RUN commands combined with `&&`
- [ ] Image tagged with version/commit hash

## Impact on srv759970

**Before optimization (15 services):**
- Average image size: 1.8 GB
- Total disk usage: 27 GB
- Build time: 5-10 minutes per service

**After optimization (15 services):**
- Average image size: 650 MB
- Total disk usage: 9.75 GB
- Build time: 3-7 minutes per service

**Savings:**
- **17.25 GB freed** (64% reduction)
- **30-40% faster builds** (better cache utilization)
- **More secure** (non-root users, minimal attack surface)

## When NOT to Optimize

**Machine Learning Models** (WhisperX, Paperflow):
- Model files are 5-10 GB
- Optimization saves only 200-500 MB (5-10%)
- Complexity not worth marginal gains
- Focus on optimizing inference code, not models

**Trade-offs:**
- More complex Dockerfiles (harder to maintain)
- Slightly longer initial build (no cache)
- May need expertise to debug build issues

**Rule of thumb:**
- Service < 1 GB: Optimize if frequently rebuilt
- Service 1-3 GB: Strongly recommended
- Service > 5 GB (ML models): Only optimize non-model layers
