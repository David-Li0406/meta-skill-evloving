# Docker Image Optimization Workflow

Step-by-step procedure for optimizing Docker images on Hostinger VPS.

## Step 1: Analysis

Check current image size and configuration:

```bash
# Verify current size
ssh automation@69.62.108.82 "docker images | grep [service-name]"

# Analyze existing Dockerfile
ssh automation@69.62.108.82 "cat /opt/[service-name]/Dockerfile"

# Check dependencies
ssh automation@69.62.108.82 "cat /opt/[service-name]/requirements.txt"  # Python
ssh automation@69.62.108.82 "cat /opt/[service-name]/package.json"      # Node.js
```

## Step 2: Preparation

Create optimized Dockerfile:

1. Backup original Dockerfile:
   ```bash
   ssh automation@69.62.108.82 "cd /opt/[service-name] && cp Dockerfile Dockerfile.old.bak"
   ```

2. Select appropriate template:
   - `python-fastapi.dockerfile` for FastAPI/Flask
   - `python-streamlit.dockerfile` for Streamlit
   - `nextjs.dockerfile` for Next.js

3. Adapt template:
   - Update ports
   - Modify CMD/ENTRYPOINT
   - Adjust healthcheck endpoint and timing
   - Customize user name if needed
   - Add service-specific runtime dependencies

4. Create `.dockerignore` using `../assets/dockerignore-standard`

## Step 3: Upload

Upload optimized Dockerfile to server (use heredoc to avoid permission issues):

```bash
ssh automation@69.62.108.82 "cat > /tmp/dockerfile-optimized.txt << 'EOF'
[paste Dockerfile content here]
EOF
sudo cp /tmp/dockerfile-optimized.txt /opt/[service-name]/Dockerfile"
```

Upload .dockerignore the same way:

```bash
ssh automation@69.62.108.82 "cat > /tmp/dockerignore.txt << 'EOF'
[paste .dockerignore content]
EOF
sudo cp /tmp/dockerignore.txt /opt/[service-name]/.dockerignore"
```

## Step 4: Build

Build without cache to ensure clean build:

```bash
ssh automation@69.62.108.82 "cd /opt/[service-name] && docker-compose build --no-cache"
```

Monitor build progress for large services.

## Step 5: Verify

Check new image size:

```bash
ssh automation@69.62.108.82 "docker images | grep [service-name]"
```

Calculate size reduction compared to original.

## Step 6: Deploy

Deploy with force-recreate:

```bash
ssh automation@69.62.108.82 "cd /opt/[service-name] && docker-compose down && docker-compose up -d --force-recreate"
```

Note: If network error occurs ("has active endpoints"), skip `down` and use only:
```bash
ssh automation@69.62.108.82 "cd /opt/[service-name] && docker-compose up -d --force-recreate"
```

## Step 7: Validation

Verify service is running:

```bash
ssh automation@69.62.108.82 "docker ps | grep [service-name]"
```

Check logs for errors:

```bash
ssh automation@69.62.108.82 "cd /opt/[service-name] && docker-compose logs --tail=50"
```

Test health check (if applicable):

```bash
ssh automation@69.62.108.82 "docker inspect --format='{{.State.Health.Status}}' [container-name]"
```

## Step 8: Cleanup

Remove dangling images:

```bash
ssh automation@69.62.108.82 "docker image prune -f"
```

This typically recovers 3-5 GB of space across all optimizations.

## Expected Results

- **Size reduction**: 20-50% for most Python/Node.js applications
- **Security**: +50 points (non-root user, minimal attack surface)
- **Build time**: Slightly longer but more reliable
- **Runtime performance**: Same or better (fewer dependencies)

## Rollback Procedure

If optimization causes issues:

1. Restore original Dockerfile:
   ```bash
   ssh automation@69.62.108.82 "cd /opt/[service-name] && cp Dockerfile.old.bak Dockerfile"
   ```

2. Rebuild and deploy:
   ```bash
   ssh automation@69.62.108.82 "cd /opt/[service-name] && docker-compose build --no-cache && docker-compose up -d --force-recreate"
   ```
