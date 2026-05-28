# Docker Hub Deployment Troubleshooting

## Build Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `failed to solve: failed to compute cache key` | File in COPY doesn't exist | Check file paths, update `.dockerignore` |
| `--mount=type=cache requires BuildKit` | Legacy builder used | Set `DOCKER_BUILDKIT=1` or use `docker buildx build` |
| `pip install failed` | Network/package issues | Add `--mount=type=cache`, check package names |
| `COPY failed: file not found` | Wrong context or `.dockerignore` | Verify build context, check `.dockerignore` |
| `permission denied` | File permissions in container | Use `chmod` in RUN or fix source permissions |

## Push Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `denied: requested access to the resource is denied` | Not logged in or wrong namespace | `docker login`, verify image name matches username |
| `unauthorized: authentication required` | Token expired or invalid | Regenerate access token on Docker Hub |
| `name invalid` | Bad image name format | Use `username/repo:tag` format |
| `repository does not exist` | Repo not created | Create repo on Docker Hub first or push will auto-create |
| `toomanyrequests` | Rate limit exceeded | Wait or upgrade Docker Hub plan |

## Image Size Issues

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Image > 500MB | Using full python image | Switch to `python:3.12-slim` |
| Image > 200MB | Build tools in final stage | Use multi-stage, copy only runtime deps |
| Large layers | apt cache not cleaned | Add `&& rm -rf /var/lib/apt/lists/*` |
| Unexpected files | No .dockerignore | Create `.dockerignore` with exclusions |

## CI/CD Issues

| Issue | Fix |
|-------|-----|
| GitHub Actions can't push | Check `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets |
| Cache not working | Verify `cache-from: type=gha` and `cache-to: type=gha,mode=max` |
| Multi-platform fails | Add `docker/setup-qemu-action@v3` step |
| Tags not generated | Check `docker/metadata-action@v5` configuration |
| Build takes too long | Enable BuildKit caching, order layers by change frequency |

## Security Issues

| Issue | Fix |
|-------|-----|
| Running as root | Add `RUN adduser` + `USER appuser` |
| Secrets in layers | Use build secrets: `--mount=type=secret` |
| Vulnerable base image | Pin to patched version, use Docker Scout |
| Open ports | Only `EXPOSE` required ports |
| .env in image | Add `.env` to `.dockerignore` |

## Debug Commands

```bash
# Inspect image layers
docker history myuser/app:latest

# Check image size
docker images myuser/app

# Run interactive shell in container
docker run -it --rm myuser/app:latest /bin/sh

# View build cache
docker buildx du

# Prune build cache
docker buildx prune

# Check Docker Hub image
docker manifest inspect myuser/app:latest

# Scan for vulnerabilities
docker scout cves myuser/app:latest
```

## Performance Diagnosis

```bash
# Measure build time
time docker build -t app:test .

# Compare image sizes
docker images --format "{{.Repository}}:{{.Tag}} {{.Size}}" | grep app

# Check layer count
docker inspect myuser/app:latest | jq '.[0].RootFS.Layers | length'

# Identify large layers
docker history --no-trunc myuser/app:latest
```
