# Hardened Base Images and Gold Images

## Overview

Using hardened or "distroless" base images is a cornerstone of **engineering reliability** - creating standardized, secure runtime environments that are consistent across development, staging, and production. Combined with version normalization (see: version-normalization-guide.md), this ensures reproducible builds with both consistent dependencies and runtime environments.

### Reliability Benefits

- **Consistent environments**: Same base image across all environments eliminates "works on my machine" issues
- **Reduced attack surface**: Fewer packages means fewer vulnerabilities and simpler patching
- **Predictable updates**: Controlled image versioning with SBOMs for transparency
- **Faster builds**: Smaller images pull and deploy faster

## What Are Gold Images?

Gold images (or "golden images") are pre-approved, security-hardened base images that:
- Contain only essential runtime components
- Are regularly patched and scanned
- Meet organizational security standards
- Provide a trusted foundation for application containers

## Image Types Comparison

| Type | Shell | Package Manager | Size | Attack Surface |
|------|-------|-----------------|------|----------------|
| Standard (ubuntu, debian) | Yes | Yes | 100-200MB | High |
| Slim variants | Limited | Limited | 50-100MB | Medium |
| Alpine | Yes (ash) | apk | 5-10MB | Medium |
| Distroless | No | No | 2-20MB | Low |
| Scratch | No | No | 0MB | Minimal |

## Hardened Image Providers Comparison

| Provider | Pricing | Key Features | Best For |
|----------|---------|--------------|----------|
| **Chainguard** | Free tier + Enterprise | 1000+ images, Wolfi-based, SBOMs, signatures | Enterprise, broad catalog |
| **Minimus** | Free tier + Enterprise | 95%+ vuln reduction, FedRAMP/PCI compliant | Regulated industries |
| **Google Distroless** | Free | Established, Debian-based, Google maintained | General use |
| **Docker Hardened** | Docker subscription | Docker Hub integration | Docker ecosystem users |

### Vulnerability Comparison (Typical Results)

| Image Type | Fixable CVEs |
|------------|--------------|
| Standard base (debian/ubuntu) | 30-100+ |
| Alpine | 10-20 |
| Google Distroless | 0-2 |
| Chainguard | 0 |
| Minimus | 0 |

## Distroless Images

### Google Distroless

Google's distroless images contain only the application and runtime dependencies—no shell, package manager, or other utilities.

```dockerfile
# VULNERABLE - Full OS with many packages
FROM ubuntu:22.04
COPY myapp /app
CMD ["/app"]

# SECURE - Distroless base
FROM gcr.io/distroless/static-debian12
COPY myapp /app
CMD ["/app"]
```

**Available Images:**
- `gcr.io/distroless/static` - Static binaries (Go, Rust)
- `gcr.io/distroless/base` - glibc + openssl
- `gcr.io/distroless/cc` - libgcc
- `gcr.io/distroless/java` - OpenJDK
- `gcr.io/distroless/python3` - Python 3
- `gcr.io/distroless/nodejs` - Node.js

### Chainguard Images

Chainguard provides hardened, SBOM-included, signed images built on Wolfi OS.

```dockerfile
# Using Chainguard base image
FROM cgr.dev/chainguard/python:latest
COPY --chown=nonroot:nonroot app/ /app/
WORKDIR /app
CMD ["python", "main.py"]

# Using Chainguard static image
FROM cgr.dev/chainguard/static:latest
COPY myapp /app
ENTRYPOINT ["/app"]
```

**Key Features:**
- Built-in SBOMs (CycloneDX, SPDX)
- Sigstore signatures for verification
- Daily CVE patching
- No shell by default
- Non-root user enforcement
- 1000+ images available

**Available Categories:**
- `cgr.dev/chainguard/static` - Minimal static binary base
- `cgr.dev/chainguard/glibc-dynamic` - Dynamic linking support
- `cgr.dev/chainguard/python` - Python runtime
- `cgr.dev/chainguard/node` - Node.js runtime
- `cgr.dev/chainguard/go` - Go build environment
- `cgr.dev/chainguard/jre` - Java runtime

### Minimus Images

Minimus provides hardened container images with 95%+ vulnerability reduction, particularly suited for regulated industries (FedRAMP, PCI, HIPAA, NIST).

```dockerfile
# Using Minimus Python image
FROM minimus.io/python:3.11
COPY --chown=nonroot:nonroot app/ /app/
WORKDIR /app
CMD ["python", "main.py"]

# Using Minimus Node.js image
FROM minimus.io/node:20
COPY --chown=nonroot:nonroot . /app
WORKDIR /app
CMD ["node", "server.js"]
```

**Key Features:**
- 90%+ package reduction vs standard images (e.g., nginx: 231 → 15 packages)
- Continuous rebuilds from upstream sources
- Production (distroless) + Dev (with shell) image pairs
- Auto-generated SBOMs
- FedRAMP, PCI-DSS, CIS, NIST compliance ready
- Government, healthcare, financial services focus

**Available Images:**
- `minimus.io/python` - Python runtime
- `minimus.io/node` - Node.js runtime
- `minimus.io/nginx` - Nginx web server
- `minimus.io/java` - Java runtime
- `minimus.io/go` - Go runtime

**Minimus vs Chainguard:**

| Feature | Minimus | Chainguard |
|---------|---------|------------|
| Image catalog | Growing | 1000+ |
| Dev/Debug images | Yes (paired) | Debug variants |
| Compliance focus | FedRAMP, PCI, HIPAA | General enterprise |
| Base OS | Custom minimal | Wolfi OS |
| Free tier | Yes | Yes (limited) |
| SBOM included | Yes | Yes |
| Signatures | Yes | Yes (Sigstore) |

## Multi-Stage Builds

Use multi-stage builds to keep final images minimal:

