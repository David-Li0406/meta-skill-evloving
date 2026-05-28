# Debugging Container Images

## Production vs Debug Images

Wolfi provides two variants for debugging purposes:

### Production Image (Default)
```dockerfile
FROM cgr.dev/chainguard/glibc-dynamic:latest
```

**Characteristics:**
- ❌ No shell (sh, bash)
- ❌ No debugging tools
- ✅ Minimal attack surface
- ✅ Smallest image size
- ✅ Most secure

**Use for:** Production deployments

### Debug Image
```dockerfile
FROM cgr.dev/chainguard/glibc-dynamic:latest-dev
```

**Characteristics:**
- ✅ Includes shell (sh)
- ✅ Basic debugging tools
- ⚠️ Larger image size
- ⚠️ Should NOT be used in production

**Use for:** Development, troubleshooting, debugging

## Build-time Image Selection

Use ARG to switch between production and debug images:

```dockerfile
ARG RUNTIME_TAG=latest
FROM cgr.dev/chainguard/glibc-dynamic:${RUNTIME_TAG} AS runtime
```

### Build for Production
```bash
podman build -t myapp:latest .
# or explicitly
podman build --build-arg RUNTIME_TAG=latest -t myapp:prod .
```

### Build for Debugging
```bash
podman build --build-arg RUNTIME_TAG=latest-dev -t myapp:debug .
```

## Debugging Techniques

### 1. Shell Access (Debug Image Only)

```bash
# Run with shell override
podman run -it --rm myapp:debug sh

# Execute shell in running container
podman exec -it <container-id> sh
```

### 2. Check Application Logs

```bash
# View logs
podman logs <container-id>

# Follow logs
podman logs -f <container-id>

# Last 100 lines
podman logs --tail 100 <container-id>
```

### 3. Inspect Environment

```bash
# In debug image with shell
podman run -it --rm myapp:debug sh -c 'env | sort'

# Check file permissions
podman run -it --rm myapp:debug sh -c 'ls -la /app'

# Verify user
podman run -it --rm myapp:debug sh -c 'id'
```

### 4. Test Application Commands

```bash
# Override CMD to test commands
podman run -it --rm myapp:debug python -c "import sys; print(sys.version)"
podman run -it --rm myapp:debug bun --version
podman run -it --rm myapp:debug node --version
```

### 5. Network Debugging (Debug Image)

```bash
# Test connectivity (if tools available)
podman run -it --rm myapp:debug sh -c 'ping -c 3 example.com'

# Check DNS resolution
podman run -it --rm myapp:debug sh -c 'nslookup example.com'
```

## CI/CD Debugging Strategy

### GitHub Actions Workflow

Add a debug build job for troubleshooting:

```yaml
jobs:
  # Regular production build
  build-app:
    runs-on: ubuntu-24.04
    steps:
      - name: Build production image
        run: podman build -t "$IMAGE:$TAG" .

  # Debug build (on-demand)
  build-app-debug:
    if: github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-24.04
    steps:
      - name: Build debug image
        run: |
          podman build \
            --build-arg RUNTIME_TAG=latest-dev \
            -t "$IMAGE:$TAG-debug" .
```

Trigger debug build manually via GitHub UI when needed.

### Local vs CI Debugging

**Local Development:**
```bash
# Build with debug image
podman build --build-arg RUNTIME_TAG=latest-dev -t myapp:debug .

# Interactive debugging
podman run -it --rm myapp:debug sh

# Mount local code for live debugging
podman run -it --rm \
  -v ./src:/app/src:ro \
  myapp:debug sh
```

**CI Environment:**
```bash
# Use workflow_dispatch for on-demand debug builds
# Add manual steps to dump environment
- name: Debug environment
  if: failure()
  run: |
    podman run myapp:debug sh -c 'env | sort'
    podman run myapp:debug sh -c 'ls -laR /app'
```

## Common Debug Scenarios

### Application Won't Start

1. **Build debug image:**
   ```bash
   podman build --build-arg RUNTIME_TAG=latest-dev -t myapp:debug .
   ```

2. **Check file permissions:**
   ```bash
   podman run -it myapp:debug sh -c 'ls -la /app'
   ```

3. **Verify dependencies:**
   ```bash
   # Python
   podman run -it myapp:debug sh -c 'pip list'
   
   # Node.js
   podman run -it myapp:debug sh -c 'ls -la /app/node_modules'
   
   # Bun
   podman run -it myapp:debug sh -c 'bun pm ls'
   ```

4. **Test command manually:**
   ```bash
   podman run -it myapp:debug sh
   # Then run commands interactively
   ```

### Missing Dependencies

```bash
# Check what's in the image
podman run -it myapp:debug sh -c 'find /app -type f'

# Verify library paths
podman run -it myapp:debug sh -c 'ldd /usr/local/bin/python'
```

### Permission Issues

```bash
# Check user and group
podman run -it myapp:debug sh -c 'id'

# Verify ownership
podman run -it myapp:debug sh -c 'ls -la /app'

# Test write permissions
podman run -it myapp:debug sh -c 'touch /tmp/test && rm /tmp/test'
```

## Security Warning

⚠️ **NEVER use :latest-dev images in production!**

- Debug images include shell and tools
- Larger attack surface
- Not hardened for production
- Should only be used for development/debugging

Always use `:latest` (production) images for deployments.

## Alternative: Ephemeral Debug Container

If you need to debug a production image without shell, use an ephemeral debug container:

```bash
# Run debug sidecar with shared PID namespace
podman run -d --name app myapp:latest
podman run -it --rm \
  --pid=container:app \
  --network=container:app \
  busybox sh

# Now you can inspect the app's processes and network
```

This approach doesn't modify the production image but allows debugging.

## Debugging Checklist

When troubleshooting container issues:

- [ ] Build with `:latest-dev` tag
- [ ] Check application logs first
- [ ] Verify file permissions and ownership
- [ ] Test commands interactively in shell
- [ ] Check environment variables
- [ ] Verify dependencies are installed
- [ ] Test network connectivity
- [ ] Review user/group configuration
- [ ] Compare with working local setup
- [ ] Check resource limits (memory, CPU)

## Best Practices

1. **Use debug images locally only** - Never in production
2. **Build both variants** - Keep production and debug builds separate
3. **Document debugging steps** - Add troubleshooting guide to your README
4. **Clean up debug images** - Remove after debugging to save space
5. **Use workflow_dispatch** - Enable on-demand debug builds in CI
