---
name: go-table-driven-tests
description: Use this skill when writing or refactoring Go table-driven tests in Go, especially to reduce code duplication and improve maintainability.
---

# Go Table-Driven Tests

Table-driven tests are a Go testing idiom that allows you to define a table of test cases and iterate over it, reducing code duplication and making tests more maintainable.

## When to Use Table-Driven Tests

Use table-driven tests when:
- You find yourself copying and pasting test code.
- You're testing the same function/behavior with multiple inputs.
- You want to add more test cases without writing more test functions.
- Edge cases and boundary conditions need systematic coverage.

**Do NOT use for**: Completely unrelated test scenarios, or when each test requires substantially different setup/teardown logic.

## Basic Template (Slice Pattern)

This is the most common pattern in Go table-driven tests:

```go
func TestFunctionName(t *testing.T) {
    tests := []struct {
        name  string              // required: subtest name
        input Type                // function input
        want  Type                // expected output
        err   error               // expected error (nil for success)
    }{
        {
            name:  "simple case",
            input: "a/b/c",
            want:  "a,b,c",
        },
        {
            name:  "empty input",
            input: "",
            want:  "",
        },
        {
            name:  "invalid input",
            input: "!!!",
            want:  "",
            err:   ErrInvalid,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := FunctionName(tt.input)
            if !errors.Is(err, tt.err) {
                t.Errorf("FunctionName(%q) error = %v, want %v", tt.input, err, tt.err)
            }
            if got != tt.want {
                t.Errorf("FunctionName(%q) = %q, want %q", tt.input, got, tt.want)
            }
        })
    }
}
```

## Map Pattern (For Non-Deterministic Test Ordering)

Use a map when you want to ensure test independence:

```go
func TestFunctionName(t *testing.T) {
    tests := map[string]struct {
        input string
        want  string
    }{
        "simple case":   {input: "a/b/c", want: "a,b,c"},
        "empty input":   {input: "", want: ""},
        "trailing sep":  {input: "a/b/c/", want: "a,b,c"},
    }

    for name, tc := range tests {
        t.Run(name, func(t *testing.T) {
            got := FunctionName(tc.input)
            if got != tc.want {
                t.Errorf("FunctionName(%q) = %q, want %q", tc.input, got, tc.want)
            }
        })
    }
}
```

## Core Principles

- **One test function, many cases** - Define test cases in a slice or map and iterate with `t.Run()`.
- **Explicit naming** - Each case has a `name` field that becomes the subtest name.
- **Structured inputs** - Use struct fields for inputs, expected outputs, and configuration.
- **Helper functions** - Use `t.Helper()` in test helpers for proper line reporting.
- **Environment guards** - Skip integration tests when credentials are unavailable.