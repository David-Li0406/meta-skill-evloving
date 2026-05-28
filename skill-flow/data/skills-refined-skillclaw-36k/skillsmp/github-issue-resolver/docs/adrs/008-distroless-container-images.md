# ADR-008: Distroless Container Images

## Status

**ACCEPTED** - 2025-12-09

## Context

The OpenShift Cluster Health MCP Server requires a container image strategy that balances security, performance, and operational requirements. Container base image selection significantly impacts image size, attack surface, vulnerability management, and deployment performance.

### Container Image Requirements

From the PRD, our targets are:

| Metric | Target | Critical? |
|--------|--------|-----------|
| **Binary Size** | <20MB | Yes |
| **Container Image** | <50MB | Yes |
| **Attack Surface** | Minimal | Yes |
| **Startup Time** | <1 second | Yes |
| **Vulnerability Count** | 0 CRITICAL/HIGH | Yes |

### Base Image Options Analysis

| Base Image | Size | Security | Ecosystem | Suitability |
|------------|------|----------|-----------|-------------|
| **ubuntu:22.04** | ~80MB | ⚠️ Many packages | ✅ Excellent | ❌ Too large |
| **alpine:3.18** | ~7MB | ✅ Minimal | ✅ Good | ⚠️ musl libc compatibility |
| **scratch** | 0MB | ✅ Nothing | ❌ No shell, no utils | ⚠️ Hard to debug |
| **gcr.io/distroless/static** | ~2MB | ✅ Minimal | ✅ Good | ✅ **BEST** |

### Security Concerns

Traditional base images (Ubuntu, CentOS) include:
- ❌ Shell (bash, sh) - potential command injection vector
- ❌ Package managers (apt, yum) - unnecessary attack surface
- ❌ System utilities (tar, wget, curl) - rarely needed at runtime
- ❌ C libraries with known CVEs
- ❌ Outdated dependencies

### Operational Considerations

- **Debugging**: How to troubleshoot issues without shell access?
- **Image Scanning**: How to handle base image vulnerabilities?
- **Updates**: How to update base images regularly?
- **Build Time**: Fast image builds for CI/CD

## Decision

We will use **Google's Distroless static base image** (`gcr.io/distroless/static:nonroot`) as the foundation for container images.

### Key Design Decisions

1. **Base Image**: `gcr.io/distroless/static:nonroot`
2. **Multi-Stage Build**: Compile in full Go environment, copy binary to distroless
3. **Static Binary**: CGO_ENABLED=0 for fully static linking
4. **Non-Root User**: Built-in nonroot user (UID 65532)
5. **Debug Images**: Separate debug image with busybox for troubleshooting
6. **Image Registry**: Quay.io for public distribution

## Rationale

### Why Distroless?

1. **Minimal Attack Surface**: Only contains application binary and runtime dependencies
2. **No Shell**: Prevents command injection attacks
3. **No Package Manager**: Can't install malicious software at runtime
4. **Small Size**: ~2MB base + ~15MB Go binary = ~17MB total (under 50MB target)
5. **Non-Root by Default**: Built-in nonroot user (UID 65532)
6. **Google-Maintained**: Regular security updates from Google
7. **Industry Standard**: Used by Kubernetes, Istio, and other CNCF projects

### Why Static Variant?

The `distroless/static` variant is ideal for Go applications:

```
gcr.io/distroless/static:
  - glibc (minimal)
  - ca-certificates (for HTTPS)
  - tzdata (timezone data)
  - /etc/passwd (nonroot user)
  - Nothing else
```

**No dynamic libraries needed** - Go static binary is self-contained.

### Why Not Alpine?

While Alpine is popular and small (~7MB), it has drawbacks:

| Aspect | Alpine | Distroless Static | Winner |
|--------|--------|-------------------|--------|
| **Size** | ~7MB | ~2MB | Distroless |
| **libc** | musl libc | glibc (minimal) | Distroless (glibc compatibility) |
| **Shell** | ash shell | None | Distroless (security) |
| **Package Manager** | apk | None | Distroless (security) |
| **DNS Resolution** | May have issues | Reliable | Distroless |
| **Attack Surface** | Higher (shell, apk) | Minimal | Distroless |

