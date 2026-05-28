# Go Core References

## References

- [**Error Handling**](error-handling.md) - Error wrapping, custom errors, sentinel errors
- [**Concurrency Patterns**](concurrency-patterns.md) - Goroutines, channels, sync primitives

## Quick Checks

- [ ] Always handle errors explicitly
- [ ] Use `fmt.Errorf` with `%w` for wrapping
- [ ] Context for cancellation and timeouts
- [ ] Prefer channels for communication, mutexes for state
- [ ] Use `defer` for cleanup
