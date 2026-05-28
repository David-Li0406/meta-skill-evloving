# Golang Base Practices

A comprehensive Go development best practices skill for Claude Code, covering frameworks, ORM, database migrations, DDD architecture, error handling, concurrency patterns, testing, and linting.

## Overview

This skill provides 53 curated best practice rules organized into 9 categories, referenced from:
- [Effective Go](https://go.dev/doc/effective_go)
- [Google Go Style Guide](https://google.github.io/styleguide/go/)
- [Uber Go Style Guide](https://github.com/uber-go/guide)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)

## Installation

```bash
npx add-skill cexll/golang-base-practices-skills
```

## Rule Categories

| Priority | Category | Impact | Rules |
|----------|----------|--------|-------|
| 1 | Framework Selection | CRITICAL | 4 rules |
| 2 | Database & ORM | CRITICAL | 5 rules |
| 3 | DDD Project Structure | HIGH | 6 rules |
| 4 | Error Handling | HIGH | 6 rules |
| 5 | Concurrency Patterns | HIGH | 7 rules |
| 6 | Idiomatic Go | MEDIUM | 11 rules |
| 7 | Testing Practices | CRITICAL | 7 rules |
| 8 | Performance Optimization | MEDIUM | 2 rules |
| 9 | Lint & Toolchain | MEDIUM | 5 rules |

## Quick Reference

### 1. Framework Selection
- **Gin** for simple projects and REST APIs
- **Go-Kratos** for complex microservices with gRPC/HTTP dual protocols
- Middleware patterns and graceful shutdown handling

### 2. Database & ORM
- GORM initialization, hooks, and transaction patterns
- Goose for version-controlled migrations
- Connection pool tuning for production

### 3. DDD Project Structure
```
internal/
├── domain/          # Business entities, value objects, repositories
├── application/     # Use cases, DTOs, service interfaces
├── infrastructure/  # External implementations (DB, cache, MQ)
└── interfaces/      # HTTP handlers, gRPC services
```

### 4. Error Handling
- Wrap errors with context using `fmt.Errorf("...: %w", err)`
- Define sentinel errors for expected conditions
- Custom error types for domain-specific errors
- Unified API error response format

### 5. Concurrency Patterns
- Goroutine lifecycle management with context cancellation
- Channel patterns: fan-out, fan-in, timeout
- Channel buffer sizing (prefer 0 or 1)
- errgroup for parallel task coordination
- Race detection with `go test -race`

### 6. Idiomatic Go
- Naming conventions (packages, variables, interfaces)
- Small interface design (Interface Segregation)
- Functional options pattern for flexible APIs
- Proper defer usage and zero value utilization
- Type embedding guidelines

### 7. Testing Practices
- **99% test coverage target** for production code
- Table-driven tests for comprehensive coverage
- Interface-based mocking with mockgen
- Integration tests with testcontainers
- Benchmark tests for performance validation

### 8. Performance Optimization
- Use `strconv` instead of `fmt` for type conversion (4x faster)
- Preallocate slices and maps when size is known

### 9. Lint & Toolchain
- golangci-lint with recommended configuration
- gofmt/goimports for consistent formatting
- go vet, staticcheck, and revive for static analysis

## Core Principles

1. **KISS** - Keep it simple, avoid over-engineering
2. **YAGNI** - Only implement what is currently needed
3. **Explicit over Implicit** - Code intent should be clear
4. **Handle All Errors** - Never ignore error returns
5. **99% Test Coverage** - Foundation for high-quality code

## Usage

Claude will automatically reference these rules when:
- Creating new Go projects or microservices
- Building API interfaces (REST/gRPC)
- Performing database operations and migrations
- Conducting code reviews and refactoring
- Optimizing performance and concurrency
- Improving test coverage

## File Structure

```
golang-base-practices/
├── SKILL.md           # Skill definition and quick reference
├── README.md          # This file
└── rules/             # 53 individual rule files
    ├── framework-*.md
    ├── db-*.md
    ├── ddd-*.md
    ├── error-*.md
    ├── concurrency-*.md
    ├── idiomatic-*.md
    ├── testing-*.md
    ├── performance-*.md
    └── lint-*.md
```

Each rule file contains:
- Rule explanation and importance (impact level)
- Bad example with analysis
- Good example with explanation
- Additional context and references

## License

MIT
