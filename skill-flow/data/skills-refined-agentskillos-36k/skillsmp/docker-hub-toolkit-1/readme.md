![Banner](./header.jpg)

# Docker Hub Toolkit Skill

A production-grade Claude Code skill that automates end-to-end Docker Hub deployment for Python projects with optimized multi-stage builds, CI/CD pipelines, and security best practices.

---

## Features

### Multi-Stage Dockerfile Generation
- Generates optimized 4-stage Dockerfiles: `base` → `builder` → `dev` → `production`
- Uses `python:3.12-slim` for minimal image size (~150MB vs ~1GB)
- Implements BuildKit cache mounts (`--mount=type=cache`) for fast rebuilds
- Bind mounts for dependency files to avoid COPY layer invalidation
- Sets `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1` automatically

### Docker Hub Push Automation
- Authenticates and pushes images with proper tagging
- Supports semantic versioning + git SHA combined tags
- Handles both single-platform and multi-platform (amd64/arm64) builds
- Automates buildx setup with QEMU for cross-platform support

### CI/CD Pipeline (GitHub Actions)
- Complete workflow template with Docker login, buildx, metadata extraction, and push
- GitHub Actions cache (`type=gha`) for fast CI builds
- Conditional push (build-only on PRs, push on main/tags)
- Docker Scout vulnerability scanning integrated
- Claude Code Action (`@claude` in PRs) for automated Dockerfile review

### Security Best Practices
- Non-root user in production containers
- No secrets or credentials in image layers
- Docker Scout scanning for HIGH/CRITICAL vulnerabilities
- Content trust support (`DOCKER_CONTENT_TRUST=1`)
- Comprehensive `.dockerignore` excluding sensitive files

### Validation & Quality Gates
- 10-point Dockerfile validation script checking:
  - Multi-stage build usage
  - Slim/Alpine base images
  - Non-root user configuration
  - Python environment variables
  - BuildKit cache mounts
  - Layer ordering optimization
  - `.dockerignore` completeness
  - Secret detection
  - Port exposure
  - Health check configuration

### Claude Code Integration
- Terminal commands for all Docker operations
- Pre-build validation hooks
- Post-build verification hooks
- CLAUDE.md standards template for team consistency
- Error piping for automated build failure debugging

---

## Skill Structure

```
.claude/skills/docker-hub-toolkit/
├── SKILL.md                              # Main skill definition (177 lines)
├── documentation/
│   ├── docker_hub_stages.md              # Multi-stage build stages reference
│   └── docker_hub_python_project_partner.md  # Claude capabilities reference
├── references/
│   ├── multi-stage-builds.md             # Stage architecture & anti-patterns
│   ├── docker-hub-deployment.md          # Push workflow & tagging strategy
│   ├── ci-cd-github-actions.md           # GitHub Actions pipeline templates
│   ├── claude-integration.md             # Claude commands, hooks, CLAUDE.md
│   └── troubleshooting.md               # Error diagnosis & resolution
├── scripts/
│   ├── build-and-push.sh                 # Build, tag, and push automation
│   ├── validate-dockerfile.sh            # 10-point Dockerfile linter
│   └── setup-multiplatform.sh            # Buildx + QEMU configuration
└── assets/templates/
    ├── Dockerfile.python                 # Multi-stage Dockerfile template
    ├── dockerignore.template             # Comprehensive .dockerignore
    ├── github-actions-docker.yml         # CI/CD workflow template
    └── docker-compose.yml                # Dev/prod compose template
```

---

## Prerequisites

- Docker Engine 20.10+ (BuildKit support)
- Docker CLI with buildx plugin
- Docker Hub account with access token
- Git (for SHA-based tagging)
- Python 3.10+ (for the project being containerized)

---

## Usage Instructions

### Step 1: Trigger the Skill

The skill activates automatically when you ask Claude Code to:
- Containerize a Python app
- Build or push Docker images
- Set up CI/CD for Docker
- Optimize a Dockerfile
- Debug Docker build failures
- Deploy Python projects as containers

### Step 2: Provide Required Information

Claude will ask for:

| Question | Example Answer |
|----------|---------------|
| Docker Hub username | `myuser` |
| Python framework | `FastAPI` |
| Entry point command | `uvicorn app.main:app --host 0.0.0.0 --port 8000` |
| Deployment method | `GitHub Actions CI/CD` |

### Step 3: Skill Execution

The skill follows this pipeline:

```
Generate Dockerfile → Create .dockerignore → Build Image → Tag → Security Scan → Push → CI/CD Setup
```

