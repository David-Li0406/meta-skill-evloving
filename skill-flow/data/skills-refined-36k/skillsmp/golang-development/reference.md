# Common Go Patterns & Snippets

## Error Handling
```go
if err != nil {
    return fmt.Errorf("failed to do something: %w", err)
}
```

# Context Usage

Always propagate context:

```go
Gofunc DoWork(ctx context.Context, ...) error {
    // Use ctx in all timeouts/cancellations
}
```

# Table-Driven Tests

```go
Gofunc TestSomething(t *testing.T) {
    tests := []struct {
        name string
        input string
        want  string
    }{ /* ... */ }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // test logic
        })
    }
}
```

# Concurrency Patterns

- Worker pool with channels
- Fan-out/fan-in
- Use sync.ErrGroup for coordinated goroutines