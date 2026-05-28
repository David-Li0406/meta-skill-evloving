# Docker Hub Deployment Guide

## Authentication

```bash
# Login to Docker Hub
docker login -u USERNAME

# Login with access token (recommended for CI)
echo $DOCKERHUB_TOKEN | docker login -u USERNAME --password-stdin
```

## Image Naming Convention

Format: `[registry/]namespace/repository[:tag]`

| Component | Example | Notes |
|-----------|---------|-------|
| Registry | `docker.io` | Default, can omit |
| Namespace | `myuser` | Docker Hub username or org |
| Repository | `task-mgmt-api` | Project name |
| Tag | `v1.0.0`, `latest` | Version identifier |

### Tagging Strategy

```bash
# Semantic versioning
docker tag app:latest myuser/app:1.0.0
docker tag app:latest myuser/app:1.0
docker tag app:latest myuser/app:1
docker tag app:latest myuser/app:latest

# Git SHA tagging
docker tag app:latest myuser/app:$(git rev-parse --short HEAD)

# Combined (recommended)
docker tag app:latest myuser/app:1.0.0-$(git rev-parse --short HEAD)
```

## Push to Docker Hub

```bash
# Single tag
docker push myuser/app:v1.0.0

# All tags for a repository
docker push myuser/app --all-tags
```

## Multi-Platform Push

```bash
# Setup buildx
docker buildx create --name multiarch --use
docker buildx inspect --bootstrap

# Build and push multi-platform
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myuser/app:v1.0.0 \
  --push .
```

## Docker Hub Repository Settings

| Setting | Recommendation |
|---------|---------------|
| Visibility | Private for proprietary, Public for open source |
| Description | Clear project description with usage instructions |
| Categories | Add relevant categories for discoverability |
| Collaborators | Limit write access, use teams for orgs |

## Security Best Practices

1. **Use access tokens** instead of passwords
2. **Scan images** with Docker Scout before pushing
3. **Pin base images** with SHA256 digests
4. **Never include secrets** in image layers
5. **Use `.dockerignore`** to exclude `.env`, credentials
6. **Enable content trust**: `export DOCKER_CONTENT_TRUST=1`

## Image Size Optimization

| Action | Typical Savings |
|--------|----------------|
| `python:slim` vs `python` | ~850MB |
| Multi-stage build | ~500MB |
| `.dockerignore` | ~100MB+ |
| Remove apt cache | ~50MB |
| `--no-install-recommends` | ~100MB |

## Automated Builds Checklist

- [ ] Docker Hub account created
- [ ] Access token generated (Account Settings → Security)
- [ ] Repository created on Docker Hub
- [ ] Local image builds successfully
- [ ] Image tagged with proper naming convention
- [ ] Image pushed and verified on Docker Hub
- [ ] README/description updated on Docker Hub
