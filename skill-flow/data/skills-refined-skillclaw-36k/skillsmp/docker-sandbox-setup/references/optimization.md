# Docker Sandbox Optimization

Performance and developer experience improvements for Docker-based Claude Code sandboxes.

## Build Performance

### Layer Caching Strategy

Optimize Dockerfile ordering to maximize cache hits:

**Principle:** Order by change frequency (least to most)

```dockerfile
# Tier 1: Rarely changes (months)
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# Tier 2: Occasionally changes (weeks)
RUN apt-get update && apt-get install -y \
    curl git build-essential

# Tier 3: Language versions (weeks/months)
RUN curl https://sh.rustup.rs | sh -s -- -y
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# Tier 4: CLI tools (weeks)
RUN cargo install ripgrep fd-find

# Tier 5: Project dependencies (days)
# Use volume mounts instead of COPY for source code

# Never include: Source code (changes constantly, use volume)
```

**Impact:**
- Cold build: 15-20 minutes
- Cached build: 30 seconds

### BuildKit Features

Enable modern Docker build features:

```bash
export DOCKER_BUILDKIT=1
docker build -t sandbox-project .
```

**Cache mounts** for package managers:

```dockerfile
# Rust builds with cache
RUN --mount=type=cache,target=/root/.cargo/registry \
    --mount=type=cache,target=/root/.cargo/git \
    cargo install cargo-dist cargo-deny

# Node builds with cache
RUN --mount=type=cache,target=/root/.npm \
    npm install -g pnpm typescript

# Python builds with cache
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install uv ruff
```

**Benefits:**
- Package downloads cached across builds
- Faster rebuilds when adding tools
- Reduced network usage

### Parallel Installation

Install independent tools in parallel:

```dockerfile
# Install Rust and Node.js simultaneously
RUN curl https://sh.rustup.rs | sh -s -- -y & \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash & \
    wait
```

**Caution:** Use only for truly independent installations. Increases complexity.

### Minimal Image Base

Start with minimal base for faster pulls:

```dockerfile
# Standard Ubuntu (500MB+)
FROM ubuntu:24.04

# Minimal Ubuntu (80MB)
FROM ubuntu:24.04-minimal

# Or Debian (smaller)
FROM debian:bookworm-slim
```

**Trade-off:** Smaller base = more packages to install manually. Recommend sticking with `ubuntu:24.04` for ease of use.

## Runtime Performance

### Volume Mount Options

Optimize volume mount performance, especially on macOS:

```bash
# Default (slow on macOS)
docker run -v $(pwd)/workspace:/workspace sandbox-project

# Delegated (faster on macOS)
docker run -v $(pwd)/workspace:/workspace:delegated sandbox-project

# Cached (even faster, use for read-mostly directories)
docker run -v $(pwd)/node_modules:/workspace/node_modules:cached sandbox-project
```

**Mount modes:**
- `delegated`: Container writes may not be immediately visible on host (faster)
- `cached`: Host writes may not be immediately visible in container (faster for read-heavy)
- Default: Fully synchronous (slower but most consistent)

**Recommendation:** Use `delegated` for workspace on macOS, default on Linux.

### Resource Allocation

Adjust Docker Desktop resources for optimal performance:

**Minimum:**
- CPUs: 2
- Memory: 2GB
- Swap: 1GB

**Recommended:**
- CPUs: 4-6
- Memory: 4-8GB
- Swap: 2GB

**High performance:**
- CPUs: 8+
- Memory: 8-16GB
- Swap: 4GB

**Setting:** Docker Desktop → Settings → Resources

**Impact on build times:**
- 2 CPUs: 15-20 min
- 4 CPUs: 8-10 min
- 8 CPUs: 5-6 min

### Language-Specific Optimizations

#### Rust

Cache cargo registry and git checkouts:

```bash
docker run \
  -v $(pwd)/.docker-cache/cargo/registry:/root/.cargo/registry \
  -v $(pwd)/.docker-cache/cargo/git:/root/.cargo/git \
  sandbox-project
```

Enable sparse registry protocol:

