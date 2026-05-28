---
name: buildkite
description: Buildkite CI/CD pipeline configuration, API integration, and workflow automation. Use when creating or modifying Buildkite pipelines (pipeline.yml), interacting with Buildkite REST/GraphQL APIs, configuring agents, managing artifacts, implementing caching strategies, or automating CI/CD workflows. Covers step types, conditional execution, parallelism, plugins, and monorepo patterns.
---

# Buildkite CI/CD

## Pipeline Configuration (pipeline.yml)

### Step Types

```yaml
env:
  CI: "true"

agents:
  queue: "default"

steps:
  # Command step
  - label: ":hammer: Build"
    key: "build"
    commands:
      - "npm install"
      - "npm run build"
    artifact_paths: "dist/**/*"
    timeout_in_minutes: 30

  # Wait step - sync point
  - wait: ~

  # Block step - manual gate
  - block: ":rocket: Deploy?"
    if: build.branch == "main"
    fields:
      - select: "Environment"
        key: "env"
        options:
          - { label: "Staging", value: "staging" }
          - { label: "Production", value: "prod" }

  # Input step - collect data without blocking
  - input: "Version"
    key: "version-input"
    fields:
      - text: "Version"
        key: "version"
        required: true

  # Trigger step - trigger another pipeline
  - trigger: "deploy-pipeline"
    build:
      branch: "${BUILDKITE_BRANCH}"
      env:
        VERSION: "${VERSION}"

  # Group step - organize steps
  - group: ":test_tube: Tests"
    steps:
      - label: "Unit"
        command: "npm test"
      - label: "Integration"
        command: "npm run test:integration"
```

### Conditional Execution

```yaml
steps:
  # Branch conditions
  - label: "Deploy"
    command: "deploy.sh"
    if: build.branch == "main"

  # Message patterns
  - label: "Skip Deploy"
    command: "echo skipped"
    if: build.message !~ /\[skip-deploy\]/

  # Multiple conditions
  - label: "Release"
    command: "release.sh"
    if: build.branch == "main" && build.tag != null

  # File change conditions (agent-evaluated)
  - label: "API Tests"
    command: "npm run test:api"
    if_changed:
      include: ["packages/api/**"]
      exclude: ["**/*.md"]
```

### Dependencies

```yaml
steps:
  - label: "Build"
    key: "build"
    command: "npm run build"

  - label: "Test"
    depends_on: "build"
    command: "npm test"

  - label: "Deploy"
    depends_on:
      - "build"
      - "test"
    allow_dependency_failure: false
    command: "deploy.sh"
```

### Parallelism and Concurrency

```yaml
steps:
  # Parallel jobs (sharding)
  - label: "Test %n"
    command: |
      SHARD=$((BUILDKITE_PARALLEL_JOB + 1))
      npm test -- --shard=${SHARD}/${BUILDKITE_PARALLEL_JOB_COUNT}
    parallelism: 4

  # Concurrency control (limit simultaneous runs)
  - label: "Deploy"
    command: "deploy.sh"
    concurrency: 1
    concurrency_group: "prod-deploy"
    concurrency_method: "eager"  # or "ordered"
```

### Matrix Builds

```yaml
steps:
  - label: "Node {{matrix.node}} / {{matrix.os}}"
    command: "npm test"
    matrix:
      setup:
        node: ["18", "20", "22"]
        os: ["linux", "darwin"]
      adjustments:
        - with: { node: "18", os: "darwin" }
          soft_fail: true
        - with: { node: "22", os: "darwin" }
          skip: true
```

### Retry Strategies

```yaml
steps:
  - label: "Flaky Test"
    command: "npm test"
    retry:
      automatic:
        - exit_status: -1     # Agent lost
          limit: 2
        - exit_status: 255    # Timeout
          limit: 1
        - exit_status: "*"    # Any failure
          limit: 2
      manual:
        allowed: true
        permit_on_passed: false

  # Soft fail - don't block pipeline
  - label: "Optional Check"
    command: "lint.sh"
    soft_fail:
      - exit_status: 1
```

### Dynamic Pipelines

Upload pipeline steps dynamically:

