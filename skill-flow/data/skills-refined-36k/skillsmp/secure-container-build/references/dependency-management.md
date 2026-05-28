# Dependency Management Best Practices

## Python + uv

### Why uv?

- **10-100x faster**: Rust-based package installer
- **Reproducible builds**: Lock file ensures consistent dependencies
- **Cache-friendly**: Excellent support for Docker layer caching
- **Modern**: Designed for container and CI environments

### uv Configuration

```dockerfile
# Install uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Configure uv for containers
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never
```

### Optimal Build Pattern

```dockerfile
# Install dependencies first (cached layer)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --no-editable

# Copy source code
COPY . ./

# Install project (separate layer for optimal caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable
```

## Bun

### Why Bun?

- **Fast package installation**: Built-in package manager
- **All-in-one**: Runtime + package manager + bundler
- **Drop-in replacement**: Compatible with npm/yarn/pnpm
- **Small binaries**: Can compile standalone executables

### Bun Configuration

```dockerfile
# Install bun from official image
COPY --from=docker.io/oven/bun:slim /usr/local/bin/bun /usr/local/bin/

# Create symlink for bunx
RUN ln -sf ./bun /usr/local/bin/bunx
```

### Lock File Usage

```dockerfile
# Copy lock file first for caching
COPY package.json bun.lockb* /app/

# Install with frozen lockfile
RUN bun install --frozen-lockfile
```

## Node.js + pnpm

### Why pnpm?

- **Disk efficient**: Content-addressable storage
- **Fast**: Symlink-based approach
- **Strict**: Better dependency resolution than npm
- **Workspace support**: Monorepo-friendly

### pnpm Configuration

```dockerfile
# Enable corepack (pnpm included in Node.js)
RUN corepack enable && corepack use pnpm

# Use cache mount for pnpm store
RUN --mount=type=cache,id=pnpm,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile --production=false
```

### Production Optimization

```dockerfile
# Build TypeScript
RUN pnpm exec tsc --project .
RUN pnpm build

# Remove devDependencies for runtime
RUN pnpm prune --production
```

## Golang + Go Modules

### Why Go Modules?

- **Built-in dependency management**: No external tools needed (since Go 1.11)
- **Reproducible builds**: go.sum ensures version integrity
- **Fast**: Module cache works well with Docker layer caching
- **Vendoring optional**: Can vendor with `go mod vendor` if needed

### Optimal Build Pattern

```dockerfile
# Copy go.mod and go.sum first (cached layer)
COPY go.mod go.sum ./

# Download dependencies (separate layer for better caching)
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Copy source code
COPY . ./

# Build with caches for both modules and build artifacts
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app/server .
```

### CGO vs Static Builds

**CGO_ENABLED=0 (Static Binary):**
```dockerfile
# Build static binary (no runtime dependencies)
RUN CGO_ENABLED=0 GOOS=linux \
    go build -ldflags="-w -s" -o /app/server .

# Runtime: Use static base image
FROM cgr.dev/chainguard/static:latest
```

**Benefits:**
- Single standalone binary (no glibc needed)
- Smallest possible image (~10-20MB)
- Most portable and secure
- Cannot use packages with C bindings

**CGO_ENABLED=1 (Dynamic Binary):**
```dockerfile
# Build with CGO enabled (can use C libraries)
RUN CGO_ENABLED=1 GOOS=linux \
    go build -ldflags="-w -s" -o /app/server .

# Runtime: Use glibc-dynamic base image
FROM cgr.dev/chainguard/glibc-dynamic:latest
```

**Benefits:**
- Can use packages with C bindings (SQLite, libgit2, etc.)
- Requires glibc at runtime
- Slightly larger image (~30-50MB)

**Build flags:**
- `-ldflags="-w -s"` - Strip debug info and symbol table (smaller binary)
- `-trimpath` - Remove file system paths from binary (reproducibility)

### When to Use CGO

✅ **Use static (CGO_ENABLED=0) if:**
- Pure Go code and dependencies
- Most web services, APIs, CLI tools

❌ **Use CGO (CGO_ENABLED=1) if:**
- Using `mattn/go-sqlite3` or other C library bindings
- Build fails with `CGO_ENABLED=0`

## Cache Mount Best Practices

### BuildKit Cache Mounts

Use cache mounts to speed up dependency installation:

```dockerfile
# Python/uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# pnpm
RUN --mount=type=cache,id=pnpm,target=/root/.local/share/pnpm/store \
    pnpm install

# npm
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Go modules
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Go build (with both module and build cache)
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app/server .
```

