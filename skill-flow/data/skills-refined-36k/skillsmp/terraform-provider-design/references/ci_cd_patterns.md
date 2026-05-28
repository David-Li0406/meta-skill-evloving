# CI/CD and Automation Patterns for Terraform Providers

## Code Quality Tools

### golangci-lint

Install and configure:

```bash
# Install
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Run linter
golangci-lint run

# Auto-fix issues
golangci-lint run --fix
```

Configuration (`.golangci.yml`):

```yaml
linters:
  enable:
    - gofmt
    - govet
    - errcheck
    - staticcheck
    - gosimple
    - ineffassign
    - unused

run:
  timeout: 5m
  tests: true

issues:
  exclude-use-default: false
```

### Code Formatting

```bash
# Format Go code
go fmt ./...

# Format Terraform examples
terraform fmt -recursive examples/

# Format all at once
make fmt
```

## Release Automation

### GoReleaser Configuration

Complete `.goreleaser.yml`:

```yaml
version: 2

before:
  hooks:
    - go mod tidy
    - go generate ./...

builds:
  - id: terraform-provider
    main: .
    binary: '{{ .ProjectName }}_v{{ .Version }}'
    env:
      - CGO_ENABLED=0
    mod_timestamp: '{{ .CommitTimestamp }}'
    flags:
      - -trimpath
    ldflags:
      - '-s -w -X main.version={{.Version}} -X main.commit={{.Commit}}'
    goos:
      - linux
      - windows
      - darwin
    goarch:
      - amd64
      - arm64
      - arm
    ignore:
      - goos: darwin
        goarch: arm
      - goos: windows
        goarch: arm

archives:
  - format: zip
    name_template: '{{ .ProjectName }}_{{ .Version }}_{{ .Os }}_{{ .Arch }}'

checksum:
  name_template: '{{ .ProjectName }}_{{ .Version }}_SHA256SUMS'
  algorithm: sha256

signs:
  - artifacts: checksum
    args:
      - "--batch"
      - "--local-user"
      - "{{ .Env.GPG_FINGERPRINT }}"
      - "--output"
      - "${signature}"
      - "--detach-sign"
      - "${artifact}"

release:
  draft: false
  prerelease: auto

changelog:
  sort: asc
  use: github
  filters:
    exclude:
      - '^docs:'
      - '^test:'
      - '^chore:'
      - Merge pull request
      - Merge remote-tracking branch
  groups:
    - title: 'Breaking Changes'
      regexp: "^.*BREAKING CHANGE.*$"
      order: 0
    - title: 'New Features'
      regexp: "^.*feat[(\\w)]*:.*$"
      order: 1
    - title: 'Bug Fixes'
      regexp: "^.*fix[(\\w)]*:.*$"
      order: 2
    - title: 'Improvements'
      regexp: "^.*improve[(\\w)]*:.*$"
      order: 3
```

### Release Process

```bash
# Tag new version
git tag v1.0.0

# Push tag to trigger release
git push origin v1.0.0

# Or use GoReleaser locally
goreleaser release --clean
```

## Pre-commit Hooks

### Installation

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install
```

### Configuration

`.pre-commit-config.yaml`:

```yaml
repos:
  # Terraform formatting
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.83.0
    hooks:
      - id: terraform_fmt
      - id: terraform_docs
        args:
          - --hook-config=--path-to-file=README.md
          - --hook-config=--add-to-existing-file=true
      - id: terraform_validate

  # Go formatting and linting
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
      - id: go-vet
      - id: go-mod-tidy

  # General checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
```

## Documentation Generation

### tfplugindocs

Automatic documentation generation:

```bash
# Install
go install github.com/hashicorp/terraform-plugin-docs/cmd/tfplugindocs@latest

# Generate docs
tfplugindocs generate

# Validate docs
tfplugindocs validate

# Generate with specific provider
tfplugindocs generate --provider-name example
```

### Directory Structure

Required for documentation generation:

```
examples/
├── provider/
│   └── provider.tf          # Provider configuration example
├── resources/
│   └── example_resource/
│       └── resource.tf      # Resource usage example
└── data-sources/
    └── example_data/
        └── data-source.tf   # Data source usage example

templates/
├── index.md.tmpl           # Provider landing page
└── resources/
    └── example_resource.md.tmpl  # Resource documentation template
