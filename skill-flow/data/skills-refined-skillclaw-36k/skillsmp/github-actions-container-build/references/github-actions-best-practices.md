# GitHub Actions Multi-arch Build Best Practices

## Public vs Private Repos: Choosing the Right Approach

### Decision Flowchart

```
Question 1: Is your repo public?
│
├─ YES (Public Repo)
│  └─ Use Standard ARM64 Runners ✅
│     • Free ubuntu-24.04-arm runners
│     • 10-50x faster (native)
│     • No setup required
│     → Use github-actions-workflow-matrix-build.yml
│
└─ NO (Private Repo)
   │
   Question 2: Have Team/Enterprise + willing to pay?
   │
   ├─ YES
   │  └─ Use ARM64 Larger Runners 💰
   │     • Custom runner setup required
   │     • Billed per minute (~37% cheaper than x64)
   │     • 10-50x faster (native)
   │     → Create custom ARM64 runner, modify workflow
   │
   └─ NO
      └─ Use QEMU Emulation ⚠️
         • Free tier compatible
         • 10-50x slower (emulation)
         • No additional setup
         → Use github-actions-workflow-qemu.yml
```

### Why This Matters

**Standard ARM64 runners (`ubuntu-24.04-arm`):**
- ✅ **Public repos**: Free, unlimited, works out of the box
- ❌ **Private repos**: **Don't work at all** (workflow will fail)

**ARM64 Larger Runners (custom runners):**
- ✅ **Private repos with Team/Enterprise**: Available (requires setup + billing)
- ❌ **Free tier**: Not available

**QEMU Emulation:**
- ✅ **All repos**: Works on free tier
- ⚠️ **Performance**: 10-50x slower than native

---

## Multi-arch Build Approaches Compared

GitHub made arm64 runners (`ubuntu-24.04-arm`) generally available in September 2024 with **37% lower cost** than x64 runners, fundamentally changing the multi-arch build landscape by eliminating the need for slow QEMU emulation.

### The Four Podman Approaches

| Approach | Storage Overhead | Artifact Size | Build Performance | Best For |
|----------|------------------|---------------|-------------------|----------|
| **Architecture tags** | 2x (images + manifest) | None | Native | Simple workflows, debugging |
| **Push-by-digest** | 1x (single per arch) | ~70 bytes | Native | Production (recommended) |
| **OCI artifacts** | 3x (upload + download + final) | Full images | Native + I/O | Maximum privacy |
| **Podman Farm** | 1x | N/A | Native | Dedicated infrastructure |

---

## 1. Push-by-Digest (2025 Best Practice - Default)

**This is the recommended approach.** Images are pushed by digest without intermediate tags. Only tiny digest files (~70 bytes) transfer as artifacts.

```yaml
# Build job (runs on each architecture)
steps:
  - name: Build image
    run: |
      podman build \
        --format docker \
        --platform linux/${{ matrix.arch }} \
        -t localhost/build:${{ matrix.arch }} \
        -f ./Containerfile \
        .

  - name: Push by digest
    run: |
      podman push \
        --digestfile /tmp/digest \
        localhost/build:${{ matrix.arch }} \
        docker://${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

  - name: Upload digest artifact
    uses: actions/upload-artifact@v5
    with:
      name: digest-${{ matrix.arch }}
      path: /tmp/digest
      retention-days: 1

# Merge job (creates manifest from digests)
steps:
  - uses: actions/download-artifact@v6
    with:
      path: /tmp/digests
      pattern: digest-*
      merge-multiple: true

  - name: Create and push manifest
    run: |
      AMD64_DIGEST=$(cat /tmp/digests/amd64)
      ARM64_DIGEST=$(cat /tmp/digests/arm64)

      podman manifest create "$IMAGE:latest"
      podman manifest add "$IMAGE:latest" "docker://$IMAGE@${AMD64_DIGEST}"
      podman manifest add "$IMAGE:latest" "docker://$IMAGE@${ARM64_DIGEST}"
      podman manifest push --all "$IMAGE:latest" "docker://$IMAGE:latest"
```

