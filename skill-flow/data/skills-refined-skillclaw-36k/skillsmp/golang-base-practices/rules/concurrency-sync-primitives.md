---
title: sync Package Primitives Usage
impact: HIGH
impactDescription: Use synchronization primitives correctly
tags: concurrency, sync, mutex
---

## sync Package Primitives Usage

Use sync package synchronization primitives correctly.

**sync.Mutex - Mutual Exclusion Lock:**

```go
type SafeCounter struct {
    mu    sync.Mutex
    count int
}

func (c *SafeCounter) Inc() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *SafeCounter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}
```

**sync.RWMutex - Read-Write Lock:**

```go
type Cache struct {
    mu   sync.RWMutex
    data map[string]string
}

func (c *Cache) Get(key string) (string, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    v, ok := c.data[key]
    return v, ok
}

func (c *Cache) Set(key, value string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.data[key] = value
}
```

**sync.Once - Single Execution:**

```go
var (
    instance *DB
    once     sync.Once
)

func GetDB() *DB {
    once.Do(func() {
        instance = newDB()
    })
    return instance
}
```

**sync.Pool - Object Pool:**

```go
var bufferPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

func processData(data []byte) {
    buf := bufferPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufferPool.Put(buf)
    }()

    buf.Write(data)
    // ...
}
```

**sync.Map - Concurrent-Safe Map:**

```go
var cache sync.Map

cache.Store("key", "value")
if v, ok := cache.Load("key"); ok {
    fmt.Println(v)
}
```