```dockerfile
RUN echo '[registries.crates-io]' > /root/.cargo/config.toml && \
    echo 'protocol = "sparse"' >> /root/.cargo/config.toml
```

**Impact:** 50% faster dependency fetching.

#### Node.js

Use pnpm for faster installs and disk efficiency:

```dockerfile
RUN npm install -g pnpm
```

In container:
```bash
pnpm install  # Instead of npm install
```

**Impact:**
- 2-3x faster than npm
- Saves disk space (hardlinks)

Cache node_modules:

```bash
docker run \
  -v $(pwd)/.docker-cache/pnpm:/root/.local/share/pnpm \
  sandbox-project
```

#### Python

Use `uv` for blazing fast installs:

```dockerfile
RUN pip install uv
```

In container:
```bash
uv pip install -r requirements.txt  # Instead of pip install
```

**Impact:** 10-100x faster than pip.

Cache pip packages:

```bash
docker run \
  -v $(pwd)/.docker-cache/pip:/root/.cache/pip \
  sandbox-project
```

## Developer Experience

### Shell Startup Time

Reduce shell startup time by deferring initializations:

**Problem:** oh-my-zsh + plugins can take 2-3 seconds to start

**Solution:** Lazy-load plugins

```bash
# .zshrc
# Instead of loading all plugins immediately
plugins=(git docker kubectl)  # Slow

# Lazy load when first used
autoload -Uz compinit
compinit -C  # Skip security check for speed
```

Or use faster alternatives:
```bash
# Zinit (faster plugin manager)
source ~/.zinit/bin/zinit.zsh

# Lazy load plugins
zinit wait lucid for \
    OMZP::git \
    OMZP::docker
```

**Impact:** 2-3s startup → 0.5s startup

### Starship Prompt

Configure starship for fast rendering:

```toml
# starship.toml

# Disable slow modules in containers
[gcloud]
disabled = true

[kubernetes]
disabled = true

# Fast modules only
[directory]
truncation_length = 3
fish_style_pwd_dir_length = 1

[git_branch]
format = "[$symbol$branch]($style) "

# Container indicator (always show)
[container]
disabled = false
symbol = "🐳 "
style = "bold red"
format = "[$symbol]($style)"
```

**Impact:** Prompt renders <50ms vs 200-500ms

### Pre-Built Base Images

Create reusable base images for faster sandbox creation:

```bash
# Build base image once
docker build -f base.dockerfile -t sandbox-base:1.0 .
docker push yourusername/sandbox-base:1.0

# Use in all sandboxes
FROM yourusername/sandbox-base:1.0
```

Include in base:
- Common CLI tools (ripgrep, fd, jq, etc.)
- Language runtimes (Rust, Python, Node.js)
- Shell configuration (oh-my-zsh, starship)
- Claude Code CLI

**Impact:**
- Sandbox creation: 15min → 2min
- Consistent tooling across projects

### Fast Feedback Loops

Optimize for quick iteration:

**1. Keep container running:**
```bash
# Don't rebuild for every change
# Instead, exec commands in running container
./sandbox/run.sh cargo test
./sandbox/run.sh npm run dev
```

**2. Use watch modes:**
```bash
# In container
cargo watch -x test
npm run dev  # With hot reload
```

**3. Avoid full rebuilds:**
```bash
# Only rebuild when Dockerfile changes
# Source code changes use volume mounts (instant)
```

## Disk Space Management

### Regular Cleanup

Prevent disk space issues:

```bash
# Clean up stopped containers and unused images
docker system prune -a

# Remove only stopped containers
docker container prune

# Remove dangling images
docker image prune
```

**Automate cleanup:**

```bash
# Cron job (weekly)
0 0 * * 0 docker system prune -af --volumes
```

### Monitor Disk Usage

```bash
# Check Docker disk usage
docker system df

# Detailed breakdown
docker system df -v

# Check specific image layers
docker history sandbox-project
```

### Exclude from Builds

Comprehensive `.dockerignore`:

```
# Version control
.git
.gitignore

# Dependencies (install in container)
node_modules/
target/
.venv/

# Build artifacts
dist/
build/
*.pyc
__pycache__/

# Docker cache
.docker-cache/

# IDE
.vscode/
.idea/
*.swp

# Logs
*.log
logs/

# OS files
.DS_Store
Thumbs.db

# Environment
.env.local
.env.*.local
```

