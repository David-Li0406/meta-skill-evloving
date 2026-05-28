# GitLab CI/CD Pipeline Optimization Guide

Best practices for optimizing GitLab CI/CD pipeline performance, reducing build times, and efficient resource usage.

## Overview

Efficient CI/CD pipelines are critical for developer productivity and cost management. This guide covers caching strategies, job parallelization, Docker optimization, and resource management.

## Caching Strategies

Caching reduces redundant work by preserving dependencies and build artifacts between pipeline runs.

### Basic Cache Configuration

```yaml
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .cache/pip
    - venv/
```

### Cache Key Strategies

**Per-branch caching** (isolates changes):

```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
```

**Shared cache** (faster but may have stale data):

```yaml
cache:
  key: shared-cache
  paths:
    - node_modules/
```

**Dependency-based cache** (invalidates when dependencies change):

```yaml
cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
```

### Pull-Push Policy

Optimize cache usage with pull-push policies:

```yaml
# Default: pull-push (download and upload)
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
  policy: pull-push

# Build job: pull-push (downloads and uploads)
build:
  cache:
    policy: pull-push

# Test job: pull (only downloads, faster)
test:
  cache:
    policy: pull
```

### Python Caching Example

```yaml
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  UV_CACHE_DIR: "$CI_PROJECT_DIR/.cache/uv"

cache:
  key:
    files:
      - pyproject.toml
      - uv.lock
  paths:
    - .cache/pip
    - .cache/uv
    - .venv/

install:
  script:
    - uv venv
    - uv sync --frozen
  cache:
    policy: pull-push

test:
  script:
    - uv run pytest
  cache:
    policy: pull
```

### Node.js Caching Example

```yaml
cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
    - .npm/

install:
  script:
    - npm ci --cache .npm --prefer-offline
  cache:
    policy: pull-push

test:
  script:
    - npm test
  cache:
    policy: pull
```

## Job Parallelization

Run independent jobs concurrently to reduce total pipeline time.

### Parallel Keyword

Run the same job multiple times in parallel:

```yaml
test:
  parallel: 5
  script:
    - npm test -- --shard=$CI_NODE_INDEX/$CI_NODE_TOTAL
```

### Matrix Builds

Test against multiple versions or configurations:

```yaml
test:
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.11", "3.12", "3.13"]
  image: python:${PYTHON_VERSION}
  script:
    - uv run pytest
```

### Stage Parallelization

Run independent jobs in the same stage:

```yaml
stages:
  - test

lint:ruff:
  stage: test
  script:
    - uv run ruff check

lint:mypy:
  stage: test
  script:
    - uv run mypy .

test:unit:
  stage: test
  script:
    - uv run pytest tests/unit

test:integration:
  stage: test
  script:
    - uv run pytest tests/integration
```

All four jobs run concurrently in the `test` stage.

## Docker Optimization

### Use Specific Image Tags

Avoid `latest` tags for reproducibility:

```yaml
# ❌ Avoid
image: python:latest

# ✅ Use specific version
image: python:3.12-slim
```

### Smaller Base Images

Use slim or alpine variants:

```yaml
# Standard image: ~900MB
image: python:3.12

# Slim image: ~120MB
image: python:3.12-slim

# Alpine image: ~50MB (may have compatibility issues)
image: python:3.12-alpine
```

### Multi-Stage Dockerfile

Build smaller production images:

```dockerfile
# Build stage
FROM python:3.12 AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv venv && uv sync --frozen

# Production stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv
COPY . .
CMD [".venv/bin/python", "app.py"]
```

### Docker Layer Caching

Enable Docker layer caching in GitLab:

```yaml
build:
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_DRIVER: overlay2
    DOCKER_BUILDKIT: 1
  script:
    - docker build --cache-from $CI_REGISTRY_IMAGE:latest --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
  cache:
    key: docker-layers
    paths:
      - .docker-cache/
```

### Docker-in-Docker Optimization

```yaml
variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

build:
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

## Job Dependencies and Needs

Control job execution order and parallelization:

### Default: Sequential Stages

```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - npm run build

test:
  stage: test
  script:
    - npm test

deploy:
  stage: deploy
  script:
    - npm run deploy
```

All `build` jobs complete before any `test` jobs start.

### Needs: Directed Acyclic Graph (DAG)

Run jobs as soon as dependencies complete:

```yaml
stages:
  - build
  - test
  - deploy

build:backend:
  stage: build
  script:
    - npm run build:backend

build:frontend:
  stage: build
  script:
    - npm run build:frontend

test:backend:
  stage: test
  needs: [build:backend]
  script:
    - npm test:backend

test:frontend:
  stage: test
  needs: [build:frontend]
  script:
    - npm test:frontend

deploy:
  stage: deploy
  needs: [test:backend, test:frontend]
  script:
    - npm run deploy
```

`test:backend` starts as soon as `build:backend` completes, without waiting for `build:frontend`.

## Artifact Management

### Selective Artifact Paths

Only preserve necessary files:

```yaml
build:
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
      - build/
    exclude:
      - dist/**/*.map
      - build/**/*.log
