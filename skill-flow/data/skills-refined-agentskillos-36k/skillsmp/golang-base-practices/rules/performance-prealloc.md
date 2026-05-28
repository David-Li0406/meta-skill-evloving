---
title: Container Preallocation
impact: HIGH
impactDescription: Reduced memory allocations
tags: performance, prealloc, capacity
---

## Container Preallocation

Preallocate slice and map capacity when size is known.

**Slice Preallocation:**

```go
// Wrong: Dynamic resizing causes multiple allocations
func collect(n int) []int {
    var result []int  // len=0, cap=0
    for i := 0; i < n; i++ {
        result = append(result, i)  // Multiple resizes
    }
    return result
}

// Correct: Preallocate capacity
func collect(n int) []int {
    result := make([]int, 0, n)  // len=0, cap=n
    for i := 0; i < n; i++ {
        result = append(result, i)  // No resizing
    }
    return result
}

// When exact length is known, set len directly
func collect(n int) []int {
    result := make([]int, n)  // len=n, cap=n
    for i := 0; i < n; i++ {
        result[i] = i  // Direct assignment
    }
    return result
}
```

**Map Preallocation:**

```go
// Wrong: Frequent rehashing
m := make(map[string]int)  // Default capacity is very small
for i := 0; i < 10000; i++ {
    m[strconv.Itoa(i)] = i  // Multiple rehashes
}

// Correct: Estimate capacity
m := make(map[string]int, 10000)
for i := 0; i < 10000; i++ {
    m[strconv.Itoa(i)] = i  // No rehashing
}
```

**Building from Other Containers:**

```go
// Correct: Preallocate based on source container size
func transform(input []string) []int {
    result := make([]int, 0, len(input))
    for _, s := range input {
        if n, err := strconv.Atoi(s); err == nil {
            result = append(result, n)
        }
    }
    return result
}

// Map to slice
func keys(m map[string]int) []string {
    result := make([]string, 0, len(m))
    for k := range m {
        result = append(result, k)
    }
    return result
}
```

**Performance Impact:**

```
// Slice with 1000 elements
BenchmarkNoPrealloc-8     50000    30000 ns/op    40960 B/op    11 allocs/op
BenchmarkPrealloc-8      200000     8000 ns/op     8192 B/op     1 allocs/op

// Preallocation is 3.75x faster with 80% less memory
```

**Strategy When Size is Unknown:**

```go
// Use reasonable initial estimate
result := make([]Item, 0, 64)  // Usually sufficient for common cases

// Or estimate based on probability distribution
// If 90% of cases have fewer than 100 elements
result := make([]Item, 0, 100)
```
