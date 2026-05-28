# Container Security Best Practices

## Runtime Image: Wolfi glibc-dynamic

### Why Wolfi?

Wolfi is a Linux distribution designed specifically for containers with security in mind:

- **Minimal attack surface**: Only includes necessary packages
- **No CVEs by design**: Built from scratch with modern, updated packages
- **glibc-dynamic**: Provides compatibility with most Python/Node.js applications
- **Non-root by default**: Uses UID 65532 (nonroot user)
- **Regular updates**: Actively maintained by Chainguard

### Image Selection

```dockerfile
# ARG for choosing runtime image tag
ARG RUNTIME_TAG=latest
FROM cgr.dev/chainguard/glibc-dynamic:${RUNTIME_TAG}
```

**Available tags:**
- `latest` - **Production** (no shell, minimal, most secure) ⭐ **Recommended for production**
- `latest-dev` - **Development/debugging** (includes shell, apk, busybox tools)

**When to use each:**

✅ **Use `latest` (default) for:**
- Production deployments
- CI/CD pipelines
- Maximum security (no shell = smaller attack surface)

✅ **Use `latest-dev` for:**
- Local debugging
- Troubleshooting container issues
- Need to exec into container for investigation

**Build-time selection:**
```bash
# Production build (no shell)
podman build -t myapp:prod .

# Debug build (with shell)
podman build --build-arg RUNTIME_TAG=latest-dev -t myapp:debug .
```

**Debugging with latest-dev:**
```bash
# Exec into container with shell
podman run -it myapp:debug sh

# Check files, environment, processes
ls -la /app
env
ps aux
```

### User Configuration

Wolfi images use UID 65532 by default (nonroot user):

```dockerfile
# No need to create user, already exists
USER 65532:65532

# When copying files from builder, use this UID
COPY --from=builder --chown=65532:65532 /app /app
```

### Init System (tini)

Wolfi images are minimal and don't include tini. Copy it from the builder stage:

```dockerfile
# In builder stage: install tini
RUN apt-get install -y tini

# In runtime stage: copy tini from builder
COPY --from=builder /usr/bin/tini-static /usr/bin/tini

# Use as entrypoint
ENTRYPOINT ["tini", "--"]
CMD ["your-app"]
```

**Why tini?**
- Handles zombie processes correctly
- Forwards signals properly (SIGTERM for graceful shutdown)
- Essential for production containers

## Builder Images

### Python Projects

Use official Python slim images for building:

```dockerfile
FROM docker.io/python:3-slim AS builder
```

Benefits:
- Official Python runtime with all necessary libraries
- Includes pip, setuptools by default
- Compatible with most Python packages
- Slim variant reduces build time and size

### Node.js/Bun Projects

Use official Node.js LTS slim images for building:

```dockerfile
FROM docker.io/node:lts-slim AS builder
```

Benefits:
- Official Node.js LTS with npm/corepack
- Compatible with Bun installation
- Includes build tools for native modules
- Slim variant balances size and compatibility

## Multi-stage Build Pattern

Always use multi-stage builds to minimize runtime image size:

```dockerfile
# Stage 1: Builder (larger, includes build tools)
FROM docker.io/python:3-slim AS builder
# Install dependencies, build application
...

# Stage 2: Runtime (minimal, Wolfi)
FROM cgr.dev/chainguard/glibc-dynamic:latest AS runtime
# Copy only runtime artifacts
COPY --from=builder --chown=65532:65532 /app /app
```

## Security Checklist

- [ ] Use minimal runtime images (Wolfi glibc-dynamic)
- [ ] Run as non-root user (UID 65532)
- [ ] Use multi-stage builds
- [ ] Pin base image versions in production
- [ ] Scan images for vulnerabilities
- [ ] Use BuildKit cache mounts for dependencies
- [ ] Remove build dependencies in runtime stage
- [ ] Set appropriate file permissions (chown)
