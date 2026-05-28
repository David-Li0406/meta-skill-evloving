# Cloud Run Deployment Paths

Detailed guide to choosing the right deployment approach for Cloud Run.

## Path Comparison

- **No-Build Deploy**: ~10s speed, Low flexibility, No maintenance, ABIU support, No custom packages/multi-stage, Great CI/CD. Best for: Development iterations, simple apps.
- **Buildpacks + ABIU**: ~2-3min speed, Medium flexibility, No maintenance, ABIU support, No custom packages/multi-stage, OK CI/CD. Best for: Most production apps.
- **Source + Dockerfile**: ~2-5min speed, High flexibility, Dockerfile maintenance, Manual updates, Custom packages & multi-stage support, OK CI/CD. Best for: Custom needs.
- **Container Image**: Instant (if image ready), Maximum flexibility, Full pipeline maintenance, Manual updates, Custom packages & multi-stage support, Native CI/CD. Best for: Enterprise CI/CD.

---

## Path 1: No-Build Deploy

### What It Does
Uploads the app (and dependencies) directly to Cloud Run without building a container image. Skips Cloud Build entirely.

### Why It's Powerful
- '10 second'' deploys because there's no container build step
- Gets automatic base image updates for selected base image
- Build your binary in CI, deploy instantly
- Perfect for Go, Rust, Dart that can generated single executable

### Requirements
- gcloud CLI >= 548.0.0
- Dependencies vendored locally (or compiled binary)
- Supported base image
- **Must target `linux/amd64`** — Go/Rust can cross-compile from any OS; some compilers on Windows may not support this

### ⚠️ Limitations
- **No native bindings**: Python/Node.js packages with native extensions (ImageMagick, sharp, bcrypt, native database drivers) won't work. These must be compiled for Linux. Use Buildpacks or Dockerfile instead.
- **Base image only**: Can't install additional OS packages

### Base Images Available
- `go122`, `go123`
- `nodejs20`, `nodejs22`, `nodejs24`
- `python312`, `python313`, `python314`
- `java21`, `java25`
- `dotnet6`, `dotnet8` 
- `ruby33`, `ruby34`
- `php83`, `php84`

`osonly24` is a valid base image for running compiled apps.

### Language-Specific Setup

#### Go (best experience)
```bash
# Cross-compile for Linux (works on Mac, Linux, Windows)
GOOS=linux GOARCH=amd64 go build -o server .

# Deploy
gcloud beta run deploy SERVICE --source . \
  --no-build \
  --base-image go122 \
  --command=./server \
  --automatic-updates \
  --region REGION
```

#### Rust
```bash
# Cross-compile for Linux
cargo build --release --target x86_64-unknown-linux-gnu

# Deploy
gcloud beta run deploy SERVICE --source . \
  --no-build \
  --base-image osonly24 \
  --command=./target/x86_64-unknown-linux-gnu/release/myapp \
  --automatic-updates \
  --region REGION
```

#### Dart
```bash
# Compile to native binary
dart compile exe -target-os=linux --target-arch=arm64 bin/server.dart -o server

# Deploy
gcloud beta run deploy SERVICE --source . \
  --no-build \
  --base-image osonly24 \
  --command=./server \
  --automatic-updates \
  --region REGION
```

#### Python
```bash
# Vendor dependencies
pip3 install -r requirements.txt --target=./vendor

# Deploy
gcloud beta run deploy SERVICE --source . \
  --no-build \
  --base-image python313 \
  --command=python \
  --args=main.py \
  --set-env-vars PYTHONPATH=./vendor \
  --automatic-updates \
  --region REGION
```

#### Node.js
```bash
# Install dependencies
npm install

# Deploy
gcloud beta run deploy SERVICE --source . \
  --no-build \
  --base-image nodejs22 \
  --command=node \
  --args=index.js \
  --automatic-updates \
  --region REGION
```

### CI/CD Integration

No-build works great in CI/CD pipelines:
```bash
# In your CI (GitHub Actions, Cloud Build, etc.):
# Step 1: Build your binary
GOOS=linux GOARCH=amd64 go build -o server .

# Step 2: Deploy instantly (~10s)
gcloud beta run deploy SERVICE --source . --no-build --base-image go122
```

This is often **faster than self-managed Docker builds** for Go/Rust projects.

---

## Path 2: Buildpacks + Automatic Base Image Updates (ABIU)