**Verdict**: Distroless is more secure and smaller for static Go binaries.

## Alternatives Considered

### Scratch (Empty Base)

**Pros**:
- ✅ Absolute minimal size (0MB base)
- ✅ Ultimate security (nothing to attack)
- ✅ Fast to pull

**Cons**:
- ❌ No ca-certificates (HTTPS fails)
- ❌ No /etc/passwd (user mapping issues)
- ❌ No timezone data
- ❌ Hard to debug (no utilities at all)

**Verdict**: Rejected - missing essential files for HTTPS and user management

### Ubuntu/Debian

**Pros**:
- ✅ Familiar ecosystem
- ✅ Easy debugging (full shell)
- ✅ Comprehensive package repository

**Cons**:
- ❌ Large size (80-150MB)
- ❌ Many unnecessary packages
- ❌ Frequent CVE vulnerabilities
- ❌ Violates minimal container principle

**Verdict**: Rejected - too large, too many vulnerabilities

### Red Hat UBI (Universal Base Image)

**Pros**:
- ✅ Red Hat official support
- ✅ OpenShift-optimized
- ✅ Good for enterprise

**Cons**:
- ❌ Large size (~80MB)
- ❌ Includes package manager
- ❌ More attack surface than distroless

**Verdict**: Rejected - unnecessary overhead for static Go binary

## Implementation

### Dockerfile (Multi-Stage Build)

```dockerfile
# Stage 1: Build stage (full Go environment)
FROM golang:1.21-alpine AS builder

WORKDIR /build

# Copy Go modules files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build static binary
# CGO_ENABLED=0: Fully static linking (no C dependencies)
# -ldflags="-s -w": Strip debug info and symbol table (reduces binary size)
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-s -w" \
    -o /build/mcp-server \
    ./cmd/mcp-server

# Stage 2: Runtime stage (distroless)
FROM gcr.io/distroless/static:nonroot

# Copy binary from builder
COPY --from=builder /build/mcp-server /usr/local/bin/mcp-server

# Distroless uses nonroot user (UID 65532) by default
USER nonroot:nonroot

# Health check endpoint
EXPOSE 8080

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/mcp-server"]
```

### Debug Dockerfile (For Troubleshooting)

```dockerfile
# Use debug variant with busybox shell for troubleshooting
FROM gcr.io/distroless/static:debug-nonroot

COPY --from=builder /build/mcp-server /usr/local/bin/mcp-server

USER nonroot:nonroot
EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/mcp-server"]
```

**Usage**:
```bash
# Production image
docker build -t cluster-health-mcp:0.1.0 .

# Debug image (with busybox shell)
docker build -t cluster-health-mcp:0.1.0-debug -f Dockerfile.debug .

# Debug container
docker run -it cluster-health-mcp:0.1.0-debug /busybox/sh
```

### Makefile Targets

```makefile
# Makefile
.PHONY: docker-build docker-build-debug docker-push

# Production image
docker-build:
	docker build \
		-t quay.io/openshift-aiops/cluster-health-mcp:$(VERSION) \
		-t quay.io/openshift-aiops/cluster-health-mcp:latest \
		.

# Debug image
docker-build-debug:
	docker build \
		-f Dockerfile.debug \
		-t quay.io/openshift-aiops/cluster-health-mcp:$(VERSION)-debug \
		.

# Push to Quay.io
docker-push:
	docker push quay.io/openshift-aiops/cluster-health-mcp:$(VERSION)
	docker push quay.io/openshift-aiops/cluster-health-mcp:latest

# Multi-arch build (amd64, arm64)
docker-buildx:
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		-t quay.io/openshift-aiops/cluster-health-mcp:$(VERSION) \
		--push \
		.
```

### Binary Size Optimization

