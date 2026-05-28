Here’s an enhanced version of `testing-guidance.md` with a significantly expanded and improved **Fuzz Testing** section, including multiple practical examples ranging from basic to advanced use cases.
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
```

Run with:
```bash
go test -fuzz=FuzzParseJSONConfig -fuzztime=30s
```

### Fuzzing with Multiple Parameters
Use separate `f.Add` calls for different types.

```go
func FuzzCalculateExpression(f *testing.F) {
    f.Add("1+2*3", int64(7))
    f.Add("(10-4)/2", int64(3))
    f.Add("invalid", int64(0))

    f.Fuzz(func(t *testing.T, expr string, _ int64) { // ignore seed result
        result, err := Calculate(expr)
        if err == nil {
            // Basic sanity checks on successful evaluation
            if result < -1e9 || result > 1e9 {
                t.Fatalf("unreasonable result: %d", result)
            }
        }
    })
}
```

### Fuzzing Round-Trip Properties
Great for serializers, encoders, parsers.

```go
func FuzzMarshalUnmarshalJSON(f *testing.F) {
    f.Add(Config{Port: 8080, Host: "localhost"})
    f.Add(Config{Port: 0, Host: ""})
    f.Add(Config{Port: 65535, Host: "example.com"})

    f.Fuzz(func(t *testing.T, cfg Config) {
        data, err := json.Marshal(cfg)
        if err != nil {
            t.Fatalf("marshal failed: %v", err)
        }

        var decoded Config
        if err := json.Unmarshal(data, &decoded); err != nil {
            t.Fatalf("unmarshal failed: %v", err)
        }

        if !reflect.DeepEqual(cfg, decoded) {
            t.Fatalf("round-trip failed: got %+v, want %+v", decoded, cfg)
        }
    })
}
```

### Fuzzing Custom Types
You can fuzz your own structs directly.

```go
type MyStruct struct {
    ID   int
    Name string
    Tags []string
}

func FuzzProcessStruct(f *testing.F) {
    f.Add(MyStruct{ID: 42, Name: "test", Tags: []string{"a", "b"}})

    f.Fuzz(func(t *testing.T, s MyStruct) {
        // Ensure processing doesn't panic and respects invariants
        processed := Process(s)
        if processed.ID != s.ID {
            t.Fatalf("ID mutated")
        }
        if len(processed.Tags) > 100 { // example business rule
            t.Fatalf("too many tags after processing")
        }
    })
}
```

### Minimizing Noise and Improving Coverage
- Add many diverse seed values to guide the fuzzer toward interesting paths.
- Skip uninteresting inputs early to reduce noise:

```go
f.Fuzz(func(t *testing.T, data []byte) {
    if len(data) == 0 || len(data) > 10_000 {
        t.Skip("uninteresting size")
    }
    if !bytes.HasPrefix(data, []byte("{")) {
        t.Skip("not JSON-like")
    }
    // Proceed with actual test
    ParseJSONConfig(data)
})
```

### Running Fuzz Tests Effectively
```bash
# Run a specific fuzz test for 60 seconds
go test -fuzz=FuzzParseJSONConfig -fuzztime=60s

# Run all fuzz tests continuously until failure
go test -fuzz=. 

# Keep and inspect the corpus
# Crashing inputs go to testdata/fuzz/FuzzName
# Interesting inputs are minimized and saved
```

### When to Write Fuzz Tests
Prioritize fuzzing for:
- Public APIs that accept untrusted input (HTTP handlers, decoders, parsers)
- Serialization/deserialization code
- Complex business logic with many edge cases
- Anything that previously had subtle bugs found manually

Fuzz tests complement unit tests — they find what you didn’t think to test.

### Optional: Update SKILL.md to Reference the Expanded Section
You can add a quick note in the **Common Tasks & Workflow** section:

