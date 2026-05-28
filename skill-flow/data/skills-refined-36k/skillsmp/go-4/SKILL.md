---
name: go
description: "Develop Go applications using modern patterns, popular libraries, and idiomatic design. Activate when working with .go files, go.mod, go.sum, or user mentions Go, Golang, goroutines, channels, or Go libraries like gin, cobra, gorm."
---

# Go Development Skill

## Activation Triggers

- Working with `.go` files, `go.mod`, `go.sum`, `go.work`
- User mentions Go, Golang, or Go-specific terms
- Questions about Go libraries, frameworks, or tooling
- Concurrency patterns (goroutines, channels, context)

## Workflow: Research-First Approach

Before implementing, gather context from authoritative sources:

```
# Context7 query-docs for repo-specific docs
query-docs({ libraryId: "/gin-gonic/gin", query: "how to set up middleware" })
query-docs({ libraryId: "/uber-go/zap", query: "structured logging setup" })

# gh search code for real-world implementation examples
gh search code "ratelimit.New(" --language=go
gh search code "errgroup.WithContext(" --language=go

# For style/idiom questions
query-docs({ libraryId: "/uber-go/guide", query: "style guide patterns and idioms" })
```

## Notes

Repository routing table lives in `reference.md`.

## CLI Quick Reference

### Module Management
```bash
go mod init <module>       # Initialize module
go mod tidy                # Sync dependencies
go get <pkg>@latest        # Add/update dependency
go get <pkg>@v1.2.3        # Specific version
go mod download            # Download dependencies
go mod why <pkg>           # Why is pkg needed
go mod graph               # Dependency graph
```

### Build & Run
```bash
go build ./...             # Build all packages
go run .                   # Run current package
go install ./cmd/...       # Install binaries
go generate ./...          # Run go:generate directives
```

### Testing
```bash
go test ./...              # Run all tests
go test -v ./...           # Verbose output
go test -race ./...        # Race detector
go test -cover ./...       # Coverage summary
go test -coverprofile=c.out ./... && go tool cover -html=c.out  # Coverage HTML
go test -bench=. ./...     # Run benchmarks
go test -fuzz=FuzzXxx ./...  # Fuzz testing
go test -run=TestName      # Run specific test
go test -count=1           # Disable test caching
```

### Linting (golangci-lint)
```bash
golangci-lint run          # Run all linters
golangci-lint run --fix    # Auto-fix issues
golangci-lint linters      # List available linters
```

### Workspaces (multi-module)
```bash
go work init ./mod1 ./mod2 # Initialize workspace
go work use ./mod3         # Add module to workspace
go work sync               # Sync workspace
```

### Other Tools
```bash
go fmt ./...               # Format code
go vet ./...               # Static analysis
go doc <pkg>               # View documentation
go env                     # Environment variables
go version                 # Go version
```

## Files

- `reference.md` - Go 1.24+ features, project layout, Uber style highlights
- `cookbook/testing.md` - Table-driven tests, testify, mocking, benchmarks
- `cookbook/concurrency.md` - Goroutines, channels, context, errgroup
- `cookbook/patterns.md` - Functional options, DI, error handling
