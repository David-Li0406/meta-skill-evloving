# Google Distroless Images

Distroless images contain only your application and its runtime dependencies. They do not contain package managers, shells or any other programs you would expect to find in a standard Linux distribution.

## Overview

| Property | Value |
|----------|-------|
| Provider | Google |
| Registry | `gcr.io/distroless` |
| Documentation | https://github.com/GoogleContainerTools/distroless |
| Security Rating | Very High |

## Features

- Minimal attack surface
- No shell or package manager
- Signed with cosign
- SBOM available
- Regular security updates

## Available Images

### Static Binary Images

| Image | Languages | Use Case | Notes |
|-------|-----------|----------|-------|
| `gcr.io/distroless/static-debian12` | Go, Rust | Static binaries with no external dependencies | Smallest possible image, for fully static binaries only |
| `gcr.io/distroless/base-debian12` | Go, Rust, C, C++ | Binaries that need glibc | Includes glibc, libssl, and CA certificates |
| `gcr.io/distroless/cc-debian12` | Rust, C, C++ | Binaries with C/C++ dependencies | Includes libgcc and libstdc++ |

### Node.js Images

| Image | Use Case | Notes |
|-------|----------|-------|
| `gcr.io/distroless/nodejs20-debian12` | Node.js 20 applications | Node.js 20 LTS runtime, minimal footprint |
| `gcr.io/distroless/nodejs22-debian12` | Node.js 22 applications | Node.js 22 runtime |

### Python Images

| Image | Use Case | Notes |
|-------|----------|-------|
| `gcr.io/distroless/python3-debian12` | Python 3 applications | Python 3 runtime, no pip included |

### Java Images

| Image | Use Case | Notes |
|-------|----------|-------|
| `gcr.io/distroless/java21-debian12` | Java 21 applications | OpenJDK 21 JRE |
| `gcr.io/distroless/java17-debian12` | Java 17 LTS applications | OpenJDK 17 LTS JRE |

## Best Practices

1. **Use multi-stage builds**: Build in full image, deploy with distroless
2. **Copy only required artifacts**: Only copy what's needed to the distroless image
3. **Debug variants**: For debugging, use `:debug` tag variant (includes busybox shell)
4. **Pin to SHA digests**: Use specific SHA digests for reproducibility

## Example Multi-stage Dockerfile

```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o /app/myapp

# Production stage
FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/myapp /myapp
ENTRYPOINT ["/myapp"]
```

## Debugging

For debugging purposes, use the `:debug` variant which includes a busybox shell:

```bash
docker run -it gcr.io/distroless/python3-debian12:debug sh
```