### Step 4: Verify Output

Use the output checklist to confirm:
- Multi-stage Dockerfile with all 4 stages
- `.dockerignore` with proper exclusions
- BuildKit cache mounts in place
- Non-root user configured
- Image tagged and pushed to Docker Hub
- CI/CD pipeline configured (if requested)

---

## Scripts Usage

### Build and Push

```bash
# Basic usage
bash .claude/skills/docker-hub-toolkit/scripts/build-and-push.sh USERNAME APP_NAME VERSION

# Example
bash .claude/skills/docker-hub-toolkit/scripts/build-and-push.sh myuser task-mgmt-api 1.0.0

# Multi-platform
bash .claude/skills/docker-hub-toolkit/scripts/build-and-push.sh myuser task-mgmt-api 1.0.0 linux/amd64,linux/arm64
```

### Validate Dockerfile

```bash
# Default (./Dockerfile)
bash .claude/skills/docker-hub-toolkit/scripts/validate-dockerfile.sh

# Custom path
bash .claude/skills/docker-hub-toolkit/scripts/validate-dockerfile.sh path/to/Dockerfile
```

### Setup Multi-Platform

```bash
bash .claude/skills/docker-hub-toolkit/scripts/setup-multiplatform.sh
```

---

## Template Placeholders

When using asset templates, replace these placeholders:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{PYTHON_VERSION}}` | Python version | `3.12` |
| `{{DEPS_FILE}}` | Dependencies file | `requirements.txt` |
| `{{PORT}}` | Application port | `8000` |
| `{{CMD}}` | Startup command | `"uvicorn", "app.main:app", "--host", "0.0.0.0"` |
| `{{APP_NAME}}` | Application name | `task-mgmt-api` |
| `{{USERNAME}}` | Docker Hub username | `myuser` |
| `{{VERSION}}` | Image version tag | `1.0.0` |
| `{{TARGET_STAGE}}` | Docker build target | `production` |
| `{{HOST_PORT}}` | Host port mapping | `8000` |
| `{{CONTAINER_PORT}}` | Container port | `8000` |

---

## Sample Prompts

### Prompt 1: Full Docker Hub Deployment

```
Using docker-hub-toolkit skill, containerize my Python FastAPI project and deploy it
to Docker Hub. My Docker Hub username is "alidev", the app name is "task-mgmt-api",
and the entry point is "uvicorn app.main:app --host 0.0.0.0 --port 8000".
I want a multi-stage Dockerfile with BuildKit caching, a .dockerignore file,
and a GitHub Actions CI/CD pipeline that builds and pushes on every merge to main.
Tag the image as v1.0.0.
```

**What this produces:**
- Optimized 4-stage Dockerfile
- `.dockerignore` with Python-specific exclusions
- `.github/workflows/docker-hub.yml` with buildx, caching, and Docker Scout
- Image built and pushed as `alidev/task-mgmt-api:1.0.0`

---

### Prompt 2: Validate and Optimize Existing Dockerfile

```
Using docker-hub-toolkit skill, validate my existing Dockerfile for best practices
and optimize it for performance. Check for multi-stage build usage, slim base images,
non-root user, BuildKit cache mounts, and layer ordering. Then set up multi-platform
builds for linux/amd64 and linux/arm64, and push the optimized image to Docker Hub
under "alidev/task-mgmt-api:2.0.0".
```

**What this produces:**
- Validation report from `validate-dockerfile.sh` (10-point check)
- Optimized Dockerfile with fixes for any issues found
- Multi-platform buildx configuration via `setup-multiplatform.sh`
- Image built for amd64 + arm64 and pushed to Docker Hub

---

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| `--mount=type=cache requires BuildKit` | Set `DOCKER_BUILDKIT=1` or use `docker buildx build` |
| `denied: requested access` on push | Run `docker login` with access token |
| Image > 500MB | Switch to `python:3.12-slim`, verify multi-stage COPY |
| GitHub Actions can't push | Check `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets |
| Multi-platform build fails | Run `setup-multiplatform.sh` to configure QEMU + buildx |

See `references/troubleshooting.md` for comprehensive error resolution.

---

## Related Documentation

- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker Python Containerization](https://docs.docker.com/guides/python/containerize/)
- [Docker Build Cache](https://docs.docker.com/build/cache/)
- [Dockerfile Best Practices](https://docs.docker.com/build/building/best-practices/)
- [Docker GitHub Actions](https://docs.docker.com/ci-cd/github-actions/)
- [Claude Code Overview](https://code.claude.com/docs/en/overview)
- [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)
