# Go Testing Guidance

## Unit & Integration Testing
- Prefer table-driven tests for clarity and coverage.
- Use `t.Parallel()` on independent tests to speed up test runs.
- Mock dependencies with interfaces; avoid external tools unless necessary.
- Aim for meaningful test names: `TestFunctionUnderTest_Condition_ExpectedBehavior`.

Example:
```go
func TestParseConfig(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    Config
        wantErr bool
    }{
        {"valid minimal", `{"port": 8080}`, Config{Port: 8080}, false},
        {"invalid json", `{"port": `, Config{}, true},
    }

    for _, tt := range tests {
        tt := tt // capture range variable
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            got, err := ParseConfig([]byte(tt.input))
            if (err != nil) != tt.wantErr {
                t.Fatalf("wantErr %v, got %v", tt.wantErr, err)
            }
            if !reflect.DeepEqual(got, tt.want) {
                t.Errorf("got %+v, want %+v", got, tt.want)
            }
        })
    }
}
```

## Benchmarking (Performance Testing)
- Write benchmarks for performance-critical functions.
- Use `testing.B` and reset timers appropriately.
- Run with `-benchmem` to track allocations.
- Compare versions using `benchstat` (install via `go install golang.org/x/perf/cmd/benchstat@latest`).

Example:
```go
func BenchmarkProcessData(b *testing.B) {
    data := prepareTestData() // setup outside the loop
    b.ResetTimer()
    
    for i := 0; i < b.N; i++ {
        ProcessData(data)
    }
}
```

Running benchmarks:
```bash
go test -bench=. -benchmem -run=^$
# For comparisons:
go test -bench=. -count=10 > old.txt
# ... make changes ...
go test -bench=. -count=10 > new.txt
benchstat old.txt new.txt
```

## Concurrency / Race Detection
- Always run the race detector on concurrent code:
  ```bash
  go test -race ./...
  ```
- Also run `go run -race` for manual testing of main programs.
- Common pitfalls to watch for:
  - Shared mutable state without synchronization
  - Closing channels multiple times
  - Sending on nil or closed channels

## Profiling (When Needed)
For deeper performance investigation:
- CPU: `go test -cpuprofile=cpu.prof`
- Memory: `go test -memprofile=mem.prof`
- Block (contention): `go test -blockprofile=block.prof`
- Visualize with:
  ```bash
  go tool pprof cpu.prof
  # Inside pprof: web, list, top
  ```

## Fuzz Testing (Go 1.18+)

Fuzz testing is excellent for finding edge cases, crashes, panics, and unexpected behavior in input-parsing or processing functions.

### Basic Fuzz Test
Start with a seed corpus of valid and interesting inputs.

```go
func FuzzParseJSONConfig(f *testing.F) {
    // Seed corpus: common valid and invalid cases
    f.Add([]byte(`{"port": 8080}`))
    f.Add([]byte(`{"host": "localhost", "port": 3000}`))
    f.Add([]byte(`invalid json`))
    f.Add([]byte(``)) // empty

    f.Fuzz(func(t *testing.T, data []byte) {
        cfg, err := ParseJSONConfig(data)
        if err == nil {
            // If parsing succeeded, validate invariants
            if cfg.Port < 0 || cfg.Port > 65535 {
                t.Fatalf("invalid port parsed: %d", cfg.Port)
            }
            if cfg.Host == "" {
                t.Fatalf("empty host on successful parse")
            }
        }
        // No need to check err != nil cases explicitly — crashes will fail the fuzz run
    })
}

Run with: `go test -fuzz=FuzzParseJSONConfig -fuzztime=30s`