```dockerfile
# Build stage with full toolchain
FROM golang:1.21-alpine AS builder
WORKDIR /build
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o app .

# Runtime stage - distroless
FROM gcr.io/distroless/static-debian12
COPY --from=builder /build/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

### Language-Specific Examples

**Node.js:**
```dockerfile
# Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Runtime
FROM gcr.io/distroless/nodejs20-debian12
COPY --from=builder /app /app
WORKDIR /app
CMD ["server.js"]
```

**Python:**
```dockerfile
# Build
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target=/deps

# Runtime
FROM gcr.io/distroless/python3-debian12
COPY --from=builder /deps /deps
COPY app.py /app/
ENV PYTHONPATH=/deps
WORKDIR /app
CMD ["app.py"]
```

**Java:**
```dockerfile
# Build
FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

# Runtime
FROM gcr.io/distroless/java21-debian12
COPY --from=builder /build/target/app.jar /app.jar
CMD ["/app.jar"]
```

## Verifying Image Signatures

### Cosign Verification

```bash
# Install cosign
brew install cosign

# Verify Chainguard image
cosign verify cgr.dev/chainguard/python:latest \
  --certificate-identity-regexp=".*" \
  --certificate-oidc-issuer-regexp=".*"

# Verify Google distroless
cosign verify gcr.io/distroless/static-debian12 \
  --certificate-identity-regexp=".*" \
  --certificate-oidc-issuer-regexp=".*"
```

### SBOM Extraction

```bash
# Get SBOM from Chainguard image
cosign download sbom cgr.dev/chainguard/python:latest > sbom.json

# View SBOM contents
cat sbom.json | jq '.components | length'

# Scan SBOM for vulnerabilities
osv-scanner --sbom=sbom.json
```

## Scanning and Hardening

### Vulnerability Scanning

```bash
# Trivy scan
trivy image gcr.io/distroless/static-debian12

# osv-scanner scan
osv-scanner --sbom=sbom.json

# Compare results
echo "Distroless:" && trivy image --severity HIGH,CRITICAL gcr.io/distroless/static-debian12
echo "Ubuntu:" && trivy image --severity HIGH,CRITICAL ubuntu:22.04
```

### Dockerfile Linting

```bash
# Hadolint for Dockerfile best practices
hadolint Dockerfile

# Common recommendations:
# - DL3007: Using latest is prone to errors
# - DL3018: Pin versions in apk add
# - DL3025: Use JSON notation for CMD
```

## Image Selection Matrix

| Use Case | Recommended Base | Alternative | Reason |
|----------|------------------|-------------|--------|
| Go static binary | `gcr.io/distroless/static` | `cgr.dev/chainguard/static` | No runtime deps |
| Go with CGO | `gcr.io/distroless/base` | `cgr.dev/chainguard/glibc-dynamic` | glibc needed |
| Node.js app | `cgr.dev/chainguard/node` | `minimus.io/node` | SBOM + signing |
| Python app | `cgr.dev/chainguard/python` | `minimus.io/python` | Daily patches |
| Java app | `gcr.io/distroless/java21` | `cgr.dev/chainguard/jre` | JRE only |
| Rust binary | Scratch | `gcr.io/distroless/static` | Static linking |
| .NET app | `mcr.microsoft.com/dotnet/runtime-deps` | - | Microsoft maintained |
| Nginx/Web | `cgr.dev/chainguard/nginx` | `minimus.io/nginx` | 90%+ package reduction |
| Regulated (FedRAMP) | `minimus.io/*` | `cgr.dev/chainguard/*` | Compliance ready |

## Registry Policies

### Allow-listing Gold Images

```yaml
# OPA/Gatekeeper policy
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sAllowedRepos
metadata:
  name: allowed-base-images
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    repos:
      - "gcr.io/distroless/"
      - "cgr.dev/chainguard/"
      - "mcr.microsoft.com/dotnet/"
```

### CI/CD Enforcement

```yaml
# GitHub Actions check
- name: Check base image
  run: |
    BASE_IMAGE=$(grep "^FROM" Dockerfile | head -1 | awk '{print $2}')
    ALLOWED="gcr.io/distroless|cgr.dev/chainguard"
    if ! echo "$BASE_IMAGE" | grep -qE "$ALLOWED"; then
      echo "ERROR: Base image must be distroless or Chainguard"
      exit 1
    fi
```

## Debugging Distroless Containers

Since distroless has no shell, debugging requires different approaches:

```bash
# Option 1: Debug image variant (has busybox shell)
FROM gcr.io/distroless/python3-debian12:debug
# Then: kubectl debug -it pod/mypod --image=busybox

# Option 2: Ephemeral containers (K8s 1.23+)
kubectl debug -it mypod --image=busybox --target=mycontainer

# Option 3: Copy files out
kubectl cp mypod:/app/logs.txt ./logs.txt
```

## Migration Checklist

- [ ] Audit current base images
- [ ] Identify runtime requirements per language
- [ ] Create multi-stage Dockerfiles
- [ ] Test with distroless images
- [ ] Verify signature and SBOM availability
- [ ] Update CI/CD pipelines
- [ ] Configure registry policies
- [ ] Document debugging procedures
- [ ] Monitor for CVEs and update regularly

## References

- [Google Distroless](https://github.com/GoogleContainerTools/distroless)
- [Chainguard Images](https://edu.chainguard.dev/chainguard/chainguard-images/)
- [Minimus.io](https://www.minimus.io/) - Secure, minimal container images
- [Minimus Documentation](https://docs.minimus.io/)
- [Wolfi OS](https://github.com/wolfi-dev)
- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Cosign](https://github.com/sigstore/cosign)
- [Container Base Image Vulnerability Comparison](https://images.latio.com/)
