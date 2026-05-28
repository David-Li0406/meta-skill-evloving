---
title: Performance Benchmark Testing
impact: MEDIUM
impactDescription: Performance quantification
tags: testing, benchmark, performance
---

## Performance Benchmark Testing

Use benchmark tests to quantify performance.

**Basic Benchmark Test:**

```go
// user_test.go
func BenchmarkHashPassword(b *testing.B) {
    password := "mysecretpassword"
    for i := 0; i < b.N; i++ {
        HashPassword(password)
    }
}

func BenchmarkValidateEmail(b *testing.B) {
    email := "test@example.com"
    for i := 0; i < b.N; i++ {
        ValidateEmail(email)
    }
}
```

**Running Benchmark Tests:**

```bash
# Run all benchmarks
go test -bench=. ./...

# Run specific benchmark
go test -bench=BenchmarkHashPassword ./...

# Include memory allocation statistics
go test -bench=. -benchmem ./...

# Run multiple times for average
go test -bench=. -count=5 ./...
```

**Output Example:**

```
BenchmarkHashPassword-8     100     15234567 ns/op     4096 B/op     2 allocs/op
```

**Comparing Benchmarks:**

```bash
# Install benchstat
go install golang.org/x/perf/cmd/benchstat@latest

# Save benchmark results
go test -bench=. -count=10 > old.txt
# After code changes
go test -bench=. -count=10 > new.txt

# Compare results
benchstat old.txt new.txt
```

**Sub-benchmarks:**

```go
func BenchmarkEncode(b *testing.B) {
    sizes := []int{100, 1000, 10000}

    for _, size := range sizes {
        b.Run(fmt.Sprintf("size-%d", size), func(b *testing.B) {
            data := make([]byte, size)
            b.ResetTimer()
            for i := 0; i < b.N; i++ {
                Encode(data)
            }
        })
    }
}
```

**Avoiding Compiler Optimization:**

```go
var result string

func BenchmarkProcess(b *testing.B) {
    var r string
    for i := 0; i < b.N; i++ {
        r = Process(input)
    }
    result = r // Prevent being optimized away
}
```
