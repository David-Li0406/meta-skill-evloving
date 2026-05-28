# CI Pipeline Reference

Level 3 resource for validate-project skill - load when understanding CI pipeline details.

## Pipeline Stages

```text
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Build     │───>│    Test     │───>│   Validate  │───>│   Deploy    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Go Projects Pipeline

### Stage 1: Build

```yaml
- go generate ./...
- go build ./...
```

### Stage 2: Test

```yaml
- go test -race -cover ./...
```

### Stage 3: Validate

```yaml
- go mod tidy
- git diff --exit-code  # Fail if go.mod/go.sum changed
- golangci-lint run
```

### Stage 4: Deploy (conditional)

```yaml
- docker build -t image:tag .
- docker push image:tag
```

## Project-Specific CI

### nah

- Uses `make ci` target
- Runs envtest for controller tests
- Generates CRD manifests

### kinm

- Uses `make ci` target
- Runs API server tests

### mcp-oauth-proxy

- Standard Go CI
- Additional security scanning

### obot-entraid

- Go backend CI
- Frontend CI in ui/user

### obot-tools

- GPTScript validation
- Tool testing

## Common CI Failures

| Failure | Cause | Fix |
| --------- | ------- | ----- |
| "dirty repo" | Generated files not committed | Run `go generate && go mod tidy` |
| Lint errors | Code style violations | Run `golangci-lint run --fix` |
| Test failures | Broken tests | Review test output, fix issues |
| Build errors | Compilation issues | Check imports, types |

## Local CI Simulation

```bash
# Simulate full CI locally
make validate-ci

# Or manually:
go generate ./...
go mod tidy
go fmt ./...
golangci-lint run
go vet ./...
go test -short ./...
git status --porcelain  # Should be empty
```

## Makefile Targets

| Target | Purpose |
| -------- | --------- |
| `make build` | Compile binaries |
| `make test` | Run tests |
| `make validate` | Run linting |
| `make validate-ci` | Full CI simulation |
| `make ci` | Complete CI pipeline |