## Network Performance

### DNS Caching

Configure DNS caching for faster resolution:

```json
// /etc/docker/daemon.json
{
  "dns": ["8.8.8.8", "1.1.1.1"],
  "dns-opts": ["ndots:0"],
  "dns-search": []
}
```

### Registry Mirrors

Use registry mirrors for faster image pulls:

```json
// /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://mirror.gcr.io"
  ]
}
```

## Advanced Optimizations

### Shared Memory

Increase shared memory for compilation-heavy workloads:

```bash
docker run --shm-size=2g sandbox-project
```

Useful for:
- Rust compilation
- Webpack builds
- Test suites with in-memory databases

### CPU Affinity

Pin container to specific CPUs (Linux only):

```bash
docker run --cpuset-cpus="0-3" sandbox-project
```

**Use case:** Dedicated build servers

### Tmpfs Mounts

Use tmpfs for temporary build artifacts:

```bash
docker run \
  --tmpfs /tmp:rw,size=1g,mode=1777 \
  sandbox-project
```

**Benefits:**
- Faster builds (RAM vs disk)
- Automatic cleanup

**Caution:** Loses data on container restart

## Benchmark Comparisons

### Build Times (Ubuntu 24.04 + Rust + Python + Node.js)

| Configuration | Cold Build | Warm Build |
|---------------|------------|------------|
| No optimization | 20min | 18min |
| Layer ordering | 20min | 2min |
| + BuildKit | 15min | 1min |
| + Cache mounts | 12min | 30sec |
| + Pre-built base | 5min | 30sec |

### Volume Mount Performance (10,000 files)

| Platform | Mode | Read | Write |
|----------|------|------|-------|
| Linux | default | 100% | 100% |
| macOS | default | 40% | 35% |
| macOS | delegated | 60% | 55% |
| macOS | cached | 80% | 40% |

*Percentages relative to native performance*

### Memory Usage

| Component | Baseline | Optimized |
|-----------|----------|-----------|
| Base image | 500MB | 300MB |
| With languages | 2GB | 1.5GB |
| With tools | 3GB | 2GB |
| Runtime | 4GB | 2.5GB |

## Optimization Checklist

**Before creating sandboxes:**
- [ ] Enable BuildKit (`export DOCKER_BUILDKIT=1`)
- [ ] Create `.dockerignore` file
- [ ] Set appropriate Docker Desktop resources
- [ ] Consider creating pre-built base image if creating multiple sandboxes

**Dockerfile optimizations:**
- [ ] Order commands by change frequency
- [ ] Clean package caches in same RUN command
- [ ] Use cache mounts for package managers
- [ ] Don't COPY source code (use volumes)

**Runtime optimizations:**
- [ ] Use delegated mounts on macOS
- [ ] Cache language package directories
- [ ] Keep containers running (don't rebuild frequently)
- [ ] Use watch modes for development

**Maintenance:**
- [ ] Regular `docker system prune`
- [ ] Monitor disk usage
- [ ] Update base images periodically
- [ ] Review and remove unused images

## Platform-Specific Recommendations

### macOS

- Use `delegated` mounts
- Increase Docker Desktop disk allocation
- Consider using colima for better performance
- Expect 50-60% of Linux performance

### Linux

- Native performance
- No special optimizations needed
- Can use host network mode safely
- Best platform for Docker development

### Windows

- Use WSL2 backend (not Hyper-V)
- Store files in WSL filesystem, not Windows
- Expect similar performance to macOS
- Enable WSL2 integration in Docker Desktop

## Measuring Impact

Track optimization effectiveness:

```bash
# Build time
time docker build -t sandbox-project .

# Container startup
time docker run --rm sandbox-project echo "ready"

# Volume mount performance
docker run --rm -v $(pwd):/test sandbox-project \
  dd if=/dev/zero of=/test/testfile bs=1M count=100

# Memory usage
docker stats sandbox-project --no-stream
```

Document baseline and optimized metrics to quantify improvements.
