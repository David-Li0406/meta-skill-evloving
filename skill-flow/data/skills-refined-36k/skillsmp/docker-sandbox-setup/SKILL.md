---
name: Docker Sandbox Setup
description: This skill should be used when creating Docker containers for Claude Code sandboxing, configuring isolated development environments, setting up Docker volumes and persistence, configuring port forwarding for sandboxed applications, or troubleshooting Docker container issues in sandbox contexts. Provides Docker configuration knowledge specifically for running Claude Code in contained environments.
version: 0.1.0
---

# Docker Sandbox Setup

Configure Docker containers to run Claude Code in isolated, safe environments that prevent AI agents from modifying the host system.

## Purpose

This skill provides Docker configuration knowledge specifically for creating sandboxed development environments. Focus on the minimum Docker setup needed for Claude Code isolation while maintaining full development capabilities, not general Docker expertise.

## Core Concepts

### Isolation Strategy

Sandboxes use Docker to create complete isolation between Claude Code and the host system:

- **Container boundary**: All Claude Code operations occur within the container
- **Volume mounts**: Workspace shared between host and container for file access
- **Network isolation**: Port forwarding for web development, no direct host network access
- **Persistent caches**: Package managers and build caches preserved across restarts

### Base Image Selection

**Default recommendation**: Ubuntu 24.04 LTS

```dockerfile
FROM ubuntu:24.04
```

**Why Ubuntu 24.04:**
- Stable LTS release with long support window
- Widely used, extensive package availability
- Good balance of stability and modern tooling

**Alternative images:**
- `debian:bookworm` - Minimal, smaller image size
- `ubuntu:25.04` - Latest features, shorter support

### Custom Base Images

For faster sandbox creation with common tools pre-installed, build a custom base image:

**When to use custom base images:**
- Creating multiple sandboxes with similar tooling
- Want faster sandbox initialization
- Standard tool set across all projects

**How to create:**

```dockerfile
# my-sandbox-base.dockerfile
FROM ubuntu:24.04

# Install common tools
RUN apt-get update && apt-get install -y \
    curl wget git build-essential \
    ripgrep fd-find jq python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Node.js via nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
```

Build and tag:
```bash
docker build -f my-sandbox-base.dockerfile -t my-sandbox-base:latest .
```

Use in Sandbox.toml:
```toml
[sandbox]
base_image = "my-sandbox-base:latest"
```

## Container Configuration

### Volume Mounts

Mount the workspace and persistence directories:

```bash
docker run \
  -v $(pwd)/workspace:/workspace \
  -v $(pwd)/.docker-cache/cargo:/root/.cargo \
  -v $(pwd)/.docker-cache/npm:/root/.npm \
  -v $(pwd)/.docker-cache/pip:/root/.cache/pip \
  -v $(pwd)/.docker-cache/claude:/root/.claude \
  sandbox-container
```

**Critical mounts:**
- `/workspace` - Project source code (editable from host)
- `/root/.cargo` - Rust package cache
- `/root/.npm` - Node.js package cache
- `/root/.cache/pip` - Python package cache
- `/root/.claude` - Claude Code config and cache

**Benefits:**
- Source code editable from host
- Packages persist across container restarts
- Claude Code authentication persists
- Fast container rebuilds

### Port Forwarding

Forward ports for web development:

```bash
docker run -p 3000-3999:3000-3999 sandbox-container
```

**Port range rationale:**
- Common dev server ports (3000, 3001, etc.)
- Supports multiple services in monorepos
- Wide enough for flexibility, narrow enough for security

**Custom ports:**
Detect from package.json scripts or user specification:

```bash
# Specific ports only
docker run -p 3000:3000 -p 8080:8080 sandbox-container
```

### Environment Variables

Pass through essential environment variables:

```bash
docker run \
  --env-file .env \
  -e GITHUB_TOKEN="${GITHUB_TOKEN}" \
  sandbox-container
```

**Always pass through:**
- `GITHUB_TOKEN` - For gh CLI operations
- Custom API keys as specified in `.env`

**Never pass through:**
- Sensitive host environment variables
- System paths or credentials

## Dockerfile Structure

### Basic Template

```dockerfile
FROM ubuntu:24.04

# Set non-interactive frontend for apt
ENV DEBIAN_FRONTEND=noninteractive

# Install base packages
RUN apt-get update && apt-get install -y \
    curl wget git build-essential \
    ca-certificates gnupg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Install languages (Rust, Python, Node.js)
# ... language-specific setup ...

# Install CLI tools
# ... tool installation ...

# Install Claude Code
RUN curl -fsSL https://claude.ai/install.sh | bash

# Configure shell
# ... shell setup ...

CMD ["/bin/bash"]
```

### Layer Optimization

Order Dockerfile commands by change frequency:

1. **Base packages** (rarely change)
2. **Language runtimes** (occasionally update)
3. **CLI tools** (occasionally update)
4. **Project dependencies** (change frequently)
5. **Source code** (changes constantly - use volume mount instead)

