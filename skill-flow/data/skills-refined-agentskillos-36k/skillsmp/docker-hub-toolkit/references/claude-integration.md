# Claude Code Integration for Docker Hub Workflows

## Terminal Commands

### Generate Optimized Dockerfile
```bash
claude "Generate an optimized multi-stage Dockerfile for my Python project with pip caching, non-root user, slim base image, and BuildKit support"
```

### Build and Push
```bash
claude "Build my Docker image, tag as myuser/app:v1.0, and push to Docker Hub"
```

### Debug Failed Builds
```bash
docker build . 2>&1 | claude -p "Analyze this Docker build error and fix it"
```

### Multi-Platform Setup
```bash
claude "Set up multi-platform Docker build for linux/amd64 and linux/arm64 and push to Docker Hub"
```

### Security Scanning
```bash
claude "Scan my Docker image for vulnerabilities and fix any HIGH/CRITICAL issues in the Dockerfile"
```

### Docker Compose
```bash
claude "Create a compose.yaml for local development with hot-reload and a production compose for deployment"
```

## Claude Code Hooks for Docker

### Pre-Build Validation Hook
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/validate-docker.sh"
          }
        ]
      }
    ]
  }
}
```

### Post-Build Verification Hook
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/verify-image.sh"
          }
        ]
      }
    ]
  }
}
```

## CLAUDE.md Docker Standards

Add to project's `CLAUDE.md` for consistent Docker work:

```markdown
## Docker Standards
- Always use multi-stage builds (base → builder → production)
- Use python:3.12-slim as base image
- Pin base image versions with SHA digests for production
- Run as non-root user (appuser)
- Use BuildKit cache mounts for pip installs
- Tag images with: semantic version + git SHA
- Include .dockerignore excluding: .git, __pycache__, .venv, .env, node_modules
- Set PYTHONDONTWRITEBYTECODE=1 and PYTHONUNBUFFERED=1
- Expose only necessary ports
- Use COPY --from for multi-stage artifact transfer
```

## Claude Capabilities Matrix

| Task | Claude Command | Automation Level |
|------|---------------|-----------------|
| Dockerfile creation | Terminal prompt | Full generation |
| Build optimization | PR review / terminal | Analysis + fix |
| CI/CD pipeline | Terminal prompt | Full generation |
| Security scan | Terminal prompt | Scan + remediate |
| Debug failures | Pipe errors | Root cause + fix |
| Multi-platform | Terminal prompt | Full setup |
| .dockerignore | Terminal prompt | Full generation |
| Docker Compose | Terminal prompt | Full generation |
| Image tagging | Terminal prompt | Strategy + execution |
| Hub push | Terminal prompt | Auth + push |

## Best Practices for Claude Docker Workflows

1. **Always read existing Dockerfile first** before generating changes
2. **Use --mount=type=cache** for all package manager installs
3. **Separate dependency install from code copy** for layer caching
4. **Test builds locally** before pushing to Docker Hub
5. **Use GitHub Actions cache** (`type=gha`) for CI builds
6. **Tag with git SHA** for traceability
7. **Run as non-root** in production stage
8. **Scan before push** for security compliance
