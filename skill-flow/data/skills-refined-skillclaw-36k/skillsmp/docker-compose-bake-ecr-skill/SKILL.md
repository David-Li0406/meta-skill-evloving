---
name: docker-compose-bake-ecr-skill
description: Guide development with modern Docker Compose, Docker Bake, and ECR for building and managing container images.
---

# Docker Compose, Bake, and ECR Skill

Use when configuring Docker Compose services, writing Docker Bake files for CI/CD builds, or managing ECR image repositories. Covers modern Compose features, Bake HCL syntax, and ECR caching strategies.

## Docker Compose (Modern Features)

### YAML anchors and aliases

Reduce duplication with anchors (`&name`) and aliases (`*name`). Use `x-` prefix for reusable fragments:

```yaml
# Define reusable fragments with x- prefix (not rendered as services)
x-common-env: &common-env
  LOG_LEVEL: ${LOG_LEVEL:-INFO}
  DEVELOPER_ID: ${USER:-}

x-postgres-depends: &postgres-depends
  postgres:
    condition: service_healthy
    restart: true

x-volumes: &app-volumes
  - type: bind
    source: ./app
    target: /app
  - type: tmpfs
    target: /app/.venv

services:
  api:
    environment:
      <<: *common-env        # Merge anchor into mapping
      API_PORT: 3500         # Add service-specific vars
    volumes: *app-volumes    # Use anchor directly
    depends_on:
      <<: *postgres-depends  # Merge dependency anchor
```

**Merge syntax:**
- `<<: *anchor` merges mapping keys into current mapping
- `<<: [*anchor1, *anchor2]` merges multiple anchors (left-to-right precedence)
- Direct `*anchor` reference for non-mapping values (lists, scalars)

### Service profiles

Group services for selective startup:

```yaml
services:
  postgres:
    profiles: ["infra", "api", "workers"]  # Multiple profiles

  api:
    profiles: ["api"]

  workers:
    profiles: ["workers"]
```

```bash
docker compose --profile infra up -d       # Start infrastructure only
docker compose --profile api up -d         # Start api + its dependencies
docker compose --profile infra --profile api up  # Combine profiles
```

### Service extends

Inherit and override service configurations:

```yaml
services:
  api-base:
    profiles: ["base"]  # Never started directly
    image: api:latest
    build:
      context: ./api
    environment:
      LOG_LEVEL: INFO

  dev-api:
    extends: api-base
    profiles: ["dev"]
    build:
      target: dev-runtime  # Override build target
    environment:
      DEBUG: "true"        # Add to inherited env

  prod-api:
    extends: api-base
    profiles: ["prod"]
    build:
      target: prod-runtime
```

### Health checks

```yaml
services:
  postgres:
    healthcheck:
      test: "pg_isready --username $$POSTGRES_USER --dbname $$POSTGRES_DB"
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s  # Grace period before checks count

  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "-s", "-o", "/dev/null", "http://0.0.0.0:3500/health"]
      interval: 20s
      timeout: 5s
      start_period: 10s
```

**Note:** Use `$$VAR` to escape environment variables in shell-form test commands.

### Dependency conditions

```yaml
services:
  api:
    depends_on:
      postgres:
        condition: service_healthy       # Wait for healthcheck
        restart: true                    # Restart if dependency restarts
      migrations:
        condition: service_completed_successfully  # Wait for exit 0
```

| Condition | Use case |
|-----------|----------|
| `service_started` | Default, just wait for container start |
| `service_healthy` | Wait for healthcheck to pass |
| `service_completed_successfully` | Wait for init container to exit 0 |

### Build configuration

```yaml
services:
  api:
    build:
      context: ./api
      dockerfile: Dockerfile           # Default, can omit
      target: dev-runtime              # Multi-stage target
      additional_contexts:             # Named build contexts
        common: ./common
        lambdas: ./lambdas
      args:
        BUILD_ENV: development
      x-bake:                          # Docker Bake integration
        targets: [api]
        platforms: ["linux/amd64"]
    pull_policy: build                 # Always rebuild locally
```

**additional_contexts** enables `COPY --from=common` in Dockerfile without separate build steps.

### Volume types