### Benefits

- **Faster builds**: Dependencies cached across builds
- **Lower bandwidth**: Don't re-download unchanged packages
- **CI-friendly**: Cache persists between workflow runs

## Lock File Management

### Always Commit Lock Files

```
✅ COMMIT:
- uv.lock
- bun.lockb
- pnpm-lock.yaml
- package-lock.json

❌ DO NOT COMMIT:
- node_modules/
- .venv/
- __pycache__/
```

### Use Frozen Lock Files in CI

```dockerfile
# Python/uv
uv sync --frozen  # Fail if lock file out of sync

# Bun
bun install --frozen-lockfile

# pnpm
pnpm install --frozen-lockfile

# npm
npm ci  # Clean install from lock file
```

## Dependency Updates

### Update Strategy

1. **Development**: Update dependencies locally
2. **Lock files**: Commit updated lock files
3. **CI**: Build validates lock files work
4. **Production**: Deploy with frozen dependencies

### Security Updates

- Run dependency audits: `uv pip check`, `npm audit`, `pnpm audit`, `cargo audit`
- Use Dependabot or Renovate for automated updates
- Test updates in CI before merging

## Rust + Cargo

### Why Cargo?

- **Built-in dependency management**: No external tools needed
- **Reproducible builds**: Cargo.lock ensures version integrity
- **Fast**: cargo build with cache mounts
- **Multi-target**: Cross-compile for different platforms (glibc, musl)

### glibc vs musl

| Aspect | glibc (Default) | musl (Advanced) |
|--------|-----------------|-----------------|
| **Runtime** | glibc-dynamic | static |
| **Image Size** | ~30-50MB | ~10-20MB |
| **Compatibility** | All crates | No C bindings |
| **Performance** | Good | ⚠️ Slow without mimalloc |
| **Allocator Options** | 3 choices | Must use mimalloc |

**Recommendation:** Start with glibc template. Use musl only if image size is critical.

### Cache Strategy

Rust builds benefit from caching both the registry and target directory:

```dockerfile
# Registry and target cache (both important for Rust)
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release
```

### Dependency Pre-caching

Separate dependency compilation from application build for optimal layer caching:

```dockerfile
# Copy only manifests first
COPY Cargo.toml Cargo.lock ./

# Create dummy source to build dependencies
RUN mkdir -p src && echo "fn main() {}" > src/main.rs

# Download and compile dependencies (cached layer)
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release

# Now copy real source (dependencies already cached)
COPY . .

# Build application (fast because dependencies are cached)
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release
```

### Allocator Options

**Why allocator choice matters:**

glibc's default malloc can use **2x+ memory** under load due to fragmentation. Modern allocators like mimalloc reduce memory footprint by ~50% and improve latency.

**For detailed comparison** of mimalloc vs jemalloc vs tcmalloc vs glibc malloc, see [allocator-comparison.md](./allocator-comparison.md).

**glibc version - three choices:**

| Option | Method | Code Changes? | Performance | Memory |
|--------|--------|---------------|-------------|--------|
| (a) Cargo + mimalloc | Static link | Yes | Best ⭐ | 50% less |
| (b) LD_PRELOAD | Uncomment ENV | No | Good | 50% less |
| (c) Default malloc | Nothing | No | OK | Baseline |

**Example: Option (a) - Cargo + mimalloc**

```toml
# Cargo.toml
[dependencies]
mimalloc = { version = "0.1", default-features = false }
```

```rust
// src/main.rs
#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;
```

**musl version - only one viable option:**

musl's allocator is 7-10x slower in multi-threaded workloads. You MUST add mimalloc:

```toml
# Cargo.toml - for musl targets only
[target.'cfg(target_env = "musl")'.dependencies]
mimalloc = { version = "0.1", default-features = false }
```

```rust
// src/main.rs
#[cfg(target_env = "musl")]
#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;
```

### Multi-arch Support

The musl template supports multi-arch via TARGETARCH:

```dockerfile
ARG TARGETARCH
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    if [ "$TARGETARCH" = "arm64" ]; then \
      RUST_TARGET="aarch64-unknown-linux-musl"; \
    else \
      RUST_TARGET="x86_64-unknown-linux-musl"; \
    fi && \
    cargo build --target $RUST_TARGET --release
```

### Lock File Management

Always commit `Cargo.lock`:

```
✅ COMMIT:
- Cargo.lock

❌ DO NOT COMMIT:
- target/
```

Use `--locked` in CI to ensure reproducible builds:

```bash
cargo build --release --locked
```:
