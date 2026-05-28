# Go Table-Driven Tests

This skill helps you write idiomatic Go table-driven tests following established patterns.

## What It Covers

The table-driven testing pattern appears throughout the Go ecosystem. This skill ensures tests are:

- **Maintainable** - Easy to add new test cases
- **Readable** - Clear test names and expectations
- **Idiomatic** - Follows Go community conventions

## Installation

### Claude Code

```bash
cp -r skills/go-table-driven-tests ~/.claude/skills/
```

### claude.ai

Add the `SKILL.md` file to your project knowledge or paste its contents into the conversation.

## Usage

Claude automatically uses this skill when you write or modify Go tests. Trigger phrases include:

- "Write tests for this function"
- "Add test cases for..."
- "Create a table-driven test"
- "Test this Go code"

## Example

Given a function to test:

```go
func Add(a, b int) int {
    return a + b
}
```

The skill generates:

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name    string
        a, b    int
        want    int
    }{
        {name: "positive numbers", a: 2, b: 3, want: 5},
        {name: "negative numbers", a: -1, b: -1, want: -2},
        {name: "zero", a: 0, b: 0, want: 0},
        {name: "mixed signs", a: -5, b: 10, want: 5},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Add(tt.a, tt.b); got != tt.want {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, got, tt.want)
            }
        })
    }
}
```

## License

MIT