```yaml
volumes:
  - type: bind                    # Host path mount
    source: ./app
    target: /app
    read_only: true               # Optional

  - type: volume                  # Named volume
    source: static-files
    target: /static

  - type: tmpfs                   # In-memory filesystem
    target: /app/.venv            # Useful for venvs in dev

volumes:
  static-files:                   # Named volume definition
```

### Network aliases

```yaml
services:
  postgres:
    networks:
      default:
        aliases:
          - postgres.myapp.local   # Additional DNS names
          - db.myapp.local
```

### Environment variable interpolation

```yaml
services:
  api:
    container_name: api${COMPOSE_ID:-}        # Suffix with ID or empty
    ports:
      - "${COMPOSE_ID:-}3500:3500"            # Prefix port
    environment:
      LOG_LEVEL: ${LOG_LEVEL:-INFO}           # Default value
      SECRET: ${SECRET:?required}             # Error if unset
```

## Docker Bake

Docker Bake builds multiple images in parallel with shared configuration. Uses HCL or JSON format.

### Variables

```hcl
variable "REGISTRY" {
  default = "760682031284.dkr.ecr.us-east-1.amazonaws.com"
}

variable "TAG" {
  default = "latest"
}

variable "BRANCH" {
  default = "main"
}

// Nullable variable (no default)
variable "SENTRY_AUTH_TOKEN" {
  default = null
}
```

### Groups

```hcl
group "default" {
  targets = ["api", "workers", "dashboard"]
}

group "backend" {
  targets = ["api", "workers"]
}
```

```bash
docker buildx bake                 # Build default group
docker buildx bake backend         # Build specific group
docker buildx bake api workers     # Build specific targets
```

### Targets

```hcl
// Base target for inheritance
target "base" {
  dockerfile = "Dockerfile"
  target     = "prod-runtime"
  platforms  = ["linux/amd64"]
}

// Inherit and extend
target "base_with_common" {
  inherits = ["base"]
  contexts = {
    common = "./common"
  }
}

target "api" {
  inherits   = ["base_with_common"]
  context    = "./api"
  tags       = ["${REGISTRY}/myapp-api:${TAG}"]
  cache-from = [
    "type=registry,ref=${REGISTRY}/myapp-api:branch-${BRANCH}",
    "type=registry,ref=${REGISTRY}/myapp-api:branch-main"
  ]
  cache-to   = ["type=registry,ref=${REGISTRY}/myapp-api:branch-${BRANCH},mode=max"]
}

target "dashboard" {
  inherits   = ["base"]
  context    = "./dashboard"
  tags       = ["${REGISTRY}/myapp-dashboard:${TAG}"]
  args = {
    VITE_GITHASH      = VITE_GITHASH
    SENTRY_AUTH_TOKEN = SENTRY_AUTH_TOKEN
  }
}
```

### Target attributes

| Attribute | Description |
|-----------|-------------|
| `inherits` | List of targets to inherit from |
| `context` | Build context directory |
| `dockerfile` | Dockerfile path relative to context |
| `target` | Multi-stage build target |
| `platforms` | Target platforms (e.g., `["linux/amd64", "linux/arm64"]`) |
| `tags` | Image tags to apply |
| `args` | Build arguments |
| `contexts` | Named build contexts (maps to `additional_contexts`) |
| `cache-from` | Cache sources |
| `cache-to` | Cache destinations |
| `output` | Output destinations |
| `pull` | Always pull base images |
| `no-cache` | Disable cache |

### Multiple contexts

```hcl
target "lambda" {
  context  = "./lambdas/my_lambda"
  contexts = {
    common         = "./common"
    lambdas_common = "./lambdas"
  }
}
```

In Dockerfile:
```dockerfile
COPY --from=common . /app/common
COPY --from=lambdas_common shared/ /app/shared/
```

### Compose integration

Reference Bake settings in compose.yml:

```yaml
services:
  api:
    build:
      context: ./api
      x-bake:
        targets: [api]
        platforms: ["linux/amd64"]
```

```bash
docker buildx bake --file compose.yml  # Build from compose
```

## ECR (Elastic Container Registry)

### Authentication

