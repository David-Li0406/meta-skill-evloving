---
title: Advanced Static Checking
impact: HIGH
impactDescription: Deep code analysis
tags: lint, staticcheck, analysis
---

## Advanced Static Checking

Use staticcheck for deep static analysis.

**Installation:**

```bash
go install honnef.co/go/tools/cmd/staticcheck@latest
```

**Running:**

```bash
staticcheck ./...
```

**Common Checks:**

```go
// SA1: Various bug checks
// SA1000: Regex syntax error
regexp.MustCompile("[") // invalid regex

// SA1006: Printf arguments
fmt.Printf("%s", 123) // wrong type

// SA1012: nil context
context.WithValue(nil, key, val)

// SA2: Concurrency issues
// SA2000: sync.WaitGroup.Add called inside goroutine
go func() {
    wg.Add(1) // SA2000
    defer wg.Done()
}()

// SA4: Useless code
// SA4003: Pointless comparison
if x > 0 && x > 10 {} // x > 10 already implies x > 0

// SA4006: Value not used
x := 1
x = 2 // SA4006: first assignment to x never used

// SA5: Correctness issues
// SA5001: os.Exit called in defer
defer os.Exit(1) // SA5001

// SA9: Suspicious code structures
// SA9003: Empty branch
if condition {
} else {
    doSomething()
}
```

**Configuration File (staticcheck.conf):**

```toml
checks = ["all", "-ST1000", "-ST1003"]

[[exclude]]
checks = ["SA1019"]  # Ignore deprecated API warnings
```

**Integration with golangci-lint:**

```yaml
# .golangci.yml
linters:
  enable:
    - staticcheck

linters-settings:
  staticcheck:
    checks:
      - all
      - -SA1019  # Ignore deprecation warnings
```
