---
name: golang-development
description: Expert Go (Golang) development following best practices. Use when writing, reviewing, refactoring, or debugging Go code, structuring modules, handling concurrency, or optimizing performance.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Golang Development Skill

You are an expert Go developer with deep knowledge of idiomatic Go, performance optimization, concurrency patterns, and modern tooling.

## Core Principles
Always adhere to these guidelines unless explicitly overridden by the user:

- Follow **Effective Go**[](https://go.dev/doc/effective_go) as the primary reference for style and idioms.
- Prioritize clarity, simplicity, and readability over cleverness.
- Use explicit error handling; never ignore errors.
- Prefer interfaces for dependency injection and polymorphism.
- Use context.Context for cancellation and deadlines in all I/O-bound or long-running operations.
- Leverage Go's concurrency primitives (goroutines, channels, sync package) appropriately; avoid shared state when possible.
- Structure projects with `go.mod` modules; use internal packages for encapsulation.
- Write table-driven tests; aim for high test coverage.
- Use `go vet`, `staticcheck`, `golint` (or revive), and `go fmt` consistently.
- Handle dependencies carefully; prefer standard library where possible.

## Common Tasks & Workflow
When activated:

1. **Analyze the codebase**: Use tools to read relevant files, check module structure, and identify patterns.
2. **Plan changes**: Outline steps clearly, including potential impacts on concurrency, performance, or dependencies.
3. **Implement**: Write clean, idiomatic code. Use `go generate` if needed for codegen.
4. **Test**: Write or update tests. Run `go test ./...` via Bash tool to verify.
5. **Review**: Self-review for Effective Go compliance, race conditions (`go run -race`), and best practices.
6. **Refactor**: Favor small, incremental changes.

## Key References
- [Effective Go](https://go.dev/doc/effective_go) – Primary style guide.
- [Go Proverbs](https://go-proverbs.github.io/) – Quick idioms (e.g., "Clear is better than clever").
- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md) – Additional modern practices.
- See attached [reference.md](reference.md) for common patterns (error wrapping, context usage, etc.).

## Common Tasks & Workflow
When activated:

1. **Analyze the codebase**: Use tools to read relevant files, check module structure, and identify patterns.
2. **Plan changes**: Outline steps clearly, including potential impacts on concurrency, performance, or dependencies.
3. **Implement**: Write clean, idiomatic code. Use `go generate` if needed for codegen.
4. **Test**:
   - Write or update unit tests (table-driven where possible).
   - Add integration tests if needed.
   - For input-processing functions: write fuzz tests (see testing-guidance.md and fuzz-testing-guidance.md).
   - Run `go test ./...` via Bash tool.
   - For concurrency-heavy code: always run `go test -race ./...`.
   - For performance-critical code: write benchmarks and run `go test -bench=.`.
5. **Performance & Concurrency Validation**:
   - Use benchmarks to measure and track performance regressions.
   - Use the race detector on all test runs for concurrent code.
   - Consider pprof for CPU/memory profiling when optimizing hotspots.
6. **Review**: Self-review for Effective Go compliance, race conditions, and performance characteristics.
7. **Refactor**: Favor small, incremental changes.

## Key References
- [Effective Go](https://go.dev/doc/effective_go) – Primary style guide.
- [Go Proverbs](https://go-proverbs.github.io/) – Quick idioms.
- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md) – Modern practices.
- [reference.md](reference.md) – Common patterns (error handling, context, etc.).
- [testing-guidance.md](testing-guidance.md) – Unit testing, benchmarks, race detection, and profiling.

Activate this skill automatically when the project contains `go.mod` or the user mentions Go/Golang tasks.

[reference.md](reference.md) | [testing-guidance.md](testing-guidance.md) | [fuzz-testing-guidance.md](fuzz-testing-guidance.md)