### What It Does
Automatically detects your stack and builds a container image using Google Cloud Buildpacks. With ABIU, OS and runtime updates are applied automatically.

### Why Use It
- Zero Dockerfile, auto-detected stack
- Security patches without rebuilds or downtime
- Optimized base images from Google
- uilt-in scanning, SLSA attestations

### Command
```bash
gcloud run deploy SERVICE --source . \
  --base-image python313 \
  --automatic-updates \
  --region REGION
```

### Trade-off
- Requires Cloud Build (~2-3 min deploy time)
- Less control than Dockerfile

### How It Works
1. Cloud Run detects your language/framework
2. Applies appropriate buildpack
3. Builds optimized container image
4. With ABIU: Automatically patches base image for security updates

### Supported Stacks
Auto-detected based on:
- `requirements.txt`, `Pipfile`, `pyproject.toml` → Python
- `package.json` → Node.js
- `go.mod` → Go
- `pom.xml`, `build.gradle` → Java
- `*.csproj` → .NET
- `Gemfile` → Ruby
- `composer.json` → PHP

### When to Use
- ✅ Production services with standard stacks
- ✅ Want simplest path with automatic security
- ✅ Don't want to maintain a Dockerfile
- ❌ Need custom OS packages
- ❌ Need fastest possible deploys (use no-build)

---

## Path 3: Source Deploy with Dockerfile

### What It Does
You provide a Dockerfile, Cloud Build runs it in the cloud, and deploys the result.

### Command
```bash
# Just needs a Dockerfile in the source directory
gcloud run deploy SERVICE --source . \
  --region REGION
```

### Sample Dockerfile
```dockerfile
# Multi-stage build for smaller image
FROM python:3.13-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY . .
CMD ["python", "main.py"]
```

### When to Use
- ✅ Need custom OS packages (apt-get)
- ✅ Multi-stage builds for optimization
- ✅ Non-standard build processes
- ✅ Want cloud-based builds without managing infra
- ❌ Full control over build pipeline

---

## Path 4: Deploy Container Image

### What It Does
Deploy any OCI-compliant container image directly to Cloud Run. This is a **first-class deployment path** — Cloud Run is fundamentally a container runtime.

### Why Use It
- **Enterprise CI/CD** — Integrates with existing Docker-based pipelines
- **Multi-target deployment** — Same image to Cloud Run, GKE, on-prem
- **Full control** — Custom base images, OS packages, build optimizations
- **Compliance** — SBOM generation, vulnerability scanning, attestations
- **Mature tooling** — Works with Cloud Build, GitHub Actions, Jenkins, etc.

> **Note**: For Go/Rust projects, consider **No-Build Deploy** — build the binary in CI, then deploy with `--no-build` for even faster deploys without Docker.

### Commands
```bash
# Deploy any container image
gcloud run deploy SERVICE \
  --image REGION-docker.pkg.dev/PROJECT/REPO/IMAGE:TAG \
  --region REGION
```

### CI/CD Integration Examples

#### GitHub Actions
```yaml
- name: Build and Push
  run: |
    docker build -t $REGION-docker.pkg.dev/$PROJECT/repo/image:$GITHUB_SHA .
    docker push $REGION-docker.pkg.dev/$PROJECT/repo/image:$GITHUB_SHA

- name: Deploy to Cloud Run
  run: |
    gcloud run deploy service \
      --image $REGION-docker.pkg.dev/$PROJECT/repo/image:$GITHUB_SHA
```

#### Cloud Build
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', '$_REGION-docker.pkg.dev/$PROJECT_ID/repo/image:$COMMIT_SHA', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', '$_REGION-docker.pkg.dev/$PROJECT_ID/repo/image:$COMMIT_SHA']
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    args: ['run', 'deploy', 'service', '--image', '$_REGION-docker.pkg.dev/$PROJECT_ID/repo/image:$COMMIT_SHA']
```

### When to Use
- ✅ Existing CI/CD pipelines
- ✅ Need SBOM generation, attestations
- ✅ Deploy same image to multiple targets
- ✅ Compliance requirements
- ✅ Custom scanning/validation steps

---

## Decision Logic

- If "Just trying things out" → No-Build
- If "Standard stack + Easy security" → Buildpacks + ABIU
- If "Custom OS packages + Cloud Build" → Source + Dockerfile
- If "Enterprise CI/CD or Compliance" → Container Image
