# Chainguard Images

Chainguard Images are minimal, hardened container images with zero or near-zero CVEs. They are built using Wolfi, a Linux undistro designed for containers.

## Overview

| Property | Value |
|----------|-------|
| Provider | Chainguard |
| Registry | `cgr.dev/chainguard` |
| Documentation | https://www.chainguard.dev/chainguard-images |
| Security Rating | Very High |

## Features

- Zero or near-zero CVEs
- Signed with Sigstore
- SLSA Level 3 provenance
- SBOM included
- Daily rebuilds for security patches
- Minimal attack surface

## Available Images

### Static Binary Images

| Image | Languages | Use Case | Stage |
|-------|-----------|----------|-------|
| `chainguard/static:latest` | Go, Rust | Static binaries with no external dependencies | Production |
| `chainguard/glibc-dynamic:latest` | Go, Rust, C, C++ | Dynamically linked binaries | Production |

**Notes**: Static is the smallest Chainguard image with no libc. Use glibc-dynamic for binaries that require dynamic linking.

### Node.js Images

| Image | Use Case | Stage |
|-------|----------|-------|
| `chainguard/node:latest` | Node.js production applications | Production |
| `chainguard/node:latest-dev` | Node.js build and development | Build |

**Notes**: Production image is minimal runtime. Dev image includes npm and shell for building.

### Python Images

| Image | Use Case | Stage |
|-------|----------|-------|
| `chainguard/python:latest` | Python production applications | Production |
| `chainguard/python:latest-dev` | Python build and development | Build |

**Notes**: Production image is minimal runtime. Dev image includes pip and shell for building.

### Go Images

| Image | Use Case | Stage |
|-------|----------|-------|
| `chainguard/go:latest` | Go application builds | Build |

**Notes**: Full Go toolchain for building. Use `chainguard/static` for production.

### Java Images

| Image | Languages | Use Case | Stage |
|-------|-----------|----------|-------|
| `chainguard/jre:latest` | Java, Kotlin, Scala | Java production applications | Production |
| `chainguard/jdk:latest` | Java, Kotlin, Scala | Java builds | Build |

**Notes**: JRE is minimal runtime. JDK includes full toolchain for building.

### Ruby Images

| Image | Use Case | Stage |
|-------|----------|-------|
| `chainguard/ruby:latest` | Ruby production applications | Production |

### Rust Images

| Image | Use Case | Stage |
|-------|----------|-------|
| `chainguard/rust:latest` | Rust application builds | Build |

**Notes**: Full Rust toolchain for building. Use `chainguard/static` for production.

### .NET Images

| Image | Languages | Use Case | Stage |
|-------|-----------|----------|-------|
| `chainguard/dotnet-runtime:latest` | .NET, C#, F# | .NET production applications | Production |
| `chainguard/dotnet-sdk:latest` | .NET, C#, F# | .NET builds | Build |

### Infrastructure Images

| Image | Use Case | Stage |
|-------|----------|-------|
| `chainguard/nginx:latest` | Web server and reverse proxy | Production |
| `chainguard/postgres:latest` | PostgreSQL database | Production |
| `chainguard/redis:latest` | Redis cache/database | Production |

## Best Practices

1. **Use appropriate variants**: Use `:latest-dev` variants for build stages, `:latest` for production
2. **Non-root by default**: Chainguard images use nonroot user by default - applications must support this
3. **Use enterprise registry**: Use `cgr.dev/chainguard` registry for enterprise support
4. **Check full catalog**: See https://images.chainguard.dev for complete image catalog

## Example Multi-stage Dockerfile

```dockerfile
# Build stage
FROM chainguard/go:latest AS builder
WORKDIR /app
COPY . .
RUN go build -o /app/myapp

# Production stage
FROM chainguard/static:latest
COPY --from=builder /app/myapp /myapp
ENTRYPOINT ["/myapp"]
```