**Pros:** Minimal storage (1x), clean registry (no intermediate tags), tiny artifacts
**Cons:** Slightly more complex than architecture tags

---

## 2. Architecture Tags (Simpler Alternative)

Build each architecture with explicit tags. Simple and debuggable:

```yaml
# Build job pushes architecture-specific tags
- name: Build & push
  run: |
    podman build \
      --format docker \
      --platform linux/${{ matrix.arch }} \
      -t "$IMAGE:${{ matrix.arch }}" \
      .
    podman push "$IMAGE:${{ matrix.arch }}"

# Merge job creates manifest from tagged images
- name: Create manifest
  run: |
    podman manifest create "$IMAGE:latest"
    podman manifest add "$IMAGE:latest" "docker://$IMAGE:arm64"
    podman manifest add "$IMAGE:latest" "docker://$IMAGE:amd64"
    podman manifest push --all "$IMAGE:latest" "docker://$IMAGE:latest"
```

**Pros:** Simple, debuggable (can pull specific arch by tag), works everywhere
**Cons:** Intermediate tags clutter registry, requires cleanup policies

---

## 3. OCI Images as Artifacts

Exports full images as OCI archives. Maximum privacy but highest overhead:

```yaml
# Build job
- name: Save OCI image
  run: podman save ghcr.io/org/app:${{ matrix.arch }} --format=oci-dir -o oci-${{ matrix.arch }}
- uses: actions/upload-artifact@v5
  with:
    name: oci-${{ matrix.arch }}
    path: oci-${{ matrix.arch }}/

# Merge job
- uses: actions/download-artifact@v6
  with:
    path: /tmp/images
- name: Create manifest from OCI
  run: |
    podman manifest create multiarch-manifest
    podman manifest add multiarch-manifest oci:/tmp/images/oci-arm64
    podman manifest add multiarch-manifest oci:/tmp/images/oci-amd64
```

**Pros:** Intermediate builds never touch registry until final push
**Cons:** Consumes GitHub artifact quotas (500MB-50GB), slow tar/untar

---

## 4. Podman Farm (Podman 5.0+)

Distributed builds across multiple remote Podman hosts via SSH:

```bash
# One-time setup
podman system connection add arm64-node ssh://builder@arm64-host
podman system connection add amd64-node ssh://builder@amd64-host
podman farm create build-farm arm64-node amd64-node

# Single command builds on all nodes
podman farm build --farm build-farm -t ghcr.io/user/image:latest .
```

**Pros:** Fastest, automatic manifest creation, single command
**Cons:** Requires persistent infrastructure, not for ephemeral GitHub runners

---

## Debugging Multi-arch Images

### Primary Method: `--platform` Flag

For debugging specific architectures, use the `--platform` flag:

```bash
# Pull specific architecture
podman pull --platform linux/arm64 ghcr.io/OWNER/REPO:latest

# Run with specific architecture
podman run --platform linux/arm64 ghcr.io/OWNER/REPO:latest

# Inspect manifest to see available architectures
podman manifest inspect ghcr.io/OWNER/REPO:latest
```

**Push-by-digest has the same debug experience as architecture tags** when using `--platform`.

### When to Use `@sha256:...` Digest References

The `@sha256:...` syntax is **only needed** in specific situations:

1. **100% immutable reference required** - Security-critical deployments where you need to guarantee the exact image
2. **Registry doesn't support `--platform`** - Older or non-standard registries
3. **Debugging manifest issues** - When `--platform` doesn't work and you need to verify individual architecture images

```bash
# Using @sha256:... (only when needed)
podman pull ghcr.io/OWNER/REPO@sha256:abc123...

# Preferred: Use --platform instead
podman pull --platform linux/arm64 ghcr.io/OWNER/REPO:latest
```

---

## Podman-Specific Pitfalls

### Wrong Push Command for Manifests

**Most frequent error:** Using `podman push` instead of `podman manifest push --all`:

