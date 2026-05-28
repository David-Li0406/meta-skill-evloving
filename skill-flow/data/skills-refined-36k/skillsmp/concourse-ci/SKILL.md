---
name: concourse-ci
description: "Agent Skill: Expert guidance for Concourse CI pipeline development, optimization, and troubleshooting. Covers pipeline creation, resource configuration (git, registry-image, 50+ types), oci-build-task for container builds, across step for multi-env deploys, build_log_retention, YAML anchors, webhook triggers, set_pipeline for dynamic pipelines, and critical gotchas like tag detection after force-push. Targets Concourse v8.0+. By Netresearch."
version: 1.2.0
---

# Concourse CI Pipeline Development

This skill provides expert guidance for writing, refactoring, upgrading, and optimizing Concourse CI pipelines. Concourse is a pipeline-based continuous thing-doer that implements CI/CD workflows as dependency flows.

> **Compatibility**: Concourse v8.0+ (current). Legacy support for v6.5+ where noted.

## Modern vs Legacy Approaches

| Task | Modern (Recommended) | Legacy (Avoid) |
|------|---------------------|----------------|
| Building images | `oci-build-task` + `registry-image` | `docker-image` resource |
| Multi-env deploys | `across` step modifier | Duplicate jobs per env |
| Notifications | Dedicated resources (slack-alert, teams) | Generic HTTP resource |
| Dynamic pipelines | `set_pipeline` + instanced pipelines | Manual pipeline duplication |
| Notification symbols | UTF-8 characters (`✅`, `❌`) | HTML entities (`&#9989;`) |
| Resource styling | Always use `icon:` property | No icon (poor UI/UX) |

## Core Concepts

### Pipeline Architecture

```
Pipeline
├── resources         # External versioned artifacts (git repos, images, buckets)
├── resource_types    # Custom resource type definitions
├── jobs              # Sequences of steps that process resources
│   └── steps         # get, put, task, set_pipeline, in_parallel, do, try
├── groups            # UI organization (optional)
└── var_sources       # Variable sources for credentials
```

### Key Design Principles

1. **Container-Native**: All execution occurs in containers
2. **Self-Contained**: Resource types defined within pipeline config
3. **Idempotent Jobs**: Loosely-coupled design for maintainability
4. **Deterministic Tasks**: Same inputs → same outputs

## Pipeline Creation Workflow

### 1. Define Resources

```yaml
resources:
- name: source-repo
  type: git
  icon: gitlab  # Material Design icon
  check_every: 5m
  source:
    uri: https://github.com/org/repo.git
    branch: main
    username: ((git.username))
    password: ((git.token))

- name: app-image
  type: registry-image
  icon: docker
  source:
    repository: registry.example.com/org/app
    username: ((registry.username))
    password: ((registry.password))
    tag: latest

# Webhook-triggered resource (instant checks instead of polling)
- name: source-webhook
  type: git
  webhook_token: ((webhook.secret))  # Trigger: POST /api/v1/teams/TEAM/pipelines/PIPE/resources/source-webhook/check/webhook?webhook_token=SECRET
  check_every: never  # Disable polling, rely on webhooks
  source:
    uri: https://github.com/org/repo.git
    branch: main
```

### 2. Define Jobs

```yaml
jobs:
- name: build
  serial: true
  plan:
  - get: source-repo
    trigger: true
  - task: compile
    file: source-repo/ci/tasks/compile.yml
  - put: app-image
    params:
      image: build-output/image.tar
```

### 3. Use YAML Anchors for DRY

```yaml
# Define reusable snippets at top
git-source: &git-source
  uri: ((git.uri))
  username: ((git.username))
  password: ((git.password))

notification: &notify-failure
  put: slack
  params:
    text: "Build failed: $BUILD_PIPELINE_NAME/$BUILD_JOB_NAME"

resources:
- name: repo-main
  type: git
  source:
    <<: *git-source
    branch: main

jobs:
- name: test
  plan:
  - get: repo-main
    trigger: true
  - task: run-tests
    file: repo-main/ci/tasks/test.yml
  on_failure:
    <<: *notify-failure
```