```bash
# Build static binary with size optimization
CGO_ENABLED=0 go build \
  -ldflags="-s -w" \
  -trimpath \
  -o mcp-server \
  ./cmd/mcp-server

# Strip additional symbols (if needed)
strip -s mcp-server

# Compress with UPX (optional, not recommended for production)
# upx --best --lzma mcp-server
```

**Size Breakdown**:
```
go build (default):       ~30 MB
-ldflags="-s -w":        ~20 MB (-33%)
-trimpath:               ~18 MB (-40%)
strip:                   ~15 MB (-50%)
```

### Image Size Verification

```bash
# Build image
docker build -t cluster-health-mcp:test .

# Check image size
docker images cluster-health-mcp:test

# Expected output:
# REPOSITORY            TAG    IMAGE ID      CREATED        SIZE
# cluster-health-mcp    test   abc123...     1 minute ago   18MB
```

**Target**: <50MB ✅

## Security Benefits

### Attack Surface Reduction

```
Traditional Ubuntu Image:
├── bash, sh (shells)
├── apt, dpkg (package managers)
├── curl, wget (download tools)
├── tar, gzip (compression)
├── Python, Perl (interpreters)
├── 100+ system utilities
└── Total: ~1000+ files

Distroless Image:
├── mcp-server (our binary)
├── ca-certificates
├── /etc/passwd
├── tzdata
└── Total: ~20 files
```

**Reduction**: 98% fewer files = 98% less attack surface

### Vulnerability Comparison

```bash
# Scan Ubuntu-based image
trivy image ubuntu-based-mcp:latest
# Result: 50+ vulnerabilities (10 CRITICAL, 20 HIGH)

# Scan Distroless image
trivy image distroless-mcp:latest
# Result: 0-2 vulnerabilities (typically 0 CRITICAL/HIGH)
```

### No Runtime Exploitation

Without shell or package manager, attackers cannot:

- ❌ Execute shell commands (no bash/sh)
- ❌ Install malware (no apt/yum)
- ❌ Download payloads (no curl/wget)
- ❌ Modify system files (read-only FS + no tools)
- ❌ Escalate privileges (no su/sudo)

## Operational Considerations

### Debugging Without Shell

**Problem**: How to debug issues without `/bin/sh`?

**Solutions**:

1. **Use Debug Image**:
   ```bash
   # Deploy debug variant temporarily
   oc patch deployment cluster-health-mcp \
     -p '{"spec":{"template":{"spec":{"containers":[{"name":"mcp-server","image":"quay.io/openshift-aiops/cluster-health-mcp:0.1.0-debug"}]}}}}'

   # Exec into container with busybox shell
   oc exec -it cluster-health-mcp-xxx -- /busybox/sh
   ```

2. **Ephemeral Debug Containers** (Kubernetes 1.23+):
   ```bash
   # Attach debug container with tools
   oc debug cluster-health-mcp-xxx --image=busybox
   ```

3. **Log Analysis**:
   ```bash
   # View logs (structured JSON)
   oc logs cluster-health-mcp-xxx | jq

   # Stream logs
   oc logs -f cluster-health-mcp-xxx
   ```

4. **Metrics and Tracing**:
   ```bash
   # Prometheus metrics
   curl http://cluster-health-mcp:8080/metrics

   # Health check
   curl http://cluster-health-mcp:8080/health
   ```

### Image Updates

```yaml
# .github/workflows/update-base-image.yml
name: Update Base Image

on:
  schedule:
    # Check for distroless updates weekly
    - cron: '0 0 * * 0'
  workflow_dispatch:

jobs:
  update-base:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check for distroless updates
        run: |
          # Pull latest distroless image
          docker pull gcr.io/distroless/static:nonroot

          # Rebuild our image
          docker build -t cluster-health-mcp:latest .

          # Scan for vulnerabilities
          trivy image cluster-health-mcp:latest

      - name: Create PR if updates available
        # ... create PR with updated image
```