```yaml
steps:
  - label: ":pipeline: Generate"
    command: |
      cat <<EOF | buildkite-agent pipeline upload
      steps:
        - label: "Dynamic Step"
          command: "echo generated"
      EOF
```

Or from a script:

```bash
#!/bin/bash
# generate-pipeline.sh
PACKAGES=$(find packages -name package.json -exec dirname {} \;)

echo "steps:"
for pkg in $PACKAGES; do
  name=$(basename $pkg)
  echo "  - label: ':package: Test $name'"
  echo "    command: 'cd $pkg && npm test'"
done
```

```yaml
steps:
  - label: ":pipeline: Upload"
    command: "./generate-pipeline.sh | buildkite-agent pipeline upload"
```

## Artifacts

```yaml
steps:
  - label: "Build"
    command: "npm run build"
    artifact_paths:
      - "dist/**/*"
      - "coverage/**/*"
      - "!dist/**/*.map"  # Exclude source maps

  - wait: ~

  - label: "Deploy"
    command: |
      buildkite-agent artifact download "dist/**/*" .
      deploy.sh
```

CLI commands:

```bash
# Upload
buildkite-agent artifact upload "dist/**/*"
buildkite-agent artifact upload "report.html" --job $BUILDKITE_JOB_ID

# Download
buildkite-agent artifact download "dist/**/*" ./output
buildkite-agent artifact download "*" . --step "build"

# Search
buildkite-agent artifact search "*.tar.gz"
```

## Caching

### Cache Plugin (S3 backend)

```yaml
env:
  BUILDKITE_PLUGIN_S3_CACHE_BUCKET: "my-cache-bucket"

steps:
  - label: "Build"
    command: "npm ci && npm run build"
    plugins:
      - cache#v1.8.0:
          manifest: package-lock.json
          path: node_modules
          backend: s3
          compression: zstd

      # Multiple caches
      - cache#v1.8.0:
          key: "turbo-{{ checksum 'turbo.json' }}-{{ .Branch }}"
          restore-keys:
            - "turbo-{{ checksum 'turbo.json' }}-"
            - "turbo-"
          path: .turbo/cache
          backend: s3
```

### Cache Key Interpolation

| Template | Description |
|----------|-------------|
| `{{ checksum 'file' }}` | SHA256 of file |
| `{{ .Branch }}` | Branch name |
| `{{ .Commit }}` | Full commit SHA |
| `{{ .BuildNumber }}` | Build number |
| `{{ arch }}` | CPU architecture |

## Plugins

### Docker Plugin

```yaml
steps:
  - command: "npm test"
    plugins:
      - docker#v5.13.0:
          image: "node:20"
          workdir: /app
          environment:
            - NODE_ENV=test
            - CI
          volumes:
            - "./:/app"
          mount-checkout: true
          propagate-uid-gid: true
          propagate-aws-auth-tokens: true
```

### Docker Compose Plugin

```yaml
steps:
  - command: "npm test"
    plugins:
      - docker-compose#v5.8.0:
          run: app
          config: docker-compose.ci.yml
          env:
            - CI=true
```

### ECR Plugin

```yaml
steps:
  - command: "./build.sh"
    plugins:
      - ecr#v2.10.0:
          credential-helper: true
          account-ids: ["123456789012"]
          region: "us-east-1"
```

### Artifacts Plugin

```yaml
steps:
  - label: "Download and Run"
    plugins:
      - artifacts#v1.9.4:
          download:
            - from: "dist.tar.gz"
              to: "/tmp/dist.tar.gz"
              step: "build"
          upload:
            - from: "results/**/*"
```

## Annotations

```bash
# Add annotation
buildkite-agent annotate "Build complete!" --style success --context deploy

# Styles: success, info, warning, error
buildkite-agent annotate "<details><summary>Logs</summary>...</details>" --style info

# Append to existing
buildkite-agent annotate "More info" --context deploy --append

# Markdown supported
buildkite-agent annotate "## Results\n| Test | Status |\n|------|--------|\n| Unit | ✅ |" --style info
```

## Metadata

