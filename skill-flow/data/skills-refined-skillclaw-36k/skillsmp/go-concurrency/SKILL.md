---
name: go-concurrency
description: Go concurrency patterns. Routes to specific patterns.
---

# Concurrency

## Route by Pattern
- Context cancellation → see [context/](context/)
- Goroutine leaks → see [goroutines/](goroutines/)
- Channel patterns → see [channels/](channels/)
- Sync primitives → see [sync/](sync/)

## Quick Check
- [ ] Every goroutine has exit path
- [ ] Context passed and checked
- [ ] Channels closed by sender only
- [ ] WaitGroup Add before go

## Common Pitfalls
1. Launching goroutines without shutdown mechanism
2. Not propagating context through call chains
3. Closing channels from receiver side
4. Using WaitGroup counter incorrectly

## Decision Tree
```
Need coordination? → Use context for cancellation
Need data flow? → Use channels
Need to wait? → Use sync.WaitGroup
Need mutual exclusion? → Use sync.Mutex
```

## References
- [Effective Go: Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go Concurrency Patterns](https://go.dev/blog/pipelines)
