---
name: go-dev
description: General Go development guide. Use when writing Go code, implementing best practices, formatting code, writing tests, using mocks, handling errors, or understanding Go coding conventions. Covers code style, testing patterns, dependency injection, interface design, and performance optimization. Project-agnostic guidelines applicable to any Go codebase.
---

# Go Development Guide

General-purpose Go development guidelines and best practices.

## Core Principles

- Write effective Go code (see `effective-go` skill for reference)
- Use the Go standard library whenever possible
- Limit line length to 120 characters
- Write testable code using interfaces and dependency injection
- Wrap OS operations in interfaces for mockability

## Code Organization

- Add interface verification after struct definitions: `var _ Interface = (*Struct)(nil)`
- Provide `NewStructName` constructors for all structs
- Always use dependency injection in constructors
- Pre-allocate collections when size is known

## Optional Types

Use `samber/mo` for safer nil handling:

```go
import "github.com/samber/mo"

type Config struct {
    Shell mo.Option[string]
}

if shell, ok := config.Shell.Get(); ok {
    // use shell
}
```

## Testing

- Use `testify` library with `require` for assertions
- Name tests descriptively: `Test_<DescriptiveStatement>`
- Use table-driven tests for multiple scenarios
- Generate mocks with `mockery` (moq template) - never edit manually
- Check errors by keywords, not full message matching

## Detailed References

**For all coding conventions and patterns:** See [Code Style Reference][code-style]

**For all testing conventions:** See [Test Style Reference][test-style]

[code-style]: references/code-style.md
[test-style]: references/test-style.md
