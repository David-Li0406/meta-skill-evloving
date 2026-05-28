# Concourse CI Resources Configuration Guide

Detailed configuration reference for commonly used Concourse CI resources.

## Git Resource (concourse/git-resource)

Tracks commits in a Git repository branch or by tags.

### Source Configuration

```yaml
resources:
- name: source-repo
  type: git
  source:
    # Required
    uri: https://github.com/org/repo.git  # Repository URL

    # Authentication (choose method)
    # HTTPS with username/password
    username: ((git.username))
    password: ((git.token))

    # SSH with private key
    private_key: ((git.private_key))
    private_key_user: git                 # SSH config User
    private_key_passphrase: ((passphrase)) # If key is encrypted

    # Branch tracking (optional, defaults to repo default branch)
    branch: main

    # Tag tracking (choose one, mutually exclusive with branch for triggers)
    tag_filter: "v*"                      # Bash glob pattern
    tag_regex: "^v[0-9]+\\.[0-9]+\\.[0-9]+$"  # Extended grep regex

    # Path filtering (trigger only on changes to specific files)
    paths:
    - src/**
    - lib/**
    ignore_paths:
    - "*.md"
    - tests/**
    - ci/**

    # Sparse checkout (only fetch specific paths)
    sparse_paths:
    - src
    - lib

    # Tag behavior options
    fetch_tags: true                      # Fetch all tags
    clean_tags: true                      # Delete cached tags before fetch
    tag_behaviour: match_tagged           # or match_tag_ancestors

    # Security
    skip_ssl_verification: false
    commit_verification_keys:             # GPG keys for signature verification
    - |
      -----BEGIN PGP PUBLIC KEY BLOCK-----
      ...
      -----END PGP PUBLIC KEY BLOCK-----

    # Git-crypt support
    git_crypt_key: ((git-crypt-key-base64))

    # Proxy configuration
    https_tunnel:
      proxy_host: proxy.example.com
      proxy_port: 8080
      proxy_user: ((proxy.user))
      proxy_password: ((proxy.pass))

    # Advanced options
    disable_ci_skip: false                # Process [ci skip] commits
    version_depth: 100                    # Versions returned in check
    search_remote_refs: false             # Search remote refs (Gerrit)

    # Commit filtering
    commit_filter:
      exclude:
        - "\\[skip ci\\]"
        - "Merge pull request"
      include:
        - "\\[deploy\\]"

    # Git config
    git_config:
    - name: core.autocrlf
      value: input

    # Submodule credentials
    submodule_credentials:
    - host: github.com
      username: ((github.user))
      password: ((github.token))
```

### Get Parameters

```yaml
- get: source-repo
  params:
    depth: 1                              # Shallow clone depth
    fetch_tags: true                      # Override source setting
    clean_tags: true                      # Delete tags before checkout
    submodules: all                       # none, all, or [list]
    submodule_recursive: true             # Recursive submodule checkout
    submodule_remote: true                # Checkout for remote branch
    disable_git_lfs: false                # Skip LFS files
    all_branches: false                   # Fetch all branches

    # Output formatting
    short_ref_format: "%s"                # Printf format for short_ref
    timestamp_format: iso8601             # Commit timestamp format
    describe_ref_options: "--always --dirty"
```

### Put Parameters

```yaml
- put: source-repo
  params:
    repository: modified-repo             # Required: path to repo

    # Branching
    branch: release                       # Target branch (default: source)
    refs_prefix: refs/heads               # Reference prefix

    # Tagging
    tag: version/tag-file                 # File containing tag name
    tag_prefix: "v"                       # Prepend to tag
    only_tag: true                        # Push only tags, not commits
    annotate: version/annotation-file     # Annotated tag message

    # Push behavior
    force: false                          # Force push
    rebase: false                         # Rebase on conflict
    rebase_strategy: recursive            # ort, octopus, ours, subtree
    rebase_strategy_option: theirs        # -X option
    merge: false                          # Merge on conflict
    returning: merged                     # merged or unmerged (with merge)

    # Notes
    notes: notes/note-file                # Git notes file
```

### Metadata Files (after get)

```
.git/ref              # Full commit SHA
.git/short_ref        # Short SHA (configurable)
.git/commit_message   # Commit message
.git/author           # Author name
.git/author_date      # Author date
.git/committer        # Committer name
.git/committer_date   # Committer date
.git/branch           # Branch name
.git/tags             # Space-separated tags
.git/describe_ref     # Git describe output
.git/metadata.json    # JSON with all metadata
```

---

## Registry Image Resource (concourse/registry-image-resource)

Tracks OCI/Docker images in container registries.

