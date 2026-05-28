---
name: github-actions-ci
description: Creates GitHub Actions CI/CD workflows for testing, building, and deploying applications. Supports Nix/devenv builds, container publishing, and multi-environment deployments. Use when setting up CI pipelines, release automation, or deployment workflows.
---

# GitHub Actions CI/CD

## Basic CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - run: go test -race -coverprofile=coverage.out ./...
      - uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - run: go build -o bin/app ./cmd/app
      - uses: actions/upload-artifact@v4
        with:
          name: binary
          path: bin/
```

## CI with Nix/devenv

```yaml
name: CI (Nix)

on:
  push:
    branches: [main]
  pull_request:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: cachix/install-nix-action@v27
      - uses: cachix/cachix-action@v15
        with:
          name: devenv
      - run: nix flake check
      - run: nix develop --command just test
      - run: nix develop --command just build
```

## Container Build & Push

```yaml
name: Container

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha

      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Release Workflow

```yaml
name: Release

on:
  push:
    tags: ['v*']

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: orhun/git-cliff-action@v3
        id: changelog
        with:
          args: --latest --strip header

      - uses: softprops/action-gh-release@v2
        with:
          body: ${{ steps.changelog.outputs.content }}
```

## Deploy Workflow

```yaml
name: Deploy

on:
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [staging, production]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4

      - name: Deploy
        run: |
          echo "Deploying to ${{ inputs.environment }}"
          # Add deployment commands

      - name: Smoke test
        run: curl -f ${{ vars.APP_URL }}/health
```

## Matrix Builds

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        go: ['1.21', '1.22']
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: ${{ matrix.go }}
      - run: go test ./...
```

## Reusable Workflow

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test

on:
  workflow_call:
    inputs:
      go-version:
        type: string
        default: '1.22'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: ${{ inputs.go-version }}
      - run: go test ./...
```

Use it:
```yaml
jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      go-version: '1.22'
```

## Common Patterns

### Concurrency (cancel in-progress)
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Conditional on files changed
```yaml
on:
  push:
    paths:
      - 'src/**'
      - '!**.md'
```

### Environment protection
```yaml
jobs:
  deploy:
    environment:
      name: production
      url: https://example.com
```

### Cache dependencies
```yaml
- uses: actions/cache@v4
  with:
    path: ~/go/pkg/mod
    key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
```

## Required Secrets

| Secret | Purpose |
|--------|---------|
| `GITHUB_TOKEN` | Auto-provided, packages/releases |
| `CODECOV_TOKEN` | Coverage reports |
| `AWS_ACCESS_KEY_ID` | AWS deployments |
| `SLACK_WEBHOOK_URL` | Notifications |