```bash
# WRONG - only pushes native architecture
podman push ghcr.io/org/app:latest

# CORRECT - pushes all architectures in manifest
podman manifest push --all ghcr.io/org/app:latest
```

### Base Image Architecture Confusion

Podman may reuse a previously-downloaded base image of wrong architecture. Always specify `--platform`:

```bash
# Always explicit, even on native runners
podman build --platform linux/arm64 -t myimage .
```

### Registry Format Compatibility

**Podman uses OCI format by default**, which is supported by modern container registries (ghcr.io, Docker Hub, ECR, ACR, GCR).

**When to specify format:**

- **Modern single registry (default)**: Use OCI format (Podman default, no flag needed)
  ```bash
  # ghcr.io, Docker Hub, ECR, ACR, GCR - OCI format (default)
  podman manifest push --all myimage docker://ghcr.io/user/image:tag
  ```

- **Quay.io or cross-registry**: Use v2s2 format for maximum compatibility
  ```bash
  # Quay.io or pushing to multiple different registries
  podman manifest push --all --format v2s2 myimage docker://quay.io/user/image:tag
  ```

- **Avoid v2s1**: Deprecated format, many registries no longer support it

**Build format**: Always use `--format docker` when building to ensure compatibility:
```bash
podman build --format docker -t myimage .
```

**Simple rule**: Single modern registry → OCI (default). Cross-registry or Quay.io → v2s2.

### Tag Command Incompatibility

`podman tag` doesn't work correctly with manifest lists in some versions. Use `buildah tag` or recreate manifests when retagging.

### QEMU Registration Loss

On WSL2 and VM-based environments, multi-arch emulation stops working after restarts:

```bash
# Re-register QEMU handlers
podman run --rm --privileged docker.io/multiarch/qemu-user-static --reset -p yes
```

---

## Native ARM64 Runners (Public Repos Only)

### Why Native Runners?

Using native GitHub-hosted ARM64 runners instead of QEMU provides:

- **10-50x faster builds**: Native compilation vs. emulation
- **Better reliability**: No QEMU compatibility issues
- **Accurate testing**: True ARM64 environment
- **Lower costs**: Faster builds = less runner time

### Runner Configuration

```yaml
strategy:
  matrix:
    include:
      - arch: amd64
        runner: ubuntu-24.04
      - arch: arm64
        runner: ubuntu-24.04-arm  # GitHub-hosted ARM64 runner
runs-on: ${{ matrix.runner }}
```

---

## QEMU Emulation (Private Repos)

### When to Use QEMU

Use QEMU for private repositories on GitHub Free plan:
- Native ARM64 runners require GitHub Team/Enterprise
- QEMU provides ARM64 compatibility without additional costs
- Acceptable tradeoff for private projects with limited CI budgets

### QEMU Setup

```yaml
jobs:
  build-app:
    runs-on: ubuntu-latest  # Single AMD64 runner, not matrix
    steps:
      - uses: actions/checkout@v6

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Build multi-arch image with QEMU
        run: |
          IMAGE="ghcr.io/${{ github.repository_owner }}/app"

          # Single build command for all platforms
          podman build \
            --platform linux/amd64,linux/arm64 \
            --format docker \
            --manifest "$IMAGE:latest" \
            -f ./Containerfile \
            .

          # Push manifest directly
          podman manifest push --all "$IMAGE:latest" "docker://$IMAGE:latest"
```

### Performance Comparison

**Native ARM64 (Public Repos):**
- AMD64 build: ~2-3 minutes
- ARM64 build: ~2-3 minutes (parallel)
- Total: ~3 minutes (parallel execution)

**QEMU (Private Repos):**
- Multi-arch build: ~30-90 minutes
- Total: ~30-90 minutes (sequential emulation)

---

## ARM64 Larger Runners (Private Repos with Team/Enterprise)

### When to Use

For private repositories with GitHub Team or Enterprise Cloud plans that need native ARM64 performance.

