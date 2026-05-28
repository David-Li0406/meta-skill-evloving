# Tokio Runtime References

## References

- [**Async Patterns**](async-patterns.md) - Spawning, joining, timeouts, select
- [**Synchronization**](synchronization.md) - Mutex, RwLock, channels, semaphores

## Quick Checks

- [ ] Use #[tokio::main] for async entry point
- [ ] Spawn tasks for concurrent work
- [ ] Use tokio::select! for racing futures
- [ ] Prefer tokio::sync over std::sync in async code
- [ ] Graceful shutdown with signal handling