## Job Lifecycle Hooks

```yaml
jobs:
- name: deploy
  plan:
  - get: app-image
    trigger: true
    passed: [build]
  - task: deploy
    file: source-repo/ci/tasks/deploy.yml
  on_success:
    put: notify
    params: { text: "Deploy succeeded" }
  on_failure:
    put: notify
    params: { text: "Deploy failed" }
  on_error:
    put: notify
    params: { text: "Deploy errored" }
  on_abort:
    put: notify
    params: { text: "Deploy aborted" }
  ensure:
    task: cleanup
    file: source-repo/ci/tasks/cleanup.yml
```

### Hook Semantics

| Hook | Triggers When | Use Case |
|------|---------------|----------|
| `on_success` | Step/job succeeds | Success notifications, promotions |
| `on_failure` | Step/job fails (non-zero exit) | Alert teams, rollback |
| `on_error` | Infrastructure error (container crash, timeout) | Page on-call, investigate |
| `on_abort` | Build manually aborted or interrupted | Cleanup partial state |
| `ensure` | Always runs regardless of outcome | Release locks, cleanup resources |

**Important**: `on_failure` ≠ `on_error`. A task returning exit code 1 triggers `on_failure`. A container OOM kill or timeout triggers `on_error`. Handle both for robust pipelines.

## Step Types Quick Reference

| Step | Purpose | Example |
|------|---------|---------|
| `get` | Fetch resource version | `get: source-repo` |
| `put` | Update/push resource | `put: app-image` |
| `task` | Execute containerized work | `task: build` |
| `set_pipeline` | Dynamic pipeline config | `set_pipeline: feature-pipeline` |
| `in_parallel` | Concurrent execution | `in_parallel: [step1, step2]` |
| `do` | Sequential steps | `do: [step1, step2]` |
| `try` | Continue on failure | `try: { task: optional }` |
| `load_var` | Runtime variable | `load_var: version` |

## Variable Syntax

```yaml
# Basic variable reference
uri: ((git.uri))

# With field access
password: ((vault:secret/git.password))

# Local scope (from load_var)
tag: ((.version))
```

## Common Patterns

### Build-Test-Release Pipeline

```yaml
jobs:
- name: build
  plan:
  - get: source
    trigger: true
  - task: build
    file: source/ci/tasks/build.yml
  - put: image-rc
    params:
      image: build/image.tar
      tag: release-candidate

- name: test
  plan:
  - get: image-rc
    passed: [build]
    trigger: true
  - get: source
    passed: [build]
  - task: integration-tests
    file: source/ci/tasks/test.yml

- name: release
  plan:
  - get: image-rc
    passed: [test]
    trigger: true
  - get: source
    passed: [test]
  - put: image-release
    params:
      image: image-rc/image.tar
      version: source/version
```

### Parallel Execution

```yaml
- in_parallel:
    limit: 3  # Max concurrent steps
    fail_fast: true
    steps:
    - task: unit-tests
    - task: lint
    - task: security-scan
```

### Multi-Environment with `across` Step

Modern alternative to duplicate resources/jobs per environment:

```yaml
jobs:
- name: deploy
  plan:
  - get: app-image
    trigger: true
  - get: source
  - task: deploy
    across:
    - var: env
      values: [dev, staging, prod]
      max_in_flight: 1  # Sequential deployment
    file: source/ci/tasks/deploy.yml
    params:
      ENVIRONMENT: ((.:env))
      CONFIG_FILE: source/config/((.:env)).yml
```

## Optimization Techniques