### Source Configuration

```yaml
resources:
- name: app-image
  type: registry-image
  source:
    # Required
    repository: registry.example.com/org/app

    # Tag tracking (choose one mode)
    # 1. Single tag tracking
    tag: latest                           # Default: latest

    # 2. Regex-based tag tracking
    tag_regex: "^[0-9]+\\.[0-9]+\\.[0-9]+$"
    created_at_sort: true                 # Sort by creation time

    # 3. Semver auto-detection (no tag/tag_regex)
    variant: alpine                       # Filter by suffix (1.2.3-alpine)
    semver_constraint: "~1.2.x"           # Semver range
    pre_releases: false                   # Include prereleases
    pre_release_prefixes: [alpha, beta, rc]

    # Authentication
    username: ((registry.username))
    password: ((registry.password))

    # AWS ECR authentication
    aws_access_key_id: ((aws.key_id))
    aws_secret_access_key: ((aws.secret))
    aws_session_token: ((aws.token))
    aws_region: us-east-1
    aws_role_arn: arn:aws:iam::123:role/ecr-role
    aws_role_arns:                        # Role chain
    - arn:aws:iam::123:role/first
    - arn:aws:iam::456:role/second
    aws_account_id: "123456789"           # For ECR

    # Platform selection (multi-arch images)
    platform:
      architecture: amd64                 # amd64, arm64, etc.
      os: linux                           # linux, windows

    # Security
    insecure: false                       # Allow insecure registries
    ca_certs:                             # Custom CA certificates
    - |
      -----BEGIN CERTIFICATE-----
      ...
      -----END CERTIFICATE-----

    # Docker Content Trust
    content_trust:
      server: https://notary.example.com
      repository_key_id: abc123
      repository_key: ((notary.key))
      repository_passphrase: ((notary.pass))
      tls_key: ((tls.key))
      tls_cert: ((tls.cert))

    # Fallback registry
    registry_mirror:
      host: mirror.example.com
      username: ((mirror.user))
      password: ((mirror.pass))

    debug: false
```

### Get Parameters

```yaml
- get: app-image
  params:
    format: rootfs                        # rootfs, oci, oci-layout
    skip_download: false                  # Skip image download (optimization)
    platform:                             # Override source platform
      architecture: arm64
      os: linux
```

### Optimization: skip_download

Use `skip_download: true` when you only need version metadata without the image:

```yaml
# Check if new version exists without downloading
- get: base-image
  params:
    skip_download: true
  trigger: true

# Later, download only when needed
- get: base-image
  passed: [check-job]
  # No skip_download = full download
```

### Put Parameters

```yaml
- put: app-image
  params:
    # Required: image source (choose one)
    image: build-output/image.tar         # OCI tarball
    # OR oci-layout directory

    # Tagging
    version: version/version-file         # Version number as tag
    bump_aliases: true                    # Auto-tag 1.2, 1, latest
    additional_tags: tags/tags-file       # Whitespace-separated tags
    tag_prefix: "v"                       # Prefix for additional_tags
```

### Output Files (after get)

**rootfs format:**
```
rootfs/           # Unpacked filesystem
metadata.json     # Image metadata
labels.json       # Image labels
repository        # Repository name
tag               # Tag name
digest            # Image digest
```

**oci format:**
```
image.tar         # OCI tarball
labels.json
repository
tag
digest
```

---

## Time Resource (concourse/time-resource)

Triggers on time intervals.

```yaml
resources:
- name: every-hour
  type: time
  icon: clock-outline
  source:
    interval: 1h                          # Trigger interval

- name: weekday-morning
  type: time
  source:
    start: 9:00 AM
    stop: 9:30 AM
    location: America/New_York
    days: [Monday, Tuesday, Wednesday, Thursday, Friday]
```

---

## S3 Resource (concourse/s3-resource)

Interacts with S3-compatible storage.

```yaml
resources:
- name: artifacts
  type: s3
  source:
    bucket: my-bucket
    regexp: releases/app-(.*)\.tar\.gz    # Version from filename
    # OR
    versioned_file: releases/app.tar.gz   # S3 versioning

    access_key_id: ((aws.key))
    secret_access_key: ((aws.secret))
    region_name: us-east-1

    # Non-AWS S3-compatible
    endpoint: https://minio.example.com
    disable_ssl: false

    # IAM role (instead of keys)
    use_v2_signing: false
```

---

## Semver Resource (concourse/semver-resource)

Manages semantic versions.

