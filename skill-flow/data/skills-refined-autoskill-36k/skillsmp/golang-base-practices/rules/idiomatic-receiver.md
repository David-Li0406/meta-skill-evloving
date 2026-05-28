---
title: Receiver Naming and Selection
impact: HIGH
impactDescription: Consistent method design
tags: idiomatic, receiver, method
---

## Receiver Naming and Selection

Choose and name method receivers correctly.

**Receiver Naming:**

```go
// Correct: 1-2 letters, abbreviation of type name
func (c *Client) Send(msg Message) error {}
func (r *Reader) Read(p []byte) (n int, err error) {}
func (b *Buffer) Write(p []byte) (n int, err error) {}

// Wrong: Do not use this, self, me
func (this *Client) Send(msg Message) error {}  // Wrong
func (self *Reader) Read(p []byte) error {}     // Wrong

// Be consistent: Use same receiver name for all methods of a type
func (c *Client) Connect() error {}
func (c *Client) Disconnect() error {}
func (c *Client) Send(msg Message) error {}
```

**When to Use Value Receiver:**

```go
// Value receiver is appropriate when:
// - The method does not modify the receiver
// - Small, immutable structs
// - Basic types (int, string)
// - map, func, chan types
// - Slices that don't need reslicing

type Point struct {
    X, Y float64
}

func (p Point) Distance(q Point) float64 {
    return math.Sqrt((p.X-q.X)*(p.X-q.X) + (p.Y-q.Y)*(p.Y-q.Y))
}
```

**When to Use Pointer Receiver:**

```go
// Pointer receiver is appropriate when:
// - The method modifies the receiver
// - Contains sync.Mutex or similar sync fields
// - Large structs (avoid copy overhead)
// - Contains pointer fields
// - Implements unmarshaling or similar methods

type Counter struct {
    mu    sync.Mutex
    count int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}
```

**Do Not Mix Receivers:**

```go
// Wrong: Mixing value and pointer receivers on same type
type T struct{}
func (t T) Method1() {}   // Value receiver
func (t *T) Method2() {}  // Pointer receiver - inconsistent!

// Correct: Use pointer receiver consistently
func (t *T) Method1() {}
func (t *T) Method2() {}
```
