---
title: golangci-lint Configuration
impact: HIGH
impactDescription: Comprehensive code checking
tags: lint, golangci-lint, quality
---

## golangci-lint Configuration

Use golangci-lint for comprehensive code quality checking.

**Installation:**

```bash
# macOS
brew install golangci-lint

# Or via go install
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

**Recommended Configuration (.golangci.yml):**

```yaml
run:
  timeout: 5m
  tests: true

linters:
  enable:
    # Default enabled
    - errcheck      # Check unhandled errors
    - gosimple      # Code simplification suggestions
    - govet         # Suspicious code checking
    - ineffassign   # Ineffective assignment checking
    - staticcheck   # Static analysis
    - unused        # Unused code checking

    # Additional recommended
    - gofmt         # Format checking
    - goimports     # Import formatting
    - revive        # golint replacement
    - misspell      # Spelling checking
    - unconvert     # Unnecessary type conversions
    - unparam       # Unused parameters
    - prealloc      # Slice preallocation suggestions
    - exportloopref # Loop variable references
    - bodyclose     # HTTP Body close checking
    - noctx         # HTTP request missing context
    - sqlclosecheck # SQL connection close checking
    - gocritic      # Code style suggestions
    - gosec         # Security checking

linters-settings:
  revive:
    rules:
      - name: exported
        arguments: [checkPrivateReceivers]
      - name: blank-imports
      - name: context-as-argument
      - name: error-return
      - name: error-strings
      - name: error-naming
      - name: increment-decrement
      - name: var-naming
      - name: package-comments
        disabled: true

  gocritic:
    enabled-tags:
      - diagnostic
      - style
      - performance

  gosec:
    excludes:
      - G104 # Unhandled errors (covered by errcheck)

issues:
  exclude-rules:
    - path: _test\.go
      linters:
        - gosec
        - errcheck
```

**Running:**

```bash
golangci-lint run ./...
```