```

### Example Templates

`templates/index.md.tmpl`:

```markdown
---
page_title: "Provider: Example"
description: |-
  The Example provider is used to interact with Example resources.
---

# Example Provider

The Example provider allows Terraform to manage Example resources.

## Example Usage

{{ tffile "examples/provider/provider.tf" }}

{{ .SchemaMarkdown | trimspace }}
```

## Makefile Automation

`GNUmakefile`:

```makefile
default: build

.PHONY: build
build:
	go build -o terraform-provider-example

.PHONY: install
install: build
	mkdir -p ~/.terraform.d/plugins/registry.terraform.io/yourusername/example/0.1.0/linux_amd64
	mv terraform-provider-example ~/.terraform.d/plugins/registry.terraform.io/yourusername/example/0.1.0/linux_amd64

.PHONY: test
test:
	go test -v -cover -timeout=120s -parallel=4 ./...

.PHONY: testacc
testacc:
	TF_ACC=1 go test -v -cover -timeout 120m ./...

.PHONY: fmt
fmt:
	gofmt -s -w -e .
	terraform fmt -recursive examples/

.PHONY: lint
lint:
	golangci-lint run

.PHONY: docs
docs:
	tfplugindocs generate

.PHONY: clean
clean:
	rm -f terraform-provider-example

.PHONY: generate
generate:
	go generate ./...
```

## GitHub Actions Workflows

### Complete Test Workflow

`.github/workflows/test.yml`:

```yaml
name: Tests

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  build:
    name: Build
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v4
        with:
          go-version-file: 'go.mod'
          cache: true
      - run: go mod download
      - run: go build -v .

  generate:
    name: Generate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v4
        with:
          go-version-file: 'go.mod'
          cache: true
      - run: go generate ./...
      - name: git diff
        run: |
          git diff --compact-summary --exit-code || \
            (echo; echo "Unexpected difference in directories after code generation. Run 'go generate ./...' command and commit."; exit 1)

  test:
    name: Unit Tests
    needs: build
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v4
        with:
          go-version-file: 'go.mod'
          cache: true
      - run: go mod download
      - run: go test -v -cover -timeout=120s -parallel=4 ./...

  acctest:
    name: Acceptance Tests
    needs: build
    runs-on: ubuntu-latest
    timeout-minutes: 60
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v4
        with:
          go-version-file: 'go.mod'
          cache: true
      - run: go mod download
      - env:
          TF_ACC: "1"
          EXAMPLE_API_KEY: ${{ secrets.EXAMPLE_API_KEY }}
        run: go test -v -cover -timeout 60m ./...
        timeout-minutes: 60
```

### Release Workflow

`.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  goreleaser:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-go@v4
        with:
          go-version-file: 'go.mod'
          cache: true
      - name: Import GPG key
        uses: crazy-max/ghaction-import-gpg@v6
        id: import_gpg
        with:
          gpg_private_key: ${{ secrets.GPG_PRIVATE_KEY }}
          passphrase: ${{ secrets.PASSPHRASE }}
      - name: Run GoReleaser
        uses: goreleaser/goreleaser-action@v5
        with:
          version: latest
          args: release --clean
        env:
          GPG_FINGERPRINT: ${{ steps.import_gpg.outputs.fingerprint }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Testing in CI

### Environment Variables

Set in GitHub repository secrets:
- `EXAMPLE_API_KEY` - API credentials for acceptance tests
- `GPG_PRIVATE_KEY` - For signing releases
- `PASSPHRASE` - GPG key passphrase

### Test Isolation

Use separate test accounts:

```bash
# Development
export EXAMPLE_API_ENDPOINT="https://dev.api.example.com"
export EXAMPLE_API_KEY="dev-key"

# CI/Testing
export EXAMPLE_API_ENDPOINT="https://test.api.example.com"
export EXAMPLE_API_KEY="${CI_API_KEY}"

# Production (DO NOT USE IN TESTS)
# Never run acceptance tests against production
```

## Local Development Workflow

```bash
# 1. Make changes
vim internal/provider/resource_example.go

# 2. Format code
make fmt

# 3. Run linter
make lint

# 4. Run unit tests
make test

# 5. Run acceptance tests (if API available)
make testacc

# 6. Generate documentation
make docs

# 7. Commit changes
git add .
git commit -m "feat: add new resource"

# 8. Push (triggers CI)
git push
```
