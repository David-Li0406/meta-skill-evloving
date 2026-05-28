---
title: Use strconv Instead of fmt
impact: MEDIUM
impactDescription: Significant performance improvement
tags: performance, strconv, conversion
---

## Use strconv Instead of fmt

Use strconv instead of fmt for basic type conversions, for better performance.

**String to Integer:**

```go
// Wrong: Using fmt.Sprintf
s := fmt.Sprintf("%d", 42)

// Correct: Using strconv
s := strconv.Itoa(42)        // int -> string
s := strconv.FormatInt(42, 10) // int64 -> string

// Parsing
i, err := strconv.Atoi("42")       // string -> int
i64, err := strconv.ParseInt("42", 10, 64) // string -> int64
```

**String to Float:**

```go
// Wrong
s := fmt.Sprintf("%f", 3.14)

// Correct
s := strconv.FormatFloat(3.14, 'f', -1, 64)

// Parsing
f, err := strconv.ParseFloat("3.14", 64)
```

**Boolean Conversion:**

```go
// Wrong
s := fmt.Sprintf("%t", true)

// Correct
s := strconv.FormatBool(true)

// Parsing
b, err := strconv.ParseBool("true")
```

**Performance Comparison (Benchmark Results):**

```
BenchmarkFmtSprintf-8     10000000    120 ns/op    16 B/op    2 allocs/op
BenchmarkStrconvItoa-8    50000000     30 ns/op     3 B/op    1 allocs/op
```

strconv is 4x faster than fmt, with 50% less memory allocation.

**When to Use fmt:**

```go
// Complex formatting still uses fmt
s := fmt.Sprintf("User %s (ID: %d) has %d items", name, id, count)

// Debug output
fmt.Printf("%+v\n", obj)
fmt.Printf("%#v\n", obj) // Go syntax representation

// Formatted output
fmt.Fprintf(w, "Status: %d\n", code)
```

**Conversions in Loops:**

```go
// Wrong: Repeated conversion in loop
for _, id := range ids {
    key := fmt.Sprintf("user:%d", id)  // Allocates each time
}

// Correct: Use strconv
for _, id := range ids {
    key := "user:" + strconv.Itoa(id)  // More efficient
}
```
