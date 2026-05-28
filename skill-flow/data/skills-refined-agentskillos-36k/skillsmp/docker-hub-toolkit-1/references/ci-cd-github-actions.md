# CI/CD with GitHub Actions for Docker Hub

## Complete Workflow Template

```yaml
name: Build and Push to Docker Hub
on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
  IMAGE_NAME: ${{ secrets.DOCKERHUB_USERNAME }}/app-name

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix=

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Required GitHub Secrets

| Secret | Value | Where to Get |
|--------|-------|--------------|
| `DOCKERHUB_USERNAME` | Docker Hub username | Docker Hub profile |
| `DOCKERHUB_TOKEN` | Access token | Docker Hub → Account Settings → Security |

## Key Actions Explained

### docker/login-action@v3
Authenticates with Docker Hub using secrets.

### docker/setup-buildx-action@v3
Enables BuildKit with advanced caching and multi-platform support.

### docker/metadata-action@v5
Auto-generates tags from git refs:
- Branch push → `main`
- Tag `v1.2.3` → `1.2.3`, `1.2`, `1`, `latest`
- PR → no push (build only)

### docker/build-push-action@v5
Builds and pushes with:
- `cache-from: type=gha` — Uses GitHub Actions cache
- `cache-to: type=gha,mode=max` — Caches all layers
- `platforms` — Multi-architecture support

## Claude Code GitHub Actions Integration

### Setup
```bash
# In Claude Code terminal
/install-github-app
```

### @claude in PRs
```
@claude review this Dockerfile for performance and security
@claude optimize Docker build layers for faster rebuilds
@claude add multi-platform build support
```

### Automated Review Workflow
```yaml
name: Claude Docker Review
on:
  pull_request:
    paths: ['Dockerfile', 'docker-compose*.yml', '.dockerignore']
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Review Docker files for: multi-stage optimization, security (non-root user, no secrets in layers), caching efficiency, and image size"
```

## Build Caching Strategies

| Strategy | Speed | Persistence | Best For |
|----------|-------|-------------|----------|
| `type=gha` | Fast | GitHub-managed | Most projects |
| `type=registry` | Medium | Docker Hub | Shared teams |
| `type=local` | Fastest | Runner-local | Self-hosted runners |

## Workflow Triggers

| Trigger | Use Case |
|---------|----------|
| `push: branches: [main]` | Deploy on merge |
| `push: tags: ['v*']` | Release versioned images |
| `pull_request` | Build-only validation |
| `schedule: cron: '0 2 * * 1'` | Weekly security rebuild |
| `workflow_dispatch` | Manual trigger |
