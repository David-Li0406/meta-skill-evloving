---
title: Slice and Map Operations
impact: MEDIUM
impactDescription: Efficient data operations
tags: idiomatic, slice, map
---

## Slice and Map Operations

Use slices and maps correctly.

**Slice Preallocation:**

```go
// Wrong: Frequent resizing
func collect(n int) []int {
    var result []int
    for i := 0; i < n; i++ {
        result = append(result, i)
    }
    return result
}

// Correct: Preallocate capacity
func collect(n int) []int {
    result := make([]int, 0, n)
    for i := 0; i < n; i++ {
        result = append(result, i)
    }
    return result
}
```

**Slice Copying:**

```go
// Shallow copy
src := []int{1, 2, 3}
dst := make([]int, len(src))
copy(dst, src)

// Or use append
dst := append([]int(nil), src...)
```

**Map Initialization:**

```go
// Preallocate when size is known
m := make(map[string]int, 100)

// Check key existence
if v, ok := m["key"]; ok {
    fmt.Println(v)
}

// Delete key
delete(m, "key")
```

**Delete While Iterating:**

```go
// Wrong: Modify during iteration
for k := range m {
    if shouldDelete(k) {
        delete(m, k) // Undefined behavior
    }
}

// Correct: Collect then delete
var toDelete []string
for k := range m {
    if shouldDelete(k) {
        toDelete = append(toDelete, k)
    }
}
for _, k := range toDelete {
    delete(m, k)
}
```

**nil Slice vs Empty Slice:**

```go
var s1 []int        // nil slice, len=0, cap=0
s2 := []int{}       // empty slice, len=0, cap=0
s3 := make([]int,0) // empty slice, len=0, cap=0

// All can be appended to
s1 = append(s1, 1) // Works fine

// JSON serialization differs
json.Marshal(s1) // null
json.Marshal(s2) // []
```