### CI/CD Integration

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: '1.21'

      - name: Build binary
        run: make build

      - name: Build container image
        run: make docker-build

      - name: Scan image for vulnerabilities
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: cluster-health-mcp:latest
          severity: CRITICAL,HIGH
          exit-code: 1

      - name: Verify image size
        run: |
          SIZE=$(docker images cluster-health-mcp:latest --format "{{.Size}}" | sed 's/MB//')
          if (( $(echo "$SIZE > 50" | bc -l) )); then
            echo "Image size $SIZE MB exceeds 50MB limit"
            exit 1
          fi

      - name: Push to Quay.io
        if: github.ref == 'refs/heads/main'
        run: |
          echo "${{ secrets.QUAY_PASSWORD }}" | docker login -u "${{ secrets.QUAY_USERNAME }}" --password-stdin quay.io
          make docker-push
```

## Performance Benefits

### Startup Time

```
Ubuntu-based image:
  - Pull time: 15-20 seconds (80MB)
  - Start time: 2-3 seconds (systemd, init scripts)
  - Total: 17-23 seconds

Distroless image:
  - Pull time: 3-5 seconds (18MB)
  - Start time: <1 second (direct binary exec)
  - Total: 4-6 seconds

Improvement: 75% faster
```

### Resource Usage

```
Ubuntu-based:
  Memory: 80-120 MB (base image + binary)
  Disk: 80 MB

Distroless:
  Memory: 30-50 MB (binary only)
  Disk: 18 MB

Savings: 60% memory, 78% disk
```

## Success Criteria

### Phase 1 Success (Week 1)
- ✅ Dockerfile builds successfully
- ✅ Binary is statically linked (CGO_ENABLED=0)
- ✅ Image size <50MB
- ✅ Image runs in OpenShift with restricted-v2 SCC

### Phase 2 Success (Week 2)
- ✅ Vulnerability scan shows 0 CRITICAL/HIGH issues
- ✅ Debug image working for troubleshooting
- ✅ Multi-arch build (amd64, arm64) successful
- ✅ CI/CD pipeline publishing to Quay.io

### Phase 3 Success (Week 3)
- ✅ Production deployment stable
- ✅ Startup time <1 second
- ✅ Memory usage <50MB at rest
- ✅ Regular base image updates automated

## Monitoring

### Image Metrics

```prometheus
# Prometheus metrics for image monitoring
container_image_size_bytes{image="cluster-health-mcp"}
container_image_pull_duration_seconds{image="cluster-health-mcp"}
container_vulnerabilities_total{image="cluster-health-mcp",severity="critical"}
```

### Alerts

```yaml
# Prometheus alert rules
groups:
- name: container-images
  rules:
  - alert: ImageSizeTooLarge
    expr: container_image_size_bytes{image="cluster-health-mcp"} > 52428800  # 50MB
    annotations:
      summary: "Container image exceeds 50MB size limit"

  - alert: ImageVulnerabilities
    expr: container_vulnerabilities_total{image="cluster-health-mcp",severity="critical"} > 0
    annotations:
      summary: "Container image has critical vulnerabilities"
```

## Related ADRs

- [ADR-001: Go Language Selection](001-go-language-selection.md)
- [ADR-007: RBAC-Based Security Model](007-rbac-based-security-model.md)

## References

- [Google Distroless Images](https://github.com/GoogleContainerTools/distroless)
- [Distroless Best Practices](https://github.com/GoogleContainerTools/distroless/blob/main/README.md)
- [Go Static Binary Compilation](https://www.arp242.net/static-go.html)
- [OpenShift Cluster Health MCP PRD](../../PRD.md)

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Debugging difficulty** | Medium | Low | Debug image variant, ephemeral containers |
| **Base image updates** | Low | Low | Automated weekly update checks |
| **Compatibility issues** | Low | Medium | Static linking eliminates library dependencies |
| **Image pull failures** | Low | Low | Multi-registry mirrors, cached layers |

## Approval

- **Architect**: Approved
- **Security Team**: Approved
- **Platform Team**: Approved
- **Date**: 2025-12-09