```yaml
resources:
- name: version
  type: semver
  source:
    driver: git                           # git, s3, gcs, swift
    uri: git@github.com:org/version.git
    branch: main
    file: version
    private_key: ((git.private_key))
    initial_version: 0.0.1

# Usage
- get: version
  params:
    bump: minor                           # major, minor, patch
    pre: rc                               # Add prerelease suffix
```

---

## Pool Resource (concourse/pool-resource)

Manages locks and shared state.

```yaml
resources:
- name: env-lock
  type: pool
  source:
    uri: git@github.com:org/locks.git
    branch: main
    pool: environments
    private_key: ((git.private_key))

# Acquire lock
- put: env-lock
  params:
    acquire: true

# Release lock
- put: env-lock
  params:
    release: env-lock
```

---

## Docker Image Resource (concourse/docker-image-resource)

> ⚠️ **LEGACY**: The `docker-image` resource is deprecated. Use `oci-build-task` + `registry-image` for new pipelines.

### Migration Guide: docker-image → oci-build-task

**Before (Legacy docker-image):**
```yaml
resources:
- name: app-image
  type: docker-image
  source:
    repository: registry.example.com/org/app
    username: ((registry.user))
    password: ((registry.pass))

jobs:
- name: build
  plan:
  - get: source
  - put: app-image
    params:
      build: source
      build_args:
        NODE_VERSION: "20"
      docker_buildkit: 1
```

**After (Modern oci-build-task + registry-image):**
```yaml
resources:
- name: app-image
  type: registry-image
  source:
    repository: registry.example.com/org/app
    username: ((registry.user))
    password: ((registry.pass))

jobs:
- name: build
  plan:
  - get: source
  - task: build
    privileged: true
    config:
      platform: linux
      image_resource:
        type: registry-image
        source:
          repository: concourse/oci-build-task
      inputs:
      - name: source
      outputs:
      - name: image
      params:
        CONTEXT: source
        BUILD_ARG_NODE_VERSION: "20"
      caches:
      - path: cache
      run:
        path: build
  - put: app-image
    params:
      image: image/image.tar
```

### Why Migrate?

| Aspect | docker-image | oci-build-task |
|--------|--------------|----------------|
| Maintenance | Deprecated, minimal updates | Actively maintained |
| Security | Requires Docker daemon | Uses BuildKit directly |
| Caching | Basic layer caching | Efficient BuildKit cache |
| Multi-arch | Limited support | Full `IMAGE_PLATFORM` support |
| Complexity | All-in-one (opaque) | Explicit build + push steps |

### Legacy docker-image Reference

If migrating existing pipelines, here's the legacy syntax:

```yaml
resources:
- name: app-image
  type: docker-image
  source:
    repository: registry.example.com/org/app
    username: ((registry.user))
    password: ((registry.pass))
    tag: latest

# Build and push
- put: app-image
  params:
    build: source-repo                    # Dockerfile context
    dockerfile: source-repo/Dockerfile
    tag_file: version/version             # Dynamic tag
    tag_as_latest: true
    build_args:
      BUILD_ARG: value
    cache: true
    cache_tag: cache
    load_base: base-image                 # Pre-loaded base
    docker_buildkit: 1                    # Enable BuildKit
```

### Passing Images Between Jobs (Legacy Pattern)

When using docker-image, pass images between jobs with `save`/`load`:

```yaml
# Job 1: Build and save
- get: app-image
  params:
    save: true  # Save image layers for downstream jobs

# Job 2: Load and use
- get: app-image
  passed: [build]
  params:
    save: true
- put: app-image
  params:
    load: app-image  # Load from previous get
    tag_file: version/tag
```

**Modern alternative**: Use task outputs with `image.tar` artifact.

---

## Slack Notification Resource

Common community resource for Slack notifications.

```yaml
resource_types:
- name: slack-notification
  type: registry-image
  source:
    repository: cfcommunity/slack-notification-resource
    tag: latest

resources:
- name: slack
  type: slack-notification
  source:
    url: ((slack.webhook_url))

# Send notification
- put: slack
  params:
    text: "Build $BUILD_PIPELINE_NAME/$BUILD_JOB_NAME completed"
    channel: "#builds"
    username: Concourse CI
    icon_emoji: ":concourse:"
```

---

## HTTP Resource

For webhook triggers and HTTP interactions.

```yaml
resource_types:
- name: http-resource
  type: registry-image
  source:
    repository: jgriff/http-resource

resources:
- name: webhook
  type: http-resource
  source:
    url: https://api.example.com/webhook
    method: POST
    headers:
      Content-Type: application/json
      Authorization: Bearer ((api.token))
    out_only: true                        # Disable implicit get
    sensitive: true                       # Hide response
    build_metadata: [headers, body]       # Resolve CI vars
```