**Important:** Standard ARM64 runners (`ubuntu-24.04-arm`) **don't work in private repos**. You must use larger runners instead.

### Setup Steps

**1. Create ARM64 Larger Runner:**
- Go to **Organization Settings → Actions → Runners → New runner**
- Select **"Larger runners"**
- Choose **"Ubuntu 24.04 by Arm Limited"** partner image
- Name your runner (e.g., `my-org-arm64-4core`)
- Configure size:
  - **4-core, 16GB RAM** (recommended for most builds)
  - **8-core, 32GB RAM** (for heavy builds)

**2. Update Workflow:**
```yaml
strategy:
  matrix:
    include:
      - arch: amd64
        runner: ubuntu-24.04
      - arch: arm64
        runner: my-org-arm64-4core  # Your custom runner name (not ubuntu-24.04-arm)
```

### Cost Comparison

| Runner Type | Public Repo | Private Repo (Free) | Private Repo (Team/Enterprise) |
|-------------|-------------|---------------------|--------------------------------|
| **Standard ARM64** | ✅ Free | ❌ Not available | ❌ Not available |
| **ARM64 Larger Runner** | ❌ Not free | ❌ Not available | ✅ Paid per minute (~37% cheaper than x64) |
| **QEMU Emulation** | ✅ Free | ✅ Free | ✅ Free (but slow) |

### Pricing

- Billed per minute of usage
- ~37% cheaper than equivalent x64 larger runners
- Not included in free minutes
- Ref: [Actions runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing)

---

## Podman Installation in GitHub Actions

### Why podman-static?

Ubuntu 24.04's default podman (4.9.3) uses buildah 1.33.7, which doesn't support heredoc syntax in Containerfiles. Use `podman-static` for modern buildah:

```yaml
- name: Install podman-static for heredoc support
  run: |
    echo "=== Installing podman-static v5.6.2 ==="
    # Containerfile uses RUN <<EOT heredoc syntax (requires buildah >= 1.35.0)

    ARCH="${{ matrix.arch }}"
    if [ "$ARCH" = "amd64" ]; then
      PODMAN_ARCH="amd64"
    else
      PODMAN_ARCH="arm64"
    fi

    curl -fsSL -o /tmp/podman-linux-${PODMAN_ARCH}.tar.gz \
      https://github.com/mgoltzsche/podman-static/releases/latest/download/podman-linux-${PODMAN_ARCH}.tar.gz
    cd /tmp && tar -xzf podman-linux-${PODMAN_ARCH}.tar.gz

    # Install to /usr/bin to avoid AppArmor issues
    sudo cp -f podman-linux-${PODMAN_ARCH}/usr/local/bin/* /usr/bin/
    sudo cp -r podman-linux-${PODMAN_ARCH}/etc/* /etc/ 2>/dev/null || true

    podman system migrate
    podman --version
```

**Why install to /usr/bin (not /usr/local/bin)?**
- Avoids AppArmor permission issues on Ubuntu
- Default AppArmor profile only allows `/usr/bin` paths
- Ref: https://github.com/mgoltzsche/podman-static#apparmor-profile

---

## Registry Authentication

### GitHub Container Registry (GHCR)

Use built-in GITHUB_TOKEN for authentication:

```yaml
env:
  REGISTRY: ghcr.io
  IMAGE_OWNER: ${{ github.repository_owner }}

steps:
  - name: Login to registry
    run: |
      echo "${{ secrets.GITHUB_TOKEN }}" | podman login "$REGISTRY" \
        -u "${{ github.actor }}" \
        --password-stdin
```

### Docker Hub Support

```yaml
- name: Login to Docker Hub
  run: |
    echo "${{ secrets.DOCKERHUB_TOKEN }}" | podman login docker.io \
      -u "${{ secrets.DOCKERHUB_USERNAME }}" \
      --password-stdin

# Push to Docker Hub
- name: Push to Docker Hub
  run: |
    podman manifest push --all "$IMAGE:latest" \
      "docker://docker.io/${{ secrets.DOCKERHUB_USERNAME }}/app:latest"
```

