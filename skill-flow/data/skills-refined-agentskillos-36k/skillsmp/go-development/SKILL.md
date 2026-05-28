---
name: go-development
description: Go development practices and tooling. Use when working with Go code (*.go files, go.mod, go.sum). Activates for Go code style, testing, linting, concurrency patterns, and Go idioms.
allowed-tools: ["shell", "apply_patch", "read_file", "write_file", "update_plan"]
metadata:
  short-description: Go development best practices
---

# Go Development

**Read these reference files before proceeding:**
- `references/style.md` - Go code style guidelines
- `references/idioms.md` - Go conventions and best practices
- `references/concurrency.md` - Go thread safety and race conditions
- `references/testing.md` - Go test practices (table-driven, subtests)
- `references/tooling.md` - Go commands (go test, golangci-lint, etc.)
- `references/organization.md` - Go code structure and package design
- `references/performance.md` - Go optimization and profiling

**Also reference:**
- `~/.config/agent/domain/coding/safety.md` - Runtime and security safety
- `~/.config/agent/domain/testing/unit.md` - Unit test strategies

## Instructions

Apply all guidance from the reference files listed above when working with Go code. This skill covers:

- **Code style**: Follow Uber Go Style Guide, proper naming, imports, line length
- **Idioms**: Leverage Go conventions, zero values, error handling patterns
- **Concurrency**: Thread safety, mutex usage, race conditions
- **Testing**: Table-driven tests, subtests, testify/mock usage
- **Tooling**: go test, golangci-lint, gofumpt, golines commands
- **Organization**: Package structure, declaration ordering
- **Performance**: Memory efficiency, allocation reduction, profiling

All guidance from AGENT.md also applies (task tracking, problem-solving framework, code review priorities).