```bash
# Configure Docker to authenticate with ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  760682031284.dkr.ecr.us-east-1.amazonaws.com
```

### Tagging strategies

```hcl
// Git-based tags for traceability
tags = [
  "${REGISTRY}/myapp-api:${GIT_SHA}",              // Immutable commit ref
  "${REGISTRY}/myapp-api:branch-${BRANCH}",        // Mutable branch ref
  "${REGISTRY}/myapp-api:${TAG}",                  // Release tag (latest, v1.2.3)
]
```

**Recommended approach:**
- Use git SHA for production deployments (immutable)
- Use branch tags for cache references (mutable)
- Use semver tags for releases

### Cache configuration

Registry-based caching with ECR:

```hcl
target "api" {
  cache-from = [
    // Try current branch cache first
    "type=registry,ref=${REGISTRY}/myapp-api:branch-${BRANCH}",
    // Fall back to main branch cache
    "type=registry,ref=${REGISTRY}/myapp-api:branch-main"
  ]
  cache-to = [
    // Push cache to branch-specific tag
    "type=registry,ref=${REGISTRY}/myapp-api:branch-${BRANCH},mode=max"
  ]
}
```

**Cache modes:**
- `mode=min`: Only cache final stage layers (smaller, faster push)
- `mode=max`: Cache all intermediate stages (better cache hits)

### CI/CD workflow

```yaml
# .github/workflows/docker-build.yml
jobs:
  build:
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::760682031284:role/github-actions
          aws-region: us-east-1

      - uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push
        run: |
          docker buildx bake \
            --set "*.cache-from=type=registry,ref=$REGISTRY/$IMAGE:branch-$BRANCH" \
            --set "*.cache-to=type=registry,ref=$REGISTRY/$IMAGE:branch-$BRANCH,mode=max" \
            --push
```

### ECR lifecycle policies

Configure in ECR console or via Terraform/Pulumi to auto-clean old images:

```json
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Keep last 10 branch images",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": ["branch-"],
        "countType": "imageCountMoreThan",
        "countNumber": 10
      },
      "action": { "type": "expire" }
    },
    {
      "rulePriority": 2,
      "description": "Expire untagged after 7 days",
      "selection": {
        "tagStatus": "untagged",
        "countType": "sinceImagePushed",
        "countUnit": "days",
        "countNumber": 7
      },
      "action": { "type": "expire" }
    }
  ]
}
```

## Dockerfile best practices

### Multi-stage builds

```dockerfile
# syntax=docker/dockerfile:1

FROM base AS builder
# Install build dependencies and compile

FROM base AS dev-builder
# Add dev/test dependencies

FROM base AS runtime
# Minimal runtime setup
COPY --from=builder /app /app

FROM runtime AS prod-runtime
COPY --from=builder /opt/venv /opt/venv

FROM runtime AS dev-runtime
COPY --from=dev-builder /opt/venv /opt/venv
```

### Cache mounts for package managers

```dockerfile
# uv/pip cache
RUN --mount=type=cache,id=uv-cache,sharing=shared,target=/root/.cache/uv \
    uv sync --no-default-groups

# npm cache
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# apt cache
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y package
```

### Copy from named contexts

```dockerfile
# Reference additional_contexts from compose or bake
COPY --from=common . /app/common
COPY --from=lambdas_common shared/ /app/shared/
```

## Debugging checklist

1. **Compose service not starting:** Check `docker compose logs <service>`
2. **Healthcheck failing:** Verify endpoint and use `docker inspect` for health status
3. **Build context too large:** Check `.dockerignore`, use targeted `additional_contexts`
4. **Cache not working:** Verify ECR auth, check `cache-from` refs exist
5. **Anchor not merging:** Ensure `<<:` syntax for mappings, direct `*ref` for lists
6. **Profile not activating:** Use `--profile` flag, check service profile list

## Safeguards

- Do not use `latest` tag for production deployments; use immutable git SHA tags
- Do not disable healthchecks in production configurations
- Validate cache-from references exist before relying on them
- Use `pull_policy: build` in development, not production
- Prefer `type=registry` cache over `type=local` for CI/CD
- Set appropriate ECR lifecycle policies to manage storage costs