```bash
# Set metadata
buildkite-agent meta-data set "version" "1.2.3"
buildkite-agent meta-data set "deploy-url" "https://app.example.com"

# Get metadata
VERSION=$(buildkite-agent meta-data get "version")
buildkite-agent meta-data get "version" --default "0.0.0"

# Check existence
buildkite-agent meta-data exists "version" && echo "exists"

# List keys
buildkite-agent meta-data keys
```

## Environment Variables

### Built-in Variables

| Variable | Description |
|----------|-------------|
| `BUILDKITE_BUILD_ID` | UUID of build |
| `BUILDKITE_BUILD_NUMBER` | Sequential build number |
| `BUILDKITE_BRANCH` | Branch name |
| `BUILDKITE_COMMIT` | Commit SHA |
| `BUILDKITE_TAG` | Git tag (if tagged) |
| `BUILDKITE_MESSAGE` | Commit message |
| `BUILDKITE_PIPELINE_SLUG` | Pipeline slug |
| `BUILDKITE_STEP_KEY` | Step key |
| `BUILDKITE_JOB_ID` | Current job ID |
| `BUILDKITE_PARALLEL_JOB` | Parallel job index (0-based) |
| `BUILDKITE_PARALLEL_JOB_COUNT` | Total parallel jobs |
| `BUILDKITE_ARTIFACT_PATHS` | Artifact upload paths |

### Pipeline-level Env

```yaml
env:
  NODE_ENV: "test"
  DOCKER_BUILDKIT: "1"

steps:
  - label: "Build"
    env:
      DEBUG: "true"  # Step-level override
    command: "npm run build"
```

## Agent Configuration

### Agent Targeting

```yaml
steps:
  - label: "Build"
    agents:
      queue: "default"

  - label: "GPU Test"
    agents:
      queue: "gpu"
      gpu: "true"

  - label: "macOS Build"
    agents:
      os: "darwin"
      xcode: "15"
```

### Agent Hooks

Located in `/etc/buildkite-agent/hooks/`:

```bash
# hooks/environment - set env vars
#!/bin/bash
export NPM_TOKEN=$(aws secretsmanager get-secret-value --secret-id npm-token --query SecretString --output text)

# hooks/pre-command - before each command
#!/bin/bash
echo "--- Setting up environment"

# hooks/post-command - after each command
#!/bin/bash
echo "--- Cleanup"

# hooks/pre-checkout - before git checkout
# hooks/post-checkout - after git checkout
# hooks/pre-exit - before job exits
```

## API Reference

For REST API endpoints, GraphQL queries, authentication, and rate limits, see [API.md](references/API.md).

## Complete Example

```yaml
# .buildkite/pipeline.yml
env:
  CI: "true"
  DOCKER_BUILDKIT: "1"

agents:
  queue: "default"

steps:
  - label: ":npm: Install"
    key: "install"
    command: "npm ci"
    plugins:
      - cache#v1.8.0:
          manifest: package-lock.json
          path: node_modules
          backend: s3

  - wait: ~

  - group: ":white_check_mark: Checks"
    steps:
      - label: ":eslint: Lint"
        command: "npm run lint"
        depends_on: "install"

      - label: ":typescript: Types"
        command: "npm run typecheck"
        depends_on: "install"

  - label: ":hammer: Build"
    key: "build"
    command: "npm run build"
    depends_on: "install"
    artifact_paths: "dist/**/*"

  - wait: ~

  - label: ":test_tube: Test %n"
    key: "test"
    parallelism: 4
    command: |
      SHARD=$((BUILDKITE_PARALLEL_JOB + 1))
      npm test -- --shard=${SHARD}/${BUILDKITE_PARALLEL_JOB_COUNT}
    depends_on: "build"
    artifact_paths: "test-results/**/*"
    retry:
      automatic:
        - exit_status: -1
          limit: 2

  - wait: ~
    continue_on_failure: true

  - label: ":junit: Annotate"
    plugins:
      - junit-annotate#v2.7.0:
          artifacts: "test-results/**/*.xml"

  - block: ":rocket: Deploy?"
    if: build.branch == "main"

  - label: ":shipit: Deploy"
    command: "./deploy.sh"
    if: build.branch == "main"
    concurrency: 1
    concurrency_group: "production"
```