**Good ordering:**
```dockerfile
# Rarely changes - cached well
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y curl git

# Occasionally changes - medium cache hit rate
RUN install_rust_stable

# Frequently changes - volume mounted, not in image
# (Don't COPY source code into image)
```

**Why this matters:**
- Earlier layers cached longer
- Changes to later layers don't invalidate earlier cache
- Faster rebuilds during development

### Multi-Stage Considerations

Multi-stage builds are typically NOT needed for sandbox containers because:

- Containers are development environments, not production images
- Need full tooling available for development
- Size optimization less critical than functionality

**Skip multi-stage builds** for sandboxes.

## Container Lifecycle

### Starting a Sandbox

```bash
#!/bin/bash
# up.sh

docker build -t sandbox-${PROJECT_NAME} .
docker run -d \
  --name sandbox-${PROJECT_NAME} \
  -v $(pwd)/workspace:/workspace \
  -v $(pwd)/.docker-cache/cargo:/root/.cargo \
  -v $(pwd)/.docker-cache/npm:/root/.npm \
  -v $(pwd)/.docker-cache/pip:/root/.cache/pip \
  -v $(pwd)/.docker-cache/claude:/root/.claude \
  -p 3000-3999:3000-3999 \
  --env-file .env \
  sandbox-${PROJECT_NAME}

echo "Sandbox is starting..."
docker logs -f sandbox-${PROJECT_NAME}
```

### Interactive Shell

```bash
#!/bin/bash
# shell.sh

docker exec -it sandbox-${PROJECT_NAME} /bin/zsh
```

### Running Commands

```bash
#!/bin/bash
# run.sh

docker exec sandbox-${PROJECT_NAME} "$@"
```

### Stopping a Sandbox

```bash
#!/bin/bash
# stop.sh

docker stop sandbox-${PROJECT_NAME}
docker rm sandbox-${PROJECT_NAME}
```

## Common Patterns

### Detecting Container Environment

Add visual indicators that you're in a container:

```bash
# In .zshrc
if [ -f /.dockerenv ]; then
    export IN_CONTAINER=true
    # Starship will show container indicator
fi
```

Starship config recognizes this:
```toml
[container]
disabled = false
symbol = "🐳 "
style = "bold red"
```

### Preserving Build Context

Use `.dockerignore` to exclude unnecessary files:

```
# .dockerignore
.git
node_modules/
.docker-cache/
*.log
.env.local
```

**Benefits:**
- Faster builds (smaller context)
- Prevents accidentally copying sensitive files
- Reduces image size

### Health Checks

Add health checks for long-running services:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:3000/ || exit 1
```

**Use sparingly** - only for services that need it.

## Security Considerations

### File Permissions

Container runs as root by default. Files created in workspace will be root-owned.

**Solution 1: Match host UID/GID**
```dockerfile
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g ${GROUP_ID} developer && \
    useradd -u ${USER_ID} -g developer developer

USER developer
```

**Solution 2: Fix permissions on stop**
```bash
# In stop.sh
docker exec sandbox-${PROJECT_NAME} chown -R $(id -u):$(id -g) /workspace
docker stop sandbox-${PROJECT_NAME}
```

Choose Solution 2 for simplicity.

### Network Isolation

Containers are network-isolated by default. Only exposed ports are accessible.

**Don't expose:**
- Port 22 (SSH)
- Database ports unless required
- Internal service ports

### Secret Management

Never build secrets into the image:

```dockerfile
# ❌ BAD
RUN git clone https://user:password@github.com/repo.git

# ✅ GOOD
RUN git clone https://github.com/repo.git
# (Requires GITHUB_TOKEN in environment)
```

Use `.env` files and `--env-file` flag instead.

## Additional Resources

### Reference Files

For detailed troubleshooting and optimization:
- **`references/troubleshooting.md`** - Common Docker issues and solutions
- **`references/optimization.md`** - Performance and DevX improvements

### Example Files

Complete working examples:
- **`examples/Dockerfile.template`** - Full Dockerfile template with all features
- **`examples/docker-compose.yml`** - Alternative using Docker Compose

## Integration with Other Skills

**With language-environment-config:**
- This skill handles Docker container setup
- language-environment-config handles language installation inside container
- Use both together when generating Dockerfiles

**With sandbox-config-management:**
- This skill implements what Sandbox.toml specifies
- Read base_image, ports, volumes from Sandbox.toml
- Generate Docker configuration matching the config file

## Quick Reference

**Default base image:** `ubuntu:24.04`

**Required volume mounts:**
- `/workspace` - Source code
- `/root/.cargo` - Rust cache
- `/root/.npm` - Node cache
- `/root/.cache/pip` - Python cache
- `/root/.claude` - Claude Code config

**Common port range:** `-p 3000-3999:3000-3999`

**Environment:** `--env-file .env` + `-e GITHUB_TOKEN`

**Order Dockerfile:** Base → Languages → Tools → Config

**Skip multi-stage builds** for dev containers