1. **Parallel Steps**: Use `in_parallel` for independent operations
2. **Task Caching**: Define `caches` for dependency directories
3. **Resource Filtering**: Use `paths`/`ignore_paths` to limit triggers
4. **Shallow Clones**: Set `depth: 1` for git resources when history not needed
5. **Serial Groups**: Prevent resource contention with `serial_groups`
6. **Build Log Retention**: Configure `build_log_retention` to manage storage
7. **Skip Download**: Use `skip_download: true` for version checks without pulling

## Build Log Retention

Control log storage per job:

```yaml
jobs:
- name: frequent-job
  build_log_retention:
    days: 7                        # Keep logs for 7 days
    builds: 100                    # Keep last 100 builds
    minimum_succeeded_builds: 1    # Always keep at least 1 success
  plan:
  - get: source
    trigger: true
  - task: build
    file: source/ci/tasks/build.yml
```

## Task Reusability with Input/Output Mapping

Map generic task inputs/outputs to specific resources:

```yaml
# Generic task file: ci/tasks/deploy.yml
platform: linux
image_resource:
  type: registry-image
  source: { repository: alpine }
inputs:
- name: app-source    # Generic name
- name: app-image     # Generic name
outputs:
- name: deploy-result
params:
  TARGET_ENV:
run:
  path: /bin/sh
  args: ["-c", "echo Deploying to $TARGET_ENV"]

# Pipeline usage with mapping
jobs:
- name: deploy-staging
  plan:
  - in_parallel:
    - get: my-repo
    - get: staging-image
  - task: deploy
    file: my-repo/ci/tasks/deploy.yml
    input_mapping:
      app-source: my-repo        # Map generic → specific
      app-image: staging-image
    output_mapping:
      deploy-result: staging-result
    params:
      TARGET_ENV: staging
```

## Critical Gotchas

### Git Resource Tag Detection Issue

**Problem**: After force-pushing a branch, Concourse may not detect new tags.

**Root Causes**:
1. Tags pointing to commits no longer reachable from tracked branch
2. Mixed read/write on same git resource creates version conflicts
3. Unescaped regex dots (`.` matches any character)

**Solutions**:

```yaml
# 1. Escape regex dots properly
tag_regex: "^v[0-9]+\\.[0-9]+\\.[0-9]+$"

# 2. Enable tag cleanup
resources:
- name: repo
  type: git
  source:
    uri: ((git.uri))
    branch: main
    tag_regex: "^v[0-9]+\\.[0-9]+\\.[0-9]+$"
    fetch_tags: true
    clean_tags: true

# 3. Separate read-only and write-only resources
- name: repo-read  # For tracking tags
  type: git
  source:
    <<: *git-source
    tag_regex: "^v.*"
    fetch_tags: true
    clean_tags: true

- name: repo-write  # For pushing tags
  type: git
  source:
    <<: *git-source
    fetch_tags: true
```

**Best Practice**: Treat tags as immutable; avoid force-pushing release branches.

## Additional Resources

### Reference Files

For detailed configuration options, consult:
- **`references/pipeline-syntax.md`** - Complete YAML schema for pipelines, jobs, resources
- **`references/resources-guide.md`** - Git-resource, registry-image-resource, docker-image migration
- **`references/best-practices.md`** - Optimization, troubleshooting, notifications, deployment patterns
- **`references/resource-types-catalog.md`** - Available resource types including Ansible, Terraform

### Example Files

Working examples in `examples/`:
- **`basic-pipeline.yml`** - Build-test-deploy pattern with versioning
- **`modern-ci-cd.yml`** - Modern patterns: oci-build-task, across, build_log_retention
- **`multi-branch.yml`** - Dynamic branch pipelines with set_pipeline
- **`docker-build.yml`** - Container image build and push
- **`vars-template.yml`** - Variable file organization pattern

### Validation Script

Use `scripts/validate-pipeline.sh` to check pipeline syntax before deployment.

## fly CLI Quick Reference