**Setup Docker Hub secrets:**
1. Go to **Settings → Secrets and variables → Actions**
2. Add these secrets:
   - `DOCKERHUB_USERNAME`: Your Docker Hub account username
   - `DOCKERHUB_TOKEN`: Personal Access Token from [Docker Hub Security](https://hub.docker.com/settings/security)

---

## Recommended Approach by Use Case

| Use Case | Recommended Approach |
|----------|---------------------|
| **Open source (public repos)** | Push-by-digest with free ARM64 runners |
| **Enterprise (private repos)** | Push-by-digest with Team/Enterprise ARM64 runners |
| **Maximum privacy required** | OCI artifacts (intermediate builds stay private) |
| **Quick setup, minimal complexity** | Architecture tags |
| **Dedicated build infrastructure** | Podman Farm |

---

## Alternative: Docker Buildx Push-by-Digest

For projects that prefer Docker/buildx over Podman, here's the equivalent approach:

```yaml
jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        include:
          - platform: linux/amd64
            runner: ubuntu-latest
          - platform: linux/arm64
            runner: ubuntu-24.04-arm
    runs-on: ${{ matrix.runner }}
    steps:
      - uses: actions/checkout@v6
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        id: build
        with:
          platforms: ${{ matrix.platform }}
          outputs: type=image,push-by-digest=true,name-canonical=true,push=true
          tags: ghcr.io/${{ github.repository }}
      - run: |
          mkdir -p /tmp/digests
          touch "/tmp/digests/${{ steps.build.outputs.digest }}"
      - uses: actions/upload-artifact@v5
        with:
          name: digests-${{ matrix.platform }}
          path: /tmp/digests/*
          retention-days: 1

  merge:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v6
        with:
          path: /tmp/digests
          pattern: digests-*
          merge-multiple: true
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/setup-buildx-action@v3
      - run: |
          docker buildx imagetools create \
            -t ghcr.io/${{ github.repository }}:latest \
            $(cd /tmp/digests && printf 'ghcr.io/${{ github.repository }}@%s ' *)
```

**Note:** This plugin's default workflows use Podman. Docker buildx is provided as an alternative for teams already using Docker tooling.

---

## Cost Optimization

- Use matrix builds to parallelize architecture builds
- Cache build layers when possible
- Only rebuild changed applications (path filters)
- Use workflow concurrency to cancel outdated builds

## Debugging Tips

### View Build Logs

```bash
# Check Podman version
podman --version

# Inspect built image
podman inspect "$IMAGE:$TAG"

# Test image locally
podman run --rm -it "$IMAGE:$TAG"

# View manifest contents
podman manifest inspect "$IMAGE:latest"
```

### Common Issues

1. **Container networking SSL errors (ubuntu-24.04 runners >= 20251208.163.1)**
   - **Symptom**: `UNKNOWN_CERTIFICATE_VERIFICATION_ERROR` or SSL certificate failures during package installation (`bun install`, `npm install`, `pip install`, `cargo build`, etc.) inside containers
   - **Root Cause**: Runner image networking configuration change affecting container bridge networking
   - **Solution**: Add `--network=host` to `podman build`
   - **Evidence**: [Test repository](https://github.com/pigfoot/test-bun-ssl-issue) | [GitHub Issue #13422](https://github.com/actions/runner-images/issues/13422)
   - **Example**:
     ```yaml
     - name: Build image
       run: |
         podman build \
           --network=host \
           --format docker \
           --platform linux/${{ matrix.arch }} \
           -f ./Containerfile \
           .
     ```
   - **Trade-off**: Reduces network isolation during build (acceptable for CI/CD)
   - **Status**: Known issue, workaround required until GitHub resolves runner image networking

2. **Authentication failed**: Ensure GITHUB_TOKEN has package write permission

3. **Manifest add failed**: Verify architecture-specific images exist

4. **Build timeout**: Check for inefficient Containerfile layers

5. **QEMU slow**: Consider native ARM64 runners for public repos