```

### Artifact Expiration

Set appropriate expiration to save storage:

```yaml
test:
  script:
    - npm test
  artifacts:
    paths:
      - coverage/
    expire_in: 7 days
```

### Artifact Dependencies

Only download required artifacts:

```yaml
build:
  script:
    - npm run build
  artifacts:
    paths:
      - dist/

deploy:
  dependencies:
    - build
  script:
    - npm run deploy
```

`deploy` only downloads artifacts from `build`, not other jobs.

## Conditional Job Execution

Run jobs only when necessary:

### Rules

```yaml
test:
  script:
    - npm test
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy:
  script:
    - npm run deploy
  rules:
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

### Only/Except (Legacy)

```yaml
test:
  script:
    - npm test
  only:
    - merge_requests
    - main

deploy:
  script:
    - npm run deploy
  only:
    - tags
    - main
  except:
    - schedules
```

### Changes

Run jobs only when specific files change:

```yaml
build:frontend:
  script:
    - npm run build:frontend
  rules:
    - changes:
        - frontend/**/*
        - package.json

build:backend:
  script:
    - npm run build:backend
  rules:
    - changes:
        - backend/**/*
        - pyproject.toml
```

## Resource Management

### Job Timeout

Prevent hanging jobs:

```yaml
test:
  script:
    - npm test
  timeout: 1h
```

### Retry Failed Jobs

```yaml
test:
  script:
    - npm test
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
```

### Runner Tags

Use specific runners for resource-intensive jobs:

```yaml
build:
  tags:
    - docker
    - high-cpu
  script:
    - npm run build

test:
  tags:
    - docker
  script:
    - npm test
```

## Environment Variables

### Project Variables

Store configuration in GitLab CI/CD settings (Settings → CI/CD → Variables):

- `DATABASE_URL`
- `API_KEY`
- `DEPLOYMENT_TOKEN`

Mark sensitive variables as **Masked** and **Protected**.

### Variable Precedence

1. Trigger variables (highest priority)
2. Project-level variables
3. Group-level variables
4. Instance-level variables
5. Variables defined in `.gitlab-ci.yml`
6. Predefined variables (lowest priority)

### Masked Variables

Prevent secrets from appearing in logs:

```yaml
variables:
  DATABASE_URL: $DATABASE_URL # Masked in GitLab settings

deploy:
  script:
    - echo "Deploying to $DATABASE_URL" # Will show [MASKED]
```

## Pipeline Efficiency Metrics

Monitor and optimize based on metrics:

### Key Metrics

- **Pipeline duration**: Total time from start to finish
- **Job duration**: Time for individual jobs
- **Queue time**: Time waiting for available runners
- **Cache hit rate**: Percentage of cache hits vs misses
- **Artifact size**: Size of stored artifacts

### Monitoring

```yaml
test:
  script:
    - start_time=$(date +%s)
    - npm test
    - end_time=$(date +%s)
    - echo "Test duration: $((end_time - start_time)) seconds"
```

## Complete Example: Optimized Pipeline

```yaml
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  UV_CACHE_DIR: "$CI_PROJECT_DIR/.cache/uv"

stages:
  - lint
  - test
  - build
  - deploy

cache:
  key:
    files:
      - pyproject.toml
      - uv.lock
  paths:
    - .cache/pip
    - .cache/uv
    - .venv/

.python_base:
  image: python:3.12-slim
  before_script:
    - pip install uv
    - uv venv
    - uv sync --frozen

lint:ruff:
  extends: .python_base
  stage: lint
  script:
    - uv run ruff check
  cache:
    policy: pull

lint:mypy:
  extends: .python_base
  stage: lint
  script:
    - uv run mypy .
  cache:
    policy: pull

test:
  extends: .python_base
  stage: test
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.11", "3.12"]
  image: python:${PYTHON_VERSION}-slim
  script:
    - uv run pytest --cov
  artifacts:
    paths:
      - htmlcov/
    expire_in: 7 days
  cache:
    policy: pull

build:
  extends: .python_base
  stage: build
  needs: [test]
  script:
    - uv build
  artifacts:
    paths:
      - dist/
    expire_in: 30 days
  rules:
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy:
  stage: deploy
  needs: [build]
  dependencies:
    - build
  script:
    - uv publish --token $PYPI_TOKEN
  rules:
    - if: $CI_COMMIT_TAG
  environment:
    name: production
```

## Best Practices Summary

1. **Use caching effectively** - Cache dependencies with appropriate keys
2. **Parallelize jobs** - Run independent jobs concurrently
3. **Optimize Docker images** - Use slim base images and layer caching
4. **Use job dependencies** - Use `needs` for DAG execution
5. **Manage artifacts** - Set expiration and selective paths
6. **Conditional execution** - Use `rules` to run only necessary jobs
7. **Set timeouts** - Prevent hanging jobs
8. **Monitor metrics** - Track duration, cache hits, artifact size
9. **Use runner tags** - Direct jobs to appropriate runners
10. **Secure variables** - Mask sensitive data and use protected variables