```bash
# Set/update pipeline
fly -t target set-pipeline -p pipeline-name -c pipeline.yml -l vars.yml

# Check resource versions
fly -t target check-resource -r pipeline/resource-name

# Trigger job manually
fly -t target trigger-job -j pipeline/job-name -w

# Hijack into container for debugging
fly -t target hijack -j pipeline/job-name -s step-name

# Watch build logs
fly -t target watch -j pipeline/job-name

# Validate pipeline syntax
fly -t target validate-pipeline -c pipeline.yml
```

## Modern Container Image Building

Use `oci-build-task` + `registry-image` (not legacy `docker-image`):

```yaml
- task: build-image
  privileged: true
  config:
    platform: linux
    image_resource:
      type: registry-image
      source: { repository: concourse/oci-build-task }
    inputs: [{ name: source }]
    outputs: [{ name: image }]
    params:
      CONTEXT: source
      DOCKERFILE: source/Dockerfile
    caches: [{ path: cache }]
    run: { path: build }
- put: app-image
  params: { image: image/image.tar }
```

Key parameters: `CONTEXT`, `DOCKERFILE`, `BUILD_ARG_*`, `TARGET`, `IMAGE_PLATFORM`, `OUTPUT_OCI`. See `references/resources-guide.md` for full migration guide from `docker-image`.

## Task Configuration Pattern

Store task configs in repository for version control:

```yaml
# ci/tasks/build.yml
platform: linux
image_resource:
  type: registry-image
  source:
    repository: node
    tag: 20-slim
inputs:
- name: source-repo
outputs:
- name: build-output
caches:
- path: source-repo/node_modules
params:
  NODE_ENV: production
run:
  path: /bin/bash
  args:
  - -exc
  - |
    cd source-repo
    npm ci
    npm run build
    cp -r dist ../build-output/
```

## Pipeline Groups

Organize jobs in the UI without affecting execution:

```yaml
groups:
- name: all
  jobs: ["*"]
- name: build
  jobs: [compile, test]
- name: deploy
  jobs: [deploy-staging, deploy-prod]
- name: infrastructure
  jobs: [terraform-*]  # Glob patterns supported
```

## Pipeline Styling Requirements

### Resource Icons (Required)

**Every resource MUST have an `icon:` property** for better UI/UX in the Concourse dashboard. Use [Material Design icon names](https://pictogrammers.com/library/mdi/).

```yaml
resources:
- name: source
  type: git
  icon: gitlab          # Required - improves dashboard readability

- name: app-image
  type: registry-image
  icon: docker          # Required

- name: notify
  type: http-resource
  icon: message-text    # Required

- name: timer
  type: time
  icon: clock-outline   # Required
```

**Common icon mappings:**

| Resource Type | Recommended Icon |
|---------------|------------------|
| `git` | `gitlab`, `github`, `git` |
| `registry-image` | `docker` |
| `time` | `clock-outline` |
| `http-resource` | `message-text`, `webhook` |
| `slack-alert` | `slack`, `bell` |
| `semver` | `tag` |
| `s3` | `aws`, `bucket` |
| `terraform` | `terraform` |

### Notification Symbols (UTF-8 Preferred)

**Always use UTF-8 characters instead of HTML entities** for notification messages. UTF-8 is more readable in YAML and works across all modern systems.

```yaml
# Modern (Preferred) - UTF-8 characters
notification:
  icon_success: "✅"
  icon_failure: "❌"
  icon_warning: "⚠️"
  icon_info: "ℹ️"
  icon_rocket: "🚀"

# Legacy (Avoid) - HTML entities
notification:
  icon_success: "&#9989;"    # Avoid - hard to read
  icon_failure: "&#128308;"  # Avoid - requires lookup
```

**Rationale:**
- UTF-8 is human-readable in YAML files
- No encoding/decoding issues
- Works in all modern terminals, chat clients, and browsers
- Easier to maintain and review in diffs
