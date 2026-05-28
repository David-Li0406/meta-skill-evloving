# Go Testing Practices

## Table-Driven Tests

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -1, -1, -2},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        tt := tt // Capture for parallel tests
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            got := Add(tt.a, tt.b)
            if got != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.expected)
            }
        })
    }
}
```

## Test Helpers

```go
func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()
    db := // ... setup
    t.Cleanup(func() { db.Close() })
    return db
}
```

## Interface Mocking

```go
type MockEmailer struct {
    SentTo []string
}

func (m *MockEmailer) Send(to string, body string) error {
    m.SentTo = append(m.SentTo, to)
    return nil
}
```

## Benchmarking

```go
func BenchmarkProcess(b *testing.B) {
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        Process(data)
    }
}
```

## Commands

- `go test -race` - Race detector
- `go test -cover` - Coverage
- `go test -short` - Skip long tests
- `go test -fuzz` - Fuzzing (Go 1.18+)
